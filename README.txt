# Monitoramento de Reputação de IPs com AbuseIPDB

Este projeto automatiza a análise de reputação de IPs utilizando a API do AbuseIPDB, com notificações por e-mail e Slack, e bloqueio de IPs suspeitos via iptables.

## Pré-requisitos

- Python 3.x
- Bibliotecas: `requests`, `csv`, `json`, `matplotlib`, `smtplib`
- Conta no AbuseIPDB para obter uma API Key.

## Instalação

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/monitoramento-ip.git
cd monitoramento-ip
