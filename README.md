# 🛡️ PROJECT TITAN
**AI Compliance Architect & Regulatory Sentinel**

---

## 🧬 Technical Architecture: The TITAN Logic

### 1. Neural Risk Mapping
Project TITAN utilizes **Zero-Shot Classification** via the `facebook/bart-large-mnli` model. Unlike standard AI, this engine does not require pre-labeled data. It uses **Natural Language Inference (NLI)** to calculate the logical entailment between the user's project description and the official EU AI Act risk categories.

**The Math:**
TITAN calculates a probability distribution across $N$ categories. If the project description $P$ logically entails the definition of "High Risk" $R$, the system outputs:

$$Score = \text{softmax}(e_{P \to R})$$

### 2. Bias Sentinel
The Bias Sentinel runs a parallel **Transformer-based Sentiment & Toxicity Analysis** using `unitary/toxic-bert`. It decomposes text into 768-dimensional vectors to identify hidden patterns of discrimination or harmful intent that standard keyword filters miss.



### 3. Integrated Workflow
* **Frontend:** Streamlit (Python-based Web Framework)
* **Intelligence:** Hugging Face Inference API
* **Data Visualization:** Plotly (Dynamic Radar Charting)

---
