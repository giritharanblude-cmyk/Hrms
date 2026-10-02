# Breach response runbook

1. **Detect** — unusual audit log entries, alert from Sentry/Coolify, user report.
2. **Contain:**
   - Lock the master user account (change env `MASTER_PASSWORD` and redeploy).
   - Revoke and rotate all secrets: `SESSION_SECRET_KEY`, `FIELD_ENCRYPTION_KEY`, SMTP, S3, OpenWA.
   - Take the app offline temporarily if needed (scale api/worker to 0 in Coolify).
3. **Preserve evidence:**
   - Export audit_log table.
   - Save container logs.
   - Snapshot the database (do NOT modify rows).
4. **Assess:**
   - Was any PII accessed? Check audit log for Aadhaar reveal events.
   - Was the encryption key compromised? If yes, Aadhaar data may be exposed.
   - Was the database dumped? Check network logs.
5. **Notify:**
   - Legal/privacy reviewer (DPDP Act obligations).
   - Affected employees if PII was exposed.
6. **Recover:**
   - Rotate all secrets (R-21).
   - Restore DB from pre-incident backup if tampered with.
   - Re-deploy from clean image.
   - Re-pair WhatsApp.
7. **Post-mortem:**
   - Document root cause in section 9 (open questions / risks).
   - Update controls to prevent recurrence.