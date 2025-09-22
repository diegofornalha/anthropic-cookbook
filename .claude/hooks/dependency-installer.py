#!/usr/bin/env python3
"""
Hook inteligente para gerenciamento de dependências do Cookbook
Versão aprimorada com detecção proativa e instalação automática
"""

import json
import sys
import re
import subprocess
from pathlib import Path
from typing import Set, Dict, List, Tuple

def main():
    # Receber dados do hook
    hook_data = json.loads(sys.stdin.read())

    tool_name = hook_data.get("toolName", "")
    tool_input = hook_data.get("toolInput", {})

    # Interceptar imports em notebooks
    if tool_name == "Bash":
        handle_bash_command(tool_input)

    # Interceptar leitura de arquivos
    if tool_name in ["Read", "NotebookEdit"]:
        handle_file_read(tool_input)

    # Permitir execução
    return 0

def handle_bash_command(tool_input: dict):
    """Processa comandos Bash e sugere/instala dependências"""
    command = tool_input.get("command", "")

    # Se está rodando Python ou Jupyter
    if "python" in command or "jupyter" in command or "ipython" in command:
        # Extrair arquivo
        file_match = re.search(r'([^\s]+\.(?:py|ipynb))', command)
        if file_match:
            file_path = Path(file_match.group(1))

            # Análise inteligente de dependências
            required_deps = analyze_dependencies(file_path)
            missing_deps = check_missing_dependencies(required_deps)

            if missing_deps:
                # Sugerir instalação com comando otimizado
                deps_cmd = generate_install_command(missing_deps)
                print(f"🔧 Dependências necessárias detectadas!\n"
                      f"\n⚠️  Faltando: {', '.join(missing_deps)}\n"
                      f"\n📦 Instalar com:\n   {deps_cmd}\n"
                      f"\n💡 Dica: Use --upgrade para versões mais recentes",
                      file=sys.stderr)

                # Verificar se deve auto-instalar
                if should_auto_install():
                    print(f"\n🤖 Auto-instalando dependências...", file=sys.stderr)
                    auto_install_dependencies(missing_deps)

def handle_file_read(tool_input: dict):
    """Analisa arquivos lidos e prepara ambiente"""
    file_path = tool_input.get("file_path", tool_input.get("notebook_path", ""))

    if file_path.endswith((".ipynb", ".py")):
        try:
            # Ler e analisar conteúdo
            content = read_file_content(file_path)
            imports = extract_imports(content)

            # Mapeamento completo de dependências
            dependencies = map_imports_to_packages(imports)

            # Verificar dependências especiais do Cookbook
            cookbook_deps = detect_cookbook_patterns(content, file_path)
            dependencies.update(cookbook_deps)

            if dependencies:
                # Checar quais estão faltando
                missing = check_missing_dependencies(dependencies)

                if missing:
                    # Criar comando de instalação otimizado
                    install_cmd = generate_install_command(missing)

                    print(f"\n📦 Análise de Dependências para {Path(file_path).name}:\n"
                          f"✅ Detectadas: {', '.join(dependencies)}\n"
                          f"⚠️  Faltando: {', '.join(missing) if missing else 'Nenhuma'}\n"
                          f"\n🔧 Comando sugerido:\n   {install_cmd}\n",
                          file=sys.stderr)

                    # Verificar compatibilidade
                    check_version_compatibility(dependencies)

        except Exception as e:
            # Não falhar silenciosamente
            print(f"⚠️  Erro ao analisar dependências: {e}", file=sys.stderr)

