import sys
import json

from input import prepare_input, prepare_file
from complexity import calculate_complexity

#print summary of result in human readable format
#wil be improved on to include more details and present user friendly way
def print_summary(result: dict) -> None:
    print("\n--- CodeShield Summary (early draft) ---")
    print(f"Status: {result.get('status')}")
    print(f"Input type: {result.get('inputType')}")
    print(f"Language: {result.get('language')}")
    print(f"Parsed: {result.get('parsed')}")
    print(f"File: {result.get('filepath', 'N/A')}")
    print(f"Raw lines: {result.get('rawLineCount')}")
    print(f"Cleaned lines: {result.get('cleanedLineCount')}")

    complexity = result.get("complexity") or {}
    print("\nComplexity")
    if complexity:
        print(f"  Lines of code (calc): {complexity.get('linesOfCode')}")
        print(f"  Decision points: {complexity.get('decisionPoints')}")
        print(f"  Cyclomatic complexity: {complexity.get('complexityScore')}")
    else:
        print("  (not calculated yet)")

    print("\nSecurity red flags:", "(not implemented yet)" if result.get("redFlags") is None else result.get("redFlags"))
    print("TDI:", "(not implemented yet)" if result.get("tdi") is None else result.get("tdi"))

#snippet input function, still to be improved for complex and edge cases
def run_snippet_demo():
    example_code = """
def greet(name):
    if name:
        return "Hello " + name
    return "Hello"
"""
    prepared = prepare_input(example_code, language="python")
    print("--- File input + complexity (early integration ---")
    print_summary(prepared)
    print("\nRaw output")
    print(json.dumps(prepared, indent=2))

#if error when retrieving file, error status message print 
def run_file_scan(filepath: str):
    prepared = prepare_file(filepath, language="python")
    if prepared.get("status") == "error":
        print("--- Error ---")
        print(json.dumps(prepared, indent=2))
        return

    complexity_result = calculate_complexity(filepath)
    prepared["complexity"] = {
        "decisionPoints": complexity_result.get("decision_points"),
        "complexityScore": complexity_result.get("complexity_score"),
        "linesOfCode": complexity_result.get("lines_of_code")
    }

    print("File input + complexity (early integration): ")
    print_summary(prepared)
    print("\nRaw output")
    print(json.dumps(prepared, indent=2))


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        run_file_scan(sys.argv[1])
    else:
        run_snippet_demo()