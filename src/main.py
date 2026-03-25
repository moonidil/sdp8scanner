import sys
from input import prepare_input, prepare_file


def run_snippet_demo():
    example_code = """
def greet(name):
    if name:
        return "Hello " + name
    return "Hello"
"""
#snippet input function, still to be improved
    result = prepare_input(example_code, language="python")
    print("--- Snippet input (early draft) ---")
    print(result)


#if error when retrieving file, error status message print 
def run_file_demo(filepath):
    result = prepare_file(filepath, language="python")
    if result.get("status") == "error":
        print("--- Error ---")
        print(result)
        return

    print("--- File input (early draft) ---")
    print(result)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        run_file_demo(sys.argv[1])
    else:
        run_snippet_demo()
