"""
Enhanced Conversation API
Integrates advanced triage engine with conversational interface
"""

from flask import Blueprint, jsonify, request, session
from datetime import datetime
import sys
import os
import uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.services.enhanced_conversational_ai import EnhancedConversationalAI

enhanced_conversation_api = Blueprint('enhanced_conversation_api', __name__)

# Store active sessions (in production, use Redis or database)
active_sessions = {}

@enhanced_conversation_api.route('/api/conversation/start', methods=['POST'])
def start_conversation():
    """
    Start a new conversation session
    """
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Create new AI instance
        ai = EnhancedConversationalAI()
        result = ai.start_new_session(session_id)
        
        # Store session
        active_sessions[session_id] = ai
        
        return jsonify({
            "success": True,
            "data": result
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_conversation_api.route('/api/conversation/message', methods=['POST'])
def send_message():
    """
    Send a message in an active conversation
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        message = data.get('message')
        context = data.get('context', {})
        
        if not session_id or not message:
            return jsonify({
                "success": False,
                "error": "session_id and message are required"
            }), 400
        
        # Get or create session
        if session_id not in active_sessions:
            ai = EnhancedConversationalAI()
            ai.start_new_session(session_id)
            active_sessions[session_id] = ai
        else:
            ai = active_sessions[session_id]
        
        # Process message
        response = ai.process_message(message, context)
        
        return jsonify({
            "success": True,
            "data": response
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_conversation_api.route('/api/conversation/session/<session_id>', methods=['GET'])
def get_session_info(session_id):
    """
    Get information about a conversation session
    """
    try:
        if session_id not in active_sessions:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
        
        ai = active_sessions[session_id]
        summary = ai.get_session_summary()
        
        return jsonify({
            "success": True,
            "data": summary
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_conversation_api.route('/api/conversation/session/<session_id>/history', methods=['GET'])
def get_conversation_history(session_id):
    """
    Get full conversation history for a session
    """
    try:
        if session_id not in active_sessions:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
        
        ai = active_sessions[session_id]
        
        return jsonify({
            "success": True,
            "data": {
                "session_id": session_id,
                "history": ai.conversation_history,
                "message_count": len(ai.conversation_history)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_conversation_api.route('/api/conversation/session/<session_id>/assessment', methods=['GET'])
def get_current_assessment(session_id):
    """
    Get current triage assessment for a session
    """
    try:
        if session_id not in active_sessions:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
        
        ai = active_sessions[session_id]
        
        if not ai.triage_engine:
            return jsonify({
                "success": False,
                "error": "No triage data available"
            }), 404
        
        assessment_data = {
            "extracted_data": ai.triage_engine.extracted_data,
            "confidence": ai.triage_engine.confidence_score,
            "assessment_complete": ai.triage_engine.assessment_complete
        }
        
        # If assessment is complete, include final CTAS
        if ai.triage_engine.assessment_complete:
            assessment_data["final_ctas"] = ai.triage_engine.calculate_final_ctas()
        
        return jsonify({
            "success": True,
            "data": assessment_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_conversation_api.route('/api/conversation/session/<session_id>/end', methods=['POST'])
def end_conversation(session_id):
    """
    End a conversation session
    """
    try:
        if session_id not in active_sessions:
            return jsonify({
                "success": False,
                "error": "Session not found"
            }), 404
        
        ai = active_sessions[session_id]
        summary = ai.get_session_summary()
        
        # Remove from active sessions
        del active_sessions[session_id]
        
        return jsonify({
            "success": True,
            "message": "Session ended successfully",
            "data": summary
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_conversation_api.route('/api/conversation/sessions/active', methods=['GET'])
def get_active_sessions():
    """
    Get list of all active sessions
    """
    try:
        sessions_list = []
        
        for session_id, ai in active_sessions.items():
            summary = ai.get_session_summary()
            sessions_list.append(summary)
        
        return jsonify({
            "success": True,
            "data": {
                "active_count": len(sessions_list),
                "sessions": sessions_list
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_conversation_api.route('/api/conversation/feedback', methods=['POST'])
def submit_feedback():
    """
    Submit feedback for a completed conversation
    """
    try:
        data = request.json
        session_id = data.get('session_id')
        feedback = data.get('feedback')
        
        if not session_id or not feedback:
            return jsonify({
                "success": False,
                "error": "session_id and feedback are required"
            }), 400
        
        # Store feedback (would be saved to database in production)
        feedback_record = {
            "session_id": session_id,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "message": "Feedback submitted successfully",
            "data": feedback_record
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@enhanced_conversation_api.route('/api/conversation/test', methods=['POST'])
def test_triage():
    """
    Test endpoint for quick triage testing
    """
    try:
        data = request.json
        symptoms = data.get('symptoms', [])
        age = data.get('age')
        severity = data.get('severity', 'moderate')
        
        # Create test session
        session_id = f"test_{uuid.uuid4()}"
        ai = EnhancedConversationalAI()
        ai.start_new_session(session_id)
        
        # Simulate conversation
        test_message = f"عمري {age} سنة. "
        test_message += " و".join(symptoms)
        test_message += f". الألم {severity}."
        
        response = ai.process_message(test_message)
        
        # Get assessment if complete
        if ai.triage_engine.assessment_complete:
            final_assessment = ai.triage_engine.calculate_final_ctas()
            response["final_assessment"] = final_assessment
        
        return jsonify({
            "success": True,
            "data": response,
            "test_input": {
                "symptoms": symptoms,
                "age": age,
                "severity": severity
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
