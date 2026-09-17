# Guia de aprendizado

Este projeto é um **check-up do computador**, como um exame médico: mede CPU (batimentos), memória (energia), disco (espaço) e tenta ver se algum “órgão” (serviço) falhou.

## Pastas

- `src/collectors`: cada arquivo pergunta uma coisa ao sistema operacional.
- `src/aggregator.py`: junta as respostas.
- `src/reports`: transforma os dados em texto/HTML/JSON.
- `src/cli.py`: o comando que você roda no terminal.
- `tests`: provas automatizadas para não quebrar o check-up.

## Conceitos

- **Processo**: programa em execução.
- **Porta em escuta**: o programa está esperando conexão naquela porta.
- **auth.log**: diário do Linux sobre logins.
- **cron**: despertador do Linux para rodar scripts.

Leia primeiro `src/cli.py`, depois `aggregator.py`, depois um coletor (`cpu.py`).
