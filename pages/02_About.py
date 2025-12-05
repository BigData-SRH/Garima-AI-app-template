# 03_About.py
import streamlit as st
from pathlib import Path
import base64


st.set_page_config(
    page_title="About - AI Job Market Dashboard",
    layout="wide",
    page_icon="🤖"
)

# Enhanced CSS styling
st.markdown("""
<style>
    /* Main page styling */
    .main { background-color: #f8f9fa; }

    /* Section headers */
    .section-header {
        font-size: 28px;
        font-weight: 700;
        color: #0b1b2b;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 16px;
        margin-top: 24px;
    }
    
    .subsection-header {
        font-size: 20px;
        font-weight: 600;
        color: #667eea;
        margin-top: 20px;
        margin-bottom: 12px;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 16px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 16px 0;
    }
    
    /* Feature badge */
    .feature-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        margin: 4px;
    }
    
    /* Code blocks */
    .code-snippet {
        background: #f6f8fa;
        padding: 12px;
        border-radius: 8px;
        border-left: 3px solid #667eea;
        font-family: 'Courier New', monospace;
        font-size: 13px;
        margin: 12px 0;
    }
    
    /* Author section */
    .author-section {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        color: white;
        margin: 10px 0;
    }
    
    /* Social links */
    .social-btn {
        display: inline-block;
        margin-right: 12px;
        margin-top: 8px;
        padding: 10px 20px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.2);
        color: white !important;
        text-decoration: none;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    .social-btn:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.5);
    }
    
    /* List styling */
    .custom-list {
        padding-left: 20px;
    }
    
    .custom-list li {
        margin: 8px 0;
        color: #4a5568;
    }
</style>
""", unsafe_allow_html=True)

# Page title
st.markdown("<h1 class='section-header'>🤖 AI Job Market Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 18px; color: #6b7785; margin-bottom: 30px;'>A comprehensive analytics platform for exploring AI and Data Science job opportunities</p>", unsafe_allow_html=True)

# Overview Section
st.markdown("<div class='author-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='subsection-header'>🎯 Project Overview</h2>", unsafe_allow_html=True)
st.markdown("""
This project was developed as part of the **MSc Big Data and AI** program for the 
*Big Data and Business Intelligence* final exam. The dashboard provides an intuitive 
interface to analyze and explore historical job market data for AI and Data Science 
positions from 2024-2025, featuring advanced filtering capabilities and interactive visualizations.
""")
st.markdown("</div>", unsafe_allow_html=True)

# Dashboard Pages Section
st.markdown("<div class='author-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='subsection-header'>🖥️ Dashboard Pages</h2>", unsafe_allow_html=True)

page_col1, page_col2 = st.columns(2)

with page_col1:
    st.markdown("""
    **🏠 Overview**
    - Key metrics and KPIs
    - Active filters display
    - Quick insights
    
    **🔍 Job Search**
    - Browse detailed listings
    - Sortable table view
    - Company information
    """)

with page_col2:
    st.markdown("""
    **📊 Top Job Titles**
    - Top 20 rankings
    - Interactive charts
    - Visual distribution
    
    **🧭 Explorer**
    - Custom column views
    - Data export (CSV)
    - Flexible exploration
    """)

st.markdown("</div>", unsafe_allow_html=True)

# Technical Stack Section
st.markdown("<div class='author-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='subsection-header'>🛠️ Technical Stack</h2>", unsafe_allow_html=True)

tech_col1, tech_col2, tech_col3 = st.columns(3)

with tech_col1:
    st.markdown("""
    **Frontend**
    - Streamlit 1.28+
    - Custom CSS
    - Responsive Layout
    """)

with tech_col2:
    st.markdown("""
    **Data Processing**
    - Pandas 2.0+
    - NumPy 1.24+
    - Python 3.8+
    """)

with tech_col3:
    st.markdown("""
    **Visualization**
    - Plotly 5.14+
    - Altair 5.0+
    - Interactive Charts
    """)

st.markdown("</div>", unsafe_allow_html=True)

# Data Requirements Section
st.markdown("<div class='author-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='subsection-header'>📊 Data Requirements</h2>", unsafe_allow_html=True)

data_col1, data_col2 = st.columns(2)

with data_col1:
    st.markdown("""
    **Required Columns:**
    - Job Title: `job_title`, `title`, `jobTitle`
    - Location: `country`, `company_location`
    - Experience: `experience_level`, `exp_level`
    """)

