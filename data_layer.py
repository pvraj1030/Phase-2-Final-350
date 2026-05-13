import json
import os
from pathlib import Path
from datetime import datetime

# Data directory
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

USERS_FILE = DATA_DIR / "users.json"
APPOINTMENTS_FILE = DATA_DIR / "appointments.json"
AVAILABLE_SLOTS_FILE = DATA_DIR / "available_slots.json"


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

    appointments = [
        apt for apt in appointments
        if apt.get("id") != appointment_id
    ]

    save_appointments(appointments)


def get_appointments_by_doctor(doctor_email):
    """Get all appointments for a doctor"""
    appointments = load_appointments()

    return [
        apt for apt in appointments
        if apt.get("doctor_email") == doctor_email
    ]


def get_appointments_by_patient(patient_email):
    """Get all appointments for a patient"""
    appointments = load_appointments()

    return [
        apt for apt in appointments
        if apt.get("patient_email") == patient_email
    ]


def load_available_slots():
    """Load available time slots from JSON file"""
    if AVAILABLE_SLOTS_FILE.exists():
        with open(AVAILABLE_SLOTS_FILE, "r") as f:
            return json.load(f)

    return []


def save_available_slots(slots):
    """Save available time slots to JSON file"""
    with open(AVAILABLE_SLOTS_FILE, "w") as f:
        json.dump(slots, f, indent=2)


def add_available_slot(slot):
    """Add a new available time slot"""
    slots = load_available_slots()
    slots.append(slot)
    save_available_slots(slots)


def delete_available_slot(slot_id):
    """Delete an available time slot"""
    slots = load_available_slots()

    slots = [
        slot for slot in slots
        if slot.get("id") != slot_id
    ]

    save_available_slots(slots)


def get_available_slots(doctor_email, date):
    """
    Get available time slots for a doctor
    on a given date that haven't been booked
    """
    slots = load_available_slots()
    available = []

    for slot in slots:
        if (
            slot.get("doctor_email") == doctor_email
            and slot.get("date") == date
            and slot.get("is_available") is True
        ):
            available.append(slot)

    return available


def book_available_slot(slot_id, patient_email):
    """Mark an available slot as booked"""
    slots = load_available_slots()

    for slot in slots:
        if slot.get("id") == slot_id:
            slot["is_available"] = False
            slot["booked_by"] = patient_email
            slot["booked_at"] = str(datetime.now())
            break

    save_available_slots(slots)


def get_all_available_slots_by_doctor(doctor_email):
    """Get all available slots for a doctor"""
    slots = load_available_slots()

    return [
        slot for slot in slots
        if slot.get("doctor_email") == doctor_email
    ]


def get_analytics_data(doctor_email):
    """Get analytics data for a doctor"""
    appointments = get_appointments_by_doctor(doctor_email)

    total_appointments = len(appointments)

    scheduled = len([
        a for a in appointments
        if a.get("status") == "Scheduled"
    ])

    completed = len([
        a for a in appointments
        if a.get("status") == "Completed"
    ])

    cancelled = len([
        a for a in appointments
        if a.get("status") == "Cancelled"
    ])

    no_show = len([
        a for a in appointments
        if a.get("status") == "No-Show"
    ])

    cancellation_rate = (
        (cancelled / total_appointments) * 100
        if total_appointments > 0 else 0
    )

    no_show_rate = (
        (no_show / total_appointments) * 100
        if total_appointments > 0 else 0
    )

    completion_rate = (
        (completed / total_appointments) * 100
        if total_appointments > 0 else 0
    )

    return {
        "total_appointments": total_appointments,
        "scheduled": scheduled,
        "completed": completed,
        "cancelled": cancelled,
        "no_show": no_show,
        "cancellation_rate": round(cancellation_rate, 2),
        "no_show_rate": round(no_show_rate, 2),
        "completion_rate": round(completion_rate, 2)
    }