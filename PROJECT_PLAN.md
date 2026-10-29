# Plano de execução

## Fase 1 — Fundação

- [x] Definir problema e usuários da plataforma
- [x] Definir arquitetura evolutiva
- [x] Selecionar stack local e equivalente cloud
- [x] Definir princípios de confiabilidade
- [x] Criar estrutura inicial do repositório
- [x] Registrar primeira decisão arquitetural

## Fase 2 — Fontes e contratos

- [x] Gerar CRM, pedidos, pagamentos e tickets de suporte
- [x] Gerar eventos de navegação em JSON Lines
- [x] Criar contratos JSON Schema versionados
- [x] Simular duplicidade, atraso e eventos fora de ordem
- [x] Criar catálogo e classificação inicial
- [x] Testar determinismo e integridade dos geradores

## Fase 3 — Infraestrutura local

- [x] Criar Docker Compose
- [x] Configurar PostgreSQL transacional
- [x] Configurar MinIO para Bronze/Silver/Gold
- [x] Configurar Redpanda e tópicos
- [x] Adicionar health checks

## Fase 4 — Ingestão

- [x] Implementar ingestão local incremental/reexecutável
- [x] Implementar contrato para eventos
- [x] Criar envelopes com metadados técnicos
- [x] Garantir deduplicação e quarentena
- [x] Implementar replay controlado

## Fase 5 — Transformação

- [x] Criar projeto dbt
- [x] Padronizar clientes entre fontes
- [x] Implementar resolução de identidade
- [x] Criar modelo Customer 360
- [x] Criar métricas de jornada e valor

## Fase 6 — Operação

- [x] Criar DAG do Airflow
- [x] Implementar testes de qualidade e freshness
- [x] Criar SLAs e SLOs
- [x] Especificar métricas e alertas
- [x] Criar runbook de incidentes

## Fase 7 — Governança

- [x] Classificar dados pessoais
- [x] Aplicar mascaramento e minimização
- [x] Documentar lineage e ownership
- [x] Documentar solicitação fictícia de exclusão LGPD
- [x] Criar regras de acesso por classificação

## Fase 8 — Publicação

- [x] Criar CI/CD e testes integrados
- [x] Criar evidência de execução
- [x] Revisar README para recrutadores
- [x] Publicar no GitHub
- [x] Fixar ou destacar no perfil

## Critério de conclusão

Uma pessoa deverá conseguir subir o ambiente, gerar dados, executar ingestão e transformações, observar falhas controladas, reconstruir a visão Customer 360 e verificar qualidade e lineage seguindo apenas a documentação.
