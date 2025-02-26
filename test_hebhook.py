import requests

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

def send_test_message():
    message = {
        'text': ':rotating_light: Teste de notificação de segurança no Slack!'
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code == 200:
        print("Mensagem de teste enviada com sucesso ao Slack!")
    else:
        print(f"Erro ao enviar mensagem. Código: {response.status_code}, Resposta: {response.text}")

send_test_message()
