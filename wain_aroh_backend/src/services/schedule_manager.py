"""
Service Schedule Manager
Handles service schedule creation, updates, and real-time availability checks
"""

from datetime import datetime, time, date, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy import and_, or_
from ..models.user import db
from ..models.hospital import Hospital
from ..models.service_schedule import (
    HospitalService, ServiceSchedule, ScheduleOverride,
    ServiceAvailabilityLog, ServiceRequest,
    ServiceType, ScheduleType, AvailabilityStatus,
    is_service_available
)
import math

class ScheduleManager:
    """Manages hospital service schedules and availability"""
    
    @staticmethod
    def create_service(hospital_id: int, service_data: dict, created_by: str = "system") -> HospitalService:
        """Create a new hospital service"""
        service = HospitalService(
            hospital_id=hospital_id,
            service_type=service_data.get('service_type'),
            service_name_ar=service_data.get('service_name_ar'),
            service_name_en=service_data.get('service_name_en'),
            description_ar=service_data.get('description_ar'),
            description_en=service_data.get('description_en'),
            is_active=service_data.get('is_active', True),
            requires_appointment=service_data.get('requires_appointment', False),
            has_on_call_coverage=service_data.get('has_on_call_coverage', False),
            capacity=service_data.get('capacity'),
            average_wait_time=service_data.get('average_wait_time'),
            phone=service_data.get('phone'),
            extension=service_data.get('extension'),
            created_by=created_by
        )
        
        db.session.add(service)
        db.session.commit()
        
        # Log creation
        ScheduleManager._log_change(
            service.id,
            "service_created",
            None,
            "active" if service.is_active else "inactive",
            f"Service created by {created_by}",
            created_by
        )
        
        return service
    
    @staticmethod
    def create_schedule(service_id: int, schedule_data: dict, created_by: str = "system") -> ServiceSchedule:
        """Create a new service schedule"""
        schedule = ServiceSchedule(
            service_id=service_id,
            schedule_type=schedule_data.get('schedule_type'),
            day_of_week=schedule_data.get('day_of_week'),
            start_time=schedule_data.get('start_time'),
            end_time=schedule_data.get('end_time'),
            start_date=schedule_data.get('start_date'),
            end_date=schedule_data.get('end_date'),
            availability_status=schedule_data.get('availability_status', 'available'),
            capacity_override=schedule_data.get('capacity_override'),
            on_call_doctor=schedule_data.get('on_call_doctor'),
            on_call_phone=schedule_data.get('on_call_phone'),
            response_time_minutes=schedule_data.get('response_time_minutes'),
            notes_ar=schedule_data.get('notes_ar'),
            notes_en=schedule_data.get('notes_en'),
            priority=schedule_data.get('priority', 0),
            created_by=created_by
        )
        
        db.session.add(schedule)
        db.session.commit()
        
        # Log creation
        ScheduleManager._log_change(
            service_id,
            "schedule_created",
            None,
            schedule.availability_status,
            f"Schedule created: {schedule.schedule_type}",
            created_by
        )
        
        return schedule
    
    @staticmethod
    def create_override(service_id: int, override_data: dict, created_by: str = "system") -> ScheduleOverride:
        """Create a temporary schedule override"""
        override = ScheduleOverride(
            service_id=service_id,
            start_datetime=override_data.get('start_datetime'),
            end_datetime=override_data.get('end_datetime'),
            availability_status=override_data.get('availability_status'),
            reason_ar=override_data.get('reason_ar'),
            reason_en=override_data.get('reason_en'),
            alternative_service_id=override_data.get('alternative_service_id'),
            alternative_hospital_id=override_data.get('alternative_hospital_id'),
            notify_patients=override_data.get('notify_patients', True),
            notification_message_ar=override_data.get('notification_message_ar'),
            notification_message_en=override_data.get('notification_message_en'),
            created_by=created_by,
            approved_by=override_data.get('approved_by')
        )
        
        db.session.add(override)
        db.session.commit()
        
        # Log creation
        ScheduleManager._log_change(
            service_id,
            "override_created",
            None,
            override.availability_status,
            f"Override: {override.reason_en}",
            created_by,
            affected_datetime=override.start_datetime
        )
        
        return override
    
    @staticmethod
    def update_service(service_id: int, update_data: dict, updated_by: str = "system") -> HospitalService:
        """Update a hospital service"""
        service = HospitalService.query.get(service_id)
        if not service:
            raise ValueError(f"Service {service_id} not found")
        
        old_status = "active" if service.is_active else "inactive"
        
        # Update fields
        for key, value in update_data.items():
            if hasattr(service, key):
                setattr(service, key, value)
        
        service.updated_at = datetime.utcnow()
        db.session.commit()
        
        new_status = "active" if service.is_active else "inactive"
        
        # Log update
        if old_status != new_status:
            ScheduleManager._log_change(
                service_id,
                "service_updated",
                old_status,
                new_status,
                f"Service updated by {updated_by}",
                updated_by
            )
        
        return service
    
    @staticmethod
    def update_schedule(schedule_id: int, update_data: dict, updated_by: str = "system") -> ServiceSchedule:
        """Update a service schedule"""
        schedule = ServiceSchedule.query.get(schedule_id)
        if not schedule:
            raise ValueError(f"Schedule {schedule_id} not found")
        
        old_status = schedule.availability_status
        
        # Update fields
        for key, value in update_data.items():
            if hasattr(schedule, key):
                setattr(schedule, key, value)
        
        schedule.updated_at = datetime.utcnow()
        db.session.commit()
        
        new_status = schedule.availability_status
        
        # Log update
        if old_status != new_status:
            ScheduleManager._log_change(
                schedule.service_id,
                "schedule_updated",
                old_status,
                new_status,
                f"Schedule updated by {updated_by}",
                updated_by
            )
        
        return schedule
    
    @staticmethod
    def delete_schedule(schedule_id: int, deleted_by: str = "system") -> bool:
        """Delete a service schedule"""
        schedule = ServiceSchedule.query.get(schedule_id)
        if not schedule:
            return False
        
        service_id = schedule.service_id
        
        db.session.delete(schedule)
        db.session.commit()
        
        # Log deletion
        ScheduleManager._log_change(
            service_id,
            "schedule_deleted",
            schedule.availability_status,
            None,
            f"Schedule deleted by {deleted_by}",
            deleted_by
        )
        
        return True
    
    @staticmethod
    def check_availability(service_id: int, check_datetime: datetime = None) -> dict:
        """Check if a service is available at a specific datetime"""
        return is_service_available(service_id, check_datetime)
    
    @staticmethod
    def get_service_status(service_id: int, start_date: date = None, end_date: date = None) -> List[dict]:
        """Get service availability status for a date range"""
        if start_date is None:
            start_date = date.today()
        if end_date is None:
            end_date = start_date + timedelta(days=7)
        
        statuses = []
        current_date = start_date
        
        while current_date <= end_date:
            # Check availability for each hour of the day
            for hour in range(24):
                check_datetime = datetime.combine(current_date, time(hour=hour))
                availability = ScheduleManager.check_availability(service_id, check_datetime)
                
                statuses.append({
                    "datetime": check_datetime.isoformat(),
                    "date": current_date.isoformat(),
                    "hour": hour,
                    "available": availability["available"],
                    "status": availability["status"],
                    "reason": availability.get("reason"),
                    "on_call": availability.get("on_call"),
                    "wait_time": availability.get("wait_time")
                })
            
            current_date += timedelta(days=1)
        
        return statuses
    
    @staticmethod
    def _log_change(service_id: int, change_type: str, old_status: str, new_status: str,
                    reason: str, created_by: str, affected_datetime: datetime = None,
                    extra_data: dict = None):
        """Log a service availability change"""
        log = ServiceAvailabilityLog(
            service_id=service_id,
            change_type=change_type,
            old_status=old_status,
            new_status=new_status,
            change_reason=reason,
            affected_datetime=affected_datetime or datetime.utcnow(),
            created_by=created_by,
            extra_data=extra_data
        )
        
        db.session.add(log)
        db.session.commit()
    
    @staticmethod
    def get_audit_log(service_id: int = None, start_date: datetime = None,
                     end_date: datetime = None, limit: int = 100) -> List[ServiceAvailabilityLog]:
        """Get audit log for service changes"""
        query = ServiceAvailabilityLog.query
        
        if service_id:
            query = query.filter(ServiceAvailabilityLog.service_id == service_id)
        
        if start_date:
            query = query.filter(ServiceAvailabilityLog.created_at >= start_date)
        
        if end_date:
            query = query.filter(ServiceAvailabilityLog.created_at <= end_date)
        
        query = query.order_by(ServiceAvailabilityLog.created_at.desc()).limit(limit)
        
        return query.all()
    
    @staticmethod
    def create_weekly_schedule(service_id: int, weekly_hours: dict, created_by: str = "system") -> List[ServiceSchedule]:
        """
        Create a weekly schedule for a service
        
        Args:
            service_id: Service ID
            weekly_hours: Dict mapping day_of_week (0-6) to (start_time, end_time) tuples
            created_by: User creating the schedule
        
        Example:
            weekly_hours = {
                0: (time(8, 0), time(17, 0)),  # Monday 8am-5pm
                1: (time(8, 0), time(17, 0)),  # Tuesday 8am-5pm
                ...
            }
        """
        schedules = []
        
        for day_of_week, (start_time, end_time) in weekly_hours.items():
            schedule_data = {
                'schedule_type': 'regular',
                'day_of_week': day_of_week,
                'start_time': start_time,
                'end_time': end_time,
                'availability_status': 'available'
            }
            
            schedule = ScheduleManager.create_schedule(service_id, schedule_data, created_by)
            schedules.append(schedule)
        
        return schedules
    
    @staticmethod
    def create_24_7_schedule(service_id: int, created_by: str = "system") -> ServiceSchedule:
        """Create a 24/7 schedule for a service"""
        schedule_data = {
            'schedule_type': 'regular',
            'day_of_week': None,  # All days
            'start_time': time(0, 0),
            'end_time': time(23, 59),
            'availability_status': 'available'
        }
        
        return ScheduleManager.create_schedule(service_id, schedule_data, created_by)
    
    @staticmethod
    def get_active_overrides(service_id: int = None, check_datetime: datetime = None) -> List[ScheduleOverride]:
        """Get active schedule overrides"""
        if check_datetime is None:
            check_datetime = datetime.now()
        
        query = ScheduleOverride.query.filter(
            ScheduleOverride.is_active == True,
            ScheduleOverride.start_datetime <= check_datetime,
            ScheduleOverride.end_datetime >= check_datetime
        )
        
        if service_id:
            query = query.filter(ScheduleOverride.service_id == service_id)
        
        return query.all()
    
    @staticmethod
    def deactivate_override(override_id: int, deactivated_by: str = "system") -> bool:
        """Deactivate a schedule override"""
        override = ScheduleOverride.query.get(override_id)
        if not override:
            return False
        
        override.is_active = False
        db.session.commit()
        
        # Log deactivation
        ScheduleManager._log_change(
            override.service_id,
            "override_deactivated",
            override.availability_status,
            None,
            f"Override deactivated by {deactivated_by}",
            deactivated_by
        )
        
        return True
