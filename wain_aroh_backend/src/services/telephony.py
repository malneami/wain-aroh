"""
Telephony Service for Voice Call Integration
Handles incoming calls, voice recording, and transcription
"""

from flask import request, Response
from openai import OpenAI
import os
import json
from datetime import datetime

# Initialize OpenAI client
client = OpenAI()

class CallSession:
    """Manages a phone call session"""
    def __init__(self, call_sid):
        self.call_sid = call_sid
        self.conversation_history = []
        self.start_time = datetime.now()
        self.patient_info = {}
        self.assessment = None
        
    def add_message(self, role, content):
        """Add message to conversation history"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

# Store active call sessions
call_sessions = {}

def generate_twiml_response(text, gather_input=True):
    """
    Generate TwiML (Twilio Markup Language) response
    This can be adapted for other telephony providers
    """
    if gather_input:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="ar-SA" voice="woman">{text}</Say>
    <Record 
        maxLength="30" 
        timeout="3"
        transcribe="true"
        transcribeCallback="/api/telephony/transcription"
        action="/api/telephony/process-recording"
        playBeep="true"
    />
</Response>"""
    else:
        return f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="ar-SA" voice="woman">{text}</Say>
    <Hangup/>
</Response>"""

def handle_incoming_call(request_data):
    """
    Handle incoming phone call
    Returns TwiML response to greet the caller
    """
    call_sid = request_data.get('CallSid')
    from_number = request_data.get('From')
    
    # Create new call session
    call_sessions[call_sid] = CallSession(call_sid)
    call_sessions[call_sid].patient_info['phone'] = from_number
    
    # Welcome message in Arabic
    welcome_message = """
    مرحباً بك في خدمة وين أروح للتوجيه الذكي للرعاية الصحية.
    أنا المساعد الصحي الذكي، وسأساعدك في معرفة المركز الصحي المناسب لحالتك.
    من فضلك، صف لي الأعراض التي تعاني منها بعد سماع الصوت.
    """
    
    return generate_twiml_response(welcome_message, gather_input=True)

def process_recording(request_data):
    """
    Process recorded audio from the call
    Transcribe and generate AI response
    """
    call_sid = request_data.get('CallSid')
    recording_url = request_data.get('RecordingUrl')
    
    if call_sid not in call_sessions:
        return generate_twiml_response("عذراً، حدث خطأ. يرجى الاتصال مرة أخرى.", gather_input=False)
    
    session = call_sessions[call_sid]
    
    # In production, you would download and transcribe the recording
    # For now, we'll use a placeholder
    # transcribed_text = transcribe_audio_from_url(recording_url)
    
    # Placeholder response
    response_text = """
    شكراً لك. هل الألم شديد؟ وهل بدأ فجأة أم تدريجياً؟
    من فضلك أجب بعد سماع الصوت.
    """
    
    return generate_twiml_response(response_text, gather_input=True)

def handle_transcription(request_data):
    """
    Handle transcription callback from telephony provider
    Process the transcribed text with AI
    """
    call_sid = request_data.get('CallSid')
    transcription_text = request_data.get('TranscriptionText')
    
    if call_sid not in call_sessions:
        return {"status": "error", "message": "Session not found"}
    
    session = call_sessions[call_sid]
    session.add_message("user", transcription_text)
    
    # Get AI response
    try:
        messages = [
            {"role": "system", "content": """أنت مساعد صحي ذكي في نظام "وين أروح" للتوجيه الطبي.
            مهمتك هي:
            1. الاستماع لأعراض المريض
            2. طرح أسئلة توضيحية
            3. تقييم الحالة حسب نظام CTAS
            4. توجيه المريض للمركز الصحي المناسب
            
            تحدث بلغة عربية واضحة ومختصرة مناسبة للمكالمات الهاتفية."""}
        ]
        
        # Add conversation history
        for msg in session.conversation_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=150
        )
        
        ai_response = response.choices[0].message.content
        session.add_message("assistant", ai_response)
        
        return {
            "status": "success",
            "response": ai_response,
            "session_id": call_sid
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def handle_dtmf_input(request_data):
    """
    Handle DTMF (keypad) input during call
    Useful for menu navigation or confirmations
    """
    call_sid = request_data.get('CallSid')
    digits = request_data.get('Digits')
    
    if digits == '1':
        # Emergency
        response_text = "سيتم توجيهك إلى أقرب قسم طوارئ. ابق على الخط."
    elif digits == '2':
        # UCC
        response_text = "سيتم توجيهك إلى مركز رعاية عاجلة. ابق على الخط."
    elif digits == '3':
        # Clinic
        response_text = "سيتم توجيهك إلى عيادة. ابق على الخط."
    else:
        response_text = "خيار غير صحيح. يرجى المحاولة مرة أخرى."
    
    return generate_twiml_response(response_text, gather_input=False)

def end_call_and_send_sms(call_sid, facility_info):
    """
    End call and send SMS with facility information
    """
    if call_sid not in call_sessions:
        return {"status": "error", "message": "Session not found"}
    
    session = call_sessions[call_sid]
    
    # Generate SMS content
    sms_content = f"""
    وين أروح - توصيتك الصحية
    
    المركز الموصى به: {facility_info['name']}
    العنوان: {facility_info['location']}
    ساعات العمل: {facility_info['hours']}
    الهاتف: {facility_info['phone']}
    
    مستوى الحالة: {facility_info['ctas_level']}
    
    شكراً لاستخدامك خدمة وين أروح
    """
    
    # In production, send SMS via telephony provider
    # send_sms(session.patient_info['phone'], sms_content)
    
    # Save call record
    call_record = {
        "call_sid": call_sid,
        "phone": session.patient_info['phone'],
        "start_time": session.start_time.isoformat(),
        "end_time": datetime.now().isoformat(),
        "conversation": session.conversation_history,
        "assessment": session.assessment,
        "recommended_facility": facility_info
    }
    
    # Clean up session
    del call_sessions[call_sid]
    
    return {
        "status": "success",
        "call_record": call_record
    }

def get_call_recording_url(call_sid, recording_sid):
    """
    Get URL for call recording
    For compliance and quality assurance
    """
    # In production, this would fetch from telephony provider
    return f"https://api.telephony-provider.com/recordings/{recording_sid}"

def transcribe_call_recording(recording_url):
    """
    Transcribe call recording using OpenAI Whisper
    """
    try:
        # Download recording
        # audio_file = download_audio(recording_url)
        
        # Transcribe using Whisper
        # with open(audio_file, "rb") as audio:
        #     transcript = client.audio.transcriptions.create(
        #         model="whisper-1",
        #         file=audio,
        #         language="ar"
        #     )
        
        # return transcript.text
        
        return "Transcription placeholder"
        
    except Exception as e:
        return f"Error transcribing: {str(e)}"

