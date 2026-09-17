# Guia de entrevista — Toolkit de Saúde do Sistema Linux

## 1. O que o projeto faz

Coleta métricas locais (CPU, RAM, disco, serviços, falhas de login, interfaces e portas) e gera relatórios em Markdown, JSON ou HTML.

## 2. Por que foi criado

Para demonstrar administração Linux, automação e observabilidade de forma executável — o tipo de ferramenta que um time de suporte/infra usaria internamente.

## 3. Arquitetura

Coletores pequenos → agregador (`HealthSnapshot`) → renderizadores. Configuração YAML + `.env`. Sem banco de dados.

## 4. Tecnologias principais

Python, psutil, PyYAML, Jinja2, pytest, Bash/cron.

## 5. Decisões técnicas

- `psutil` em vez de parsear `/proc` na mão: portabilidade (Linux e Windows para testes).
- Coletores isolados para testar parsing de log sem precisar de um servidor real.
- Relatórios em três formatos: humano (MD/HTML) e máquina (JSON).

## 6. Banco de dados

Não há. Persistência é arquivo de relatório.

## 7. Segurança

Somente host local, leitura de logs, sem credenciais, sem varrer a rede de terceiros.

## 8. Problema mais difícil

Parsear `auth.log` com formatos diferentes (syslog clássico vs ISO-8601) e lidar com permissão negada em `net_connections`.

## 9. Como foi resolvido

Dois regex, leitura das últimas linhas, e `try/except` em APIs privilegiadas retornando lista vazia.

## 10–11. 20 perguntas e respostas sugeridas

1. **Por que psutil?** — API estável sobre `/proc` e WMI; reduz código específico de SO.
2. **O que é load average?** — média de processos em execução/espera em 1/5/15 min (Linux).
3. **Diferença CPU lógica e física?** — threads vs núcleos.
4. **Como o cron entra nisso?** — `scripts/install-cron.sh` agenda o relatório diário.
5. **O que acontece no Windows?** — CPU/RAM/disco/rede funcionam; systemd e auth.log ficam vazios.
6. **Como evitar falso positivo de disco?** — ignoramos tmpfs, overlay, proc.
7. **O que é um serviço failed?** — unidade systemd cujo estado ativo é `failed`.
8. **Por que não enviar dados para a nuvem?** — privacidade, custo zero, execução air-gapped.
9. **Como testar sem root?** — fixtures de log e mocks; métricas psutil não exigem root.
10. **O que você loga?** — eventos da CLI (nível INFO), não dumps de senha.
11. **Como configurar limiares?** — YAML `thresholds`.
12. **O que é um snapshot?** — ponto no tempo com todas as métricas.
13. **Como serializar dataclass?** — `dataclasses.asdict`.
14. **Por que JSON além de Markdown?** — integração com outras ferramentas.
15. **Risco de `net_connections`?** — pode exigir privilégio; tratamos AccessDenied.
16. **Como provar que o código é seu?** — explicar o fluxo CLI → aggregator → collector.
17. **Como adicionaria alertas?** — comparar limiares e POST em webhook (roadmap).
18. **O que é observabilidade?** — métricas + logs para entender o sistema.
19. **Por que type hints?** — clareza e menos bugs em entrevistas/CI.
20. **Como o CI funciona?** — GitHub Actions instala deps, ruff e pytest.

## 12. Alterações de live-coding

- Adicionar limiar de swap.
- Filtrar portas apenas em `127.0.0.1`.
- Contar falhas de auth por IP.
- Exportar CSV.
- Falhar o processo (`exit 1`) se houver warning (modo Nagios).
