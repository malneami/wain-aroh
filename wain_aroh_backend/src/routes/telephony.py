"""
Telephony API Routes
Handles webhook endpoints for telephony provider (Twilio, Vonage, etc.)
"""

from flask import Blueprint, request, Response
from src.services.telephony import (
    handle_incoming_call,
    process_recording,
    handle_transcription,
    handle_dtmf_input,
    end_call_and_send_sms
)
import json

telephony_bp = Blueprint('telephony', __name__, url_prefix='/api/telephony')

@telephony_bp.route('/incoming-call', methods=['POST'])
def incoming_call():
    """
    Webhook endpoint for incoming calls
    Called by telephony provider when a call is received
    """
    try:
        request_data = request.form.to_dict() or request.get_json()
        twiml_response = handle_incoming_call(request_data)
        return Response(twiml_response, mimetype='text/xml')
    except Exception as e:
        error_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="ar-SA">عذراً، حدث خطأ. يرجى الاتصال مرة أخرى لاحقاً.</Say>
    <Hangup/>
</Response>"""
        return Response(error_response, mimetype='text/xml')

@telephony_bp.route('/process-recording', methods=['POST'])
def process_recording_endpoint():
    """
    Webhook endpoint for processing recorded audio
    Called after each recording is completed
    """
    try:
        request_data = request.form.to_dict() or request.get_json()
        twiml_response = process_recording(request_data)
        return Response(twiml_response, mimetype='text/xml')
    except Exception as e:
        error_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="ar-SA">عذراً، حدث خطأ في معالجة تسجيلك.</Say>
    <Hangup/>
</Response>"""
        return Response(error_response, mimetype='text/xml')

@telephony_bp.route('/transcription', methods=['POST'])
def transcription_callback():
    """
    Webhook endpoint for transcription results
    Called when transcription is completed by telephony provider
    """
    try:
        request_data = request.form.to_dict() or request.get_json()
        result = handle_transcription(request_data)
        return json.dumps(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }), 500, {'Content-Type': 'application/json'}

@telephony_bp.route('/dtmf-input', methods=['POST'])
def dtmf_input():
    """
    Webhook endpoint for DTMF (keypad) input
    Handles menu selections during call
    """
    try:
        request_data = request.form.to_dict() or request.get_json()
        twiml_response = handle_dtmf_input(request_data)
        return Response(twiml_response, mimetype='text/xml')
    except Exception as e:
        error_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="ar-SA">عذراً، حدث خطأ.</Say>
    <Hangup/>
</Response>"""
        return Response(error_response, mimetype='text/xml')

@telephony_bp.route('/end-call', methods=['POST'])
def end_call():
    """
    Endpoint to end call and send SMS with facility info
    """
    try:
        data = request.get_json()
        call_sid = data.get('call_sid')
        facility_info = data.get('facility_info')
        
        result = end_call_and_send_sms(call_sid, facility_info)
        return json.dumps(result), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }), 500, {'Content-Type': 'application/json'}

@telephony_bp.route('/call-status', methods=['POST'])
def call_status():
    """
    Webhook endpoint for call status updates
    Tracks call lifecycle (ringing, answered, completed, etc.)
    """
    try:
        request_data = request.form.to_dict() or request.get_json()
        call_sid = request_data.get('CallSid')
        call_status = request_data.get('CallStatus')
        
        # Log call status for monitoring
        print(f"Call {call_sid} status: {call_status}")
        
        return json.dumps({
            "status": "received",
            "call_sid": call_sid,
            "call_status": call_status
        }), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }), 500, {'Content-Type': 'application/json'}

@telephony_bp.route('/recordings/<recording_sid>', methods=['GET'])
def get_recording(recording_sid):
    """
    Endpoint to retrieve call recording
    For compliance and quality assurance
    """
    try:
        # In production, fetch recording from telephony provider
        # or from local storage
        return json.dumps({
            "status": "success",
            "recording_sid": recording_sid,
            "recording_url": f"/recordings/{recording_sid}.mp3"
        }), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        }), 404, {'Content-Type': 'application/json'}

@telephony_bp.route('/test-voice', methods=['GET'])
def test_voice():
    """
    Test endpoint to verify TwiML generation
    """
    test_response = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="ar-SA" voice="woman">مرحباً بك في خدمة وين أروح. هذا اختبار للنظام الصوتي.</Say>
</Response>"""
    return Response(test_response, mimetype='text/xml')

