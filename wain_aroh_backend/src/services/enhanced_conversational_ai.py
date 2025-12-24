"""
Enhanced Conversational AI Service
Integrates advanced triage engine with conversational interface
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from openai import OpenAI

# Import advanced triage components
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.services.advanced_triage_engine import AdvancedTriageEngine
from src.services.triage_training_module import training_module
from src.data.medical_knowledge_base import SYMPTOM_DATABASE, CTAS_GUIDELINES

class EnhancedConversationalAI:
    """
    Enhanced conversational AI with advanced triage capabilities
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.triage_engine = None
        self.conversation_history = []
        self.session_id = None
        self.session_start_time = None
        
    def start_new_session(self, session_id: str = None):
        """
        Start a new conversation session
        """
        self.session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_start_time = datetime.now()
        self.triage_engine = AdvancedTriageEngine()
        self.conversation_history = []
        
        welcome_message = self._generate_welcome_message()
        
        return {
            "session_id": self.session_id,
            "message": welcome_message,
            "status": "started"
        }
    
    def _generate_welcome_message(self) -> str:
        """
        Generate contextual welcome message
        """
        return """مرحباً بك في نظام وين أروح للتوجيه الصحي الذكي.

أنا هنا لمساعدتك في تحديد المكان المناسب للحصول على الرعاية الصحية بناءً على حالتك.

كيف يمكنني مساعدتك اليوم؟ ما الذي تشعر به؟"""
    
    def process_message(self, user_message: str, context: Dict = None) -> Dict:
        """
        Process user message with advanced triage analysis
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Analyze message with triage engine
        triage_analysis = self.triage_engine.analyze_message(user_message, context)
        
        # Generate AI response
        ai_response = self._generate_ai_response(user_message, triage_analysis)
        
        # Add AI response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": ai_response["message"],
            "timestamp": datetime.now().isoformat(),
            "triage_data": triage_analysis
        })
        
        # Check if assessment is complete
        if triage_analysis["assessment_complete"]:
            final_assessment = self.triage_engine.calculate_final_ctas()
            ai_response["final_assessment"] = final_assessment
            ai_response["recommendations"] = self._generate_recommendations(final_assessment)
            ai_response["status"] = "assessment_complete"
            
            # Record session for training
            self._record_session(final_assessment)
        else:
            ai_response["status"] = "gathering_information"
        
        return ai_response
    
    def _generate_ai_response(self, user_message: str, triage_analysis: Dict) -> Dict:
        """
        Generate contextual AI response using GPT
        """
        # Build system prompt with medical context
        system_prompt = self._build_system_prompt(triage_analysis)
        
        # Build conversation context
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent conversation history (last 5 messages)
        recent_history = self.conversation_history[-5:] if len(self.conversation_history) > 5 else self.conversation_history
        for msg in recent_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            ai_message = response.choices[0].message.content
            
            # Add follow-up questions if needed
            if triage_analysis["next_questions"]:
                ai_message += "\n\n" + triage_analysis["next_questions"][0]
            
            return {
                "message": ai_message,
                "detected_symptoms": triage_analysis["detected_symptoms"],
                "confidence": triage_analysis["confidence"],
                "red_flags": triage_analysis["red_flags"]
            }
            
        except Exception as e:
            # Fallback response
            fallback_message = "شكراً لمشاركة هذه المعلومات. "
            
            if triage_analysis["next_questions"]:
                fallback_message += triage_analysis["next_questions"][0]
            else:
                fallback_message += "هل يمكنك إخباري المزيد عن أعراضك؟"
            
            return {
                "message": fallback_message,
                "detected_symptoms": triage_analysis["detected_symptoms"],
                "confidence": triage_analysis["confidence"],
                "red_flags": triage_analysis["red_flags"],
                "error": str(e)
            }
    
    def _build_system_prompt(self, triage_analysis: Dict) -> str:
        """
        Build dynamic system prompt based on current triage state
        """
        base_prompt = """أنت مساعد طبي ذكي متخصص في تصنيف المرضى (Triage) وتوجيههم للرعاية الصحية المناسبة.

دورك:
1. جمع معلومات دقيقة عن أعراض المريض
2. تقييم مدى خطورة الحالة
3. طرح أسئلة محددة لفهم الحالة بشكل أفضل
4. التعامل بتعاطف واحترافية

إرشادات مهمة:
- استخدم لغة عربية واضحة وبسيطة
- اطرح سؤالاً واحداً في كل مرة
- كن متعاطفاً ومطمئناً
- لا تقدم تشخيصاً طبياً
- ركز على جمع المعلومات للتصنيف

