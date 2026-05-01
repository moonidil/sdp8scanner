import os
import tempfile
from typing import Dict

from input import prepare_input, prepare_file
from complexity import calculate_complexity
from security import detect_red_flags
from metrics import calculate_vulnerability_density, calculate_tdi, classify_risk


def _read_file_text(filepath: str) -> str:
    #small helper so we don't repeat the open/read boilerplate
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read()


def _build_final_result(prepared: Dict, complexity_result: Dict, code_text: str) -> Dict:
    #stitches together the three analysis stages into one result dict
    findings = detect_red_flags(code_text)

    complexity_score = complexity_result.get("complexity_score", 0)
    lines_of_code = complexity_result.get("lines_of_code", 0)
    red_flag_count = len(findings)

    #density first, then TDI uses it — order matters here
    vulnerability_density = calculate_vulnerability_density(red_flag_count, lines_of_code)
    tdi = calculate_tdi(complexity_score, vulnerability_density)
    risk = classify_risk(tdi)

    #remap Abdul's snake_case keys to the camelCase the frontend/JSON output expects
    prepared["complexity"] = {
        "decisionPoints": complexity_result.get("decision_points", 0),
        "complexityScore": complexity_score,
        "linesOfCode": lines_of_code,
    }

    prepared["security"] = {
        "redFlagCount": red_flag_count,
        "findings": findings,
    }

    prepared["metrics"] = {
        "vulnerabilityDensity": vulnerability_density,
        "tdi": tdi,
    }

    prepared["risk"] = risk

    #keeping these top-level too for backwards compatibility with the early prototype
    prepared["redFlags"] = findings
    prepared["tdi"] = tdi

    return prepared


def scan_file(filepath: str, language: str = "python") -> Dict:
    #full pipeline for the file input path
    prepared = prepare_file(filepath, language=language)

    #bail early if input prep already flagged something (missing file, wrong type, etc.)
    if prepared.get("status") == "error":
        return prepared

    #no point analysing code that won't even parse
    if not prepared.get("parsed"):
        prepared["status"] = "error"
        prepared["message"] = "Python syntax could not be parsed. Fix syntax errors before scanning."
        return prepared

    code_text = _read_file_text(filepath)
    complexity_result = calculate_complexity(filepath)

    return _build_final_result(prepared, complexity_result, code_text)


def scan_snippet(code_text: str, language: str = "python") -> Dict:
    #full pipeline for the snippet input path
    prepared = prepare_input(code_text, language=language)

    if prepared.get("status") == "error":
        return prepared

    if not prepared.get("parsed"):
        prepared["status"] = "error"
        prepared["message"] = "Python syntax could not be parsed. Fix syntax errors before scanning."
        return prepared

    #calculate_complexity expects a path on disk, so we drop the snippet into a temp file
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as temp_file:
            temp_file.write(code_text)
            temp_path = temp_file.name

        complexity_result = calculate_complexity(temp_path)
        result = _build_final_result(prepared, complexity_result, code_text)
        #snippet didn't come from a real path, so make that obvious in the output
        result["filepath"] = "N/A - snippet input"

        return result

    finally:
        #always clean up the temp fileneven if something blew up above
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)