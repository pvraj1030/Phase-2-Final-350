import streamlit as st
from datetime import datetime, timedelta
from service_layer import authenticate_user, register_user, User, Appointment, validate_email, validate_password, hash_password, logout_user
from data_layer import load_appointments, save_appointments, get_appointments_by_doctor, get_appointments_by_patient, get_available_slots, update_appointment, delete_appointment, add_appointment
from ai_assistant import AIChatAssistant
import json
import uuid

def render_login_page():
    """Render the login page"""
    st.subheader("🔐 Login to Your Account")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button", use_container_width=True):
            if email and password:
                success, role, message = authenticate_user(email, password)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.user_role = role
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)
            else:
                st.error("Please enter both email and password.")
    
    with col2:
        st.info("""
        **Demo Credentials:**
        
        Doctor:
        - doctor@clinic.com
        - doctor123
        
        Patient:
        - patient@test.com
        - patient123
        """)

def render_registration_page():
    """Render the registration page"""
    st.subheader("📝 Create a New Account")
    
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    role = st.selectbox("Select Role", ["Patient", "Doctor"], key="register_role")
    
    if st.button("Register", use_container_width=True):
        if email and password and confirm_password:
            if password != confirm_password:
                st.error("Passwords do not match.")
            else:
                success, message = register_user(email, password, role)
                if success:
                    st.success(message)
                else:
                    st.error(message)
        else:
            st.error("Please fill in all fields.")


def apply_role_theme():
    if st.session_state.get("user_role") == "Doctor":
        primary_color = "#1a6b8a"
    else:
        primary_color = "#2e7d4f"

    st.markdown(f"""
        <style>
            /* Buttons */
            .stButton > button,
            div.stButton > button,
            button[kind="primary"],
            button[kind="secondary"] {{
                background-color: {primary_color} !important;
                color: white !important;
                border: none !important;
                border-radius: 8px !important;
            }}
            .stButton > button:hover,
            div.stButton > button:hover {{
                opacity: 0.85 !important;
                background-color: {primary_color} !important;
            }}

            /* Active tab underline */
            .stTabs [data-baseweb="tab-highlight"] {{
                background-color: {primary_color} !important;
            }}
            .stTabs [aria-selected="true"] {{
                color: {primary_color} !important;
            }}

            /* Sidebar active item */
            [data-testid="stSidebarNav"] a[aria-selected="true"] {{
                color: {primary_color} !important;
            }}

            /* Top border accent */
            [data-testid="stAppViewContainer"] > section:first-child {{
                border-top: 4px solid {primary_color} !important;
            }}

            /* Links */
            a {{
                color: {primary_color} !important;
            }}
        </style>
    """, unsafe_allow_html=True)

