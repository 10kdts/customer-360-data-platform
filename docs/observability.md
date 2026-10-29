# Observabilidade e SLOs

| Indicador | SLO | Alerta |
|---|---:|---:|
| Freshness diário | até 07:00 | após 07:30 |
| Completude de fontes | 100% | qualquer fonte ausente |
| Duplicidade de event_id em Silver | 0% | maior que 0% |
| Registros em quarentena | abaixo de 1% | acima de 2% |
| Reconciliação pedidos × pagamentos | diferença menor que 0,1% | acima de 0,5% |
| Disponibilidade do pipeline | 99% mensal | duas falhas consecutivas |

Métricas técnicas mínimas: duração por etapa, linhas lidas/escritas/rejeitadas, lag de evento, tamanho da DLQ, último sucesso e versão de contrato observada.
