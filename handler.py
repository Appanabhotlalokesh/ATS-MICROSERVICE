import os
import json
import requests

ZOHO_BASE_URL = os.getenv("ZOHO_BASE_URL")
ZOHO_ACCESS_TOKEN = os.getenv("ZOHO_ACCESS_TOKEN")

HEADERS = {
    "Authorization": f"Zoho-oauthtoken {ZOHO_ACCESS_TOKEN}"
}

def get_jobs(event, context):
    url = f"{ZOHO_BASE_URL}/recruit/v2/JobOpenings"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        return {
            "statusCode": res.status_code,
            "body": json.dumps({"error": res.text})
        }

    jobs = []
    for j in res.json().get("data", []):
        jobs.append({
            "id": j.get("id"),
            "title": j.get("Job_Opening_Name"),
            "location": j.get("City"),
            "status": j.get("Status"),
            "external_url": j.get("Career_Page_URL")
        })

    return {
        "statusCode": 200,
        "body": json.dumps(jobs)
    }


def create_candidate(event, context):
    body = json.loads(event["body"])

    payload = {
        "data": [{
            "First_Name": body["name"],
            "Email": body["email"],
            "Mobile": body["phone"]
        }]
    }

    url = f"{ZOHO_BASE_URL}/recruit/v2/Candidates"
    res = requests.post(url, headers=HEADERS, json=payload)

    return {
        "statusCode": res.status_code,
        "body": res.text
    }
