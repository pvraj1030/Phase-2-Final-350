import streamlit as st
from datetime import datetime
import uuid
import pandas as pd

from service_layer import (
    authenticate_user,
    register_user,
    Appointment,
    logout_user
)

from data_layer import (
    get_appointments_by_doctor,
    get_appointments_by_patient,
    get_available_slots,
    update_appointment,
    delete_appointment,
    add_appointment,
    add_available_slot,
    delete_available_slot,
    get_all_available_slots_by_doctor,
    get_analytics_data,
    book_available_slot
)

from ai_assistant import AIChatAssistant


# LOGIN PAGE

def render_login_page():
    """Render login page"""

    st.subheader("🔐 Login to Your Account")

    col1, col2 = st.columns(2)

    with col1:
        email = st.text_input("Email", key="login_email")

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            use_container_width=True,
            key="login_btn"
        ):

            if email and password:

                success, role, message = authenticate_user(
                    email,
                    password
                )

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
        Demo Accounts

        Doctor
        - doctor@clinic.com
        - doctor123

        Patient
        - patient@test.com
        - patient123
        """)


# =========================
# REGISTRATION PAGE
# =========================
def render_registration_page():
    """Render registration page"""

    st.subheader("📝 Create Account")

    email = st.text_input("Email", key="register_email")

    password = st.text_input(
        "Password",
        type="password",
        key="register_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="confirm_password"
    )

    role = st.selectbox(
        "Select Role",
        ["Patient", "Doctor"],
        key="register_role"
    )

    if st.button(
        "Register",
        use_container_width=True
    ):

        if email and password and confirm_password:

            if password != confirm_password:
                st.error("Passwords do not match.")

            else:
                success, message = register_user(
                    email,
                    password,
                    role
                )

                if success:
                    st.success(message)

                else:
                    st.error(message)

        else:
            st.error("Please fill in all fields.")


# NAVBAR

def render_navbar():
    """Render top navbar"""

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        st.markdown("### 🏥 Patient Appointment Tracker")

    with col2:
        role_badge = (
            "👨‍⚕️ Doctor"
            if st.session_state.user_role == "Doctor"
            else "👤 Patient"
        )

        st.markdown(f"**{role_badge}**")

    with col3:
        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):
            logout_user()
            st.success("Logged out successfully!")
            st.rerun()

    st.divider()


# DOCTOR DASHBOARD

def render_doctor_dashboard():
    """Render doctor dashboard"""

    st.subheader("👨‍⚕️ Doctor Dashboard")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Analytics",
        "📅 Manage Schedule",
        "📋 Appointments",
        "💬 AI Assistant",
        "⚙️ Settings"
    ])

    # ANALYTICS TAB
   
    with tab1:

        analytics = get_analytics_data(
            st.session_state.user_email
        )

        st.write("### 📊 Analytics Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total",
                analytics["total_appointments"]
            )

        with col2:
            st.metric(
                "Scheduled",
                analytics["scheduled"]
            )

        with col3:
            st.metric(
                "Completed",
                analytics["completed"]
            )

        with col4:
            st.metric(
                "Cancelled",
                analytics["cancelled"]
            )

        st.divider()

        breakdown_data = {
            "Scheduled": analytics["scheduled"],
            "Completed": analytics["completed"],
            "Cancelled": analytics["cancelled"],
            "No-Show": analytics["no_show"]
        }

        df = pd.DataFrame(
            list(breakdown_data.items()),
            columns=["Status", "Count"]
        )

        st.bar_chart(df.set_index("Status"))


    # MANAGE SCHEDULE TAB
    
    with tab2:

        st.write("### Create Available Time Slot")

        col1, col2, col3 = st.columns(3)

        with col1:
            slot_date = st.date_input(
                "Date",
                min_value=datetime.now().date()
            )

        with col2:
            slot_time = st.time_input("Time")

        with col3:
            duration = st.selectbox(
                "Duration",
                [15, 30, 45, 60]
            )

        if st.button(
            "Add Available Slot",
            key="add_slot_btn",
            use_container_width=True
        ):

            slot = {
                "id": str(uuid.uuid4()),
                "doctor_email": st.session_state.user_email,
                "date": slot_date.strftime("%Y-%m-%d"),
                "time": slot_time.strftime("%H:%M"),
                "duration": duration,
                "is_available": True,
                "created_at": str(datetime.now())
            }

            add_available_slot(slot)

            st.success("Time slot added!")
            st.rerun()

        st.divider()

        st.write("### Your Available Slots")

        slots = get_all_available_slots_by_doctor(
            st.session_state.user_email
        )

        if slots:

            for slot in slots:

                col1, col2 = st.columns([4, 1])

                with col1:

                    status = (
                        "Available"
                        if slot.get("is_available")
                        else "Booked"
                    )

                    st.write(
                        f"📅 {slot['date']} at "
                        f"{slot['time']} "
                        f"({slot['duration']} mins) "
                        f"- {status}"
                    )

                with col2:

                    if slot.get("is_available"):

                        if st.button(
                            "Remove",
                            key=f"remove_{slot['id']}"
                        ):
                            delete_available_slot(slot["id"])
                            st.success("Removed!")
                            st.rerun()

        else:
            st.info("No available slots yet.")

    
    # APPOINTMENTS TAB
    
    with tab3:

        st.write("### Your Appointments")

        appointments = get_appointments_by_doctor(
            st.session_state.user_email
        )

        if appointments:

            for apt in appointments:

                with st.container():

                    col1, col2, col3 = st.columns([2, 1, 1])

                    with col1:

                        st.write(
                            f"**Patient:** "
                            f"{apt.get('patient_email')}"
                        )

                        st.write(
                            f"**Date:** "
                            f"{apt.get('date')} "
                            f"at {apt.get('time')}"
                        )

                        st.write(
                            f"**Reason:** "
                            f"{apt.get('reason')}"
                        )

                    with col2:

                        status = st.selectbox(
                            "Status",
                            [
                                "Scheduled",
                                "Completed",
                                "No-Show",
                                "Cancelled"
                            ],
                            index=[
                                "Scheduled",
                                "Completed",
                                "No-Show",
                                "Cancelled"
                            ].index(
                                apt.get(
                                    "status",
                                    "Scheduled"
                                )
                            ),
                            key=f"status_{apt['id']}"
                        )

                        if status != apt.get("status"):

                            update_appointment(
                                apt["id"],
                                {"status": status}
                            )

                            st.success("Updated!")
                            st.rerun()

                    with col3:

                        if st.button(
                            "Delete",
                            key=f"delete_{apt['id']}"
                        ):
                            delete_appointment(apt["id"])
                            st.success("Deleted!")
                            st.rerun()

                    st.divider()

        else:
            st.info("No appointments yet.")

   
    # AI TAB
    
    with tab4:

        st.write("### AI Assistant")

        render_ai_assistant()

    # =========================
    # SETTINGS TAB
    # =========================
    with tab5:

        st.write("### Account Settings")

        st.write(
            f"**Email:** "
            f"{st.session_state.user_email}"
        )

        st.write(
            f"**Role:** "
            f"{st.session_state.user_role}"
        )



# PATIENT DASHBOARD

def render_patient_dashboard():
    """Render patient dashboard"""

    st.subheader("👤 Patient Dashboard")

    tab1, tab2, tab3 = st.tabs([
        "📅 Book Appointment",
        "📋 My Appointments",
        "💬 AI Chat"
    ])

    
    # BOOK APPOINTMENT
    
    with tab1:

        st.write("### Book Appointment")

        col1, col2 = st.columns(2)

        with col1:

            doctors = ["doctor@clinic.com"]

            selected_doctor = st.selectbox(
                "Select Doctor",
                doctors
            )

        with col2:

            appointment_date = st.date_input(
                "Appointment Date",
                min_value=datetime.now().date()
            )

        available_slots = get_available_slots(
            selected_doctor,
            appointment_date.strftime("%Y-%m-%d")
        )

        if available_slots:

            slot_options = [
                f"{slot['time']} "
                f"({slot['duration']} mins)"
                for slot in available_slots
            ]

            selected_index = st.selectbox(
                "Select Time Slot",
                range(len(slot_options)),
                format_func=lambda x: slot_options[x]
            )

            reason = st.text_area(
                "Reason for Visit"
            )

            if st.button(
                "Book Appointment",
                use_container_width=True
            ):

                if reason:

                    selected_slot = available_slots[
                        selected_index
                    ]

                    appointment = Appointment(
                        str(uuid.uuid4()),
                        selected_doctor,
                        st.session_state.user_email,
                        appointment_date.strftime("%Y-%m-%d"),
                        selected_slot["time"],
                        reason,
                        "Scheduled"
                    )

                    add_appointment(
                        appointment.to_dict()
                    )

                    book_available_slot(
                        selected_slot["id"],
                        st.session_state.user_email
                    )

                    st.success(
                        "Appointment booked!"
                    )

                    st.balloons()
                    st.rerun()

                else:
                    st.error(
                        "Please enter a reason."
                    )

        else:
            st.warning(
                "No available slots found."
            )

    
    # MY APPOINTMENTS
    
    with tab2:

        appointments = get_appointments_by_patient(
            st.session_state.user_email
        )

        if appointments:

            for apt in appointments:

                with st.container():

                    st.write(
                        f"**Doctor:** "
                        f"{apt.get('doctor_email')}"
                    )

                    st.write(
                        f"**Date:** "
                        f"{apt.get('date')} "
                        f"at {apt.get('time')}"
                    )

                    st.write(
                        f"**Reason:** "
                        f"{apt.get('reason')}"
                    )

                    st.info(
                        f"Status: "
                        f"{apt.get('status')}"
                    )

                    if (
                        apt.get("status")
                        == "Scheduled"
                    ):

                        if st.button(
                            "Cancel Appointment",
                            key=f"cancel_{apt['id']}"
                        ):

                            update_appointment(
                                apt["id"],
                                {
                                    "status":
                                    "Cancelled"
                                }
                            )

                            st.success(
                                "Appointment cancelled!"
                            )

                            st.rerun()

                    st.divider()

        else:
            st.info("No appointments found.")

    
    # AI CHAT TAB
    
    with tab3:

        render_patient_ai_chat()



# AI ASSISTANT

def render_ai_assistant():
    """Doctor AI assistant"""

    assistant = AIChatAssistant()

    st.write(
        "Ask questions about scheduling, "
        "clinic workflow, or patient care."
    )

    user_question = st.text_input(
        "Ask a question:",
        key="doctor_ai_input"
    )

    if (
        user_question
        and st.button(
            "Ask AI",
            key="doctor_ai_button"
        )
    ):

        with st.spinner("Thinking..."):

            response = assistant.get_response(
                user_question
            )

            st.success(response)



# PATIENT AI CHAT

def render_patient_ai_chat():
    """Patient AI pre-visit chat"""

    if "patient_chat_history" not in st.session_state:
        st.session_state.patient_chat_history = []

    st.write(
        "Describe your symptoms "
        "before your visit."
    )

    for message in st.session_state.patient_chat_history:

        if message["role"] == "user":
            st.write(
                f"**You:** "
                f"{message['content']}"
            )

        else:
            st.write(
                f"**Assistant:** "
                f"{message['content']}"
            )

    user_input = st.text_input(
        "Tell me about your symptoms:",
        key="patient_ai_input"
    )

    if (
        user_input
        and st.button(
            "Send",
            key="patient_ai_button"
        )
    ):

        st.session_state.patient_chat_history.append({
            "role": "user",
            "content": user_input
        })

        assistant = AIChatAssistant()

        response = assistant.get_medical_response(
            user_input
        )

        st.session_state.patient_chat_history.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()

    if st.session_state.patient_chat_history:

        if st.button(
            "Save Summary For Doctor"
        ):

            st.success(
                "Chat summary saved!"
            )