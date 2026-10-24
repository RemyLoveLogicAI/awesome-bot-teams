# Template: Cyber Security & Smart Contract Red Team

> **Topology**: Recon -> Exploitation Sandbox -> Defense Verification  
> **Ideal For**: Code security reviews, API fuzzing, smart contract audits, CVE analysis, and penetration testing simulations.

---

## 1. Roster & Roles

| Role | Responsibility | Input | Output | Tools / Permissions |
|------|---------------|-------|--------|---------------------|
| **Recon & Threat Modeler** | Maps attack surface, dependency vulnerabilities, and privileged endpoints. | Target codebase / Architecture diagram | Threat model & STRIDE matrix | AST parser, dependency scanner, SAST |
| **Exploit & Fuzzing Specialist** | Crafts edge case inputs, explores race conditions, simulates malicious transactions in isolated sandboxes. | Threat model & candidate endpoints | Proof-of-concept (PoC) exploit scripts | Local container sandbox, fuzzer |
| **Remediation & Patch Engineer** | Formulates defensive countermeasures, refactors vulnerable logic, adds boundary constraints. | Validated PoC exploits | Hardened patches & regression tests | Git edit, compiler, test harness |
| **Audit Lead** | Scores findings against CVSS / OWASP standards, writes audit report with executive mitigation steps. | Verified patch & PoC validation | Formal security audit report | Report generator |
