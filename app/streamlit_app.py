#!/usr/bin/env python3
"""
CryptoPrism Database Monitoring Dashboard
Streamlit application for real-time monitoring and analytics
"""

import streamlit as st
import os
import sys
from datetime import datetime

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.settings import config
from utils.helpers import check_authentication_status, login_user, logout_user

# Page Configuration
st.set_page_config(
    page_title="CryptoPrism Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "CryptoPrism Database Analytics Platform v1.2.0"
    }
)

# Enhanced CSS Styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #1f77b4, #ff4b4b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }

    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #ff4b4b;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        margin-bottom: 1rem;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }

    .status-success {
        color: #28a745;
        font-weight: bold;
    }

    .status-failed {
        color: #dc3545;
        font-weight: bold;
    }

    .status-running {
        color: #ffc107;
        font-weight: bold;
    }

    .viz-container {
        background: white;
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }

    div[data-testid="stMetricValue"] > div {
        color: #ff6b6b !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)


# Authentication
def check_authentication():
    """Authentication handler using utility functions."""
    if config.auth_config['enabled']:
        if not check_authentication_status():
            st.markdown('<div class="main-header">🔒 CryptoPrism Dashboard Login</div>', unsafe_allow_html=True)
            password = st.text_input("Enter dashboard password:", type="password")
            if st.button("Login"):
                if login_user(password):
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid password. Please try again.")
            st.stop()


# Main Application
def main():
    """Main Streamlit application with lazy page loading."""

    # Check authentication
    check_authentication()

    # Sidebar Navigation
    page_options = {
        "🏠 HOME Overview": "overview",
        "🔄 MONITOR Pipeline": "pipeline_monitor",
        "✅ QA Checks": "qa_checks",
        "⚡ PERFORMANCE Analytics": "performance",
        "📊 TABLES FE Monitor": "business_signals",
        "📜 LOGS & Artifacts": "logs"
    }

    selected_page = st.sidebar.radio("📍 Navigation", list(page_options.keys()))

    # Auto-refresh toggle
    auto_refresh_enabled = config.ui_config['auto_refresh']
    auto_refresh_interval = config.ui_config['refresh_interval']

    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ Settings")

    auto_refresh = st.sidebar.checkbox(
        f"🔄 Auto-refresh ({auto_refresh_interval}s)",
        value=auto_refresh_enabled
    )

    if auto_refresh:
        import time
        time.sleep(auto_refresh_interval)
        st.rerun()

    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Data", type="primary"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.success("✅ Cache cleared!")
        st.rerun()

    # Logout button
    if st.sidebar.button("🚪 Logout"):
        logout_user()
        st.rerun()

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Dashboard Info")
    st.sidebar.markdown(f"**Version:** {os.getenv('DASHBOARD_VERSION', 'v1.2.0')}")
    st.sidebar.markdown(f"**Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.sidebar.markdown("**Status:** 🟢 Online")

    # Lazy load and run selected page (dramatically improves performance)
    page_module = page_options[selected_page]

    if page_module == "overview":
        from pages.overview import render_overview_page
        render_overview_page()
    elif page_module == "pipeline_monitor":
        from pages.pipeline_monitor import render_pipeline_monitor_page
        render_pipeline_monitor_page()
    elif page_module == "qa_checks":
        from pages.qa_checks import render_qa_checks_page
        render_qa_checks_page()
    elif page_module == "performance":
        from pages.performance import render_performance_page
        render_performance_page()
    elif page_module == "business_signals":
        from pages.business_signals import render_business_signals_page
        render_business_signals_page()
    elif page_module == "logs":
        from pages.logs import render_logs_page
        render_logs_page()


if __name__ == "__main__":
    main()
