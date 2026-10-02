# Rollback runbook

Use when a deploy fails healthcheck or introduces a critical bug.

1. **Identify previous working image tag** — from Coolify deploy history or Git log.
2. **Redeploy previous tag** — in Coolify, set the service image tag to the previous sha and deploy.
3. **Verify** — healthcheck passes, smoke test passes.
4. **If migration was applied** — do NOT automatically revert. Migrations are additive only. If a migration damaged data, restore from backup (see `restore.md`).
5. **Notify** — check alerts, confirm WhatsApp gateway reconnects.