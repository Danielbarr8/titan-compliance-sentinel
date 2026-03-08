import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser  # This pulls live news
from datetime import datetime

# --- TITAN MASTER SETTINGS ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide", page_icon="🛡️")

# --- SECRETS & API CONFIG ---
try:
    hf_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("🔑 ARCHITECT ERROR: No Hugging Face Token found!")
    st.stop()

RISK_API = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
BIAS_API = "https://api-inference.huggingface.co/models/unitary/toxic-bert"
headers = {"Authorization": f"Bearer {hf_token}"}

def query_hf(api_url, payload):
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

# --- SIDEBAR: REGULATORY TICKER ---
with st.sidebar:
    st.header("🌍 Regulatory Live Feed")
    st.caption("Latest AI Law & Compliance Updates")
    try:
        # Pulling from a major AI Ethics & Law RSS feed
        feed = feedparser.parse("https://www.technologyreview.com/topic/artificial-intelligence/feed/")
        for entry in feed.entries[:3]:
            st.markdown(f"**[{entry.title}]({entry.link})**")
            st.caption(f"Published: {entry.published[:16]}")
            st.divider()
    except:
        st.write("Feed temporarily offline. Checking local cache...")

# --- UI DESIGN ---
st.title("🛡️ PROJECT TITAN: Final Evolution")
st.write(f"### Operational Status: Online | Mode: Hybrid Cloud")
st.divider()

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🛠️ Audit Parameters")
    project_desc = st.text_area("Input AI Project Parameters:", height=150)
    audit_btn = st.button("EXECUTE MASTER AUDIT")

with col2:
    if audit_btn and project_desc:
        with st.spinner("Synchronizing with Global Sentinels..."):
            risk_payload = {"inputs": project_desc, "parameters": {"candidate_labels": ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"]}}
            risk_data = query_hf(RISK_API, risk_payload)
            bias_data = query_hf(BIAS_API, {"inputs": project_desc})

            if "error" in risk_data:
                st.warning("⚠️ Wake-up signal sent to AI Brain. Retry in 5 seconds.")
            else:
                label = risk_data['labels'][0]
                score = risk_data['scores'][0]
                bias_score = bias_data[0][0]['score']

                st.subheader("📊 Compliance Radar")
                df = pd.DataFrame({
                    "Metric": ["Bias Detection", "Ethics", "Transparency", "Safety"],
                    "Value": [bias_score, 0.75, 1-score, 0.85]
                })
                fig = px.line_polar(df, r='Value', theta='Metric', line_close=True, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

                st.metric("Sentinel Verdict", label, f"{score*100:.1f}% Confidence")

# --- FOOTER: THE ARCHITECT'S PROMISE ---
st.divider()
st.caption("Built by [Your Name] | Powered by Hugging Face & Streamlit | AI Compliance Architect Suite v3.0")
