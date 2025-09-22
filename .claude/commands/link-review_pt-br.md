---
allowed-tools: Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*)
description: Review links in changed arquivos for quality e segurança issues
---

Review the links in the changed arquivos e verificar for potential issues:

## link Quality Checks
1. **Broken Links**: Identify any links aquele might be broken ou malformed
2. **Outdated Links**: verificar for links para depreciado resources ou antigo Documentação
3. **segurança**: Ensure no links para suspicious ou potentially harmful sites
4. **Best Practices**: 
   - Links should use HTTPS onde possible
   - interno links should use relative paths
   - externo links should be para estável, reputable sources

## Specific Checks for Anthropic Content
- Links para Claude Documentação should point para the mais recente versions
- API Documentação links should be atual
- Model Documentação should reference atual models, não depreciado ones
- GitHub links should use the correct repositório paths

## relatório Format
Provide a limpar summary com:
- ✅ Valid e well-formed links
- ⚠️ Links aquele might need attention (e.g., HTTP instead of HTTPS)
- ❌ Broken ou problematic links aquele must be fixed

se todos links look good, provide a brief confirmation.

**Importante: Post your review as a comment on the pull requisição using the comando: `gh pr comment $PR_NUMBER --body "your review content"`**