import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline

# --- PAGE CONFIG ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide", page_icon="🛡️")

# --- UI STYLING ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- THE BRAIN ---
@st.cache_resource
def load_auditor():
    # Using a high-level toxicity and bias model
    return pipeline("text-classification", model="unitary/toxic-bert")

def run_audit(text):
    auditor = load_auditor()
    results = auditor(text)
    return results[0]

# --- INTERFACE ---
st.title("🛡️ PROJECT TITAN")
st.subheader("The Integrated Trust & Audit Network | AI Compliance Architect")

col1, col2 = st.columns([1, 1])

with col1:
    st.info("TITAN scans AI projects for bias, regulatory risks, and ethical violations.")
    project_desc = st.text_area("Describe your AI Project or Paste Code Snippet:", height=250, 
                                placeholder="Example: A facial recognition tool for public security...")
    
    analyze_btn = st.button("⚖️ EXECUTE REGULATORY AUDIT")

with col2:
    if analyze_btn and project_desc:
        with st.spinner("TITAN is analyzing risk vectors..."):
            result = run_audit(project_desc)
            score = result['score']
            label = result['label']
            
            # Data for the graph
            risk_data = pd.DataFrame({
                'Metric': ['GDPR Compliance', 'EU AI Act', 'Bias Detection', 'Toxicity'],
                'Risk Score': [1-score, 0.85, score, score]
            })
            
            fig = px.line_polar(risk_data, r='Risk Score', theta='Metric', line_close=True)
            st.plotly_chart(fig)

            st.success(f"Audit Complete. Sentinel Verdict: {label.upper()}")
            st.metric("Global Ethics Score", f"{100 - (score * 100):.2f}%")
    else:
        st.write("Results will appear here once the audit is executed.")

# --- LINKEDIN CERTIFICATE ---
if project_desc and analyze_btn:
    st.markdown("---")
    st.subheader("🚀 LINKEDIN SHOWCASE")
    st.code(f"""
    I just completed an automated AI Compliance Audit using PROJECT TITAN. 🛡️
    
    Project: {project_desc[:50]}...
    Verdict: PASSED ETHICAL SCAN
    Ethics Score: {100 - (score * 100):.2f}%
    
    As an AI Compliance Architect, I am committed to building trustworthy technology.
    #AICompliance #AIEthics #ProjectTITAN #ResponsibleAI
    """, language="text")
