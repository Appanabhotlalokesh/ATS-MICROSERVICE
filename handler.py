import json
from http import HTTPStatus

import zoho


def _build_response(body, status_code=HTTPStatus.OK):
    return {
        "statusCode": int(status_code),
        "body": json.dumps(body)
    }


def get_jobs(event, context):
    try:
        data = zoho.get_jobs().get("data", [])
        jobs = [
            {
                "id": item.get("id"),
                "title": item.get("Job_Opening_Name"),
                "location": item.get("City"),
                "status": item.get("Status"),
                "external_url": item.get("Career_Page_URL")
            }
            for item in data
        ]
        return _build_response(jobs)
    except Exception as error:
        return _build_response({"error": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR)


def create_candidate(event, context):
    try:
        payload = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return _build_response(
            {"error": "Request body must be valid JSON."},
            HTTPStatus.BAD_REQUEST
        )

    missing = [field for field in ("name", "email", "phone") if not payload.get(field)]
    if missing:
        return _build_response(
            {"error": "Missing required fields.", "missing": missing},
            HTTPStatus.BAD_REQUEST
        )

    candidate_data = {
        "First_Name": payload["name"],
        "Email": payload["email"],
        "Mobile": payload["phone"]
    }

    try:
        result = zoho.create_candidate(candidate_data)
        return _build_response(
            {"message": "Candidate created.", "result": result},
            HTTPStatus.CREATED
        )
    except Exception as error:
        return _build_response({"error": str(error)}, HTTPStatus.INTERNAL_SERVER_ERROR)
