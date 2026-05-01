# CodeShield: Technical Debt and Security Scanner

CodeShield is a prototype technical debt and security scanner developed for our SDP8 group project
The tool analyses Python source code, calculates complexity metrics, detects security red flags, calculates vulnerability density, produces a Technical Debt Index (TDI) and classifies modules by risk

The current prototype supports  command-line scanning and a Streamlit dashboard demo

## Current Features
- Python file scanning
- Python snippet scanning
- Input validation and preprocessing
- Python syntax parse check
- Cyclomatic complexity integration
- Security red-flag detection
- Vulnerability density calculation
- Technical Debt Index calculation
- Risk classification
- High risk alerting
- CLI summary output
- Raw JSON output
- Streamlit dashboard interface

## Prototype Scope
This is a coursework prototype, not a full commercial static analysis tool

the c urrent assumptions:
- Python only
- Single file or pasted snippet input
- Repository scanning is future work
- Security detection is pattern-based and explainable
- TDI uses the project brief formula
- High risk alert follows the reference threshold of TDI >= 50

## Project Structure
```text
src/
  main.py          CLI runner
  input.py         input handling, preprocessing and parse validation
  complexity.py    cyclomatic complexity calculation
  security.py      security red-flag detection
  metrics.py       vulnerability density, TDI and risk classification
  scanner.py       full scan orchestration
  app.py           Streamlit dashboard

samples/
  test.py              low-risk/basic sample
  high_risk.py         small unsafe sample
  extreme_risk.py      short stress-test sample
  full_demo_risk.py    main high-risk demo sample

notes/
  notes.txt        developer notes and run guide