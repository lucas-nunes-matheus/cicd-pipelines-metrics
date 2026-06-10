# Entrega — Experimento de Métricas de Pipeline CI/CD

**Aluno:** Lucas Matheus Nunes
**Repositório:** <https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics>

Esta pasta é o ponto de entrada da entrega: todos os artefatos exigidos no enunciado
estão listados e linkados abaixo.

## Entregáveis

| Entregável (enunciado) | Localização |
|---|---|
| Relatório técnico em Markdown | [RELATORIO.md](RELATORIO.md) |
| Base de dados gerada (CSV) | [dados/metrics.csv](dados/metrics.csv) · [dados/steps.csv](dados/steps.csv) |
| Gráficos produzidos | [graficos/](graficos/) — ver lista abaixo |
| Evidências das execuções reais | [evidencias/](evidencias/) + links na tabela abaixo |
| Arquivo YAML do GitHub Actions | [../.github/workflows/ci.yml](../.github/workflows/ci.yml) |
| Script de coleta das métricas | [../scripts/collect_metrics.py](../scripts/collect_metrics.py) |
| Script de geração dos gráficos | [../scripts/generate_charts.py](../scripts/generate_charts.py) |
| Como reproduzir o experimento | [../README.md](../README.md) |
| Especificação do experimento | [../SPEC.md](../SPEC.md) |

## Gráficos

1. [Tempo total do pipeline por execução](graficos/01_tempo_total_por_execucao.png)
2. [Tempo por job em cada execução](graficos/02_tempo_por_job.png)
3. [Taxa de sucesso e falha](graficos/03_taxa_sucesso_falha.png)
4. [Quantidade de testes × duração do pipeline](graficos/04_testes_vs_duracao.png)
5. [Efeito do cache no step Install dependencies](graficos/05_cache_vs_sem_cache.png) (extra)
6. [Sequencial × paralelo](graficos/06_sequencial_vs_paralelo.png) (extra)

## Execuções reais (13 runs)

| Run | Run ID (link) | Commit | Status | Variação |
|---|---|---|---|---|
| run-01 | [27306176271](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27306176271) | `a89386f` | success | Baseline |
| run-02 | [27307336491](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27307336491) | `c8e6392` | success | Repetição baseline |
| run-03 | [27307722430](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27307722430) | `830c4e2` | success | Cache pip (cold) |
| run-04 | [27307871395](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27307871395) | `1d17c8e` | success | Cache quente (hit) |
| run-05 | [27307988407](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27307988407) | `a8c64b5` | **failure** | Teste quebrado proposital |
| run-06 | [27308063457](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27308063457) | `2010bdc` | success | Correção (volta ao verde) |
| run-07 | [27308157078](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27308157078) | `8181867` | success | 65 testes (~4×) |
| run-08 | [27308281107](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27308281107) | `c3355ac` | success | 137 testes (~9×) |
| run-09 | [27308435165](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27308435165) | `263a5a7` | success | Teste lento (sleep 30 s) |
| run-10 | [27308620254](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27308620254) | `867a7b1` | success | Jobs sequenciais |
| run-11 | [27308812787](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27308812787) | `5762953` | success | Jobs paralelos |
| run-12 | [27309062606](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27309062606) | `7c62627` | success | Repetição paralela |
| run-13 | [27309113580](https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/runs/27309113580) | `ef62cc7` | success | Estado final limpo |

Lista completa de execuções:
<https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics/actions/workflows/ci.yml>
