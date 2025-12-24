"""
Agentic AI System for Wain Aroh
- Automated OPD booking
- Best center search
- Patient reallocation
- Intelligent decision making
"""

from openai import OpenAI
import json
from datetime import datetime, timedelta
from src.data.facilities_ngh import FACILITIES, get_clinics, get_virtual_opd, get_main_hospital

client = OpenAI()

class AgenticAI:
    """
    Autonomous AI agent that can:
    1. Book OPD appointments
    2. Search for best medical centers
    3. Reallocate patients to suitable emergency centers
    4. Make intelligent decisions based on patient needs
    """
    
    def __init__(self):
        self.tools = self._define_tools()
        self.conversation_history = []
    
    def _define_tools(self):
        """Define available tools for the AI agent"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "search_available_appointments",
                    "description": "Search for available appointment slots at clinics",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "specialty": {
                                "type": "string",
                                "description": "Medical specialty (e.g., 'طب عام', 'باطنية', 'أطفال')"
                            },
                            "preferred_date": {
                                "type": "string",
                                "description": "Preferred date in YYYY-MM-DD format"
                            },
                            "preferred_time": {
                                "type": "string",
                                "description": "Preferred time period ('morning', 'afternoon', 'evening')"
                            },
                            "clinic_id": {
                                "type": "integer",
                                "description": "Specific clinic ID if patient has preference"
                            }
                        },
                        "required": ["specialty"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "book_appointment",
                    "description": "Book an appointment at a clinic",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "clinic_id": {
                                "type": "integer",
                                "description": "Clinic ID"
                            },
                            "specialty": {
                                "type": "string",
                                "description": "Medical specialty"
                            },
                            "appointment_datetime": {
                                "type": "string",
                                "description": "Appointment date and time in ISO format"
                            },
                            "patient_name": {
                                "type": "string",
                                "description": "Patient full name"
                            },
                            "patient_phone": {
                                "type": "string",
                                "description": "Patient phone number"
                            },
                            "reason": {
                                "type": "string",
                                "description": "Reason for visit"
                            }
                        },
                        "required": ["clinic_id", "specialty", "appointment_datetime", "patient_name", "patient_phone"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_best_center",
                    "description": "Search for the best medical center based on patient needs",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "condition": {
                                "type": "string",
                                "description": "Medical condition or symptoms"
                            },
                            "urgency_level": {
                                "type": "string",
                                "enum": ["emergency", "urgent", "routine"],
                                "description": "Level of urgency"
                            },
                            "patient_location": {
                                "type": "object",
                                "properties": {
                                    "latitude": {"type": "number"},
                                    "longitude": {"type": "number"}
                                }
                            },
                            "preferences": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Patient preferences (e.g., 'short_wait', 'specialized_care', 'nearby')"
                            }
                        },
                        "required": ["condition", "urgency_level"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "reallocate_patient",
                    "description": "Reallocate patient to a more suitable emergency center based on capacity and specialization",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "current_facility_id": {
                                "type": "integer",
                                "description": "Current facility ID"
                            },
                            "patient_condition": {
                                "type": "string",
                                "description": "Patient's medical condition"
                            },
                            "ctas_level": {
                                "type": "integer",
                                "description": "CTAS triage level (1-5)"
                            },
                            "required_specialty": {
                                "type": "string",
                                "description": "Required medical specialty"
                            },
                            "patient_location": {
                                "type": "object",
                                "properties": {
                                    "latitude": {"type": "number"},
                                    "longitude": {"type": "number"}
                                }
                            }
                        },
                        "required": ["patient_condition", "ctas_level"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "check_facility_capacity",
                    "description": "Check current capacity and wait times at facilities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "facility_ids": {
                                "type": "array",
                                "items": {"type": "integer"},
                                "description": "List of facility IDs to check"
                            },
                            "facility_type": {
                                "type": "string",
                                "enum": ["emergency", "ucc", "clinic"],
                                "description": "Type of facility"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_sms_notification",
                    "description": "Send SMS notification to patient with appointment or facility details",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "phone_number": {
                                "type": "string",
                                "description": "Patient phone number"
                            },
                            "message_type": {
                                "type": "string",
                                "enum": ["appointment_confirmation", "facility_directions", "wait_time_update"],
                                "description": "Type of SMS message"
                            },
                            "details": {
                                "type": "object",
                                "description": "Details to include in SMS"
                            }
                        },
                        "required": ["phone_number", "message_type"]
                    }
                }
            }
        ]
    
    # Tool implementations
    
    def search_available_appointments(self, specialty, preferred_date=None, preferred_time=None, clinic_id=None):
        """Search for available appointments"""
        
        # Get clinics that offer this specialty
        clinics = get_clinics()
        
        if clinic_id:
            clinics = [c for c in clinics if c['id'] == clinic_id]
        
        # Filter by specialty
        suitable_clinics = [
            c for c in clinics 
            if specialty in c.get('specialties', []) or 'طب عام' in c.get('specialties', [])
        ]
        
        # Generate available slots (mock data - in production, connect to real booking system)
        if not preferred_date:
            preferred_date = datetime.now().date()
        else:
            preferred_date = datetime.fromisoformat(preferred_date).date()
        
        available_slots = []
        
        for clinic in suitable_clinics:
            # Generate slots for next 7 days
            for day_offset in range(7):
                date = preferred_date + timedelta(days=day_offset)
                
                # Skip weekends (Friday-Saturday in Saudi Arabia)
                if date.weekday() in [4, 5]:
                    continue
                
                # Generate time slots
                time_slots = []
                if not preferred_time or preferred_time == 'morning':
                    time_slots.extend(['08:00', '09:00', '10:00', '11:00'])
                if not preferred_time or preferred_time == 'afternoon':
                    time_slots.extend(['13:00', '14:00', '15:00', '16:00'])
                if not preferred_time or preferred_time == 'evening':
                    time_slots.extend(['17:00', '18:00', '19:00'])
                
                for time_slot in time_slots:
                    available_slots.append({
                        'clinic_id': clinic['id'],
                        'clinic_name': clinic['name'],
                        'specialty': specialty,
                        'date': str(date),
                        'time': time_slot,
                        'datetime': f"{date}T{time_slot}:00",
                        'doctor': f"د. محمد أحمد",  # Mock doctor name
                        'available': True
                    })
        
        return {
            'success': True,
            'available_slots': available_slots[:20],  # Return first 20 slots
            'total_found': len(available_slots)
        }
    
    def book_appointment(self, clinic_id, specialty, appointment_datetime, patient_name, patient_phone, reason=""):
        """Book an appointment"""
        
        # Find clinic
        clinic = next((f for f in FACILITIES if f['id'] == clinic_id), None)
        
        if not clinic:
            return {
                'success': False,
                'error': 'Clinic not found'
            }
        
        # Parse datetime
        appointment_dt = datetime.fromisoformat(appointment_datetime)
        
        # Create booking (mock - in production, save to database)
        booking = {
            'booking_id': f"APT{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'clinic_id': clinic_id,
            'clinic_name': clinic['name'],
            'specialty': specialty,
            'appointment_datetime': appointment_datetime,
            'patient_name': patient_name,
            'patient_phone': patient_phone,
            'reason': reason,
            'status': 'confirmed',
            'created_at': datetime.now().isoformat()
        }
        
        # Generate confirmation message
        confirmation_message = f"""
