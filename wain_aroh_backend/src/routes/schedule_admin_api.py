"""
Schedule Administration API
Admin endpoints for managing service schedules, on-call coverage, and audit logs
"""

from flask import Blueprint, request, jsonify
from datetime import datetime, time, date, timedelta
from ..services.schedule_manager import ScheduleManager
from ..services.intelligent_router import IntelligentRouter
from ..models.service_schedule import (
    HospitalService, ServiceSchedule, ScheduleOverride,
    ServiceAvailabilityLog, ServiceType, ScheduleType, AvailabilityStatus
)
from ..models.hospital import Hospital

schedule_admin_api = Blueprint('schedule_admin_api', __name__)

# ============================================================================
# Service Management
# ============================================================================

@schedule_admin_api.route('/api/admin/services', methods=['GET'])
def list_services():
    """List all hospital services"""
    try:
        hospital_id = request.args.get('hospital_id', type=int)
        service_type = request.args.get('service_type')
        is_active = request.args.get('is_active', type=bool)
        
        query = HospitalService.query
        
        if hospital_id:
            query = query.filter(HospitalService.hospital_id == hospital_id)
        if service_type:
            query = query.filter(HospitalService.service_type == service_type)
        if is_active is not None:
            query = query.filter(HospitalService.is_active == is_active)
        
        services = query.all()
        
        return jsonify({
            "success": True,
            "count": len(services),
            "services": [{
                "id": s.id,
                "hospital_id": s.hospital_id,
                "hospital_name_ar": s.hospital.name_ar if s.hospital else None,
                "hospital_name_en": s.hospital.name_en if s.hospital else None,
                "service_type": s.service_type,
                "service_name_ar": s.service_name_ar,
                "service_name_en": s.service_name_en,
                "description_ar": s.description_ar,
                "description_en": s.description_en,
                "is_active": s.is_active,
                "requires_appointment": s.requires_appointment,
                "has_on_call_coverage": s.has_on_call_coverage,
                "capacity": s.capacity,
                "average_wait_time": s.average_wait_time,
                "phone": s.phone,
                "extension": s.extension,
                "created_at": s.created_at.isoformat() if s.created_at else None,
                "updated_at": s.updated_at.isoformat() if s.updated_at else None
            } for s in services]
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/services', methods=['POST'])
def create_service():
    """Create a new hospital service"""
    try:
        data = request.get_json()
        created_by = data.get('created_by', 'admin')
        
        service = ScheduleManager.create_service(
            hospital_id=data['hospital_id'],
            service_data=data,
            created_by=created_by
        )
        
        return jsonify({
            "success": True,
            "message": "Service created successfully",
            "service_id": service.id
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/services/<int:service_id>', methods=['GET'])
def get_service(service_id):
    """Get service details"""
    try:
        service = HospitalService.query.get(service_id)
        if not service:
            return jsonify({"success": False, "error": "Service not found"}), 404
        
        return jsonify({
            "success": True,
            "service": {
                "id": service.id,
                "hospital_id": service.hospital_id,
                "hospital_name_ar": service.hospital.name_ar if service.hospital else None,
                "hospital_name_en": service.hospital.name_en if service.hospital else None,
                "service_type": service.service_type,
                "service_name_ar": service.service_name_ar,
                "service_name_en": service.service_name_en,
                "description_ar": service.description_ar,
                "description_en": service.description_en,
                "is_active": service.is_active,
                "requires_appointment": service.requires_appointment,
                "has_on_call_coverage": service.has_on_call_coverage,
                "capacity": service.capacity,
                "average_wait_time": service.average_wait_time,
                "phone": service.phone,
                "extension": service.extension,
                "schedules_count": len(service.schedules),
                "created_at": service.created_at.isoformat() if service.created_at else None,
                "updated_at": service.updated_at.isoformat() if service.updated_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/services/<int:service_id>', methods=['PUT'])
def update_service(service_id):
    """Update a service"""
    try:
        data = request.get_json()
        updated_by = data.get('updated_by', 'admin')
        
        service = ScheduleManager.update_service(service_id, data, updated_by)
        
        return jsonify({
            "success": True,
            "message": "Service updated successfully",
            "service_id": service.id
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/services/<int:service_id>', methods=['DELETE'])
def delete_service(service_id):
    """Deactivate a service"""
    try:
        deleted_by = request.args.get('deleted_by', 'admin')
        
        service = ScheduleManager.update_service(
            service_id,
            {'is_active': False},
            deleted_by
        )
        
        return jsonify({
            "success": True,
            "message": "Service deactivated successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# Schedule Management
# ============================================================================

@schedule_admin_api.route('/api/admin/schedules', methods=['GET'])
def list_schedules():
    """List service schedules"""
    try:
        service_id = request.args.get('service_id', type=int)
        schedule_type = request.args.get('schedule_type')
        is_active = request.args.get('is_active', type=bool)
        
        query = ServiceSchedule.query
        
        if service_id:
            query = query.filter(ServiceSchedule.service_id == service_id)
        if schedule_type:
            query = query.filter(ServiceSchedule.schedule_type == schedule_type)
        if is_active is not None:
            query = query.filter(ServiceSchedule.is_active == is_active)
        
        schedules = query.all()
        
        return jsonify({
            "success": True,
            "count": len(schedules),
            "schedules": [{
                "id": s.id,
                "service_id": s.service_id,
                "service_name_ar": s.service.service_name_ar if s.service else None,
                "service_name_en": s.service.service_name_en if s.service else None,
                "schedule_type": s.schedule_type,
                "day_of_week": s.day_of_week,
                "start_time": s.start_time.isoformat() if s.start_time else None,
                "end_time": s.end_time.isoformat() if s.end_time else None,
                "start_date": s.start_date.isoformat() if s.start_date else None,
                "end_date": s.end_date.isoformat() if s.end_date else None,
                "availability_status": s.availability_status,
                "capacity_override": s.capacity_override,
                "on_call_doctor": s.on_call_doctor,
                "on_call_phone": s.on_call_phone,
                "response_time_minutes": s.response_time_minutes,
                "notes_ar": s.notes_ar,
                "notes_en": s.notes_en,
                "priority": s.priority,
                "is_active": s.is_active,
                "created_at": s.created_at.isoformat() if s.created_at else None
            } for s in schedules]
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/schedules', methods=['POST'])
def create_schedule():
    """Create a new schedule"""
    try:
        data = request.get_json()
        created_by = data.get('created_by', 'admin')
        
        # Parse time fields
        if 'start_time' in data and isinstance(data['start_time'], str):
            data['start_time'] = datetime.strptime(data['start_time'], '%H:%M:%S').time()
        if 'end_time' in data and isinstance(data['end_time'], str):
            data['end_time'] = datetime.strptime(data['end_time'], '%H:%M:%S').time()
        if 'start_date' in data and isinstance(data['start_date'], str):
            data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data and isinstance(data['end_date'], str):
            data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        schedule = ScheduleManager.create_schedule(
            service_id=data['service_id'],
            schedule_data=data,
            created_by=created_by
        )
        
        return jsonify({
            "success": True,
            "message": "Schedule created successfully",
            "schedule_id": schedule.id
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/schedules/<int:schedule_id>', methods=['PUT'])
def update_schedule(schedule_id):
    """Update a schedule"""
    try:
        data = request.get_json()
        updated_by = data.get('updated_by', 'admin')
        
        # Parse time fields
        if 'start_time' in data and isinstance(data['start_time'], str):
            data['start_time'] = datetime.strptime(data['start_time'], '%H:%M:%S').time()
        if 'end_time' in data and isinstance(data['end_time'], str):
            data['end_time'] = datetime.strptime(data['end_time'], '%H:%M:%S').time()
        if 'start_date' in data and isinstance(data['start_date'], str):
            data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data and isinstance(data['end_date'], str):
            data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        
        schedule = ScheduleManager.update_schedule(schedule_id, data, updated_by)
        
        return jsonify({
            "success": True,
            "message": "Schedule updated successfully",
            "schedule_id": schedule.id
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/schedules/<int:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    """Delete a schedule"""
    try:
        deleted_by = request.args.get('deleted_by', 'admin')
        
        success = ScheduleManager.delete_schedule(schedule_id, deleted_by)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Schedule deleted successfully"
            }), 200
        else:
            return jsonify({"success": False, "error": "Schedule not found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/schedules/weekly', methods=['POST'])
def create_weekly_schedule():
    """Create a weekly schedule"""
    try:
        data = request.get_json()
        service_id = data['service_id']
        created_by = data.get('created_by', 'admin')
        
        # Parse weekly_hours
        weekly_hours = {}
        for day_str, hours in data['weekly_hours'].items():
            day = int(day_str)
            start = datetime.strptime(hours['start'], '%H:%M:%S').time()
            end = datetime.strptime(hours['end'], '%H:%M:%S').time()
            weekly_hours[day] = (start, end)
        
        schedules = ScheduleManager.create_weekly_schedule(service_id, weekly_hours, created_by)
        
        return jsonify({
            "success": True,
            "message": f"Created {len(schedules)} weekly schedules",
            "schedule_ids": [s.id for s in schedules]
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/schedules/24-7', methods=['POST'])
def create_24_7_schedule():
    """Create a 24/7 schedule"""
    try:
        data = request.get_json()
        service_id = data['service_id']
        created_by = data.get('created_by', 'admin')
        
        schedule = ScheduleManager.create_24_7_schedule(service_id, created_by)
        
        return jsonify({
            "success": True,
            "message": "24/7 schedule created successfully",
            "schedule_id": schedule.id
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# Override Management
# ============================================================================

@schedule_admin_api.route('/api/admin/overrides', methods=['GET'])
def list_overrides():
    """List schedule overrides"""
    try:
        service_id = request.args.get('service_id', type=int)
        is_active = request.args.get('is_active', type=bool)
        
        query = ScheduleOverride.query
        
        if service_id:
            query = query.filter(ScheduleOverride.service_id == service_id)
        if is_active is not None:
            query = query.filter(ScheduleOverride.is_active == is_active)
        
        overrides = query.order_by(ScheduleOverride.start_datetime.desc()).all()
        
        return jsonify({
            "success": True,
            "count": len(overrides),
            "overrides": [{
                "id": o.id,
                "service_id": o.service_id,
                "service_name_ar": o.service.service_name_ar if o.service else None,
                "service_name_en": o.service.service_name_en if o.service else None,
                "start_datetime": o.start_datetime.isoformat(),
                "end_datetime": o.end_datetime.isoformat(),
                "availability_status": o.availability_status,
                "reason_ar": o.reason_ar,
                "reason_en": o.reason_en,
                "alternative_service_id": o.alternative_service_id,
                "alternative_hospital_id": o.alternative_hospital_id,
                "notify_patients": o.notify_patients,
                "is_active": o.is_active,
                "created_at": o.created_at.isoformat() if o.created_at else None,
                "created_by": o.created_by
            } for o in overrides]
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/overrides', methods=['POST'])
def create_override():
    """Create a schedule override"""
    try:
        data = request.get_json()
        created_by = data.get('created_by', 'admin')
        
        # Parse datetime fields
        if isinstance(data['start_datetime'], str):
            data['start_datetime'] = datetime.fromisoformat(data['start_datetime'])
        if isinstance(data['end_datetime'], str):
            data['end_datetime'] = datetime.fromisoformat(data['end_datetime'])
        
        override = ScheduleManager.create_override(
            service_id=data['service_id'],
            override_data=data,
            created_by=created_by
        )
        
        return jsonify({
            "success": True,
            "message": "Override created successfully",
            "override_id": override.id
        }), 201
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/overrides/<int:override_id>', methods=['DELETE'])
def deactivate_override(override_id):
    """Deactivate an override"""
    try:
        deactivated_by = request.args.get('deactivated_by', 'admin')
        
        success = ScheduleManager.deactivate_override(override_id, deactivated_by)
        
        if success:
            return jsonify({
                "success": True,
                "message": "Override deactivated successfully"
            }), 200
        else:
            return jsonify({"success": False, "error": "Override not found"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/overrides/active', methods=['GET'])
def get_active_overrides():
    """Get currently active overrides"""
    try:
        service_id = request.args.get('service_id', type=int)
        
        overrides = ScheduleManager.get_active_overrides(service_id)
        
        return jsonify({
            "success": True,
            "count": len(overrides),
            "overrides": [{
                "id": o.id,
                "service_id": o.service_id,
                "service_name_ar": o.service.service_name_ar if o.service else None,
                "service_name_en": o.service.service_name_en if o.service else None,
                "start_datetime": o.start_datetime.isoformat(),
                "end_datetime": o.end_datetime.isoformat(),
                "availability_status": o.availability_status,
                "reason_ar": o.reason_ar,
                "reason_en": o.reason_en
            } for o in overrides]
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# Availability Checking
# ============================================================================

@schedule_admin_api.route('/api/admin/availability/check', methods=['POST'])
def check_availability():
    """Check service availability at a specific time"""
    try:
        data = request.get_json()
        service_id = data['service_id']
        check_datetime_str = data.get('check_datetime')
        
        if check_datetime_str:
            check_datetime = datetime.fromisoformat(check_datetime_str)
        else:
            check_datetime = None
        
        availability = ScheduleManager.check_availability(service_id, check_datetime)
        
        return jsonify({
            "success": True,
            "service_id": service_id,
            "check_datetime": (check_datetime or datetime.now()).isoformat(),
            "availability": availability
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@schedule_admin_api.route('/api/admin/availability/status', methods=['GET'])
def get_service_status():
    """Get service availability status for a date range"""
    try:
        service_id = request.args.get('service_id', type=int, required=True)
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        
        statuses = ScheduleManager.get_service_status(service_id, start_date, end_date)
        
        return jsonify({
            "success": True,
            "service_id": service_id,
            "start_date": (start_date or date.today()).isoformat(),
            "end_date": (end_date or (date.today() + timedelta(days=7))).isoformat(),
            "statuses": statuses
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# Audit Logs
# ============================================================================

@schedule_admin_api.route('/api/admin/audit-log', methods=['GET'])
def get_audit_log():
    """Get audit log for service changes"""
    try:
        service_id = request.args.get('service_id', type=int)
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        limit = request.args.get('limit', type=int, default=100)
        
        start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else None
        
        logs = ScheduleManager.get_audit_log(service_id, start_date, end_date, limit)
        
        return jsonify({
            "success": True,
            "count": len(logs),
            "logs": [{
                "id": log.id,
                "service_id": log.service_id,
                "change_type": log.change_type,
                "old_status": log.old_status,
                "new_status": log.new_status,
                "change_reason": log.change_reason,
                "affected_datetime": log.affected_datetime.isoformat() if log.affected_datetime else None,
                "created_at": log.created_at.isoformat() if log.created_at else None,
                "created_by": log.created_by
            } for log in logs]
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

# ============================================================================
# Service Types
# ============================================================================

@schedule_admin_api.route('/api/admin/service-types', methods=['GET'])
def get_service_types():
    """Get list of available service types"""
    return jsonify({
        "success": True,
        "service_types": [
            {"value": st.value, "label": st.value.replace('_', ' ').title()}
            for st in ServiceType
        ]
    }), 200

@schedule_admin_api.route('/api/admin/schedule-types', methods=['GET'])
def get_schedule_types():
    """Get list of schedule types"""
    return jsonify({
        "success": True,
        "schedule_types": [
            {"value": st.value, "label": st.value.replace('_', ' ').title()}
            for st in ScheduleType
        ]
    }), 200

@schedule_admin_api.route('/api/admin/availability-statuses', methods=['GET'])
def get_availability_statuses():
    """Get list of availability statuses"""
    return jsonify({
        "success": True,
        "availability_statuses": [
            {"value": ast.value, "label": ast.value.replace('_', ' ').title()}
            for ast in AvailabilityStatus
        ]
    }), 200
