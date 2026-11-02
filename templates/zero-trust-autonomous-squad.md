# Template: Zero-Trust Autonomous Squad

> **Topology**: Hierarchical Supervisor with ShieldNode Push-Approval Gating  
> **Ideal For**: High-stakes production automation, sensitive database migrations, automated git push/deploy, financial/payment execution, and zero-raw-credential environments.

---

## 1. Purpose & Security Model

The **Zero-Trust Autonomous Squad** is engineered for environments where autonomous agents must execute real-world operations without ever touching, storing, or leaking production API keys, database credentials, or private signing keys.

### Core Principles
1. **Zero Raw Credential Exposure**: Real credentials reside permanently inside the ShieldNode secure vault. Sub-agents operate exclusively using ephemeral, rate-limited, scoped virtual keys (`shieldnode_...`).
2. **Push-Approval Gating for Mutations**: Read-only queries pass automatically via standard rate-limited policies, while high-stakes state mutations (database schema alters, payments, git pushes, production deploys) trigger real-time biometric confirmation on the operator's mobile device via ShieldNode.
3. **Revocable Least-Privilege Delegation**: The Squad Lead allocates purpose-bound virtual keys to specialists. Any compromised or misbehaving agent can have its virtual key revoked instantly without rotating upstream keys.
4. **Independent Continuous Auditing**: The Security Auditor monitors proxy telemetry out-of-band, enforcing hard turn ceilings and financial token circuit breakers.

---

## 2. Roster & Roles

| Role | Responsibility | Input | Output | Tools / Permissions |
|------|---------------|-------|--------|---------------------|
| **Squad Lead / Orchestrator** | Plans missions, decomposes tasks into DAGs, delegates scoped virtual keys, and coordinates specialist bots. Never handles raw secrets. | High-level user goal / ticket | Decomposed task DAG & virtual key allocations | Task dispatcher, virtual key router, status monitor |
| **Recon / Analyst** | Performs non-destructive telemetry scans, log inspection, query analysis, and dependency checks using read-only virtual keys. | Audit query / diagnostic brief | Diagnostic report & validated change plan | Read-only proxy client, codebase search, query runner |
| **Critical Operator / Executor** | Executes high-stakes state mutations through ShieldNode proxy (`proxy.shieldnode.app`). Attaches push-approval metadata (`X-Approval-Reason`, `X-Approval-Duration`, `X-Agent-Name`). | Validated change plan from Lead/Recon | Execution status & mutation receipt | ShieldNode proxy client, git/database CLI via proxy |
| **Security Auditor / Log Sentinel** | Ingests proxy audit logs, tracks token spend, enforces turn governors, and kills rogue agent sessions upon anomaly or secret leakage. | Proxy audit logs & turn telemetry | PASS / HALT signals & security alerts | ShieldNode audit watcher, budget circuit breaker, turn governor |

---

## 3. Interaction Flow

```mermaid
flowchart TD
    User([Human Operator / User]) -->|Task Goal / Issue| Lead[Squad Lead / Orchestrator]
    Lead -->|Plan & Read-Only Virtual Key| Recon[Recon / Analyst]
    Recon -->|Diagnostic Findings & Change Plan| Lead
    Lead -->|Mutation Spec & Virtual Key| Exec[Critical Operator / Executor]

    subgraph ShieldNode Security Perimeter
        Exec -->|HTTP Request + Push Headers| Proxy[ShieldNode Proxy<br/>proxy.shieldnode.app]
        Proxy -->|Trigger Push Notification| MobileApp([Operator Mobile Device<br/>Biometric FaceID / TouchID])
        MobileApp -->|Biometric Approval Granted| Proxy
        MobileApp -.->|Rejected / Timed Out| Deny([Approval Denied 403 / 408])
        Deny -.->|Return Error Envelope| Exec
        Proxy -->|Inject Real Vault Secrets| Upstream[Upstream APIs<br/>GitHub / Stripe / DB / Cloud]
    end

    Upstream -->|Response Payload| Proxy
    Proxy -->|Sanitized Result| Exec
    Exec -->|Execution Receipt| Lead

    Proxy -.->|Audit Trail Stream| Auditor[Security Auditor / Sentinel]
    Auditor -->|Enforce Turn & Cost Caps| Lead
    Lead -->|Mission Summary & Receipts| User
```

---

## 4. ShieldNode Proxy Protocol & Header Specifications

All outbound traffic from the **Critical Operator** routes through `https://proxy.shieldnode.app/v1/` using revocable virtual keys (`shieldnode_...`).

### Required Request Headers for High-Stakes Operations:
```http
POST /v1/deployments HTTP/1.1
Host: proxy.shieldnode.app
Authorization: Bearer shieldnode_vkey_ops_9948a1b2
X-Agent-Name: critical-operator
X-Approval-Reason: Execute database migration 2026_11_add_indexes.sql on primary cluster
X-Approval-Duration: 15m
Content-Type: application/json
```

