import openai
import os
import streamlit as st

class AIChatAssistant:
    """AI Chat Assistant using OpenAI API"""
    
    def __init__(self):
        """Initialize the AI assistant"""
        # Note: In production, store API key in environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            openai.api_key = self.api_key
    
    def get_response(self, question):
        """Get response from OpenAI for general questions"""
        try:
            if not self.api_key:
                return self._get_hardcoded_response(question)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful clinic assistant. Answer questions about clinic operations, appointments, and general healthcare."},
                    {"role": "user", "content": question}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return self._get_hardcoded_response(question)
    
    def get_medical_response(self, symptoms):
        """Get response for medical/symptom questions"""
        try:
            if not self.api_key:
                return self._get_hardcoded_medical_response(symptoms)
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medical assistant AI. Help patients describe their symptoms clearly and professionally for their doctor. Ask clarifying questions if needed. Keep responses concise and professional."},
                    {"role": "user", "content": symptoms}
                ],
                max_tokens=250,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return self._get_hardcoded_medical_response(symptoms)
    
    def _get_hardcoded_response(self, question):
        """Fallback hardcoded responses"""
        question_lower = question.lower()
        
        responses = {
            "hours": "Our clinic operates Monday to Friday, 9 AM to 5 PM. We are closed on weekends and public holidays.",
            "appointment": "You can book appointments through our portal. Select your doctor, preferred date and time, and provide the reason for your visit.",
            "cancel": "To cancel an appointment, go to 'My Appointments' and click the Cancel button. You must cancel at least 24 hours in advance.",
            "payment": "We accept cash, credit cards, and insurance. Please contact our reception for payment options.",
            "insurance": "Yes, we accept most major insurance plans. Please verify your coverage with our reception team.",
        }
        
        for key, value in responses.items():
            if key in question_lower:
                return value
        
        return "I'm sorry, I don't have information about that. Please contact our reception team at (555) 123-4567."
    
    def _get_hardcoded_medical_response(self, symptoms):
        """Fallback hardcoded medical responses"""
        symptoms_lower = symptoms.lower()
        
        responses = {
            "pain": "Please describe where the pain is located and when it started. Is it constant or intermittent? This information will help your doctor.",
            "fever": "If you have a fever, please take your temperature and note it. Also let us know for how long you've had it.",
            "cough": "How long have you had this cough? Is it dry or productive (with phlegm)? Any other symptoms?",
            "headache": "Describe your headache - is it sharp, dull, throbbing? Where exactly do you feel it? When did it start?",
            "cold": "Common cold symptoms include congestion, cough, and sore throat. Your doctor will check you over.",
        }
        
        for key, value in responses.items():
            if key in symptoms_lower:
                return value
        
        return "Thank you for sharing this information. Your doctor will review these notes before your appointment and may have follow-up questions."