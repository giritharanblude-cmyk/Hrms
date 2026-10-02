# SANGAD Build Plan

Based on `SANGAD_ARCHITECTURE_v0.2.md` — a complete, phased plan to go from repo to go-live.

---

## Prerequisites (resolve before any coding)

| # | Action | Ref |
|---|---|---|
| 1 | Approve open questions in section 9 (Q-01 to Q-24). Blocking items: Q-15 (WhatsApp risk), Q-13 (domain names), Q-20 (S3 bucket). | T-000 |
| 2 | Provision a Linux VPS (~2 vCPU / 4 GB RAM). | C-06 |
| 3 | Install Coolify on the VPS, connect your Git account. | T-002 |
| 4 | Set up domains: app domain, Coolify dashboard domain, email sending domain (SPF/DKIM). | Q-13 |
| 5 | Create S3-compatible bucket in an India region. | ADR-15, Q-20 |
| 6 | Get Hostinger SMTP credentials and confirm send limits. | C-03, Q-12 |
| 7 | Dedicate a phone number for the WhatsApp gateway. | C-10, Q-17 |

---

## Phase 0 — Platform Skeleton (weeks 1-2)

Build the shared foundation that every module depends on.

| Step | What | Key deliverables | Validation |
|---|---|---|---|
| 0.1 | Monorepo setup | `sangad/` with `backend/`, `frontend/`, `infra/`, `docs/` dirs; `pyproject.toml`, `package.json`, linter/type configs, pre-commit hooks, CI pipeline (GitHub Actions) | V-PLAT-01 |
| 0.2 | Backend core | FastAPI app factory, config from env, DB session, Alembic migrations, RFC 9457 error model, structured JSON logging | T-003 |
| 0.3 | Kernel: Auth | Login (name + password), email OTP (6-digit, 5-min expiry, max 5 attempts, 60s cooldown), server-side sessions in Redis, password change, CSRF, idle timeout | T-004, V-AUTH-01..06 |
| 0.4 | Kernel: Shared services | Audit log (append-only DB role), files service, number sequences (gapless, per-FY), job runner (RQ) | T-005, V-PLAT-03, V-SEC-02 |
| 0.5 | Frontend shell | AppShell with sidebar (5 modules), TopBar (username + role), shared components (KpiCard, DataTable, FileDropzone, CameraCapture, FormDrawer, etc.), Landing page with 5 cards | T-006, V-UI-01 |
| 0.6 | API client | `openapi-typescript` generation wired into the build | T-007, R-14 |
| 0.7 | File storage | `FileStoragePort` with S3 adapter + local dev adapter | T-010 |
| 0.8 | Deploy pipeline | VPS → Coolify → `sangad` Compose app (api, worker, migrate), Postgres + Redis DB resources, domain + TLS, env config, health checks, backups to S3, deploy webhook from CI | T-002, T-008, V-PLAT-02, V-DEP-01, V-OPS-01 |
| 0.9 | Hardening | Coolify dashboard domain + auth, firewall (80/443 only + SSH allow-list), encryption key escrow, update cadence | T-009, V-DEP-02 |

**Exit criteria:** Login + OTP works end-to-end on the Coolify-deployed environment. Landing shows 5 empty module cards. CI green. First backup restored successfully.

---

## Phase 1 — Modules (standalone, ~2 weeks per module)

Each module is built fully standalone with stub adapters. No cross-module dependencies yet.

### Module 1: Payslip (T-101 to T-109)

| Step | What |
|---|---|
| 1.1 | Models + migration (`payslips`, `payslip_lines`, `payslip_deliveries`, `import_jobs`) + stub adapters for EmployeeDirectoryPort, CompanyProfilePort |
| 1.2 | `amount_to_words_inr()` (Indian numbering: lakh/crore) + unit tests |
| 1.3 | Manual form API + UI (employee fields, earnings, deductions, working days) |
| 1.4 | Import template (downloadable .xlsx/.csv), upload + row-level validation wizard |
| 1.5 | Jinja2 HTML template matching the Blude TechX LLP payslip layout; preview endpoint |
| 1.6 | Edit-and-re-preview flow; revision tracking (Draft → Generated → Sent) |
| 1.7 | PDF generation via WeasyPrint (worker job) + download |
| 1.8 | Email delivery (single + bulk) via Hostinger SMTP, retry, delivery status tracking |
| 1.9 | Payroll list screen: KPI cards, search/filter/month picker, list/grid toggle, status badges |

**Validation:** V-PAY-01..05

### Module 2: Bills (T-201 to T-213)

| Step | What |
|---|---|
| 2.1 | Models + migration (`bills` with `review_state`, nullable `serial`; `bill_items`, `vouchers`, `extraction_jobs`) + `SequencePort` |
| 2.2 | Upload (image/PDF/Word) + camera capture + SHA-256 deduplication |
| 2.3 | `ExtractionPort`: LLM vision adapter (primary) + local OCR adapter (fallback) |
| 2.4 | Review screen → confirm/edit → commit + serial assignment (`BILL-<FY>-NNNNNN` / `VCH-<FY>-NNNNNN`) |
| 2.5 | Manual entry form + voucher flow (below configurable threshold, default ₹2,000) |
| 2.6 | Excel/CSV export |
| 2.7 | Expense dashboard: KPI cards, 6-month trend chart, by-category breakdown, filterable table |
| 2.8 | Kernel: `channel_senders`, `inbound_messages` migration; `InboundChannelPort`, `MessagingPort`, `BillIntakePort` interfaces |
| 2.9 | OpenWA adapter: internal webhook receiver (HMAC, timestamp window, allow-list, idempotency) on port 8001 |
| 2.10 | Ingest worker: fetch media from OpenWA → validate → store → create draft (needs_review) → start extraction → reply acknowledgement |
| 2.11 | Needs-review inbox UI (source badge: WhatsApp/upload/camera), gateway-status banner + email alert |
| 2.12 | Add `openwa` service to Compose (pinned version), scoped API key, pairing runbook |
| 2.13 | Contract tests with recorded OpenWA webhook fixtures; Playwright test: WhatsApp draft → review → commit |

