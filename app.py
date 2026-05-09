import streamlit as st
from datetime import datetime, timedelta
import json
import os
from ui_layer import (
    render_login_page,
    render_doctor_dashboard,
    render_patient_dashboard,
    render_registration_page,
    render_navbar
)
from data_layer import (
    load_users,
    save_users,
    load_appointments,
    save_appointments
)
from service_layer import (
    authenticate_user,
    register_user,
    validate_email,
    validate_password,
    get_user_role,
    is_user_logged_in,
    logout_user
)

# Page configuration
st.set_page_config(
    page_title="Patient Appointment Tracker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_role = None

# Sidebar
st.sidebar.title("🏥 Patient Appointment Tracker")

if st.session_state.logged_in:
    st.sidebar.success(f"Logged in as: {st.session_state.user_role}")
    st.sidebar.write(f"📧 {st.session_state.user_email}")

    st.sidebar.markdown("---")
    st.sidebar.subheader("Navigation")

    if st.session_state.user_role == "Doctor":
        st.sidebar.info("👨‍⚕️ Doctor Dashboard")
        st.sidebar.write("• Manage Schedule")
        st.sidebar.write("• View Appointments")
        st.sidebar.write("• AI Assistant")

    elif st.session_state.user_role == "Patient":
        st.sidebar.info("👤 Patient Dashboard")
        st.sidebar.write("• Book Appointment")
        st.sidebar.write("• My Appointments")
        st.sidebar.write("• Pre-Visit AI Chat")

    st.sidebar.markdown("---")

    if st.sidebar.button("🚪 Logout"):
        logout_user()
        st.rerun()

else:
    st.sidebar.info("Please log in to continue.")

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        padding-top: 0rem;
    }

    .header-title {
        color: #1f77b4;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }

    .role-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 0.5rem;
        font-weight: bold;
        margin-left: 1rem;
    }

    .doctor-badge {
        background-color: #d4edda;
        color: #155724;
    }

    .patient-badge {
        background-color: #cfe2ff;
        color: #084298;
    }

    .stButton > button {
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }

    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application flow"""

    # Check if user is logged in
    if not st.session_state.logged_in:

        # Show login/registration page
        st.markdown(
            '<div class="header-title">🏥 Patient Appointment Tracker</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        # Tabs for login and registration
        login_tab, register_tab, test_info_tab = st.tabs(
            ["🔐 Login", "📝 Register", "🧪 Test Accounts"]
        )

        with login_tab:
            render_login_page()

        with register_tab:
            render_registration_page()

        with test_info_tab:
            st.success("### Test Accounts for Demo")

            col1, col2 = st.columns(2)

            with col1:
                st.info("""
                **👨‍⚕️ Doctor/Admin Account**

                Email: `doctor@clinic.com`

                Password: `doctor123`
                """)

            with col2:
                st.info("""
                **👤 Patient Account**

                Email: `patient@test.com`

                Password: `patient123`
                """)

    else:
        # User is logged in - show dashboard
        render_navbar()

        if st.session_state.user_role == "Doctor":
            render_doctor_dashboard()

        elif st.session_state.user_role == "Patient":
            render_patient_dashboard()

if __name__ == "__main__":
    main()