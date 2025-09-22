#!/usr/bin/env python3
"""
Hook avançado para rastreamento e aprendizado com notebooks do Cookbook
Integra com Neo4j para criar memória de padrões e melhores práticas
"""

import json
import os
import sys
import re
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

def main():
    # Receber dados do hook
    hook_data = json.loads(sys.stdin.read())

    # Extrair informações relevantes
    tool_name = hook_data.get("toolName", "")
    tool_input = hook_data.get("toolInput", {})
    tool_result = hook_data.get("toolResult", {})

    # Diretório para logs
    log_dir = Path("/Users/2a/.claude/anthropic-cookbook/.claude/logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Múltiplos arquivos de tracking
    tracking_file = log_dir / "notebook_usage.json"
    patterns_file = log_dir / "learned_patterns.json"
    metrics_file = log_dir / "usage_metrics.json"
    insights_file = log_dir / "cookbook_insights.json"

    # Processar evento
    if should_track(tool_name, tool_input):
        # Rastrear uso
        entry = create_tracking_entry(tool_name, tool_input, tool_result)
        update_tracking(tracking_file, entry)

        # Aprender padrões
        patterns = extract_patterns(tool_name, tool_input, tool_result)
        if patterns:
            update_patterns(patterns_file, patterns)

        # Atualizar métricas
        update_metrics(metrics_file, entry)

        # Gerar insights
        insights = generate_insights(tracking_file, patterns_file)
        if insights:
            save_insights(insights_file, insights)

        # Enviar para Neo4j (se configurado)
        send_to_neo4j(entry, patterns, insights)

        # Feedback contextual
        provide_contextual_feedback(entry, patterns)

    # Permitir execução
    return 0

def should_track(tool_name: str, tool_input: dict) -> bool:
    """Determina se o evento deve ser rastreado"""
    # Tools relevantes
    relevant_tools = ["Read", "NotebookEdit", "Bash", "Write", "Edit", "MultiEdit"]
    if tool_name not in relevant_tools:
        return False

    # Verificar se é relacionado ao Cookbook
    file_path = extract_file_path(tool_input)
    if file_path:
        path_str = str(file_path).lower()
        cookbook_indicators = [
            ".ipynb", "jupyter", "notebook",
            "anthropic-cookbook", "claude_code_sdk",
            "example", "demo", "tutorial"
        ]
        return any(ind in path_str for ind in cookbook_indicators)

    # Comandos relevantes
    command = tool_input.get("command", "").lower()
    return any(kw in command for kw in ["python", "jupyter", "notebook", "ipynb"])

def create_tracking_entry(tool_name: str, tool_input: dict, tool_result: dict) -> dict:
    """Cria entrada detalhada de tracking"""
    file_path = extract_file_path(tool_input)
    content = extract_content(tool_input, tool_result)

    entry = {
        "id": generate_id(),
        "timestamp": datetime.now().isoformat(),
        "tool": tool_name,
        "file": str(file_path) if file_path else "unknown",
        "category": detect_category(file_path),
        "action": detect_action(tool_name, tool_input),
        "technique": detect_technique(content),
        "complexity": assess_complexity(content),
        "modifications": detect_modifications(tool_name, tool_input),
        "patterns_used": detect_patterns_in_code(content),
        "sdk_migration": detect_sdk_migration(content),
        "success": determine_success(tool_result),
        "session_id": get_session_id(),
    }

    return entry

def extract_patterns(tool_name: str, tool_input: dict, tool_result: dict) -> List[dict]:
    """Extrai padrões de uso e aprendizados"""
    patterns = []
    content = extract_content(tool_input, tool_result)

    if not content:
        return patterns

    # Padrões de código
    code_patterns = {
        "async_pattern": r"async\s+def|await\s+",
        "sdk_client": r"ClaudeSDKClient|ClaudeCodeOptions",
        "query_pattern": r"query\(|async\s+for.*in\s+query",
        "tool_use": r"allowed_tools\s*=\s*\[",
        "system_prompt": r"system_prompt\s*=",
        "neo4j_integration": r"neo4j|graph|GraphRAG",
        "error_handling": r"try:|except\s+\w+:|finally:",
        "type_hints": r"->\s*\w+|:\s*\w+\[|from\s+typing\s+import",
        "decorators": r"@\w+",
        "context_managers": r"with\s+.*as\s+",
    }

    for pattern_name, pattern_regex in code_patterns.items():
        matches = re.findall(pattern_regex, content, re.MULTILINE | re.IGNORECASE)
        if matches:
            patterns.append({
                "name": pattern_name,
                "count": len(matches),
                "examples": matches[:3],  # Primeiros 3 exemplos
                "timestamp": datetime.now().isoformat(),
                "context": detect_category(extract_file_path(tool_input)),
            })

    # Padrões de migração
    migration_patterns = detect_migration_patterns(content)
    patterns.extend(migration_patterns)

    return patterns

def detect_migration_patterns(content: str) -> List[dict]:
    """Detecta padrões de migração de API para SDK"""
    patterns = []

    # Antes e depois
    migrations = {
        "api_to_sdk": {
            "before": r"anthropic\.Anthropic\(",
            "after": r"ClaudeSDKClient\(",
        },
        "sync_to_async": {
            "before": r"def\s+\w+\(",
            "after": r"async\s+def\s+\w+\(",
        },
        "messages_to_query": {
            "before": r"messages\.create\(",
            "after": r"query\(",
        },
    }

    for pattern_name, checks in migrations.items():
        before_found = bool(re.search(checks["before"], content))
        after_found = bool(re.search(checks["after"], content))

        if before_found or after_found:
            patterns.append({
                "name": f"migration_{pattern_name}",
                "migrated": after_found,
                "legacy": before_found,
                "timestamp": datetime.now().isoformat(),
            })

    return patterns

def update_metrics(metrics_file: Path, entry: dict):
    """Atualiza métricas de uso"""
    metrics = load_json(metrics_file, default={
        "total_uses": 0,
        "by_category": defaultdict(int),
        "by_action": defaultdict(int),
        "by_technique": defaultdict(int),
        "success_rate": {"success": 0, "total": 0},
        "daily_usage": defaultdict(int),
        "popular_notebooks": defaultdict(int),
        "sdk_adoption": {"sdk": 0, "api": 0},
    })

    # Atualizar contadores
    metrics["total_uses"] += 1
    metrics["by_category"][entry["category"]] += 1
    metrics["by_action"][entry["action"]] += 1
    metrics["by_technique"][entry["technique"]] += 1

    # Taxa de sucesso
    metrics["success_rate"]["total"] += 1
    if entry["success"]:
        metrics["success_rate"]["success"] += 1

    # Uso diário
    today = datetime.now().date().isoformat()
    metrics["daily_usage"][today] += 1

    # Notebooks populares
    if entry["file"] != "unknown":
        metrics["popular_notebooks"][Path(entry["file"]).name] += 1

    # Adoção do SDK
    if entry.get("sdk_migration"):
        if entry["sdk_migration"] == "sdk":
            metrics["sdk_adoption"]["sdk"] += 1
        else:
            metrics["sdk_adoption"]["api"] += 1

    # Calcular estatísticas derivadas
    metrics["calculated"] = {
        "success_percentage": (
            metrics["success_rate"]["success"] / metrics["success_rate"]["total"] * 100
            if metrics["success_rate"]["total"] > 0 else 0
        ),
        "sdk_percentage": (
            metrics["sdk_adoption"]["sdk"] /
            (metrics["sdk_adoption"]["sdk"] + metrics["sdk_adoption"]["api"]) * 100
            if (metrics["sdk_adoption"]["sdk"] + metrics["sdk_adoption"]["api"]) > 0 else 0
        ),
        "most_used_category": max(metrics["by_category"].items(), key=lambda x: x[1])[0]
            if metrics["by_category"] else "none",
        "most_popular_notebook": max(metrics["popular_notebooks"].items(), key=lambda x: x[1])[0]
            if metrics["popular_notebooks"] else "none",
    }

    save_json(metrics_file, metrics)

def generate_insights(tracking_file: Path, patterns_file: Path) -> List[dict]:
    """Gera insights baseados no histórico e padrões"""
    insights = []

    # Carregar dados
    history = load_json(tracking_file, [])
    patterns = load_json(patterns_file, [])

    if len(history) < 10:  # Precisa de dados suficientes
        return insights

    # Insight: Progressão de aprendizado
    complexity_over_time = analyze_complexity_progression(history)
    if complexity_over_time:
        insights.append({
            "type": "learning_progression",
            "message": "Usuário progredindo de exemplos simples para avançados",
            "data": complexity_over_time,
            "recommendation": "Considere explorar exemplos Expert level",
        })

    # Insight: Padrões frequentes
    frequent_patterns = analyze_frequent_patterns(patterns)
    if frequent_patterns:
        insights.append({
            "type": "common_patterns",
            "message": f"Padrões mais usados: {', '.join(frequent_patterns[:3])}",
            "data": frequent_patterns,
            "recommendation": "Otimize estes padrões para máxima eficiência",
        })

    # Insight: Migração SDK
    migration_status = analyze_migration_status(history)
    if migration_status["total"] > 0:
        insights.append({
            "type": "sdk_migration",
            "message": f"Migração SDK: {migration_status['percentage']:.1f}% completo",
            "data": migration_status,
            "recommendation": "Continue migrando exemplos legacy para SDK",
        })

    # Insight: Categorias exploradas
    explored_categories = analyze_categories(history)
    unexplored = set(["skills", "tool_use", "multimodal", "third_party", "claude_code_sdk"]) - \
                 set(explored_categories)
    if unexplored:
        insights.append({
            "type": "exploration",
            "message": f"Categorias não exploradas: {', '.join(unexplored)}",
            "data": {"explored": explored_categories, "unexplored": list(unexplored)},
            "recommendation": f"Explore exemplos em {list(unexplored)[0]}",
        })

    return insights

def send_to_neo4j(entry: dict, patterns: List[dict], insights: List[dict]):
    """Envia dados para Neo4j Memory"""
    # Esta função seria integrada com o MCP Neo4j
    # Por ora, apenas prepara os dados
    neo4j_data = {
        "node": {
            "label": "Learning",
            "properties": {
                "name": f"Cookbook_{entry['category']}_{entry['action']}",
                "timestamp": entry["timestamp"],
                "category": entry["category"],
                "technique": entry["technique"],
                "success": entry["success"],
                "file": entry["file"],
            }
        },
        "relationships": []
    }

    # Adicionar relacionamentos com padrões
    for pattern in patterns:
        neo4j_data["relationships"].append({
            "type": "USES_PATTERN",
            "target": pattern["name"],
            "properties": {"count": pattern.get("count", 1)}
        })

    # Registrar para processamento posterior
    neo4j_file = Path("/Users/2a/.claude/anthropic-cookbook/.claude/logs/neo4j_queue.json")
    queue = load_json(neo4j_file, [])
    queue.append(neo4j_data)
    save_json(neo4j_file, queue)

def provide_contextual_feedback(entry: dict, patterns: List[dict]):
    """Fornece feedback contextual baseado no uso"""
    messages = []

    # Feedback sobre categoria
    if entry["category"] == "claude_code_sdk":
        messages.append("🎆 Excelente! Usando exemplos do Claude Code SDK")
    elif entry["category"] == "skills" and entry["technique"] == "rag":
        messages.append("📊 Considere migrar para Neo4j GraphRAG para melhor performance")

    # Feedback sobre padrões
    if any(p["name"] == "sdk_client" for p in patterns):
        messages.append("✅ SDK detectado! Lembre-se: sem API keys")
    elif any(p["name"] == "api_to_sdk" and not p.get("migrated") for p in patterns):
        messages.append("⚠️  Código legacy detectado. Use: /migrate-to-sdk")

    # Feedback sobre complexidade
    if entry["complexity"] == "expert":
        messages.append("🏆 Nível Expert! Considere compartilhar seu aprendizado")
    elif entry["complexity"] == "beginner":
        messages.append("🌱 Começando bem! Próximo: exemplos intermediários")

    # Exibir mensagens
    if messages:
        print(f"\n📓 Notebook Insights:", file=sys.stderr)
        for msg in messages:
            print(f"   {msg}", file=sys.stderr)

# Funções auxiliares

def extract_file_path(tool_input: dict) -> Optional[Path]:
    """Extrai caminho do arquivo de diferentes inputs"""
    for key in ["file_path", "notebook_path", "path"]:
        if key in tool_input:
            return Path(tool_input[key])

    # Tentar extrair de comandos
    command = tool_input.get("command", "")
    match = re.search(r'([^\s]+\.(?:py|ipynb))', command)
    if match:
        return Path(match.group(1))

    return None

def extract_content(tool_input: dict, tool_result: dict) -> str:
    """Extrai conteúdo relevante"""
    # Tentar várias fontes
    content = tool_input.get("content", "")
    if not content:
        content = tool_input.get("new_string", "")
    if not content:
        content = tool_input.get("new_source", "")
    if not content and "edits" in tool_input:
        contents = [e.get("new_string", "") for e in tool_input["edits"]]
        content = " ".join(contents)
    if not content:
        content = tool_result.get("output", "")

    return content

def detect_category(file_path: Optional[Path]) -> str:
    """Detecta categoria aprimorada"""
    if not file_path:
        return "unknown"

    path_str = str(file_path).lower()

    # Mapeamento detalhado
    category_map = {
        "skills/retrieval_augmented_generation": "rag",
        "skills/classification": "classification",
        "skills/summarization": "summarization",
        "tool_use": "tool_use",
        "multimodal": "multimodal",
        "third_party": "third_party",
        "claude_code_sdk": "claude_code_sdk",
        "misc": "misc",
    }

    for pattern, category in category_map.items():
        if pattern in path_str:
            return category

    # Detecção por palavras-chave
    keywords = {
        "rag": ["rag", "retrieval", "augmented", "vector", "embedding"],
        "classification": ["classify", "classification", "categorize"],
        "summarization": ["summar", "abstract", "tldr"],
        "tool_use": ["tool", "function", "api", "integration"],
        "multimodal": ["image", "vision", "pdf", "chart", "visual"],
        "claude_code_sdk": ["sdk", "claudesdk", "claude_code"],
    }

    for category, words in keywords.items():
        if any(word in path_str for word in words):
            return category

    return "general"

def detect_action(tool_name: str, tool_input: dict) -> str:
    """Detecta ação detalhada"""
    actions = {
        "Read": "reading",
        "Write": "creating",
        "Edit": "editing",
        "MultiEdit": "refactoring",
        "NotebookEdit": "notebook_editing",
        "Bash": "executing",
    }

    base_action = actions.get(tool_name, "unknown")

    # Refinar baseado no contexto
    if tool_name == "Bash":
        command = tool_input.get("command", "").lower()
        if "jupyter" in command:
            return "jupyter_executing"
        elif "python" in command:
            return "python_executing"
        elif "pip" in command:
            return "installing"
        elif "test" in command:
            return "testing"

    return base_action

def detect_technique(content: str) -> str:
    """Detecta técnica principal usada"""
    if not content:
        return "unknown"

    techniques = {
        "rag": ["embedding", "vector", "retrieval", "similarity", "faiss", "voyage"],
        "graphrag": ["neo4j", "graph", "cypher", "node", "relationship"],
        "classification": ["classify", "predict", "label", "category"],
        "summarization": ["summarize", "abstract", "tldr", "summary"],
        "multimodal": ["image", "vision", "pdf", "ocr", "visual"],
        "tool_use": ["tool", "function_call", "api", "integration"],
        "async": ["async", "await", "asyncio", "concurrent"],
        "streaming": ["stream", "yield", "chunk", "realtime"],
    }

    content_lower = content.lower()
    for technique, keywords in techniques.items():
        if any(kw in content_lower for kw in keywords):
            return technique

    return "general"

def assess_complexity(content: str) -> str:
    """Avalia complexidade do código"""
    if not content:
        return "unknown"

    # Indicadores de complexidade
    beginner_indicators = [
        r"print\(",
        r"input\(",
        r"^\s*#.*simple",
        r"hello.*world",
    ]

    intermediate_indicators = [
        r"class\s+\w+",
        r"def\s+\w+.*->\s*\w+",
        r"try:.*except",
        r"with\s+.*as\s+",
    ]

    advanced_indicators = [
        r"async\s+def",
        r"yield\s+from",
        r"@\w+\.\w+",
        r"metaclass\s*=",
        r"Protocol\[",
    ]

    expert_indicators = [
        r"__\w+__.*Protocol",
        r"TypeVar\[",
        r"@contextmanager",
        r"async\s+with.*async\s+for",
        r"GraphRAG|neo4j",
    ]

    # Contar indicadores
    scores = {
        "beginner": sum(1 for p in beginner_indicators if re.search(p, content, re.M)),
        "intermediate": sum(1 for p in intermediate_indicators if re.search(p, content, re.M)),
        "advanced": sum(1 for p in advanced_indicators if re.search(p, content, re.M)),
        "expert": sum(1 for p in expert_indicators if re.search(p, content, re.M)),
    }

    # Retornar nível com maior pontuação
    return max(scores.items(), key=lambda x: x[1])[0] if any(scores.values()) else "intermediate"

def detect_modifications(tool_name: str, tool_input: dict) -> List[str]:
    """Detecta tipos de modificações feitas"""
    mods = []

    if tool_name in ["Edit", "MultiEdit", "NotebookEdit"]:
        old = tool_input.get("old_string", "")
        new = tool_input.get("new_string", "")

        if old and new:
            if "ANTHROPIC_API_KEY" in old and "ClaudeSDKClient" in new:
                mods.append("api_to_sdk_migration")
            if "def " in old and "async def" in new:
                mods.append("sync_to_async")
            if len(new) > len(old) * 1.5:
                mods.append("expansion")
            if len(new) < len(old) * 0.7:
                mods.append("simplification")

    return mods

def detect_patterns_in_code(content: str) -> List[str]:
    """Detecta padrões de design no código"""
    patterns = []

    pattern_detectors = {
        "singleton": r"class.*\(.*\):.*_instance\s*=\s*None",
        "factory": r"def\s+create_\w+|class\s+\w+Factory",
        "observer": r"subscribe|notify|observers?",
        "decorator": r"@\w+|def\s+\w+\(.*func.*\)",
        "context_manager": r"__enter__|__exit__|with\s+",
        "iterator": r"__iter__|__next__|yield\s+",
        "async_pattern": r"async\s+def|await\s+|asyncio",
    }

    for pattern_name, regex in pattern_detectors.items():
        if re.search(regex, content, re.M | re.I):
            patterns.append(pattern_name)

    return patterns

def detect_sdk_migration(content: str) -> str:
    """Detecta status de migração para SDK"""
    if "ClaudeSDKClient" in content or "claude_code_sdk" in content:
        return "sdk"
    elif "anthropic.Anthropic" in content or "ANTHROPIC_API_KEY" in content:
        return "api"
    return "unknown"

def determine_success(tool_result: dict) -> bool:
    """Determina se a execução foi bem-sucedida"""
    # Verificar indicadores de erro
    if "error" in tool_result or "Error" in str(tool_result):
        return False
    if "traceback" in str(tool_result).lower():
        return False
    if "failed" in str(tool_result).lower():
        return False

    return True

def generate_id() -> str:
    """Gera ID único para entrada"""
    return hashlib.md5(
        f"{datetime.now().isoformat()}{os.getpid()}".encode()
    ).hexdigest()[:12]

def get_session_id() -> str:
    """Obtém ID da sessão atual"""
    session_file = Path("/tmp/claude_session_id")
    if session_file.exists():
        return session_file.read_text().strip()

    session_id = hashlib.md5(
        f"{datetime.now().date()}{os.getpid()}".encode()
    ).hexdigest()[:8]
    session_file.write_text(session_id)
    return session_id

def update_tracking(file: Path, entry: dict):
    """Atualiza arquivo de tracking"""
    history = load_json(file, [])
    history.append(entry)

    # Limitar tamanho do histórico
    max_entries = 10000
    if len(history) > max_entries:
        history = history[-max_entries:]

    save_json(file, history)

def update_patterns(file: Path, patterns: List[dict]):
    """Atualiza arquivo de padrões"""
    existing = load_json(file, [])
    existing.extend(patterns)

    # Agregar padrões similares
    aggregated = {}
    for pattern in existing:
        key = pattern["name"]
        if key not in aggregated:
            aggregated[key] = pattern
            aggregated[key]["occurrences"] = 1
        else:
            aggregated[key]["occurrences"] += 1
            if "count" in pattern:
                aggregated[key]["count"] = aggregated[key].get("count", 0) + pattern["count"]

    save_json(file, list(aggregated.values()))

def save_insights(file: Path, insights: List[dict]):
    """Salva insights gerados"""
    existing = load_json(file, [])
    existing.extend(insights)

    # Manter apenas insights recentes
    cutoff = (datetime.now() - timedelta(days=30)).isoformat()
    recent = [i for i in existing if i.get("timestamp", "") > cutoff]

    save_json(file, recent)

def analyze_complexity_progression(history: List[dict]) -> Optional[dict]:
    """Analisa progressão de complexidade ao longo do tempo"""
    if len(history) < 10:
        return None

    progression = {}
    for entry in history:
        date = entry["timestamp"][:10]  # YYYY-MM-DD
        complexity = entry.get("complexity", "unknown")
        if date not in progression:
            progression[date] = []
        progression[date].append(complexity)

    # Calcular tendência
    complexity_scores = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
    daily_scores = {}
    for date, complexities in progression.items():
        scores = [complexity_scores.get(c, 2) for c in complexities]
        daily_scores[date] = sum(scores) / len(scores) if scores else 2

    return daily_scores

def analyze_frequent_patterns(patterns: List[dict]) -> List[str]:
    """Analisa padrões mais frequentes"""
    pattern_counts = {}
    for pattern in patterns:
        name = pattern["name"]
        pattern_counts[name] = pattern_counts.get(name, 0) + pattern.get("occurrences", 1)

    sorted_patterns = sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True)
    return [name for name, _ in sorted_patterns]

def analyze_migration_status(history: List[dict]) -> dict:
    """Analisa status de migração para SDK"""
    sdk_count = sum(1 for e in history if e.get("sdk_migration") == "sdk")
    api_count = sum(1 for e in history if e.get("sdk_migration") == "api")
    total = sdk_count + api_count

    return {
        "sdk": sdk_count,
        "api": api_count,
        "total": total,
        "percentage": (sdk_count / total * 100) if total > 0 else 0,
    }

def analyze_categories(history: List[dict]) -> List[str]:
    """Analisa categorias exploradas"""
    categories = set()
    for entry in history:
        category = entry.get("category")
        if category and category != "unknown":
            categories.add(category)
    return list(categories)

def load_json(file: Path, default=None):
    """Carrega arquivo JSON com fallback"""
    if file.exists():
        try:
            with open(file, 'r') as f:
                return json.load(f)
        except:
            pass
    return default if default is not None else {}

def save_json(file: Path, data):
    """Salva dados em JSON"""
    file.parent.mkdir(parents=True, exist_ok=True)
    with open(file, 'w') as f:
        json.dump(data, f, indent=2, default=str)

if __name__ == "__main__":
    sys.exit(main())