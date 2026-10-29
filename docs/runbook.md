# Runbook: reprocessar Customer 360

**Owner:** Customer Platform | **Frequência:** conforme necessidade  
**Última atualização:** 2026-10-29

## Finalidade

Recuperar uma execução com atraso, contrato inválido ou falha parcial sem duplicar dados ou perder evidências.

## Pré-requisitos

- [ ] Acesso ao ambiente e logs da execução.
- [ ] Manifesto e arquivos Bronze preservados.
- [ ] Incidente registrado com período e fontes afetadas.

## Procedimento

### 1. Executar validação local

```bash
python -m src.customer360.pipeline --source data/sample --storage storage-replay
```

**Esperado:** `run_report.json` com contagens e quarentena.  
**Se falhar:** validar manifesto, contrato e codificação dos arquivos.

### 2. Comparar contagens

Compare Bronze, Silver, Gold e execução anterior. Confirme que deduplicação explica a diferença de eventos.

### 3. Reexecutar transformações

```bash
dbt build --select customer_360+
```

**Esperado:** testes de unicidade, obrigatoriedade e relacionamentos aprovados.  
**Se falhar:** não publique Gold; mantenha a execução anterior.

## Verificação

- [ ] Nenhum `event_id` duplicado em Silver.
- [ ] Customer 360 possui uma linha por cliente.
- [ ] PII permanece ausente ou mascarada em Gold.
- [ ] Freshness e reconciliação estão dentro do SLO.

## Rollback

Restaure o apontamento de consumo para a última versão Gold aprovada. Bronze não deve ser apagado. Mantenha a execução defeituosa isolada para investigação.

## Escalonamento

| Situação | Responsável | Ação |
|---|---|---|
| Vazamento ou PII em Gold | Segurança e DPO | Suspender acesso e iniciar resposta a incidente |
| Pagamentos divergentes | Finance Data Owner | Bloquear publicação e reconciliar |
| Contrato incompatível | Owner da fonte | Restaurar versão anterior ou criar migração |
| Duas falhas consecutivas | Data Platform On-call | Abrir incidente de alta prioridade |
