# Linux System Health Toolkit

Um toolkit profissional de monitoramento e relatórios de saúde de sistemas Linux, projetado para demonstrar conhecimento prático de administração de sistemas, automação e observabilidade.

## Problema

Administradores de sistemas e equipes de TI precisam de visibilidade rápida sobre o estado de um servidor: uso de CPU, memória, disco, serviços falhos, falhas de autenticação e portas em escuta. Ferramentas comerciais são caras; este projeto oferece uma alternativa open-source, leve e fácil de implantar.

## Funcionalidades

- Coleta de métricas de CPU, RAM e disco
- Listagem de serviços ativos e falhos
- Detecção de falhas de autenticação (auth.log)
- Inventário de interfaces de rede e portas em escuta
- Relatórios em JSON, Markdown e HTML
- Agendamento via cron
- Configuração via arquivo YAML / variáveis de ambiente
- Logging estruturado

## Arquitetura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Coletores  │────▶│  Agregador   │────▶│ Relatórios  │
│  (CPU, RAM, │     │  (Health     │     │ (JSON, MD,  │
│   Disco,    │     │   Snapshot)  │     │  HTML)      │
│   Rede...)  │     └──────────────┘     └─────────────┘
└─────────────┘
```

## Tecnologias

- **Python 3.11+**: linguagem principal, tipagem estática
- **psutil**: coleta de métricas de sistema de forma portável
- **PyYAML**: configuração
- **Jinja2**: templates de relatórios HTML
- **pytest**: testes automatizados

## Instalação

```bash
git clone https://github.com/lcsmqt/linux-system-health-toolkit.git
cd linux-system-health-toolkit
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Configuração

Copie o arquivo de exemplo e ajuste:

```bash
cp .env.example .env
cp config/config.example.yaml config/config.yaml
```

Variáveis de ambiente (`.env`):

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `HEALTH_CONFIG` | Caminho do arquivo YAML | `config/config.yaml` |
| `HEALTH_LOG_LEVEL` | Nível de log | `INFO` |
| `HEALTH_OUTPUT_DIR` | Diretório de relatórios | `reports/` |

## Uso

```bash
# Relatório completo no terminal
python -m src.cli report

# Exportar JSON
python -m src.cli report --format json --output reports/health.json

# Exportar HTML
python -m src.cli report --format html --output reports/health.html

# Apenas métricas de CPU/RAM
python -m src.cli snapshot --section cpu,memory
```

## Testes

```bash
pytest -v
```

## Estrutura do Projeto

```
linux-system-health-toolkit/
├── src/
│   ├── collectors/     # Coletores de métricas
│   ├── reports/        # Geradores de relatório
│   ├── config.py       # Carregamento de configuração
│   ├── cli.py          # Interface de linha de comando
│   └── models.py       # Modelos de dados
├── tests/
├── docs/
├── scripts/            # Scripts bash de agendamento
├── config/
├── .github/workflows/
├── requirements.txt
└── README.md
```

## Segurança

- Sem acesso remoto; executa apenas no host local
- Não coleta senhas nem conteúdo de arquivos de usuário
- Logs de autenticação são lidos em modo somente leitura
- Configuração nunca contém credenciais

## Roadmap

- [ ] Alertas por e-mail/webhook quando limiares são ultrapassados
- [ ] Exportação para Prometheus
- [ ] Dashboard web local (opcional)

## Lições Aprendidas

Este projeto demonstra coleta de métricas de SO, parsing de logs, geração de relatórios, configuração desacoplada e testes de código de infraestrutura.

## Autor

Lucas Mesquita  
GitHub: https://github.com/lcsmqt
