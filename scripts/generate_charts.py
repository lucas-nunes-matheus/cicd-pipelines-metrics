"""Gera os gráficos do experimento a partir de entregaveis/dados/*.csv.

Saída: PNGs em entregaveis/graficos/.

Uso:
    python3 scripts/generate_charts.py
"""

import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "entregaveis" / "dados"
OUT_DIR = BASE_DIR / "entregaveis" / "graficos"

COLOR_SUCCESS = "#2da44e"
COLOR_FAILURE = "#cf222e"


def run_label(message: str, run_id: int) -> str:
    """Extrai o rótulo run-NN da mensagem de commit; cai no run_id se ausente."""
    match = re.search(r"run-\d+", message)
    return match.group() if match else str(run_id)


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    metrics = pd.read_csv(DATA_DIR / "metrics.csv")
    steps = pd.read_csv(DATA_DIR / "steps.csv")
    metrics["label"] = [
        run_label(m, r) for m, r in zip(metrics["commit_message"], metrics["run_id"])
    ]
    metrics = metrics.sort_values("timestamp")
    runs = metrics.drop_duplicates("run_id").reset_index(drop=True)
    return metrics, steps, runs


def save(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(OUT_DIR / name, dpi=150)
    plt.close(fig)
    print(f"Gravado {OUT_DIR / name}")


def chart_tempo_total(runs: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = [COLOR_SUCCESS if s == "success" else COLOR_FAILURE for s in runs["status"]]
    ax.bar(runs["label"], runs["workflow_duration"], color=colors)
    ax.set_title("Tempo total do pipeline por execução")
    ax.set_xlabel("Execução")
    ax.set_ylabel("Duração do workflow (s)")
    ax.tick_params(axis="x", rotation=45)
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=COLOR_SUCCESS),
        plt.Rectangle((0, 0), 1, 1, color=COLOR_FAILURE),
    ]
    ax.legend(handles, ["sucesso", "falha"])
    save(fig, "01_tempo_total_por_execucao.png")


def chart_tempo_por_job(metrics: pd.DataFrame) -> None:
    pivot = metrics.pivot_table(
        index="label", columns="job_name", values="job_duration", sort=False
    )
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot.bar(ax=ax)
    ax.set_title("Tempo por job em cada execução")
    ax.set_xlabel("Execução")
    ax.set_ylabel("Duração do job (s)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Job")
    save(fig, "02_tempo_por_job.png")


def chart_taxa_sucesso(runs: pd.DataFrame) -> None:
    counts = runs["status"].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(
        counts,
        labels=[f"{status} ({count})" for status, count in counts.items()],
        colors=[COLOR_SUCCESS if s == "success" else COLOR_FAILURE for s in counts.index],
        autopct="%1.0f%%",
        startangle=90,
    )
    ax.set_title(f"Taxa de sucesso e falha ({len(runs)} execuções)")
    save(fig, "03_taxa_sucesso_falha.png")


def chart_testes_vs_duracao(runs: pd.DataFrame) -> None:
    com_testes = runs.dropna(subset=["test_count"])
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(
        com_testes["test_count"],
        com_testes["workflow_duration"],
        color="#0969da",
        zorder=3,
    )
    for _, row in com_testes.iterrows():
        ax.annotate(
            row["label"],
            (row["test_count"], row["workflow_duration"]),
            textcoords="offset points",
            xytext=(6, 4),
            fontsize=8,
        )
    ax.set_title("Quantidade de testes × duração do pipeline")
    ax.set_xlabel("Quantidade de testes executados")
    ax.set_ylabel("Duração do workflow (s)")
    ax.grid(True, alpha=0.3, zorder=0)
    save(fig, "04_testes_vs_duracao.png")


def chart_install_por_run(steps: pd.DataFrame, runs: pd.DataFrame) -> None:
    """Duração do step Install dependencies por run — evidencia o efeito do cache."""
    install = steps[steps["step_name"] == "Install dependencies"]
    label_por_run = runs.set_index("run_id")["label"]
    pivot = install.pivot_table(index="run_id", columns="job_name", values="step_duration")
    pivot.index = [label_por_run.get(i, str(i)) for i in pivot.index]
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot.bar(ax=ax)
    ax.set_title("Duração do step 'Install dependencies' por execução (efeito do cache)")
    ax.set_xlabel("Execução")
    ax.set_ylabel("Duração do step (s)")
    ax.tick_params(axis="x", rotation=45)
    ax.legend(title="Job")
    save(fig, "05_cache_vs_sem_cache.png")


def chart_paralelismo(metrics: pd.DataFrame, runs: pd.DataFrame) -> None:
    """Soma dos jobs × duração real do workflow — a diferença é o ganho do paralelismo."""
    soma_jobs = metrics.groupby("run_id")["job_duration"].sum()
    ordered = runs.set_index("run_id")
    x = range(len(ordered))
    width = 0.4
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(
        [i - width / 2 for i in x],
        [soma_jobs[i] for i in ordered.index],
        width,
        label="Soma dos jobs (execução sequencial teórica)",
        color="#8250df",
    )
    ax.bar(
        [i + width / 2 for i in x],
        ordered["workflow_duration"],
        width,
        label="Duração real do workflow",
        color="#0969da",
    )
    ax.set_xticks(list(x))
    ax.set_xticklabels(ordered["label"], rotation=45)
    ax.set_title("Paralelismo: soma dos jobs × duração real do workflow")
    ax.set_xlabel("Execução")
    ax.set_ylabel("Duração (s)")
    ax.legend()
    save(fig, "06_sequencial_vs_paralelo.png")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    metrics, steps, runs = load_data()
    chart_tempo_total(runs)
    chart_tempo_por_job(metrics)
    chart_taxa_sucesso(runs)
    chart_testes_vs_duracao(runs)
    chart_install_por_run(steps, runs)
    chart_paralelismo(metrics, runs)
    print(f"\n{len(runs)} execuções plotadas.")


if __name__ == "__main__":
    main()
