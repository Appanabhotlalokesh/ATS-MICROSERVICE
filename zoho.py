import os

import requests


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Environment variable {name} is required.")
    return value


def _build_headers() -> dict:
    return {
        "Authorization": f"Zoho-oauthtoken {_require_env('ZOHO_ACCESS_TOKEN')}",
        "Content-Type": "application/json"
    }


def _base_url() -> str:
    return _require_env("ZOHO_BASE_URL")


def get_jobs() -> dict:
    url = f"{_base_url()}/recruit/v2/JobOpenings"
    response = requests.get(url, headers=_build_headers())
    response.raise_for_status()
    return response.json()


def create_candidate(data: dict) -> dict:
    url = f"{_base_url()}/recruit/v2/Candidates"
    payload = {"data": [data]}
    response = requests.post(url, json=payload, headers=_build_headers())
    response.raise_for_status()
    return response.json()


def get_applications(job_id: str) -> dict:
    url = f"{_base_url()}/recruit/v2/Applications/search?criteria=(Job_Opening:equals:{job_id})"
    response = requests.get(url, headers=_build_headers())
    response.raise_for_status()
    return response.json()