with data_col2:
    st.markdown("""
    **Optional Columns:**
    - Company: `company_name`, `employer`
    - Remote: `remote_ratio`, `work_setting`
    - Skills: `required_skills`, `skills`
    """)

st.markdown("</div>", unsafe_allow_html=True)

# Installation Section
st.markdown("<div class='author-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='subsection-header'>🚀 Quick Start</h2>", unsafe_allow_html=True)

quick_col1, quick_col2 = st.columns(2)

with quick_col1:
    st.markdown("**Install Dependencies**")
    st.code("""pip install streamlit pandas numpy plotly""", language="bash")

with quick_col2:
    st.markdown("**Run the Dashboard**")
    st.code("""streamlit run app.py""", language="bash")

st.markdown("</div>", unsafe_allow_html=True)

# Author Section
st.markdown("<div class='author-section'>", unsafe_allow_html=True)

author_col1, _ = st.columns([3, 2])

with author_col1:
    # Author text
    st.markdown("""
        <h2 style='margin: 0; color: Black;'>👩‍💻 Author</h2>
        <h3 style='margin: 10px 0; color: Black;'>Garima Agrawal</h3>
        <p style='margin: 0; color: Black; font-size: 16px;'>
        MSc Big Data & AI<br>
        Big Data and Business Intelligence – Final Exam Project
        </p>
        <p style='margin-top: 20px; margin-bottom: 12px; color: Black; font-size: 16px;'>
        Connect with me:
        </p>
    """, unsafe_allow_html=True)

    # Horizontal QR row
    qr1, qr2, qr3 = st.columns(3)

    def clickable_qr(col, file, label, url):
        path = Path("assets") / file
        if path.exists():
            with open(path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode("utf-8")
            col.markdown(
                f"""
                <div style='text-align:left;'>
                    <a href="{url}" target="_blank">
                        <img src="data:image/png;base64,{b64}" style="width:120px; border-radius:10px;" />
                    </a>
                    <div style="color:Black; margin-top:8px; font-size:14px;">{label}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            col.markdown(
                f"""
                <div style='background: rgba(255,255,255,0.15); 
                            padding: 18px; border-radius: 10px; text-align:center;'>
                    <p style='color:Black; margin:0; font-size:13px;'>{label}</p>
                    <p style='color:Black; font-size:10px; margin-top:5px;'>
                        {file} missing
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # ✅ Replace these URLs with your real ones
    clickable_qr(qr1, "Garima.png", "Outlook",  "mailto:Garima.Agrawal@stud.srh-university.de")
    clickable_qr(qr2, "github.png", "GitHub",   "https://github.com/BigData-SRH/Garima-AI-app-template")
    clickable_qr(qr3, "linkedin.png", "LinkedIn","https://www.linkedin.com/in/garima-agrawal-291a78185/")

st.markdown("</div>", unsafe_allow_html=True)


# Version History Section
st.markdown("<div class='author-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='subsection-header'>🔄 Version History</h2>", unsafe_allow_html=True)

version_col1, version_col2 = st.columns(2)

with version_col1:
    st.markdown("""
    **v2.0.0** (Current)
    - Moved filters from sidebar to main page
    - Enhanced UI with gradient styling
    - Improved filter layout with 5-column design
    - Added reset functionality
    """)

with version_col2:
    st.markdown("""
    **v1.0.0**
    - Initial release
    - Sidebar-based filtering
    - Four main dashboard pages
    - Basic visualization and export features
    """)

st.markdown("</div>", unsafe_allow_html=True)

# Acknowledgments Section
st.markdown("<div class='author-section'>", unsafe_allow_html=True)
st.markdown("<h2 class='subsection-header'>🧠 Acknowledgments</h2>", unsafe_allow_html=True)

ack_col1, ack_col2, ack_col3 = st.columns(3)

with ack_col1:
    st.markdown("""
    **🏗️ Built with:**
    - [Streamlit](https://streamlit.io/)
    """)

with ack_col2:
    st.markdown("""
    **☁️ Data Source:**
    - [Data Source](https://www.kaggle.com/datasets/bismasajjad/global-ai-job-market-and-salary-trends-2025)
    """)
    
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7785; padding: 20px;'>
    <p style='font-size: 16px;'>🤖 <strong>AI Job Market Dashboard</strong></p>
    <p style='font-size: 14px;'>Historical data from 2024-2025 | Made with ❤️ for the AI/Data Science community</p>
    <p style='font-size: 12px; margin-top: 12px;'>© 2025 Garima Agrawal | MSc Big Data & AI</p>
</div>
""", unsafe_allow_html=True)