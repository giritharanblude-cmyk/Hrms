# SANGAD

Customized Admin Management Dashboard (micro-SaaS)

## Docs

- [Architecture](SANGAD_ARCHITECTURE_v0.2.md)
- [Build Plan](BUILD_PLAN.md)

## Repo layout

```
sangad/
├─ docs/                    # architecture, ADRs, runbooks
├─ backend/                 # FastAPI + Python
│  ├─ app/
│  │  ├─ core/              # config, db, security, errors, logging
│  │  ├─ kernel/            # auth, audit, files, mail, jobs, ports
│  │  └─ modules/           # payslip, bills, inventory, employees, company
│  └─ tests/
├─ frontend/                # React + Vite + TypeScript
│  └─ src/
│     ├─ app/               # router, providers, shell
│     ├─ shared/            # ui kit, api client, hooks
│     └─ features/          # per-module feature folders
└─ infra/
   ├─ coolify/              # docker-compose, .env.example
   ├─ runbooks/             # deploy, rollback, restore
   └─ scripts/              # backup verify, restore drill
```

## Getting started

1. Copy `infra/coolify/.env.example` to `.env` and fill secrets.
2. Start dev: `docker compose -f infra/coolify/docker-compose.yml up`
3. Backend: `cd backend && pip install -e ".[dev]" && uvicorn app.main:app --reload`
4. Frontend: `cd frontend && npm install && npm run dev`