"""
Service Schedule and On-Call Coverage Models
Manages hospital services, schedules, and real-time availability
"""

from datetime import datetime, time
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Time, Date, ForeignKey, Text, JSON, Float
from sqlalchemy.orm import relationship
from .user import db

class ServiceType(str, Enum):
    """Types of hospital services"""
    EMERGENCY = "emergency"
    CARDIOLOGY = "cardiology"
    NEUROLOGY = "neurology"
    ORTHOPEDICS = "orthopedics"
    PEDIATRICS = "pediatrics"
    OBSTETRICS = "obstetrics"
    SURGERY = "surgery"
    ICU = "icu"
    NICU = "nicu"
    RADIOLOGY = "radiology"
    LABORATORY = "laboratory"
    PHARMACY = "pharmacy"
    DIALYSIS = "dialysis"
    ONCOLOGY = "oncology"
    PSYCHIATRY = "psychiatry"
    DERMATOLOGY = "dermatology"
    OPHTHALMOLOGY = "ophthalmology"
    ENT = "ent"
    DENTAL = "dental"
    PHYSIOTHERAPY = "physiotherapy"

class ScheduleType(str, Enum):
    """Types of schedules"""
    REGULAR = "regular"  # Regular weekly schedule
    ON_CALL = "on_call"  # On-call coverage
    TEMPORARY = "temporary"  # Temporary override
    HOLIDAY = "holiday"  # Holiday schedule

class AvailabilityStatus(str, Enum):
    """Service availability status"""
    AVAILABLE = "available"
    LIMITED = "limited"  # Limited capacity
    UNAVAILABLE = "unavailable"
    ON_CALL_ONLY = "on_call_only"

class HospitalService(db.Model):
    """Hospital services configuration"""
    __tablename__ = 'service_configurations'
    
    id = Column(Integer, primary_key=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=False)
    service_type = Column(String(50), nullable=False)  # ServiceType enum
    service_name_ar = Column(String(200), nullable=False)
    service_name_en = Column(String(200), nullable=False)
    description_ar = Column(Text)
    description_en = Column(Text)
    
    # Service details
    is_active = Column(Boolean, default=True)
    requires_appointment = Column(Boolean, default=False)
    has_on_call_coverage = Column(Boolean, default=False)
    capacity = Column(Integer)  # Max patients/day or beds
    average_wait_time = Column(Integer)  # Minutes
    
    # Contact
    phone = Column(String(20))
    extension = Column(String(10))
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    hospital = relationship("Hospital", backref="service_configs")
    schedules = relationship("ServiceSchedule", back_populates="service", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<HospitalService {self.service_name_en} at Hospital {self.hospital_id}>"

class ServiceSchedule(db.Model):
    """Service schedules and on-call coverage"""
    __tablename__ = 'service_schedules'
    
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service_configurations.id'), nullable=False)
    schedule_type = Column(String(20), nullable=False)  # ScheduleType enum
    
    # Time-based schedule
    day_of_week = Column(Integer)  # 0=Monday, 6=Sunday, null=all days
    start_time = Column(Time)
    end_time = Column(Time)
    
    # Date-based schedule (for temporary/holiday)
    start_date = Column(Date)
    end_date = Column(Date)
    
    # Availability
    availability_status = Column(String(20), default="available")  # AvailabilityStatus enum
    capacity_override = Column(Integer)  # Override service capacity
    
    # On-call details
    on_call_doctor = Column(String(200))
    on_call_phone = Column(String(20))
    response_time_minutes = Column(Integer)  # Expected response time
    
    # Notes
    notes_ar = Column(Text)
    notes_en = Column(Text)
    
    # Priority (higher = more important, for conflict resolution)
    priority = Column(Integer, default=0)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = Column(String(100))
    
    # Relationships
    service = relationship("HospitalService", back_populates="schedules")
    
    def __repr__(self):
        return f"<ServiceSchedule {self.schedule_type} for Service {self.service_id}>"

class ScheduleOverride(db.Model):
    """Temporary schedule overrides (e.g., emergency closures, special events)"""
    __tablename__ = 'schedule_overrides'
    
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service_configurations.id'), nullable=False)
    
    # Override period
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    
    # Override details
    availability_status = Column(String(20), nullable=False)  # AvailabilityStatus enum
    reason_ar = Column(Text, nullable=False)
    reason_en = Column(Text, nullable=False)
    
    # Alternative service (if available)
    alternative_service_id = Column(Integer, ForeignKey('service_configurations.id'))
    alternative_hospital_id = Column(Integer, ForeignKey('hospitals.id'))
    
    # Notification
    notify_patients = Column(Boolean, default=True)
    notification_message_ar = Column(Text)
    notification_message_en = Column(Text)
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100))
    approved_by = Column(String(100))
    
    # Relationships
    service = relationship("HospitalService", foreign_keys=[service_id])
    alternative_service = relationship("HospitalService", foreign_keys=[alternative_service_id])
    
    def __repr__(self):
        return f"<ScheduleOverride for Service {self.service_id} from {self.start_datetime}>"

