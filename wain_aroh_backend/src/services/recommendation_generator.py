"""
Recommendation Generator Service
Generates interactive recommendations based on AI analysis
"""
import json
import re

def analyze_urgency(symptoms_text):
    """Analyze urgency level based on symptoms"""
    urgent_keywords = [
        'ألم شديد', 'نزيف', 'صعوبة تنفس', 'ألم في الصدر', 'فقدان وعي',
        'شلل', 'تشنجات', 'حمى شديدة', 'severe pain', 'bleeding', 'chest pain',
        'difficulty breathing', 'unconscious', 'seizure'
    ]
    
    critical_keywords = [
        'نوبة قلبية', 'سكتة دماغية', 'جلطة', 'heart attack', 'stroke',
        'لا أستطيع التنفس', 'cannot breathe', 'فقدت الوعي', 'passed out'
    ]
    
    text_lower = symptoms_text.lower()
    
    for keyword in critical_keywords:
        if keyword in text_lower:
            return 'critical'
    
    for keyword in urgent_keywords:
        if keyword in text_lower:
            return 'urgent'
    
    return 'normal'

def generate_recommendations(ai_response, symptoms, conversation_id, ctas_level=None, location=None):
    """Generate interactive recommendations from AI response"""
    recommendations = []
    
    # Use CTAS level if provided, otherwise analyze symptoms
    if ctas_level:
        if ctas_level <= 2:
            urgency = 'critical'
        elif ctas_level == 3:
            urgency = 'urgent'
        else:
            urgency = 'normal'
    else:
        urgency = analyze_urgency(symptoms)
    
    # Parse AI response for recommendations
    lines = ai_response.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # Emergency recommendation
        if any(word in line.lower() for word in ['طوارئ', 'emergency', '997', 'اتصل فوراً']):
            recommendations.append({
                'type': 'emergency',
                'title': '🚨 اتصل بالطوارئ فوراً',
                'description': 'حالتك تتطلب رعاية طبية عاجلة. اتصل بالطوارئ على الرقم 997',
                'priority': 'high',
                'is_urgent': True,
                'requires_doctor_approval': False,
                'action_type': 'call_emergency',
                'action_data': {'emergency_number': '997'},
                'icon': '🚨',
                'button_text': 'اتصل بالطوارئ 997'
            })
        
        # Doctor consultation recommendation
        elif any(word in line.lower() for word in ['استشارة طبيب', 'راجع طبيب', 'زيارة طبيب', 'consult doctor']):
            recommendations.append({
                'type': 'doctor_consultation',
                'title': '👨‍⚕️ استشارة طبيب',
                'description': line,
                'priority': 'high' if urgency in ['critical', 'urgent'] else 'medium',
                'is_urgent': urgency in ['critical', 'urgent'],
                'requires_doctor_approval': True,
                'action_type': 'contact_doctor',
                'action_data': {
                    'urgency_level': urgency,
                    'symptoms': symptoms,
                    'conversation_id': conversation_id
                },
                'icon': '👨‍⚕️',
                'button_text': 'طلب استشارة طبية عاجلة'
            })
        
        # Clinic appointment recommendation
        elif any(word in line.lower() for word in ['عيادة', 'موعد', 'clinic', 'appointment']):
            # Extract clinic type if mentioned
            clinic_type = 'general'
            if 'قلب' in line or 'cardio' in line.lower():
                clinic_type = 'cardiology'
            elif 'أعصاب' in line or 'neuro' in line.lower():
                clinic_type = 'neurology'
            elif 'عظام' in line or 'ortho' in line.lower():
                clinic_type = 'orthopedics'
            elif 'جلدية' in line or 'derma' in line.lower():
                clinic_type = 'dermatology'
            
            recommendations.append({
                'type': 'clinic',
                'title': '🏥 حجز موعد في العيادة',
                'description': line,
                'priority': 'medium',
                'is_urgent': False,
                'requires_doctor_approval': False,
                'action_type': 'book_clinic',
                'action_data': {
                    'clinic_type': clinic_type,
                    'symptoms_summary': symptoms,
                    'conversation_id': conversation_id
                },
                'icon': '🏥',
                'button_text': 'حجز موعد في العيادة'
            })
        
        # Self-care recommendation
        elif any(word in line.lower() for word in ['راحة', 'شرب', 'تناول', 'rest', 'drink', 'take']):
            if len(line) > 10:  # Only if it's a meaningful recommendation
                recommendations.append({
                    'type': 'self_care',
                    'title': '💊 رعاية ذاتية',
                    'description': line,
                    'priority': 'low',
                    'is_urgent': False,
                    'requires_doctor_approval': False,
                    'action_type': 'self_care',
                    'action_data': {'advice': line},
                    'icon': '💊',
                    'button_text': 'تم الاطلاع'
                })
    
    # If no recommendations were generated from text, generate based on CTAS level
    if not recommendations and ctas_level:
        if ctas_level <= 2:
            # Critical/Emergency - Go to Emergency
            recommendations.append({
                'type': 'emergency',
                'title': '🚨 الذهاب إلى الطوارئ',
                'description': 'حالتك تتطلب رعاية طبية عاجلة في قسم الطوارئ',
                'priority': 'high',
                'is_urgent': True,
                'requires_doctor_approval': False,
                'action_type': 'go_to_emergency',
                'action_data': {'ctas_level': ctas_level, 'location': location},
                'icon': '🚨',
                'button_text': 'عرض أقرب طوارئ'
            })
        elif ctas_level == 3:
            # Urgent - Urgent Care Center
            recommendations.append({
                'type': 'urgent_care',
                'title': '🏥 مركز الرعاية العاجلة',
                'description': 'حالتك تحتاج رعاية عاجلة في مركز الرعاية العاجلة',
                'priority': 'medium',
                'is_urgent': True,
                'requires_doctor_approval': False,
                'action_type': 'go_to_urgent_care',
                'action_data': {'ctas_level': ctas_level, 'location': location},
                'icon': '🏥',
                'button_text': 'عرض أقرب مركز رعاية عاجلة'
            })
        else:
            # Non-urgent - Clinic
            recommendations.append({
                'type': 'clinic',
                'title': '🏥 العيادة',
                'description': 'يمكنك حجز موعد في العيادة',
                'priority': 'low',
                'is_urgent': False,
                'requires_doctor_approval': False,
                'action_type': 'book_clinic',
                'action_data': {'ctas_level': ctas_level, 'location': location},
                'icon': '🏥',
                'button_text': 'حجز موعد في العيادة'
            })
    
    # If still no recommendations, create a default one
    if not recommendations:
        recommendations.append({
            'type': 'self_care',
            'title': '📋 نصيحة عامة',
            'description': ai_response[:200] if len(ai_response) > 200 else ai_response,
            'priority': 'low',
            'is_urgent': False,
            'requires_doctor_approval': False,
            'action_type': 'self_care',
            'action_data': {'advice': ai_response},
            'icon': '📋',
            'button_text': 'تم الاطلاع'
        })
    
    return recommendations

def format_recommendations_response(ai_message, recommendations):
    """Format the response with recommendations"""
    response = {
        'message': ai_message,
        'recommendations': recommendations,
        'has_urgent': any(r.get('is_urgent', False) for r in recommendations),
        'requires_action': any(r.get('requires_doctor_approval', False) for r in recommendations)
    }
    return response

