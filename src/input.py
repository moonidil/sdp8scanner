#Developer: Idil Cabdullahi

import ast
import os

SUPPORTED_LANGUAGES = {"python"}

def _normalise_text(code_text: str) -> str:
    return code_text.replace("\r\n", "\n").replace("\r", "\n").strip()


def prepare_input(code_text, language="python"):
    # snippet/text path
    if not code_text or not code_text.strip():
        return {"status": "error", "message": "No code provided."}

    language = (language or "").lower()
    if language not in SUPPORTED_LANGUAGES:
        return {"status": "error", "message": f"Unsupported language '{language}' (Python only for now)."}

    cleaned = _normalise_text(code_text)

    parsed = False
    try:
        ast.parse(cleaned)
        parsed = True
    except SyntaxError:
        parsed = False

    return {
        "status": "ok",
        "inputType": "snippet",
        "language": language,
        "rawLineCount": len(code_text.splitlines()),
        "cleanedLineCount": len(cleaned.splitlines()) if cleaned else 0,
        "parsed": parsed,
        "complexity": None,
        "redFlags": None,
        "tdi": None
    }


def prepare_file(filepath, language="python"):
    #file path route which i needed for later complexity integration
    if not filepath or not str(filepath).strip():
        return {"status": "error", "message": "No file path provided."}

    language = (language or "").lower()
    if language not in SUPPORTED_LANGUAGES:
        return {"status": "error", "message": f"Unsupported language '{language}' (Python only for now)."}

    if not os.path.exists(filepath):
        return {"status": "error", "message": f"File not found: {filepath}"}

    if not filepath.endswith((".py", ".txt")):
        return {"status": "error", "message": "Unsupported file type. Use .py or .txt."}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    base = prepare_input(content, language=language)
    if base.get("status") == "error":
        return base

    base["inputType"] = "file"
    base["filepath"] = filepath
    return base