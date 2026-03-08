import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline

# --- TITAN SETTINGS ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide")

# --- TOKEN CHECK ---
# This looks for the key in your Streamlit Secrets 'locked box'
try:
    hf_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("🔑 ARCHITECT ERROR: No Hugging Face Token found in Streamlit Secrets!")
    st.stop()

# --- THE BRAIN ---
@st.cache_resource
def load_auditor():
    # We pass the token here to ensure the connection is authorized
    return pipeline("zero-shot-classification", 
                    model="facebook/bart-large-mnli", 
                    token=hf_token)

def run_audit(text):
    try:
        classifier = load_auditor()
        risk_tiers = ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"]
        results = classifier(text, risk_tiers)
        return {"label": results['labels'][0], "score": results['scores'][0]}
    except Exception as e:
        return {"error": str(e)}

# --- UI DESIGN ---
st.title("🛡️ PROJECT TITAN")
st.write("### AI Compliance Architect | Operational")
st.divider()

project_desc = st.text_area("Enter AI Project Description:", height=200)
if st.button("RUN SENTINEL AUDIT"):
    if project_desc:
        with st.spinner("Analyzing neural pathways..."):
            audit = run_audit(project_desc)
            
            if "error" in audit:
                st.error(f"TITAN OFFLINE: {audit['error']}")
            else:
                label = audit['label']
                score = audit['score']
                
                # Visual Risk Radar
                df = pd.DataFrame({
                    "Category": ["Regulatory Bias", "Data Ethics", "Safety", "Transparency"],
                    "Value": [score, 0.70, 0.85, 1-score]
                })
                fig = px.line_polar(df, r='Value', theta='Category', line_close=True)
                st.plotly_chart(fig)
                
                st.success(f"VERDICT: {label} ({score*100:.1f}% Confidence)")
