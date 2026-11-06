from pathlib import Path

import httpx2

TRACES_PATH = Path(__file__).parent / "traces.jsonl"
MLFLOW_URL = "http://localhost:5000"
EXPERIMENT_NAME = "code-search"


def get_or_create_experiment(client: httpx2.Client) -> str:
    response = client.get("/api/2.0/mlflow/experiments/get-by-name", params={"experiment_name": EXPERIMENT_NAME})

    if response.status_code == httpx2.codes.NOT_FOUND:
        response = client.post("/api/2.0/mlflow/experiments/create", json={"name": EXPERIMENT_NAME})
        return response.json()["experiment_id"]

    return response.json()["experiment"]["experiment_id"]


def main() -> None:
    with httpx2.Client(base_url=MLFLOW_URL) as client:
        experiment_id = get_or_create_experiment(client)
        headers = {"content-type": "application/json", "x-mlflow-experiment-id": experiment_id}

        for line in TRACES_PATH.read_text().splitlines():
            client.post("/v1/traces", content=line, headers=headers)


if __name__ == "__main__":
    main()
