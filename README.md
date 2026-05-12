# Claude Skills

Shared [Claude Code](https://docs.claude.com/en/docs/claude-code/overview) skills. Skills are reusable instruction bundles that teach Claude how to handle recurring tasks — compliance docs, Kubernetes diagnostics, Terraform patterns, internal runbooks, etc.

This repo holds the source for our skills and publishes them as installable `.skill` files (zip archives) on the [Releases](../../releases) page.

## Install a skill

1. Grab the latest `<skill-name>.skill` from [Releases](../../releases) (or `dist/` on `main`).
2. Drop it into your Claude Code skills directory:

   ```bash
   # macOS / Linux
   mkdir -p ~/.claude/skills
   unzip -o some-skill.skill -d ~/.claude/skills/
   ```

   `.skill` files are plain zips — `unzip` is enough. The archive expands into `~/.claude/skills/<skill-name>/`.

3. Restart Claude Code (or open a new session). Claude will pick the skill up automatically when it matches a task.

> Prefer to install everything at once? See [`scripts/install-all.sh`](scripts/install-all.sh).

## What's in a skill

Every skill is a folder containing at minimum a `SKILL.md` with YAML frontmatter:

```
my-skill/
├── SKILL.md          # required — frontmatter + instructions
├── scripts/          # optional — executable helpers
├── references/       # optional — docs Claude loads on demand
└── assets/           # optional — templates, fixtures, etc.
```

The `SKILL.md` frontmatter must include `name` and `description`. The `description` is what Claude reads to decide whether to use the skill, so be specific about _when_ it should trigger.

Example:

```markdown
---
name: soc2-responder
description: Drafts SOC 2 questionnaire responses in formal voice and format. Use whenever the user is filling out a security questionnaire, responding to a customer's compliance request, or writing SOC 2 system description content.
---

# SOC 2 Responder

...
```

See Anthropic's [skill authoring guide](https://docs.claude.com/en/docs/claude-code/skills) for the full spec.

## Add a new skill

1. Create a branch.
2. Add a folder under `skills/` — `skills/my-new-skill/SKILL.md` at minimum.
3. Validate locally:

   ```bash
   python scripts/validate.py skills/my-new-skill
   ```

4. Optionally package it to test the install flow:

   ```bash
   python scripts/package.py skills/my-new-skill
   # → dist/my-new-skill.skill
   ```

5. Open a PR. CI runs validation and packages all skills; on merge to `main`, packaged `.skill` files are attached to a release.

## Update an existing skill

Keep the folder name and the `name:` field in frontmatter stable — that's how installed copies get overwritten cleanly. Bump version notes in the PR description; the changelog lives in releases.

## Repository layout

```
.
├── skills/              # source skills, one folder each
├── scripts/
│   ├── package.py       # zip a skill folder into <name>.skill
│   ├── validate.py      # check SKILL.md frontmatter and structure
│   ├── package-all.sh   # package every skill into dist/
│   └── install-all.sh   # install every .skill in dist/ to ~/.claude/skills/
├── dist/                # built .skill files (gitignored)
└── .github/workflows/
    └── release.yml      # validates on PR, releases on tag
```

## Conventions

- **Naming**: kebab-case folder names matching the `name:` in frontmatter (e.g., `terraform-for-debugger`).
- **Scope**: prefer one skill per task type. Splitting is cheap; merging later is fine too.
- **Secrets**: never. No credentials, internal URLs, or customer data in skills — they ship to laptops.
- **Languages**: skills are English. Cross-language tasks (Armenian/Russian/English) belong inside the instructions, not as separate skills.

## Questions

Ping `#platform` on Slack or open an issue.
