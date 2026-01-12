import time
import pandas as pd
import requests
from datetime import datetime

from stats import extract_schema, compute_column_stats
from dq_checks import run_soda_checks
from openlineage_emit import emit_event

# MUST match docker-compose service name
API_URL = "http://metadata-api:5000"


# --------------------------------
# Wait for Metadata API
# --------------------------------
def wait_for_api(url, retries=60, delay=2):
    for i in range(retries):
        try:
            r = requests.get(f"{url}/health/lineage", timeout=3)
            if r.status_code == 200:
                print("Metadata API is ready")
                return
        except Exception:
            pass

        print(f"Waiting for API... attempt {i + 1}")
        time.sleep(delay)

    raise RuntimeError("Metadata API not reachable")


# --------------------------------
# Emit lineage edge
# --------------------------------
def emit_lineage(api_url, source_dataset_id, target_dataset_id):
    r = requests.post(
        f"{api_url}/lineage",
        json={
            "source_dataset_id": source_dataset_id,
            "target_dataset_id": target_dataset_id,
            "job_name": "pipeline_ingestion"
        }
    )
    r.raise_for_status()
    print("Lineage stored")


# --------------------------------
# Main Pipeline
# --------------------------------
def main():
    # 0. Wait for API
    wait_for_api(API_URL)

    # 1. Read dataset
    df = pd.read_csv("/data/sample.csv")

    # 2. Register dataset (IDEMPOTENT)
    dataset_payload = {
        "name": "sample_dataset",
        "description": "Sample dataset for pipeline testing",
        "tags": "sample,test"
    }

    r = requests.post(f"{API_URL}/datasets", json=dataset_payload)
    r.raise_for_status()
    dataset = r.json()
    dataset_id = dataset["id"]

    print("Dataset ID:", dataset_id)

    # 3. Create RUN (START)
    run_resp = requests.post(
        f"{API_URL}/runs",
        json={
            "job_name": "pipeline_ingestion",
            "status": "START",
            "dataset_id": dataset_id
        }
    )
    run_resp.raise_for_status()
    run_id = run_resp.json()["run_id"]

    print("Run ID:", run_id)

    # Emit OpenLineage START
    emit_event("START", dataset_id)

    # 4. Extract schema & stats
    schema = extract_schema(df)
    stats = compute_column_stats(df)

    r = requests.post(
        f"{API_URL}/datasets/{dataset_id}/schema",
        json={
            "schema": schema,
            "stats": stats
        }
    )
    r.raise_for_status()
    print("Schema & stats stored")

    # 5. Run Soda Core DQ checks
    dq_results = run_soda_checks()

    for check in dq_results:
        requests.post(
            f"{API_URL}/dq-results",
            json={
                "dataset_id": dataset_id,
                "run_id": run_id,
                "check_name": check["name"],
                "status": check["status"],
                "success_percentage": check["success_percentage"]
            }
        )

    print("DQ results stored")

    # 6. Emit lineage (raw → processed)
    emit_lineage(
        API_URL,
        source_dataset_id=0,
        target_dataset_id=dataset_id
    )

    # 7. Update RUN (COMPLETE)
    requests.post(
        f"{API_URL}/runs",
        json={
            "job_name": "pipeline_ingestion",
            "status": "COMPLETE",
            "dataset_id": dataset_id
        }
    )

    # Emit OpenLineage COMPLETE
    emit_event("COMPLETE", dataset_id)

    print("Pipeline completed successfully")


# --------------------------------
# Entry Point
# --------------------------------
if __name__ == "__main__":
    main()