def analyze_dependencies(file_path: Path) -> Set[str]:
    """Analisa profundamente dependências de um arquivo"""
    deps = set()

    # Mapeamento por categoria do Cookbook
    cookbook_categories = {
        "skills/retrieval_augmented_generation": [
            "neo4j", "numpy", "pandas", "scikit-learn",
            "sentence-transformers", "faiss-cpu"
        ],
        "skills/classification": [
            "scikit-learn", "numpy", "pandas", "matplotlib"
        ],
        "skills/summarization": [
            "transformers", "torch", "nltk", "rouge-score"
        ],
        "tool_use": [
            "pydantic", "jsonschema", "requests", "aiohttp"
        ],
        "multimodal": [
            "pillow", "matplotlib", "opencv-python", "pdf2image",
            "pytesseract", "pdfplumber"
        ],
        "third_party": [
            "boto3", "google-cloud-storage", "azure-storage-blob",
            "pinecone-client", "weaviate-client", "chromadb"
        ],
        "claude_code_sdk": [
            "claude-code-sdk", "httpx", "pydantic", "rich"
        ]
    }

    # Detectar categoria pelo path
    for category, category_deps in cookbook_categories.items():
        if category in str(file_path):
            deps.update(category_deps)
            break

    return deps

def extract_imports(content: str) -> Set[str]:
    """Extrai todos os imports de um arquivo Python/Notebook"""
    imports = set()

    # Patterns para diferentes tipos de import
    patterns = [
        r'import\s+([\w\.]+)',
        r'from\s+([\w\.]+)\s+import',
        r'%pip\s+install\s+([\w\-\[\]]+)',
        r'!pip\s+install\s+([\w\-\[\]]+)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content, re.MULTILINE)
        for match in matches:
            # Pegar apenas o nome base do módulo
            base_module = match.split('.')[0]
            imports.add(base_module)

    return imports

def map_imports_to_packages(imports: Set[str]) -> Set[str]:
    """Mapeia imports Python para pacotes pip"""
    # Mapeamento completo e atualizado
    import_to_pip = {
        # Claude e AI
        "anthropic": "anthropic",
        "claude_code_sdk": "claude-code-sdk",
        "openai": "openai",

        # Data Science
        "sklearn": "scikit-learn",
        "cv2": "opencv-python",
        "PIL": "pillow",
        "Image": "pillow",
        "bs4": "beautifulsoup4",
        "yaml": "pyyaml",

        # Vector DBs
        "voyageai": "voyageai",
        "pinecone": "pinecone-client",
        "weaviate": "weaviate-client",
        "chromadb": "chromadb",
        "qdrant_client": "qdrant-client",

        # Graph DBs
        "neo4j": "neo4j",
        "py2neo": "py2neo",

        # Cloud
        "boto3": "boto3",
        "google": "google-cloud-storage",
        "azure": "azure-storage-blob",

        # ML/DL
        "torch": "torch",
        "tensorflow": "tensorflow",
        "transformers": "transformers",
        "sentence_transformers": "sentence-transformers",
        "faiss": "faiss-cpu",

        # Web
        "flask": "flask",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "gradio": "gradio",
        "streamlit": "streamlit",

        # Utils
        "dotenv": "python-dotenv",
        "tqdm": "tqdm",
        "rich": "rich",
        "typer": "typer",
        "click": "click",
    }

    packages = set()
    for imp in imports:
        if imp in import_to_pip:
            packages.add(import_to_pip[imp])
        elif not is_stdlib(imp):
            # Se não está no mapeamento e não é stdlib, assume mesmo nome
            packages.add(imp)

    return packages

def is_stdlib(module_name: str) -> bool:
    """Verifica se um módulo é da biblioteca padrão Python"""
    stdlib_modules = {
        'os', 'sys', 'json', 're', 'math', 'random', 'datetime', 'time',
        'pathlib', 'typing', 'collections', 'itertools', 'functools',
        'asyncio', 'threading', 'multiprocessing', 'subprocess', 'shutil',
        'tempfile', 'io', 'pickle', 'csv', 'sqlite3', 'urllib', 'http',
        'socket', 'ssl', 'email', 'html', 'xml', 'base64', 'hashlib',
        'hmac', 'secrets', 'uuid', 'copy', 'warnings', 'traceback',
        'logging', 'unittest', 'doctest', 'pdb', 'profile', 'timeit',
    }
    return module_name in stdlib_modules

def detect_cookbook_patterns(content: str, file_path: str) -> Set[str]:
    """Detecta padrões específicos do Cookbook que requerem dependências"""
    deps = set()

    # Padrões que indicam uso de funcionalidades específicas
    patterns = {
        r"GraphRAG|graph_rag|neo4j": ["neo4j", "py2neo"],
        r"embeddings?|vectoriz|voyage": ["voyageai", "sentence-transformers"],
        r"pdf|PDF|PyPDF": ["pypdf2", "pdfplumber", "pdf2image"],
        r"image|Image|vision|PIL": ["pillow", "opencv-python"],
        r"claude.*sdk|ClaudeSDKClient": ["claude-code-sdk"],
        r"asyncio|async def|await": ["aiohttp", "httpx"],
        r"@app\.|FastAPI|uvicorn": ["fastapi", "uvicorn"],
        r"st\.|streamlit": ["streamlit"],
        r"gr\.|gradio": ["gradio"],
    }

    for pattern, packages in patterns.items():
        if re.search(pattern, content):
            deps.update(packages)

    return deps

def check_missing_dependencies(packages: Set[str]) -> Set[str]:
    """Verifica quais pacotes não estão instalados"""
    missing = set()

    for package in packages:
        try:
            # Tentar importar para verificar se está instalado
            result = subprocess.run(
                [sys.executable, "-c", f"import {package.replace('-', '_')}"],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.returncode != 0:
                missing.add(package)
        except:
            missing.add(package)

    return missing

def generate_install_command(packages: Set[str]) -> str:
    """Gera comando otimizado de instalação"""
    if not packages:
        return ""

    # Agrupar pacotes relacionados
    groups = {
        "ml": ["torch", "tensorflow", "transformers"],
        "data": ["numpy", "pandas", "scikit-learn"],
        "viz": ["matplotlib", "seaborn", "plotly"],
    }

    # Comando base
    base_cmd = "pip install"

    # Adicionar flags úteis
    flags = []
    if any(p in ["torch", "tensorflow"] for p in packages):
        flags.append("--upgrade")

    # Construir comando
    cmd_parts = [base_cmd]
    if flags:
        cmd_parts.extend(flags)
    cmd_parts.extend(sorted(packages))

    return " ".join(cmd_parts)

def check_version_compatibility(packages: Set[str]):
    """Verifica compatibilidade de versões"""
    # Avisos de compatibilidade conhecidos
    compatibility_warnings = {
        ("anthropic", "claude-code-sdk"): (
            "⚠️  Conflito: Use claude-code-sdk ao invés de anthropic"
        ),
        ("tensorflow", "torch"): (
            "🔄 Nota: TensorFlow e PyTorch juntos podem ser pesados"
        ),
    }

    for combo, warning in compatibility_warnings.items():
        if all(p in packages for p in combo):
            print(f"\n{warning}", file=sys.stderr)

def should_auto_install() -> bool:
    """Determina se deve auto-instalar dependências"""
    # Verificar configuração
    config_path = Path("/Users/2a/.claude/anthropic-cookbook/.claude/settings.local.json")
    if config_path.exists():
        try:
            with open(config_path) as f:
                config = json.load(f)
                return config.get("custom_settings", {}).get("auto_install_deps", False)
        except:
            pass
    return False

def auto_install_dependencies(packages: Set[str]):
    """Instala dependências automaticamente"""
    try:
        cmd = [sys.executable, "-m", "pip", "install", "-q"] + list(packages)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print(f"✅ Dependências instaladas com sucesso!", file=sys.stderr)
        else:
            print(f"❌ Erro na instalação: {result.stderr}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Erro ao auto-instalar: {e}", file=sys.stderr)

def read_file_content(file_path: str) -> str:
    """Lê conteúdo de arquivo Python ou Notebook"""
    path = Path(file_path)

    if not path.exists():
        return ""

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Se for notebook, extrair células de código
    if path.suffix == '.ipynb':
        try:
            notebook = json.loads(content)
            code_cells = []
            for cell in notebook.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = cell.get('source', [])
                    if isinstance(source, list):
                        code_cells.append(''.join(source))
                    else:
                        code_cells.append(source)
            content = '\n'.join(code_cells)
        except:
            pass  # Se falhar, usa conteúdo original

    return content

if __name__ == "__main__":
    sys.exit(main())