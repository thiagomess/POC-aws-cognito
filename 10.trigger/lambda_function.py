import os


def lambda_handler(event, context):
    if event['userPoolId'] == os.environ['user-pool-id']:
        if event['triggerSource'] == "CustomMessage_SignUp":
            event['response']['emailSubject'] = "Bem-vindo"
            event['response']['emailMessage'] = SIGNUP.format(event['request']['userAttributes']['name'],
                                                              event['request']['codeParameter'])

        if event['triggerSource'] == "CustomMessage_ResendCode":
            event['response']['emailSubject'] = "Novo código de confirmação"
            event['response']['emailMessage'] = RESEND_CODE.format(event['request']['userAttributes']['name'],
                                                                   event['request']['codeParameter'])

        if event['triggerSource'] == "CustomMessage_ForgotPassword":
            event['response']['emailSubject'] = "Recuperação de senha"
            event['response']['emailMessage'] = FORGOT_PASSWORD.format(event['request']['userAttributes']['name'],
                                                                       event['request']['codeParameter'])

    return event


SIGNUP = '''<html>
    <body>
        <td width="480" align="center" style="font-family: Arial; color: #000000; text-align: left; line-height: 18px;">
            <span style="font-weight: bold; font-size: 14px;">Olá, {0}</span><br />
            <br />
            <span style="font-size: 14px;">
                 Confirme seu cadastro inserindo o código:
                <b>{1}</b> .
            </span>
          
        </td>
    </body>
</html>'''

RESEND_CODE = '''<html>
    <body>
        <td width="480" align="center" style="font-family: Arial; color: #000000; text-align: left; line-height: 18px;">
            <span style="font-weight: bold; font-size: 14px;">Olá, {0}</span><br />
            <br />
            <span style="font-size: 14px;">
                Você solicitou um novo código de confirmação. Confirme seu cadastro inserindo o código:
                <b>{1}</b>.
            </span>
        </td>
    </body>
</html>'''

FORGOT_PASSWORD = '''<html>
    <body>
        <td width="480" align="center" style="font-family: Arial; color: #000000; text-align: left; line-height: 18px;">
            <span style="font-weight: bold; font-size: 14px;">Olá, {0} </span><br />
            <br />
            <span style="font-size: 14px;">
                Você solicitou a redefinição de senha. Insira o código: <b>{1}</b>  para cadastrar a sua nova senha.
            </span>
        </td>
    </body>
</html>'''
