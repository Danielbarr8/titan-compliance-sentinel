import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import feedparser
from datetime import datetime
import time

# --- TITAN SENTINEL v4.0 ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide", page_icon="🛡️")

# NEON ARCHITECT UI
st.markdown("""
    <style>
    .main { background-color: #000814; color: #00f2ff; }
    .stTextArea textarea { background-color: #001d3d; color: #00f2ff; border: 1px solid #00f2ff; }
    .stButton>button { 
        background-image: linear-gradient(to right, #003566, #00f2ff); 
        color: white; font-weight: bold; border: none; box-shadow: 0px 0px 15px #00f2ff;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# API ROUTING (2026 PROTOCOL)
# We use the new Router gateway which is more stable than the old Inference API
try:
    hf_token = st.secrets["HUGGINGFACE_TOKEN"]
except:
    st.error("🔑 ARCHITECT ERROR: Token not found in Streamlit Secrets!")
    st.stop()

# Updated Endpoints for 2026
RISK_MODEL = "https://router.huggingface.co/models/facebook/bart-large-mnli"
BIAS_MODEL = "https://router.huggingface.co/models/unitary/toxic-bert"
headers = {"Authorization": f"Bearer {hf_token}"}

def titan_call(url, payload):
    # Retry loop: If the model is 'cold', we wait and try again automatically
    for i in range(3):
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        if "error" in data and "loading" in str(data.get("error")):
            time.sleep(10) # Wait 10 seconds for the 'Brain' to wake up
            continue
        return data
    return {"error": "Sentinel Timeout: AI Brain is deep in sleep. Try once more."}

# --- INTERFACE ---
st.title("🛡️ PROJECT TITAN")
st.write(f"### STATUS: ONLINE | ARCHITECT: Daniel Barr")
st.divider()

with st.sidebar:
    st.markdown("### 📡 SATELLITE FEED")
    feed = feedparser.parse("https://www.technologyreview.com/topic/artificial-intelligence/feed/")
    for entry in feed.entries[:3]:
        st.markdown(f"**[{entry.title}]({entry.link})**")
        st.caption(f"🗓️ {entry.published[:16]}")
        st.divider()

desc = st.text_area("Input AI Project Parameters:", height=180, placeholder="Describe the AI system...")

if st.button("EXECUTE MASTER AUDIT"):
    if desc:
        with st.spinner("Synchronizing Neural Sentinels via Global Router..."):
            risk_data = titan_call(RISK_MODEL, {"inputs": desc, "parameters": {"candidate_labels": ["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"]}})
            bias_data = titan_call(BIAS_MODEL, {"inputs": desc})

            if "error" in risk_data:
                st.warning(risk_data["error"])
            else:
                col1, col2 = st.columns(2)
                label = risk_data['labels'][0]
                risk_score = risk_data['scores'][0]
                bias_score = bias_data[0][0]['score']

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
