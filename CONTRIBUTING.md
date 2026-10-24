# Contribution Guidelines

Thank you for contributing to **Awesome Bot Teams**!

Please follow these guidelines to keep this list high-quality and useful for everyone deploying bot squads and agent teams.

---

### Criteria for Inclusion

1. **Working & Reproducible**: Teams, bots, frameworks, or templates submitted should be actively maintained, runnable, and documented.
2. **Clear Architecture or Role Specification**: Entries should clearly indicate what the bot or team does, how communication is handled, and what role boundaries exist.
3. **Format**: Follow the existing Markdown schema:
   - `- [Project Name](url) - Concise description highlighting its team architecture or role capability.`
4. **Awesome Standard**: Keep listings alphabetized within their categories and check spelling/links before submitting.

---

### Proposing a New Team Template

If you are adding a template to `templates/`:
- Include a descriptive markdown or YAML specification.
- Specify:
  - Team Objective
  - Roles & Capabilities
  - Topology (Hierarchical, Peer-to-Peer, Blackboard, Pipeline)
  - Initialization Prompts / System Seeds
  - Handoff & Completion Protocols
  - Guardrails & Safety Brakes

---

### Submitting a Pull Request

1. Fork the repo and create your branch from `main`:
   ```bash
   git checkout -b add/my-bot-team
   ```
2. Add your entry or template in the relevant section.
3. Ensure markdown links are valid.
4. Open a Pull Request with a clear title and description of the tool or team setup.
