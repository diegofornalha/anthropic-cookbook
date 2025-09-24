---
allowed-tools: Bash(gh pr comment:*),Bash(gh pr diff:*),Bash(gh pr view:*)
Descrição: Comprehensive review of Jupyter notebooks and Python scripts
---

Review the changes to Jupyter notebooks and Python scripts in this PR. Please check para:

## Code Quality
- Python code follows PEP 8 conventions
- Proper Erro handling
- Clear variable names and documentation
- No hardcoded api keys (use os.getenv("ANTHROPIC_API_KEY"))

## Notebook Structure
- Clear introduction explaining what the notebook demonstrates and why isso's useful
- Configuração instructions (how to definir up api keys, install Dependências, etc.)
- Connecting explanations between cells that help users understand the flow
- Clear markdown explanations between code cells
- Logical flow from simple to complex
- Outputs preserved para educational value
- Dependências properly imported

## Security
- Check para any hardcoded api keys or secrets (not just Anthropic keys)
- Ensure all sensitive credentials use environment variables (os.environ, getenv, etc.)
- Flag any potential secret patterns (tokens, passwords, privado keys)
- NOTA: Educational Exemplos showing "what not to do" are acceptable se clearly marked
- Safe handling of user inputs
- Appropriate use of environment variables

Provide a clear summary with:
- ✅ What looks good
- ⚠️ Suggestions para improvement
- ❌ Crítico issues that must be fixed

**IMPORTANT: Post your review as a comment on the pull request using the command: `gh pr comment $PR_NUMBER --body "your review"`**