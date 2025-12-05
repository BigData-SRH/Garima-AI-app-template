import streamlit as st
import pandas as pd
from pathlib import Path

st.subheader("🔍 Dataset Health Check")

st.title("Dataset Description")

st.markdown(
    """
### What's Inside

This dataset provides a comprehensive view of the global artificial intelligence job market, containing more than **15,000 real job postings** gathered from major job platforms worldwide. It includes detailed salary information, job requirements, company attributes, and geographic trends.

---

### Key Features

- **15,000+ job listings** spanning **50+ countries**
- Salary information in multiple currencies (**normalized to USD**)
- Categorized experience levels (Entry, Mid, Senior, Executive)
- Company-size segmentation and comparison
- Analysis of **remote**, **hybrid**, and **on-site** work patterns
- Skills frequency and demand analysis
- Geographic salary variations
- Time-series indicators showing changes in market behavior over time

---
"""
)

# ------------------ Load Dataset ------------------
data_path = Path("data") / "AI_DATASET_CLEANED.csv"

try:
    df = pd.read_csv(data_path)
except FileNotFoundError:
    st.error(f"Could not find data file at `{data_path}`.")
    st.stop()

# ------------------ Display Raw Data ------------------
st.subheader("Raw Dataset")
st.dataframe(df, use_container_width=True)


#Footer
st.markdown(
    """
    <div>
        <p style='font-size: 20px; margin-top: 12px;'>
            © <a href='https://www.kaggle.com/datasets/abhishekjaiswal4896/ai-job-market-trends'
                 target='_blank'
                 style='color: Black; text-decoration: none;'>
                 Raw Dataset Source
            </a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)