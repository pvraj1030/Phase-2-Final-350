# Patient Appointment Tracker 🏥

A multi-role web application for managing patient appointments at a medical clinic.

## Features

### Phase 1 MVP
- ✅ User authentication (registration, login, logout)
- ✅ Session state management
- ✅ Two distinct roles (Doctor/Admin and Patient)
- ✅ JSON-based data storage
- ✅ Complete CRUD functionality
- ✅ Multi-page responsive design

### Phase 2 Enhancements
- ✅ OOP refactoring with classes and methods
- ✅ Layered architecture (UI, Data, Service layers)
- ✅ Improved design and layout
- ✅ OpenAI AI Assistant integration
- ✅ Pre-visit chat for symptom description
- ✅ Test accounts with sample data
- ✅ Professional dashboard interface

## Project Structure

```
MISY350 FINAL PROJECT/
├── app.py                          # Main application file
├── ui_layer.py                     # UI/presentation logic
├── data_layer.py                   # JSON data persistence
├── service_layer.py                # Business logic & classes
├── ai_assistant.py                 # OpenAI integration
├── requirements.txt                # Python dependencies
├── README.md                       # Documentation
├── .gitignore                      # Git configuration
└── data/
    ├── users.json                  # User accounts storage
    └── appointments.json           # Appointments storage
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/misy350-final-project-app.git
cd misy350-final-project-app
```

2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up OpenAI API (optional, for full AI features)
```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Running the Application

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Test Accounts

### Doctor Account
- Email: `doctor@clinic.com`
- Password: `doctor123`

### Patient Account
- Email: `patient@test.com`
- Password: `patient123`

## Features by Role

### Doctor/Admin Dashboard
- 📅 Create and manage available time slots
- 📋 View daily patient roster
- 📊 Update appointment statuses (Scheduled, Completed, No-Show)
- 💬 AI Clinic Assistant
- 🗑️ Delete canceled appointments

### Patient Dashboard
- 📅 View doctor's available time slots
- 📋 Book new appointments
- 📝 Reschedule or cancel existing appointments
- 💬 Pre-visit AI chat to describe symptoms
- ✅ Confirm appointments

## Architecture

### UI Layer (ui_layer.py)
- Handles all Streamlit interface rendering
- Manages page navigation
- Displays data with proper formatting

### Data Layer (data_layer.py)
- Reads/writes JSON files
- Manages data persistence
- Database operations (CRUD)

### Service Layer (service_layer.py)
- User authentication and validation
- Business logic
- User and Appointment classes
- Role-based permissions

### AI Assistant (ai_assistant.py)
- OpenAI API integration
- Hardcoded fallback responses
- General clinic questions
- Medical symptom assistance

## CRUD Functionality

### Create
- Register new users
- Create available time slots
- Book appointments

### Read
- View user appointments
- Display available slots
- Show appointment details

### Update
- Change appointment status
- Reschedule appointments

### Delete
- Cancel appointments
- Remove time slots

## AI Features

### Hardcoded Responses (5 categories)
1. **Clinic Hours** - Operating hours and holidays
2. **Appointments** - How to book and manage
3. **Cancellation** - Cancellation policies
4. **Payment** - Payment methods accepted
5. **Insurance** - Insurance coverage

### OpenAI Integration
- General clinic assistant
- Medical symptom analysis
- Pre-visit preparation
- Professional note generation

## Contributing

This is a final project for MISY 350.

## License

MIT License