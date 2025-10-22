"""
Automated Response Service
Sends automated responses to patients based on specialist actions
"""
from datetime import datetime
import json

def generate_doctor_approval_response(communication, doctor_response):
    """Generate automated response when doctor approves/rejects communication"""
    
    if communication.status == 'approved':
        return {
            'type': 'doctor_approved',
            'title': '✅ تمت الموافقة على طلب الاستشارة',
            'message': f"""تم الموافقة على طلبك للتواصل مع الطبيب.

**رد الطبيب:**
{doctor_response}

**الخطوات التالية:**
- سيتم التواصل معك خلال 24 ساعة
- يرجى متابعة هاتفك للرد على المكالمة
- في حالة الطوارئ، اتصل بالرقم 997

شكراً لاستخدامك خدمة "وين أروح" 🏥""",
            'urgency': communication.urgency_level,
            'next_steps': [
                'انتظر اتصال الطبيب خلال 24 ساعة',
                'تأكد من توفر هاتفك',
                'في حالة الطوارئ اتصل بـ 997'
            ]
        }
    else:
        return {
            'type': 'doctor_rejected',
            'title': '❌ تم رفض طلب الاستشارة',
            'message': f"""للأسف، لم يتم الموافقة على طلب الاستشارة.

**سبب الرفض:**
{doctor_response}

**التوصيات البديلة:**
- يمكنك حجز موعد في العيادة
- راجع قسم الطوارئ إذا كانت حالتك عاجلة
- اتصل بالرقم 997 في حالات الطوارئ الحرجة

شكراً لاستخدامك خدمة "وين أروح" 🏥""",
            'urgency': 'normal',
            'next_steps': [
                'احجز موعد في العيادة',
                'راجع الطوارئ إذا لزم الأمر',
                'اتصل بـ 997 في الحالات الحرجة'
            ]
        }

def generate_clinic_appointment_response(appointment, specialist_notes, appointment_details):
    """Generate automated response when specialist reviews clinic appointment"""
    
    if appointment.status == 'scheduled':
        appt_data = json.loads(appointment_details) if isinstance(appointment_details, str) else appointment_details
        
        return {
            'type': 'appointment_scheduled',
            'title': '✅ تم تأكيد موعدك في العيادة',
            'message': f"""تم تأكيد موعدك في العيادة بنجاح!

**تفاصيل الموعد:**
📅 التاريخ: {appt_data.get('date', 'سيتم تحديده')}
🕐 الوقت: {appt_data.get('time', 'سيتم تحديده')}
📍 المكان: {appt_data.get('location', 'العيادة الخارجية')}
👨‍⚕️ الطبيب: {appt_data.get('doctor_name', 'سيتم تحديده')}

**ملاحظات المختص:**
{specialist_notes}

**تعليمات مهمة:**
- احضر قبل الموعد بـ 15 دقيقة
- أحضر بطاقة الهوية والتأمين
- أحضر أي تقارير طبية سابقة

شكراً لاستخدامك خدمة "وين أروح" 🏥""",
            'appointment_details': appt_data,
            'next_steps': [
                f"احضر يوم {appt_data.get('date', 'الموعد')} الساعة {appt_data.get('time', 'المحددة')}",
                'أحضر بطاقة الهوية والتأمين',
                'أحضر التقارير الطبية السابقة'
            ]
        }
    
    elif appointment.status == 'approved':
        return {
            'type': 'appointment_approved',
            'title': '✅ تمت الموافقة على طلب الموعد',
            'message': f"""تمت الموافقة على طلبك لحجز موعد في العيادة.

**ملاحظات المختص:**
{specialist_notes}

**الخطوات التالية:**
- سيتم التواصل معك خلال 48 ساعة لتحديد الموعد
- تأكد من توفر هاتفك
- يمكنك الاتصال بالعيادة لتحديد الموعد مباشرة

شكراً لاستخدامك خدمة "وين أروح" 🏥""",
            'next_steps': [
                'انتظر اتصال العيادة خلال 48 ساعة',
                'أو اتصل بالعيادة مباشرة',
                'جهز المستندات المطلوبة'
            ]
        }
    
    else:  # rejected
        return {
            'type': 'appointment_rejected',
            'title': '❌ لم يتم الموافقة على الموعد',
            'message': f"""للأسف، لم يتم الموافقة على طلب الموعد.

**سبب الرفض:**
{specialist_notes}

**التوصيات البديلة:**
- يمكنك حجز موعد في عيادة أخرى
- راجع قسم الطوارئ إذا كانت حالتك عاجلة
- اتصل بالعيادة مباشرة للاستفسار

شكراً لاستخدامك خدمة "وين أروح" 🏥""",
            'next_steps': [
                'جرب حجز موعد في عيادة أخرى',
                'راجع الطوارئ إذا لزم الأمر',
                'اتصل بالعيادة للاستفسار'
            ]
        }

def send_automated_response(response_type, recipient_id, response_data):
    """Send automated response to patient"""
    # In a real system, this would send SMS, email, or push notification
    # For now, we'll just log it and return the response
    
    automated_response = {
        'recipient_id': recipient_id,
        'response_type': response_type,
        'sent_at': datetime.now().isoformat(),
        'data': response_data
    }
    
    # TODO: Integrate with SMS/Email/Push notification service
    print(f"[AUTOMATED RESPONSE] Sent to {recipient_id}: {response_data['title']}")
    
    return automated_response

def format_response_for_chat(response_data):
    """Format automated response for display in chat interface"""
    return {
        'type': 'automated_response',
        'title': response_data['title'],
        'message': response_data['message'],
        'next_steps': response_data.get('next_steps', []),
        'urgency': response_data.get('urgency', 'normal'),
        'timestamp': datetime.now().isoformat()
    }

