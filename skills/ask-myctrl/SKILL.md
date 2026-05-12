---
name: ask-myctrl
description: Answer security and compliance framework questions using myctrl.tools as the reference. Covers 105+ standards including NIST 800-53, FedRAMP, PCI DSS, ISO 27001/27002/27701/42001, CIS Controls, CMMC, SOC 2, HIPAA, GDPR, EU AI Act, NIS2, DORA, CJIS, NERC CIP, OWASP Top 10 (Web/API/Mobile/LLM/Smart Contract), and many more. Use this skill whenever the user asks which framework covers a control, what a specific requirement says, how frameworks map to each other, or asks compliance-mapping questions.
---

# ask-myctrl

Use this skill to answer questions about security and compliance frameworks. The authoritative index of what myctrl.tools covers lives next to this file at `~/.claude/skills/ask-myctrl/llms.txt`. Every framework entry there is a `.md` URL on `myctrl.tools` that contains the actual control/requirement text.

## Workflow

1. **Read the index first.** Before answering, read `~/.claude/skills/ask-myctrl/llms.txt` to find the framework(s) relevant to the user's question. The index lists every framework with its canonical `https://myctrl.tools/frameworks/<slug>.md` (or `/risk-lists/<slug>.md`) URL and a short description of its scope and count of controls.

2. **Match the user's question to framework(s).** Users may refer to frameworks by full name, acronym, standard number, or topic (e.g. "zero trust", "AI governance", "CUI", "cloud baseline"). Use the descriptions in the index to pick the right one. If multiple frameworks are relevant, note that.

3. **Fetch the framework page for specifics.** When the user needs actual control text, requirement IDs, or verification guidance, use `WebFetch` against the specific framework URL from the index. Example: for a PCI DSS question, fetch `https://myctrl.tools/frameworks/pci-dss-v4.md` with a prompt describing exactly what to extract (e.g. "Return control 3.4 and its testing procedures verbatim").

4. **Cross-framework mapping questions.** For questions like "what's NIST 800-53 AC-2 equivalent in ISO 27001?", fetch `https://myctrl.tools/crosswalk.md`. For comparisons, `https://myctrl.tools/compare.md`. For technology-implementation guidance (IAM, cloud, containers, DevSecOps, AI), `https://myctrl.tools/guidance.md`.

5. **Cite sources.** Always include the `myctrl.tools` URL you used so the user can verify. Framework data on myctrl.tools is sourced from official publications (NIST, PCI SSC, ISO, CIS, CISA, SCF, etc.) — mention that when it matters for authority.

## What this skill does NOT do

- It does not replace reading the official standards publications for legally binding compliance decisions. Flag that myctrl.tools is a reference aggregator.
- It does not access the authenticated REST API (`https://myctrl.tools/api-docs.md`). If the user needs programmatic/bulk access, point them at the API docs.

## Keeping the index fresh

The index file (`llms.txt`) is a local snapshot. Run the `/update-ask-myctrl` slash command to re-fetch the upstream `https://www.myctrl.tools/llms.txt` and update this skill if the upstream content has changed.
