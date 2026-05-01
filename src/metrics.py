from typing import Dict


def calculate_vulnerability_density(red_flag_count: int, lines_of_code: int) -> float:
    """
    Vulnerability Density = red flags per 1,000 lines of code.
    """
    #guard against empty/unreadable files so we don't divide by zero
    if lines_of_code <= 0:
        return 0.0

    #per 1k LOC keeps the number readable for small files
    return round((red_flag_count / lines_of_code) * 1000, 2)


def calculate_tdi(complexity_score: float, vulnerability_density: float) -> float:
    """
    Technical Debt Index from the brief:
    TDI = (Complexity Score * 0.5) + (Vulnerability Density * 0.5)
    """
    #50/50 split between complexity and security densit
    return round((complexity_score * 0.5) + (vulnerability_density * 0.5), 2)


def classify_risk(tdi: float) -> Dict:
    """
    Prototype risk thresholds.

    The brief gives 50 as a useful high-risk reference baseline, so this implementation
    alerts at TDI >= 50.
    """
    #thresholds are prototype-level, can be tuned once we have more sample data
    if tdi >= 50:
        return {
            "label": "High Risk",
            "alert": True,
            "recommendation": "Immediate refactoring recommended."
        }

    #medium band catches code that's worth a look but not on fire
    if tdi >= 20:
        return {
            "label": "Medium Risk",
            "alert": False,
            "recommendation": "Review and refactor if this module is business-critical."
        }

    #default fallthrough — looks fine for now
    return {
        "label": "Low Risk",
        "alert": False,
        "recommendation": "No immediate refactoring required."
    }