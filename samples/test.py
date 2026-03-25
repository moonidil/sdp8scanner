#sample snippet to mke sure its working. to be improved later for more complex code and edge cases
def classify_score(score):
    if score > 80:
        return "A"
    elif score > 60:
        return "B"
    else:
        return "C"


def total(values):
    s = 0
    for v in values:
        if v % 2 == 0:
            s += v
    return s


def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
