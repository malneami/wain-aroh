"""
Recommendation and Doctor Communication Models
"""
from datetime import datetime
import json

class Recommendation:
    """Model for AI recommendations"""
    
    def __init__(self, id=None, conversation_id=None, recommendation_type=None, 
                 title=None, description=None, priority=None, is_urgent=False,
                 requires_doctor_approval=False, action_type=None, action_data=None,
                 status='pending', created_at=None):
        self.id = id
        self.conversation_id = conversation_id
        self.recommendation_type = recommendation_type  # 'emergency', 'clinic', 'self_care', 'medication'
        self.title = title
        self.description = description
        self.priority = priority  # 'high', 'medium', 'low'
        self.is_urgent = is_urgent
        self.requires_doctor_approval = requires_doctor_approval
        self.action_type = action_type  # 'contact_doctor', 'book_clinic', 'self_care', 'call_emergency'
        self.action_data = action_data  # JSON data for the action
        self.status = status  # 'pending', 'approved', 'rejected', 'completed'
        self.created_at = created_at or datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'conversation_id': self.conversation_id,
            'recommendation_type': self.recommendation_type,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'is_urgent': self.is_urgent,
            'requires_doctor_approval': self.requires_doctor_approval,
            'action_type': self.action_type,
            'action_data': self.action_data,
            'status': self.status,
            'created_at': self.created_at
        }

class DoctorCommunication:
    """Model for doctor-patient communication requests"""
    
    def __init__(self, id=None, patient_id=None, conversation_id=None, 
                 recommendation_id=None, urgency_level=None, symptoms=None,
                 doctor_id=None, status='pending', doctor_response=None,
                 created_at=None, responded_at=None):
        self.id = id
        self.patient_id = patient_id
        self.conversation_id = conversation_id
        self.recommendation_id = recommendation_id
        self.urgency_level = urgency_level  # 'critical', 'urgent', 'normal'
        self.symptoms = symptoms
        self.doctor_id = doctor_id
        self.status = status  # 'pending', 'approved', 'rejected', 'completed'
        self.doctor_response = doctor_response
        self.created_at = created_at or datetime.now().isoformat()
        self.responded_at = responded_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'conversation_id': self.conversation_id,
            'recommendation_id': self.recommendation_id,
            'urgency_level': self.urgency_level,
            'symptoms': self.symptoms,
            'doctor_id': self.doctor_id,
            'status': self.status,
            'doctor_response': self.doctor_response,
            'created_at': self.created_at,
            'responded_at': self.responded_at
        }

class ClinicAppointmentRequest:
    """Model for clinic appointment requests"""
    
    def __init__(self, id=None, patient_id=None, conversation_id=None,
                 recommendation_id=None, clinic_type=None, symptoms_summary=None,
                 preferred_date=None, preferred_time=None, specialist_id=None,
                 status='pending', specialist_notes=None, appointment_details=None,
                 created_at=None, reviewed_at=None, auto_response_sent=False):
        self.id = id
        self.patient_id = patient_id
        self.conversation_id = conversation_id
        self.recommendation_id = recommendation_id
        self.clinic_type = clinic_type  # 'general', 'cardiology', 'neurology', etc.
        self.symptoms_summary = symptoms_summary
        self.preferred_date = preferred_date
        self.preferred_time = preferred_time
        self.specialist_id = specialist_id
        self.status = status  # 'pending', 'approved', 'scheduled', 'rejected'
        self.specialist_notes = specialist_notes
        self.appointment_details = appointment_details  # JSON with date, time, location
        self.created_at = created_at or datetime.now().isoformat()
        self.reviewed_at = reviewed_at
        self.auto_response_sent = auto_response_sent
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'conversation_id': self.conversation_id,
            'recommendation_id': self.recommendation_id,
            'clinic_type': self.clinic_type,
            'symptoms_summary': self.symptoms_summary,
            'preferred_date': self.preferred_date,
            'preferred_time': self.preferred_time,
            'specialist_id': self.specialist_id,
            'status': self.status,
            'specialist_notes': self.specialist_notes,
            'appointment_details': self.appointment_details,
            'created_at': self.created_at,
            'reviewed_at': self.reviewed_at,
            'auto_response_sent': self.auto_response_sent
        }

# In-memory storage (replace with database in production)
recommendations_db = []
doctor_communications_db = []
clinic_appointments_db = []

def save_recommendation(recommendation):
    """Save a recommendation to the database"""
    if not recommendation.id:
        recommendation.id = len(recommendations_db) + 1
    recommendations_db.append(recommendation)
    return recommendation

def save_doctor_communication(communication):
    """Save a doctor communication request"""
    if not communication.id:
        communication.id = len(doctor_communications_db) + 1
    doctor_communications_db.append(communication)
    return communication

def save_clinic_appointment(appointment):
    """Save a clinic appointment request"""
    if not appointment.id:
        appointment.id = len(clinic_appointments_db) + 1
    clinic_appointments_db.append(appointment)
    return appointment

def get_recommendations_by_conversation(conversation_id):
    """Get all recommendations for a conversation"""
    return [r for r in recommendations_db if r.conversation_id == conversation_id]

def get_pending_doctor_communications():
    """Get all pending doctor communication requests"""
    return [c for c in doctor_communications_db if c.status == 'pending']

def get_pending_clinic_appointments():
    """Get all pending clinic appointment requests"""
    return [a for a in clinic_appointments_db if a.status == 'pending']

def update_doctor_communication_status(comm_id, status, doctor_response=None):
    """Update doctor communication status"""
    for comm in doctor_communications_db:
        if comm.id == comm_id:
            comm.status = status
            if doctor_response:
                comm.doctor_response = doctor_response
            comm.responded_at = datetime.now().isoformat()
            return comm
    return None

def update_clinic_appointment_status(appt_id, status, specialist_notes=None, appointment_details=None):
    """Update clinic appointment status"""
    for appt in clinic_appointments_db:
        if appt.id == appt_id:
            appt.status = status
            if specialist_notes:
                appt.specialist_notes = specialist_notes
            if appointment_details:
                appt.appointment_details = appointment_details
            appt.reviewed_at = datetime.now().isoformat()
            return appt
    return None