class ServiceAvailabilityLog(db.Model):
    """Audit log for service availability changes"""
    __tablename__ = 'service_availability_logs'
    
    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('service_configurations.id'), nullable=False)
    
    # Change details
    change_type = Column(String(50), nullable=False)  # 'schedule_created', 'override_added', 'status_changed', etc.
    old_status = Column(String(20))
    new_status = Column(String(20))
    
    # Context
    change_reason = Column(Text)
    affected_datetime = Column(DateTime)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(100))
    ip_address = Column(String(50))
    user_agent = Column(String(200))
    
    # Additional data (JSON)
    extra_data = Column(JSON)
    
    # Relationships
    service = relationship("HospitalService")
    
    def __repr__(self):
        return f"<ServiceAvailabilityLog {self.change_type} at {self.created_at}>"

class ServiceRequest(db.Model):
    """Track patient service requests for analytics"""
    __tablename__ = 'service_requests'
    
    id = Column(Integer, primary_key=True)
    
    # Request details
    service_type = Column(String(50), nullable=False)
    requested_hospital_id = Column(Integer, ForeignKey('hospitals.id'))
    
    # Patient location
    patient_latitude = Column(Float)
    patient_longitude = Column(Float)
    patient_city = Column(String(100))
    
    # Recommendation
    recommended_hospital_id = Column(Integer, ForeignKey('hospitals.id'))
    recommended_service_id = Column(Integer, ForeignKey('service_configurations.id'))
    distance_km = Column(Float)
    
    # Result
    was_available = Column(Boolean)
    availability_status = Column(String(20))
    wait_time_minutes = Column(Integer)
    
    # Patient decision
    patient_accepted = Column(Boolean)
    patient_feedback = Column(Text)
    
    # Metadata
    request_datetime = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String(100))
    user_id = Column(Integer)  # Optional: link to user if users table exists
    
    # Relationships
    requested_hospital = relationship("Hospital", foreign_keys=[requested_hospital_id])
    recommended_hospital = relationship("Hospital", foreign_keys=[recommended_hospital_id])
    recommended_service = relationship("HospitalService")
    
    def __repr__(self):
        return f"<ServiceRequest {self.service_type} at {self.request_datetime}>"

# Helper function to check if a service is available at a specific datetime
def is_service_available(service_id: int, check_datetime: datetime = None) -> dict:
    """
    Check if a service is available at a specific datetime
    
    Args:
        service_id: ID of the hospital service
        check_datetime: DateTime to check (default: now)
    
    Returns:
        dict with keys: available (bool), status (str), reason (str), alternative (dict)
    """
    if check_datetime is None:
        check_datetime = datetime.now()
    
    # Get service
    service = HospitalService.query.get(service_id)
    if not service or not service.is_active:
        return {
            "available": False,
            "status": "unavailable",
            "reason": "Service not found or inactive",
            "alternative": None
        }
    
    # Check for active overrides (highest priority)
    override = ScheduleOverride.query.filter(
        ScheduleOverride.service_id == service_id,
        ScheduleOverride.is_active == True,
        ScheduleOverride.start_datetime <= check_datetime,
        ScheduleOverride.end_datetime >= check_datetime
    ).first()
    
    if override:
        return {
            "available": override.availability_status == "available",
            "status": override.availability_status,
            "reason": override.reason_en,
            "alternative": {
                "service_id": override.alternative_service_id,
                "hospital_id": override.alternative_hospital_id
            } if override.alternative_service_id else None
        }
    
    # Check regular schedules
    day_of_week = check_datetime.weekday()
    check_time = check_datetime.time()
    check_date = check_datetime.date()
    
    # Get applicable schedules (ordered by priority)
    schedules = ServiceSchedule.query.filter(
        ServiceSchedule.service_id == service_id,
        ServiceSchedule.is_active == True
    ).order_by(ServiceSchedule.priority.desc()).all()
    
    for schedule in schedules:
        # Check if schedule applies to this datetime
        applies = False
        
        if schedule.schedule_type == "temporary":
            # Temporary schedule with date range
            if schedule.start_date and schedule.end_date:
                if schedule.start_date <= check_date <= schedule.end_date:
                    applies = True
        elif schedule.schedule_type == "holiday":
            # Holiday schedule with date range
            if schedule.start_date and schedule.end_date:
                if schedule.start_date <= check_date <= schedule.end_date:
                    applies = True
        else:
            # Regular or on-call schedule
            if schedule.day_of_week is None or schedule.day_of_week == day_of_week:
                if schedule.start_time and schedule.end_time:
                    if schedule.start_time <= check_time <= schedule.end_time:
                        applies = True
                else:
                    # No time restriction = all day
                    applies = True
        
        if applies:
            return {
                "available": schedule.availability_status in ["available", "limited"],
                "status": schedule.availability_status,
                "reason": f"Schedule: {schedule.schedule_type}",
                "on_call": {
                    "doctor": schedule.on_call_doctor,
                    "phone": schedule.on_call_phone,
                    "response_time": schedule.response_time_minutes
                } if schedule.schedule_type == "on_call" else None,
                "capacity": schedule.capacity_override or service.capacity,
                "wait_time": service.average_wait_time
            }
    
    # No schedule found = unavailable
    return {
        "available": False,
        "status": "unavailable",
        "reason": "No active schedule for this time",
        "alternative": None
    }
