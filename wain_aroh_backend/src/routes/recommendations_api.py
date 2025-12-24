"""
API routes for recommendations and doctor communication
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.recommendation import (
    Recommendation, DoctorCommunication, ClinicAppointmentRequest,
    save_recommendation, save_doctor_communication, save_clinic_appointment,
    get_recommendations_by_conversation, get_pending_doctor_communications,
    get_pending_clinic_appointments, update_doctor_communication_status,
    update_clinic_appointment_status
)
from src.services.automated_response import (
    generate_doctor_approval_response,
    generate_clinic_appointment_response,
    send_automated_response,
    format_response_for_chat
)

recommendations_bp = Blueprint('recommendations', __name__)

@recommendations_bp.route('/api/recommendations/create', methods=['POST'])
def create_recommendation():
    """Create a new recommendation"""
    try:
        data = request.json
        
        recommendation = Recommendation(
            conversation_id=data.get('conversation_id'),
            recommendation_type=data.get('recommendation_type'),
            title=data.get('title'),
            description=data.get('description'),
            priority=data.get('priority', 'medium'),
            is_urgent=data.get('is_urgent', False),
            requires_doctor_approval=data.get('requires_doctor_approval', False),
            action_type=data.get('action_type'),
            action_data=data.get('action_data')
        )
        
        saved_rec = save_recommendation(recommendation)
        return jsonify(saved_rec.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/api/recommendations/conversation/<int:conversation_id>', methods=['GET'])
def get_conversation_recommendations(conversation_id):
    """Get all recommendations for a conversation"""
    try:
        recommendations = get_recommendations_by_conversation(conversation_id)
        return jsonify([r.to_dict() for r in recommendations]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/api/doctor-communication/create', methods=['POST'])
def create_doctor_communication():
    """Create a doctor communication request"""
    try:
        data = request.json
        
        communication = DoctorCommunication(
            patient_id=data.get('patient_id'),
            conversation_id=data.get('conversation_id'),
            recommendation_id=data.get('recommendation_id'),
            urgency_level=data.get('urgency_level', 'normal'),
            symptoms=data.get('symptoms')
        )
        
        saved_comm = save_doctor_communication(communication)
        
        # TODO: Send notification to doctor
        
        return jsonify(saved_comm.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/api/doctor-communication/pending', methods=['GET'])
def get_pending_communications():
    """Get all pending doctor communication requests"""
    try:
        communications = get_pending_doctor_communications()
        return jsonify([c.to_dict() for c in communications]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/api/doctor-communication/<int:comm_id>/respond', methods=['POST'])
def respond_to_communication(comm_id):
    """Doctor responds to a communication request"""
    try:
        data = request.json
        status = data.get('status')  # 'approved' or 'rejected'
        doctor_response = data.get('doctor_response')
        
        updated_comm = update_doctor_communication_status(
            comm_id, status, doctor_response
        )
        
        if not updated_comm:
            return jsonify({'error': 'Communication not found'}), 404
        
        # Generate and send automated response to patient
        auto_response = generate_doctor_approval_response(updated_comm, doctor_response)
        sent_response = send_automated_response(
            'doctor_communication',
            updated_comm.patient_id,
            auto_response
        )
        
        return jsonify({
            'communication': updated_comm.to_dict(),
            'automated_response': format_response_for_chat(auto_response)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/api/clinic-appointment/create', methods=['POST'])
def create_clinic_appointment():
    """Create a clinic appointment request"""
    try:
        data = request.json
        
        appointment = ClinicAppointmentRequest(
            patient_id=data.get('patient_id'),
            conversation_id=data.get('conversation_id'),
            recommendation_id=data.get('recommendation_id'),
            clinic_type=data.get('clinic_type'),
            symptoms_summary=data.get('symptoms_summary'),
            preferred_date=data.get('preferred_date'),
            preferred_time=data.get('preferred_time')
        )
        
        saved_appt = save_clinic_appointment(appointment)
        
        # TODO: Send notification to specialist
        
        return jsonify(saved_appt.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/api/clinic-appointment/pending', methods=['GET'])
def get_pending_appointments():
    """Get all pending clinic appointment requests"""
    try:
        appointments = get_pending_clinic_appointments()
        return jsonify([a.to_dict() for a in appointments]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/api/clinic-appointment/<int:appt_id>/review', methods=['POST'])
def review_appointment(appt_id):
    """Specialist reviews and responds to appointment request"""
    try:
        data = request.json
        status = data.get('status')  # 'approved', 'scheduled', or 'rejected'
        specialist_notes = data.get('specialist_notes')
        appointment_details = data.get('appointment_details')  # date, time, location
        
        updated_appt = update_clinic_appointment_status(
            appt_id, status, specialist_notes, appointment_details
        )
        
        if not updated_appt:
            return jsonify({'error': 'Appointment not found'}), 404
        
        # Send automated response to patient
        if not updated_appt.auto_response_sent:
            auto_response = generate_clinic_appointment_response(
                updated_appt,
                specialist_notes,
                appointment_details
            )
            sent_response = send_automated_response(
                'clinic_appointment',
                updated_appt.patient_id,
                auto_response
            )
            updated_appt.auto_response_sent = True
        
        return jsonify({
            'appointment': updated_appt.to_dict(),
            'automated_response': format_response_for_chat(auto_response)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recommendations_bp.route('/api/recommendations/action', methods=['POST'])
def execute_recommendation_action():
    """Execute an action from a recommendation"""
    try:
        data = request.json
        recommendation_id = data.get('recommendation_id')
        action_type = data.get('action_type')
        action_data = data.get('action_data', {})
        
        # Handle different action types
        if action_type == 'contact_doctor':
            # Create doctor communication request
            communication = DoctorCommunication(
                patient_id=action_data.get('patient_id'),
                conversation_id=action_data.get('conversation_id'),
                recommendation_id=recommendation_id,
                urgency_level=action_data.get('urgency_level', 'urgent'),
                symptoms=action_data.get('symptoms')
            )
            saved_comm = save_doctor_communication(communication)
            return jsonify({
                'success': True,
                'message': 'تم إرسال طلب التواصل مع الطبيب بنجاح',
                'data': saved_comm.to_dict()
            }), 201
            
        elif action_type == 'book_clinic':
            # Create clinic appointment request
            appointment = ClinicAppointmentRequest(
                patient_id=action_data.get('patient_id'),
                conversation_id=action_data.get('conversation_id'),
                recommendation_id=recommendation_id,
                clinic_type=action_data.get('clinic_type'),
                symptoms_summary=action_data.get('symptoms_summary'),
                preferred_date=action_data.get('preferred_date'),
                preferred_time=action_data.get('preferred_time')
            )
            saved_appt = save_clinic_appointment(appointment)
            return jsonify({
                'success': True,
                'message': 'تم إرسال طلب حجز موعد العيادة بنجاح',
                'data': saved_appt.to_dict()
            }), 201
            
        elif action_type == 'call_emergency':
            return jsonify({
                'success': True,
                'message': 'يرجى الاتصال بالطوارئ على الرقم 997',
                'emergency_number': '997'
            }), 200
            
        elif action_type == 'self_care':
            return jsonify({
                'success': True,
                'message': 'تم تسجيل توصية الرعاية الذاتية'
            }), 200
            
        else:
            return jsonify({'error': 'Invalid action type'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

