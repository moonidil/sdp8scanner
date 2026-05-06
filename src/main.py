#Developer: Idil Cabdullahi

import sys
import json

from scanner import scan_file, scan_snippet


def print_summary(result: dict) -> None:
    #human-readable view of the scan result for the CLI
    print("\n--- CodeShield Summary ---")
    print(f"Status: {result.get('status')}")
    print(f"Input type: {result.get('inputType', 'N/A')}")
    print(f"Language: {result.get('language', 'N/A')}")
    print(f"Parsed: {result.get('parsed', 'N/A')}")
    print(f"File: {result.get('filepath', 'N/A')}")
    print(f"Raw lines: {result.get('rawLineCount', 'N/A')}")
    print(f"Cleaned lines: {result.get('cleanedLineCount', 'N/A')}")

    #stop here if the scan didn't actually run (bad input, parse fail, etc.)
    if result.get("status") == "error":
        print(f"\nError: {result.get('message', 'Unknown error')}")
        return

    complexity = result.get("complexity") or {}
    print("\nComplexity")
    print(f"Lines of code: {complexity.get('linesOfCode', 'N/A')}")
    print(f"Decision points: {complexity.get('decisionPoints', 'N/A')}")
    print(f"Cyclomatic complexity: {complexity.get('complexityScore', 'N/A')}")

    security = result.get("security") or {}
    print("\nSecurity")
    print(f"Red flags found: {security.get('redFlagCount', 0)}")

    #list each finding on its own line, or a friendly note if there were none
    findings = security.get("findings", [])
    if findings:
        for finding in findings:
            print(
                f"- {finding.get('ruleId')} | line {finding.get('line')} | "
                f"{finding.get('type')} | {finding.get('severity')}"
            )
    else:
        print("- No red flags found.")

    metrics = result.get("metrics") or {}
    print("\nMetrics")
    print(f"Vulnerability density: {metrics.get('vulnerabilityDensity', 'N/A')}")
    print(f"TDI: {metrics.get('tdi', 'N/A')}")

    risk = result.get("risk") or {}
    print("\nRisk")
    print(f"Label: {risk.get('label', 'N/A')}")
    print(f"Alert: {risk.get('alert', 'N/A')}")
    print(f"Recommendation: {risk.get('recommendation', 'N/A')}")


def run_snippet_demo() -> None:
    #hardcoded demo snippet with obvious red flags for quick testing
    example_code = """
import hashlib

def login(username, password):
    saved_password = "admin123"
    query = "SELECT * FROM users WHERE name = " + username
    hashed = hashlib.md5(password.encode()).hexdigest()

    if username and password:
        return query, hashed, saved_password

    return None
"""

    result = scan_snippet(example_code, language="python")

    print("=== Snippet input + full scan ===")
    print_summary(result)

    #raw JSON dump is handy when checking the full structure
    print("\n--- Raw JSON Output ---")
    print(json.dumps(result, indent=2))


def run_file_scan(filepath: str) -> None:
    #real file path coming in from the CLI args
    result = scan_file(filepath, language="python")

    print("=== File input + full scan ===")
    print_summary(result)

    print("\n--- Raw JSON Output ---")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    # Usage:
    #   python3 src/main.py
    #   python3 src/main.py samples/test.py

    #if a path was passed in, scan that file; otherwise fall back to the demo snippet
    if len(sys.argv) >= 2:
        run_file_scan(sys.argv[1])
    else:
        run_snippet_demo()