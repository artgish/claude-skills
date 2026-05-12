---
name: git-commit
description: Stage all changes, generate a short commit message, commit, and push to the current branch
disable-model-invocation: true
allowed-tools: Bash(git *)
---

Perform a full git commit and push workflow:

1. Stage all changes:

   ```bash
   git add .
   ```

2. Review the staged changes to understand what was modified:

   ```bash
   git diff --cached --stat
   ```

   ```bash
   git diff --cached
   ```

3. Based on the diff, generate a short commit message (max 15 words) that summarizes the changes. Then commit:

   ```bash
   git commit -m "GENERATED_COMMIT_MESSAGE"
   ```

4. Get the current branch name:

   ```bash
   git branch --show-current
   ```

5. Push to remote:

   ```bash
   git push origin RESOLVED_BRANCH_NAME
   ```
