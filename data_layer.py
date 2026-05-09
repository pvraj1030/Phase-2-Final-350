import json
import os
from pathlib import Path
from datetime import datetime

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"
APPOINTMENTS_FILE = DATA_DIR / "appointments.json"

def load_users():
    """Load users from JSON file"""
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def load_appointments():
    """Load appointments from JSON file"""
    if APPOINTMENTS_FILE.exists():
        with open(APPOINTMENTS_FILE, "r") as f:
            return json.load(f)
    return []

def save_appointments(appointments):
    """Save appointments to JSON file"""
    with open(APPOINTMENTS_FILE, "w") as f:
        json.dump(appointments, f, indent=2)

def get_user_by_email(email):
    """Get a user by email"""
    users = load_users()
    return users.get(email)

def user_exists(email):
    """Check if user exists"""
    return email in load_users()

def add_user(email, password_hash, role):
    """Add a new user"""
    users = load_users()
    users[email] = {
        "email": email,
        "password": password_hash,
        "role": role,
        "created_at": str(datetime.now())
    }
    save_users(users)

def get_appointment_by_id(appointment_id):
    """Get appointment by ID"""
    appointments = load_appointments()
    for apt in appointments:
        if apt.get("id") == appointment_id:
            return apt
    return None

def add_appointment(appointment):
    """Add a new appointment"""
    appointments = load_appointments()
    appointments.append(appointment)
    save_appointments(appointments)

def update_appointment(appointment_id, updated_data):
    """Update an appointment"""
    appointments = load_appointments()
    for i, apt in enumerate(appointments):
        if apt.get("id") == appointment_id:
            appointments[i].update(updated_data)
            save_appointments(appointments)
            return True
    return False

def delete_appointment(appointment_id):
    """Delete an appointment"""
    appointments = load_appointments()
    appointments = [apt for apt in appointments if apt.get("id") != appointment_id]
    save_appointments(appointments)

def get_appointments_by_doctor(doctor_email):
    """Get all appointments for a doctor"""
    appointments = load_appointments()
    return [apt for apt in appointments if apt.get("doctor_email") == doctor_email]

def get_appointments_by_patient(patient_email):
    """Get all appointments for a patient"""
    appointments = load_appointments()
    return [apt for apt in appointments if apt.get("patient_email") == patient_email]

def get_available_slots(doctor_email, date):
    """Get available time slots for a doctor on a given date"""
    appointments = get_appointments_by_doctor(doctor_email)
    booked_times = set()
    
    for apt in appointments:
        if apt.get("date") == date and apt.get("status") != "Cancelled":
            booked_times.add(apt.get("time"))
    
    # Define available time slots (9 AM to 5 PM, 30-min intervals)
    all_slots = []
    for hour in range(9, 17):
        for minute in [0, 30]:
            time_str = f"{hour:02d}:{minute:02d}"
            if time_str not in booked_times:
                all_slots.append(time_str)
    
    return all_slots