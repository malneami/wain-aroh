"""
Patient Routing API
Public endpoints for finding nearest hospitals with available services
Integrates with the "وين أروح" patient guidance flow
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from ..services.intelligent_router import IntelligentRouter
from ..services.schedule_manager import ScheduleManager
from ..models.service_schedule import ServiceType

routing_api = Blueprint('routing_api', __name__)

@routing_api.route('/api/routing/find-nearest', methods=['POST'])
def find_nearest_hospital():
    """
    Find nearest hospital with required service available
    
    Request body:
    {
        "patient_lat": 24.7136,
        "patient_lon": 46.6753,
        "service_type": "emergency",
        "patient_city": "Riyadh",
        "ctas_level": 2,
        "max_distance_km": 50,
        "limit": 10
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'patient_lat' not in data or 'patient_lon' not in data:
            return jsonify({
                "success": False,
                "error": "Patient location (patient_lat, patient_lon) is required"
            }), 400
        
        if 'service_type' not in data:
            return jsonify({
                "success": False,
                "error": "Service type is required"
            }), 400
        
        # Get parameters
        patient_lat = float(data['patient_lat'])
        patient_lon = float(data['patient_lon'])
        service_type = data['service_type']
        patient_city = data.get('patient_city')
        ctas_level = data.get('ctas_level')
        max_distance_km = data.get('max_distance_km', 50.0)
        limit = data.get('limit', 10)
        check_datetime_str = data.get('check_datetime')
        
        # Parse datetime if provided
        check_datetime = None
        if check_datetime_str:
            check_datetime = datetime.fromisoformat(check_datetime_str)
        
        # Find nearest hospitals
        results = IntelligentRouter.find_nearest_with_service(
            patient_lat=patient_lat,
            patient_lon=patient_lon,
            service_type=service_type,
            check_datetime=check_datetime,
            max_distance_km=max_distance_km,
            limit=limit,
            patient_city=patient_city,
            ctas_level=ctas_level
        )
        
        if not results:
            return jsonify({
                "success": True,
                "message": "No hospitals found with the requested service within the search radius",
                "results": [],
                "count": 0
            }), 200
        
        return jsonify({
            "success": True,
            "count": len(results),
            "results": results,
            "search_params": {
                "patient_location": {
                    "latitude": patient_lat,
                    "longitude": patient_lon,
                    "city": patient_city
                },
                "service_type": service_type,
                "ctas_level": ctas_level,
                "max_distance_km": max_distance_km,
                "check_datetime": (check_datetime or datetime.now()).isoformat()
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@routing_api.route('/api/routing/find-alternative', methods=['POST'])
def find_alternative_services():
    """
    Find alternative hospitals when primary hospital service is unavailable
    
    Request body:
    {
        "hospital_id": 1,
        "service_type": "cardiology",
        "max_distance_km": 30
    }
    """
    try:
        data = request.get_json()
        
        if 'hospital_id' not in data or 'service_type' not in data:
            return jsonify({
                "success": False,
                "error": "hospital_id and service_type are required"
            }), 400
        
        hospital_id = data['hospital_id']
        service_type = data['service_type']
        max_distance_km = data.get('max_distance_km', 30.0)
        check_datetime_str = data.get('check_datetime')
        
        check_datetime = None
        if check_datetime_str:
            check_datetime = datetime.fromisoformat(check_datetime_str)
        
        alternatives = IntelligentRouter.find_alternative_services(
            hospital_id=hospital_id,
            service_type=service_type,
            check_datetime=check_datetime,
            max_distance_km=max_distance_km
        )
        
        return jsonify({
            "success": True,
            "count": len(alternatives),
            "alternatives": alternatives
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@routing_api.route('/api/routing/coverage-map', methods=['GET'])
def get_coverage_map():
    """
    Get service coverage map across all hospitals
    
    Query params:
    - service_type: Required service type
    - check_datetime: Optional datetime to check (ISO format)
    """
    try:
        service_type = request.args.get('service_type')
        
        if not service_type:
            return jsonify({
                "success": False,
                "error": "service_type is required"
            }), 400
        
        check_datetime_str = request.args.get('check_datetime')
        check_datetime = None
        if check_datetime_str:
            check_datetime = datetime.fromisoformat(check_datetime_str)
        
        coverage_map = IntelligentRouter.get_service_coverage_map(
            service_type=service_type,
            check_datetime=check_datetime
        )
        
        return jsonify({
            "success": True,
            "service_type": service_type,
            "check_datetime": (check_datetime or datetime.now()).isoformat(),
            "coverage_by_city": coverage_map
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@routing_api.route('/api/routing/check-service', methods=['POST'])
def check_service_availability():
    """
    Check if a specific service is available at a hospital
    
    Request body:
    {
        "service_id": 1,
        "check_datetime": "2025-01-15T14:30:00" (optional)
    }
    """
    try:
        data = request.get_json()
        
        if 'service_id' not in data:
            return jsonify({
                "success": False,
                "error": "service_id is required"
            }), 400
        
        service_id = data['service_id']
        check_datetime_str = data.get('check_datetime')
        
        check_datetime = None
        if check_datetime_str:
            check_datetime = datetime.fromisoformat(check_datetime_str)
        
        availability = ScheduleManager.check_availability(service_id, check_datetime)
        
        return jsonify({
            "success": True,
            "service_id": service_id,
            "check_datetime": (check_datetime or datetime.now()).isoformat(),
            "availability": availability
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@routing_api.route('/api/routing/service-types', methods=['GET'])
def list_service_types():
    """Get list of available service types"""
    return jsonify({
        "success": True,
        "service_types": [
            {
                "value": st.value,
                "label_en": st.value.replace('_', ' ').title(),
                "label_ar": _get_arabic_service_name(st.value)
            }
            for st in ServiceType
        ]
    }), 200

@routing_api.route('/api/routing/recommend', methods=['POST'])
def recommend_facility():
    """
    Recommend facility based on CTAS level and location
    Integrated with "وين أروح" patient guidance flow
    
    Request body:
    {
        "patient_lat": 24.7136,
        "patient_lon": 46.6753,
        "patient_city": "Riyadh",
        "ctas_level": 2,
        "symptoms": ["chest pain", "shortness of breath"],
        "required_specialty": "cardiology" (optional)
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'patient_lat' not in data or 'patient_lon' not in data:
            return jsonify({
                "success": False,
                "error": "Patient location is required"
            }), 400
        
        if 'ctas_level' not in data:
            return jsonify({
                "success": False,
                "error": "CTAS level is required"
            }), 400
        
        patient_lat = float(data['patient_lat'])
        patient_lon = float(data['patient_lon'])
        patient_city = data.get('patient_city')
        ctas_level = int(data['ctas_level'])
        required_specialty = data.get('required_specialty')
        
        # Determine service type based on CTAS level
        if ctas_level <= 2:
            # Critical - Emergency Department
            service_type = "emergency"
            recommendation_type = "emergency_department"
            message_ar = "يجب التوجه فوراً إلى قسم الطوارئ"
            message_en = "Go immediately to Emergency Department"
        elif ctas_level == 3:
            # Urgent - Urgent Care Center or Emergency
            service_type = required_specialty if required_specialty else "emergency"
            recommendation_type = "urgent_care"
            message_ar = "يُنصح بزيارة مركز الرعاية العاجلة أو الطوارئ"
            message_en = "Visit Urgent Care Center or Emergency Department"
        else:
            # Less urgent - Clinic or Urgent Care
            service_type = required_specialty if required_specialty else "emergency"
            recommendation_type = "clinic"
            message_ar = "يمكن حجز موعد في العيادة أو زيارة مركز الرعاية العاجلة"
            message_en = "Book appointment at clinic or visit Urgent Care Center"
        
        # Find nearest facilities
        results = IntelligentRouter.find_nearest_with_service(
            patient_lat=patient_lat,
            patient_lon=patient_lon,
            service_type=service_type,
            max_distance_km=50.0,
            limit=5,
            patient_city=patient_city,
            ctas_level=ctas_level
        )
        
        if not results:
            return jsonify({
                "success": True,
                "recommendation": {
                    "type": recommendation_type,
                    "ctas_level": ctas_level,
                    "message_ar": "لم يتم العثور على منشآت قريبة. يرجى الاتصال بالإسعاف 997",
                    "message_en": "No nearby facilities found. Please call ambulance 997",
                    "facilities": []
                }
            }), 200
        
        return jsonify({
            "success": True,
            "recommendation": {
                "type": recommendation_type,
                "ctas_level": ctas_level,
                "message_ar": message_ar,
                "message_en": message_en,
                "primary_facility": results[0],
                "alternative_facilities": results[1:5] if len(results) > 1 else [],
                "total_facilities_found": len(results)
            }
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@routing_api.route('/api/routing/analytics', methods=['GET'])
def get_routing_analytics():
    """Get routing analytics"""
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        service_type = request.args.get('service_type')
        city = request.args.get('city')
        
        start_date = datetime.fromisoformat(start_date_str) if start_date_str else None
        end_date = datetime.fromisoformat(end_date_str) if end_date_str else None
        
        analytics = IntelligentRouter.get_routing_analytics(
            start_date=start_date,
            end_date=end_date,
            service_type=service_type,
            city=city
        )
        
        return jsonify({
            "success": True,
            "analytics": analytics
        }), 200
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

def _get_arabic_service_name(service_type: str) -> str:
    """Get Arabic name for service type"""
    arabic_names = {
        "emergency": "الطوارئ",
        "cardiology": "أمراض القلب",
        "neurology": "الأعصاب",
        "orthopedics": "العظام",
        "pediatrics": "الأطفال",
        "obstetrics": "النساء والولادة",
        "surgery": "الجراحة",
        "icu": "العناية المركزة",
        "nicu": "عناية الأطفال المركزة",
        "radiology": "الأشعة",
        "laboratory": "المختبر",
        "pharmacy": "الصيدلية",
        "dialysis": "الغسيل الكلوي",
        "oncology": "الأورام",
        "psychiatry": "الطب النفسي",
        "dermatology": "الجلدية",
        "ophthalmology": "العيون",
        "ent": "الأنف والأذن والحنجرة",
        "dental": "الأسنان",
        "physiotherapy": "العلاج الطبيعي"
    }
    return arabic_names.get(service_type, service_type)
