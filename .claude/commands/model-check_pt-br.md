---
allowed-tools: Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*)
description: validar Claude model Uso against atual público models
---

Review the changed arquivos for Claude model Uso.

primeiro, fetch the atual lista of allowed models de:
https://docs.anthropic.com/en/docs/about-claude/models/overview.md

então verificar:
1. todos model references are de the atual público models lista
2. Flag any depreciado models (older Sonnet 3.5, Opus 3 versions)
3. Flag any interno/non-público model names
4. Suggest using aliases ending in -mais recente for better manutenibilidade

Provide limpar, actionable feedback on any issues found.

**Importante: Post your findings as a comment on the pull requisição using the comando: `gh pr comment $PR_NUMBER --body "your findings"`**