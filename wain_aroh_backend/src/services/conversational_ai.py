"""
Conversational AI for Wain Aroh
Natural dialogue-based interaction for patient navigation
"""

from openai import OpenAI
import json
from datetime import datetime
from services.location_service import location_service
from services.agentic_ai import agentic_ai
from services.location_detector import location_detector
from data.facilities_ngh import get_main_hospital
from services.recommendation_generator import generate_recommendations, format_recommendations_response

client = OpenAI()

class ConversationalAI:
    """
    Handles natural conversation with patients to:
    1. Understand their symptoms and needs
    2. Ask for location naturally
    3. Perform triage assessment
    4. Recommend appropriate facility
    5. Book appointments if needed
    6. Guide patient through the entire process
    """
    
    def __init__(self):
        self.conversation_state = {}
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self):
        """Build comprehensive system prompt for conversational AI"""
        return """أنت مساعد طبي ذكي لمستشفى الحرس الوطني بالرياض. اسمك "وين أروح".

**مهمتك الرئيسية:**
توجيه المرضى للمكان الصحيح بناءً على حالتهم الصحية.

**أسلوب المحادثة:**
- تحدث بالعربية الفصحى البسيطة
- كن ودوداً ومطمئناً
- اسأل أسئلة واضحة ومباشرة
- لا تستخدم مصطلحات طبية معقدة
- كن متعاطفاً مع المريض

**خطوات المحادثة:**

1. **الترحيب والسؤال عن الحالة:**
   - ابدأ بالترحيب
   - اسأل: "كيف يمكنني مساعدتك؟" أو "ما الذي تشعر به؟"

2. **جمع المعلومات عن الأعراض:**
   - اسأل عن الأعراض بالتفصيل
   - متى بدأت الأعراض؟
   - ما شدة الألم (1-10)؟
   - هل هناك أعراض أخرى؟
   - هل حدث فجأة أم تدريجياً؟

3. **السؤال عن الموقع بشكل طبيعي:**
   - بعد فهم الحالة، اسأل: "أين أنت الآن؟" أو "في أي حي تسكن؟"
   - إذا لم يعرف، اقترح: "هل يمكنك مشاركة موقعك الحالي لأساعدك في إيجاد أقرب مركز؟"
   - اشرح: "سأستخدم موقعك فقط لتوجيهك لأقرب مركز رعاية مناسب"

4. **تقييم الحالة (CTAS):**
   - حدد مستوى الخطورة:
     * CTAS 1: حالة حرجة جداً (فقدان وعي، ألم صدر شديد مع ضيق تنفس، نزيف حاد)
     * CTAS 2: حالة طارئة (ألم صدر شديد، كسور، حمى عالية مع أعراض خطيرة)
     * CTAS 3: حالة عاجلة (آلام متوسطة، حمى، إصابات بسيطة)
     * CTAS 4: حالة أقل إلحاحاً (أعراض خفيفة، يمكن الانتظار)
     * CTAS 5: حالة غير عاجلة (فحص دوري، استشارة عامة)

5. **التوجيه للمكان المناسب (فقط بعد التقييم الكامل):**
   - لا تقدم التوصيات في بداية المحادثة
   - اجمع المعلومات الكافية أولاً (الأعراض، الشدة، المدة، الموقع)
   - بعد التقييم الكامل، قدم التوصيات:
     * CTAS 1-2: طوارئ مستشفى الحرس الوطني الرئيسي
     * CTAS 3: مركز رعاية عاجلة (UCC) إذا كان قريباً
     * CTAS 4-5: عيادة أو عيادة افتراضية

6. **تقديم التفاصيل:**
   - اسم المنشأة
   - العنوان
   - المسافة والوقت المتوقع
   - رقم الهاتف
   - رابط الخريطة

7. **حجز موعد إذا لزم الأمر:**
   - للحالات غير العاجلة (CTAS 4-5)
   - اسأل: "هل تريد حجز موعد؟"
   - اجمع المعلومات: الاسم، رقم الجوال، التاريخ المفضل
   - احجز وأكد الموعد

8. **الختام:**
   - اسأل: "هل هناك شيء آخر يمكنني مساعدتك فيه؟"
   - قدم نصائح إضافية إذا لزم الأمر
   - تمنى له السلامة

**معلومات مهمة:**

**المستشفى الرئيسي:**
- الاسم: مستشفى الحرس الوطني - الرياض
- الموقع: طريق الملك عبدالعزيز، حي الملقا
- الطوارئ: 937
- متاح: 24/7

**مراكز الرعاية العاجلة (UCC):**
1. مركز الملقا (1.2 كم من المستشفى الرئيسي)
2. مركز النخيل (3.5 كم)
3. مركز العليا (8.2 كم)
4. مركز الربوة (5.8 كم)

**العيادات:**
- عيادات الملقا (8 ص - 8 م)
- عيادات العليا (8 ص - 8 م)

**العيادات الافتراضية:**
- متاحة 24/7
- استشارات عن بعد

**حالات الطوارئ:**
- إذا كانت الحالة حرجة جداً، انصح بالاتصال بالإسعاف 997
- للحالات الطارئة، وجه للطوارئ مباشرة

**ملاحظات:**
- لا تقدم تشخيصاً طبياً
- لا تصف أدوية
- ركز على التوجيه للمكان المناسب
- كن حذراً مع الحالات الحرجة

**أمثلة على الأسئلة:**
- "ما الذي تشعر به؟"
- "متى بدأت هذه الأعراض؟"
- "هل الألم شديد؟ من 1 إلى 10، كم تقيمه؟"
- "هل هناك أعراض أخرى مثل حمى أو غثيان؟"
- "أين أنت الآن؟ في أي حي؟"
- "هل يمكنك مشاركة موقعك لأساعدك في إيجاد أقرب مركز؟"
- "هل تريد حجز موعد في العيادة؟"

**تذكر:**
أنت تساعد المرضى في اتخاذ القرار الصحيح حول المكان الذي يجب أن يذهبوا إليه.
كن واضحاً، ودوداً، ومطمئناً.
"""
    
    def start_conversation(self, session_id):
        """Start a new conversation"""
        self.conversation_state[session_id] = {
            'messages': [],
            'patient_data': {},
            'location': None,
            'ctas_level': None,
            'symptoms': [],
            'stage': 'greeting',  # greeting, symptoms, location, triage, recommendation, booking, closing
            'location_requested': False,
            'location_provided': False
        }
         # Generate welcome message with location request
        welcome_message = """مرحباً بك في خدمة "وين أروح" 👋

أنا هنا لمساعدتك في معرفة المكان المناسب للرعاية الصحية.

كيف يمكنني مساعدتك اليوم؟ ما الذي تشعر به؟"""  
        self.conversation_state[session_id]['messages'].append({
            'role': 'assistant',
            'content': welcome_message
        })
        
        return {
            'session_id': session_id,
            'message': welcome_message,
            'stage': 'greeting'
        }
    
    def process_message(self, session_id, user_message, gps_data=None):
        """Process user message and generate response"""
        
        if session_id not in self.conversation_state:
            self.start_conversation(session_id)
        
        state = self.conversation_state[session_id]
        
        # Add user message to conversation
        state['messages'].append({
            'role': 'user',
            'content': user_message
        })
        
        # Process GPS data if provided
        if gps_data:
            state['location'] = location_service.get_patient_location(gps_data)
            state['location_provided'] = True
        
        # Build conversation context
        messages = [
            {'role': 'system', 'content': self.system_prompt}
        ] + state['messages']
        
        # Add context about current stage
        if state['stage'] == 'symptoms' and not state['location_provided']:
            messages.append({
                'role': 'system',
                'content': 'ملاحظة: بعد جمع معلومات كافية عن الأعراض، اسأل المريض عن موقعه الحالي بشكل طبيعي.'
            })
        
        # Call GPT-4 for response
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to conversation
        state['messages'].append({
            'role': 'assistant',
            'content': assistant_message
        })
        
        # Analyze conversation to determine stage and actions
        analysis = self._analyze_conversation(state)
        
        # Update state based on analysis
        state['stage'] = analysis['stage']
        state['ctas_level'] = analysis.get('ctas_level', state['ctas_level'])
        state['symptoms'] = analysis.get('symptoms', state['symptoms'])
        
        # Check if we should request location
        should_request_location = (
            analysis['stage'] in ['location', 'triage'] and
            not state['location_provided'] and
            not state['location_requested']
        )
        
        # Try to detect location from text if not provided
        if should_request_location and not state['location']:
            text_location = location_detector.detect_location_from_text(user_message)
            if text_location.get('detected'):
                state['location'] = {
                    'latitude': text_location['latitude'],
                    'longitude': text_location['longitude']
                }
                state['location_provided'] = True
                
                # Add confirmation message
                confirmation = location_detector.format_location_confirmation(text_location)
                state['messages'].append({
                    'role': 'system',
                    'content': confirmation
                })
                response_data['location_confirmation'] = confirmation
        
        # Generate response with actions
        response_data = {
            'session_id': session_id,
            'message': assistant_message,
            'stage': state['stage'],
            'request_location': should_request_location
        }
        
        if should_request_location and not state['location_provided']:
            state['location_requested'] = True
            
            # Generate contextual location request
            location_request = location_detector.request_location_with_context(
                state.get('ctas_level', 3),
                state.get('symptoms', [])
            )
            response_data['location_request_details'] = location_request
        
        # If we have location and CTAS, provide recommendation
        if state['location'] and state['ctas_level']:
            # Get detailed recommendation with alternatives
            detailed_recommendation = location_detector.find_nearest_facility_for_patient(
                state['location'],
                state['ctas_level']
            )
            
            response_data['recommendation'] = detailed_recommendation['primary_recommendation']
            response_data['alternatives'] = detailed_recommendation['alternatives']
            
            # Format detailed facility message
            facility_message = location_detector.format_facility_recommendation_detailed(
                detailed_recommendation,
                state['ctas_level']
            )
            
            state['messages'].append({
                'role': 'assistant',
                'content': facility_message
            })
            response_data['facility_message'] = facility_message
            
            # Cache location for session
            location_detector.update_location_cache(session_id, state['location'])
        
        # Check if patient wants to book appointment
        if analysis.get('wants_booking') and state['ctas_level'] and state['ctas_level'] >= 4:
            response_data['offer_booking'] = True
        
        # Generate interactive recommendations ONLY after complete assessment
        # Check if we have: symptoms, location, and CTAS level
        if (state.get('symptoms') and len(state['symptoms']) > 0 and 
            state.get('location') and state.get('ctas_level')):
            symptoms_text = ' '.join(state['symptoms'])
            recommendations = generate_recommendations(
                assistant_message,
                symptoms_text,
                session_id,
                state['ctas_level'],
                state['location']
            )
            response_data['recommendations'] = recommendations
            response_data['show_recommendations'] = True
        
        return response_data
    
    def _analyze_conversation(self, state):
        """Analyze conversation to determine stage and extract information"""
        
        # Get last few messages
        recent_messages = state['messages'][-6:]
        conversation_text = '\n'.join([
            f"{msg['role']}: {msg['content']}" 
            for msg in recent_messages
        ])
        
        # Use GPT to analyze
        analysis_prompt = f"""حلل المحادثة التالية واستخرج:
1. المرحلة الحالية (greeting, symptoms, location, triage, recommendation, booking, closing)
2. مستوى CTAS (1-5) إذا كان واضحاً
3. الأعراض المذكورة
4. هل المريض يريد حجز موعد؟

المحادثة:
{conversation_text}

أجب بصيغة JSON فقط:
{{
    "stage": "...",
    "ctas_level": 3,
    "symptoms": ["...", "..."],
    "wants_booking": false
}}
"""
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {'role': 'user', 'content': analysis_prompt}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            analysis_text = response.choices[0].message.content
            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', analysis_text, re.DOTALL)
            if json_match:
                analysis = json.loads(json_match.group())
                return analysis
        except:
            pass
        
        # Fallback analysis
        return {
            'stage': state['stage'],
            'ctas_level': state['ctas_level'],
            'symptoms': state['symptoms'],
            'wants_booking': False
        }
    
    def _format_facility_message(self, recommendation, patient_location):
        """Format facility recommendation as conversational message"""
        
        facility = recommendation['facility']
        reason = recommendation['reason']
        distance = recommendation.get('distance_km')
        travel_time = recommendation.get('estimated_travel_time_minutes')
        
        message = f"""بناءً على حالتك، أنصحك بـ:

📍 **{facility['name']}**

{reason}

**التفاصيل:**
📌 العنوان: {facility['location']}
📞 الهاتف: {facility['phone']}
⏰ ساعات العمل: {facility['hours']}
"""
        
        if distance:
            message += f"🚗 المسافة: {distance:.1f} كم\n"
        
        if travel_time:
            message += f"⏱️ الوقت المتوقع للوصول: {travel_time} دقيقة\n"
        
        if facility.get('wait_time_minutes'):
            message += f"⏳ وقت الانتظار المتوقع: {facility['wait_time_minutes']} دقيقة\n"
        
        # Add directions link
        if patient_location:
            directions_url = location_service.get_directions_url(patient_location, facility)
            message += f"\n🗺️ [اضغط هنا للحصول على الاتجاهات]({directions_url})\n"
        
        # Add special instructions
        if facility.get('is_main_hub'):
            message += "\n⚠️ **تعليمات مهمة:**\n"
            message += "- توجه مباشرة إلى قسم الطوارئ\n"
            message += "- أحضر بطاقة الهوية وبطاقة التأمين\n"
            message += "- إذا كانت حالتك حرجة، اتصل بالإسعاف 997\n"
        
        message += "\nهل هناك شيء آخر يمكنني مساعدتك فيه؟"
        
        return message
    
    def handle_booking_request(self, session_id, specialty, preferred_date=None):
        """Handle appointment booking through conversation"""
        
        state = self.conversation_state.get(session_id)
        if not state:
            return {'error': 'Session not found'}
        
        # Search for appointments
        result = agentic_ai.search_available_appointments(
            specialty=specialty,
            preferred_date=preferred_date
        )
        
        if result['success'] and result['available_slots']:
            slots = result['available_slots'][:5]  # Show first 5
            
            message = f"وجدت {len(slots)} موعد متاح:\n\n"
            
            for i, slot in enumerate(slots, 1):
                message += f"{i}. {slot['date']} - {slot['time']} في {slot['clinic_name']}\n"
            
            message += "\nأي موعد تفضل؟ (اختر الرقم)"
            
            state['booking_slots'] = slots
            state['stage'] = 'booking'
            
            return {
                'session_id': session_id,
                'message': message,
                'slots': slots
            }
        else:
            return {
                'session_id': session_id,
                'message': 'عذراً، لا توجد مواعيد متاحة حالياً. هل تريد المحاولة بتاريخ آخر؟'
            }
    
    def confirm_booking(self, session_id, slot_index, patient_name, patient_phone):
        """Confirm appointment booking"""
        
        state = self.conversation_state.get(session_id)
        if not state or 'booking_slots' not in state:
            return {'error': 'No booking in progress'}
        
        slots = state['booking_slots']
        if slot_index < 0 or slot_index >= len(slots):
            return {'error': 'Invalid slot selection'}
        
        selected_slot = slots[slot_index]
        
        # Book appointment
        result = agentic_ai.book_appointment(
            clinic_id=selected_slot['clinic_id'],
            specialty=selected_slot['specialty'],
            appointment_datetime=selected_slot['datetime'],
            patient_name=patient_name,
            patient_phone=patient_phone
        )
        
        if result['success']:
            state['stage'] = 'closing'
            return {
                'session_id': session_id,
                'message': result['confirmation_message'],
                'booking': result['booking']
            }
        else:
            return {
                'session_id': session_id,
                'message': 'عذراً، حدث خطأ في الحجز. يرجى المحاولة مرة أخرى.',
                'error': result.get('error')
            }
    
    def get_conversation_history(self, session_id):
        """Get conversation history"""
        state = self.conversation_state.get(session_id)
        if not state:
            return []
        
        return state['messages']

    def add_file_analysis_to_context(self, session_id, analysis_message, filename):
        """Add file analysis to conversation context"""
        if session_id not in self.conversation_state:
            return
        
        state = self.conversation_state[session_id]
        
        # Add file analysis as system message
        state['messages'].append({
            'role': 'system',
            'content': f"تم رفع ملف: {filename}\n\n{analysis_message}"
        })
        
        # Add to patient data
        if 'uploaded_files' not in state['patient_data']:
            state['patient_data']['uploaded_files'] = []
        
        state['patient_data']['uploaded_files'].append({
            'filename': filename,
            'analysis': analysis_message,
            'timestamp': datetime.now().isoformat()
        })


# Initialize conversational AI
conversational_ai = ConversationalAI()
