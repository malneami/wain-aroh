"""
خدمة حجز المواعيد
Appointment Booking Service
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, field
import random


@dataclass
class TimeSlot:
    """فترة زمنية متاحة"""
    datetime: datetime
    available: bool = True
    doctor_name: str = ""
    specialty: str = ""


@dataclass
class Appointment:
    """موعد طبي"""
    id: int
    facility_id: int
    facility_name: str
    patient_name: str
    patient_phone: str
    patient_email: str
    specialty: str
    doctor_name: str
    appointment_date: datetime
    status: str  # "pending", "confirmed", "cancelled", "completed"
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)


class AppointmentService:
    """خدمة حجز المواعيد"""
    
    def __init__(self):
        """تهيئة الخدمة"""
        self.appointments = []
        self.next_id = 1
    
    def get_available_slots(
        self,
        facility_id: int,
        specialty: str,
        start_date: datetime,
        days: int = 7
    ) -> List[TimeSlot]:
        """
        الحصول على الفترات المتاحة
        Get available time slots
        
        Args:
            facility_id: معرف المنشأة
            specialty: التخصص
            start_date: تاريخ البداية
            days: عدد الأيام
            
        Returns:
            قائمة الفترات المتاحة
        """
        slots = []
        
        # أسماء أطباء عشوائية
        doctors = [
            "د. أحمد العمري",
            "د. فاطمة الشمري",
            "د. محمد السعيد",
            "د. نورة القحطاني",
            "د. خالد المطيري"
        ]
        
        # توليد فترات زمنية للأيام القادمة
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # تخطي الجمعة
            if current_date.weekday() == 4:  # الجمعة
                continue
            
            # الفترة الصباحية (8 صباحاً - 12 ظهراً)
            for hour in range(8, 12):
                for minute in [0, 30]:
                    slot_time = current_date.replace(hour=hour, minute=minute, second=0)
                    slots.append(TimeSlot(
                        datetime=slot_time,
                        available=random.choice([True, True, True, False]),  # 75% متاح
                        doctor_name=random.choice(doctors),
                        specialty=specialty
                    ))
            
            # الفترة المسائية (4 عصراً - 8 مساءً)
            for hour in range(16, 20):
                for minute in [0, 30]:
                    slot_time = current_date.replace(hour=hour, minute=minute, second=0)
                    slots.append(TimeSlot(
                        datetime=slot_time,
                        available=random.choice([True, True, False]),  # 66% متاح
                        doctor_name=random.choice(doctors),
                        specialty=specialty
                    ))
        
        return [slot for slot in slots if slot.available]
    
    def book_appointment(
        self,
        facility_id: int,
        facility_name: str,
        patient_name: str,
        patient_phone: str,
        patient_email: str,
        specialty: str,
        doctor_name: str,
        appointment_datetime: datetime,
        notes: str = ""
    ) -> Appointment:
        """
        حجز موعد
        Book an appointment
        
        Args:
            facility_id: معرف المنشأة
            facility_name: اسم المنشأة
            patient_name: اسم المريض
            patient_phone: هاتف المريض
            patient_email: بريد المريض
            specialty: التخصص
            doctor_name: اسم الطبيب
            appointment_datetime: تاريخ ووقت الموعد
            notes: ملاحظات
            
        Returns:
            الموعد المحجوز
        """
        appointment = Appointment(
            id=self.next_id,
            facility_id=facility_id,
            facility_name=facility_name,
            patient_name=patient_name,
            patient_phone=patient_phone,
            patient_email=patient_email,
            specialty=specialty,
            doctor_name=doctor_name,
            appointment_date=appointment_datetime,
            status="pending",
            notes=notes
        )
        
        self.appointments.append(appointment)
        self.next_id += 1
        
        return appointment
    
    def confirm_appointment(self, appointment_id: int) -> bool:
        """
        تأكيد موعد
        Confirm appointment
        
        Args:
            appointment_id: معرف الموعد
            
        Returns:
            نجح أم لا
        """
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                appointment.status = "confirmed"
                return True
        return False
    
    def cancel_appointment(self, appointment_id: int) -> bool:
        """
        إلغاء موعد
        Cancel appointment
        
        Args:
            appointment_id: معرف الموعد
            
        Returns:
            نجح أم لا
        """
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                appointment.status = "cancelled"
                return True
        return False
    
    def get_appointment(self, appointment_id: int) -> Optional[Appointment]:
        """
        الحصول على موعد
        Get appointment
        
        Args:
            appointment_id: معرف الموعد
            
        Returns:
            الموعد أو None
        """
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                return appointment
        return None
    
    def get_patient_appointments(self, patient_phone: str) -> List[Appointment]:
        """
        الحصول على مواعيد المريض
        Get patient appointments
        
        Args:
            patient_phone: هاتف المريض
            
        Returns:
            قائمة المواعيد
        """
        return [
            app for app in self.appointments
            if app.patient_phone == patient_phone
        ]
    
    def get_facility_appointments(
        self,
        facility_id: int,
        date: Optional[datetime] = None
    ) -> List[Appointment]:
        """
        الحصول على مواعيد المنشأة
        Get facility appointments
        
        Args:
            facility_id: معرف المنشأة
            date: التاريخ (اختياري)
            
        Returns:
            قائمة المواعيد
        """
        appointments = [
            app for app in self.appointments
            if app.facility_id == facility_id
        ]
        
        if date:
            appointments = [
                app for app in appointments
                if app.appointment_date.date() == date.date()
            ]
        
        return appointments
    
    def send_appointment_confirmation(self, appointment: Appointment) -> Dict:
        """
        إرسال تأكيد الموعد
        Send appointment confirmation
        
        Args:
            appointment: الموعد
            
        Returns:
            نتيجة الإرسال
        """
        # في بيئة الإنتاج، هنا سيتم إرسال رسالة نصية أو بريد إلكتروني
        message = f"""
        تأكيد موعد طبي
        
        عزيزي/عزيزتي {appointment.patient_name}،
        
        تم تأكيد موعدك الطبي بنجاح:
        
        📅 التاريخ: {appointment.appointment_date.strftime('%Y-%m-%d')}
        🕐 الوقت: {appointment.appointment_date.strftime('%I:%M %p')}
        🏥 المنشأة: {appointment.facility_name}
        👨‍⚕️ الطبيب: {appointment.doctor_name}
        🔬 التخصص: {appointment.specialty}
        
        يرجى الحضور قبل الموعد بـ 15 دقيقة.
        
        للإلغاء أو التعديل، يرجى الاتصال على: 920000000
        
        مع تمنياتنا لك بالشفاء العاجل.
        """
        
        return {
            "success": True,
            "message": message,
            "sent_to": {
                "phone": appointment.patient_phone,
                "email": appointment.patient_email
            }
        }
    
    def send_appointment_reminder(self, appointment: Appointment) -> Dict:
        """
        إرسال تذكير بالموعد
        Send appointment reminder
        
        Args:
            appointment: الموعد
            
        Returns:
            نتيجة الإرسال
        """
        message = f"""
        تذكير بموعد طبي
        
        عزيزي/عزيزتي {appointment.patient_name}،
        
        نذكرك بموعدك الطبي غداً:
        
        📅 التاريخ: {appointment.appointment_date.strftime('%Y-%m-%d')}
        🕐 الوقت: {appointment.appointment_date.strftime('%I:%M %p')}
        🏥 المنشأة: {appointment.facility_name}
        👨‍⚕️ الطبيب: {appointment.doctor_name}
        
        يرجى الحضور في الموعد المحدد.
        """
        
        return {
            "success": True,
            "message": message,
            "sent_to": {
                "phone": appointment.patient_phone,
                "email": appointment.patient_email
            }
        }


# مثيل عام من الخدمة
appointment_service = AppointmentService()

