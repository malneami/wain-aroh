"""
Doctor Alert Service
Sends alerts to assigned doctors for critical cases
"""

import json
from datetime import datetime
from openai import OpenAI

client = OpenAI()

class DoctorAlertService:
    """
    Manages doctor alerts and communications for critical cases
    """
    
    def __init__(self):
        self.alerts_sent = []
    
    def should_alert_doctor(self, ctas_level, uploaded_files=None):
        """
        Determine if doctor should be alerted
        
        Args:
            ctas_level: CTAS level (1-5)
            uploaded_files: List of uploaded files
        
        Returns:
            Boolean indicating if alert should be sent
        """
        # Alert for CTAS 1-2 (critical/emergent)
        if ctas_level <= 2:
            return True
        
        # Alert if critical findings in uploaded reports
        if uploaded_files:
            return True
        
        return False
    
    def generate_doctor_summary(self, patient_info, conversation_history, 
                                uploaded_files=None, triage_result=None):
        """
        Generate AI summary for doctor
        
        Args:
            patient_info: Patient information
            conversation_history: Chat history
            uploaded_files: Uploaded medical files
            triage_result: Triage assessment result
        
        Returns:
            Structured summary for doctor
        """
        # Extract key information from conversation
        symptoms = self.extract_symptoms(conversation_history)
        
        # Create prompt for AI summary
        prompt = f"""
        أنت طبيب متخصص. قم بإنشاء ملخص طبي موجز ومهني للطبيب المعالج.
        
        معلومات المريض:
        - الاسم: {patient_info.get('name', 'غير محدد')}
        - العمر: {patient_info.get('age', 'غير محدد')}
        - الجنس: {patient_info.get('gender', 'غير محدد')}
        
        الأعراض المذكورة:
        {symptoms}
        
        تقييم CTAS: المستوى {triage_result.get('ctas_level') if triage_result else 'غير محدد'}
        
        {'ملفات مرفقة: ' + str(len(uploaded_files)) + ' ملف' if uploaded_files else 'لا توجد ملفات مرفقة'}
        
        قم بإنشاء ملخص يتضمن:
        1. الشكوى الرئيسية
        2. الأعراض الرئيسية
        3. مستوى الحالة الحرجة
        4. التوصيات الأولية
        5. الإجراءات المطلوبة
        
        اجعل الملخص موجزاً ومهنياً (200 كلمة كحد أقصى).
        """
        
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "أنت طبيب متخصص في الطوارئ."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            summary = response.choices[0].message.content
            
            return {
                "summary": summary,
                "patient_info": patient_info,
                "ctas_level": triage_result.get('ctas_level') if triage_result else None,
                "symptoms": symptoms,
                "uploaded_files_count": len(uploaded_files) if uploaded_files else 0,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None
    
    def extract_symptoms(self, conversation_history):
        """Extract symptoms from conversation"""
        symptoms = []
        for msg in conversation_history:
            if msg.get('role') == 'user':
                symptoms.append(msg.get('content', ''))
        
        return '\n'.join(symptoms[-5:])  # Last 5 user messages
    
    def send_doctor_alert(self, doctor_info, patient_summary, urgency="high"):
        """
        Send alert to doctor
        
        Args:
            doctor_info: Doctor contact information
            patient_summary: Generated patient summary
            urgency: Alert urgency level
        
        Returns:
            Alert status
        """
        alert = {
            "alert_id": f"ALERT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "urgency": urgency,
            "doctor": doctor_info,
            "patient_summary": patient_summary,
            "status": "sent",
            "channels": []
        }
        
        # Send via SMS (simulated)
        if doctor_info.get('phone'):
            sms_result = self.send_sms_alert(
                doctor_info['phone'],
                patient_summary,
                urgency
            )
            alert["channels"].append({
                "type": "sms",
                "status": "sent",
                "details": sms_result
            })
        
        # Send via Email (simulated)
        if doctor_info.get('email'):
            email_result = self.send_email_alert(
                doctor_info['email'],
                patient_summary,
                urgency
            )
            alert["channels"].append({
                "type": "email",
                "status": "sent",
                "details": email_result
            })
        
        # Send via Hospital System (simulated)
        system_result = self.send_system_alert(
            doctor_info,
            patient_summary,
            urgency
        )
        alert["channels"].append({
            "type": "hospital_system",
            "status": "sent",
            "details": system_result
        })
        
        # Store alert
        self.alerts_sent.append(alert)
        
        return {
            "success": True,
            "alert_id": alert["alert_id"],
            "message": f"تم إرسال تنبيه للطبيب {doctor_info['name']}",
            "channels_used": len(alert["channels"])
        }
    
    def send_sms_alert(self, phone, summary, urgency):
        """Send SMS alert (simulated)"""
        # In production, integrate with SMS gateway (Twilio, etc.)
        
        message = f"""
        🚨 تنبيه طارئ - مستوى {urgency.upper()}
        
        حالة جديدة تتطلب انتباهك:
        
        {summary['summary'][:150]}...
        
        CTAS: المستوى {summary['ctas_level']}
        الوقت: {datetime.now().strftime('%H:%M')}
        
        يرجى مراجعة النظام للتفاصيل الكاملة.
        """
        
        print(f"[SMS ALERT] To: {phone}")
        print(message)
        
        return {
            "phone": phone,
            "message_length": len(message),
            "sent_at": datetime.now().isoformat()
        }
    
    def send_email_alert(self, email, summary, urgency):
        """Send email alert (simulated)"""
        # In production, integrate with email service
        
        subject = f"🚨 تنبيه طارئ - حالة CTAS {summary['ctas_level']}"
        
        body = f"""
        <html dir="rtl">
        <body style="font-family: Arial, sans-serif;">
            <h2 style="color: #d32f2f;">تنبيه طارئ - مستوى {urgency.upper()}</h2>
            
            <h3>ملخص الحالة:</h3>
            <p>{summary['summary']}</p>
            
            <h3>معلومات المريض:</h3>
            <ul>
                <li><strong>الاسم:</strong> {summary['patient_info'].get('name', 'غير محدد')}</li>
                <li><strong>العمر:</strong> {summary['patient_info'].get('age', 'غير محدد')}</li>
                <li><strong>CTAS:</strong> المستوى {summary['ctas_level']}</li>
            </ul>
            
            <h3>الأعراض:</h3>
            <p>{summary['symptoms']}</p>
            
            {f"<p><strong>ملفات مرفقة:</strong> {summary['uploaded_files_count']} ملف</p>" 
             if summary['uploaded_files_count'] > 0 else ""}
            
            <p style="color: #666; margin-top: 20px;">
                <em>تم إرسال هذا التنبيه تلقائياً من نظام "وين أروح"</em><br>
                <em>الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em>
            </p>
        </body>
        </html>
        """
        
        print(f"[EMAIL ALERT] To: {email}")
        print(f"Subject: {subject}")
        
        return {
            "email": email,
            "subject": subject,
            "sent_at": datetime.now().isoformat()
        }
    
    def send_system_alert(self, doctor_info, summary, urgency):
        """Send alert to hospital system (simulated)"""
        # In production, integrate with hospital EMR/HIS
        
        system_alert = {
            "alert_type": "critical_patient",
            "urgency": urgency,
            "doctor_id": doctor_info.get('id'),
            "doctor_name": doctor_info.get('name'),
            "patient_summary": summary,
            "action_required": True,
            "created_at": datetime.now().isoformat()
        }
        
        print(f"[SYSTEM ALERT] Doctor ID: {doctor_info.get('id')}")
        print(f"Alert: {json.dumps(system_alert, ensure_ascii=False, indent=2)}")
        
        return {
            "system": "NGHA-HIS",
            "alert_id": f"SYS-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "sent_at": datetime.now().isoformat()
        }
    
    def get_alert_history(self, doctor_id=None):
        """Get alert history"""
        if doctor_id:
            return [a for a in self.alerts_sent 
                   if a['doctor'].get('id') == doctor_id]
        return self.alerts_sent

# Global instance
doctor_alert_service = DoctorAlertService()

