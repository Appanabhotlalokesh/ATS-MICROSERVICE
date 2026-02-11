import os
import requests

BASE_URL = os.getenv("ZOHO_BASE_URL")
ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Zoho-oauthtoken {ACCESS_TOKEN}"
}

def get_jobs():
    url = f"{BASE_URL}/recruit/v2/JobOpenings"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def create_candidate(data):
    url = f"{BASE_URL}/recruit/v2/Candidates"
    payload = {"data": [data]}
    response = requests.post(url, json=payload, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_applications(job_id):
    url = f"{BASE_URL}/recruit/v2/Applications/search?criteria=(Job_Opening:equals:{job_id})"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()
