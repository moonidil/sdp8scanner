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
 
# ============================================
# PROFESSIONAL HEADER - Enhanced by Abdul Basit Farooq
# ============================================
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); border-radius: 10px; margin-bottom: 30px;'>
        <h1 style='color: white; margin: 0;'>🛡️ CodeShield</h1>
        <p style='color: #e3f2fd; margin: 5px 0 0 0;'>Technical Debt & Security Scanner</p>
    </div>
""", unsafe_allow_html=True)
 
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
    
    # Get findings early so we can use them in visualizations
    findings = security.get("findings", [])
 
    # ============================================
    # COLOR-CODED METRICS - Enhanced by Abdul Basit Farooq
    # ============================================
    col1, col2, col3, col4, col5 = st.columns(5)
 
    # Color-coded Complexity
    complexity_score = complexity.get("complexityScore", 0)
    if complexity_score > 15:
        col1.markdown(f"""<div style='padding:10px; background-color:#ffcccc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>Complexity</p>
            <h1 style='color:#d32f2f; margin:5px 0;'>{complexity_score}</h1>
            <small style='color:#d32f2f;'>⚠️ High</small></div>""", unsafe_allow_html=True)
    elif complexity_score > 10:
        col1.markdown(f"""<div style='padding:10px; background-color:#fff4cc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>Complexity</p>
            <h1 style='color:#f57f17; margin:5px 0;'>{complexity_score}</h1>
            <small style='color:#f57f17;'>⚡ Moderate</small></div>""", unsafe_allow_html=True)
    else:
        col1.markdown(f"""<div style='padding:10px; background-color:#ccf5cc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>Complexity</p>
            <h1 style='color:#388e3c; margin:5px 0;'>{complexity_score}</h1>
            <small style='color:#388e3c;'>✅ Good</small></div>""", unsafe_allow_html=True)
 
    # Regular metric for Lines of Code
    col2.metric("Lines of Code", complexity.get("linesOfCode", "N/A"))
 
    # Color-coded Red Flags
    red_flags = security.get("redFlagCount", 0)
    if red_flags > 5:
        col3.markdown(f"""<div style='padding:10px; background-color:#ffcccc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>Red Flags</p>
            <h1 style='color:#d32f2f; margin:5px 0;'>{red_flags}</h1>
            <small style='color:#d32f2f;'>🚨 Critical</small></div>""", unsafe_allow_html=True)
    elif red_flags > 0:
        col3.markdown(f"""<div style='padding:10px; background-color:#fff4cc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>Red Flags</p>
            <h1 style='color:#f57f17; margin:5px 0;'>{red_flags}</h1>
            <small style='color:#f57f17;'>⚠️ Issues Found</small></div>""", unsafe_allow_html=True)
    else:
        col3.markdown(f"""<div style='padding:10px; background-color:#ccf5cc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>Red Flags</p>
            <h1 style='color:#388e3c; margin:5px 0;'>{red_flags}</h1>
            <small style='color:#388e3c;'>✅ Clean</small></div>""", unsafe_allow_html=True)
 
    # Regular metric for Vulnerability Density
    col4.metric("Vulnerability Density", metrics.get("vulnerabilityDensity", "N/A"))
 
    # Color-coded TDI
    tdi_score = metrics.get("tdi", 0)
    if tdi_score >= 100:
        col5.markdown(f"""<div style='padding:10px; background-color:#ffcccc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>TDI</p>
            <h1 style='color:#d32f2f; margin:5px 0;'>{tdi_score}</h1>
            <small style='color:#d32f2f;'>🔴 Critical</small></div>""", unsafe_allow_html=True)
    elif tdi_score >= 50:
        col5.markdown(f"""<div style='padding:10px; background-color:#fff4cc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>TDI</p>
            <h1 style='color:#f57f17; margin:5px 0;'>{tdi_score}</h1>
            <small style='color:#f57f17;'>🟡 High</small></div>""", unsafe_allow_html=True)
    else:
        col5.markdown(f"""<div style='padding:10px; background-color:#ccf5cc; border-radius:5px; text-align:center;'>
            <p style='margin:0; color:#666; font-size:14px;'>TDI</p>
            <h1 style='color:#388e3c; margin:5px 0;'>{tdi_score}</h1>
            <small style='color:#388e3c;'>🟢 Low</small></div>""", unsafe_allow_html=True)
    
    # ============================================
    # VISUALIZATIONS - Added by Abdul Basit Farooq
    # ============================================
    
    st.markdown("---")
    st.subheader("📊 Risk Visualizations")
    
    # Create two columns for charts
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        # TDI Gauge Meter
        import plotly.graph_objects as go
        
        tdi_value = metrics.get("tdi", 0)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=tdi_value,
            delta={'reference': 50, 'increasing': {'color': "red"}},
            title={'text': "Technical Debt Index (TDI)", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [None, 300], 'tickwidth': 1},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgreen"},
                    {'range': [50, 100], 'color': "yellow"},
                    {'range': [100, 300], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            }
        ))
        
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        st.caption("🟢 Low Risk: 0-50 | 🟡 Medium Risk: 50-100 | 🔴 High Risk: 100+")
    
    with viz_col2:
        # Complexity Bar Chart
        import plotly.express as px
        
        complexity_score = complexity.get("complexityScore", 0)
        
        fig_complexity = px.bar(
            x=["Cyclomatic Complexity"],
            y=[complexity_score],
            title="Complexity Score",
            labels={'x': '', 'y': 'Score'},
            color_discrete_sequence=['#1f77b4']
        )
        
        fig_complexity.update_layout(
            showlegend=False,
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            yaxis_title="Complexity Score"
        )
        
        fig_complexity.add_hline(
            y=10, 
            line_dash="dash", 
            line_color="orange",
            annotation_text="Recommended Max: 10"
        )
        
        st.plotly_chart(fig_complexity, use_container_width=True)
        
        st.caption(f"📊 Decision Points: {complexity.get('decisionPoints', 0)}")
    
    # Security Findings Visualization (if there are findings)
    if findings:
        st.markdown("---")
        viz_col3, viz_col4 = st.columns(2)
        
        with viz_col3:
            # Pie chart of severity distribution
            severity_counts = {}
            for finding in findings:
                severity = finding.get('severity', 'Unknown')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            fig_pie = px.pie(
                values=list(severity_counts.values()),
                names=list(severity_counts.keys()),
                title="Security Findings by Severity",
                color_discrete_map={
                    'High': '#ff6b6b',
                    'Medium': '#ffa500',
                    'Low': '#ffeb3b'
                }
            )
            
            fig_pie.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with viz_col4:
            # Bar chart of finding types
            type_counts = {}
            for finding in findings:
                finding_type = finding.get('type', 'Unknown')
                type_counts[finding_type] = type_counts.get(finding_type, 0) + 1
            
            fig_types = px.bar(
                x=list(type_counts.keys()),
                y=list(type_counts.values()),
                title="Security Issues by Type",
                labels={'x': 'Issue Type', 'y': 'Count'},
                color_discrete_sequence=['#e74c3c']
            )
            
            fig_types.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=50, b=20),
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig_types, use_container_width=True)
    
    # Risk Level Progress Bar
    st.markdown("---")
    risk_label = risk.get("label", "Unknown")
    
    if "High" in risk_label:
        risk_progress = 1.0
        risk_color = "red"
    elif "Medium" in risk_label:
        risk_progress = 0.6
        risk_color = "orange"
    else:
        risk_progress = 0.2
        risk_color = "green"
    
    st.metric("Overall Risk Level", risk_label)
    st.progress(risk_progress)
    
    # ============================================
    # REFACTORING SIMULATOR - Added by Abdul Basit Farooq
    # ============================================
    st.markdown("---")
    st.subheader("💡 Refactoring Impact Simulator")
    st.caption("See how fixing issues would improve your TDI score")
 
    col_sim1, col_sim2, col_sim3 = st.columns(3)
 
    with col_sim1:
        st.markdown("**📊 Current State**")
        current_tdi = metrics.get("tdi", 0)
        st.metric("TDI Score", f"{current_tdi:.1f}", 
                  delta=f"+{current_tdi-50:.1f} above threshold" if current_tdi >= 50 else f"{50-current_tdi:.1f} below threshold",
                  delta_color="inverse" if current_tdi >= 50 else "normal")
 
    with col_sim2:
        st.markdown("**🔧 Fix High-Risk Issues**")
        high_severity_count = sum(1 for f in findings if f.get('severity') == 'High')
        simulated_tdi_high = max(0, current_tdi - (high_severity_count * 12))
        
        st.metric("Projected TDI", f"{simulated_tdi_high:.1f}", 
                  delta=f"-{current_tdi-simulated_tdi_high:.1f} improvement",
                  delta_color="normal")
        
        if simulated_tdi_high < 50:
            st.success("✅ Moves to LOW RISK!")
        elif simulated_tdi_high < current_tdi:
            st.info("📉 Still needs more work")
 
    with col_sim3:
        st.markdown("**✨ Fix All Issues**")
        all_issues_count = security.get("redFlagCount", 0)
        simulated_tdi_all = max(0, current_tdi - (all_issues_count * 8))
        
        st.metric("Projected TDI", f"{simulated_tdi_all:.1f}",
                  delta=f"-{current_tdi-simulated_tdi_all:.1f} improvement",
                  delta_color="normal")
        
        if simulated_tdi_all < 50:
            st.success("🎯 TARGET ACHIEVED!")
        else:
            st.warning(f"⚠️ Needs {simulated_tdi_all-50:.0f}+ more improvement")
    
    st.markdown("---")
    
    st.subheader("Risk Classification")
 
    if risk.get("alert"):
        st.error(f"{risk.get('label')} - {risk.get('recommendation')}")
    elif risk.get("label") == "Medium Risk":
        st.warning(f"{risk.get('label')} - {risk.get('recommendation')}")
    else:
        st.success(f"{risk.get('label')} - {risk.get('recommendation')}")
 
    st.subheader("Security Findings")
 
    if findings:
        st.dataframe(findings, use_container_width=True)
    else:
        st.info("No security red flags were found.")
 
    # ============================================
    # EXPORT BUTTONS - Added by Abdul Basit Farooq
    # ============================================
    
    st.markdown("---")
    st.subheader("📥 Export Results")
    
    col_export1, col_export2, col_export3 = st.columns(3)
    
    with col_export1:
        # Export as JSON
        json_str = json.dumps(result, indent=2)
        st.download_button(
            label="📄 Download JSON Report",
            data=json_str,
            file_name="codeshield_report.json",
            mime="application/json",
            use_container_width=True,
            key="download_json"
        )
    
    with col_export2:
        # Export as Text Summary
        summary_text = f"""CodeShield Analysis Report
{'='*50}
 
