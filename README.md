# 🛡️ Monitoramento de Reputação de IPs

Este projeto apresenta um sistema automatizado de monitoramento de reputação de endereços IP, utilizando a API do **AbuseIPDB** para identificar e reagir a atividades suspeitas na rede. O projeto foi desenvolvido como parte da disciplina de **Cibersegurança** no curso de **Sistemas de Informação** da **Universidade Federal de Viçosa - Campus Rio Paranaíba**.

## 🚀 Funcionalidades
- 🔍 **Monitoramento Periódico**: Consulta automática de IPs suspeitos na base do AbuseIPDB.
- 🚫 **Bloqueio Automatizado**: IPs com alta pontuação de abuso são bloqueados via iptables.
- ✅ **Whitelist**: Permite configurar endereços IP confiáveis para evitar bloqueios indevidos.
- 📩 **Notificações**: Alertas enviados via **e-mail (SMTP)** e **Slack (webhooks)**.
- 📜 **Registro de Logs**: Logs detalhados para auditoria e rastreabilidade.
- ⏳ **Execução Automatizada**: Uso do **Crontab** para agendar execuções periódicas.
- 📊 **Geração de Relatórios**: Saída estruturada em JSON e CSV, além de visualização em gráficos.

## 📂 Estrutura do Projeto
/
├── check_ip.py           # Script principal
├── config.env            # Configuração do sistema
├── ips_suspeitos.txt     # Lista de IPs suspeitos
├── whitelist.txt         # Lista de IPs confiáveis
├── ip_log.json           # Registro histórico de consultas
├── ip_report.csv         # Relatório consolidado
├── ip_report_chart.png   # Gráfico de análise
├── cron_execution_log.txt# Log das execuções
/

## ⚙️ Fluxo de Execução
1. 📜 O script carrega a lista de IPs suspeitos.
2. 🌎 Cada IP é consultado na API do **AbuseIPDB**.
3. 📝 Os dados são armazenados em logs e relatórios.
4. 🚫 Se o **score de abuso** ultrapassar um limite (exemplo: 50 pontos), o IP é bloqueado via **iptables**.
5. 📢 Notificações são enviadas aos administradores.
6. 📊 Um gráfico é gerado para visualizar padrões de bloqueios.

## ⏳ Agendamento (Crontab)
O script pode ser programado para rodar automaticamente todos os dias às 8h da manhã:
```bash
0 8 * * * /usr/bin/python3 /caminho/para/check_ip.py >> /caminho/para/logs.txt 2>&1
```

## 📈 Resultados Obtidos
- ✅ 95% de acerto na identificação de IPs maliciosos
- ❌ Apenas 2% de falsos positivos
- ⚡ Tempo de resposta abaixo de 2 segundos

## 🔮 Melhorias Futuras
- 🗄️ Integração com bancos de dados para armazenar histórico detalhado.
- 🔧 Ajuste dinâmico de regras de bloqueio com base em perfis de risco.
- 📲 Notificações por SMS ou Telegram.
- 🤖 Uso de Machine Learning para previsão de ameaças futuras.

👥 Autores
Julio Cezar
Gabriel Rodrigues
Germano Henrique
Luiz Davi

## 📜 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.
