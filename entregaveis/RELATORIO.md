# Relatório — Métricas de Pipeline CI/CD no GitHub Actions

> **Status:** em construção. Seções 1–2 escritas e commitadas **antes** da primeira execução
> do experimento (run-01), para que o histórico git comprove que as hipóteses foram
> formuladas a priori. Demais seções serão preenchidas após as execuções (SPEC T3–T6).

## 1. Contexto e objetivo

Este experimento instrumenta um pipeline CI/CD no GitHub Actions para medir, com dados
reais de execução, o desempenho, a estabilidade e os gargalos do processo. O pipeline
roda lint (ruff) e testes (pytest) sobre um módulo Python pequeno, é executado ao menos
12 vezes com variações controladas (cache, falhas, volume de testes, teste lento,
paralelismo) e tem suas métricas coletadas via API REST do GitHub por script Python
próprio ([`scripts/collect_metrics.py`](../scripts/collect_metrics.py)).

## 2. Hipóteses iniciais

Formuladas antes de qualquer execução; serão confrontadas com os dados na seção 7.

- **H1 (cache):** habilitar `cache: pip` reduzirá a duração do step `Install dependencies`
  em mais de 50% nos runs com cache hit, em comparação aos runs sem cache.
- **H2 (paralelismo):** com jobs paralelos, o tempo total do workflow será próximo ao do
  job mais lento (`test`); com `needs: lint`, o tempo total será aproximadamente a soma
  dos dois jobs — ou seja, o paralelismo economiza ~tempo do job `lint`.
- **H3 (volume de testes):** aumentar a quantidade de testes de ~16 para ~120 terá impacto
  pequeno (< 10%) na duração total, pois o overhead fixo (provisionar runner, checkout,
  setup Python, instalar dependências) domina o tempo do pipeline.
- **H4 (gargalo):** o step mais caro do pipeline, sem cache, será `Install dependencies`.
- **H5 (teste lento):** um único teste com `time.sleep(30)` aumentará a duração total em
  ~30 s, tornando-se o maior contribuinte individual do job `test`.

## 3. Metodologia

_(a preencher após as execuções — SPEC T6, seção 6.2)_

### 3.1 Projeto-alvo e pipeline

### 3.2 Tabela de execuções

### 3.3 Coleta

## 4. Resultados

_(a preencher)_

## 5. Respostas às perguntas de análise

_(a preencher)_

## 6. Resultados inesperados

_(a preencher)_

## 7. Hipóteses × observado

_(a preencher)_

## 8. Limitações do experimento

_(a preencher)_

## 9. Conclusão

_(a preencher)_
