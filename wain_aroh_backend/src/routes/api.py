from flask import Blueprint, request, jsonify, send_file
import json
import os
from datetime import datetime
from src.services.ai_triage import chat_with_ai, analyze_symptoms, transcribe_audio, text_to_speech
from src.data.facilities import FACILITIES, CTAS_DEFINITIONS, get_facilities_by_ctas, get_facility_by_id
import math

api_bp = Blueprint('api', __name__, url_prefix='/api')

# In-memory session storage (for prototype)
sessions = {}
assessments = []

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Wain Aroh API",
        "timestamp": datetime.now().isoformat()
    })

@api_bp.route('/chat', methods=['POST'])
def chat():
    """
    Chat with AI assistant
    
    Request body:
    {
        "session_id": "unique_session_id",
        "message": "user message",
        "messages": [optional array of previous messages]
    }
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        user_message = data.get('message')
        messages = data.get('messages', [])
        
        if not session_id or not user_message:
            return jsonify({
                "success": False,
                "error": "session_id and message are required"
            }), 400
        
        # Initialize session if not exists
        if session_id not in sessions:
            sessions[session_id] = {
                "id": session_id,
                "started_at": datetime.now().isoformat(),
                "messages": [],
                "assessment": None
            }
        
        # Add user message to conversation
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Get AI response
        result = chat_with_ai(messages)
        
        if result['success']:
            # Add assistant message
            messages.append({
                "role": "assistant",
                "content": result['message']
            })
            
            # Update session
            sessions[session_id]['messages'] = messages
            
            # If assessment is available, save it
            if result.get('assessment'):
                sessions[session_id]['assessment'] = result['assessment']
            
            return jsonify({
                "success": True,
                "message": result['message'],
                "assessment": result.get('assessment'),
                "session_id": session_id
            })
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze symptoms and get CTAS assessment
    
    Request body:
    {
        "symptoms": "description of symptoms",
        "location": {"lat": 16.8892, "lng": 42.5511}
    }
    """
    try:
        data = request.json
        symptoms = data.get('symptoms')
        location = data.get('location')
        
        if not symptoms:
            return jsonify({
                "success": False,
                "error": "symptoms are required"
            }), 400
        
        # Analyze symptoms
        result = analyze_symptoms(symptoms)
        
        if result['success']:
            # If location provided, sort facilities by distance
            if location and 'recommended_facilities' in result:
                facilities = result['recommended_facilities']
                for facility in facilities:
                    if facility['location']['lat'] != 0:
                        distance = calculate_distance(
                            location['lat'], location['lng'],
                            facility['location']['lat'], facility['location']['lng']
                        )
                        facility['distance_km'] = round(distance, 2)
                
                # Sort by distance
                facilities.sort(key=lambda x: x.get('distance_km', float('inf')))
                result['recommended_facilities'] = facilities
            
            # Save assessment
            assessment = {
                "id": len(assessments) + 1,
                "timestamp": datetime.now().isoformat(),
                "symptoms": symptoms,
                "ctas_level": result['ctas_level'],
                "care_type": result['care_type'],
                "location": location
            }
            assessments.append(assessment)
            
            return jsonify(result)
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/voice/transcribe', methods=['POST'])
def transcribe():
    """
    Transcribe audio to text
    
    Expects multipart/form-data with 'audio' file
    """
    try:
        if 'audio' not in request.files:
            return jsonify({
                "success": False,
                "error": "audio file is required"
            }), 400
        
        audio_file = request.files['audio']
        
        # Save temporarily
        temp_path = f"/tmp/audio_{datetime.now().timestamp()}.webm"
        audio_file.save(temp_path)
        
        # Transcribe
        result = transcribe_audio(temp_path)
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/voice/speak', methods=['POST'])
def speak():
    """
    Convert text to speech
    
    Request body:
    {
        "text": "text to convert"
    }
    """
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({
                "success": False,
                "error": "text is required"
            }), 400
        
        # Generate speech
        output_path = f"/tmp/speech_{datetime.now().timestamp()}.mp3"
        result = text_to_speech(text, output_path)
        
        if result['success']:
            return send_file(output_path, mimetype='audio/mpeg')
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/facilities', methods=['GET'])
def get_facilities():
    """Get all facilities or filter by CTAS level"""
    try:
        ctas_level = request.args.get('ctas_level', type=int)
        
        if ctas_level:
            facilities = get_facilities_by_ctas(ctas_level)
        else:
            facilities = FACILITIES
        
        return jsonify({
            "success": True,
            "facilities": facilities
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/facilities/<int:facility_id>', methods=['GET'])
def get_facility(facility_id):
    """Get specific facility by ID"""
    try:
        facility = get_facility_by_id(facility_id)
        
        if facility:
            return jsonify({
                "success": True,
                "facility": facility
            })
        else:
            return jsonify({
                "success": False,
                "error": "Facility not found"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/ctas', methods=['GET'])
def get_ctas_info():
    """Get CTAS definitions"""
    return jsonify({
        "success": True,
        "ctas_definitions": CTAS_DEFINITIONS
    })

@api_bp.route('/dashboard/stats', methods=['GET'])
def get_stats():
    """Get dashboard statistics"""
    try:
        total_sessions = len(sessions)
        total_assessments = len(assessments)
        
        # Count by CTAS level
        ctas_distribution = {i: 0 for i in range(1, 6)}
        for assessment in assessments:
            level = assessment.get('ctas_level')
            if level in ctas_distribution:
                ctas_distribution[level] += 1
        
        # Count by care type
        care_type_distribution = {}
        for assessment in assessments:
            care_type = assessment.get('care_type', 'unknown')
            care_type_distribution[care_type] = care_type_distribution.get(care_type, 0) + 1
        
        return jsonify({
            "success": True,
            "stats": {
                "total_sessions": total_sessions,
                "total_assessments": total_assessments,
                "ctas_distribution": ctas_distribution,
                "care_type_distribution": care_type_distribution,
                "timestamp": datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/dashboard/assessments', methods=['GET'])
def get_assessments():
    """Get recent assessments"""
    try:
        limit = request.args.get('limit', 50, type=int)
        recent_assessments = assessments[-limit:]
        recent_assessments.reverse()
        
        return jsonify({
            "success": True,
            "assessments": recent_assessments
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in kilometers"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c


@api_bp.route('/voice/text-to-speech', methods=['POST'])
def convert_text_to_speech():
    """
    Convert text to speech
    
    Request body:
    {
        "text": "النص المراد تحويله إلى صوت",
        "voice": "alloy" (optional),
        "speed": 1.0 (optional)
    }
    """
    try:
        data = request.json
        text = data.get('text')
        voice = data.get('voice', 'alloy')
        speed = data.get('speed', 1.0)
        
        if not text:
            return jsonify({
                "success": False,
                "error": "text is required"
            }), 400
        
        # Import TTS service
        from src.services.text_to_speech import tts_service
        
        # Convert text to speech
        audio_data = tts_service.text_to_speech(text, voice, speed)
        
        if not audio_data:
            return jsonify({
                "success": False,
                "error": "Failed to generate speech"
            }), 500
        
        # Return audio as response
        from flask import Response
        return Response(
            audio_data,
            mimetype='audio/mpeg',
            headers={
                'Content-Disposition': 'attachment; filename=response.mp3'
            }
        )
        
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