**Validation:** V-BILL-01..04, V-WA-01..09

### Module 3: Inventory (T-301 to T-303)

| Step | What |
|---|---|
| 3.1 | Models + migration (`stock_items`, `stock_movements` with movement ledger) |
| 3.2 | CRUD API + form + list with search/filter/export |
| 3.3 | Low-stock flag (qty ≤ reorder level) |

**Validation:** V-INV-01

### Module 4: Employees (T-401 to T-404)

| Step | What |
|---|---|
| 4.1 | Models + migration (`employees`, `employee_documents`); Aadhaar field AES-GCM encrypted, masked by default, Verhoeff checksum |
| 4.2 | CRUD API + form + list with soft-delete, search/filter/export |
| 4.3 | Document upload tab |
| 4.4 | Implement `EmployeeDirectoryPort` |

**Validation:** V-EMP-01

### Module 5: Company (T-501 to T-503)

| Step | What |
|---|---|
| 5.1 | Model + migration (`company_profile`, `company_documents`); GSTIN format + checksum validator |
| 5.2 | Single profile form + documents tab |
| 5.3 | Implement `CompanyProfilePort` (feeds payslip letterhead and signatory) |

**Validation:** V-CMP-01

**Phase 1 exit criteria:** All `V-` ids pass per module. Each module demoable standalone. R-15 satisfied (unit tests, API tests, Playwright happy-path per module).

---

## Phase 2 — Integration (~1 week)

Wire modules together by swapping stub adapters for real implementations.

| Step | What |
|---|---|
| 2.1 | Payslip ← Employees: employee picker replaces manual employee fields; import resolves employee ID from DB |
| 2.2 | Payslip ← Company: letterhead, signatory, PF flag come from Company module |
| 2.3 | Landing cards show live summary counts (pending payslips, bills needing review, low-stock items, employee count) |
| 2.4 | End-to-end Playwright: login+OTP → add employee → set company → create payslip → preview → edit → PDF → email |

**Validation:** V-INT-01..03

---

## Phase 3 — Hardening & Release (~1 week)

| Step | What |
|---|---|
| 3.1 | Security pass: dependency audit, security headers, rate limits, pen-test checklist (OWASP ASVS L2, Top 10) | T-701, V-SEC-01 |
| 3.2 | Performance pass: list endpoints p95 < 500ms at 10k rows; batch 50 PDFs < 2 min | T-702, V-PERF-01 |
| 3.3 | Backup restore drill; runbook | T-703, V-PLAT-04 |
| 3.4 | Legal/privacy review of PII handling (DPDP Act 2023) | T-704 |
| 3.5 | UAT with real payslips and bills | T-705 |
| 3.6 | Retention schedule: gateway media purge, record retention | T-706, V-WA-09 |
| 3.7 | Supply chain: SBOM, image scan, pinned digests | T-707 |
| 3.8 | Live WhatsApp UAT with production number | T-708 |

---

## Key architectural decisions to respect

- **Modular monolith** — one backend deployable, modules talk through ports only (R-01, R-02, ADR-01)
- **Standalone first** — each module built with stub adapters, wired in Phase 2 (ADR-02)
- **FastAPI + Pydantic v2** — thin routers, services for logic, repos for DB (R-03, R-04)
- **Server-side sessions in Redis** — no JWT (ADR-04)
- **Payslip snapshots** — issued payslips store employee/company data at time of issue (ADR-05)
- **Money = Decimal/NUMERIC(14,2)** — never float (R-05)
- **Serial numbers at commit** — gapless via locked sequence table (ADR-09)
- **WhatsApp drafts** — never auto-committed (ADR-13)
- **Internal webhook listener** — port 8001, not publicly routed (ADR-14)
- **S3 files** — from day one (ADR-15)
- **Coolify DB resources** — not Compose volumes (ADR-16)
- **SPA served from API image** — single origin (ADR-17)

## Critical rules from the doc

| Rule | Summary |
|---|---|
| R-10 | Slow work (>1s) goes in the worker queue |
| R-11 | Extraction is advisory; human review before commit |
| R-12 | Serial numbers from `SequencePort` only, inside the insert transaction |
| R-13 | Every data mutation writes an audit row |
| R-19 | Webhooks: HMAC in constant time + timestamp window + dedupe + internal listener |
| R-21 | Encryption key escrowed offline, recovery rehearsed |
| R-24 | Modules never call the gateway directly — use ports only |
| R-25 | Conventional Commits with T- id; API versioned; SemVer releases |

## Risk mitigations to build in from day one

- RK-01: Dedicated WhatsApp number + transactional-only replies + manual fallback
- RK-02: Pin OpenWA version + contract tests with recorded fixtures
- RK-03: Coolify hardening checklist (T-009)
- RK-04: Nightly S3 backups + quarterly restore drill
- RK-05: Offline encryption key escrow
- RK-06: Field-level encryption + masking + audit + legal review

## Estimated timeline

| Phase | Duration |
|---|---|
| Prerequisites | 1 week |
| Phase 0 — Platform | 2 weeks |
| Phase 1 — 5 Modules | 8-10 weeks (2 weeks each) |
| Phase 2 — Integration | 1 week |
| Phase 3 — Hardening | 1 week |
| **Total** | **~13-15 weeks** |