# CodeShield: Technical Debt and Security Scanner

CodeShield is a prototype technical debt and security scanner developed for our SDP8 group project
The tool analyses Python source code, calculates complexity metrics, detects security red flags, calculates vulnerability density, produces a technical debt index (TDI) and classifies the modules by risk.
The current prototype supports command-line scanning, pasted snippet scanning, file upload scanning and a Streamlit dashboard demo, and the prototyp is open to future work by being organised and scalable.

## Current Features

- Python file scanning
- Python snippet scanning
- Dashboard file upload scanning
- Input validation and preprocessing
- Python syntax parse checking
- Cyclomatic complexity integration
- Security red-flag detection
- Vulnerability density calculation
- Technical Debt Index calculation
- Risk classification
- High-risk alerting
- CLI summary output
- Raw JSON output
- Streamlit dashboard interface
- Dashboard visualisations
- Export support
- Refactoring Impact Simulator
- Regression checklist and refactoring evidence notes
- Basic pytest coverage for metric calculations

## Prototype Scope

This is a coursework prototype and is not a full commercial static analysis tool.

The current assumptions:

- Python only
- Single file or pasted snippet input
- Repository-level scanning is future work
- Security detection is pattern-based and explainable
- Pattern-based rules may produce false positives or miss issues requiring deeper program analysis
- TDI uses the project brief formula
- High-risk alert follows the reference threshold of TDI > and = 50
- The Refactoring Impact Simulator provides projected impact only and does not automatically rewrite or rescan code

## Project Structure

```text
src/
  main.py              CLI runner
  input.py             input handling, preprocessing and parse validation
  complexity.py        cyclomatic complexity calculation
  security.py          security red-flag detection
  metrics.py           vulnerability density, TDI, risk classification and simulator projection helper
  scanner.py           full scan orchestration
  app.py               Streamlit dashboard

samples/
  test.py              low-risk/basic sample
  high_risk.py         small unsafe sample
  extreme_risk.py      short stress-test sample
  full_demo_risk.py    main high-risk demo sample

tests/
  test_metrics.py      pytest tests for metrics and simulator projection helper

notes/
  notes.txt                    developer notes and run guide
  week6_dev_notes.txt          development notes
  regression_checklist.txt     final dashboard and scanner regression checklist
  refactoring_idil.txt         refactoring support evidence note

requirements.txt       Python dependencies
README.md              project overview and usage notes
.gitignore             ignored files and folders


- written by Developer: idil cabdullahi