File: {result.get('displayFilename', result.get('filepath', 'N/A'))}
 
METRICS SUMMARY:
{'-'*50}
Cyclomatic Complexity: {complexity.get('complexityScore', 'N/A')}
Decision Points: {complexity.get('decisionPoints', 'N/A')}
Lines of Code: {complexity.get('linesOfCode', 'N/A')}
 
SECURITY:
{'-'*50}
Red Flags Found: {security.get('redFlagCount', 0)}
Vulnerability Density: {metrics.get('vulnerabilityDensity', 'N/A')}
 
TECHNICAL DEBT:
{'-'*50}
TDI Score: {metrics.get('tdi', 'N/A')}
Risk Classification: {risk.get('label', 'N/A')}
Recommendation: {risk.get('recommendation', 'N/A')}
 
SECURITY FINDINGS:
{'-'*50}
"""
        
        # Add each finding
        if findings:
            for i, finding in enumerate(findings, 1):
                summary_text += f"\n{i}. [{finding.get('severity', 'Unknown')}] {finding.get('type', 'Unknown')}"
                summary_text += f"\n   Line {finding.get('line', 'N/A')}: {finding.get('evidence', 'N/A')}"
                summary_text += f"\n   Recommendation: {finding.get('recommendation', 'N/A')}\n"
        else:
            summary_text += "\nNo security red flags found.\n"
        
        summary_text += f"\n{'='*50}\nGenerated by CodeShield Scanner\n"
        
        st.download_button(
            label="📋 Download Text Summary",
            data=summary_text,
            file_name="codeshield_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_text"
        )
    
    with col_export3:
        # Export findings as CSV
        if findings:
            import io
            csv_buffer = io.StringIO()
            csv_buffer.write("Rule ID,Type,Severity,Line,Evidence,Recommendation\n")
            for finding in findings:
                csv_buffer.write(f'"{finding.get("ruleId", "")}",')
                csv_buffer.write(f'"{finding.get("type", "")}",')
                csv_buffer.write(f'"{finding.get("severity", "")}",')
                csv_buffer.write(f'"{finding.get("line", "")}",')
                csv_buffer.write(f'"{finding.get("evidence", "")}",')
                csv_buffer.write(f'"{finding.get("recommendation", "")}"\n')
            
            st.download_button(
                label="📊 Download Findings CSV",
                data=csv_buffer.getvalue(),
                file_name="codeshield_findings.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_csv"
            )
        else:
            st.info("No findings to export")
    
    st.markdown("---")
 
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

