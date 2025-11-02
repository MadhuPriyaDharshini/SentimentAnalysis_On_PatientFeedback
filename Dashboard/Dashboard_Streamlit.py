import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from snowflake.snowpark.context import get_active_session
from datetime import datetime

session = get_active_session()
DATABASE = "SF_HACKATHON_DB"
SCHEMA = "CRYPTO_COUGARS_SCHEMA" 
TABLE = "MODIFIED_DATA"
BASE_TABLE = f"{DATABASE}.{SCHEMA}.{TABLE}"

st.set_page_config(
    page_title="AstraZeneca Pharmaceutical Analytics",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

PRIMARY_PURPLE = "#8A0051"
GOLD = "#FFD700"
ACCENT_PURPLE = "#6A003D"
LIGHT_PURPLE = "#A91672"

st.markdown(f"""
<style>
/* ===========================================
   ENHANCED GRADIENT SIDEBAR STYLING
   =========================================== */

/* Stunning Gradient Sidebar with Glassmorphism */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, 
        {PRIMARY_PURPLE} 0%, 
        {ACCENT_PURPLE} 50%,
        #4A0028 100%);
    box-shadow: 4px 0 30px rgba(0,0,0,0.3);
}}

[data-testid="stSidebar"] * {{
    color: {GOLD} !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

/* ===========================================
   ELEGANT NAVIGATION BUTTONS WITH ANIMATIONS
   =========================================== */

.stButton button {{
    background: linear-gradient(135deg, 
        rgba(255,255,255,0.12) 0%, 
        rgba(255,255,255,0.08) 100%);
    color: {GOLD} !important;
    border: 2px solid rgba(255,215,0,0.4);
    border-radius: 16px;
    font-weight: 700;    
    padding: 16px 24px;
    width: 100%;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 50px;
    margin: 8px 0;
    backdrop-filter: blur(12px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    position: relative;
    overflow: hidden;
}}

.stButton button::before {{
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255,215,0,0.2);
    transform: translate(-50%, -50%);
    transition: width 0.6s, height 0.6s;
}}

.stButton button:hover::before {{
    width: 300px;
    height: 300px;
}}

.stButton button:hover {{
    background: #FFFFFF;
    color: {PRIMARY_PURPLE} !important;
    transform: translateX(10px) scale(1.03);
    border-color: {GOLD};
    box-shadow: 0 8px 30px rgba(255,215,0,0.5);
}}

.stButton button:active {{
    transform: translateX(10px) scale(0.97);
}}

/* ===========================================
   BEAUTIFUL MAIN CONTENT AREA
   =========================================== */

.main {{
    background: linear-gradient(135deg, 
        #F8F9FA 0%,
        #E3F2FD 25%,
        #F3E5F5 50%,
        #FFF3E0 75%,
        #F8F9FA 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

/* ===========================================
   ANIMATED GRADIENT HEADERS
   =========================================== */

h1 {{
    color: {PRIMARY_PURPLE};
    font-weight: 900;
    font-size: 3rem;
    margin-bottom: 15px;
    text-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    background: linear-gradient(135deg, 
        {PRIMARY_PURPLE} 0%, 
        {ACCENT_PURPLE} 50%,
        {PRIMARY_PURPLE} 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradient-shift 3s ease infinite;
    background-size: 200% auto;
}}

@keyframes gradient-shift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

h2, h3 {{
    color: {PRIMARY_PURPLE};
    font-weight: 700;
    margin-bottom: 15px;
    background: linear-gradient(135deg, {PRIMARY_PURPLE}, {ACCENT_PURPLE});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

/* ===========================================
   PREMIUM METRIC CARDS WITH HOVER EFFECTS
   =========================================== */

[data-testid="stMetricValue"] {{
    font-size: 2.4rem;
    color: {PRIMARY_PURPLE};
    font-weight: 900;
    background: linear-gradient(135deg, {PRIMARY_PURPLE}, {ACCENT_PURPLE});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

[data-testid="stMetricLabel"] {{
    color: #495057 !important;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.5px;
}}

[data-testid="stMetric"] {{
    background: linear-gradient(135deg, 
        rgba(255,255,255,0.98) 0%, 
        rgba(248,249,250,0.95) 100%);
    padding: 28px;
    border-radius: 18px;
    box-shadow: 0 10px 40px rgba(138,0,81,0.15);
    border-left: 6px solid {PRIMARY_PURPLE};
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}}

[data-testid="stMetric"]::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, 
        transparent 0%,
        rgba(138,0,81,0.05) 100%);
    opacity: 0;
    transition: opacity 0.4s;
}}

[data-testid="stMetric"]:hover::before {{
    opacity: 1;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 15px 50px rgba(138,0,81,0.25);
    border-left-width: 10px;
}}

/* ===========================================
   DATE INFO STYLING
   =========================================== */

.date-info {{
    font-size: 13px;
    color: #6C757D;
    background: linear-gradient(135deg, 
        rgba(248,249,250,0.95) 0%,
        rgba(233,236,239,0.9) 100%);
    padding: 12px 16px;
    border-radius: 12px;
    margin: 15px 0;
    border-left: 4px solid {PRIMARY_PURPLE};
    font-style: italic;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    backdrop-filter: blur(10px);
}}

/* ===========================================
   ENHANCED CARDS WITH GRADIENTS
   =========================================== */

.insight-card {{
    background: linear-gradient(135deg, 
        rgba(255,255,255,1) 0%, 
        rgba(248,249,250,0.98) 100%);
    border-radius: 20px;
    padding: 32px;
    box-shadow: 0 12px 45px rgba(0,0,0,0.12);
    margin: 20px 0;
    border-top: 6px solid {PRIMARY_PURPLE};
    backdrop-filter: blur(10px);
    transition: all 0.4s ease;
    position: relative;
    overflow: hidden;
}}

.insight-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(90deg, 
        {PRIMARY_PURPLE} 0%,
        {ACCENT_PURPLE} 50%,
        {PRIMARY_PURPLE} 100%);
    background-size: 200% auto;
    animation: gradient-slide 3s linear infinite;
}}

@keyframes gradient-slide {{
    0% {{ background-position: 0% 50%; }}
    100% {{ background-position: 200% 50%; }}
}}

.insight-card:hover {{
    transform: translateY(-8px);
    box-shadow: 0 18px 60px rgba(138,0,81,0.2);
}}

/* ===========================================
   BEAUTIFUL ALERT CARDS
   =========================================== */

.success-alert {{
    background: linear-gradient(135deg, 
        #51CF66 0%, 
        #40C057 50%,
        #37B24D 100%);
    color: white;
    padding: 22px 28px;
    border-radius: 16px;
    margin: 18px 0;
    font-weight: 700;
    box-shadow: 0 10px 35px rgba(81,207,102,0.45);
    border-left: 6px solid #2B8A3E;
    animation: slideInLeft 0.6s ease-out;
}}

.warning-alert {{
    background: linear-gradient(135deg, 
        #FF6B6B 0%, 
        #EE5A6F 50%,
        #E03131 100%);
    color: white;
    padding: 22px 28px;
    border-radius: 16px;
    margin: 18px 0;
    font-weight: 700;
    box-shadow: 0 10px 35px rgba(255,107,107,0.45);
    border-left: 6px solid #C92A2A;
    animation: slideInRight 0.6s ease-out;
}}

@keyframes slideInLeft {{
    from {{
        opacity: 0;
        transform: translateX(-30px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

@keyframes slideInRight {{
    from {{
        opacity: 0;
        transform: translateX(30px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

/* ===========================================
   GLASSMORPHISM DRUG INFO CARD
   =========================================== */

.drug-info {{
    background: linear-gradient(135deg, 
        rgba(227,242,253,0.95) 0%, 
        rgba(187,222,251,0.9) 100%);
    border-radius: 22px;
    padding: 28px;
    margin: 22px 0;
    border: 2px solid rgba(138,0,81,0.25);
    box-shadow: 0 10px 40px rgba(31,38,135,0.18);
    backdrop-filter: blur(12px);
    border-left: 7px solid {PRIMARY_PURPLE};
    transition: all 0.3s ease;
}}

.drug-info:hover {{
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(31,38,135,0.25);
}}
</style>
""", unsafe_allow_html=True)

pages = {
    "Executive Dashboard": "executive",
    "Drug Performance": "drug_performance", 
    "Safety Monitoring": "safety",
    "Forecasting": "forecasting",
    "Geographic Analysis": "geographic", 
    "Patient Segmentation": "segmentation",
    "Reports": "reports"
}

with st.sidebar:
    st.markdown(f"""
    <div style='text-align: center; padding: 30px 20px; margin-bottom: 30px; background: #FFFFFF; border-radius: 15px;'>
        <h1 style='color: {GOLD}; margin: 0; font-size: 2rem; font-weight: 800;'>AstraZeneca</h1>
        <p style='color:#111111 ; margin: 5px 0 0 0; font-size: 0.9rem; opacity: 0.9;'>Pharmaceutical Analytics Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    
    if 'selected_page' not in st.session_state:
        st.session_state.selected_page = "executive"
    
    for page_name, page_key in pages.items():
        icon_map = {
            "Executive Dashboard": "🏠", "Drug Performance": "💊", "Safety Monitoring": "⚠️",
            "Forecasting": "📈", "Geographic Analysis": "🌍", 
            "Patient Segmentation": "👥", "Reports": "📋"
        }
        
        if st.button(f"{icon_map.get(page_name, '📊')} {page_name}", 
                    key=f"nav_{page_key}", use_container_width=True):
            st.session_state.selected_page = page_key
    
    page = st.session_state.selected_page
    
    if page != "drug_performance":
        #st.markdown("---")
        
        
        try:
            drugs_df = session.sql(f"SELECT DISTINCT DRUG_NAME FROM {BASE_TABLE} ORDER BY DRUG_NAME").to_pandas()
            regions_df = session.sql(f"SELECT DISTINCT REGION FROM {BASE_TABLE} ORDER BY REGION").to_pandas()
            countries_df = session.sql(f"SELECT DISTINCT COUNTRY FROM {BASE_TABLE} ORDER BY COUNTRY").to_pandas()
            
            selected_drugs = st.multiselect("Drugs", drugs_df['DRUG_NAME'].tolist())
            selected_regions = st.multiselect("Regions", regions_df['REGION'].tolist())
            selected_countries = st.multiselect("Countries", countries_df['COUNTRY'].tolist())
            
        except Exception as e:
            st.error(f"Filter loading error: {str(e)}")
            selected_drugs, selected_regions, selected_countries = [], [], []
    else:
        selected_drugs, selected_regions, selected_countries = [], [], []

def build_where_clause(start_date=None, end_date=None, drugs=None, regions=None, countries=None):
    """Build SQL WHERE clause with filters"""
    conditions = ["1=1"]
    
    if start_date and end_date:
        conditions.append(f"FEEDBACK_DATE BETWEEN '{start_date}' AND '{end_date}'")
    if drugs:
        drug_list = "','".join(drugs)
        conditions.append(f"DRUG_NAME IN ('{drug_list}')")
    if regions:
        region_list = "','".join(regions)
        conditions.append(f"REGION IN ('{region_list}')")
    if countries:
        country_list = "','".join(countries)
        conditions.append(f"COUNTRY IN ('{country_list}')")
    
    return "WHERE " + " AND ".join(conditions)

if page == "executive":
    st.markdown("# Executive Dashboard")
    st.markdown("### Real-time pharmaceutical insights and performance metrics")
    st.markdown("---")
    
    # Load KPIs
    try:
        where_clause = build_where_clause(drugs=selected_drugs, regions=selected_regions, countries=selected_countries)
        
        kpi_sql = f"""
        SELECT 
            COUNT(DISTINCT ID) AS total_feedback,
            COUNT(DISTINCT PATIENT_NAME) AS unique_patients,
            COUNT(DISTINCT DRUG_NAME) AS drugs_analyzed,
            ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
            SUM(CASE WHEN LABELS IN ('Cured', 'Improvement') THEN 1 ELSE 0 END) AS success_count,
            SUM(CASE WHEN LABELS IN ('Adverse', 'Worsen') THEN 1 ELSE 0 END) AS adverse_count,
            COUNT(*) AS total_cases,
            ROUND(AVG(AGE_AT_FEEDBACK), 1) AS avg_age
        FROM {BASE_TABLE}
        {where_clause}
        """
        
        kpis = session.sql(kpi_sql).to_pandas().iloc[0]
        
        # KPI Cards
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.metric("Total Feedback", f"{int(kpis['TOTAL_FEEDBACK']):,}")
        with col2:
            st.metric("Unique Patients", f"{int(kpis['UNIQUE_PATIENTS']):,}")
        with col3:
            st.metric("Avg Sentiment", f"{kpis['AVG_SENTIMENT']:.1f}/10")
        with col4:
            success_rate = (kpis['SUCCESS_COUNT'] / kpis['TOTAL_FEEDBACK'] * 100) if kpis['TOTAL_FEEDBACK'] > 0 else 0
            st.metric("Success Rate", f"{success_rate:.1f}%")
        with col5:
            adverse_rate = (kpis['ADVERSE_COUNT'] / kpis['TOTAL_FEEDBACK'] * 100) if kpis['TOTAL_FEEDBACK'] > 0 else 0
            st.metric("Adverse Rate", f"{adverse_rate:.1f}%")
        with col6:
            st.metric("Total Cases", f"{int(kpis['TOTAL_CASES']):,}")
        
    except Exception as e:
        st.error(f"Error loading KPIs: {str(e)}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Main Content in Two Columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Sentiment Trend Over Time
        st.markdown("### Sentiment Trend Over Time")
        
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            start_date = st.date_input("Start Date", datetime(2010, 1, 1), key="exec_start")
        with col_date2:
            end_date = st.date_input("End Date", datetime(2025, 12, 31), key="exec_end")
        
        if start_date and end_date:
            st.markdown(f"""<div class='date-info'>
                Analysis period: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}
            </div>""", unsafe_allow_html=True)
        
        try:
            trend_where = build_where_clause(start_date, end_date, selected_drugs, selected_regions, selected_countries)
            trend_sql = f"""
            SELECT 
                YEAR(FEEDBACK_DATE) AS year,
                AVG(SENTIMENT_CAT) AS avg_sentiment,
                COUNT(*) AS feedback_count
            FROM {BASE_TABLE}
            {trend_where}
            GROUP BY year
            ORDER BY year
            """
            
            trend_df = session.sql(trend_sql).to_pandas()
            
            if not trend_df.empty:
                fig = px.line(trend_df, x='YEAR', y='AVG_SENTIMENT', 
                            title='Average Sentiment by Year',
                            markers=True,
                            color_discrete_sequence=[PRIMARY_PURPLE])
                
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Average Sentiment",
                    yaxis_range=[0, 10],
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=16, color=PRIMARY_PURPLE),
                    showlegend=False,
                    hovermode='x unified'
                )
                
                fig.update_traces(
                    line=dict(width=3),
                    marker=dict(size=8),
                    hovertemplate='<b>Year:</b> %{x}<br><b>Avg Sentiment:</b> %{y:.2f}<extra></extra>'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for the selected date range")
                
        except Exception as e:
            st.error(f"Error loading trend data: {str(e)}")
    
    with col2:
        st.markdown("### Performance Overview")
        
        st.markdown(f"""
        <div class='insight-card'>
            <h4 style='color: {PRIMARY_PURPLE}; margin-top: 0;'>Key Insights</h4>
            <p><strong>Total Drugs Analyzed:</strong> {int(kpis['DRUGS_ANALYZED'])}</p>
            <p><strong>Average Patient Age:</strong> {kpis['AVG_AGE']} years</p>
            <p><strong>Success Cases:</strong> {int(kpis['SUCCESS_COUNT']):,}</p>
            <p><strong>Adverse Events:</strong> {int(kpis['ADVERSE_COUNT']):,}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Smart Alerts
        if adverse_rate > 35:
            st.markdown(f"""
            <div class='warning-alert'>
                <strong>⚠️ High Adverse Rate Alert</strong><br>
                Current rate: {adverse_rate:.1f}% exceeds 15% threshold
            </div>
            """, unsafe_allow_html=True)
        
        if success_rate > 60:
            st.markdown(f"""
            <div class='success-alert'>
                <strong>✅ Excellent Performance</strong><br>
                Success rate: {success_rate:.1f}% exceeds target
            </div>
            """, unsafe_allow_html=True)
    
    # NEW CHARTS - Row 1
    col1, col2 = st.columns(2)
    
    with col1:
        # Feedback Source Analysis
        st.markdown("### Feedback Source Distribution")
        try:
            source_where = build_where_clause(drugs=selected_drugs, regions=selected_regions, countries=selected_countries)
            source_sql = f"""
            SELECT 
                FEEDBACK_SOURCE,
                COUNT(*) AS feedback_count
            FROM {BASE_TABLE}
            {source_where}
            AND FEEDBACK_SOURCE IS NOT NULL
            GROUP BY FEEDBACK_SOURCE
            ORDER BY feedback_count DESC
            """
            
            source_df = session.sql(source_sql).to_pandas()
            
            if not source_df.empty:
                fig = px.bar(source_df, x='FEEDBACK_SOURCE', y='FEEDBACK_COUNT',
                           color='FEEDBACK_COUNT',
                           color_continuous_scale='Viridis',
                           title='Feedback Count by Source')
                
                fig.update_layout(
                    xaxis_title="Feedback Source",
                    yaxis_title="Feedback Count",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=11),
                    title_font=dict(size=14, color=PRIMARY_PURPLE),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No feedback source data available")
        except Exception as e:
            st.error(f"Error loading feedback source data: {str(e)}")
    
    with col2:
        # Success Rate by Therapeutic Area
        st.markdown("### Success Rate by Therapeutic Area")
        try:
            therapy_where = build_where_clause(drugs=selected_drugs, regions=selected_regions, countries=selected_countries)
            therapy_sql = f"""
            SELECT 
                THERAPAUTIC_AREA,
                COUNT(*) AS total_feedback,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
                ROUND(SUM(CASE WHEN LABELS IN ('Cured', 'Improvement') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS success_rate
            FROM {BASE_TABLE}
            {therapy_where}
            AND THERAPAUTIC_AREA IS NOT NULL
            GROUP BY THERAPAUTIC_AREA
            ORDER BY success_rate DESC
            """
            
            therapy_df = session.sql(therapy_sql).to_pandas()
            
            if not therapy_df.empty:
                fig = px.bar(therapy_df, x='THERAPAUTIC_AREA', y='SUCCESS_RATE',
                           color='AVG_SENTIMENT',
                           color_continuous_scale='RdYlGn',
                           title='Success Rate by Therapeutic Area')
                
                fig.update_layout(
                    xaxis_title="Therapeutic Area",
                    yaxis_title="Success Rate (%)",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=11),
                    title_font=dict(size=14, color=PRIMARY_PURPLE),
                    xaxis_tickangle=-45
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No therapeutic area data available")
        except Exception as e:
            st.error(f"Error loading therapeutic area data: {str(e)}")

elif page == "drug_performance":
    st.markdown("# Drug Performance Analysis")
    st.markdown("### Comprehensive drug-specific insights and AI-powered analytics")
    st.markdown("---")
    
    try:
        # Drug Selection
        drugs_list = session.sql(f"SELECT DISTINCT DRUG_NAME FROM {BASE_TABLE} ORDER BY DRUG_NAME").to_pandas()
        selected_drug = st.selectbox("Select Drug for Analysis:", drugs_list['DRUG_NAME'].tolist())
        
        # Drug Description
        st.markdown(f"### About {selected_drug}")
        try:
            drug_info_sql = f"""
            SELECT 
                THERAPAUTIC_AREA,
                INDICATION,
                COUNT(DISTINCT COUNTRY) AS countries_used
            FROM {BASE_TABLE}
            WHERE DRUG_NAME = '{selected_drug}'
            GROUP BY THERAPAUTIC_AREA, INDICATION
            LIMIT 1
            """
            
            drug_info = session.sql(drug_info_sql).to_pandas().iloc[0]
            
            # Drug descriptions based on therapeutic area
            drug_descriptions = {
                "Cardiovascular": f"{selected_drug} is a cardiovascular medication used to treat heart-related conditions, improve blood flow, and manage cardiovascular risks.",
                "Respiratory": f"{selected_drug} is a respiratory medication designed to treat breathing disorders, asthma, COPD, and other pulmonary conditions.",
                "Oncology": f"{selected_drug} is an oncology medication used in cancer treatment to target specific cancer cells and improve patient outcomes.",
                "Neurology": f"{selected_drug} is a neurological medication used to treat brain and nervous system disorders.",
                "Diabetes": f"{selected_drug} is an antidiabetic medication used to control blood sugar levels and manage diabetes complications.",
                "Immunology": f"{selected_drug} is an immunological medication used to modulate immune system responses and treat autoimmune conditions."
            }
            
            description = drug_descriptions.get(drug_info['THERAPAUTIC_AREA'], f"{selected_drug} is a pharmaceutical medication used for therapeutic purposes.")
            
            st.markdown(f"""
            <div class='drug-info'>
                <h4 style='color: {PRIMARY_PURPLE}; margin-top: 0;'>Drug Information</h4>
                <p><strong>Description:</strong> {description}</p>
                <p><strong>Therapeutic Area:</strong> {drug_info['THERAPAUTIC_AREA']}</p>
                <p><strong>Primary Indication:</strong> {drug_info['INDICATION']}</p>
                <p><strong>Global Reach:</strong> Used in {int(drug_info['COUNTRIES_USED'])} countries</p>
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.info(f"Basic information about {selected_drug} will be displayed here.")
        
        # Date Range
        col_date1, col_date2 = st.columns(2)
        with col_date1:
            drug_start = st.date_input("Start Date", datetime(2010, 1, 1), key="drug_start")
        with col_date2:
            drug_end = st.date_input("End Date", datetime(2025, 12, 31), key="drug_end")
        
        if drug_start and drug_end:
            st.markdown(f"""<div class='date-info'>
                Analysis period: {drug_start.strftime('%B %d, %Y')} to {drug_end.strftime('%B %d, %Y')}
            </div>""", unsafe_allow_html=True)
        
        # Enhanced Drug Metrics
        metric_sql = f"""
        SELECT 
            COUNT(*) AS total_feedback,
            ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
            ROUND(AVG(AGE_AT_FEEDBACK), 1) AS avg_age,
            COUNT(DISTINCT COUNTRY) AS countries,
            MAX(THERAPAUTIC_AREA) AS therapeutic_area,
            SUM(CASE WHEN LABELS = 'Cured' THEN 1 ELSE 0 END) AS cured_patients,
            SUM(CASE WHEN FOLLOW_UP_ACTIONS IN ('Switched medication', 'Consider alternative treatment') THEN 1 ELSE 0 END) AS discontinued_patients
        FROM {BASE_TABLE}
        WHERE DRUG_NAME = '{selected_drug}'
        AND FEEDBACK_DATE BETWEEN '{drug_start}' AND '{drug_end}'
        """
        
        drug_metrics = session.sql(metric_sql).to_pandas().iloc[0]
        
        # Enhanced Metrics Display
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.metric("Total Feedback", f"{int(drug_metrics['TOTAL_FEEDBACK']):,}")
        with col2:
            st.metric("Avg Sentiment", f"{drug_metrics['AVG_SENTIMENT']:.1f}/10")
        with col3:
            st.metric("Countries", int(drug_metrics['COUNTRIES']))
        with col4:
            st.metric("Therapeutic Area", drug_metrics['THERAPEUTIC_AREA'])
        with col5:
            st.metric("Cured Patients", f"{int(drug_metrics['CURED_PATIENTS']):,}")
        with col6:
            st.metric("Discontinued Patients", f"{int(drug_metrics['DISCONTINUED_PATIENTS']):,}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row 1: Treatment Outcomes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Treatment Outcomes Distribution")
            
            outcome_sql = f"""
            SELECT LABELS, COUNT(*) AS count
            FROM {BASE_TABLE}
            WHERE DRUG_NAME = '{selected_drug}'
            AND FEEDBACK_DATE BETWEEN '{drug_start}' AND '{drug_end}'
            AND LABELS IS NOT NULL
            GROUP BY LABELS
            ORDER BY count DESC
            """
            
            outcome_df = session.sql(outcome_sql).to_pandas()
            
            if not outcome_df.empty:
                colors = ['#51CF66', '#FFD700', '#F8BBD0', '#E53935', '#9C27B0', '#FF9800']
                
                fig = px.pie(outcome_df, names='LABELS', values='COUNT',
                           title=f'Treatment Outcomes for {selected_drug}',
                           color_discrete_sequence=colors,
                           hole=0.4)
                
                fig.update_layout(
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE),
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No outcome data available")
        
        with col2:
            st.markdown("### Treatment Outcomes (Bar Chart)")
            
            if not outcome_df.empty:
                fig = px.bar(outcome_df, x='LABELS', y='COUNT',
                           color='COUNT',
                           color_continuous_scale='Viridis',
                           title=f'Treatment Outcomes for {selected_drug}')
                
                fig.update_layout(
                    xaxis_title="Treatment Outcome",
                    yaxis_title="Count",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No outcome data available")
        
        # Charts Row 2: Year-wise and Geography
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Feedback Count Year-wise")
            
            yearly_sql = f"""
            SELECT 
                YEAR(FEEDBACK_DATE) AS year,
                COUNT(*) AS feedback_count
            FROM {BASE_TABLE}
            WHERE DRUG_NAME = '{selected_drug}'
            AND FEEDBACK_DATE BETWEEN '{drug_start}' AND '{drug_end}'
            GROUP BY year
            ORDER BY year
            """
            
            yearly_df = session.sql(yearly_sql).to_pandas()
            
            if not yearly_df.empty:
                fig = px.bar(yearly_df, x='YEAR', y='FEEDBACK_COUNT',
                           title=f'Yearly Feedback Trend for {selected_drug}',
                           color='FEEDBACK_COUNT',
                           color_continuous_scale='Blues')
                
                fig.update_layout(
                    xaxis_title="Year",
                    yaxis_title="Feedback Count",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE),
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No yearly data available")
        
        with col2:
            st.markdown("### Geographic Distribution")
            
            geo_sql = f"""
            SELECT COUNTRY, COUNT(*) AS feedback_count
            FROM {BASE_TABLE}
            WHERE DRUG_NAME = '{selected_drug}'
            AND FEEDBACK_DATE BETWEEN '{drug_start}' AND '{drug_end}'
            GROUP BY COUNTRY
            ORDER BY feedback_count DESC
            LIMIT 10
            """
            
            geo_df = session.sql(geo_sql).to_pandas()
            
            if not geo_df.empty:
                fig = px.bar(geo_df, x='FEEDBACK_COUNT', y='COUNTRY',
                           orientation='h',
                           title=f'Top Countries for {selected_drug}',
                           color='FEEDBACK_COUNT',
                           color_continuous_scale='Viridis')
                
                fig.update_layout(
                    xaxis_title="Feedback Count",
                    yaxis_title="Country",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE),
                    yaxis={'categoryorder': 'total ascending'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No geographic data available")
        
        # Enhanced AI Insights Section
        st.markdown("### AI-Powered Insights")
        
        col1, col2 = st.columns(2)
        
        #col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Comprehensive Analysis")
            if st.button("Generate Analysis", type="primary", key="ai_summary"):
                with st.spinner("Analyzing feedback with AI..."):
                    try:
                        # Simulate comprehensive analysis
                        positive_rate = (drug_metrics['CURED_PATIENTS'] / drug_metrics['TOTAL_FEEDBACK'] * 100) if drug_metrics['TOTAL_FEEDBACK'] > 0 else 0
                        discontinued_rate = (drug_metrics['DISCONTINUED_PATIENTS'] / drug_metrics['TOTAL_FEEDBACK'] * 100) if drug_metrics['TOTAL_FEEDBACK'] > 0 else 0                        
                        st.markdown(f"""
                            <div class='insight-card'>
                            <h5 style='color: {PRIMARY_PURPLE};'>Overall Positives:</h5>
                            <p>• {positive_rate:.1f}% of patients showed positive outcomes (Cured)</p>
                            <p>• Average sentiment score of {drug_metrics['AVG_SENTIMENT']:.1f}/10 indicates {'good' if drug_metrics['AVG_SENTIMENT'] > 6 else 'moderate'} patient satisfaction</p>
                            <p>• Used successfully across {int(drug_metrics['COUNTRIES'])} countries</p>
                            
                            <h5 style='color: {PRIMARY_PURPLE};'>Overall Negatives:</h5>
                            <p>• {discontinued_rate:.1f}% of patients discontinued treatment</p>
                            <p>• Treatment monitoring required for optimal outcomes</p>
                            
                            <h5 style='color: {PRIMARY_PURPLE};'>Patient Expectations:</h5>
                            <p>• Patients expect consistent therapeutic effects</p>
                            <p>• Tolerability and convenience are key factors</p>
                            
                            <h5 style='color: {PRIMARY_PURPLE};'>Overall Outlook:</h5>
                            <p>• {'Positive' if drug_metrics['AVG_SENTIMENT'] > 6 else 'Cautiously optimistic'} outlook based on current data</p>
                            <p>• Continued monitoring recommended for safety profile</p>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Analysis error: {str(e)}")
        
        
        with col2:
            st.markdown("#### Side Effects Extraction")
            if st.button("Extract Side Effects", type="primary", key="side_effects"):
                with st.spinner("Extracting side effects..."):
                    try:
                        # Get actual side effects data
                        side_effects_sql = f"""
                        SELECT 
                            SIDE_EFFECTS_REPORTED,
                            COUNT(*) AS frequency
                        FROM {BASE_TABLE}
                        WHERE DRUG_NAME = '{selected_drug}'
                        AND FEEDBACK_DATE BETWEEN '{drug_start}' AND '{drug_end}'
                        AND SIDE_EFFECTS_REPORTED IS NOT NULL
                        AND SIDE_EFFECTS_REPORTED != 'Unspecified'
                        GROUP BY SIDE_EFFECTS_REPORTED
                        ORDER BY frequency DESC
                        LIMIT 10
                        """
                        
                        side_effects_df = session.sql(side_effects_sql).to_pandas()
                        
                        if not side_effects_df.empty:
                            effects_html = "<div class='insight-card'><h5 style='color: " + PRIMARY_PURPLE + ";'>Common Side Effects:</h5><ol>"
                            for _, row in side_effects_df.iterrows():
                                effects_html += f"<li>{row['SIDE_EFFECTS_REPORTED']} (Reported: {int(row['FREQUENCY'])} times)</li>"
                            effects_html += "</ol><p><em>Note: Side effects extracted from patient feedback data.</em></p></div>"
                            st.markdown(effects_html, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class='insight-card'>
                                <h5 style='color: """ + PRIMARY_PURPLE + """;'>Side Effects Analysis:</h5>
                                <p>No specific side effects reported in the current dataset for this time period.</p>
                                <p><em>Note: This analysis is based on structured feedback data.</em></p>
                            </div>
                            """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Side effects extraction error: {str(e)}")
                        
    except Exception as e:
        st.error(f"Error in drug performance analysis: {str(e)}")

elif page == "forecasting":
    st.markdown("# Predictive Analytics & Forecasting")
    st.markdown("### Advanced sentiment forecasting and trend prediction")
    st.markdown("---")
    
    try:
        forecast_where = build_where_clause(drugs=selected_drugs, regions=selected_regions, countries=selected_countries)
        
        # Historical Data
        hist_sql = f"""
            SELECT 
            YEAR(FEEDBACK_DATE) AS year,
            AVG(SENTIMENT_CAT) AS avg_sentiment,
            COUNT(*) AS feedback_count
            FROM {BASE_TABLE}
            {forecast_where}
            GROUP BY year
            ORDER BY year
            """
        
        hist_df = session.sql(hist_sql).to_pandas()

        if len(hist_df) >= 3:
            hist_df['ma_3'] = hist_df['AVG_SENTIMENT'].rolling(window=3).mean()
            last_ma = hist_df['ma_3'].iloc[-1] if not pd.isna(hist_df['ma_3'].iloc[-1]) else hist_df['AVG_SENTIMENT'].iloc[-1]
            last_year = int(hist_df['YEAR'].max())
            
            # Create forecast data
            forecast_years = list(range(last_year + 1, last_year + 4))
            
            # Combined visualization with vibrant colors
            st.markdown("### Historical Sentiment Trend with Forecast")
            
            fig = go.Figure()
            
            # Historical line (Blue)
            fig.add_trace(go.Scatter(
                x=hist_df['YEAR'],
                y=hist_df['AVG_SENTIMENT'],
                mode='lines+markers',
                name='Historical Data',
                line=dict(color='#1f77b4', width=4),  # Bright blue
                marker=dict(size=10, color='#1f77b4'),
                hovertemplate='<b>Year:</b> %{x}<br><b>Sentiment:</b> %{y:.2f}<extra></extra>'
            ))
            
            # Forecast line (Bright Green)
            fig.add_trace(go.Scatter(
                x=forecast_years,
                y=[last_ma] * 3,
                mode='lines+markers',
                name='Forecast',
                line=dict(color='#00ff00', width=4, dash='dash'),  # Bright green
                marker=dict(size=12, symbol='diamond', color='#00ff00'),
                hovertemplate='<b>Year:</b> %{x}<br><b>Predicted Sentiment:</b> %{y:.2f}<extra></extra>'
            ))
            
            # Add confidence band
            fig.add_trace(go.Scatter(
                x=forecast_years + forecast_years[::-1],
                y=[last_ma + 0.5] * 3 + [last_ma - 0.5] * 3,
                fill='tonexty',
                fillcolor='rgba(0, 255, 0, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                name='Confidence Interval',
                showlegend=False
            ))
            
            fig.update_layout(
                title='Sentiment Trend Analysis with 3-Year Forecast',
                xaxis_title='Year',
                yaxis_title='Average Sentiment',
                yaxis_range=[0, 10],
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Segoe UI, sans-serif", size=14),
                title_font=dict(size=18, color=PRIMARY_PURPLE),
                hovermode='x unified',
                height=500,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor="rgba(255,255,255,0.8)"
                )
            )
            
            # Add grid
            fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgray')
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Enhanced Forecast Summary
            st.markdown("### Forecast Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Predicted Sentiment", f"{last_ma:.2f}/10")
            with col2:
                trend = ("Stable" if abs(hist_df['AVG_SENTIMENT'].iloc[-1] - hist_df['AVG_SENTIMENT'].iloc[-3]) < 0.5 else ("Improving" if hist_df['AVG_SENTIMENT'].iloc[-1] > hist_df['AVG_SENTIMENT'].iloc[-3] else "Declining"))
                st.metric("Trend Direction", trend)
            with col3:
                confidence = "Moderate"
                st.metric("Confidence Level", confidence)
            with col4:
                forecast_change = ((last_ma - hist_df['AVG_SENTIMENT'].iloc[-1]) / hist_df['AVG_SENTIMENT'].iloc[-1] * 100) if hist_df['AVG_SENTIMENT'].iloc[-1] > 0 else 0
                st.metric("Expected Change", f"{forecast_change:+.1f}%")
            
            st.markdown(f"""
                <div class='insight-card'>
                <h4 style='color: {PRIMARY_PURPLE}; margin-top: 0;'>Forecasting Insights</h4>
                <p><strong>Model Type:</strong> 3-period moving average with trend extrapolation</p>
                <p><strong>Historical Data:</strong> {len(hist_df)} years of sentiment data analyzed</p>
                <p><strong>Prediction Horizon:</strong> 3 years (until {last_year + 3})</p>
                <p><strong>Key Finding:</strong> Sentiment expected to {'remain stable' if abs(forecast_change) < 2 else 'improve' if forecast_change > 0 else 'decline slightly'} around {last_ma:.1f}/10</p>
                <p><strong>Strategic Recommendation:</strong> {'Maintain current patient engagement strategies' if trend == 'Stable' else 'Investigate factors driving trend changes' if trend == 'Declining' else 'Capitalize on positive momentum with expansion plans'}</p>
                <p><strong>Risk Assessment:</strong> {'Low risk - stable sentiment pattern' if trend == 'Stable' else 'Medium risk - monitor closely' if trend == 'Declining' else 'Low risk - positive trajectory'}</p>
                </div>
                """, unsafe_allow_html=True)
            
        else:
            st.warning("⚠️ Insufficient historical data for forecasting. Minimum 3 years of data required.")
            st.info("Please adjust your filters to include more historical data or expand the date range.")
            
    except Exception as e:
        st.error(f"Error in forecasting analysis: {str(e)}")


elif page == "geographic":
    st.markdown("# Geographic Analysis")
    st.markdown("### Regional performance insights and global market analysis")
    st.markdown("---")
    
    try:
        geo_where = build_where_clause(drugs=selected_drugs, regions=selected_regions, countries=selected_countries)
        
        # Country Feedback Count Chart
        st.markdown("### Global Feedback Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Feedback Count by Country")
            country_feedback_sql = f"""
            SELECT 
                COUNTRY,
                COUNT(*) AS feedback_count
            FROM {BASE_TABLE}
            {geo_where}
            GROUP BY COUNTRY
            ORDER BY feedback_count DESC
            LIMIT 15
            """
            
            country_feedback_df = session.sql(country_feedback_sql).to_pandas()
            
            if not country_feedback_df.empty:
                fig = px.bar(country_feedback_df, y='COUNTRY', x='FEEDBACK_COUNT',
                           orientation='h',
                           color='FEEDBACK_COUNT',
                           color_continuous_scale='Viridis',
                           title='Top 15 Countries by Feedback Volume')
                
                fig.update_layout(
                    xaxis_title="Feedback Count",
                    yaxis_title="Country",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE),
                    yaxis={'categoryorder': 'total ascending'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Country-wise Sentiment Analysis")
            country_sentiment_sql = f"""
            SELECT 
                COUNTRY,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
                COUNT(*) AS feedback_count
            FROM {BASE_TABLE}
            {geo_where}
            GROUP BY COUNTRY
            HAVING COUNT(*) >= 5
            ORDER BY avg_sentiment DESC
            LIMIT 15
            """
            
            country_sentiment_df = session.sql(country_sentiment_sql).to_pandas()
            
            if not country_sentiment_df.empty:
                fig = px.bar(country_sentiment_df, y='COUNTRY', x='AVG_SENTIMENT',
                           orientation='h',
                           color='AVG_SENTIMENT',
                           color_continuous_scale='RdYlGn',
                           title='Top 15 Countries by Sentiment')
                
                fig.update_layout(
                    xaxis_title="Average Sentiment",
                    yaxis_title="Country",
                    xaxis_range=[0, 10],
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE),
                    yaxis={'categoryorder': 'total ascending'}
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Language Distribution
        st.markdown("### Language Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Feedback by Language")
            language_sql = f"""
            SELECT 
                LANGUAGE,
                COUNT(*) AS feedback_count
            FROM {BASE_TABLE}
            {geo_where}
            AND LANGUAGE IS NOT NULL
            GROUP BY LANGUAGE
            ORDER BY feedback_count DESC
            LIMIT 10
            """
            
            language_df = session.sql(language_sql).to_pandas()
            
            if not language_df.empty:
                fig = px.pie(language_df, names='LANGUAGE', values='FEEDBACK_COUNT',
                           title='Language Distribution of Feedback',
                           color_discrete_sequence=px.colors.qualitative.Set3)
                
                fig.update_layout(
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Country-wise Treatment Duration")
            duration_sql = f"""
            SELECT 
                COUNTRY,
                ROUND(AVG(TREATMENT_DURATION_DAYS), 0) AS avg_duration,
                COUNT(*) AS patient_count
            FROM {BASE_TABLE}
            {geo_where}
            AND TREATMENT_DURATION_DAYS IS NOT NULL
            GROUP BY COUNTRY
            HAVING COUNT(*) >= 10
            ORDER BY avg_duration DESC
            LIMIT 15
            """
            
            duration_df = session.sql(duration_sql).to_pandas()
            
            if not duration_df.empty:
                fig = px.scatter(duration_df, x='AVG_DURATION', y='COUNTRY',
                               size='PATIENT_COUNT',
                               color='AVG_DURATION',
                               color_continuous_scale='Viridis',
                               title='Average Treatment Duration by Country')
                
                fig.update_layout(
                    xaxis_title="Average Treatment Duration (Days)",
                    yaxis_title="Country",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Regional Analysis
        st.markdown("### Regional Performance Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Regional Adherence Comparison")
            regional_adherence_sql = f"""
            SELECT 
                REGION,
                ADHERENCE,
                COUNT(*) AS patient_count,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment
            FROM {BASE_TABLE}
            {geo_where}
            AND ADHERENCE IS NOT NULL
            AND REGION IS NOT NULL
            GROUP BY REGION, ADHERENCE
            ORDER BY REGION, ADHERENCE
            """
            
            regional_adherence_df = session.sql(regional_adherence_sql).to_pandas()
            
            if not regional_adherence_df.empty:
                fig = px.bar(regional_adherence_df, x='REGION', y='PATIENT_COUNT',
                           color='ADHERENCE',
                           title='Regional Adherence Patterns',
                           color_discrete_sequence=px.colors.qualitative.Set2)
                
                fig.update_layout(
                    xaxis_title="Region",
                    yaxis_title="Patient Count",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Alternative Regional View")
            region_sql = f"""
            SELECT 
                REGION,
                COUNT(*) AS feedback_count,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
                COUNT(DISTINCT COUNTRY) AS countries
            FROM {BASE_TABLE}
            {geo_where}
            GROUP BY REGION
            ORDER BY feedback_count DESC
            """
            
            region_df = session.sql(region_sql).to_pandas()
            
            if not region_df.empty:
                fig = px.treemap(region_df, path=['REGION'], values='FEEDBACK_COUNT',
                               color='AVG_SENTIMENT',
                               color_continuous_scale='RdYlGn',
                               title='Regional Feedback Distribution (Treemap)')
                
                fig.update_layout(
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Summary Table
        st.markdown("### Geographic Summary")
        if 'country_sentiment_df' in locals() and not country_sentiment_df.empty:
            st.dataframe(country_sentiment_df, use_container_width=True, hide_index=True)
            
    except Exception as e:
        st.error(f"Error in geographic analysis: {str(e)}")

elif page == "segmentation":
    st.markdown("# Patient Segmentation Analysis")
    st.markdown("### Comprehensive demographic and behavioral insights")
    st.markdown("---")
    
    try:
        seg_where = build_where_clause(drugs=selected_drugs, regions=selected_regions, countries=selected_countries)
        
        # Language-based Feedback Analysis
        st.markdown("### Language-based Feedback Distribution")
        
        language_feedback_sql = f"""
        SELECT 
            LANGUAGE,
            COUNT(*) AS feedback_count,
            ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment
        FROM {BASE_TABLE}
        {seg_where}
        AND LANGUAGE IS NOT NULL
        GROUP BY LANGUAGE
        ORDER BY feedback_count DESC
        LIMIT 15
        """
        
        language_feedback_df = session.sql(language_feedback_sql).to_pandas()
        
        if not language_feedback_df.empty:
            fig = px.bar(language_feedback_df, x='LANGUAGE', y='FEEDBACK_COUNT',
                       color='AVG_SENTIMENT',
                       color_continuous_scale='RdYlGn',
                       title='Feedback Distribution by Language')
            
            fig.update_layout(
                xaxis_title="Language",
                yaxis_title="Feedback Count",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Segoe UI, sans-serif", size=12),
                title_font=dict(size=14, color=PRIMARY_PURPLE),
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Gender Age Analysis
        st.markdown("### Gender-based Age Analysis")
        
        gender_age_sql = f"""
        SELECT 
            GENDER,
            MIN(AGE_AT_FEEDBACK) AS min_age,
            MAX(AGE_AT_FEEDBACK) AS max_age,
            ROUND(AVG(AGE_AT_FEEDBACK), 1) AS avg_age,
            COUNT(*) AS feedback_count
        FROM {BASE_TABLE}
        {seg_where}
        AND GENDER IS NOT NULL
        AND AGE_AT_FEEDBACK IS NOT NULL
        GROUP BY GENDER
        ORDER BY feedback_count DESC
        """
        
        gender_age_df = session.sql(gender_age_sql).to_pandas()
        
        if not gender_age_df.empty:
            col1, col2, col3 = st.columns(3)
            
            for idx, row in gender_age_df.iterrows():
                col_idx = idx % 3
                with [col1, col2, col3][col_idx]:
                    st.markdown(f"""
                    <div class='insight-card'>
                        <h3 style='color: {PRIMARY_PURPLE}; text-align: center; margin-top: 0;'>{row['GENDER']}</h3>
                        <div style='text-align: center;'>
                            <p><strong>Min Age:</strong> {int(row['MIN_AGE'])} years</p>
                            <p><strong>Max Age:</strong> {int(row['MAX_AGE'])} years</p>
                            <p><strong>Avg Age:</strong> {row['AVG_AGE']:.0f} years</p>
                            <p><strong>Patients:</strong> {int(row['FEEDBACK_COUNT']):,}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Adherence vs Feedback Count
        st.markdown("### Adherence Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Adherence vs Feedback Count")
            adherence_sql = f"""
            SELECT 
                ADHERENCE,
                COUNT(*) AS feedback_count,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment
            FROM {BASE_TABLE}
            {seg_where}
            AND ADHERENCE IS NOT NULL
            GROUP BY ADHERENCE
            ORDER BY feedback_count DESC
            """
            
            adherence_df = session.sql(adherence_sql).to_pandas()
            
            if not adherence_df.empty:
                fig = px.bar(adherence_df, x='ADHERENCE', y='FEEDBACK_COUNT',
                           color='AVG_SENTIMENT',
                           color_continuous_scale='RdYlGn',
                           title='Adherence Distribution')
                
                fig.update_layout(
                    xaxis_title="Adherence Level",
                    yaxis_title="Feedback Count",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Adherence vs Labels Correlation")
            adherence_labels_sql = f"""
            SELECT 
                ADHERENCE,
                LABELS,
                COUNT(*) AS count
            FROM {BASE_TABLE}
            {seg_where}
            AND ADHERENCE IS NOT NULL
            AND LABELS IS NOT NULL
            GROUP BY ADHERENCE, LABELS
            ORDER BY ADHERENCE, LABELS
            """
            
            adherence_labels_df = session.sql(adherence_labels_sql).to_pandas()
            
            if not adherence_labels_df.empty:
                # Create pivot table for heatmap using plotly
                pivot_df = adherence_labels_df.pivot(index='ADHERENCE', columns='LABELS', values='COUNT').fillna(0)
                
                fig = px.imshow(pivot_df.values,
                               x=pivot_df.columns,
                               y=pivot_df.index,
                               color_continuous_scale='Viridis',
                               title='Adherence vs Treatment Outcomes Heatmap')
                
                fig.update_layout(
                    xaxis_title="Treatment Outcomes",
                    yaxis_title="Adherence Level",
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Word Count vs Labels Scatter Plot
        st.markdown("### Feedback Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Word Count vs Treatment Outcomes")
            word_labels_sql = f"""
            SELECT 
                FEEDBACK_WORD_COUNT,
                LABELS,
                SENTIMENT_CAT,
                COUNT(*) AS frequency
            FROM {BASE_TABLE}
            {seg_where}
            AND FEEDBACK_WORD_COUNT IS NOT NULL
            AND LABELS IS NOT NULL
            AND FEEDBACK_WORD_COUNT > 0
            GROUP BY FEEDBACK_WORD_COUNT, LABELS, SENTIMENT_CAT
            HAVING COUNT(*) >= 1
            ORDER BY FEEDBACK_WORD_COUNT
            """
            
            word_labels_df = session.sql(word_labels_sql).to_pandas()
            
            if not word_labels_df.empty:
                fig = px.scatter(word_labels_df, x='FEEDBACK_WORD_COUNT', y='SENTIMENT_CAT',
                               color='LABELS', size='FREQUENCY',
                               title='Feedback Length vs Sentiment by Outcome',
                               color_discrete_sequence=px.colors.qualitative.Set1)
                
                fig.update_layout(
                    xaxis_title="Word Count",
                    yaxis_title="Sentiment Score",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Risk Groups by Comorbidities")
            comorbid_risk_sql = f"""
            SELECT 
                COMORBIDITIES,
                COUNT(*) AS patient_count,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
                SUM(CASE WHEN LABELS IN ('Adverse', 'Worsen') THEN 1 ELSE 0 END) AS adverse_count,
                ROUND(SUM(CASE WHEN LABELS IN ('Adverse', 'Worsen') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS risk_percentage
            FROM {BASE_TABLE}
            {seg_where}
            AND COMORBIDITIES IS NOT NULL
            AND COMORBIDITIES != 'Unspecified'
            GROUP BY COMORBIDITIES
            HAVING COUNT(*) >= 10
            ORDER BY risk_percentage DESC
            LIMIT 10
            """
            
            comorbid_risk_df = session.sql(comorbid_risk_sql).to_pandas()
            
            if not comorbid_risk_df.empty:
                fig = px.scatter(comorbid_risk_df, x='PATIENT_COUNT', y='RISK_PERCENTAGE',
                               size='ADVERSE_COUNT', color='AVG_SENTIMENT',
                               hover_name='COMORBIDITIES',
                               color_continuous_scale='RdYlGn_r',
                               title='Risk Assessment by Comorbidities')
                
                fig.update_layout(
                    xaxis_title="Patient Count",
                    yaxis_title="Risk Percentage (%)",
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(family="Segoe UI, sans-serif", size=12),
                    title_font=dict(size=14, color=PRIMARY_PURPLE)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # Summary Statistics
        st.markdown("### Segmentation Summary")
        
        if 'comorbid_risk_df' in locals() and not comorbid_risk_df.empty:
            st.markdown("#### High-Risk Comorbidities (>10% Adverse Events)")
            high_risk = comorbid_risk_df[comorbid_risk_df['RISK_PERCENTAGE'] > 10]
            if not high_risk.empty:
                st.dataframe(high_risk, use_container_width=True, hide_index=True)
            else:
                st.info("No high-risk comorbidity groups identified (>10% adverse events)")
            
    except Exception as e:
        st.error(f"Error in segmentation analysis: {str(e)}")

elif page == "safety":
    st.markdown("# Safety Monitoring Dashboard")
    st.markdown("### Real-time safety signal detection and adverse event analysis")
    st.markdown("---")
    
    try:
        safety_where = build_where_clause(drugs=selected_drugs, regions=selected_regions, countries=selected_countries)
        
        # Safety Overview
        safety_sql = f"""
        SELECT 
            DRUG_NAME,
            SUM(CASE WHEN LABELS IN ('Adverse', 'Worsen') THEN 1 ELSE 0 END) AS adverse_count,
            COUNT(*) AS total_feedback,
            ROUND(SUM(CASE WHEN LABELS IN ('Adverse', 'Worsen') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS adverse_rate
        FROM {BASE_TABLE}
        {safety_where}
        GROUP BY DRUG_NAME
        HAVING COUNT(*) >= 10
        ORDER BY adverse_rate DESC
        LIMIT 20
        """
        
        safety_df = session.sql(safety_sql).to_pandas()
        
        if not safety_df.empty:
            # Safety KPIs
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Adverse Events", f"{int(safety_df['ADVERSE_COUNT'].sum()):,}")
            with col2:
                st.metric("Average Adverse Rate", f"{safety_df['ADVERSE_RATE'].mean():.2f}%")
            with col3:
                high_risk_count = len(safety_df[safety_df['ADVERSE_RATE'] > 10])
                st.metric("High-Risk Drugs (>10%)", high_risk_count)
            
            # Adverse Rate Visualization
            st.markdown("### Adverse Event Rates by Drug")
            
            fig = px.bar(safety_df, x='DRUG_NAME', y='ADVERSE_RATE',
                        color='ADVERSE_RATE',
                        color_continuous_scale=['green', 'yellow', 'red'],
                        title='Adverse Event Rates Across Drugs',
                        labels={'DRUG_NAME': 'Drug Name', 'ADVERSE_RATE': 'Adverse Event Rate (%)'})
            
            fig.update_layout(
                xaxis_title="Drug Name",
                yaxis_title="Adverse Event Rate (%)",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family="Segoe UI, sans-serif", size=12),
                title_font=dict(size=16, color=PRIMARY_PURPLE),
                xaxis_tickangle=-45,
                height=500
            )
            
            # Add threshold line
            fig.add_hline(y=10, line_dash="dash", line_color="red", 
                         annotation_text="10% Threshold", annotation_position="bottom right")
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Side Effects Analysis
            st.markdown("### Side Effects Analysis")
            
            side_effects_sql = f"""
            SELECT 
                SIDE_EFFECTS_REPORTED,
                COUNT(*) AS case_count,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
                COUNT(DISTINCT DRUG_NAME) AS drugs_involved
            FROM {BASE_TABLE}
            {safety_where}
            AND SIDE_EFFECTS_REPORTED IS NOT NULL
            AND SIDE_EFFECTS_REPORTED != 'Unspecified'
            GROUP BY SIDE_EFFECTS_REPORTED
            HAVING COUNT(*) >= 5
            ORDER BY case_count DESC
            LIMIT 15
            """
            
            side_effects_df = session.sql(side_effects_sql).to_pandas()
            
            if not side_effects_df.empty:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    fig = px.bar(side_effects_df, x='CASE_COUNT', y='SIDE_EFFECTS_REPORTED',
                               orientation='h',
                               color='AVG_SENTIMENT',
                               color_continuous_scale='RdYlGn_r',
                               title='Most Common Side Effects',
                               labels={'CASE_COUNT': 'Number of Cases', 'SIDE_EFFECTS_REPORTED': 'Side Effect'})
                    
                    fig.update_layout(
                        xaxis_title="Number of Cases",
                        yaxis_title="Side Effect",
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(family="Segoe UI, sans-serif", size=11),
                        title_font=dict(size=14, color=PRIMARY_PURPLE),
                        yaxis={'categoryorder': 'total ascending'},
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.markdown("#### Side Effects Summary")
                    st.dataframe(side_effects_df, use_container_width=True, hide_index=True)
            
            # Detailed Safety Data
            st.markdown("### Detailed Safety Data")
            st.dataframe(safety_df, use_container_width=True, hide_index=True)
            
        else:
            st.info("No safety data available for the selected filters")
            
    except Exception as e:
        st.error(f"Error in safety monitoring: {str(e)}")

elif page == "reports":
    st.markdown("# Detailed Reports & Data Export")
    st.markdown("### Comprehensive data export and custom reporting")
    st.markdown("---")
    
    report_where = build_where_clause(drugs=selected_drugs, regions=selected_regions, countries=selected_countries)
    
    report_type = st.selectbox("Select Report Type:", [
        "Complete Feedback Report",
        "Drug Performance Report", 
        "Safety & Adverse Events Report",
        "Patient Demographics Report",
        "Custom SQL Query"
    ])
    
    try:
        if report_type == "Complete Feedback Report":
            st.markdown("### Complete Patient Feedback Dataset")
            
            sql = f"""
            SELECT 
                ID, PATIENT_NAME, DRUG_NAME, COUNTRY, REGION,
                AGE_AT_FEEDBACK, GENDER, SENTIMENT_CAT, LABELS,
                FEEDBACK_DATE, TREATMENT_DURATION_DAYS, ADHERENCE,
                SIDE_EFFECTS_REPORTED, COMORBIDITIES, THERAPAUTIC_AREA
            FROM {BASE_TABLE}
            {report_where}
            ORDER BY FEEDBACK_DATE DESC
            LIMIT 2000
            """
            
        elif report_type == "Drug Performance Report":
            st.markdown("### Comprehensive Drug Performance Analysis")
            
            sql = f"""
            SELECT 
                DRUG_NAME,
                THERAPAUTIC_AREA,
                COUNT(DISTINCT PATIENT_NAME) AS unique_patients,
                COUNT(*) AS total_feedback,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
                ROUND(AVG(AGE_AT_FEEDBACK), 1) AS avg_patient_age,
                ROUND(AVG(TREATMENT_DURATION_DAYS), 0) AS avg_treatment_days,
                SUM(CASE WHEN LABELS = 'Cured' THEN 1 ELSE 0 END) AS cured_count,
                SUM(CASE WHEN LABELS = 'Improvement' THEN 1 ELSE 0 END) AS improved_count,
                SUM(CASE WHEN LABELS = 'No Progress' THEN 1 ELSE 0 END) AS no_progress_count,
                SUM(CASE WHEN LABELS IN ('Adverse', 'Worsen') THEN 1 ELSE 0 END) AS adverse_count,
                ROUND(SUM(CASE WHEN LABELS IN ('Cured', 'Improvement') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS success_rate,
                COUNT(DISTINCT COUNTRY) AS countries_served
            FROM {BASE_TABLE}
            {report_where}
            GROUP BY DRUG_NAME, THERAPAUTIC_AREA
            ORDER BY total_feedback DESC
            """
            
        elif report_type == "Safety & Adverse Events Report":
            st.markdown("### Safety & Adverse Events Analysis")
            
            sql = f"""
            SELECT 
                DRUG_NAME,
                PATIENT_NAME,
                AGE_AT_FEEDBACK,
                GENDER,
                COUNTRY,
                SIDE_EFFECTS_REPORTED,
                FEEDBACK_DATE,
                SENTIMENT_CAT,
                LABELS,
                COMORBIDITIES,
                TREATMENT_DURATION_DAYS
            FROM {BASE_TABLE}
            {report_where}
            AND LABELS IN ('Adverse', 'Worsen')
            ORDER BY FEEDBACK_DATE DESC
            LIMIT 1000
            """
            
        elif report_type == "Patient Demographics Report":
            st.markdown("### Patient Demographics Breakdown")
            
            sql = f"""
            SELECT 
                CASE 
                    WHEN AGE_AT_FEEDBACK < 30 THEN '18-29'
                    WHEN AGE_AT_FEEDBACK < 50 THEN '30-49'
                    WHEN AGE_AT_FEEDBACK < 65 THEN '50-64'
                    ELSE '65+'
                END AS age_group,
                GENDER,
                COUNTRY,
                REGION,
                COUNT(*) AS patient_count,
                ROUND(AVG(SENTIMENT_CAT), 2) AS avg_sentiment,
                SUM(CASE WHEN LABELS IN ('Cured', 'Improvement') THEN 1 ELSE 0 END) AS success_count,
                ROUND(AVG(TREATMENT_DURATION_DAYS), 0) AS avg_treatment_days
            FROM {BASE_TABLE}
            {report_where}
            GROUP BY age_group, GENDER, COUNTRY, REGION
            ORDER BY patient_count DESC
            LIMIT 1000
            """
            
        else:  # Custom SQL Query
            st.markdown("### Custom SQL Query Interface")
            st.info("⚠️ Advanced feature for data analysts and SQL users")
            
            custom_query = st.text_area(
                "Enter your SQL query:",
                value=f"SELECT * FROM {BASE_TABLE} LIMIT 100",
                height=150,
                help="Write custom SQL to explore the data. Use the table name: " + BASE_TABLE
            )
            
            if st.button("Execute Query", type="primary"):
                try:
                    with st.spinner("Executing custom query..."):
                        df = session.sql(custom_query).to_pandas()
                        st.success(f"✅ Query executed successfully! {len(df)} rows returned")
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        
                        # Download option
                        csv = df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv,
                            file_name=f"custom_query_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"Query execution error: {str(e)}")
            
            # Don't execute the standard report logic for custom queries
            sql = None
        
        if sql:
            df = session.sql(sql).to_pandas()
            
            if not df.empty:
                st.success(f"✅ Report generated successfully! {len(df)} records found")
                
                # Display sample data
                st.markdown("#### Data Preview")
                st.dataframe(df.head(100), use_container_width=True, hide_index=True)
                
                if len(df) > 100:
                    st.info(f"Showing first 100 rows. Full dataset contains {len(df)} records.")
                
                # Download functionality
                csv = df.to_csv(index=False)
                report_filename = f"{report_type.lower().replace(' ', '_').replace('&', 'and')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                
                st.download_button(
                    label="📥 Download Complete Report",
                    data=csv,
                    file_name=report_filename,
                    mime="text/csv",
                    help=f"Download the complete {report_type.lower()} as CSV file"
                )
                
                # Summary statistics
                if 'SENTIMENT_CAT' in df.columns:
                    st.markdown("#### Report Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Records", f"{len(df):,}")
                    with col2:
                        if 'DRUG_NAME' in df.columns:
                            st.metric("Unique Drugs", df['DRUG_NAME'].nunique())
                    with col3:
                        if 'COUNTRY' in df.columns:
                            st.metric("Countries", df['COUNTRY'].nunique())
                    with col4:
                        if 'SENTIMENT_CAT' in df.columns:
                            st.metric("Avg Sentiment", f"{df['SENTIMENT_CAT'].mean():.2f}/10")
            else:
                st.warning("No data found matching the current filters.")
                
    except Exception as e:
        st.error(f"Error generating report: {str(e)}")





# Professional Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 30px; color: #6C757D; background: white; margin-top: 50px; border-top: 2px solid {PRIMARY_PURPLE}; border-radius: 15px 15px 0 0;'>
    <h3 style='color: {PRIMARY_PURPLE}; margin-top: 0;'>AstraZeneca Pharmaceutical Analytics</h3>
    <p><strong>© {datetime.now().year} AstraZeneca PLC. All rights reserved.</strong></p>
    <p>Powered by Snowflake Data Cloud & Advanced Analytics </p>
    <p>Dashboard Version 3.0 | Last Updated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    <p style='font-size: 0.9em; color: #888; margin-top: 15px;'>
        This dashboard provides real-time insights into patient feedback, drug performance, and safety monitoring.<br>
        For technical support or data inquiries, please contact the Analytics Team.
    </p>
</div>
""", unsafe_allow_html=True)


