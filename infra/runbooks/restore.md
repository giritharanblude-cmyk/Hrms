# Restore from backup runbook

Target: RTO ≤ 4 hours, RPO ≤ 24 hours.

1. **Provision new VPS** (if original is gone) — see `deploy.md` for base setup.
2. **Install Coolify** — same version, connect the same Git account.
3. **Restore Postgres from S3 backup:**
   - Download latest backup from S3 bucket `sangad-backups`:
     ```
     aws s3 cp s3://sangad-backups/postgres/latest.dump ./restore.dump
     ```
   - Create the Postgres resource in Coolify (same name).
   - Restore: `pg_restore -d postgresql://... -Fc restore.dump`
4. **Recreate the app** — Coolify Compose application from Git, same env vars (from vault).
5. **Verify data** — log in, check employee count, payslips, bills.
6. **Re-pair WhatsApp** — see `whatsapp-repair.md`.
7. **Test** — full smoke test: login+OTP → payslip → PDF → email → bill upload.