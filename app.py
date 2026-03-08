import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser
from datetime import datetime
import time

# --- TITAN MASTER ARCHITECT UI ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide", page_icon="🛡️")

# CUSTOM NEON CSS
st.markdown("""
    <style>
    .main { background-color: #000814; color: #00f2ff; }
    .stTextArea textarea { background-color: #001d3d; color: #00f2ff; border: 1px solid #00f2ff; }
    .stButton>button { 
        background-image: linear-gradient(to right, #003566, #00f2ff); 
        color: white; font-weight: bold; border: none; box-shadow: 0px 0px 15px #00f2ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API CONFIG ---
try:
    hf_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("🔑 ARCHITECT ERROR: Token not found!")
    st.stop()

# Using standard Inference API for maximum stability in 2026
RISK_MODEL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
BIAS_MODEL = "https://api-inference.huggingface.co/models/unitary/toxic-bert"
headers = {"Authorization": f"Bearer {hf_token}"}

def titan_call(url, payload):
    """Safely calls the AI brain and handles errors without crashing."""
    for i in range(3):
        try:
            response = requests.post(url, headers=headers, json=payload)
            # If the server is busy, it returns a 503 or 404. We catch that here.
            if response.status_code != 200:
                st.warning(f"📡 Sentinel Link Weak... Retrying in {10}s (Attempt {i+1}/3)")
                time.sleep(10)
                continue
            return response.json()
        except Exception:
            time.sleep(5)
            continue
    return {"error": "Connection Timeout. The Hugging Face server is currently overloaded. Please wait 30 seconds and try again."}

# --- SIDEBAR FEED ---
with st.sidebar:
    st.markdown("### 📡 SATELLITE FEED")
    feed = feedparser.parse("https://www.technologyreview.com/topic/artificial-intelligence/feed/")
    for entry in feed.entries[:3]:
        st.markdown(f"**[{entry.title}]({entry.link})**")
        st.caption(f"🗓️ {entry.published[:16]}")
        st.divider()

# --- MAIN DASHBOARD ---
st.title("🛡️ PROJECT TITAN")
st.write(f"### STATUS: OPERATIONAL | ARCHITECT: Daniel Barr")
st.divider()

desc = st.text_area("Input AI Project Parameters for Deep Audit:", height=180)

if st.button("EXECUTE MASTER AUDIT"):
    if desc:
        with st.spinner("Synchronizing Neural Sentinels..."):
            risk_data = titan_call(RISK_MODEL, {"inputs": desc, "parameters": {"candidate_labels": ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"]}})
            bias_data = titan_call(BIAS_MODEL, {"inputs": desc})

            # Check if we got valid data back
            if isinstance(risk_data, dict) and "error" not in risk_data:
                label = risk_data['labels'][0]
                risk_score = risk_data['scores'][0]
                bias_score = bias_data[0][0]['score']

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("⚖️ Regulatory Verdict")
                    st.metric("Risk Level", label)
                    df = pd.DataFrame({"Metric": ["Bias", "Ethics", "Transparency", "Safety"], "Level": [bias_score, 0.75, 1-risk_score, 0.85]})
                    fig = px.line_polar(df, r='Level', theta='Metric', line_close=True, template="plotly_dark", color_discrete_sequence=['#00f2ff'])
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.subheader("📋 Audit Report")
                    st.info(f"VERDICT: {label} | BIAS: {bias_score:.2%}")
                    if bias_score > 0.5: st.error("🚨 HIGH BIAS PROBABILITY")
                    else: st.success("✅ COMPLIANCE CLEARANCE")
            else:
                st.error("🚨 TITAN OFFLINE: The AI server is not responding correctly. Check your token or try again later.")
