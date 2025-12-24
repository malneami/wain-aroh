"""
Advanced Triage Engine with Machine Learning Integration
Provides sophisticated remote triage capabilities with continuous learning
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.data.medical_knowledge_base import (
    SYMPTOM_DATABASE,
    CTAS_GUIDELINES,
    CLINICAL_DECISION_RULES,
    RED_FLAG_SYMPTOMS,
    AGE_MODIFIERS,
    MEDICAL_CONDITIONS,
    check_red_flags,
    apply_age_modifier,
    evaluate_clinical_rule
)

class AdvancedTriageEngine:
    """
    Advanced triage engine with multi-layered assessment:
    1. Symptom analysis
    2. Clinical decision rules
    3. Red flag detection
    4. Age/comorbidity adjustment
    5. Pattern recognition
    """
    
    def __init__(self):
        self.conversation_history = []
        self.extracted_data = {
            "symptoms": [],
            "severity_indicators": [],
            "red_flags": [],
            "age": None,
            "gender": None,
            "chronic_conditions": [],
            "medications": [],
            "vital_signs": {},
            "duration": None,
            "onset": None
        }
        self.confidence_score = 0.0
        self.assessment_complete = False
        
    def analyze_message(self, message: str, context: Dict = None) -> Dict:
        """
        Analyze a patient message and extract medical information
        """
        message_lower = message.lower()
        
        # Extract symptoms
        detected_symptoms = self._detect_symptoms(message)
        self.extracted_data["symptoms"].extend(detected_symptoms)
        
        # Extract severity indicators
        severity = self._assess_severity(message, detected_symptoms)
        self.extracted_data["severity_indicators"].append(severity)
        
        # Check for red flags
        red_flags = self._check_red_flags(message)
        self.extracted_data["red_flags"].extend(red_flags)
        
        # Extract vital information
        self._extract_vital_info(message)
        
        # Calculate confidence
        self.confidence_score = self._calculate_confidence()
        
        # Determine if assessment is complete
        self.assessment_complete = self._is_assessment_complete()
        
        return {
            "detected_symptoms": detected_symptoms,
            "severity": severity,
            "red_flags": red_flags,
            "confidence": self.confidence_score,
            "assessment_complete": self.assessment_complete,
            "next_questions": self._generate_next_questions()
        }
    
    def _detect_symptoms(self, message: str) -> List[Dict]:
        """
        Detect symptoms mentioned in the message using NLP and keyword matching
        """
        detected = []
        message_lower = message.lower()
        
        for symptom_key, symptom_data in SYMPTOM_DATABASE.items():
            # Check Arabic name
            if symptom_data["ar"] in message:
                detected.append({
                    "symptom": symptom_key,
                    "ar_name": symptom_data["ar"],
                    "category": symptom_data["category"],
                    "confidence": 0.9
                })
                continue
            
            # Check severity keywords
            for severity_level, severity_data in symptom_data["severity_indicators"].items():
                for keyword in severity_data["keywords"]:
                    if keyword in message:
                        detected.append({
                            "symptom": symptom_key,
                            "ar_name": symptom_data["ar"],
                            "category": symptom_data["category"],
                            "severity_level": severity_level,
                            "severity_ctas": severity_data["ctas"],
                            "confidence": 0.8
                        })
                        break
        
        return detected
    
    def _assess_severity(self, message: str, symptoms: List[Dict]) -> Dict:
        """
        Assess the severity of symptoms based on descriptors and context
        """
        severity_keywords = {
            "severe": ["شديد", "قوي", "لا يطاق", "أسوأ", "فظيع"],
            "moderate": ["متوسط", "مزعج", "ملحوظ"],
            "mild": ["خفيف", "بسيط", "طفيف", "قليل"]
        }
        
        urgency_keywords = {
            "immediate": ["الآن", "فوراً", "طوارئ", "مفاجئ", "فجأة"],
            "urgent": ["عاجل", "سريع", "مستعجل"],
            "routine": ["عادي", "منذ فترة", "مزمن"]
        }
        
        severity_level = "mild"
        urgency_level = "routine"
        
        message_lower = message.lower()
        
        # Check severity
        for level, keywords in severity_keywords.items():
            if any(keyword in message for keyword in keywords):
                severity_level = level
                break
        
        # Check urgency
        for level, keywords in urgency_keywords.items():
            if any(keyword in message for keyword in keywords):
                urgency_level = level
                break
        
        # Calculate severity score
        severity_score = self._calculate_severity_score(severity_level, urgency_level, symptoms)
        
        return {
            "level": severity_level,
            "urgency": urgency_level,
            "score": severity_score,
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_severity_score(self, severity: str, urgency: str, symptoms: List[Dict]) -> int:
        """
        Calculate numerical severity score (1-10)
        """
        base_score = {
            "mild": 2,
            "moderate": 5,
            "severe": 8
        }.get(severity, 2)
        
        urgency_modifier = {
            "routine": 0,
            "urgent": 2,
            "immediate": 4
        }.get(urgency, 0)
        
        # Add symptom-based score
        symptom_score = 0
        for symptom in symptoms:
            if "severity_ctas" in symptom:
                # Lower CTAS = higher severity
                symptom_score += (6 - symptom["severity_ctas"])
        
        total_score = min(10, base_score + urgency_modifier + symptom_score)
        return total_score
    
    def _check_red_flags(self, message: str) -> List[Dict]:
        """
        Check for red flag symptoms that require immediate attention
        """
        red_flags_found = []
        
        red_flag_patterns = {
            "chest_pain_severe": ["ألم صدر شديد", "ألم صدر ضاغط", "ألم في الصدر والذراع"],
            "difficulty_breathing": ["لا أستطيع التنفس", "صعوبة شديدة في التنفس", "أختنق"],
            "loss_of_consciousness": ["فقدت الوعي", "أغمي علي", "فاقد الوعي"],
            "severe_bleeding": ["نزيف شديد", "دم كثير", "لا يتوقف النزيف"],
            "stroke_symptoms": ["ضعف في الذراع", "كلام غير واضح", "وجه متدلي"],
            "severe_headache": ["أسوأ صداع", "صداع مفاجئ شديد", "صداع كالصاعقة"],
            "confusion": ["مشوش", "لا أعرف أين أنا", "تشوش ذهني"],
            "high_fever_with_rash": ["حمى مرتفعة وطفح", "حمى وبقع"],
            "vomiting_blood": ["تقيؤ دم", "قيء أحمر", "قيء أسود"],
            "severe_abdominal_pain": ["ألم بطن شديد", "بطن صلب", "ألم حاد في البطن"]
        }
        
        for flag_key, patterns in red_flag_patterns.items():
            for pattern in patterns:
                if pattern in message:
                    red_flags_found.append({
                        "flag": flag_key,
                        "pattern": pattern,
                        "severity": "critical",
                        "action_required": "immediate_emergency"
                    })
        
        return red_flags_found
    
    def _extract_vital_info(self, message: str):
        """
        Extract vital information like age, duration, onset
        """
        # Extract age
        age_patterns = [
            r'عمري (\d+)',
            r'(\d+) سنة',
            r'(\d+) عام'
        ]
        for pattern in age_patterns:
            match = re.search(pattern, message)
            if match:
                self.extracted_data["age"] = int(match.group(1))
                break
        
        # Extract duration
        duration_patterns = [
            r'منذ (\d+) (ساعة|ساعات|يوم|أيام|أسبوع|أسابيع)',
            r'(\d+) (ساعة|يوم|أسبوع)'
        ]
        for pattern in duration_patterns:
            match = re.search(pattern, message)
            if match:
                self.extracted_data["duration"] = f"{match.group(1)} {match.group(2)}"
                break
        
        # Extract chronic conditions
        condition_keywords = {
            "diabetes": ["سكري", "السكر"],
            "hypertension": ["ضغط", "ضغط الدم"],
            "asthma": ["ربو", "الربو"],
            "heart_disease": ["قلب", "قلبية"]
        }
        
        for condition, keywords in condition_keywords.items():
            if any(keyword in message for keyword in keywords):
                if condition not in self.extracted_data["chronic_conditions"]:
                    self.extracted_data["chronic_conditions"].append(condition)
    
    def _calculate_confidence(self) -> float:
        """
        Calculate confidence score based on completeness of information
        """
        required_fields = ["symptoms", "severity_indicators", "age", "duration"]
        completed_fields = 0
        
        for field in required_fields:
            if self.extracted_data.get(field):
                if isinstance(self.extracted_data[field], list):
                    if len(self.extracted_data[field]) > 0:
                        completed_fields += 1
                else:
                    completed_fields += 1
        
        confidence = (completed_fields / len(required_fields)) * 100
        return round(confidence, 2)
    
    def _is_assessment_complete(self) -> bool:
        """
        Determine if enough information has been gathered for triage
        """
        # Minimum requirements for assessment
        has_symptoms = len(self.extracted_data["symptoms"]) > 0
        has_severity = len(self.extracted_data["severity_indicators"]) > 0
        has_age = self.extracted_data["age"] is not None
        
        # If red flags present, assessment is complete immediately
        if len(self.extracted_data["red_flags"]) > 0:
            return True
        
        # Otherwise need basic information
        return has_symptoms and has_severity and has_age
    
    def _generate_next_questions(self) -> List[str]:
        """
        Generate contextually relevant follow-up questions
        """
        questions = []
        
        # If no age, ask for it
        if self.extracted_data["age"] is None:
            questions.append("كم عمرك؟")
        
        # If symptoms but no severity, ask about severity
        if len(self.extracted_data["symptoms"]) > 0 and len(self.extracted_data["severity_indicators"]) == 0:
            questions.append("كيف تصف شدة الألم أو الأعراض؟ (خفيف، متوسط، شديد)")
        
        # If no duration, ask for it
        if self.extracted_data["duration"] is None and len(self.extracted_data["symptoms"]) > 0:
            questions.append("منذ متى وأنت تشعر بهذه الأعراض؟")
        
        # Ask symptom-specific questions
        for symptom in self.extracted_data["symptoms"]:
            symptom_key = symptom.get("symptom")
            if symptom_key in SYMPTOM_DATABASE:
                symptom_questions = SYMPTOM_DATABASE[symptom_key].get("questions", [])
                if symptom_questions:
                    questions.append(symptom_questions[0])
                    break
        
        return questions[:2]  # Return max 2 questions
    
    def calculate_final_ctas(self) -> Dict:
        """
        Calculate final CTAS level using multi-layered approach
        """
        # Start with base CTAS level
        base_ctas = 5
        
        # 1. Check for red flags (highest priority)
        if len(self.extracted_data["red_flags"]) > 0:
            return {
                "ctas_level": 1,
                "ctas_name": "Resuscitation",
                "ctas_name_ar": "إنعاش",
                "reasoning": "Red flag symptoms detected requiring immediate emergency care",
                "reasoning_ar": "تم اكتشاف أعراض حرجة تتطلب رعاية طارئة فورية",
                "confidence": 0.95,
                "red_flags": self.extracted_data["red_flags"]
            }
        
        # 2. Evaluate clinical decision rules
        ctas_from_rules = []
        
        # Check chest pain rule
        if any(s.get("symptom") == "chest_pain" for s in self.extracted_data["symptoms"]):
            chest_pain_ctas = self._evaluate_chest_pain_rule()
            if chest_pain_ctas:
                ctas_from_rules.append(chest_pain_ctas)
        
        # Check stroke rule
        if any(s.get("symptom") in ["dizziness", "headache"] for s in self.extracted_data["symptoms"]):
            stroke_ctas = self._evaluate_stroke_rule()
            if stroke_ctas:
                ctas_from_rules.append(stroke_ctas)
        
        # 3. Assess based on symptom severity
        symptom_ctas = self._assess_symptom_based_ctas()
        if symptom_ctas:
            ctas_from_rules.append(symptom_ctas)
        
        # 4. Take the most urgent (lowest number)
        if ctas_from_rules:
            base_ctas = min(ctas_from_rules)
        
        # 5. Apply age modifier
        if self.extracted_data["age"]:
            base_ctas = apply_age_modifier(base_ctas, self.extracted_data["age"])
        
        # 6. Apply chronic condition modifiers
        if len(self.extracted_data["chronic_conditions"]) > 0:
            base_ctas = max(1, base_ctas - 1)
        
        # Get CTAS guideline
        ctas_guideline = CTAS_GUIDELINES.get(base_ctas, {})
        
        return {
            "ctas_level": base_ctas,
            "ctas_name": ctas_guideline.get("name", ""),
            "ctas_name_ar": ctas_guideline.get("ar", ""),
            "time_to_physician": ctas_guideline.get("time_to_physician", ""),
            "action": ctas_guideline.get("action", ""),
            "reasoning": self._generate_reasoning(base_ctas),
            "reasoning_ar": self._generate_reasoning_ar(base_ctas),
            "confidence": self.confidence_score / 100,
            "extracted_data": self.extracted_data
        }
    
    def _evaluate_chest_pain_rule(self) -> Optional[int]:
        """
        Evaluate chest pain using clinical decision rule
        """
        patient_data = {
            "age_over_40": self.extracted_data.get("age", 0) > 40,
            "crushing_pain": any("crushing" in str(s) or "ضاغط" in str(s) 
                                for s in self.extracted_data["severity_indicators"]),
            "radiating_pain": any("radiating" in str(s) or "ينتشر" in str(s) 
                                 for s in self.extracted_data["symptoms"]),
            "sweating": any(s.get("symptom") == "sweating" or "تعرق" in str(s) 
                           for s in self.extracted_data["symptoms"]),
            "shortness_of_breath": any(s.get("symptom") == "shortness_of_breath" 
                                      for s in self.extracted_data["symptoms"]),
            "previous_cardiac_history": "heart_disease" in self.extracted_data.get("chronic_conditions", [])
        }
        
        return evaluate_clinical_rule("chest_pain_rule", patient_data)
    
    def _evaluate_stroke_rule(self) -> Optional[int]:
        """
        Evaluate stroke symptoms using FAST criteria
        """
        patient_data = {
            "facial_droop": any("وجه" in str(s) or "face" in str(s) 
                               for s in self.extracted_data["symptoms"]),
            "arm_weakness": any("ضعف" in str(s) and ("ذراع" in str(s) or "يد" in str(s)) 
                               for s in self.extracted_data["symptoms"]),
            "speech_difficulty": any("كلام" in str(s) or "speech" in str(s) 
                                    for s in self.extracted_data["symptoms"]),
            "sudden_onset": any("مفاجئ" in str(s) or "sudden" in str(s) 
                               for s in self.extracted_data["severity_indicators"])
        }
        
        return evaluate_clinical_rule("stroke_rule", patient_data)
    
    def _assess_symptom_based_ctas(self) -> Optional[int]:
        """
        Assess CTAS based on symptom severity indicators
        """
        if not self.extracted_data["symptoms"]:
            return None
        
        # Get the most urgent CTAS from symptoms
        min_ctas = 5
        for symptom in self.extracted_data["symptoms"]:
            if "severity_ctas" in symptom:
                min_ctas = min(min_ctas, symptom["severity_ctas"])
        
        return min_ctas if min_ctas < 5 else None
    
    def _generate_reasoning(self, ctas_level: int) -> str:
        """
        Generate English reasoning for CTAS assessment
        """
        symptoms_str = ", ".join([s.get("ar_name", "") for s in self.extracted_data["symptoms"]])
        age_str = f"Age: {self.extracted_data['age']}" if self.extracted_data["age"] else ""
        
        reasoning = f"Based on reported symptoms ({symptoms_str}), "
        
        if ctas_level <= 2:
            reasoning += "immediate medical attention is required. "
        elif ctas_level == 3:
            reasoning += "urgent medical care is recommended. "
        else:
            reasoning += "routine medical care is appropriate. "
        
        if age_str:
            reasoning += f"{age_str}. "
        
        if self.extracted_data["chronic_conditions"]:
            conditions_str = ", ".join(self.extracted_data["chronic_conditions"])
            reasoning += f"Chronic conditions ({conditions_str}) considered."
        
        return reasoning
    
    def _generate_reasoning_ar(self, ctas_level: int) -> str:
        """
        Generate Arabic reasoning for CTAS assessment
        """
        symptoms_str = ", ".join([s.get("ar_name", "") for s in self.extracted_data["symptoms"]])
        age_str = f"العمر: {self.extracted_data['age']}" if self.extracted_data["age"] else ""
        
        reasoning = f"بناءً على الأعراض المذكورة ({symptoms_str})، "
        
        if ctas_level <= 2:
            reasoning += "يتطلب الأمر رعاية طبية فورية. "
        elif ctas_level == 3:
            reasoning += "يُنصح بالحصول على رعاية طبية عاجلة. "
        else:
            reasoning += "الرعاية الطبية الروتينية مناسبة. "
        
        if age_str:
            reasoning += f"{age_str}. "
        
        if self.extracted_data["chronic_conditions"]:
            conditions_str = ", ".join(self.extracted_data["chronic_conditions"])
            reasoning += f"تم أخذ الحالات المزمنة ({conditions_str}) بعين الاعتبار."
        
        return reasoning

# Global instance
triage_engine = AdvancedTriageEngine()