"""
        
        # Add context about detected symptoms
        if triage_analysis["detected_symptoms"]:
            symptoms_list = ", ".join([s.get("ar_name", "") for s in triage_analysis["detected_symptoms"]])
            base_prompt += f"\nالأعراض المكتشفة حتى الآن: {symptoms_list}\n"
        
        # Add red flag warning
        if triage_analysis["red_flags"]:
            base_prompt += "\n⚠️ تنبيه: تم اكتشاف أعراض حرجة. يجب التعامل بحذر وسرعة.\n"
        
        # Add confidence level
        base_prompt += f"\nمستوى الثقة في التقييم الحالي: {triage_analysis['confidence']}%\n"
        
        # Add specific guidance based on confidence
        if triage_analysis["confidence"] < 50:
            base_prompt += "\nيجب جمع المزيد من المعلومات. ركز على: العمر، شدة الأعراض، مدة الأعراض.\n"
        
        return base_prompt
    
    def _generate_recommendations(self, assessment: Dict) -> Dict:
        """
        Generate detailed recommendations based on CTAS assessment
        """
        ctas_level = assessment["ctas_level"]
        ctas_data = CTAS_GUIDELINES.get(ctas_level, {})
        
        recommendations = {
            "ctas_level": ctas_level,
            "ctas_name": assessment["ctas_name"],
            "ctas_name_ar": assessment["ctas_name_ar"],
            "urgency": "",
            "urgency_ar": "",
            "action": ctas_data.get("action", ""),
            "facility_type": "",
            "time_frame": ctas_data.get("time_to_physician", ""),
            "instructions": [],
            "instructions_ar": []
        }
        
        # Set urgency and facility type based on CTAS
        if ctas_level <= 2:
            recommendations["urgency"] = "Emergency - Immediate"
            recommendations["urgency_ar"] = "طوارئ - فوري"
            recommendations["facility_type"] = "emergency"
            recommendations["instructions_ar"] = [
                "اذهب إلى أقرب قسم طوارئ فوراً",
                "إذا كنت لا تستطيع الوصول بنفسك، اتصل بالإسعاف (997)",
                "لا تقود السيارة بنفسك إذا كانت الأعراض شديدة"
            ]
        elif ctas_level == 3:
            recommendations["urgency"] = "Urgent"
            recommendations["urgency_ar"] = "عاجل"
            recommendations["facility_type"] = "urgent_care"
            recommendations["instructions_ar"] = [
                "توجه إلى مركز الرعاية العاجلة أو قسم الطوارئ",
                "يُفضل الوصول خلال 30 دقيقة",
                "أحضر معك قائمة بالأدوية التي تتناولها"
            ]
        elif ctas_level == 4:
            recommendations["urgency"] = "Less Urgent"
            recommendations["urgency_ar"] = "أقل إلحاحاً"
            recommendations["facility_type"] = "clinic"
            recommendations["instructions_ar"] = [
                "يمكنك حجز موعد في العيادة",
                "يُفضل المراجعة خلال 24 ساعة",
                "راقب الأعراض وإذا ساءت توجه للطوارئ"
            ]
        else:
            recommendations["urgency"] = "Non-urgent"
            recommendations["urgency_ar"] = "غير عاجل"
            recommendations["facility_type"] = "clinic_or_virtual"
            recommendations["instructions_ar"] = [
                "يمكنك حجز موعد روتيني في العيادة",
                "أو استخدام الاستشارة الطبية عن بُعد",
                "لا حاجة للتوجه للطوارئ"
            ]
        
        return recommendations
    
    def _record_session(self, final_assessment: Dict):
        """
        Record completed session for training
        """
        session_data = {
            "session_id": self.session_id,
            "age": self.triage_engine.extracted_data.get("age"),
            "gender": self.triage_engine.extracted_data.get("gender"),
            "chronic_conditions": self.triage_engine.extracted_data.get("chronic_conditions", []),
            "conversation": self.conversation_history,
            "symptoms": self.triage_engine.extracted_data.get("symptoms", []),
            "severity_indicators": self.triage_engine.extracted_data.get("severity_indicators", []),
            "red_flags": self.triage_engine.extracted_data.get("red_flags", []),
            "ctas_level": final_assessment["ctas_level"],
            "confidence": final_assessment["confidence"],
            "reasoning": final_assessment["reasoning_ar"]
        }
        
        try:
            training_module.record_triage_session(session_data)
        except Exception as e:
            print(f"Error recording session: {e}")
    
    def get_session_summary(self) -> Dict:
        """
        Get summary of current session
        """
        return {
            "session_id": self.session_id,
            "duration": str(datetime.now() - self.session_start_time) if self.session_start_time else None,
            "message_count": len(self.conversation_history),
            "symptoms_detected": len(self.triage_engine.extracted_data.get("symptoms", [])) if self.triage_engine else 0,
            "confidence": self.triage_engine.confidence_score if self.triage_engine else 0,
            "assessment_complete": self.triage_engine.assessment_complete if self.triage_engine else False
        }

# Create global instance
enhanced_ai = EnhancedConversationalAI()
