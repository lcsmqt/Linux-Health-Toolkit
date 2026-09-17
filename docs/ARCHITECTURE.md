# Arquitetura

```mermaid
flowchart LR
    CLI[CLI] --> Agg[Agregador]
    Agg --> CPU[Coletor CPU]
    Agg --> MEM[Coletor Memória]
    Agg --> DISK[Coletor Disco]
    Agg --> SVC[Coletor Serviços]
    Agg --> AUTH[Coletor Auth]
    Agg --> NET[Coletor Rede]
    Agg --> REP[Relatórios JSON / MD / HTML]
```

Cada coletor é independente. Falha em um coletor (ex.: systemd ausente no Windows) não impede o snapshot: a seção fica vazia e um aviso pode ser registrado.

Limiares vêm de `config/config.yaml`. A CLI apenas orquestra coleta e renderização.
