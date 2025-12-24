"""
Training Analytics API
Provides endpoints for accessing training data, analytics, and system improvement metrics
"""

from flask import Blueprint, jsonify, request
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.services.triage_training_module import training_module

training_analytics_api = Blueprint('training_analytics_api', __name__)

@training_analytics_api.route('/api/training/statistics', methods=['GET'])
def get_training_statistics():
    """
    Get training statistics for specified period
    """
    try:
        days = request.args.get('days', default=30, type=int)
        stats = training_module.get_training_statistics(days=days)
        
        return jsonify({
            "success": True,
            "data": stats,
            "generated_at": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@training_analytics_api.route('/api/training/accuracy', methods=['GET'])
def get_accuracy_metrics():
    """
    Get accuracy metrics and performance indicators
    """
    try:
        metrics = training_module.get_accuracy_metrics()
        
        return jsonify({
            "success": True,
            "data": metrics,
            "generated_at": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@training_analytics_api.route('/api/training/recommendations', methods=['GET'])
def get_improvement_recommendations():
    """
    Get AI-generated recommendations for system improvement
    """
    try:
        recommendations = training_module.get_improvement_recommendations()
        
        return jsonify({
            "success": True,
            "data": recommendations,
            "count": len(recommendations),
            "generated_at": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@training_analytics_api.route('/api/training/export', methods=['POST'])
def export_training_dataset():
    """
    Export training dataset for ML model training
    """
    try:
        output_file = training_module.export_training_dataset()
        
        return jsonify({
            "success": True,
            "message": "Training dataset exported successfully",
            "file_path": output_file,
            "generated_at": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@training_analytics_api.route('/api/training/session/record', methods=['POST'])
def record_training_session():
    """
    Manually record a training session
    """
    try:
        session_data = request.json
        
        if not session_data:
            return jsonify({
                "success": False,
                "error": "No session data provided"
            }), 400
        
        recorded_session = training_module.record_triage_session(session_data)
        
        return jsonify({
            "success": True,
            "message": "Session recorded successfully",
            "session_id": recorded_session.get("session_id"),
            "timestamp": recorded_session.get("timestamp")
        }), 201
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@training_analytics_api.route('/api/training/dashboard', methods=['GET'])
def get_training_dashboard():
    """
    Get comprehensive dashboard data for training analytics
    """
    try:
        days = request.args.get('days', default=30, type=int)
        
        # Get all metrics
        statistics = training_module.get_training_statistics(days=days)
        accuracy = training_module.get_accuracy_metrics()
        recommendations = training_module.get_improvement_recommendations()
        
        # Build dashboard
        dashboard = {
            "overview": {
                "total_sessions": statistics.get("total_sessions", 0),
                "accuracy_rate": accuracy.get("accuracy_rate", 0),
                "average_confidence": statistics.get("average_confidence", 0),
                "patient_acceptance_rate": statistics.get("patient_acceptance_rate", 0)
            },
            "ctas_distribution": statistics.get("ctas_distribution", {}),
            "top_symptoms": dict(list(statistics.get("symptom_frequency", {}).items())[:10]),
            "red_flag_frequency": statistics.get("red_flag_frequency", {}),
            "facility_distribution": statistics.get("facility_type_distribution", {}),
            "age_distribution": statistics.get("age_distribution", {}),
            "accuracy_by_ctas": accuracy.get("ctas_accuracy_by_level", {}),
            "triage_errors": {
                "over_triage": accuracy.get("over_triage", 0),
                "under_triage": accuracy.get("under_triage", 0)
            },
            "recommendations": recommendations,
            "period_days": days,
            "generated_at": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "data": dashboard
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@training_analytics_api.route('/api/training/symptom-patterns', methods=['GET'])
def get_symptom_patterns():
    """
    Get common symptom patterns and combinations
    """
    try:
        days = request.args.get('days', default=30, type=int)
        statistics = training_module.get_training_statistics(days=days)
        
        patterns = {
            "common_combinations": statistics.get("common_symptom_combinations", []),
            "top_symptoms": statistics.get("symptom_frequency", {}),
            "period_days": days
        }
        
        return jsonify({
            "success": True,
            "data": patterns,
            "generated_at": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@training_analytics_api.route('/api/training/quality-metrics', methods=['GET'])
def get_quality_metrics():
    """
    Get quality metrics for triage system
    """
    try:
        accuracy = training_module.get_accuracy_metrics()
        statistics = training_module.get_training_statistics(days=30)
        
        # Calculate quality scores
        accuracy_score = accuracy.get("accuracy_rate", 0)
        confidence_score = statistics.get("average_confidence", 0)
        acceptance_score = statistics.get("patient_acceptance_rate", 0)
        
        # Calculate overall quality score (weighted average)
        overall_quality = (
            accuracy_score * 0.5 +  # 50% weight on accuracy
            confidence_score * 0.3 +  # 30% weight on confidence
            acceptance_score * 0.2  # 20% weight on patient acceptance
        )
        
        quality_metrics = {
            "overall_quality_score": round(overall_quality, 2),
            "components": {
                "accuracy": {
                    "score": accuracy_score,
                    "weight": 0.5,
                    "status": "excellent" if accuracy_score >= 90 else "good" if accuracy_score >= 80 else "needs_improvement"
                },
                "confidence": {
                    "score": confidence_score,
                    "weight": 0.3,
                    "status": "excellent" if confidence_score >= 85 else "good" if confidence_score >= 70 else "needs_improvement"
                },
                "patient_acceptance": {
                    "score": acceptance_score,
                    "weight": 0.2,
                    "status": "excellent" if acceptance_score >= 90 else "good" if acceptance_score >= 80 else "needs_improvement"
                }
            },
            "safety_metrics": {
                "under_triage_rate": round((accuracy.get("under_triage", 0) / max(accuracy.get("total_assessments", 1), 1)) * 100, 2),
                "over_triage_rate": round((accuracy.get("over_triage", 0) / max(accuracy.get("total_assessments", 1), 1)) * 100, 2),
                "red_flag_detection_rate": 100  # Placeholder - would need actual data
            },
            "generated_at": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "data": quality_metrics
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@training_analytics_api.route('/api/training/health', methods=['GET'])
def get_system_health():
    """
    Get system health status
    """
    try:
        statistics = training_module.get_training_statistics(days=7)  # Last week
        accuracy = training_module.get_accuracy_metrics()
        
        # Determine health status
        health_status = "healthy"
        issues = []
        
        # Check data volume
        if statistics.get("total_sessions", 0) < 10:
            health_status = "warning"
            issues.append("Low training data volume")
        
        # Check accuracy
        if accuracy.get("accuracy_rate", 0) < 75:
            health_status = "critical"
            issues.append("Low accuracy rate")
        
        # Check under-triage
        under_triage_rate = (accuracy.get("under_triage", 0) / max(accuracy.get("total_assessments", 1), 1)) * 100
        if under_triage_rate > 10:
            health_status = "critical"
            issues.append("High under-triage rate")
        
        health_data = {
            "status": health_status,
            "issues": issues,
            "metrics": {
                "sessions_last_7_days": statistics.get("total_sessions", 0),
                "accuracy_rate": accuracy.get("accuracy_rate", 0),
                "under_triage_rate": round(under_triage_rate, 2)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "data": health_data
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
