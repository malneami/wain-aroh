"""
Database models for medical specialties and performance metrics
"""
from datetime import datetime
import json

# In-memory storage (replace with database in production)
specialties = []
facility_specialties = []
performance_metrics = []
appointments = []

specialty_id_counter = 1
facility_specialty_id_counter = 1
metric_id_counter = 1
appointment_id_counter = 1

class MedicalSpecialty:
    """Medical specialty/department"""
    def __init__(self, name_ar, name_en, category, description_ar=None, description_en=None, icon=None):
        global specialty_id_counter
        self.id = specialty_id_counter
        specialty_id_counter += 1
        self.name_ar = name_ar
        self.name_en = name_en
        self.category = category  # clinic, center, department
        self.description_ar = description_ar
        self.description_en = description_en
        self.icon = icon
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'category': self.category,
            'description_ar': self.description_ar,
            'description_en': self.description_en,
            'icon': self.icon,
            'created_at': self.created_at
        }

class FacilitySpecialty:
    """Link between facility and specialty with specific details"""
    def __init__(self, facility_id, specialty_id, doctors_count=0, available_slots=0, 
                 average_wait_time=None, accepts_insurance=True, contact_phone=None,
                 working_hours=None, booking_available=True):
        global facility_specialty_id_counter
        self.id = facility_specialty_id_counter
        facility_specialty_id_counter += 1
        self.facility_id = facility_id
        self.specialty_id = specialty_id
        self.doctors_count = doctors_count
        self.available_slots = available_slots
        self.average_wait_time = average_wait_time  # in minutes
        self.accepts_insurance = accepts_insurance
        self.contact_phone = contact_phone
        self.working_hours = working_hours  # JSON string
        self.booking_available = booking_available
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'facility_id': self.facility_id,
            'specialty_id': self.specialty_id,
            'doctors_count': self.doctors_count,
            'available_slots': self.available_slots,
            'average_wait_time': self.average_wait_time,
            'accepts_insurance': self.accepts_insurance,
            'contact_phone': self.contact_phone,
            'working_hours': json.loads(self.working_hours) if self.working_hours else None,
            'booking_available': self.booking_available,
            'created_at': self.created_at
        }

class PerformanceMetric:
    """Performance metrics for facilities and specialties"""
    def __init__(self, facility_id, specialty_id=None, metric_type=None, value=None, 
                 month=None, year=None):
        global metric_id_counter
        self.id = metric_id_counter
        metric_id_counter += 1
        self.facility_id = facility_id
        self.specialty_id = specialty_id
        self.metric_type = metric_type  # patient_satisfaction, success_rate, wait_time, etc.
        self.value = value
        self.month = month
        self.year = year
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'facility_id': self.facility_id,
            'specialty_id': self.specialty_id,
            'metric_type': self.metric_type,
            'value': self.value,
            'month': self.month,
            'year': self.year,
            'created_at': self.created_at
        }

class Appointment:
    """Appointment booking"""
    def __init__(self, patient_id, facility_id, specialty_id, doctor_name=None,
                 appointment_date=None, appointment_time=None, status='pending',
                 notes=None, contact_phone=None):
        global appointment_id_counter
        self.id = appointment_id_counter
        appointment_id_counter += 1
        self.patient_id = patient_id
        self.facility_id = facility_id
        self.specialty_id = specialty_id
        self.doctor_name = doctor_name
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status  # pending, confirmed, cancelled, completed
        self.notes = notes
        self.contact_phone = contact_phone
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
    
    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'facility_id': self.facility_id,
            'specialty_id': self.specialty_id,
            'doctor_name': self.doctor_name,
            'appointment_date': self.appointment_date,
            'appointment_time': self.appointment_time,
            'status': self.status,
            'notes': self.notes,
            'contact_phone': self.contact_phone,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

# CRUD operations
def save_specialty(specialty):
    specialties.append(specialty)
    return specialty

def save_facility_specialty(facility_specialty):
    facility_specialties.append(facility_specialty)
    return facility_specialty

def save_performance_metric(metric):
    performance_metrics.append(metric)
    return metric

def save_appointment(appointment):
    appointments.append(appointment)
    return appointment

def get_all_specialties():
    return specialties

def get_specialty_by_id(specialty_id):
    return next((s for s in specialties if s.id == specialty_id), None)

def get_facilities_by_specialty(specialty_id):
    return [fs for fs in facility_specialties if fs.specialty_id == specialty_id]

def get_specialties_by_facility(facility_id):
    return [fs for fs in facility_specialties if fs.facility_id == facility_id]

def get_performance_metrics(facility_id, specialty_id=None):
    metrics = [m for m in performance_metrics if m.facility_id == facility_id]
    if specialty_id:
        metrics = [m for m in metrics if m.specialty_id == specialty_id]
    return metrics

def get_appointments_by_patient(patient_id):
    return [a for a in appointments if a.patient_id == patient_id]

def get_appointments_by_facility(facility_id):
    return [a for a in appointments if a.facility_id == facility_id]

def update_appointment_status(appointment_id, status):
    appointment = next((a for a in appointments if a.id == appointment_id), None)
    if appointment:
        appointment.status = status
        appointment.updated_at = datetime.now().isoformat()
    return appointment

