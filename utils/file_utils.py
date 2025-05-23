# ✅ file_utils.py — Safe File Reader for RAPID Context Ingestion
# ---------------------------------------------------------------
# Supports selective reading of allowed text-based file types.
# Skips or flags unsupported or problematic files gracefully.

import os

# ✅ Allowed file types for ingestion (for context building)
SUPPORTED_EXTENSIONS = [".txt", ".csv", ".py", ".log", ".md", ".json"]

def safe_read_file(file_path, max_chars=10000):
    """
    Read the content of a supported file type safely (up to max_chars).
    Unsupported types return a placeholder notice.

    Args:
        file_path (str): Full path to the file to read
        max_chars (int): Maximum characters to read

    Returns:
        str: File content (or error message)
    """
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        return f"[Unsupported file type: {ext} — Skipped]"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(max_chars)
            return content.strip()
    except Exception as e:
        return f"[Error reading {file_path}: {str(e)}]"


def chunk_text_content(text, chunk_size=1000):
    """
    Split long text into smaller semantic chunks for LLM context.
    Attempts to split on paragraph boundaries (\n\n).

    Args:
        text (str): The full input text
        chunk_size (int): Max characters per chunk

    Returns:
        List[str]: List of chunked strings
    """
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < chunk_size:
            current_chunk += para + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks