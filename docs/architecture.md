# Arquitetura

## Domínios de origem

- CRM: cadastro e preferências do cliente.
- Commerce: pedidos e itens.
- Payments: autorizações, capturas e estornos.
- Web/App: eventos comportamentais.
- Support: tickets, motivos e satisfação.

## Camadas

### Bronze

Preserva payload, schema version, origem, horário do evento, horário de ingestão e identificador de execução.

### Silver

Aplica tipos, deduplicação, validações, normalização e quarentena. Mantém dados no nível mais detalhado disponível.

### Gold

Publica entidades e métricas de consumo: Customer 360, jornada, pedidos, pagamentos, suporte e indicadores de qualidade.

## Equivalência cloud

| Ambiente local | AWS | Azure | GCP |
|---|---|---|---|
| MinIO | S3 | ADLS Gen2 | Cloud Storage |
| Redpanda | MSK/Kinesis | Event Hubs | Pub/Sub |
| PostgreSQL | RDS | Azure Database | Cloud SQL |
| Airflow | MWAA | Data Factory/Managed Airflow | Cloud Composer |
| DuckDB/dbt | Athena/Redshift | Synapse/Databricks | BigQuery |

O projeto local não pretende simular todos os detalhes de uma nuvem. Ele preserva os principais contratos e limites arquiteturais para facilitar a migração.
