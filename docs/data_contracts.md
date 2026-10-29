# Contratos e evolução de schema

## Compatibilidade

- Alteração aditiva opcional: compatível, incremento minor.
- Novo campo obrigatório: incompatível, incremento major.
- Mudança de tipo ou semântica: incompatível, incremento major.
- Remoção de campo: somente após período de descontinuação.

## Evento comportamental

Todo evento contém `event_id`, `schema_version`, `event_time`, `ingested_at`, `anonymous_id` e `session_id`. Propriedades específicas permanecem dentro de `properties`.

## Tempo e atraso

Regras de jornada utilizam `event_time`. Freshness e atraso utilizam `ingested_at - event_time`. Eventos com atraso superior à janela de watermark continuam armazenados em Bronze e podem ser reprocessados.

## Dead-letter queue

Mensagens incompatíveis ou inválidas devem ser enviadas a uma DLQ com payload, erro, versão, tópico, partição, offset e horário da falha. Correções são republicadas com novo evento técnico, sem apagar a evidência original.
