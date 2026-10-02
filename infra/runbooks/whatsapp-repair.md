# WhatsApp re-pair runbook

Use when OpenWA session disconnects (banner shown on Bills screen + email alert).

1. **SSH into the VPS** (allow-listed IP only).
2. **Forward OpenWA dashboard port:**
   ```
   ssh -L 3000:localhost:3000 user@vps-ip
   ```
3. **Open browser** to `http://localhost:3000` — OpenWA admin UI.
4. **Authenticate** with the scoped API key.
5. **Re-pair session:**
   - If QR code method: scan with WhatsApp on the dedicated gateway number.
   - If pairing code method: enter the code in WhatsApp → Settings → Linked Devices.
6. **Verify** — session status shows "connected" in OpenWA dashboard.
7. **Check** — Bills screen banner disappears within 5 minutes.
8. **Close tunnel.**

Prevention: keep the dedicated phone powered and online. Session usually lasts 2-6 weeks before needing re-pair.