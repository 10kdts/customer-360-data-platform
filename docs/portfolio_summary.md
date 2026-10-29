# Resumo para entrevista

## Pitch

Esta plataforma consolida cinco domínios em uma visão Customer 360 usando padrões de arquitetura moderna: contratos versionados, Bronze imutável, Silver validada, Gold governada, deduplicação de eventos, resolução de identidade, dbt, Airflow, observabilidade e LGPD.

## Evidências

- 3.566 registros recebidos em Bronze.
- 2.509 registros publicados em Silver.
- 99 clientes consolidados em Gold.
- Cinco eventos duplicados detectados e removidos.
- Falhas controladas enviadas à quarentena.
- Pipeline determinístico e reexecutável.

## Decisões de especialista

- Separação entre tempo do evento e tempo de ingestão.
- Contrato semântico versionado para eventos.
- Identidade resolvida por referências normalizadas.
- PII removida ou mascarada na camada Gold.
- SLOs de freshness, completude, duplicidade e reconciliação.
- Runbook com verificação, rollback e escalonamento.
