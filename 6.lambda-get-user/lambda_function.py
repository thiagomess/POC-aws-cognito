import boto3


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
        response = client.get_user(
            AccessToken=event['access_token']
        )

        print(response)

        return returnResponse(200, 'Usuario encontrado com sucesso.', response)

    except client.exceptions.UserNotFoundException as e:
        return returnResponse(404, 'Usuario nao existe.')

    except client.exceptions.UserNotConfirmedException as e:
        return returnResponse(422, 'Usuário não confirmado.')
    except client.exceptions.NotAuthorizedException as e:
        return returnResponse(401, 'Access Token expirado.')

    except Exception as e:
        print(str(e))
        return returnResponse(500, "Algo deu errado, tente novamente")
