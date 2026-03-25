from input import prepare_input

example_code = """
def greet(name):
    if name:
        return "Hello " + name
    return "Hello"
"""

result = prepare_input(example_code, language="python")
print(result)
