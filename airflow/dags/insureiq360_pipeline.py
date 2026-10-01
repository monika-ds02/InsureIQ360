from datetime import datetime, timedelta
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

from airflow import DAG
from airflow.operators.python import PythonOperator


API_BASE_URL = "http://host.docker.internal:8000"


def get_token():
    data = urlencode({
        "username": "admin",
        "password": "admin123",
    }).encode("utf-8")

    request = Request(
        f"{API_BASE_URL}/auth/login",
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST",
    )

    with urlopen(request, timeout=30) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["access_token"]


def call_api(endpoint):
    token = get_token()

    request = Request(
        f"{API_BASE_URL}{endpoint}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
        method="GET",
    )

    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def data_quality_check():
    print("Running real data quality check...")

    result = call_api("/data-quality/")

    print("Data Quality Result:")
    print(json.dumps(result, indent=2))

    if result.get("quality_score") != 100:
        raise Exception(
            f"Data quality check failed. "
            f"Quality score: {result.get('quality_score')}"
        )

    print("Data quality check passed.")


def fraud_detection_check():
    print("Running real fraud detection check...")

    result = call_api("/fraud-detection/")

    print("Fraud Detection Result:")
    print(json.dumps(result, indent=2))

    print(
        f"Fraud risk level: {result.get('risk_level')}"
    )

    print("Fraud detection check completed.")


def risk_analysis_check():
    print("Running real claims risk analysis...")

    result = call_api("/claims/dashboard")

    print("Risk Analysis Result:")
    print(json.dumps(result, indent=2))

    print("Risk analysis check completed.")


def workflow_alert_check():
    print("Running real workflow and alert check...")

    result = call_api("/alerts/")

    print("Alert Result:")
    print(json.dumps(result, indent=2))

    print("Workflow and alert check completed.")


default_args = {
    "owner": "insureiq360",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


with DAG(
    dag_id="insureiq360_pipeline",
    default_args=default_args,
    description="InsureIQ360 insurance claims intelligence pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["insureiq360", "claims", "risk"],
) as dag:

    data_quality = PythonOperator(
        task_id="data_quality_check",
        python_callable=data_quality_check,
    )

    fraud_detection = PythonOperator(
        task_id="fraud_detection_check",
        python_callable=fraud_detection_check,
    )

    risk_analysis = PythonOperator(
        task_id="risk_analysis_check",
        python_callable=risk_analysis_check,
    )

    workflow_alerts = PythonOperator(
        task_id="workflow_alert_check",
        python_callable=workflow_alert_check,
    )

    data_quality >> fraud_detection >> risk_analysis >> workflow_alerts