def render_navbar():
    apply_role_theme()   # ← add this one line
    """Render navigation bar and logout button"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### 🏥 Patient Appointment Tracker")
    
    with col2:
        role_badge = "👨‍⚕️ Doctor" if st.session_state.user_role == "Doctor" else "👤 Patient"
        st.markdown(f"**{role_badge}**")
    
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            logout_user()
            st.success("Logged out successfully!")
            st.rerun()
    
    st.divider()

def render_doctor_dashboard():
    """Render doctor dashboard"""
    st.subheader("👨‍⚕️ Doctor Dashboard")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["📅 Manage Schedule", "📋 Appointments", "💬 AI Assistant", "Settings"])
    
    with tab1:
        st.write("### Create Available Time Slots")
        
        col1, col2 = st.columns(2)
        with col1:
            slot_date = st.date_input("Select Date", min_value=datetime.now().date())
        
        with col2:
            slot_time = st.time_input("Select Time")
        
        if st.button("Add Available Slot", use_container_width=True, key="add_slot"):
            # Create a placeholder appointment for availability
            appointment = Appointment(
                str(uuid.uuid4()),
                st.session_state.user_email,
                "AVAILABLE",
                slot_date.strftime("%Y-%m-%d"),
                slot_time.strftime("%H:%M"),
                "Available Slot",
                "Available"
            )
            add_appointment(appointment.to_dict())
            st.success("✅ Time slot created!")
            st.rerun()
    
    with tab2:
        st.write("### Your Appointments")
        
        appointments = get_appointments_by_doctor(st.session_state.user_email)
        appointments = [apt for apt in appointments if apt.get("status") != "Available"]
        
        if appointments:
            for apt in appointments:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Patient:** {apt.get('patient_email')}")
                        st.write(f"**Date:** {apt.get('date')} at {apt.get('time')}")
                        st.write(f"**Reason:** {apt.get('reason')}")
                        if apt.get('ai_notes'):
                            st.info(f"**AI Notes:** {apt.get('ai_notes')}")
                    
                    with col2:
                        status = st.selectbox(
                            "Status",
                            ["Scheduled", "Completed", "No-Show", "Cancelled"],
                            index=["Scheduled", "Completed", "No-Show", "Cancelled"].index(apt.get("status", "Scheduled")),
                            key=f"status_{apt.get('id')}"
                        )
                        if status != apt.get("status"):
                            update_appointment(apt.get("id"), {"status": status})
                            st.success("Updated!")
                            st.rerun()
                    
                    with col3:
                        if st.button("Delete", key=f"delete_{apt.get('id')}"):
                            delete_appointment(apt.get("id"))
                            st.success("Deleted!")
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("No appointments yet.")
    
    with tab3:
        st.write("### Clinic Assistant AI")
        render_ai_assistant()
    
    with tab4:
        st.write("### Settings")
        st.write(f"**Email:** {st.session_state.user_email}")
        st.write(f"**Role:** {st.session_state.user_role}")

def render_patient_dashboard():
    """Render patient dashboard"""
    st.subheader("👤 Patient Dashboard")
    
    tab1, tab2, tab3 = st.tabs(["📅 Book Appointment", "📋 My Appointments", "💬 Pre-Visit Chat"])
    
    with tab1:
        st.write("### Book an Appointment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            appointment_date = st.date_input("Select Date", min_value=datetime.now().date(), key="book_date")
        
        with col2:
            # Get available doctors (simplified - in real app would load from users)
            doctors = ["doctor@clinic.com"]
            selected_doctor = st.selectbox("Select Doctor", doctors, key="book_doctor")
        
        # Get available slots
        available_slots = get_available_slots(selected_doctor, appointment_date.strftime("%Y-%m-%d"))
        
        if available_slots:
            selected_time = st.selectbox("Select Time", available_slots, key="book_time")
            reason = st.text_area("Reason for Visit", key="book_reason")
            
            if st.button("Book Appointment", use_container_width=True, key="book_btn"):
                if reason:
                    appointment = Appointment(
                        str(uuid.uuid4()),
                        selected_doctor,
                        st.session_state.user_email,
                        appointment_date.strftime("%Y-%m-%d"),
                        selected_time,
                        reason,
                        "Scheduled"
                    )
                    add_appointment(appointment.to_dict())
                    st.success("✅ Appointment booked successfully!")
                    st.rerun()
                else:
                    st.error("Please enter a reason for your visit.")
        else:
            st.warning("No available slots on this date. Please select another date.")
    
    with tab2:
        st.write("### Your Appointments")
        
        appointments = get_appointments_by_patient(st.session_state.user_email)
        
        if appointments:
            for apt in appointments:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Doctor:** {apt.get('doctor_email')}")
                        st.write(f"**Date:** {apt.get('date')} at {apt.get('time')}")
                        st.write(f"**Reason:** {apt.get('reason')}")
                        
                        # Status badge
                        status = apt.get("status", "Scheduled")
                        if status == "Scheduled":
                            st.info(f"Status: {status}")
                        elif status == "Completed":
                            st.success(f"Status: {status}")
                        elif status == "Cancelled":
                            st.error(f"Status: {status}")
                        else:
                            st.warning(f"Status: {status}")
                    
                    with col2:
                        if apt.get("status") == "Scheduled":
                            if st.button("Cancel", key=f"cancel_{apt.get('id')}"):
                                update_appointment(apt.get("id"), {"status": "Cancelled"})
                                st.success("Appointment cancelled!")
                                st.rerun()
                    
                    st.divider()
        else:
            st.info("You have no appointments yet.")
    
    with tab3:
        st.write("### Pre-Visit Chat with AI")
        render_patient_ai_chat()

def render_ai_assistant():
    """Render general AI assistant"""
    assistant = AIChatAssistant()
    
    st.write("Ask me about clinic operations, patient care, or scheduling!")
    
    user_question = st.text_input("Your question:", key="doctor_ai_input")
    
    if user_question and st.button("Ask", key="doctor_ai_button"):
        with st.spinner("Thinking..."):
            response = assistant.get_response(user_question)
            st.success(response)

def render_patient_ai_chat():
    """Render patient AI chat for pre-visit preparation"""
    if "patient_chat_history" not in st.session_state:
        st.session_state.patient_chat_history = []
    
    st.write("Describe your symptoms and concerns. This information will be prepared for your doctor.")
    
    # Display chat history
    for message in st.session_state.patient_chat_history:
        if message["role"] == "user":
            st.write(f"**You:** {message['content']}")
        else:
            st.write(f"**Assistant:** {message['content']}")
    
    user_input = st.text_input("Tell me about your symptoms:", key="patient_ai_input")
    
    if user_input and st.button("Send", key="patient_ai_button"):
        # Add user message to history
        st.session_state.patient_chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        assistant = AIChatAssistant()
        response = assistant.get_medical_response(user_input)
        st.session_state.patient_chat_history.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    # Option to save notes for doctor
    if st.session_state.patient_chat_history:
        if st.button("Save Chat Summary for Doctor"):
            # This would be attached to the appointment
            summary = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in st.session_state.patient_chat_history])
            st.success("Summary saved! Your doctor will review this before your appointment.")