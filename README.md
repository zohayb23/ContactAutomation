# ContactAutomationCloud

Cloud-ready email automation service you can trigger from any laptop.

## Features

- Trigger artist email campaigns from an authenticated API endpoint.
- Queue sends through Redis + RQ worker for reliability.
- Persist run history, recipient logs, and statuses in Postgres.
- Built-in safety rails:
  - dry-run mode
  - max send cap per run
  - dedupe window to prevent repeat sends
  - basic API rate limiting

## Quick Start

1. Copy environment template:

   ```bash
   cp .env.example .env
   ```

2. Update `.env`:
   - set `API_TOKEN`
   - set SMTP credentials (`SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_SENDER_EMAIL`)

3. Start stack:

   ```bash
   docker compose up --build -d
   ```

4. Seed sample contacts:

   ```bash
   docker compose exec api python -m scripts.seed_contacts
   ```

## Trigger a Campaign

```bash
curl -X POST http://localhost:8000/campaigns/send \
  -H "Authorization: Bearer change-this-token" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_name":"artist-outreach",
    "subject":"New beat pack available",
    "body":"Yo! New beats are live. Reply if you want previews.",
    "dry_run":true,
    "max_send_per_run":25
  }'
```

## Check Campaign Status

```bash
curl http://localhost:8000/campaigns/1 \
  -H "Authorization: Bearer change-this-token"
```

## Deploy Suggestions

- Render/Railway/Fly for API + worker
- Managed Postgres (Neon/Supabase/Render)
- Managed Redis (Upstash/Redis Cloud)

Keep API token and SMTP secrets in host secret manager. Do not commit `.env`.