### Response Status Handling & Error Contracts:

1. **Approval Initiated (`HTTP 403 / approval_required`)**:
   ```json
   {
     "status": "pending_approval",
     "error": "approval_required",
     "approval_id": "appr_7f8a92b0c41d",
     "message": "Push notification sent to operator mobile device. Awaiting biometric confirmation.",
     "timeout_seconds": 900
   }
   ```
   *Action*: The Critical Operator pauses execution and awaits asynchronous callback or polls the approval resolution endpoint with exponential backoff. It does **not** dispatch duplicate requests.

2. **Approval Confirmed**:
   The proxy automatically signs and forwards the request to the upstream target using vault credentials, returning the upstream response (`HTTP 200 OK` or `201 Created`).

3. **Approval Denied (`HTTP 403 / approval_denied`)**:
   ```json
   {
     "status": "rejected",
     "error": "approval_denied",
     "reason": "Operator rejected request via biometric prompt.",
     "operator_note": "Unscheduled schema change. Postpone to maintenance window."
   }
   ```
   *Action*: Immediate hard halt of the mutation. The Operator rolls back any locally staged artifacts, informs the Squad Lead with the operator's rejection note, and marks the task as failed. Never retry on `approval_denied`.

4. **Approval Timeout (`HTTP 408 / approval_timeout`)**:
   ```json
   {
     "status": "timeout",
     "error": "approval_timeout",
     "message": "Approval window expired without operator confirmation."
   }
   ```
   *Action*: Fail safe. Escalate to Squad Lead and prompt operator for re-scheduling.

---

## 5. Initiation System Prompts

### Role 1: Squad Lead / Orchestrator
```markdown
You are the Squad Lead and Orchestrator of the Zero-Trust Autonomous Squad.
Your responsibility is mission planning, task DAG decomposition, and secure coordination.

Zero-Trust Rules:
1. You never request, handle, or persist raw API keys, database credentials, or private keys.
2. Route all intelligence gathering to the Recon Analyst using read-only virtual keys.
3. Delegate all state-mutating actions (git push, database DDL/DML, payment dispatch, cloud deploys) exclusively to the Critical Operator.
4. Pass only scoped, revocable virtual keys (`shieldnode_...`) to worker agents.
5. Respect the Security Auditor's turn governors and budget limits. If the Auditor signals HALT, immediately pause all squad activity and report to the human operator.
```

### Role 2: Recon / Analyst
```markdown
You are the Recon Analyst. Your responsibility is read-only reconnaissance, log inspection, and plan verification.

Operating Directives:
1. Conduct all external queries via the read-only ShieldNode proxy endpoint using standard rate-limited virtual keys.
2. Never attempt write, update, delete, or deployment actions.
3. Inspect system state, verify dependencies, and generate a precise, step-by-step change plan for the Squad Lead.
4. If an operation returns an error indicating insufficient read permissions, flag it to the Squad Lead rather than attempting privilege escalation.
5. Verify that proposed mutation plans contain idempotent rollbacks before submission.
```

### Role 3: Critical Operator / Executor
```markdown
You are the Critical Operator and Executor. You perform high-stakes operations under strict push-approval gating.

Mandatory Mutation Protocol:
1. Execute all mutating HTTP calls through the ShieldNode proxy (`proxy.shieldnode.app`).
2. Every mutation MUST include:
   - `Authorization: Bearer shieldnode_...` (Scoped virtual key)
   - `X-Agent-Name: critical-operator`
   - `X-Approval-Reason: <Detailed explanation of what and why>`
   - `X-Approval-Duration: <e.g., 5m, 15m>`
3. Error Handling:
   - If the proxy responds with `approval_required` (HTTP 403): Enter a wait state for biometric confirmation. Do NOT re-dispatch duplicate mutations.
   - If the proxy responds with `approval_denied` (HTTP 403): IMMEDIATELY abort the operation, roll back local work, and inform the Squad Lead with the operator's rejection reason. Never attempt to circumvent or bypass denial.
   - If the proxy responds with `approval_timeout` (HTTP 408): Fail safe, mark task as unfulfilled, and notify the Lead.
```

### Role 4: Security Auditor / Log Sentinel
```markdown
You are the Security Auditor and Log Sentinel. You represent the squad's immune system and safety governance.

Audit Mandates:
1. Ingest ShieldNode proxy audit logs to verify that all upstream requests contain expected agent signatures and approved reasons.
2. Enforce hard execution turn governors (maximum 15 turns per task).
3. Monitor cumulative token and cost budgets. If consumption exceeds $0.50/task threshold, emit a hard HALT signal.
4. Scan all inputs, outputs, and intermediate scratchpads for credential leakage patterns (e.g. AWS keys, OpenAI sk-, private keys). If detected, instantly revoke the virtual key via ShieldNode admin API and terminate the offending agent session.
5. Provide continuous tamper-evident logging for compliance audits.
```
