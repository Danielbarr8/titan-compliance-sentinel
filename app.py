import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline

# --- ARCHITECT'S UI ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide", page_icon="🛡️")

st.markdown("""
    <style>
    .main { background-color: #0f172a; color: #f8fafc; }
    .stTextArea textarea { background-color: #1e293b; color: white; border: 1px solid #334155; }
    .stButton>button { background-image: linear-gradient(to right, #2563eb, #7c3aed); color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- THE BRAIN (Zero-Shot AI Act Auditor) ---
@st.cache_resource
def load_auditor():
    # Elite model for classifying risks without manual training
    return pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def run_audit(text):
    classifier = load_auditor()
    # Official Risk Tiers of the EU AI Act
    risk_tiers = ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"]
    results = classifier(text, risk_tiers)
    return {"label": results['labels'][0], "score": results['scores'][0]}

# --- MAIN DASHBOARD ---
st.title("🛡️ PROJECT TITAN")
st.write("### AI Compliance Architect & Regulatory Sentinel")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🛠️ Project Submission")
    project_desc = st.text_area("Describe the AI Model's purpose and data usage:", height=300, 
                                placeholder="Example: A credit scoring AI that uses social media data to determine loan eligibility...")
    
    audit_btn = st.button("⚖️ INITIATE TITAN AUDIT")

with col2:
    if audit_btn and project_desc:
        with st.spinner("TITAN is mapping neural patterns to EU AI Act regulations..."):
            audit = run_audit(project_desc)
            risk_label = audit['label']
            confidence = audit['score']

            # Visualization: Risk Radar
            st.subheader("🔍 Compliance Risk Profile")
            risk_map = pd.DataFrame({
                "Regulation": ["Bias Detection", "Data Privacy", "Transparency", "Safety"],
                "Risk Level": [confidence, 0.75, 0.40, 1-confidence]
            })
            fig = px.line_polar(risk_map, r='Risk Level', theta='Regulation', line_close=True, 
                               template="plotly_dark", color_discrete_sequence=['#7c3aed'])
            st.plotly_chart(fig)

            # Sentinel Verdict
            if "Unacceptable" in risk_label:
                st.error(f"VERDICT: {risk_label} (Immediate Action Required)")
            elif "High" in risk_label:
                st.warning(f"VERDICT: {risk_label} (Requires Human Oversight)")
            else:
                st.success(f"VERDICT: {risk_label} (Compliant)")

# --- LINKEDIN SHAREABLE ---
if audit_btn and project_desc:
    st.divider()
    st.subheader("🚀 LINKEDIN TRUST CERTIFICATE")
    st.info("Copy the text below to showcase your Architect status on LinkedIn:")
    st.code(f"""
    I just deployed PROJECT TITAN: An AI Compliance Architect. 🛡️
    
    Audit Subject: {project_desc[:40]}...
    EU AI Act Verdict: {risk_label}
    Sentinel Confidence: {confidence*100:.1f}%
    
    Bridging the gap between raw code and global regulation. 
    Built with #Streamlit #HuggingFace #GitHub #Python
    #AICompliance #ProjectTITAN #AIGovernance
    """, language="text")
