"""
Enhanced API Routes for Wain Aroh
- GPS location detection
- Facility recommendation
- Agentic AI for OPD booking
- Patient reallocation
"""

from flask import Blueprint, request, jsonify
from src.services.location_service import location_service
from src.services.agentic_ai import agentic_ai
from src.data.facilities_ngh import get_main_hospital, get_uccs_near_main, get_clinics

enhanced_api_bp = Blueprint('enhanced_api', __name__, url_prefix='/api/v2')

# ==========================================
# LOCATION & FACILITY ENDPOINTS
# ==========================================

@enhanced_api_bp.route('/location/request-permission', methods=['POST'])
def request_location_permission():
    """Request GPS permission from patient"""
    try:
        permission_request = location_service.request_location_permission()
        
        return jsonify({
            'success': True,
            **permission_request
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/location/detect', methods=['POST'])
def detect_location():
    """Process GPS location from patient"""
    try:
        data = request.json
        gps_data = data.get('gps_data')
        
        if not gps_data:
            return jsonify({
                'success': False,
                'error': 'GPS data required'
            }), 400
        
        patient_location = location_service.get_patient_location(gps_data)
        
        return jsonify({
            'success': True,
            'location': patient_location
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/facility/recommend', methods=['POST'])
def recommend_facility():
    """Recommend best facility based on location and CTAS"""
    try:
        data = request.json
        
        patient_location = data.get('patient_location')
        ctas_level = data.get('ctas_level', 3)
        preferred_type = data.get('preferred_type')
        
        # Get recommendation
        recommendation = location_service.find_best_facility(
            patient_location,
            ctas_level,
            preferred_type
        )
        
        # Format message
        message = location_service.format_facility_recommendation(
            recommendation,
            patient_location
        )
        
        # Get all options
        if patient_location:
            all_options = location_service.get_all_nearby_options(
                patient_location,
                ctas_level
            )
        else:
            all_options = []
        
        return jsonify({
            'success': True,
            'recommendation': {
                'facility': recommendation['facility'],
                'reason': recommendation['reason'],
                'distance_km': recommendation.get('distance_km'),
                'travel_time_minutes': recommendation.get('estimated_travel_time_minutes'),
                'message': message
            },
            'all_options': all_options
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/facility/nearby', methods=['POST'])
def get_nearby_facilities():
    """Get all nearby facilities"""
    try:
        data = request.json
        
        patient_location = data.get('patient_location')
        ctas_level = data.get('ctas_level')
        facility_type = data.get('facility_type')
        
        if not patient_location:
            return jsonify({
                'success': False,
                'error': 'Patient location required'
            }), 400
        
        # Get nearby options
        from src.data.facilities_ngh import find_nearest_facilities
        
        facilities = find_nearest_facilities(
            patient_location['latitude'],
            patient_location['longitude'],
            facility_type=facility_type,
            ctas_level=ctas_level,
            limit=10
        )
        
        # Add directions for each
        for facility in facilities:
            facility['directions_url'] = location_service.get_directions_url(
                patient_location,
                facility
            )
            facility['travel_time_minutes'] = location_service.estimate_travel_time(
                facility.get('distance_km')
            )
        
        return jsonify({
            'success': True,
            'facilities': facilities,
            'count': len(facilities)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/facility/main-hospital', methods=['GET'])
def get_main_hospital_info():
    """Get National Guard Hospital information"""
    try:
        main_hospital = get_main_hospital()
        
        return jsonify({
            'success': True,
            'hospital': main_hospital
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/facility/uccs', methods=['GET'])
def get_uccs():
    """Get all UCCs around main hospital"""
    try:
        uccs = get_uccs_near_main()
        
        return jsonify({
            'success': True,
            'uccs': uccs,
            'count': len(uccs)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==========================================
# AGENTIC AI ENDPOINTS
# ==========================================

@enhanced_api_bp.route('/agent/execute', methods=['POST'])
def execute_agent_task():
    """Execute agentic AI task"""
    try:
        data = request.json
        
        user_request = data.get('request')
        patient_data = data.get('patient_data')
        
        if not user_request:
            return jsonify({
                'success': False,
                'error': 'Request required'
            }), 400
        
        # Execute task with agentic AI
        result = agentic_ai.execute_task(user_request, patient_data)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/agent/book-appointment', methods=['POST'])
def book_appointment():
    """Book OPD appointment"""
    try:
        data = request.json
        
        # Extract booking details
        clinic_id = data.get('clinic_id')
        specialty = data.get('specialty')
        appointment_datetime = data.get('appointment_datetime')
        patient_name = data.get('patient_name')
        patient_phone = data.get('patient_phone')
        reason = data.get('reason', '')
        
        # Validate required fields
        if not all([clinic_id, specialty, appointment_datetime, patient_name, patient_phone]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Book appointment
        result = agentic_ai.book_appointment(
            clinic_id=clinic_id,
            specialty=specialty,
            appointment_datetime=appointment_datetime,
            patient_name=patient_name,
            patient_phone=patient_phone,
            reason=reason
        )
        
        # Send SMS confirmation
        if result['success']:
            agentic_ai.send_sms_notification(
                phone_number=patient_phone,
                message_type='appointment_confirmation',
                details={
                    'booking_id': result['booking']['booking_id'],
                    'date': appointment_datetime.split('T')[0],
                    'time': appointment_datetime.split('T')[1],
                    'clinic': result['booking']['clinic_name']
                }
            )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/agent/search-appointments', methods=['POST'])
def search_appointments():
    """Search available appointments"""
    try:
        data = request.json
        
        specialty = data.get('specialty')
        preferred_date = data.get('preferred_date')
        preferred_time = data.get('preferred_time')
        clinic_id = data.get('clinic_id')
        
        if not specialty:
            return jsonify({
                'success': False,
                'error': 'Specialty required'
            }), 400
        
        # Search appointments
        result = agentic_ai.search_available_appointments(
            specialty=specialty,
            preferred_date=preferred_date,
            preferred_time=preferred_time,
            clinic_id=clinic_id
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/agent/search-best-center', methods=['POST'])
def search_best_center():
    """Search for best medical center"""
    try:
        data = request.json
        
        condition = data.get('condition')
        urgency_level = data.get('urgency_level', 'routine')
        patient_location = data.get('patient_location')
        preferences = data.get('preferences', [])
        
        if not condition:
            return jsonify({
                'success': False,
                'error': 'Condition required'
            }), 400
        
        # Search best center
        result = agentic_ai.search_best_center(
            condition=condition,
            urgency_level=urgency_level,
            patient_location=patient_location,
            preferences=preferences
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/agent/reallocate-patient', methods=['POST'])
def reallocate_patient():
    """Reallocate patient to suitable emergency center"""
    try:
        data = request.json
        
        patient_condition = data.get('patient_condition')
        ctas_level = data.get('ctas_level')
        current_facility_id = data.get('current_facility_id')
        required_specialty = data.get('required_specialty')
        patient_location = data.get('patient_location')
        
        if not all([patient_condition, ctas_level]):
            return jsonify({
                'success': False,
                'error': 'Patient condition and CTAS level required'
            }), 400
        
        # Reallocate patient
        result = agentic_ai.reallocate_patient(
            patient_condition=patient_condition,
            ctas_level=ctas_level,
            current_facility_id=current_facility_id,
            required_specialty=required_specialty,
            patient_location=patient_location
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@enhanced_api_bp.route('/agent/check-capacity', methods=['POST'])
def check_capacity():
    """Check facility capacity and wait times"""
    try:
        data = request.json
        
        facility_ids = data.get('facility_ids')
        facility_type = data.get('facility_type')
        
        # Check capacity
        result = agentic_ai.check_facility_capacity(
            facility_ids=facility_ids,
            facility_type=facility_type
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==========================================
# INTEGRATED TRIAGE WITH LOCATION
# ==========================================

@enhanced_api_bp.route('/triage/complete', methods=['POST'])
def complete_triage_with_location():
    """Complete triage assessment with location-based recommendation"""
    try:
        data = request.json
        
        conversation = data.get('conversation', [])
        patient_data = data.get('patient_data', {})
        patient_location = data.get('patient_location')
        
        # Get CTAS assessment (using existing triage service)
        from src.services.ai_triage import assess_patient_condition
        
        triage_result = assess_patient_condition(conversation)
        ctas_level = triage_result.get('ctas_level', 3)
        
        # Get facility recommendation
        recommendation = location_service.find_best_facility(
            patient_location,
            ctas_level
        )
        
        # Format complete response
        facility_message = location_service.format_facility_recommendation(
            recommendation,
            patient_location
        )
        
        # Get all nearby options
        if patient_location:
            all_options = location_service.get_all_nearby_options(
                patient_location,
                ctas_level
            )
        else:
            all_options = []
        
        return jsonify({
            'success': True,
            'triage': {
                'ctas_level': ctas_level,
                'assessment': triage_result.get('assessment', ''),
                'urgency': triage_result.get('urgency', '')
            },
            'recommendation': {
                'facility': recommendation['facility'],
                'reason': recommendation['reason'],
                'distance_km': recommendation.get('distance_km'),
                'travel_time_minutes': recommendation.get('estimated_travel_time_minutes'),
                'message': facility_message
            },
            'all_options': all_options[:5]
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# ==========================================
# HEALTH CHECK
# ==========================================

@enhanced_api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'Wain Aroh Enhanced API',
        'version': '2.0',
        'features': [
            'GPS location detection',
            'Facility recommendation',
            'Agentic AI for OPD booking',
            'Patient reallocation',
            'National Guard Hospital network'
        ]
    })

