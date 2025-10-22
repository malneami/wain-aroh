"""
واجهة برمجة التطبيقات لحجز المواعيد
Appointment Booking API Routes
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from ..services.appointment_service import appointment_service
from ..models.hospital import Hospital

# إنشاء Blueprint
appointment_bp = Blueprint('appointment', __name__, url_prefix='/api/appointments')


@appointment_bp.route('/slots', methods=['POST'])
def get_available_slots():
    """
    الحصول على الفترات المتاحة
    Get available time slots
    
    Body:
    {
        "facility_id": 1,
        "specialty": "قلب",
        "start_date": "2024-10-15",
        "days": 7
    }
    """
    try:
        data = request.json or {}
        
        facility_id = data.get('facility_id')
        specialty = data.get('specialty', '')
        start_date_str = data.get('start_date')
        days = data.get('days', 7)
        
        if not facility_id:
            return jsonify({
                'success': False,
                'error': 'يجب تحديد المنشأة'
            }), 400
        
        # التحقق من وجود المنشأة
        hospital = Hospital.query.get(facility_id)
        if not hospital:
            return jsonify({
                'success': False,
                'error': 'المنشأة غير موجودة'
            }), 404
        
        # تحويل التاريخ
        if start_date_str:
            start_date = datetime.fromisoformat(start_date_str)
        else:
            start_date = datetime.now()
        
        # الحصول على الفترات المتاحة
        slots = appointment_service.get_available_slots(
            facility_id,
            specialty,
            start_date,
            days
        )
        
        # تحويل إلى JSON
        slots_dict = [
            {
                "datetime": slot.datetime.isoformat(),
                "date": slot.datetime.strftime('%Y-%m-%d'),
                "time": slot.datetime.strftime('%I:%M %p'),
                "day_name": slot.datetime.strftime('%A'),
                "doctor_name": slot.doctor_name,
                "specialty": slot.specialty,
                "available": slot.available
            }
            for slot in slots
        ]
        
        return jsonify({
            'success': True,
            'slots': slots_dict,
            'total_slots': len(slots_dict)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@appointment_bp.route('/book', methods=['POST'])
def book_appointment():
    """
    حجز موعد
    Book an appointment
    
    Body:
    {
        "facility_id": 1,
        "patient_name": "أحمد محمد",
        "patient_phone": "0501234567",
        "patient_email": "ahmad@example.com",
        "specialty": "قلب",
        "doctor_name": "د. أحمد العمري",
        "appointment_datetime": "2024-10-15T10:00:00",
        "notes": "ملاحظات إضافية"
    }
    """
    try:
        data = request.json or {}
        
        facility_id = data.get('facility_id')
        patient_name = data.get('patient_name')
        patient_phone = data.get('patient_phone')
        patient_email = data.get('patient_email', '')
        specialty = data.get('specialty')
        doctor_name = data.get('doctor_name')
        appointment_datetime_str = data.get('appointment_datetime')
        notes = data.get('notes', '')
        
        # التحقق من البيانات المطلوبة
        if not all([facility_id, patient_name, patient_phone, specialty, doctor_name, appointment_datetime_str]):
            return jsonify({
                'success': False,
                'error': 'يجب تعبئة جميع الحقول المطلوبة'
            }), 400
        
        # التحقق من وجود المنشأة
        hospital = Hospital.query.get(facility_id)
        if not hospital:
            return jsonify({
                'success': False,
                'error': 'المنشأة غير موجودة'
            }), 404
        
        # تحويل التاريخ والوقت
        appointment_datetime = datetime.fromisoformat(appointment_datetime_str)
        
        # حجز الموعد
        appointment = appointment_service.book_appointment(
            facility_id=facility_id,
            facility_name=hospital.name,
            patient_name=patient_name,
            patient_phone=patient_phone,
            patient_email=patient_email,
            specialty=specialty,
            doctor_name=doctor_name,
            appointment_datetime=appointment_datetime,
            notes=notes
        )
        
        # إرسال تأكيد
        confirmation = appointment_service.send_appointment_confirmation(appointment)
        
        return jsonify({
            'success': True,
            'appointment': {
                'id': appointment.id,
                'facility_name': appointment.facility_name,
                'patient_name': appointment.patient_name,
                'specialty': appointment.specialty,
                'doctor_name': appointment.doctor_name,
                'appointment_date': appointment.appointment_date.isoformat(),
                'status': appointment.status,
                'notes': appointment.notes
            },
            'confirmation': confirmation
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@appointment_bp.route('/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """
    الحصول على تفاصيل موعد
    Get appointment details
    """
    try:
        appointment = appointment_service.get_appointment(appointment_id)
        
        if not appointment:
            return jsonify({
                'success': False,
                'error': 'الموعد غير موجود'
            }), 404
        
        return jsonify({
            'success': True,
            'appointment': {
                'id': appointment.id,
                'facility_id': appointment.facility_id,
                'facility_name': appointment.facility_name,
                'patient_name': appointment.patient_name,
                'patient_phone': appointment.patient_phone,
                'patient_email': appointment.patient_email,
                'specialty': appointment.specialty,
                'doctor_name': appointment.doctor_name,
                'appointment_date': appointment.appointment_date.isoformat(),
                'status': appointment.status,
                'notes': appointment.notes,
                'created_at': appointment.created_at.isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@appointment_bp.route('/<int:appointment_id>/confirm', methods=['POST'])
def confirm_appointment(appointment_id):
    """
    تأكيد موعد
    Confirm appointment
    """
    try:
        success = appointment_service.confirm_appointment(appointment_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'الموعد غير موجود'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'تم تأكيد الموعد بنجاح'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@appointment_bp.route('/<int:appointment_id>/cancel', methods=['POST'])
def cancel_appointment(appointment_id):
    """
    إلغاء موعد
    Cancel appointment
    """
    try:
        success = appointment_service.cancel_appointment(appointment_id)
        
        if not success:
            return jsonify({
                'success': False,
                'error': 'الموعد غير موجود'
            }), 404
        
        return jsonify({
            'success': True,
            'message': 'تم إلغاء الموعد بنجاح'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@appointment_bp.route('/patient/<phone>', methods=['GET'])
def get_patient_appointments(phone):
    """
    الحصول على مواعيد المريض
    Get patient appointments
    """
    try:
        appointments = appointment_service.get_patient_appointments(phone)
        
        appointments_dict = [
            {
                'id': app.id,
                'facility_name': app.facility_name,
                'specialty': app.specialty,
                'doctor_name': app.doctor_name,
                'appointment_date': app.appointment_date.isoformat(),
                'status': app.status,
                'notes': app.notes
            }
            for app in appointments
        ]
        
        return jsonify({
            'success': True,
            'appointments': appointments_dict,
            'total': len(appointments_dict)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@appointment_bp.route('/facility/<int:facility_id>', methods=['GET'])
def get_facility_appointments(facility_id):
    """
    الحصول على مواعيد المنشأة
    Get facility appointments
    
    Query params:
    - date: التاريخ (YYYY-MM-DD)
    """
    try:
        date_str = request.args.get('date')
        date = None
        
        if date_str:
            date = datetime.fromisoformat(date_str)
        
        appointments = appointment_service.get_facility_appointments(facility_id, date)
        
        appointments_dict = [
            {
                'id': app.id,
                'patient_name': app.patient_name,
                'patient_phone': app.patient_phone,
                'specialty': app.specialty,
                'doctor_name': app.doctor_name,
                'appointment_date': app.appointment_date.isoformat(),
                'status': app.status,
                'notes': app.notes
            }
            for app in appointments
        ]
        
        return jsonify({
            'success': True,
            'appointments': appointments_dict,
            'total': len(appointments_dict)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

