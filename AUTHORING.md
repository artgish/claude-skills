# Authoring skills

A short field guide for writing skills people will actually use.

## The shape

```
skills/your-skill/
├── SKILL.md          # required
├── references/       # optional — long docs loaded on demand
├── scripts/          # optional — executable helpers
└── assets/           # optional — templates, fixtures
```

## The frontmatter is doing most of the work

Claude doesn't read the body of every skill. It scans names and descriptions, then loads the body of skills whose description seems to match. The description is your trigger — write it like a job ad.

```markdown
---
name: kubernetes-pod-owner-tracer
description: Walks a Kubernetes pod's ownerReferences chain to find the root workload (Deployment, StatefulSet, DaemonSet, Job, CronJob). Use this whenever the user is debugging which workload owns a pod, tracing pod provenance, or writing Go code that resolves ownerReferences (e.g., a getPodOwnerName helper). Trigger even when the user only says "find the deployment for this pod" or "what created this pod".
---
```

Note what's happening there: the description names the **task**, the **concrete signals** (`ownerReferences`, `getPodOwnerName`), and **paraphrases the user might use** ("find the deployment for this pod"). Claude undertriggers skills, so err on the side of being explicit and slightly pushy.

## Keep SKILL.md focused

- Aim for under 500 lines of body. If you need more, push detail into `references/` and tell Claude when to read each file.
- Lead with the workflow, then edge cases, then references.
- Show, don't just tell — concrete examples beat abstract rules.
- If the skill has a deterministic step (regex, parsing, file transform), put it in `scripts/` rather than asking Claude to redo it in prose every time.

## Naming

- Folder name = `name:` in frontmatter, kebab-case (e.g., `terraform-for-debugger`).
- Prefix with a domain when it helps disambiguate: `cloudchipr-soc2-responder`, `azure-apim-llm-observability`.

## Things that don't belong in a skill

- Secrets, API keys, internal hostnames, customer names.
- One-shot scripts you'll never run again — write those in a chat, not a skill.
- Anything you wouldn't be comfortable open-sourcing if the repo flipped public. (This one's public, but adopt the habit.)

## Testing locally

Before opening a PR:

```bash
python scripts/validate.py skills/your-skill
python scripts/package.py skills/your-skill
./scripts/install-all.sh
```

Then open Claude Code and try a prompt that *should* trigger your skill, plus one that shouldn't, to make sure the description isn't over- or under-firing.

## More background

- [Claude Code skills docs](https://docs.claude.com/en/docs/claude-code/skills)
- The `skill-creator` skill bundled with Claude Code has a deeper guide and an iteration loop for tuning descriptions against test prompts. Worth running if your skill keeps mis-triggering.
