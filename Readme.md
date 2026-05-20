# ATS Microservice

A serverless Python microservice that integrates with Zoho Recruit to fetch job listings and create candidates.

## Key features

- AWS Lambda functions powered by the Serverless Framework
- Zoho Recruit API integration
- HTTP endpoints for job retrieval and candidate creation
- Local development with `serverless-offline`
- Basic test coverage with `pytest`

## Project structure

- `handler.py` — Lambda entrypoints and request handling
- `zoho.py` — Zoho Recruit API client
- `serverless.yml` — Serverless Framework configuration
- `requirements.txt` — Python dependencies
- `tests/` — automated tests
- `.env.example` — required environment variables template

## Local setup

1. Copy `.env.example` to `.env`
2. Populate Zoho credentials and base URL
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Install Node dependencies for Serverless plugins:

```bash
npm install
```

## Run locally

```bash
npx serverless offline start
```

Then use:

- `GET /jobs`
- `POST /candidates`

## Frontend UI

A simple frontend has been added under `frontend/`.

- Open `frontend/index.html` in your browser
- It displays open jobs and allows candidate submissions
- It sends requests to the local API at `http://localhost:3000/local`

If you are running the local backend, just open the file in your browser and refresh the page.

## Deployment

```bash
npx serverless deploy
```

## Testing

```bash
pytest
```

## Environment variables

- `ZOHO_CLIENT_ID`
- `ZOHO_CLIENT_SECRET`
- `ZOHO_ACCESS_TOKEN`
- `ZOHO_BASE_URL`

## Notes

This project is designed as a resume-ready example of a serverless backend service with an external ATS integration.
