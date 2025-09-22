#!/usr/bin/env python3
"""
Hook Automático Inteligente para Python
Executa APENAS em contextos apropriados
"""

import sys
import os
import json
from pathlib import Path

# Configuração do que deve ser validado automaticamente
AUTO_VALIDATE_PATTERNS = [
    'candidate_*.py',      # Arquivos de candidatos
    'submission_*.py',     # Submissões
    'test_*.py',          # Arquivos de teste
    '*_evaluation.py',    # Avaliações
]

# Scripts disponíveis para execução condicional
AVAILABLE_VALIDATORS = {
    'quality': '.claude/commands/scripts/python-quality-synergy.py',
    'cache': '.claude/commands/scripts/cache_evaluation.py',
    'ai_expertise': '.claude/commands/scripts/ai_expertise_evaluator.py',
}

def should_auto_validate(file_path: str) -> bool:
    """Determina se arquivo deve ser validado automaticamente"""

    file_name = Path(file_path).name

    # Verifica se match com patterns
    for pattern in AUTO_VALIDATE_PATTERNS:
        if pattern.startswith('*'):
            if file_name.endswith(pattern[1:]):
                return True
        elif pattern.endswith('*'):
            if file_name.startswith(pattern[:-1]):
                return True
        elif file_name == pattern:
            return True

    # Verifica se tem marker no arquivo
    try:
        with open(file_path, 'r') as f:
            first_lines = f.read(500)
            if '# AUTO_EVALUATE' in first_lines or '# CANDIDATE_CODE' in first_lines:
                return True
    except:
        pass

    return False

def detect_validation_type(file_path: str) -> str:
    """Detecta qual tipo de validação aplicar"""

    file_name = Path(file_path).name.lower()

    if 'cache' in file_name:
        return 'cache'
    elif 'ai' in file_name or 'agent' in file_name:
        return 'ai_expertise'
    else:
        return 'quality'

def main():
    if len(sys.argv) < 2:
        sys.exit(0)  # Silently exit

    file_path = sys.argv[1]

    # Verifica se é Python
    if not file_path.endswith('.py'):
        sys.exit(0)

    # Verifica se deve validar
    if not should_auto_validate(file_path):
        print(f"⏭️ Skipping auto-validation for {Path(file_path).name}")
        sys.exit(0)

    # Detecta tipo de validação
    validation_type = detect_validation_type(file_path)
    validator_script = AVAILABLE_VALIDATORS.get(validation_type)

    if validator_script:
        print(f"🎯 Auto-validating {Path(file_path).name} with {validation_type} validator")

        # Executa validador apropriado
        import subprocess
        result = subprocess.run(
            ['python3', validator_script, file_path, 'auto'],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ Validation failed!")
            print(result.stdout)
            sys.exit(1)
        else:
            print(f"✅ Validation passed!")
            sys.exit(0)

    sys.exit(0)

if __name__ == "__main__":
    main()