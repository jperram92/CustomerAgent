import requests
from dotenv import load_dotenv
import os

load_dotenv() # Load the environment variables

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "fc5863d6-b718-4ba7-9158-d43ea09066fd"
FLOW_ID = "e5e837db-ff19-45a1-ae69-4d1df9d262da"
APPLICATION_TOKEN = "OS.environ.get('APP_TOKEN')"
ENDPOINT = "" # You can set a specific endpoint name in the flow settings


def run_flow(message: str) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{ENDPOINT}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }
    headers = {"Authorization": "Bearer " + APPLICATION_TOKEN, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
