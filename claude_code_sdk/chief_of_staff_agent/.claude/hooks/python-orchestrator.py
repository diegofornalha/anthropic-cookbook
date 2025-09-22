#!/usr/bin/env python3
"""
Orquestrador Principal de Hooks Python
Gerencia execução automática de todos os scripts de avaliação
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Cores para output
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
RESET = '\033[0m'
BOLD = '\033[1m'

class PythonHookOrchestrator:
    """Orquestra execução de todos os hooks Python"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.hooks_dir = Path(__file__).parent / "scripts"
        self.results = {}

    def should_run_hooks(self) -> bool:
        """Determina se deve executar hooks para este arquivo"""

        # Sempre executa para arquivos Python
        if not self.file_path.endswith('.py'):
            return False

        # Pula arquivos do próprio sistema de hooks
        if '.claude/hooks' in self.file_path:
            return False

        # Pula arquivos de configuração
        if any(x in self.file_path for x in ['setup.py', '__pycache__', '.pyc']):
            return False

        return True

    def detect_evaluation_type(self) -> str:
        """Detecta que tipo de avaliação aplicar baseado no contexto"""

        file_name = Path(self.file_path).name.lower()

        # Detecta por nome do arquivo
        if 'candidate' in file_name or 'submission' in file_name:
            return 'full_evaluation'  # Avaliação completa para candidatos
        elif 'cache' in file_name:
            return 'cache_focused'    # Foco em cache
        elif 'test_' in file_name:
            return 'test_validation'  # Validação de testes
        elif 'agent' in file_name or 'ai' in file_name:
            return 'ai_evaluation'    # Avaliação de IA/ML
        else:
            return 'quality_check'    # Check de qualidade padrão

    def run_hook_script(self, script_name: str, args: list = None) -> dict:
        """Executa um script de hook específico"""

        script_path = self.hooks_dir / script_name

        if not script_path.exists():
            return {"status": "skipped", "reason": "script not found"}

        try:
            cmd = ['python3', str(script_path)]
            if args:
                cmd.extend(args)
            else:
                cmd.append(self.file_path)

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # Timeout de 30 segundos
            )

            return {
                "status": "success" if result.returncode == 0 else "failed",
                "returncode": result.returncode,
                "output": result.stdout,
                "error": result.stderr
            }

        except subprocess.TimeoutExpired:
            return {"status": "timeout", "error": "Execution exceeded 30 seconds"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def orchestrate_evaluation(self) -> dict:
        """Orquestra a execução de múltiplos hooks baseado no contexto"""

        eval_type = self.detect_evaluation_type()

        print(f"\n{BOLD}🎯 PYTHON HOOK ORCHESTRATOR{RESET}")
        print(f"{'='*50}")
        print(f"📄 File: {Path(self.file_path).name}")
        print(f"🔍 Type: {eval_type}")
        print(f"{'='*50}\n")

        results = {
            "file": self.file_path,
            "evaluation_type": eval_type,
            "timestamp": datetime.now().isoformat(),
            "hooks_executed": [],
            "overall_status": "pending"
        }

        # Define sequência de hooks baseado no tipo
        if eval_type == 'full_evaluation':
            # Avaliação completa para candidatos
            hooks_sequence = [
                ("python-quality-synergy.py", ["auto-fix"]),
                ("ai_expertise_evaluator.py", []),
                ("talent_scorer.py", []),
                ("decision_matrix.py", [])
            ]
        elif eval_type == 'cache_focused':
            hooks_sequence = [
                ("cache_evaluation.py", []),
                ("python-quality-synergy.py", ["permissive"])
            ]
        elif eval_type == 'ai_evaluation':
            hooks_sequence = [
                ("ai_expertise_evaluator.py", []),
                ("python-quality-synergy.py", ["strict"])
            ]
        else:
            # Quality check básico
            hooks_sequence = [
                ("python-quality-synergy.py", ["permissive"])
            ]

        # Executa hooks em sequência
        all_passed = True
        for hook_script, args in hooks_sequence:
            print(f"{CYAN}▶ Executando: {hook_script}{RESET}")

            full_args = [self.file_path] + args if args else None
            result = self.run_hook_script(hook_script, full_args)

            results["hooks_executed"].append({
                "hook": hook_script,
                "result": result
            })

            if result["status"] == "success":
                print(f"  {GREEN}✅ Passed{RESET}")
            elif result["status"] == "skipped":
                print(f"  {YELLOW}⏭️  Skipped{RESET}")
            else:
                print(f"  {RED}❌ Failed{RESET}")
                all_passed = False

                # Se crítico, para execução
                if eval_type == 'full_evaluation' and 'quality' in hook_script:
                    print(f"\n{RED}⛔ Avaliação interrompida devido a falha crítica{RESET}")
                    break

        # Decisão final
        results["overall_status"] = "passed" if all_passed else "failed"

        # Salva resultado no Neo4j
        self.save_to_neo4j(results)

        # Output final
        print(f"\n{'='*50}")
        if all_passed:
            print(f"{GREEN}{BOLD}✅ AVALIAÇÃO COMPLETA - APROVADO{RESET}")
        else:
            print(f"{RED}{BOLD}❌ AVALIAÇÃO COMPLETA - REPROVADO{RESET}")
        print(f"{'='*50}\n")

        return results

    def save_to_neo4j(self, results: dict):
        """Salva resultados no Neo4j para aprendizado"""

        # Simula salvamento no Neo4j
        print(f"\n{PURPLE}💾 Salvando no Neo4j...{RESET}")

        learning_data = {
            "file": Path(results["file"]).name,
            "type": results["evaluation_type"],
            "status": results["overall_status"],
            "hooks_count": len(results["hooks_executed"]),
            "timestamp": results["timestamp"]
        }

        print(f"  📊 Tipo: {learning_data['type']}")
        print(f"  🎯 Status: {learning_data['status']}")
        print(f"  🔢 Hooks executados: {learning_data['hooks_count']}")


def main():
    """Função principal"""

    if len(sys.argv) < 2:
        sys.exit(0)

    file_path = sys.argv[1]

    orchestrator = PythonHookOrchestrator(file_path)

    if not orchestrator.should_run_hooks():
        print(f"⏭️ Skipping hooks for {Path(file_path).name}")
        sys.exit(0)

    results = orchestrator.orchestrate_evaluation()

    # Retorna código baseado no resultado
    if results["overall_status"] == "passed":
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()