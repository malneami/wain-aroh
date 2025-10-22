"""
Settings API Routes
Handles user settings, preferences, and doctor assignments
"""

from flask import Blueprint, request, jsonify
from src.services.settings_service import settings_service
from src.services.waiting_time_service import waiting_time_service
from src.services.doctor_alert_service import doctor_alert_service
from src.data.facilities_ngh import FACILITIES

settings_api_bp = Blueprint('settings_api', __name__, url_prefix='/api/settings')

@settings_api_bp.route('/get', methods=['POST'])
def get_settings():
    """Get user settings"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        
        settings = settings_service.get_user_settings(user_id)
        
        return jsonify({
            "success": True,
            "settings": settings
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@settings_api_bp.route('/update', methods=['POST'])
def update_settings():
    """Update user settings"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        settings = data.get('settings')
        
        if not settings:
            return jsonify({
                "success": False,
                "error": "Settings required"
            }), 400
        
        result = settings_service.update_user_settings(user_id, settings)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@settings_api_bp.route('/hospital/add', methods=['POST'])
def add_preferred_hospital():
    """Add hospital to preferred list"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        hospital_id = data.get('hospital_id')
        hospital_name = data.get('hospital_name')
        
        result = settings_service.add_preferred_hospital(user_id, hospital_id, hospital_name)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@settings_api_bp.route('/doctor/assign', methods=['POST'])
def assign_doctor():
    """Assign doctor to patient"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        doctor_info = data.get('doctor_info')
        
        if not doctor_info:
            return jsonify({
                "success": False,
                "error": "Doctor info required"
            }), 400
        
        result = settings_service.set_assigned_doctor(user_id, doctor_info)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@settings_api_bp.route('/waiting-times', methods=['POST'])
def get_waiting_times():
    """Get waiting times for facilities"""
    try:
        data = request.json
        ctas_level = data.get('ctas_level', 3)
        facility_ids = data.get('facility_ids', None)
        
        # Get facilities
        if facility_ids:
            facilities = [f for f in FACILITIES if f['id'] in facility_ids]
        else:
            facilities = FACILITIES
        
        # Get waiting times
        waiting_times = waiting_time_service.get_all_waiting_times(facilities, ctas_level)
        
        # Add facility info
        results = []
        for facility in facilities:
            facility_id = facility['id']
            results.append({
                "facility": facility,
                "waiting_time": waiting_times[facility_id]
            })
        
        # Sort by wait time
        results.sort(key=lambda x: x['waiting_time']['wait_time_minutes'])
        
        return jsonify({
            "success": True,
            "facilities": results,
            "ctas_level": ctas_level
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@settings_api_bp.route('/doctor/alert', methods=['POST'])
def send_doctor_alert():
    """Send alert to doctor for critical case"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        patient_info = data.get('patient_info', {})
        conversation_history = data.get('conversation_history', [])
        uploaded_files = data.get('uploaded_files', [])
        triage_result = data.get('triage_result', {})
        
        # Get assigned doctor
        assigned_doctor = settings_service.get_assigned_doctor(user_id)
        
        if not assigned_doctor:
            return jsonify({
                "success": False,
                "error": "No assigned doctor found"
            }), 404
        
        # Check if alert should be sent
        ctas_level = triage_result.get('ctas_level', 5)
        should_alert = doctor_alert_service.should_alert_doctor(ctas_level, uploaded_files)
        
        if not should_alert:
            return jsonify({
                "success": False,
                "message": "Alert not required for this case"
            })
        
        # Generate summary
        summary = doctor_alert_service.generate_doctor_summary(
            patient_info,
            conversation_history,
            uploaded_files,
            triage_result
        )
        
        if not summary:
            return jsonify({
                "success": False,
                "error": "Failed to generate summary"
            }), 500
        
        # Determine urgency
        urgency = "critical" if ctas_level <= 2 else "high"
        
        # Send alert
        result = doctor_alert_service.send_doctor_alert(
            assigned_doctor,
            summary,
            urgency
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@settings_api_bp.route('/doctor/alerts/history', methods=['POST'])
def get_alert_history():
    """Get alert history"""
    try:
        data = request.json
        doctor_id = data.get('doctor_id', None)
        
        alerts = doctor_alert_service.get_alert_history(doctor_id)
        
        return jsonify({
            "success": True,
            "alerts": alerts,
            "count": len(alerts)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