✅ **تم تأكيد الموعد**

**رقم الحجز:** {booking['booking_id']}

**المريض:** {patient_name}
**العيادة:** {clinic['name']}
**التخصص:** {specialty}
**التاريخ:** {appointment_dt.strftime('%Y-%m-%d')}
**الوقت:** {appointment_dt.strftime('%H:%M')}

**العنوان:** {clinic['location']}
**الهاتف:** {clinic['phone']}

**تعليمات:**
- يرجى الحضور قبل 15 دقيقة من الموعد
- أحضر بطاقة الهوية وبطاقة التأمين
- أحضر أي تقارير طبية سابقة

لإلغاء أو تعديل الموعد، اتصل على: {clinic['phone']}
"""
        
        return {
            'success': True,
            'booking': booking,
            'confirmation_message': confirmation_message
        }
    
    def search_best_center(self, condition, urgency_level, patient_location=None, preferences=None):
        """Search for best medical center"""
        
        from src.services.location_service import location_service
        
        # Map urgency to CTAS
        urgency_to_ctas = {
            'emergency': 2,
            'urgent': 3,
            'routine': 5
        }
        ctas_level = urgency_to_ctas.get(urgency_level, 3)
        
        # Find best facility
        if patient_location:
            recommendation = location_service.find_best_facility(
                patient_location, 
                ctas_level
            )
        else:
            # Default to main hospital
            recommendation = {
                'facility': get_main_hospital(),
                'reason': 'المستشفى الرئيسي - مستشفى الحرس الوطني'
            }
        
        # Get all nearby options
        if patient_location:
            all_options = location_service.get_all_nearby_options(
                patient_location, 
                ctas_level
            )
        else:
            all_options = []
        
        return {
            'success': True,
            'best_center': recommendation['facility'],
            'reason': recommendation['reason'],
            'all_options': all_options[:5],  # Top 5 options
            'urgency_level': urgency_level,
            'ctas_level': ctas_level
        }
    
    def reallocate_patient(self, patient_condition, ctas_level, current_facility_id=None, 
                          required_specialty=None, patient_location=None):
        """Reallocate patient to more suitable facility"""
        
        from src.services.location_service import location_service
        
        # Determine best facility based on condition and CTAS
        if ctas_level <= 2:
            # Critical - always main hospital
            target_facility = get_main_hospital()
            reason = "حالة حرجة - يجب التحويل لطوارئ مستشفى الحرس الوطني الرئيسي"
            
        elif ctas_level == 3:
            # Urgent - UCC or main hospital
            if patient_location:
                recommendation = location_service.find_best_facility(
                    patient_location, 
                    ctas_level
                )
                target_facility = recommendation['facility']
                reason = recommendation['reason']
            else:
                target_facility = get_main_hospital()
                reason = "حالة عاجلة - التحويل لمستشفى الحرس الوطني"
        
        else:
            # Less urgent - clinic or UCC
            if patient_location:
                recommendation = location_service.find_best_facility(
                    patient_location, 
                    ctas_level,
                    preferred_type='clinic'
                )
                target_facility = recommendation['facility']
                reason = recommendation['reason']
            else:
                clinics = get_clinics()
                target_facility = clinics[0] if clinics else get_main_hospital()
                reason = "يمكن التحويل للعيادات الخارجية"
        
        # Generate transfer instructions
        transfer_instructions = f"""
