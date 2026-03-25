import ast


def prepare_input(code_text, language="python"):
    # early draft: snippet handling + basic parse check
    if not code_text or not code_text.strip():
        return {"status": "error", "message": "No code provided."}

    cleaned = code_text.replace("\r\n", "\n").replace("\r", "\n").strip()

    parsed = False
    if language == "python":
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
