import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px

# ---------- CONFIG ----------
DATA_PATH = Path("data/AI_DATASET_CLEANED.csv")
st.set_page_config(
    page_title="AI Job Market Dashboard", 
    layout="wide",
    page_icon="🤖",
    initial_sidebar_state="collapsed"  # Changed to collapsed
)

# Initialize session state for reset functionality
if 'reset_trigger' not in st.session_state:
    st.session_state.reset_trigger = 0

# ---------- ENHANCED STYLING ----------
st.markdown("""
<style>
/* Main page styling */
.main { background-color: #f8f9fa; }

/* Page header */
.page-title { 
    font-size: 42px; 
    font-weight: 700; 
    margin-bottom: 10px; 
    color: #0b1b2b;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.page-subtitle {
    font-size: 16px;
    color: #6b7785;
    margin-bottom: 30px;
}

/* Filter container */
.filter-section {
    background: linear-gradient(180deg, #ffffff, #fbfdff);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.05);
    margin-bottom: 30px;
}

/* Enhanced Card */
.card {
    background: linear-gradient(180deg, #ffffff, #fbfdff);
    padding: 24px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.08);
    border: 1px solid rgba(0, 0, 0, 0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.12);
}

/* Enhanced KPI metrics */
.kpi-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin: 10px 0;
}

.kpi-title { 
    font-size: 14px; 
    opacity: 0.9;
    margin-bottom: 8px;
    font-weight: 500;
    letter-spacing: 0.5px;
}

.kpi-value { 
    font-size: 36px; 
    font-weight: 700;
    margin: 5px 0;
}

.kpi-subtitle {
    font-size: 12px;
    opacity: 0.8;
    margin-top: 4px;
}

/* Enhanced badges */
.badge { 
    display: inline-block; 
    padding: 6px 12px; 
    border-radius: 20px; 
    font-size: 12px; 
    font-weight: 600;
    color: white;
    margin: 2px;
}
.badge-remote { background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }
.badge-hybrid { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
.badge-onsite { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }

/* Info boxes */
.info-box {
    background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    padding: 16px;
    border-radius: 10px;
    border-left: 4px solid #667eea;
    margin: 16px 0;
}

/* Button styling */
.stButton > button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

/* DataFrames */
.dataframe { 
    border-radius: 10px; 
    overflow: hidden;
}

/* Metric styling */
[data-testid="stMetricValue"] {
    font-size: 32px;
    font-weight: 700;
    color: #667eea;
}

/* Expander styling */
.streamlit-expanderHeader {
    background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
    border-radius: 8px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ---------- HELPERS ----------
@st.cache_data
def load_data(path: Path):
    df = pd.read_csv(path, low_memory=False, parse_dates=True)
    return df

def first_existing_column(df, candidates):
    for c in candidates:
        if c in df.columns:
            return c
    return None

def pick_defaults(options, preferred_list):
    if not options:
        return []
    picks = []
    for p in preferred_list:
        for o in options:
            if p.lower() == o.lower() or p.lower() in o.lower():
                if o not in picks:
                    picks.append(o)
    if not picks:
        picks = options[:2]
    return picks

def format_number(num):
    """Format large numbers with K, M suffixes"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    return str(int(num))

# ---------- LOAD ----------
df = load_data(DATA_PATH)

# Detect columns
job_col = first_existing_column(df, ["job_title", "title", "jobTitle", "Job Title"])
country_col = first_existing_column(df, ["country", "company_location", "location", "company_location_name"])
exp_col = first_existing_column(df, ["experience_level", "experience", "years_experience", "exp_level"])
skills_col = first_existing_column(df, ["required_skills", "skills", "requirements", "skillset"])
company_col = first_existing_column(df, ["company_name", "company", "employer"])
remote_col = first_existing_column(df, [
    "remote_ratio", "remote", "remote_status", "work_setting", "onsite_remote_hybrid"
])

# Normalize string columns
for c in [job_col, country_col, exp_col, remote_col, skills_col, company_col]:
    if c and c in df.columns:
        df[c] = df[c].astype(str).fillna("")

# ---------- SIDEBAR (Minimal) ----------
st.sidebar.markdown("# 🤖 AI Job Market")
st.sidebar.markdown("**Dashboard Navigation**")
st.sidebar.markdown("---")

menu_choice = st.sidebar.radio(
    label="",
    options=[
        "🏠 Overview",
        "🔍 Job Search",
        "📊 Top Job Titles",
        # "🧭 Explorer",
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 Dataset Info")
st.sidebar.metric("Total Jobs", format_number(len(df)))
st.sidebar.caption("💡 Use filters on the main page to refine your search")

# ---------- MAIN PAGE FILTERS ----------
def render_filters():
    """Render filters on the main page"""
    st.markdown("### 🎯 Filter Options")
    
    # Determine if filters should be reset
    reset_filters = (st.session_state.reset_trigger > 0)
    
    # Create filter columns
    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns([2, 2, 2, 2, 1])
    
    # Job Title filter
    with filter_col1:
        if job_col:
            all_job_titles = sorted(df[job_col].replace("", np.nan).dropna().unique())
            default_jobs = [] if reset_filters else pick_defaults(all_job_titles, ["Data Scientist", "Ai Research Scientist"])
            selected_job_titles = st.multiselect(
                "💼 Job Title", 
                all_job_titles, 
                default=default_jobs,
                help="Select one or more job titles",
                key=f"job_titles_{st.session_state.reset_trigger}"
            )
        else:
            selected_job_titles = []
    
    # Location filter
    with filter_col2:
        if country_col:
            all_countries = sorted(df[country_col].replace("", np.nan).dropna().unique())
            germany_matches = [c for c in all_countries if "germany" in c.lower()]
            default_locations = [] if reset_filters else (germany_matches if germany_matches else (all_countries[:1] if all_countries else []))
            selected_countries = st.multiselect(
                "🌍 Location", 
                all_countries, 
                default=default_locations,
                help="Filter by country",
                key=f"countries_{st.session_state.reset_trigger}"
            )
        else:
            selected_countries = []
    
    # Experience filter
    with filter_col3:
        if exp_col:
            all_exp = sorted(df[exp_col].replace("", np.nan).dropna().unique())
            mi_matches = [e for e in all_exp if "mi" in e.lower()]
            default_exp = [] if reset_filters else (mi_matches if mi_matches else (all_exp[:1] if all_exp else []))
            selected_exp = st.multiselect(
                "🎓 Experience Level", 
                all_exp, 
                default=default_exp,
                help="Select experience levels",
                key=f"exp_{st.session_state.reset_trigger}"
            )
        else:
            selected_exp = []
    
    # Remote filter
    with filter_col4:
        if remote_col:
            all_remote = sorted(df[remote_col].dropna().unique().tolist())
            default_remote = [] if reset_filters else ([r for r in all_remote if r != 0][:1] or all_remote[:1])
            selected_remote = st.multiselect(
                "🏡 Remote Ratio (%)", 
                all_remote, 
                default=default_remote,
                help="0=Onsite, 50=Hybrid, 100=Remote",
                key=f"remote_{st.session_state.reset_trigger}"
            )
        else:
            selected_remote = []
    
    # Reset button
    with filter_col5:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.reset_trigger += 1
            st.rerun()
    
    return selected_job_titles, selected_countries, selected_exp, selected_remote

# ---------- FILTERING ----------
def apply_filters(selected_job_titles, selected_countries, selected_exp, selected_remote):
    """Apply filters to the dataframe"""
    mask = pd.Series(True, index=df.index)
    
    if job_col and selected_job_titles:
        mask &= df[job_col].astype(str).isin(selected_job_titles)
    
    if country_col and selected_countries:
        mask &= df[country_col].astype(str).isin(selected_countries)
    
    if exp_col and selected_exp:
        mask &= df[exp_col].astype(str).isin(selected_exp)
    
    if remote_col and selected_remote:
        mask &= df[remote_col].isin(selected_remote)
    
    return df[mask].copy()

# ---------- PAGES ----------

def page_overview():
    st.markdown("<h1 class='page-title'>AI Job Market Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Explore AI and Data Science job opportunities with powerful filtering and insights</p>", unsafe_allow_html=True)
    
    # Render filters
    selected_job_titles, selected_countries, selected_exp, selected_remote = render_filters()
    filtered = apply_filters(selected_job_titles, selected_countries, selected_exp, selected_remote)
    
    st.markdown("---")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Filtered Jobs",
            value=format_number(len(filtered)),
            delta=f"{len(filtered)/len(df)*100:.1f}% of total"
        )
    
    with col2:
        unique_titles = int(filtered[job_col].nunique()) if job_col and not filtered.empty else 0
        st.metric(
            label="💼 Unique Titles",
            value=unique_titles
        )
    
    with col3:
        unique_companies = int(filtered[company_col].nunique()) if company_col and not filtered.empty else 0
        st.metric(
            label="🏢 Companies",
            value=unique_companies
        )
    
    with col4:
        unique_locations = int(filtered[country_col].nunique()) if country_col and not filtered.empty else 0
        st.metric(
            label="🌎 Locations",
            value=unique_locations
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Active filters display
    st.markdown("### 🎯 Active Filters")
    filter_col1, filter_col2 = st.columns(2)
    
    with filter_col1:
        st.markdown(f"""
        <div class='info-box'>
            <strong>Job Titles:</strong> {', '.join(selected_job_titles) if selected_job_titles else 'All'}<br>
            <strong>Locations:</strong> {', '.join(selected_countries) if selected_countries else 'All'}
        </div>
        """, unsafe_allow_html=True)
    
    with filter_col2:
        st.markdown(f"""
        <div class='info-box'>
            <strong>Experience:</strong> {', '.join(selected_exp) if selected_exp else 'All'}<br>
            <strong>Remote Ratio:</strong> {', '.join(map(str, selected_remote)) if selected_remote else 'All'}
        </div>
        """, unsafe_allow_html=True)
    
    # Quick insights
    if not filtered.empty:
        st.markdown("### 📈 Quick Insights")
        
        insight_col1, insight_col2 = st.columns(2)
        
        with insight_col1:
            if job_col:
                top_job = filtered[job_col].value_counts().head(1)
                if not top_job.empty:
                    st.info(f"🔥 **Most Common Role:** {top_job.index[0]} ({top_job.values[0]} listings)")
        
        with insight_col2:
            if country_col:
                top_country = filtered[country_col].value_counts().head(1)
                if not top_country.empty:
                    st.info(f"📍 **Top Location:** {top_country.index[0]} ({top_country.values[0]} jobs)")

def page_job_search():
    st.markdown("<h1 class='page-title'>Job Search</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Browse through available positions</p>", unsafe_allow_html=True)
    
    # Render filters
    selected_job_titles, selected_countries, selected_exp, selected_remote = render_filters()
    filtered = apply_filters(selected_job_titles, selected_countries, selected_exp, selected_remote)
    
    st.markdown("---")
    st.markdown("<h6>Historical job market data for AI and Data Science roles (2024-2025)</h6>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📋 Total Listings", format_number(len(filtered)))
    with col2:
        st.metric("💼 Unique Titles", int(filtered[job_col].nunique()) if job_col and not filtered.empty else 0)
    with col3:
        st.metric("🏢 Unique Companies", int(filtered[company_col].nunique()) if company_col and not filtered.empty else 0)
    
    st.markdown("---")
    
    st.markdown(f"### 📄 Job Listings ({len(filtered)} results)")
    
    display_cols = [c for c in [job_col, company_col, country_col, exp_col, remote_col] if c in filtered.columns]
    
    st.dataframe(
        filtered[display_cols].head(50).reset_index(drop=True), 
        use_container_width=True,
        height=600
    )

def page_top_job_titles():
    st.markdown("<h1 class='page-title'>Top Job Titles</h1>", unsafe_allow_html=True)
    st.markdown("<p class='page-subtitle'>Most in-demand positions in the current market</p>", unsafe_allow_html=True)
    
    # Render filters
    selected_job_titles, selected_countries, selected_exp, selected_remote = render_filters()
    filtered = apply_filters(selected_job_titles, selected_countries, selected_exp, selected_remote)
    
    st.markdown("---")

    if not job_col or filtered.empty:
        st.info("No job-title data available.")
        return

    counts = filtered[job_col].astype(str).value_counts()
    top_n = min(20, len(counts))
    top_counts = counts.head(top_n).reset_index()
    top_counts.columns = ["Job Title", "Count"]
    
    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Top Title", top_counts.iloc[0]["Job Title"])
    with col2:
        st.metric("🔢 Listings", top_counts.iloc[0]["Count"])
    with col3:
        avg_per_title = top_counts["Count"].mean()
        st.metric("📈 Avg per Title", f"{avg_per_title:.0f}")
    
    st.markdown("---")

    # Table first
    st.markdown("### 📋 Job Title Rankings")
    st.dataframe(top_counts.reset_index(drop=True), use_container_width=True, height=400)

    st.markdown("<br>", unsafe_allow_html=True)

    # Chart
    st.markdown("### 📊 Visual Distribution")
    hc = top_counts[::-1].reset_index(drop=True)

    vals = hc["Count"].values.astype(float)
    norm = (vals - vals.min()) / (vals.max() - vals.min() + 1e-9)
    base_rgb = np.array([102, 126, 234])
    light_rgb = np.array([118, 75, 162])
    colors = [
        "rgb({},{},{})".format(
            int(base_rgb[0] * (1 - v) + light_rgb[0] * v),
            int(base_rgb[1] * (1 - v) + light_rgb[1] * v),
            int(base_rgb[2] * (1 - v) + light_rgb[2] * v),
        )
        for v in norm
    ]

    height_px = max(400, hc.shape[0] * 48)
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=hc["Count"],
        y=hc["Job Title"],
        orientation='h',
        marker=dict(color=colors, line=dict(width=0)),
        hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
        text=hc["Count"].astype(int),
        textposition='inside',
        textfont=dict(color='white', size=12, family='Arial'),
        showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=hc["Count"],
        y=hc["Job Title"],
        mode='markers',
        marker=dict(size=28, color=colors, line=dict(width=0)),
        hoverinfo='skip',
        showlegend=False
    ))

    fig.update_layout(
        height=height_px,
        margin=dict(l=240, r=24, t=40, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(248,249,250,1)',
        bargap=0.22,
        xaxis=dict(
            title="Number of Listings", 
            showgrid=True, 
            gridcolor="rgba(200,200,200,0.2)", 
            zeroline=False,
            title_font=dict(size=14, family='Arial')
        ),
        yaxis=dict(automargin=True, title_font=dict(size=14, family='Arial')),
        showlegend=False,
        font=dict(family='Arial', size=12)
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# def page_explorer():
#     st.markdown("<h1 class='page-title'>Data Explorer</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='page-subtitle'>Dive deep into the dataset with custom views</p>", unsafe_allow_html=True)
    
#     # Render filters
#     selected_job_titles, selected_countries, selected_exp, selected_remote = render_filters()
#     filtered = apply_filters(selected_job_titles, selected_countries, selected_exp, selected_remote)
    
#     st.markdown("---")
    
#     col1, col2 = st.columns([3, 1])
    
#     with col1:
#         st.metric("📊 Rows in View", format_number(len(filtered)))
#     with col2:
#         st.metric("🔢 Columns", len(filtered.columns))
    
#     st.markdown("---")
    
#     default_cols = [job_col, company_col, country_col, exp_col, remote_col] if job_col else filtered.columns.tolist()[:6]
#     cols_to_show = st.multiselect(
#         "📋 Select Columns to Display", 
#         options=filtered.columns.tolist(),
#         default=default_cols,
#         help="Choose which columns to view and export"
#     )
    
#     if cols_to_show:
#         st.markdown(f"### 📄 Dataset Preview ({len(filtered)} rows)")
#         st.dataframe(
#             filtered[cols_to_show].reset_index(drop=True), 
#             use_container_width=True,
#             height=500
#         )
        
#         @st.cache_data
#         def to_csv(df_):
#             return df_.to_csv(index=False).encode("utf-8")
        
#         st.download_button(
#             "⬇️ Download Filtered Data (CSV)", 
#             to_csv(filtered[cols_to_show]), 
#             file_name="ai_jobs_filtered.csv", 
#             mime="text/csv",
#             help="Download the current filtered view as CSV"
#         )
#     else:
#         st.warning("⚠️ Please select at least one column to display")

# Route to pages
if menu_choice == "🏠 Overview":
    page_overview()
elif menu_choice == "🔍 Job Search":
    page_job_search()
elif menu_choice == "📊 Top Job Titles":
    page_top_job_titles()
# elif menu_choice == "🧭 Explorer":
#     page_explorer()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6b7785; padding: 20px;'>
    <p>🤖 <strong>AI Job Market Dashboard</strong></p>
    <p>Historical data from 2024-2025</p>
</div>
""", unsafe_allow_html=True)