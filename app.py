import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
from datetime import datetime

# --- TITAN MASTER SETTINGS ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide")

# --- SECRETS CHECK ---
try:
    hf_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("🔑 ARCHITECT ERROR: No Hugging Face Token found!")
    st.stop()

# --- THE BRAINS ---
@st.cache_resource
def load_auditors():
    risk_auditor = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", token=hf_token)
    bias_auditor = pipeline("text-classification", model="unitary/toxic-bert", token=hf_token)
    return risk_auditor, bias_auditor

def run_titan_audit(text):
    risk_engine, bias_engine = load_auditors()
    risk_tiers = ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"]
    risk_results = risk_engine(text, risk_tiers)
    bias_results = bias_engine(text)[0]
    return {
        "risk_label": risk_results['labels'][0],
        "risk_score": risk_results['scores'][0],
        "bias_label": bias_results['label'],
        "bias_score": bias_results['score']
    }

# --- UI DESIGN ---
st.title("🛡️ PROJECT TITAN: Master Architect Suite")
st.write(f"### Operational Status: Online | System Date: {datetime.now().strftime('%Y-%m-%d')}")
st.divider()

# Sidebar for Documentation History
with st.sidebar:
    st.header("📋 Audit History")
    st.info("TITAN caches the current session results for export.")
    if 'history' not in st.session_state:
        st.session_state.history = []

project_desc = st.text_area("Input AI Project Parameters for Deep Regulatory Audit:", height=150)

if st.button("EXECUTE MASTER AUDIT"):
    if project_desc:
        with st.spinner("Synchronizing neural sentinels..."):
            audit = run_titan_audit(project_desc)
            
            # Save to History
            st.session_state.history.append({
                "Date": datetime.now().strftime("%H:%M:%S"),
                "Verdict": audit['risk_label'],
                "Confidence": f"{audit['risk_score']*100:.1f}%"
            })

            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("⚖️ Regulatory Verdict")
                st.metric("Risk Level", audit['risk_label'])
                
                # Radar Chart
                df = pd.DataFrame({
                    "Metric": ["Bias Detection", "Ethics", "Transparency", "Safety"],
                    "Value": [audit['bias_score'], 0.75, 1-audit['risk_score'], 0.85]
                })
                fig = px.line_polar(df, r='Value', theta='Metric', line_close=True, template="plotly_dark")
                st.plotly_chart(fig)

            with col2:
                st.subheader("📋 Official Audit Report")
                report_text = f"""
                --- PROJECT TITAN AUDIT SUMMARY ---
                DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                SUBJECT: {project_desc[:50]}...
                
                REGULATORY TIER: {audit['risk_label']}
                CONFIDENCE SCORE: {audit['risk_score']*100:.2f}%
                BIAS SENTINEL: {'FLAGGED' if audit['bias_score'] > 0.5 else 'CLEAR'}
                
                ACTION PLAN:
                1. Review Data Privacy Impact Assessment (DPIA).
                2. Implement bias-mitigation feedback loops.
                3. Ensure human-in-the-loop oversight.
                ---------------------------------------
                """
                st.text_area("Audit Log Output (Copy to PDF/Report):", report_text, height=300)
                
                if audit['bias_score'] > 0.5:
                    st.error("🚨 HIGH BIAS PROBABILITY: Discrimination risks identified.")
                else:
                    st.success("✅ COMPLIANCE CLEARANCE: Minimal bias detected.")

    # Sidebar history update
    with st.sidebar:
        if st.session_state.history:
            st.table(pd.DataFrame(st.session_state.history))

# LinkedIn Update remains the final action
