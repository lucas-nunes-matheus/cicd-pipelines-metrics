"""Coleta métricas de execuções do workflow CI via API REST do GitHub.

Gera entregaveis/dados/metrics.csv (1 linha por run+job) e
entregaveis/dados/steps.csv (1 linha por run+job+step), cruzando os dados
da API com o report.json do pytest baixado dos artifacts.

Uso:
    export GITHUB_TOKEN=$(gh auth token)
    python3 scripts/collect_metrics.py
"""

import argparse
import csv
import io
import json
import os
import sys
import zipfile
from datetime import datetime
from pathlib import Path

import requests

API_URL = "https://api.github.com"
WORKFLOW_PATH = ".github/workflows/ci.yml"
ARTIFACT_NAME = "test-report"

METRICS_FIELDS = [
    "run_id",
    "commit_sha",
    "commit_message",
    "status",
    "workflow_duration",
    "job_name",
    "job_duration",
    "test_count",
    "test_failures",
    "timestamp",
    "avg_test_time",
    "run_attempt",
    "lead_time_s",
]

STEPS_FIELDS = ["run_id", "job_name", "step_name", "step_duration", "step_status"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--owner", default="lucas-nunes-matheus")
    parser.add_argument("--repo", default="cicd-pipelines-metrics")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "entregaveis" / "dados",
    )
    return parser.parse_args()


def get_token() -> str:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit(
            "Erro: variável GITHUB_TOKEN não definida.\n"
            "Defina com: export GITHUB_TOKEN=$(gh auth token)\n"
            "ou use um PAT com permissão Actions: Read."
        )
    return token


def make_session(token: str) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        }
    )
    return session


def duration_s(start: str | None, end: str | None) -> float | None:
    """Diferença em segundos entre dois timestamps ISO-8601 da API."""
    if not start or not end:
        return None
    return (datetime.fromisoformat(end) - datetime.fromisoformat(start)).total_seconds()


def fetch_runs(session: requests.Session, owner: str, repo: str) -> list[dict]:
    """Lista todas as execuções do workflow de CI, da mais antiga à mais recente."""
    runs = []
    page = 1
    while True:
        resp = session.get(
            f"{API_URL}/repos/{owner}/{repo}/actions/runs",
            params={"per_page": 100, "page": page},
        )
        resp.raise_for_status()
        batch = resp.json()["workflow_runs"]
        if not batch:
            break
        runs.extend(r for r in batch if r["path"] == WORKFLOW_PATH)
        page += 1
    return sorted(runs, key=lambda r: r["run_started_at"])


def fetch_jobs(session: requests.Session, owner: str, repo: str, run_id: int) -> list[dict]:
    resp = session.get(
        f"{API_URL}/repos/{owner}/{repo}/actions/runs/{run_id}/jobs",
        params={"per_page": 100},
    )
    resp.raise_for_status()
    return resp.json()["jobs"]


def fetch_test_report(
    session: requests.Session, owner: str, repo: str, run_id: int
) -> dict | None:
    """Baixa o artifact test-report do run e devolve o report.json parseado."""
    resp = session.get(f"{API_URL}/repos/{owner}/{repo}/actions/runs/{run_id}/artifacts")
    resp.raise_for_status()
    artifact = next(
        (a for a in resp.json()["artifacts"] if a["name"] == ARTIFACT_NAME and not a["expired"]),
        None,
    )
    if artifact is None:
        return None
    download = session.get(artifact["archive_download_url"])
    download.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(download.content)) as zf:
        with zf.open("report.json") as fh:
            return json.load(fh)


def parse_report(report: dict | None) -> dict:
    """Extrai test_count, test_failures e avg_test_time do report.json do pytest."""
    if report is None:
        return {"test_count": "", "test_failures": "", "avg_test_time": ""}
    summary = report["summary"]
    total = summary.get("total", 0)
    durations = [
        test["call"]["duration"] for test in report.get("tests", []) if "call" in test
    ]
    avg = round(sum(durations) / len(durations), 4) if durations else ""
    return {
        "test_count": total,
        "test_failures": summary.get("failed", 0),
        "avg_test_time": avg,
    }


def build_rows(
    session: requests.Session, owner: str, repo: str, runs: list[dict]
) -> tuple[list[dict], list[dict]]:
    metrics_rows = []
    steps_rows = []
    for run in runs:
        run_id = run["id"]
        print(f"Coletando run {run_id} ({run['head_commit']['message'].splitlines()[0]})")
        test_metrics = parse_report(fetch_test_report(session, owner, repo, run_id))
        run_common = {
            "run_id": run_id,
            "commit_sha": run["head_sha"],
            "commit_message": run["head_commit"]["message"].splitlines()[0],
            "status": run["conclusion"],
            "workflow_duration": duration_s(run["run_started_at"], run["updated_at"]),
            "timestamp": run["run_started_at"],
            "run_attempt": run["run_attempt"],
            "lead_time_s": duration_s(run["head_commit"]["timestamp"], run["updated_at"]),
            **test_metrics,
        }
        for job in fetch_jobs(session, owner, repo, run_id):
            metrics_rows.append(
                {
                    **run_common,
                    "job_name": job["name"],
                    "job_duration": duration_s(job["started_at"], job["completed_at"]),
                }
            )
            for step in job["steps"]:
                steps_rows.append(
                    {
                        "run_id": run_id,
                        "job_name": job["name"],
                        "step_name": step["name"],
                        "step_duration": duration_s(step["started_at"], step["completed_at"]),
                        "step_status": step["conclusion"],
                    }
                )
    return metrics_rows, steps_rows


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Gravado {path} ({len(rows)} linhas)")


def main() -> None:
    args = parse_args()
    session = make_session(get_token())
    runs = fetch_runs(session, args.owner, args.repo)
    if not runs:
        sys.exit(f"Nenhuma execução do workflow {WORKFLOW_PATH} encontrada.")
    metrics_rows, steps_rows = build_rows(session, args.owner, args.repo, runs)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(args.out_dir / "metrics.csv", METRICS_FIELDS, metrics_rows)
    write_csv(args.out_dir / "steps.csv", STEPS_FIELDS, steps_rows)


if __name__ == "__main__":
    main()
