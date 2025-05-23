# ✅ context_indexer.py — Project + Knowledge Context Reader
# ----------------------------------------------------------
# Extracts and chunks context from project artifacts and KB files for prompt generation.

import os
from utils.file_utils import safe_read_file, chunk_text_content
from config.pyenv import get_path

PROJECTS_ROOT = get_path("RAPID_PROJECTS_PATH")
KB_ROOT = get_path("RAPID_KNOWLEDGE_BASE_PATH")
MAX_CHARS = 10000
CHUNK_SIZE = 1000  # ideal characters per chunk

def get_project_context(project_id: str) -> list:
    """
    Extract chunked context from all supported files in a project folder.

    Args:
        project_id (str): e.g., "PRJ-1234_Nostro_Recon_Control"

    Returns:
        List[Tuple[str, str]]: [(chunk_id, chunk_content), ...]
    """
    chunks = []
    folder_path = os.path.join(PROJECTS_ROOT, project_id)

    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"❌ Project folder '{project_id}' not found at {folder_path}")

    for file_name in sorted(os.listdir(folder_path)):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            content = safe_read_file(file_path, max_chars=MAX_CHARS)
            sub_chunks = chunk_text_content(content, chunk_size=CHUNK_SIZE)
            for i, chunk in enumerate(sub_chunks):
                chunks.append((f"{file_name} [Part {i+1}]", chunk.strip()))

    return chunks

def get_kb_context(kb_files=None) -> list:
    """
    Load and chunk important knowledge base files.

    Args:
        kb_files (list or None): Default set if not provided.

    Returns:
        List[Tuple[str, str]]: [(chunk_id, chunk_content), ...]
    """
    default_files = [
        "master_sop.md",
        "controls_glossary.md",
        "risk_frameworks.md",
        "qa_checklist.md"
    ]
    chunks = []

    for fname in kb_files or default_files:
        fpath = os.path.join(KB_ROOT, fname)
        if os.path.exists(fpath):
            content = safe_read_file(fpath, max_chars=MAX_CHARS)
            sub_chunks = chunk_text_content(content, chunk_size=CHUNK_SIZE)
            for i, chunk in enumerate(sub_chunks):
                chunks.append((f"{fname} [KB-{i+1}]", chunk.strip()))

    return chunks

def format_context_blocks(context_list: list) -> str:
    """
    Format chunked context into clean sections for LLM input.

    Args:
        context_list (list): List of (chunk_id, chunk_content) tuples

    Returns:
        str: Markdown-formatted context string
    """
    blocks = []
    for chunk_id, content in context_list:
        block_header = f"\n### {chunk_id}\n" + "-" * 60
        blocks.append(f"{block_header}\n{content}")
    return "\n\n".join(blocks)