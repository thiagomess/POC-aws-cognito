import json
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
            'data': json.loads(json.dumps(data, default=str))
        }
    }


def lambda_handler(event, context):
    client = boto3.client('cognito-idp')

    try:
        response = client.admin_get_user(
            UserPoolId=os.environ['user-pool-id'],
            Username=event['email']
        )

        print(response)

        return returnResponse(200, 'Usuario encontrado com sucesso.', response)

    except client.exceptions.UserNotFoundException as e:
        return returnResponse(404, 'Usuario não existe.')

    except Exception as e:
        print(str(e))
        return returnResponse(500, "Algo deu errado, tente novamente")
