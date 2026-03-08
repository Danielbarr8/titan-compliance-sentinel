import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline

# --- TITAN SETTINGS ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide")

# --- SECRETS CHECK ---
try:
    hf_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("🔑 ARCHITECT ERROR: No Hugging Face Token found!")
    st.stop()

# --- THE BRAIN (Risk & Bias Engines) ---
@st.cache_resource
def load_auditors():
    # Auditor 1: Regulatory Risk
    risk_auditor = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", token=hf_token)
    # Auditor 2: Bias & Toxicity Sentinel
    bias_auditor = pipeline("text-classification", model="unitary/toxic-bert", token=hf_token)
    return risk_auditor, bias_auditor

def run_titan_audit(text):
    risk_engine, bias_engine = load_auditors()
    
    # Run Risk Scan
    risk_tiers = ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"]
    risk_results = risk_engine(text, risk_tiers)
    
    # Run Bias Scan
    bias_results = bias_engine(text)[0]
    
    return {
        "risk_label": risk_results['labels'][0],
        "risk_score": risk_results['scores'][0],
        "bias_label": bias_results['label'],
        "bias_score": bias_results['score']
    }

# --- UI DESIGN ---
st.title("🛡️ PROJECT TITAN: Sentinel Upgrade")
st.write("### AI Compliance Architect | Bias & Regulatory Pipeline")
st.divider()

project_desc = st.text_area("Enter AI Project Description for Deep Audit:", height=200)

if st.button("RUN DEEP SENTINEL AUDIT"):
    if project_desc:
        with st.spinner("Executing neural bias check..."):
            audit = run_titan_audit(project_desc)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("⚖️ Regulatory Verdict")
                st.info(f"VERDICT: {audit['risk_label']}")
                st.metric("Risk Confidence", f"{audit['risk_score']*100:.1f}%")
                
                # Radar Chart for Portfolio Visual
                df = pd.DataFrame({
                    "Category": ["Bias", "Ethics", "Safety", "Transparency"],
                    "Value": [audit['bias_score'], 0.70, 0.85, 1-audit['risk_score']]
                })
                fig = px.line_polar(df, r='Value', theta='Category', line_close=True, template="plotly_dark")
                st.plotly_chart(fig)

            with col2:
                st.subheader("🧬 Bias Sentinel Results")
                if audit['bias_label'] == "toxic" or audit['bias_score'] > 0.5:
                    st.error("🚨 BIAS DETECTED: Potential discriminatory patterns found.")
                else:
                    st.success("✅ BIAS CLEAR: No immediate harmful patterns detected.")
                
                st.progress(audit['bias_score'])
                st.caption(f"Sentiment/Bias Intensity: {audit['bias_score']*100:.1f}%")

# --- AUTO-LINKEDIN UPDATE ---
            st.divider()
            st.subheader("🚀 UPDATED LINKEDIN SHOWCASE")
            st.code(f"""
            UPDATE: My AI Compliance Architect, PROJECT TITAN, now features an Integrated Bias Sentinel. 🛡️
            
            Audit: {project_desc[:30]}...
            Risk Tier: {audit['risk_label']}
            Bias Scan: {'ALARM' if audit['bias_score'] > 0.5 else 'CLEAR'}
            
            Building trust through transparency. Check out the live Sentinel: 
            [YOUR APP URL]
            """, language="text")
