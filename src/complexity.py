# CodeShield - Cyclomatic Complexity Calculator
# Developer: Abdul Basit Farooq (Enhanced Version)

import ast

def calculate_complexity(filepath):
    """
    Calculate Cyclomatic Complexity using AST parsing for accuracy.
    More robust than simple string matching.
    """
    with open(filepath, 'r') as file:
        code = file.read()
    
    # Parse the code into AST
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return {
            'filepath': filepath,
            'decision_points': 0,
            'complexity_score': 0,
            'lines_of_code': 0,
            'error': 'Invalid Python syntax'
        }
    
    decision_points = 0
    
    # Walk through AST nodes and count decision points
    for node in ast.walk(tree):
        # if, elif
        if isinstance(node, ast.If):
            decision_points += 1
        # for loops
        elif isinstance(node, ast.For):
            decision_points += 1
        # while loops
        elif isinstance(node, ast.While):
            decision_points += 1
        # except handlers
        elif isinstance(node, ast.ExceptHandler):
            decision_points += 1
        # and, or (boolean operators)
        elif isinstance(node, ast.BoolOp):
            decision_points += len(node.values) - 1
        # match/case (Python 3.10+)
        elif isinstance(node, ast.Match):
            decision_points += len(node.cases)
    
    # Count actual lines of code (non-blank, non-comment)
    lines_of_code = len([
        line for line in code.split('\n') 
        if line.strip() and not line.strip().startswith('#')
    ])
    
    complexity = decision_points + 1
    
    return {
        'filepath': filepath,
        'decision_points': decision_points,
        'complexity_score': complexity,
        'lines_of_code': lines_of_code
    }

# Keep the same main section...
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python complexity.py <filepath>")
    else:
        result = calculate_complexity(sys.argv[1])
        print(f"\n--- CodeShield Analysis ---")
        print(f"File: {result['filepath']}")
        print(f"Lines of Code: {result['lines_of_code']}")
        print(f"Decision Points: {result['decision_points']}")
        print(f"Cyclomatic Complexity: {result['complexity_score']}")