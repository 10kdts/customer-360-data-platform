# Customer 360 Data Platform

[![CI](https://github.com/10kdts/customer-360-data-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/10kdts/customer-360-data-platform/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Projeto de portfólio orientado a Engenharia, Arquitetura e Especialista de Dados.

## Objetivo

Construir uma plataforma moderna que consolide clientes, pedidos, pagamentos, navegação e atendimento em uma visão Customer 360 confiável, governada e preparada para analytics.

O projeto deverá responder:

- Qual é o valor total e o comportamento de cada cliente?
- Quais jornadas antecedem compra, abandono ou churn?
- Como garantir identidade única entre sistemas diferentes?
- Quais dados estão atrasados, incompletos ou inconsistentes?
- Como reprocessar eventos sem duplicação?
- Como aplicar privacidade, linhagem e controle de acesso?

## Arquitetura planejada

```text
APIs + PostgreSQL + eventos JSON
              |
              v
     Ingestão batch e streaming
              |
              v
       Data Lake / Bronze
              |
              v
      Silver / dados validados
              |
              v
   Gold / Customer 360 + métricas
        |                 |
        v                 v
   Analytics/API     Qualidade e lineage
```

## Stack planejada

- Python e SQL
- PostgreSQL e MinIO como ambiente local
- Apache Kafka/Redpanda para eventos
- Apache Airflow para orquestração
- dbt para transformação, testes e documentação
- DuckDB para desenvolvimento analítico local
- OpenMetadata ou documentação equivalente para governança
- Docker Compose e GitHub Actions
- Prometheus/Grafana ou métricas estruturadas para observabilidade

## Diferenciais demonstrados

- Arquitetura batch e streaming
- Medallion architecture: Bronze, Silver e Gold
- Resolução de identidade e regras de sobrevivência
- CDC e cargas incrementais
- Data contracts e schema evolution
- Qualidade, freshness, lineage e observabilidade
- LGPD, classificação e mascaramento
- Infraestrutura reproduzível e decisões arquiteturais documentadas

## Roadmap

| Fase | Entrega | Status |
|---|---|---|
| 1 | Escopo, arquitetura e estrutura | Concluída |
| 2 | Geradores de fontes e contratos de dados | Concluída |
| 3 | Ambiente local: PostgreSQL, MinIO e Redpanda | Concluída |
| 4 | Ingestão batch, eventos e idempotência | Concluída |
| 5 | Transformações dbt e Customer 360 | Concluída |
| 6 | Orquestração, qualidade e observabilidade | Concluída |
| 7 | Governança, segurança e LGPD | Concluída |
| 8 | CI/CD, demonstração e publicação | Publicado; destaque pendente |

## Princípios

1. Toda entrada possui contrato versionado.
2. Dados brutos são imutáveis.
3. Reprocessamentos não geram duplicidade.
4. Falhas ficam observáveis e recuperáveis.
5. Dados pessoais recebem classificação e tratamento explícito.
6. Métricas de negócio possuem definição e proprietário.

## Status

MVP completo e validado localmente. O repositório inclui dados sintéticos determinísticos, pipeline reexecutável Bronze/Silver/Gold, modelo Customer 360, contratos, testes automatizados, infraestrutura local e documentação operacional.

**Evidência da última execução:** 3.566 registros Bronze, 2.509 Silver, 99 clientes Gold, seis registros em quarentena e cinco eventos duplicados removidos.

## Executar localmente

```bash
python -m src.customer360.generate
python -m src.customer360.pipeline
python -m unittest discover -s tests -v
```

Consulte também a [arquitetura](docs/architecture.md), o [runbook](docs/runbook.md), as [decisões arquiteturais](docs/adr/001-medallion-and-event-time.md) e o [resumo para portfólio](docs/portfolio_summary.md).
