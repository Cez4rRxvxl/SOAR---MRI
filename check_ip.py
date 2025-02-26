import requests
import json
import csv
import os
import smtplib
import matplotlib.pyplot as plt
from datetime import datetime

# Configuração de variáveis de ambiente para segurança
API_KEY = "56c966680200cf7ec5d93fedcbf493df5d168a9eb120c1e21642e64789e9bbfd38c903da96719680"
EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'zezinhorpa123@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'zezinhorpa123')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT', 'deathgunjp2014@gmail.com')
SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL', 'https://hooks.slack.com/services/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')

# Verificação de variáveis de ambiente
if not all([API_KEY, EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENT, SLACK_WEBHOOK_URL]):
    print("Erro: Algumas configurações essenciais estão ausentes. Verifique as variáveis de ambiente.")
    exit(1)

# Caminhos dos arquivos de log
CSV_FILE = 'ip_report.csv'
JSON_FILE = 'ip_log.json'
LOG_EXECUTION_FILE = 'cron_execution_log.txt'
IP_FILE = 'ips_suspeitos.txt'

# Criar arquivo de IPs se não existir
if not os.path.exists(IP_FILE):
    with open(IP_FILE, 'w') as f:
        f.write("8.8.8.8\n")  # Exemplo de IP para inicializar o arquivo
    print(f"Arquivo {IP_FILE} criado. Adicione os IPs suspeitos.")

# Função para salvar logs no formato JSON
def save_log_json(ip, isp, domain, country, abuse_score, total_reports, last_report):
    log_entry = {
        "IP": ip,
        "ISP": isp,
        "Domain": domain if domain else 'N/A',
        "Country": country if country else 'N/A',
        "Abuse Score": abuse_score,
        "Total Reports": total_reports,
        "Last Report": last_report
    }
    with open(JSON_FILE, 'a') as file:
        json.dump(log_entry, file, indent=4)
        file.write(",\n")

# Função para salvar logs no formato CSV
def save_log_csv(ip, isp, domain, country, abuse_score, total_reports, last_report):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['IP', 'ISP', 'Domain', 'Country', 'Abuse Score', 'Total Reports', 'Last Report'])
        writer.writerow([ip, isp, domain, country, abuse_score, total_reports, last_report])

# Função para enviar e-mail de alerta em caso de IP suspeito
def send_alert(ip, abuse_score):
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECIPIENT:
        print("Erro: Configuração de e-mail ausente.")
        return

    subject = f"Alerta de segurança para o IP: {ip}"
    message = f"Foi detectado um IP suspeito com score de abuso {abuse_score}. Verifique imediatamente."
    msg = f"Subject: {subject}\n\n{message}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECIPIENT, msg)
        server.quit()
        print(f"Alerta enviado para {EMAIL_RECIPIENT}")
    except smtplib.SMTPAuthenticationError:
        print("Erro de autenticação SMTP. Verifique as credenciais do e-mail.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

# Função para verificar a reputação de um IP
def check_ip_reputation(ip):
    url = 'https://api.abuseipdb.com/api/v2/check'
    params = {'ipAddress': ip, 'maxAgeInDays': 90}
    headers = {'Accept': 'application/json', 'Key': API_KEY}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        isp = data['data']['isp']
        domain = data['data'].get('domain', 'N/A')
        country = data['data']['countryCode']
        abuse_score = data['data']['abuseConfidenceScore']
        total_reports = data['data']['totalReports']
        last_report = data['data']['lastReportedAt']

        print(f"\nConsultando o IP: {ip}")
        print(f"  - ISP: {isp}")
        print(f"  - Domínio: {domain}")
        print(f"  - País: {country if country else 'N/A'}")
        print(f"  - Pontuação de abuso: {abuse_score}")
        print(f"  - Total de denúncias: {total_reports}")
        print(f"  - Última denúncia: {last_report}\n")

        save_log_json(ip, isp, domain, country, abuse_score, total_reports, last_report)
        save_log_csv(ip, isp, domain, country, abuse_score, total_reports, last_report)

        if abuse_score > 50:
            print(f'O IP {ip} possui uma pontuação de abuso alta: {abuse_score}. Tomando ação!')
            send_alert(ip, abuse_score)
            send_slack_notification(ip, abuse_score)
            block_ip(ip)
        else:
            print(f'O IP {ip} é seguro. Pontuação de abuso: {abuse_score}')
    else:
        print(f"Erro ao consultar API para o IP {ip}: {response.status_code}, {response.text}")

# Função para enviar notificação para o Slack
def send_slack_notification(ip, abuse_score):
    if not SLACK_WEBHOOK_URL:
        print("Erro: URL do Webhook do Slack não está configurada.")
        return

    message = {
        'text': f':rotating_light: Alerta de Segurança!\nIP: {ip}\nScore de Abuso: {abuse_score}\nVerifique imediatamente!'
    }
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code == 200:
        print(f"Notificação enviada ao Slack para o IP: {ip}")
    else:
        print(f"Falha ao enviar notificação para o Slack. Código: {response.status_code}, Resposta: {response.text}")

# Função para bloquear IPs via iptables
def block_ip(ip):
    check = os.system(f'sudo iptables -C INPUT -s {ip} -j DROP')
    if check != 0:
        os.system(f'sudo iptables -A INPUT -s {ip} -j DROP')
        print(f'IP {ip} bloqueado com sucesso.')
    else:
        print(f'IP {ip} já está bloqueado.')

# Função para registrar a execução do script via cron
def log_execution():
    with open(LOG_EXECUTION_FILE, "a") as log_file:
        log_file.write(f"Script executado em: {datetime.now()}\n")

def generate_report_chart():
    ips = []
    scores = []

    try:
        with open(CSV_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Pular cabeçalho
            for row in reader:
                ips.append(row[0])  # Coluna IP
                scores.append(int(row[4]))  # Coluna Abuse Score

        # Geração do gráfico
        plt.figure(figsize=(10, 6))
        plt.bar(ips, scores, color='red')
        plt.xlabel('IPs')
        plt.ylabel('Pontuação de Abuso')
        plt.title('Análise de Segurança de IPs')
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig('ip_report_chart.png')
        plt.show()

    except FileNotFoundError:
        print("Nenhum relatório encontrado para gerar gráficos.")
    except Exception as e:
        print(f"Erro ao gerar o gráfico: {e}")

# Função para processar a lista de IPs ignorando comentários
def load_ip_list(filename):
    ip_list = []
    with open(filename, 'r') as file:
        for line in file:
            # Remove espaços extras e ignora linhas vazias ou que começam com '#'
            ip = line.split('#')[0].strip()
            if ip:
                ip_list.append(ip)
    return ip_list

# Chamando a função para carregar IPs corretamente
ips = load_ip_list('ips_suspeitos.txt')

for ip in ips:
    check_ip_reputation(ip)


# Função principal para processar a lista de IPs
if __name__ == "__main__":
    log_execution()
    try:
        with open(IP_FILE, 'r') as file:
            for ip in file.readlines():
                check_ip_reputation(ip.strip())

        generate_report_chart()

    except FileNotFoundError:
        print(f"Erro: O arquivo '{IP_FILE}' não foi encontrado.")
