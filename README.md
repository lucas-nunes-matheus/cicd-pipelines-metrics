# cicd-pipelines-metrics

> **👉 Professor: a entrega completa está em [`entregaveis/`](entregaveis/)** — relatório,
> base de dados, gráficos e evidências das execuções, com índice em
> [`entregaveis/README.md`](entregaveis/README.md).

Experimento prático de medição e análise de um pipeline CI/CD no GitHub Actions:
um projeto Python pequeno (módulo `calculadora`, pytest + ruff) é executado ≥12 vezes
com variações controladas (cache, falhas, volume de testes, teste lento, paralelismo);
as métricas reais são coletadas via API REST do GitHub por script próprio e analisadas
em gráficos e relatório técnico. A especificação completa está em [`SPEC.md`](SPEC.md).

## Estrutura

```
├── .github/workflows/ci.yml   # pipeline CI (lint + test, artifact com report de testes)
├── src/calculadora/           # módulo-alvo do pipeline
├── tests/                     # testes pytest (ponto de expansão do experimento)
├── scripts/
│   ├── collect_metrics.py     # coleta via API do GitHub -> CSVs
│   └── generate_charts.py     # gera os gráficos a partir dos CSVs
├── entregaveis/               # PONTO DE ENTRADA DA ENTREGA
│   ├── RELATORIO.md           # relatório técnico
│   ├── dados/                 # metrics.csv + steps.csv
│   ├── graficos/              # PNGs gerados
│   └── evidencias/            # prints das execuções reais
└── SPEC.md                    # especificação do experimento
```

## Como reproduzir

```bash
git clone https://github.com/lucas-nunes-matheus/cicd-pipelines-metrics
cd cicd-pipelines-metrics
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-analysis.txt
pytest && ruff check .            # validação local

# disparar execuções: commits seguindo o roteiro da SPEC T3 (exp(run-NN): ...)
# ou manualmente: gh workflow run ci.yml

# coletar métricas e gerar gráficos
export GITHUB_TOKEN=$(gh auth token)   # ou um PAT com Actions: Read
python3 scripts/collect_metrics.py     # gera entregaveis/dados/*.csv
python3 scripts/generate_charts.py     # gera entregaveis/graficos/*.png
```

**Token:** `gh auth login` e `export GITHUB_TOKEN=$(gh auth token)`, ou crie um
PAT fine-grained em <https://github.com/settings/tokens> com permissões
**Actions: Read** e **Contents: Read** no repositório.
