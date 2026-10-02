# Deploy runbook

Trigger: Merge to `main` → CI builds image → Coolify deploy webhook fires.

1. **Verify CI passed** — check GitHub Actions: lint, types, tests, audit, image build.
2. **Monitor Coolify** — deployment dashboard shows `migrate` → `api` → `worker` status.
3. **Check health** — `curl https://app.sangad.in/healthz` and `/readyz`.
4. **Run smoke test** — login + OTP, create a test payslip, verify PDF download.
5. **Rollback if failed** — see `rollback.md`.

Notes:
- Coolify pulls the image tag matching the commit SHA.
- Migrations run automatically; if they fail, the api service does not start.
- Keep the previous image tag — redeploy it for rollback.