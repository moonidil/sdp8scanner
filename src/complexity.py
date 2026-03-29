# CodeShield - Cyclomatic Complexity Calculator
# Developer: Abdul Basit Farooq

def calculate_complexity(filepath):
    """Read a Python file and calculate its Cyclomatic Complexity."""
    
    # Decision point keywords to look for
    decision_points = ['if ', 'elif ', 'for ', 'while ', 'except ', ' and ', ' or ']
    
    count = 0
    lines_of_code = 0

    with open(filepath, 'r') as file:
        for line in file:
            stripped = line.strip()
            
            # Skip blank lines and comments
            if stripped == '' or stripped.startswith('#'):
                continue
            
            lines_of_code += 1
            
            # Count decision points
            for dp in decision_points:
                if dp in line:
                    count += 1

    complexity = count + 1  # CC = Decision Points + 1
    
    return {
        'filepath': filepath,
        'decision_points': count,
        'complexity_score': complexity,
        'lines_of_code': lines_of_code
    }


# Run the scanner
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