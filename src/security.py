#Developer: Idil Cabdullahi

import re
from typing import List, Dict


SECURITY_RULES = [
    {
        #classic hardcoded secret pattern — variable name + string literal
        "ruleId": "SEC001",
        "name": "Hardcoded credential",
        "severity": "High",
        "pattern": re.compile(
            r"""(?i)\b(password|passwd|pwd|secret|api_key|apikey|token)\b\s*=\s*["'][^"']+["']"""
        ),
        "recommendation": "Move secrets into environment variables or a secure secrets manager."
    },
    {
        #flags md5/sha1 whether or not hashlib is prefixed
        "ruleId": "SEC002",
        "name": "Weak hash function",
        "severity": "Medium",
        "pattern": re.compile(r"\b(hashlib\.)?(md5|sha1)\s*\("),
        "recommendation": "Use a stronger hashing approach such as SHA-256, bcrypt, or Argon2 where appropriate."
    },
    {
        #SQL keyword followed by concat / format / f-string is a strong injection smell
        "ruleId": "SEC003",
        "name": "Possible SQL injection pattern",
        "severity": "High",
        "pattern": re.compile(
            r"""(?i)(select|insert|update|delete).*(\+|%|\.format\(|f["'])"""
        ),
        "recommendation": "Use parameterised queries instead of string concatenation or interpolation."
    },
    {
        #eval / exec are almost never what you want in production code
        "ruleId": "SEC004",
        "name": "Unsafe dynamic execution",
        "severity": "High",
        "pattern": re.compile(r"\b(eval|exec)\s*\("),
        "recommendation": "Avoid eval/exec with user-controlled input."
    },
    {
        #debug=True left on in prod leaks internals (Flask/Django etc.)
        "ruleId": "SEC005",
        "name": "Debug mode enabled",
        "severity": "Medium",
        "pattern": re.compile(r"(?i)\bdebug\s*=\s*True\b"),
        "recommendation": "Disable debug mode in production environments."
    },
]


def _clean_evidence(line: str) -> str:
    #keeps screenshots readable without dumping long or sensitive lines
    evidence = line.strip()
    #cap long lines so the report doesn't get a wall of text
    if len(evidence) > 120:
        evidence = evidence[:117] + "..."
    return evidence


def detect_red_flags(code_text: str) -> List[Dict]:
    """
    Runs simple pattern-based security checks over Python source code.

    This is intentionally lightweight for the prototype. It does not claim to be a full
    static analysis engine, but it gives explainable security red flags that can feed
    vulnerability density and TDI.
    """
    findings = []

    #walk line by line so we can record the line number on each finding
    for line_number, line in enumerate(code_text.splitlines(), start=1):
        stripped = line.strip()

        #skip blanks and comments — no point scanning those
        if not stripped or stripped.startswith("#"):
            continue

        #every rule gets a chance to match the same line (one line can trip multiple rules)
        for rule in SECURITY_RULES:
            if rule["pattern"].search(stripped):
                findings.append({
                    "ruleId": rule["ruleId"],
                    "type": rule["name"],
                    "severity": rule["severity"],
                    "line": line_number,
                    "evidence": _clean_evidence(stripped),
                    "recommendation": rule["recommendation"]
                })

    return findings