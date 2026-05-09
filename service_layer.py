import re
import hashlib
from datetime import datetime
from data_layer import load_users, user_exists, add_user, get_user_by_email
import streamlit as st

class User:
    """User class representing a user in the system"""
    def __init__(self, email, role):
        self.email = email
        self.role = role
    
    def can_access_page(self, page):
        """Check if user can access a page based on role"""
        if self.role == "Doctor":
            return page in ["doctor_dashboard", "view_slots", "manage_appointments"]
        elif self.role == "Patient":
            return page in ["patient_dashboard", "book_appointment", "my_appointments"]
        return False
    
    def is_doctor(self):
        return self.role == "Doctor"
    
    def is_patient(self):
        return self.role == "Patient"

class Appointment:
    """Appointment class representing an appointment"""
    def __init__(self, appointment_id, doctor_email, patient_email, date, time, reason, status="Scheduled"):
        self.id = appointment_id
        self.doctor_email = doctor_email
        self.patient_email = patient_email
        self.date = date
        self.time = time
        self.reason = reason
        self.status = status
        self.ai_notes = ""
    
    def to_dict(self):
        return {
            "id": self.id,
            "doctor_email": self.doctor_email,
            "patient_email": self.patient_email,
            "date": self.date,
            "time": self.time,
            "reason": self.reason,
            "status": self.status,
            "ai_notes": self.ai_notes,
            "created_at": str(datetime.now())
        }
    
    def update_status(self, new_status):
        """Update appointment status"""
        self.status = new_status

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""

def hash_password(password):
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email, password, role):
    """Register a new user"""
    # Validate email
    if not validate_email(email):
        return False, "Invalid email format."
    
    # Check if user already exists
    if user_exists(email):
        return False, "User already exists. Please log in."
    
    # Validate password
    valid, msg = validate_password(password)
    if not valid:
        return False, msg
    
    # Hash password and add user
    password_hash = hash_password(password)
    add_user(email, password_hash, role)
    return True, "Registration successful! Please log in."

def authenticate_user(email, password):
    """Authenticate a user"""
    if not validate_email(email):
        return False, None, "Invalid email format."
    
    user = get_user_by_email(email)
    if not user:
        return False, None, "User not found."
    
    password_hash = hash_password(password)
    if user.get("password") == password_hash:
        return True, user.get("role"), "Login successful!"
    else:
        return False, None, "Invalid password."

def get_user_role(email):
    """Get user role"""
    user = get_user_by_email(email)
    if user:
        return user.get("role")
    return None

def is_user_logged_in():
    """Check if user is logged in"""
    return st.session_state.get("logged_in", False)

def logout_user():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.user_email = None
    st.session_state.user_role = None