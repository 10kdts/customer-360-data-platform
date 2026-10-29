# ADR 001 — Arquitetura Medallion e tempo do evento

- Status: aceito
- Data: 2026-10-29

## Contexto

As fontes possuem frequências diferentes e eventos podem chegar atrasados ou fora de ordem. A solução precisa permitir replay e auditoria sem sobrescrever evidências.

## Decisão

Adotar camadas Bronze, Silver e Gold. Bronze será imutável. Processamento comportamental usará `event_time` para regras de negócio e `ingested_at` para observabilidade. Eventos repetidos serão identificados por `event_id` e versão do produtor.

## Consequências

- Replay e investigação ficam mais seguros.
- Atraso de eventos pode ser medido explicitamente.
- Transformações precisam tratar watermark e janela de atraso.
- O armazenamento aumenta, pois dados brutos e tratados coexistem.
