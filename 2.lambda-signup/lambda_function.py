import boto3
import os
import hmac
import hashlib
import base64


def get_secret_hash(username):
    msg = username + os.environ['clientId']
    dig = hmac.new(str(os.environ['clientSecret']).encode('utf-8'),
                   msg=str(msg).encode('utf-8'), digestmod=hashlib.sha256).digest()
    d2 = base64.b64encode(dig).decode()
    return d2


def returnResponse(code, message, data=None):
    return {
        'statusCode': code,
        'body': {
            'message': message,
            'data': data
        }
    }


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')

    try:

        response = client.sign_up(
            ClientId=os.environ['clientId'],
            SecretHash=get_secret_hash(event['email']),
            Username=event['email'],
            Password=event['password'],
            UserAttributes=[
                {
                    'Name': 'name',
                    'Value': event['name']
                },
                {
                    'Name': 'email',
                    'Value': event['email']
                },
                {
                    'Name': 'phone_number',
                    'Value': event['phone_number']
                },
                {
                    'Name': 'custom:accepted_terms',
                    'Value': event['accepted_terms']
                }
            ],
            ClientMetadata={
                'username': event['name']
            },
        )

        print(response)

        return returnResponse(200, 'Conta criada com sucesso.', response)

    except client.exceptions.UsernameExistsException as e:
        return returnResponse(422, 'Já existe uma conta com este mesmo email.')

    except client.exceptions.InvalidPasswordException as e:
        return returnResponse(422, 'A senha não atende aos requisitos minimos.')

    except client.exceptions.InvalidParameterException as e:
        return returnResponse(422, 'Parametros Invalidos.')

    except client.exceptions.CodeDeliveryFailureException as e:
        return returnResponse(422, 'Falha ao enviar codigo de verificação.')

    except client.exceptions.LimitExceededException as e:
        return returnResponse(422, 'Limite de email diario atingido.')

    except Exception as e:
        print(str(e))
        return returnResponse(500, "Algo deu errado, tente novamente")
