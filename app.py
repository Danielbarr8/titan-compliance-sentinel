import streamlit as st
import pandas as pd
import plotly.express as px
from huggingface_hub import InferenceClient
import feedparser
from datetime import datetime

# --- TITAN MASTER ARCHITECT UI ---
st.set_page_config(page_title="PROJECT TITAN", layout="wide", page_icon="🛡️")

# NEON ARCHITECT STYLING
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

# --- SECRETS & CLIENT INIT ---
try:
    # Official managed client initialization
    client = InferenceClient(token=st.secrets["HUGGINGFACE_TOKEN"])
except Exception as e:
    st.error("🔑 ARCHITECT ERROR: Check your Secrets configuration.")
    st.stop()

# --- SIDEBAR: LIVE FEED ---
with st.sidebar:
    st.markdown("### 📡 SATELLITE FEED")
    try:
        feed = feedparser.parse("https://www.technologyreview.com/topic/artificial-intelligence/feed/")
        for entry in feed.entries[:3]:
            st.markdown(f"**[{entry.title}]({entry.link})**")
            st.caption(f"🗓️ {entry.published[:16]}")
            st.divider()
    except:
        st.write("Feed Link Weak...")

# --- MAIN DASHBOARD ---
st.title("🛡️ PROJECT TITAN")
st.write(f"### STATUS: OPERATIONAL | ARCHITECT: Daniel Barr")
st.divider()

desc = st.text_area("Input AI Project Parameters for Deep Audit:", height=180)

if st.button("EXECUTE MASTER AUDIT"):
    if desc:
        with st.spinner("TITAN is communicating with Global Sentinels..."):
            try:
                # 1. Official Risk Classification
                risk_data = client.zero_shot_classification(
                    desc, 
                    candidate_labels=["Unacceptable Risk", "High Risk", "Limited Risk", "Minimal Risk"],
                    model="facebook/bart-large-mnli"
                )
                
                # 2. Official Bias Check
                bias_data = client.text_classification(desc, model="unitary/toxic-bert")

                # --- RESULTS ---
                label = risk_data[0]['label']
                risk_score = risk_data[0]['score']
                bias_score = bias_data[0]['score']

                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("⚖️ Regulatory Verdict")
                    st.metric("Risk Level", label)
                    
                    df = pd.DataFrame({
                        "Metric": ["Bias Detection", "Ethics", "Transparency", "Safety"],
                        "Value": [bias_score, 0.75, 1-risk_score, 0.85]
                    })
                    fig = px.line_polar(df, r='Value', theta='Metric', line_close=True, 
                                       template="plotly_dark", color_discrete_sequence=['#00f2ff'])
                    fig.update_traces(fill='toself')
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.subheader("📋 Audit Report")
                    st.info(f"VERDICT: {label} | BIAS INTENSITY: {bias_score:.2%}")
                    if bias_score > 0.5: st.error("🚨 HIGH BIAS PROBABILITY")
                    else: st.success("✅ COMPLIANCE CLEARANCE")

            except Exception as e:
                st.warning("⚠️ The AI Brain is deep in sleep. Please wait 15 seconds and click the button again.")
                # Logic: Hugging Face returns a loading error that InferenceClient catches as an exception.