🔄 **تحويل المريض**

**السبب:** {reason}

**المنشأة المستهدفة:** {target_facility['name']}
**العنوان:** {target_facility['location']}
**الهاتف:** {target_facility['phone']}

**الحالة:** {patient_condition}
**مستوى CTAS:** {ctas_level}
"""
        
        if required_specialty:
            transfer_instructions += f"**التخصص المطلوب:** {required_specialty}\n"
        
        if patient_location:
            directions_url = location_service.get_directions_url(patient_location, target_facility)
            transfer_instructions += f"\n🗺️ [الاتجاهات]({directions_url})\n"
        
        return {
            'success': True,
            'target_facility': target_facility,
            'reason': reason,
            'transfer_instructions': transfer_instructions,
            'estimated_transfer_time': location_service.estimate_travel_time(
                target_facility.get('distance_km')
            ) if patient_location else None
        }
    
    def check_facility_capacity(self, facility_ids=None, facility_type=None):
        """Check facility capacity and wait times"""
        
        facilities_to_check = FACILITIES
        
        if facility_ids:
            facilities_to_check = [f for f in FACILITIES if f['id'] in facility_ids]
        
        if facility_type:
            type_map = {
                'emergency': 'main_hospital',
                'ucc': 'ucc',
                'clinic': 'clinic'
            }
            facilities_to_check = [f for f in facilities_to_check if f['type'] == type_map.get(facility_type)]
        
        capacity_info = []
        
        for facility in facilities_to_check:
            # Mock capacity data (in production, get real-time data)
            capacity = facility.get('capacity', {})
            
            info = {
                'facility_id': facility['id'],
                'facility_name': facility['name'],
                'type': facility['type'],
                'wait_time_minutes': facility.get('wait_time_minutes', 30),
                'capacity': capacity,
                'current_occupancy_percent': 65,  # Mock data
                'accepting_patients': True,
                'status': 'normal'  # normal, busy, full
            }
            
            # Determine status based on wait time
            if info['wait_time_minutes'] > 60:
                info['status'] = 'busy'
            elif info['wait_time_minutes'] > 90:
                info['status'] = 'full'
                info['accepting_patients'] = False
            
            capacity_info.append(info)
        
        return {
            'success': True,
            'facilities': capacity_info,
            'timestamp': datetime.now().isoformat()
        }
    
    def send_sms_notification(self, phone_number, message_type, details=None):
        """Send SMS notification"""
        
        # Generate message based on type
        if message_type == 'appointment_confirmation':
            message = f"""
