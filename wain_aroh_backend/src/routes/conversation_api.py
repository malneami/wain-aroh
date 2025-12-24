"""
Conversational API Routes for Wain Aroh
Natural dialogue-based patient navigation
"""

from flask import Blueprint, request, jsonify
from src.services.conversational_ai import conversational_ai
import uuid

conversation_api_bp = Blueprint('conversation_api', __name__, url_prefix='/api/conversation')

@conversation_api_bp.route('/start', methods=['POST'])
def start_conversation():
    """Start a new conversation session"""
    try:
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Start conversation
        result = conversational_ai.start_conversation(session_id)
        
        return jsonify({
            'success': True,
            **result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@conversation_api_bp.route('/message', methods=['POST'])
def send_message():
    """Send a message in an ongoing conversation"""
    try:
        data = request.json
        
        session_id = data.get('session_id')
        message = data.get('message')
        gps_data = data.get('gps_data')
        
        if not session_id or not message:
            return jsonify({
                'success': False,
                'error': 'Session ID and message required'
            }), 400
        
        # Process message
        result = conversational_ai.process_message(
            session_id=session_id,
            user_message=message,
            gps_data=gps_data
        )
        
        return jsonify({
            'success': True,
            **result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@conversation_api_bp.route('/location', methods=['POST'])
def provide_location():
    """Provide GPS location during conversation"""
    try:
        data = request.json
        
        session_id = data.get('session_id')
        gps_data = data.get('gps_data')
        
        if not session_id or not gps_data:
            return jsonify({
                'success': False,
                'error': 'Session ID and GPS data required'
            }), 400
        
        # Process with location
        result = conversational_ai.process_message(
            session_id=session_id,
            user_message="[مشاركة الموقع]",
            gps_data=gps_data
        )
        
        return jsonify({
            'success': True,
            **result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@conversation_api_bp.route('/booking/search', methods=['POST'])
def search_booking():
    """Search for appointment slots during conversation"""
    try:
        data = request.json
        
        session_id = data.get('session_id')
        specialty = data.get('specialty')
        preferred_date = data.get('preferred_date')
        
        if not session_id or not specialty:
            return jsonify({
                'success': False,
                'error': 'Session ID and specialty required'
            }), 400
        
        # Handle booking request
        result = conversational_ai.handle_booking_request(
            session_id=session_id,
            specialty=specialty,
            preferred_date=preferred_date
        )
        
        return jsonify({
            'success': True,
            **result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@conversation_api_bp.route('/booking/confirm', methods=['POST'])
def confirm_booking():
    """Confirm appointment booking"""
    try:
        data = request.json
        
        session_id = data.get('session_id')
        slot_index = data.get('slot_index')
        patient_name = data.get('patient_name')
        patient_phone = data.get('patient_phone')
        
        if not all([session_id, slot_index is not None, patient_name, patient_phone]):
            return jsonify({
                'success': False,
                'error': 'All booking details required'
            }), 400
        
        # Confirm booking
        result = conversational_ai.confirm_booking(
            session_id=session_id,
            slot_index=slot_index,
            patient_name=patient_name,
            patient_phone=patient_phone
        )
        
        return jsonify({
            'success': True,
            **result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@conversation_api_bp.route('/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    try:
        session_id = request.args.get('session_id')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required'
            }), 400
        
        # Get history
        history = conversational_ai.get_conversation_history(session_id)
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'messages': history
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@conversation_api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'Wain Aroh Conversational API',
        'version': '1.0',
        'features': [
            'Natural Arabic conversation',
            'Intelligent symptom assessment',
            'Conversational location request',
            'Facility recommendation',
            'Appointment booking',
            'Multi-turn dialogue'
        ]
    })



@conversation_api_bp.route('/upload', methods=['POST'])
def upload_file():
    """Upload and analyze medical file"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        session_id = request.form.get('session_id')
        context = request.form.get('context', '')
        
        if not session_id:
            return jsonify({
                'success': False,
                'error': 'Session ID required'
            }), 400
        
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Import file analyzer
        from src.services.file_analyzer import file_analyzer
        
        # Check if file type is supported
        mime_type = file.content_type
        is_supported, file_type = file_analyzer.is_supported(mime_type)
        
        if not is_supported:
            return jsonify({
                'success': False,
                'error': f'نوع الملف غير مدعوم. الأنواع المدعومة: صور (JPG, PNG), PDF',
                'supported_types': list(file_analyzer.supported_types.keys())
            }), 400
        
        # Save file
        file_path = file_analyzer.save_file(file, session_id)
        
        if not file_path:
            return jsonify({
                'success': False,
                'error': 'Failed to save file'
            }), 500
        
        # Analyze file
        analysis_result = file_analyzer.analyze_file(file_path, file_type, context)
        
        if not analysis_result['success']:
            return jsonify({
                'success': False,
                'error': analysis_result.get('error', 'Failed to analyze file')
            }), 500
        
        # Format message
        message = file_analyzer.format_analysis_message(analysis_result, file.filename)
        
        # Add to conversation context
        conversational_ai.add_file_analysis_to_context(session_id, message, file.filename)
        
        return jsonify({
            'success': True,
            'message': message,
            'file_type': file_type,
            'filename': file.filename,
            'analysis': analysis_result.get('analysis')
        })
    
    except Exception as e:
        print(f"Error uploading file: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

