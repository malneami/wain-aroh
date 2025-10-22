import os
import json
from openai import OpenAI
from src.data.facilities import CTAS_DEFINITIONS, get_facilities_by_ctas, get_recommended_care_type

# Initialize OpenAI client (API key is already configured in environment)
client = OpenAI()

TRIAGE_SYSTEM_PROMPT = """أنت مساعد طبي ذكي متخصص في تقييم الحالات الصحية وتوجيه المرضى إلى الجهة الصحية المناسبة.

مهمتك:
1. التحدث مع المريض بلطف واحترافية باللغة العربية
2. طرح أسئلة واضحة لفهم الأعراض
3. تقييم خطورة الحالة حسب نظام CTAS (1-5)
4. التوصية بالجهة الصحية المناسبة

معايير تصنيف CTAS:
- المستوى 1 (إنعاش): حالات تهدد الحياة فوراً - قسم الطوارئ
- المستوى 2 (طارئ): حالات خطيرة تحتاج رعاية عاجلة - قسم الطوارئ
- المستوى 3 (عاجل): حالات تحتاج رعاية سريعة - مركز الرعاية العاجلة
- المستوى 4 (أقل عجلة): حالات يمكن معالجتها في العيادات - مركز صحي
- المستوى 5 (غير عاجل): حالات روتينية - عيادة افتراضية

إرشادات:
- كن متعاطفاً ومطمئناً
- اطرح أسئلة محددة عن الأعراض والمدة والشدة
- لا تقدم تشخيصاً طبياً، فقط وجه للجهة المناسبة
- في حالات الطوارئ، أكد على ضرورة التوجه الفوري

عند الانتهاء من التقييم، قدم:
1. مستوى CTAS (رقم من 1-5)
2. نوع الرعاية الموصى بها
3. ملخص قصير للحالة
"""

def chat_with_ai(messages, session_data=None):
    """
    Chat with AI assistant for triage
    
    Args:
        messages: List of conversation messages
        session_data: Optional session data for context
    
    Returns:
        dict with response and assessment if available
    """
    try:
        # Add system prompt
        full_messages = [
            {"role": "system", "content": TRIAGE_SYSTEM_PROMPT}
        ] + messages
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=full_messages,
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_message = response.choices[0].message.content
        
        # Try to extract CTAS assessment if mentioned
        assessment = extract_assessment(assistant_message)
        
        return {
            "success": True,
            "message": assistant_message,
            "assessment": assessment
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "عذراً، حدث خطأ. يرجى المحاولة مرة أخرى."
        }

def extract_assessment(text):
    """
    Extract CTAS assessment from AI response
    
    Args:
        text: AI response text
    
    Returns:
        dict with CTAS level and recommendation, or None
    """
    # Look for CTAS level mentions
    for level in range(1, 6):
        if f"المستوى {level}" in text or f"CTAS {level}" in text or f"مستوى {level}" in text:
            care_type = get_recommended_care_type(level)
            return {
                "ctas_level": level,
                "care_type": care_type,
                "ctas_info": CTAS_DEFINITIONS[level]
            }
    
    return None

def analyze_symptoms(symptoms_text):
    """
    Analyze symptoms and provide CTAS assessment
    
    Args:
        symptoms_text: Patient's description of symptoms
    
    Returns:
        dict with assessment results
    """
    try:
        prompt = f"""قم بتحليل الأعراض التالية وتحديد مستوى CTAS المناسب:

الأعراض: {symptoms_text}

قدم تقييمك في صيغة JSON:
{{
    "ctas_level": <رقم من 1-5>,
    "severity": "<منخفض/متوسط/عالي/حرج>",
    "reasoning": "<سبب التصنيف>",
    "urgent_keywords": [<كلمات مفتاحية تدل على الخطورة>]
}}
"""
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": TRIAGE_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        ctas_level = result.get("ctas_level", 5)
        
        # Get facilities and care type
        care_type = get_recommended_care_type(ctas_level)
        facilities = get_facilities_by_ctas(ctas_level)
        
        return {
            "success": True,
            "ctas_level": ctas_level,
            "ctas_info": CTAS_DEFINITIONS[ctas_level],
            "severity": result.get("severity"),
            "reasoning": result.get("reasoning"),
            "care_type": care_type,
            "recommended_facilities": facilities[:3]  # Top 3 facilities
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def transcribe_audio(audio_file_path):
    """
    Transcribe audio to text using OpenAI Whisper
    
    Args:
        audio_file_path: Path to audio file
    
    Returns:
        dict with transcription result
    """
    try:
        with open(audio_file_path, 'rb') as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ar"
            )
        
        return {
            "success": True,
            "text": transcript.text
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def text_to_speech(text, output_path):
    """
    Convert text to speech using OpenAI TTS
    
    Args:
        text: Text to convert
        output_path: Path to save audio file
    
    Returns:
        dict with result
    """
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        
        response.stream_to_file(output_path)
        
        return {
            "success": True,
            "audio_path": output_path
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

