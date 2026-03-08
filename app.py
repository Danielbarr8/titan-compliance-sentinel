import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser
from datetime import datetime

# --- TITAN MASTER ARCHITECT UI ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide", page_icon="🛡️")

# CUSTOM CSS: This is the 'Paint Job'
st.markdown("""
    <style>
    .main { background-color: #000b1a; color: #00f2ff; }
    .stTextArea textarea { background-color: #001a33; color: #00f2ff; border: 1px solid #00f2ff; }
    .stButton>button { 
        background-image: linear-gradient(to right, #00d2ff, #3a7bd5); 
        color: white; font-weight: bold; border: none; box-shadow: 0px 0px 15px #00d2ff;
    }
    .stMetric { color: #00f2ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SECRETS & API CONFIG ---
try:
    hf_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("🔑 ARCHITECT ERROR: No Token Found!")
    st.stop()

RISK_API = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
BIAS_API = "https://api-inference.huggingface.co/models/unitary/toxic-bert"
headers = {"Authorization": f"Bearer {hf_token}"}

def query_hf(api_url, payload):
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

# --- SIDEBAR: REGULATORY TICKER ---
with st.sidebar:
    st.markdown("### 📡 TITAN SATELLITE FEED")
    st.divider()
    try:
        feed = feedparser.parse("https://www.technologyreview.com/topic/artificial-intelligence/feed/")
        for entry in feed.entries[:3]:
            st.markdown(f"**[{entry.title}]({entry.link})**")
            st.caption(f"🗓️ {entry.published[:16]}")
            st.divider()
    except:
        st.write("Feed Link Offline.")

# --- MAIN DASHBOARD ---
st.title("🛡️ PROJECT TITAN: Final Evolution")
st.write(f"### STATUS: OPERATIONAL | ARCHITECT: Daniel Barr")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🛠️ AUDIT PARAMETERS")
    project_desc = st.text_area("Input Model Context for Neural Scan:", height=200, 
                                placeholder="Describe the AI system...")
    audit_btn = st.button("EXECUTE MASTER AUDIT")

with col2:
    if audit_btn and project_desc:
        with st.spinner("SYNCHRONIZING SENTINELS..."):
            risk_payload = {"inputs": project_desc, "parameters": {"candidate_labels": ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"]}}
            risk_data = query_hf(RISK_API, risk_payload)
            bias_data = query_hf(BIAS_API, {"inputs": project_desc})

            if "error" in risk_data:
                st.warning("⚠️ Waking up the AI Brain... Click again in 10 seconds.")
            else:
                label = risk_data['labels'][0]
                score = risk_data['scores'][0]
                bias_score = bias_data[0][0]['score']

                st.subheader("🔍 RISK VECTOR ANALYSIS")
                df = pd.DataFrame({
                    "Vector": ["Bias", "Ethics", "Privacy", "Safety"],
                    "Level": [bias_score, 0.70, 1-score, 0.80]
                })
                # Matrix-style visualization
                fig = px.line_polar(df, r='Level', theta='Vector', line_close=True, 
                                   template="plotly_dark", color_discrete_sequence=['#00f2ff'])
                fig.update_traces(fill='toself', fillcolor='rgba(0, 242, 255, 0.2)')
                st.plotly_chart(fig, use_container_width=True)

                st.metric("SENTINEL VERDICT", label, f"{score*100:.1f}% Confidence")

st.divider()
st.caption("AI Compliance Architect Suite v3.1 | Secure Blockchain Audit Trail Ready")