مستشفى الحرس الوطني
تم تأكيد موعدك
التاريخ: {details.get('date')}
الوقت: {details.get('time')}
العيادة: {details.get('clinic')}
رقم الحجز: {details.get('booking_id')}
"""
        
        elif message_type == 'facility_directions':
            message = f"""
مستشفى الحرس الوطني
توجه إلى: {details.get('facility_name')}
العنوان: {details.get('address')}
الهاتف: {details.get('phone')}
الخريطة: {details.get('map_url')}
"""
        
        elif message_type == 'wait_time_update':
            message = f"""
مستشفى الحرس الوطني
تحديث وقت الانتظار
المنشأة: {details.get('facility_name')}
الانتظار المتوقع: {details.get('wait_time')} دقيقة
"""
        
        else:
            message = details.get('custom_message', '')
        
        # In production, integrate with SMS gateway (e.g., Twilio)
        # For now, return mock success
        
        return {
            'success': True,
            'phone_number': phone_number,
            'message': message,
            'sent_at': datetime.now().isoformat(),
            'status': 'sent'
        }
    
    # Main agent execution
    
    def execute_task(self, user_request, patient_data=None):
        """Execute a task based on user request"""
        
        # Build system prompt
        system_prompt = """أنت مساعد ذكي متخصص في خدمات مستشفى الحرس الوطني بالرياض.

مهامك:
1. حجز المواعيد في العيادات الخارجية
2. البحث عن أفضل مركز رعاية للمريض
3. إعادة توجيه المرضى للمنشآت المناسبة
4. التحقق من أوقات الانتظار والطاقة الاستيعابية

استخدم الأدوات المتاحة لتنفيذ طلبات المستخدم بكفاءة.
تحدث بالعربية دائماً.
كن دقيقاً ومفيداً."""

        # Add user request to conversation
        self.conversation_history.append({
            'role': 'user',
            'content': user_request
        })
        
        # Call GPT-4 with tools
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {'role': 'system', 'content': system_prompt},
                *self.conversation_history
            ],
            tools=self.tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        # Check if tool calls are needed
        if message.tool_calls:
            # Execute tool calls
            tool_results = []
            
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the function
                if hasattr(self, function_name):
                    result = getattr(self, function_name)(**function_args)
                    tool_results.append({
                        'tool_call_id': tool_call.id,
                        'result': result
                    })
            
            # Add tool results to conversation
            self.conversation_history.append({
                'role': 'assistant',
                'content': message.content,
                'tool_calls': message.tool_calls
            })
            
            for tool_result in tool_results:
                self.conversation_history.append({
                    'role': 'tool',
                    'tool_call_id': tool_result['tool_call_id'],
                    'content': json.dumps(tool_result['result'], ensure_ascii=False)
                })
            
            # Get final response
            final_response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {'role': 'system', 'content': system_prompt},
                    *self.conversation_history
                ]
            )
            
            final_message = final_response.choices[0].message.content
            
            return {
                'success': True,
                'response': final_message,
                'tool_calls': [
                    {
                        'function': tc.function.name,
                        'arguments': json.loads(tc.function.arguments)
                    }
                    for tc in message.tool_calls
                ],
                'tool_results': tool_results
            }
        
        else:
            # No tool calls needed
            self.conversation_history.append({
                'role': 'assistant',
                'content': message.content
            })
            
            return {
                'success': True,
                'response': message.content,
                'tool_calls': [],
                'tool_results': []
            }

# Initialize agentic AI
agentic_ai = AgenticAI()

