#Developer: Idil Cabdullahi

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_PATH))


from metrics import (
    calculate_vulnerability_density,
    calculate_tdi,
    classify_risk,
    estimate_refactoring_impact,
)


def test_vulnerability_density_calculation():
    assert calculate_vulnerability_density(9, 46) == 195.65

def test_tdi_calculation():
    assert calculate_tdi(18, 195.65) == 106.83

def test_high_risk_classification():
    result = classify_risk(106.83)

    assert result["label"] == "High Risk"
    assert result["alert"] is True

def test_low_risk_classification():
    result = classify_risk(3.5)

    assert result["label"] == "Low Risk"
    assert result["alert"] is False

def test_refactoring_impact_projection():
    findings = [
        {"severity": "High"},
        {"severity": "High"},
        {"severity": "Medium"},
    ]

    result = estimate_refactoring_impact(100, findings)

    assert result["highSeverityFindings"] == 2
    assert result["totalFindings"] == 3
    assert result["projectedAfterHighRiskFixes"] == 76
    assert result["projectedAfterAllFixes"] == 76
    assert result["highRiskThreshold"] == 50
    assert "Projection only" in result["note"]
