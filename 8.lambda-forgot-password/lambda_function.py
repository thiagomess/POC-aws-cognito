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
        response = client.forgot_password(
            ClientId=os.environ['clientId'],
            SecretHash=get_secret_hash(event['email']),
            Username=event['email']
        )

        print(response)

        return returnResponse(200, 'Codigo para redefinir a senha enviado com sucesso.', response)

    except client.exceptions.UserNotFoundException as e:
        return returnResponse(404, 'Usuario nao existe.')

    except client.exceptions.CodeDeliveryFailureException as e:
        return returnResponse(422, 'Falha ao enviar codigo de verificação.')

    except client.exceptions.UserNotConfirmedException as e:
        return returnResponse(422, 'Usuario ainda não confirmado.')

    except Exception as e:
        print(str(e))
        return returnResponse(500, "Algo deu errado, tente novamente")
