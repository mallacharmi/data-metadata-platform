import requests
from datetime import datetime

API_URL = "http://metadata-api:5000"

def emit_event(event_type, dataset_id):
    event = {
        "eventType": event_type,
        "eventTime": datetime.utcnow().isoformat(),
        "job": {
            "name": "pipeline_ingestion"
        },
        "run": {
            "runId": f"run-{dataset_id}"
        },
        "inputs": [
            {"name": "raw_source"}
        ],
        "outputs": [
            {"name": f"dataset_{dataset_id}"}
        ]
    }

    requests.post(f"{API_URL}/openlineage/events", json=event)
