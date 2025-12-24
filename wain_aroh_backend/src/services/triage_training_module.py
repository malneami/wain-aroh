"""
Training and Analytics Module for Continuous AI Improvement
Collects data, analyzes patterns, and improves triage accuracy over time
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
from collections import defaultdict, Counter

class TriageTrainingModule:
    """
    Manages training data collection and analysis for continuous improvement
    """
    
    def __init__(self, data_dir="/home/ubuntu/wain-aroh/wain_aroh_backend/training_data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.training_data_file = os.path.join(data_dir, "triage_training_data.jsonl")
        self.analytics_file = os.path.join(data_dir, "triage_analytics.json")
        
    def record_triage_session(self, session_data: Dict):
        """
        Record a complete triage session for training
        """
        session_record = {
            "session_id": session_data.get("session_id"),
            "timestamp": datetime.now().isoformat(),
            "patient_data": {
                "age": session_data.get("age"),
                "gender": session_data.get("gender"),
                "chronic_conditions": session_data.get("chronic_conditions", [])
            },
            "conversation": session_data.get("conversation", []),
            "symptoms_detected": session_data.get("symptoms", []),
            "severity_indicators": session_data.get("severity_indicators", []),
            "red_flags": session_data.get("red_flags", []),
            "ai_assessment": {
                "ctas_level": session_data.get("ctas_level"),
                "confidence": session_data.get("confidence"),
                "reasoning": session_data.get("reasoning")
            },
            "outcome": {
                "facility_type": session_data.get("facility_type"),
                "facility_name": session_data.get("facility_name"),
                "patient_accepted": session_data.get("patient_accepted", True)
            },
            "feedback": session_data.get("feedback")
        }
        
        # Append to training data file
        with open(self.training_data_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(session_record, ensure_ascii=False) + '\n')
        
        return session_record
    
    def get_training_statistics(self, days=30) -> Dict:
        """
        Get training statistics for the last N days
        """
        if not os.path.exists(self.training_data_file):
            return {"error": "No training data available"}
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        stats = {
            "total_sessions": 0,
            "ctas_distribution": defaultdict(int),
            "symptom_frequency": defaultdict(int),
            "average_confidence": 0.0,
            "red_flag_frequency": defaultdict(int),
            "facility_type_distribution": defaultdict(int),
            "age_distribution": {
                "0-17": 0,
                "18-40": 0,
                "41-65": 0,
                "65+": 0
            },
            "patient_acceptance_rate": 0.0,
            "common_symptom_combinations": []
        }
        
        confidence_scores = []
        acceptance_count = 0
        symptom_combinations = []
        
        with open(self.training_data_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    session = json.loads(line)
                    session_date = datetime.fromisoformat(session["timestamp"])
                    
                    if session_date < cutoff_date:
                        continue
                    
                    stats["total_sessions"] += 1
                    
                    # CTAS distribution
                    ctas_level = session["ai_assessment"]["ctas_level"]
                    stats["ctas_distribution"][f"CTAS {ctas_level}"] += 1
                    
                    # Symptom frequency
                    symptoms = session["symptoms_detected"]
                    for symptom in symptoms:
                        symptom_name = symptom.get("ar_name", symptom.get("symptom"))
                        stats["symptom_frequency"][symptom_name] += 1
                    
                    # Symptom combinations
                    if len(symptoms) > 1:
                        symptom_names = tuple(sorted([s.get("ar_name", s.get("symptom")) for s in symptoms]))
                        symptom_combinations.append(symptom_names)
                    
                    # Confidence scores
                    confidence = session["ai_assessment"]["confidence"]
                    if confidence:
                        confidence_scores.append(confidence)
                    
                    # Red flags
                    for red_flag in session["red_flags"]:
                        flag_name = red_flag.get("flag", "unknown")
                        stats["red_flag_frequency"][flag_name] += 1
                    
                    # Facility type
                    facility_type = session["outcome"].get("facility_type", "unknown")
                    stats["facility_type_distribution"][facility_type] += 1
                    
                    # Age distribution
                    age = session["patient_data"].get("age")
                    if age:
                        if age < 18:
                            stats["age_distribution"]["0-17"] += 1
                        elif age < 41:
                            stats["age_distribution"]["18-40"] += 1
                        elif age < 66:
                            stats["age_distribution"]["41-65"] += 1
                        else:
                            stats["age_distribution"]["65+"] += 1
                    
                    # Patient acceptance
                    if session["outcome"].get("patient_accepted", True):
                        acceptance_count += 1
                        
                except Exception as e:
                    continue
        
        # Calculate averages
        if confidence_scores:
            stats["average_confidence"] = round(sum(confidence_scores) / len(confidence_scores), 2)
        
        if stats["total_sessions"] > 0:
            stats["patient_acceptance_rate"] = round((acceptance_count / stats["total_sessions"]) * 100, 2)
        
        # Find common symptom combinations
        if symptom_combinations:
            combination_counts = Counter(symptom_combinations)
            stats["common_symptom_combinations"] = [
                {"symptoms": list(combo), "count": count}
                for combo, count in combination_counts.most_common(10)
            ]
        
        # Convert defaultdicts to regular dicts
        stats["ctas_distribution"] = dict(stats["ctas_distribution"])
        stats["symptom_frequency"] = dict(sorted(
            stats["symptom_frequency"].items(),
            key=lambda x: x[1],
            reverse=True
        )[:20])  # Top 20 symptoms
        stats["red_flag_frequency"] = dict(stats["red_flag_frequency"])
        stats["facility_type_distribution"] = dict(stats["facility_type_distribution"])
        
        # Save analytics
        with open(self.analytics_file, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_at": datetime.now().isoformat(),
                "period_days": days,
                "statistics": stats
            }, f, ensure_ascii=False, indent=2)
        
        return stats
    
    def get_accuracy_metrics(self) -> Dict:
        """
        Calculate accuracy metrics based on feedback and outcomes
        """
        if not os.path.exists(self.training_data_file):
            return {"error": "No training data available"}
        
        metrics = {
            "total_assessments": 0,
            "correct_assessments": 0,
            "over_triage": 0,  # Assessed as more urgent than needed
            "under_triage": 0,  # Assessed as less urgent than needed
            "accuracy_rate": 0.0,
            "ctas_accuracy_by_level": defaultdict(lambda: {"total": 0, "correct": 0})
        }
        
        with open(self.training_data_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    session = json.loads(line)
                    feedback = session.get("feedback")
                    
                    if not feedback:
                        continue
                    
                    metrics["total_assessments"] += 1
                    ai_ctas = session["ai_assessment"]["ctas_level"]
                    actual_ctas = feedback.get("actual_ctas")
                    
                    if actual_ctas:
                        metrics["ctas_accuracy_by_level"][f"CTAS {ai_ctas}"]["total"] += 1
                        
                        if ai_ctas == actual_ctas:
                            metrics["correct_assessments"] += 1
                            metrics["ctas_accuracy_by_level"][f"CTAS {ai_ctas}"]["correct"] += 1
                        elif ai_ctas < actual_ctas:
                            metrics["over_triage"] += 1
                        else:
                            metrics["under_triage"] += 1
                            
                except Exception as e:
                    continue
        
        if metrics["total_assessments"] > 0:
            metrics["accuracy_rate"] = round(
                (metrics["correct_assessments"] / metrics["total_assessments"]) * 100, 2
            )
        
        # Calculate accuracy by CTAS level
        ctas_accuracy = {}
        for level, data in metrics["ctas_accuracy_by_level"].items():
            if data["total"] > 0:
                ctas_accuracy[level] = {
                    "total": data["total"],
                    "correct": data["correct"],
                    "accuracy": round((data["correct"] / data["total"]) * 100, 2)
                }
        
        metrics["ctas_accuracy_by_level"] = ctas_accuracy
        
        return metrics
    
    def get_improvement_recommendations(self) -> List[Dict]:
        """
        Generate recommendations for improving triage accuracy
        """
        stats = self.get_training_statistics(days=30)
        accuracy = self.get_accuracy_metrics()
        
        recommendations = []
        
        # Check overall accuracy
        if accuracy.get("accuracy_rate", 0) < 80:
            recommendations.append({
                "priority": "high",
                "area": "Overall Accuracy",
                "issue": f"Current accuracy rate is {accuracy.get('accuracy_rate', 0)}%",
                "recommendation": "Review and refine symptom detection algorithms. Consider adding more training data.",
                "recommendation_ar": "مراجعة وتحسين خوارزميات اكتشاف الأعراض. النظر في إضافة المزيد من بيانات التدريب."
            })
        
        # Check under-triage rate
        under_triage_rate = 0
        if accuracy.get("total_assessments", 0) > 0:
            under_triage_rate = (accuracy.get("under_triage", 0) / accuracy["total_assessments"]) * 100
        
        if under_triage_rate > 10:
            recommendations.append({
                "priority": "critical",
                "area": "Under-Triage",
                "issue": f"Under-triage rate is {round(under_triage_rate, 2)}%",
                "recommendation": "Increase sensitivity for red flag symptoms. Review missed critical cases.",
                "recommendation_ar": "زيادة الحساسية للأعراض الحرجة. مراجعة الحالات الحرجة المفقودة."
            })
        
        # Check confidence scores
        if stats.get("average_confidence", 0) < 70:
            recommendations.append({
                "priority": "medium",
                "area": "Confidence Scores",
                "issue": f"Average confidence is {stats.get('average_confidence', 0)}%",
                "recommendation": "Improve data collection completeness. Add more structured questions.",
                "recommendation_ar": "تحسين اكتمال جمع البيانات. إضافة المزيد من الأسئلة المنظمة."
            })
        
        # Check patient acceptance rate
        if stats.get("patient_acceptance_rate", 0) < 80:
            recommendations.append({
                "priority": "medium",
                "area": "Patient Acceptance",
                "issue": f"Patient acceptance rate is {stats.get('patient_acceptance_rate', 0)}%",
                "recommendation": "Review recommendation communication. Improve explanation of triage decisions.",
                "recommendation_ar": "مراجعة توصيل التوصيات. تحسين شرح قرارات التصنيف."
            })
        
        # Check for data gaps
        if stats.get("total_sessions", 0) < 100:
            recommendations.append({
                "priority": "low",
                "area": "Training Data",
                "issue": f"Only {stats.get('total_sessions', 0)} sessions recorded",
                "recommendation": "Collect more training data to improve model accuracy.",
                "recommendation_ar": "جمع المزيد من بيانات التدريب لتحسين دقة النموذج."
            })
        
        return recommendations
    
    def export_training_dataset(self, output_file: str = None) -> str:
        """
        Export training data in a format suitable for ML training
        """
        if output_file is None:
            output_file = os.path.join(self.data_dir, f"ml_training_data_{datetime.now().strftime('%Y%m%d')}.json")
        
        training_dataset = []
        
        if not os.path.exists(self.training_data_file):
            return output_file
        
        with open(self.training_data_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    session = json.loads(line)
                    
                    # Extract features for ML
                    features = {
                        "age": session["patient_data"].get("age"),
                        "gender": session["patient_data"].get("gender"),
                        "has_chronic_conditions": len(session["patient_data"].get("chronic_conditions", [])) > 0,
                        "num_symptoms": len(session["symptoms_detected"]),
                        "symptoms": [s.get("symptom") for s in session["symptoms_detected"]],
                        "has_red_flags": len(session["red_flags"]) > 0,
                        "severity_score": session["severity_indicators"][0].get("score") if session["severity_indicators"] else 0
                    }
                    
                    # Label (target)
                    label = session["ai_assessment"]["ctas_level"]
                    
                    # Add feedback if available
                    feedback_label = None
                    if session.get("feedback"):
                        feedback_label = session["feedback"].get("actual_ctas")
                    
                    training_dataset.append({
                        "features": features,
                        "label": label,
                        "feedback_label": feedback_label,
                        "session_id": session["session_id"]
                    })
                    
                except Exception as e:
                    continue
        
        # Save dataset
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(training_dataset, f, ensure_ascii=False, indent=2)
        
        return output_file

# Global instance
training_module = TriageTrainingModule()
