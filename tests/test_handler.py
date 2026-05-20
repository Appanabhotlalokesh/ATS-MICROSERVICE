import json
import pytest
from handler import create_candidate, get_jobs

class DummyResponse:
    def __init__(self, json_data=None, status_code=200, text=""):
        self._json_data = json_data or {}
        self.status_code = status_code
        self.text = text

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise Exception(f"HTTP {self.status_code}")


def test_get_jobs_success(monkeypatch):
    from zoho import get_jobs as zoho_get_jobs

    def fake_get_jobs():
        return {
            "data": [
                {"id": "1", "Job_Opening_Name": "Developer", "City": "Remote", "Status": "Open", "Career_Page_URL": "https://example.com"}
            ]
        }

    import zoho
    monkeypatch.setattr(zoho, "get_jobs", fake_get_jobs)

    event = {}
    result = get_jobs(event, None)
    assert result["statusCode"] == 200
    payload = json.loads(result["body"])
    assert payload[0]["title"] == "Developer"
    assert payload[0]["location"] == "Remote"


def test_create_candidate_missing_fields():
    event = {"body": json.dumps({"name": "Alice"})}
    result = create_candidate(event, None)
    assert result["statusCode"] == 400
    body = json.loads(result["body"])
    assert "missing" in body


def test_create_candidate_success(monkeypatch):
    from zoho import create_candidate as zoho_create_candidate

    def fake_create_candidate(data):
        return {"data": [{"id": "123", **data}]}

    import zoho
    monkeypatch.setattr(zoho, "create_candidate", fake_create_candidate)

    event = {"body": json.dumps({"name": "Alice", "email": "alice@example.com", "phone": "1234567890"})}
    result = create_candidate(event, None)
    assert result["statusCode"] == 201
    body = json.loads(result["body"])
    assert body["message"] == "Candidate created."
    assert body["result"]["data"][0]["Email"] == "alice@example.com"
