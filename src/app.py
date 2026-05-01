import json
import os
import tempfile

import streamlit as st

from scanner import scan_file, scan_snippet


st.set_page_config(
    page_title="CodeShield Scanner",
    page_icon="🛡️",
    layout="wide"
)

st.title("CodeShield: Technical Debt and Security Scanner")
st.write(
    "Upload a Python file or paste a code snippet to calculate complexity, "
    "security red flags, vulnerability density, TDI and risk classification."
)

input_mode = st.radio(
    "Choose input type",
    ["Upload Python file", "Paste code snippet"],
    horizontal=True
)

result = None

if input_mode == "Upload Python file":
    uploaded_file = st.file_uploader("Upload a .py or .txt file", type=["py", "txt"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".py",
            delete=False
        ) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        try:
            if st.button("Run scan"):
                result = scan_file(temp_path)
                result["displayFilename"] = uploaded_file.name
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

else:
    code_text = st.text_area(
        "Paste Python code",
        height=420,
        placeholder="def example():\n    return True"
    )

    if st.button("Run scan"):
        result = scan_snippet(code_text)


if result:
    if result.get("status") == "error":
        st.error(result.get("message", "Unknown error"))
        st.stop()

    st.subheader("Scan Summary")

    complexity = result.get("complexity", {})
    security = result.get("security", {})
    metrics = result.get("metrics", {})
    risk = result.get("risk", {})

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Complexity", complexity.get("complexityScore", "N/A"))
    col2.metric("Lines of Code", complexity.get("linesOfCode", "N/A"))
    col3.metric("Red Flags", security.get("redFlagCount", 0))
    col4.metric("Vulnerability Density", metrics.get("vulnerabilityDensity", "N/A"))
    col5.metric("TDI", metrics.get("tdi", "N/A"))

    st.subheader("Risk Classification")

    if risk.get("alert"):
        st.error(f"{risk.get('label')} - {risk.get('recommendation')}")
    elif risk.get("label") == "Medium Risk":
        st.warning(f"{risk.get('label')} - {risk.get('recommendation')}")
    else:
        st.success(f"{risk.get('label')} - {risk.get('recommendation')}")

    st.subheader("Security Findings")

    findings = security.get("findings", [])

    if findings:
        st.dataframe(findings, use_container_width=True)
    else:
        st.info("No security red flags were found.")

    with st.expander("Raw JSON output"):
        st.json(result)

    with st.expander("Prototype assumptions and limitations"):
        st.write(
            """
            - This prototype currently supports Python only.
            - Security detection is pattern-based and explainable, not a full static analysis engine.
            - Repository-link scanning is treated as future work.
            - Vulnerability density is calculated per 1,000 LOC, so very small sample files may produce high values.
            - The high-risk alert follows the brief's reference threshold of TDI >= 50.
            """
        )

