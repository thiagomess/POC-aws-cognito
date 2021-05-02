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

        response = client.confirm_forgot_password(
            ClientId=os.environ['clientId'],
            SecretHash=get_secret_hash(event['email']),
            Username=event['email'],
            ConfirmationCode=event['code'],
            Password=event['password']
        )
        print(response)

        return returnResponse(200, 'Senha alterada com sucesso', response)

    except client.exceptions.UserNotFoundException as e:
        return returnResponse(404, 'Usuario nao existe.')

    except client.exceptions.ExpiredCodeException as e:
        return returnResponse(422, 'Codigo de validação expirado.')

    except client.exceptions.UserNotConfirmedException as e:
        return returnResponse(422, 'Usuario ainda nao confirmado.')

    except client.exceptions.InvalidPasswordException as e:
        return returnResponse(422, 'Senha nao atende aos requisitos minimos.')

    except client.exceptions.CodeMismatchException as e:
        return returnResponse(422, 'Codigo de validação inválido.')

    except Exception as e:
        print(str(e))
        return returnResponse(500, "Algo deu errado, tente novamente")