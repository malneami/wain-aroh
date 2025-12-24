"""
Comprehensive Medical Knowledge Base for Remote Triage
Contains extensive symptom databases, clinical guidelines, and decision support data
"""

# Comprehensive Symptom Database with Clinical Significance
SYMPTOM_DATABASE = {
    # Cardiovascular Symptoms
    "chest_pain": {
        "ar": "ألم في الصدر",
        "category": "cardiovascular",
        "severity_indicators": {
            "crushing": {"ctas": 1, "keywords": ["ضاغط", "سحق", "ثقيل"]},
            "radiating": {"ctas": 1, "keywords": ["ينتشر", "يمتد", "الذراع", "الفك"]},
            "sudden_onset": {"ctas": 1, "keywords": ["مفاجئ", "فجأة"]},
            "with_sweating": {"ctas": 1, "keywords": ["تعرق", "عرق"]},
            "sharp": {"ctas": 2, "keywords": ["حاد", "طعن"]},
            "dull": {"ctas": 3, "keywords": ["خفيف", "مزعج"]}
        },
        "red_flags": ["shortness_of_breath", "sweating", "nausea", "arm_pain"],
        "differential_diagnosis": ["MI", "angina", "pulmonary_embolism", "aortic_dissection"],
        "questions": [
            "هل الألم ضاغط أم حاد؟",
            "هل ينتشر الألم إلى الذراع أو الفك؟",
            "هل بدأ الألم فجأة؟",
            "هل تشعر بضيق في التنفس؟"
        ]
    },
    
    "shortness_of_breath": {
        "ar": "ضيق في التنفس",
        "category": "respiratory",
        "severity_indicators": {
            "at_rest": {"ctas": 1, "keywords": ["راحة", "جالس", "نائم"]},
            "unable_to_speak": {"ctas": 1, "keywords": ["لا أستطيع الكلام", "صعوبة الكلام"]},
            "with_chest_pain": {"ctas": 1, "keywords": ["ألم صدر"]},
            "on_exertion": {"ctas": 3, "keywords": ["مجهود", "حركة", "مشي"]},
            "mild": {"ctas": 4, "keywords": ["خفيف", "بسيط"]}
        },
        "red_flags": ["chest_pain", "cyanosis", "altered_consciousness"],
        "differential_diagnosis": ["PE", "pneumonia", "CHF", "asthma", "COPD"],
        "questions": [
            "هل ضيق التنفس يحدث أثناء الراحة؟",
            "هل تستطيع التحدث بجمل كاملة؟",
            "هل لديك ألم في الصدر؟",
            "منذ متى وأنت تشعر بهذا؟"
        ]
    },
    
    "headache": {
        "ar": "صداع",
        "category": "neurological",
        "severity_indicators": {
            "thunderclap": {"ctas": 1, "keywords": ["مفاجئ", "أسوأ صداع", "صاعقة"]},
            "with_fever_stiff_neck": {"ctas": 1, "keywords": ["حمى", "تصلب الرقبة"]},
            "with_vision_changes": {"ctas": 2, "keywords": ["زغللة", "رؤية مزدوجة"]},
            "migraine": {"ctas": 3, "keywords": ["نصفي", "غثيان", "حساسية للضوء"]},
            "tension": {"ctas": 4, "keywords": ["ضاغط", "حول الرأس"]}
        },
        "red_flags": ["sudden_onset", "worst_ever", "fever", "stiff_neck", "vision_changes"],
        "differential_diagnosis": ["SAH", "meningitis", "migraine", "tension_headache"],
        "questions": [
            "هل بدأ الصداع فجأة؟",
            "هل هذا أسوأ صداع شعرت به؟",
            "هل لديك حمى أو تصلب في الرقبة؟",
            "هل لديك تغيرات في الرؤية؟"
        ]
    },
    
    "abdominal_pain": {
        "ar": "ألم في البطن",
        "category": "gastrointestinal",
        "severity_indicators": {
            "severe_sudden": {"ctas": 1, "keywords": ["شديد", "مفاجئ", "لا يطاق"]},
            "with_vomiting_blood": {"ctas": 1, "keywords": ["تقيؤ دم", "براز أسود"]},
            "right_lower_quadrant": {"ctas": 2, "keywords": ["أسفل اليمين", "حول السرة"]},
            "cramping": {"ctas": 3, "keywords": ["مغص", "تقلصات"]},
            "mild": {"ctas": 4, "keywords": ["خفيف", "بسيط"]}
        },
        "red_flags": ["rigid_abdomen", "vomiting_blood", "severe_pain", "fever"],
        "differential_diagnosis": ["appendicitis", "cholecystitis", "perforation", "obstruction"],
        "questions": [
            "أين بالضبط موقع الألم؟",
            "هل الألم ثابت أم متقطع؟",
            "هل لديك قيء أو إسهال؟",
            "هل لديك حمى؟"
        ]
    },
    
    "fever": {
        "ar": "حمى",
        "category": "infectious",
        "severity_indicators": {
            "high_with_rash": {"ctas": 1, "keywords": ["طفح", "بقع", "نزيف"]},
            "with_confusion": {"ctas": 1, "keywords": ["تشوش", "هذيان"]},
            "high_persistent": {"ctas": 2, "keywords": ["مرتفعة", "مستمرة", "39"]},
            "moderate": {"ctas": 3, "keywords": ["38", "متوسطة"]},
            "low_grade": {"ctas": 4, "keywords": ["37.5", "خفيفة"]}
        },
        "red_flags": ["rash", "confusion", "stiff_neck", "difficulty_breathing"],
        "differential_diagnosis": ["sepsis", "meningitis", "pneumonia", "URI", "UTI"],
        "questions": [
            "كم درجة حرارتك؟",
            "منذ متى وأنت تعاني من الحمى؟",
            "هل لديك أعراض أخرى؟",
            "هل لديك طفح جلدي؟"
        ]
    },
    
    "dizziness": {
        "ar": "دوخة",
        "category": "neurological",
        "severity_indicators": {
            "with_chest_pain": {"ctas": 1, "keywords": ["ألم صدر", "ضيق تنفس"]},
            "with_weakness": {"ctas": 2, "keywords": ["ضعف", "تنميل", "كلام غير واضح"]},
            "vertigo": {"ctas": 3, "keywords": ["دوار", "غرفة تدور"]},
            "lightheaded": {"ctas": 4, "keywords": ["خفة رأس", "عدم توازن"]}
        },
        "red_flags": ["chest_pain", "weakness", "speech_difficulty", "vision_changes"],
        "differential_diagnosis": ["stroke", "cardiac", "vertigo", "orthostatic_hypotension"],
        "questions": [
            "هل تشعر أن الغرفة تدور؟",
            "هل لديك ضعف أو تنميل؟",
            "هل لديك صعوبة في الكلام؟",
            "متى بدأت الدوخة؟"
        ]
    },
    
    "cough": {
        "ar": "سعال",
        "category": "respiratory",
        "severity_indicators": {
            "with_blood": {"ctas": 2, "keywords": ["دم", "نزيف"]},
            "severe_with_fever": {"ctas": 2, "keywords": ["شديد", "حمى", "صعوبة تنفس"]},
            "persistent": {"ctas": 3, "keywords": ["مستمر", "أسبوعين"]},
            "dry": {"ctas": 4, "keywords": ["جاف", "بدون بلغم"]},
            "productive": {"ctas": 4, "keywords": ["بلغم", "مخاط"]}
        },
        "red_flags": ["hemoptysis", "severe_dyspnea", "chest_pain", "weight_loss"],
        "differential_diagnosis": ["pneumonia", "TB", "bronchitis", "URI", "COPD"],
        "questions": [
            "هل السعال جاف أم مع بلغم؟",
            "هل يوجد دم في البلغم؟",
            "منذ متى وأنت تسعل؟",
            "هل لديك حمى؟"
        ]
    },
    
    "nausea_vomiting": {
        "ar": "غثيان وتقيؤ",
        "category": "gastrointestinal",
        "severity_indicators": {
            "with_blood": {"ctas": 1, "keywords": ["دم", "أحمر", "أسود"]},
            "severe_dehydration": {"ctas": 2, "keywords": ["جفاف", "لا يستطيع الشرب"]},
            "persistent": {"ctas": 3, "keywords": ["مستمر", "متكرر"]},
            "mild": {"ctas": 4, "keywords": ["خفيف", "مرة واحدة"]}
        },
        "red_flags": ["vomiting_blood", "severe_abdominal_pain", "dehydration"],
        "differential_diagnosis": ["gastroenteritis", "obstruction", "pregnancy", "medication"],
        "questions": [
            "هل يوجد دم في القيء؟",
            "كم مرة تقيأت؟",
            "هل تستطيع شرب السوائل؟",
            "هل لديك ألم في البطن؟"
        ]
    },
    
    "back_pain": {
        "ar": "ألم في الظهر",
        "category": "musculoskeletal",
        "severity_indicators": {
            "with_leg_weakness": {"ctas": 2, "keywords": ["ضعف الساق", "تنميل", "صعوبة المشي"]},
            "severe_trauma": {"ctas": 2, "keywords": ["حادث", "سقوط", "إصابة"]},
            "chronic": {"ctas": 4, "keywords": ["مزمن", "أسابيع", "متكرر"]},
            "acute": {"ctas": 3, "keywords": ["حاد", "مفاجئ"]}
        },
        "red_flags": ["leg_weakness", "bowel_bladder_dysfunction", "trauma", "fever"],
        "differential_diagnosis": ["herniated_disc", "spinal_stenosis", "fracture", "strain"],
        "questions": [
            "هل لديك ضعف أو تنميل في الساقين؟",
            "هل تعرضت لإصابة أو حادث؟",
            "هل لديك صعوبة في التبول؟",
            "منذ متى وأنت تشعر بالألم؟"
        ]
    },
    
    "rash": {
        "ar": "طفح جلدي",
        "category": "dermatological",
        "severity_indicators": {
            "with_fever_purpura": {"ctas": 1, "keywords": ["حمى", "بقع نزفية", "لا تختفي بالضغط"]},
            "severe_allergic": {"ctas": 2, "keywords": ["تورم", "صعوبة تنفس", "حكة شديدة"]},
            "widespread": {"ctas": 3, "keywords": ["منتشر", "كل الجسم"]},
            "localized": {"ctas": 4, "keywords": ["موضعي", "منطقة صغيرة"]}
        },
        "red_flags": ["fever", "non_blanching", "respiratory_symptoms", "facial_swelling"],
        "differential_diagnosis": ["meningococcemia", "allergic_reaction", "viral_exanthem", "dermatitis"],
        "questions": [
            "هل لديك حمى؟",
            "هل الطفح يختفي عند الضغط عليه؟",
            "هل لديك صعوبة في التنفس؟",
            "متى ظهر الطفح؟"
        ]
    }
}

# CTAS (Canadian Triage and Acuity Scale) Guidelines
CTAS_GUIDELINES = {
    1: {
        "name": "Resuscitation",
        "ar": "إنعاش",
        "time_to_physician": "0 minutes",
        "description": "Conditions threatening life or limb requiring immediate intervention",
        "examples": [
            "Cardiac arrest",
            "Major trauma with shock",
            "Severe respiratory distress",
            "Unconscious/unresponsive"
        ],
        "keywords": ["فاقد الوعي", "لا يتنفس", "نزيف شديد", "ألم صدر ساحق"],
        "action": "emergency_immediate"
    },
    2: {
        "name": "Emergent",
        "ar": "طارئ",
        "time_to_physician": "15 minutes",
        "description": "Conditions that are a potential threat to life, limb or function",
        "examples": [
            "Chest pain (possible MI)",
            "Severe trauma",
            "Altered level of consciousness",
            "Severe pain"
        ],
        "keywords": ["ألم صدر", "إصابة شديدة", "تشوش ذهني", "ألم شديد"],
        "action": "emergency_urgent"
    },
    3: {
        "name": "Urgent",
        "ar": "عاجل",
        "time_to_physician": "30 minutes",
        "description": "Conditions that could potentially progress to serious problem",
        "examples": [
            "Moderate trauma",
            "Abdominal pain",
            "Persistent vomiting",
            "Moderate asthma"
        ],
        "keywords": ["ألم متوسط", "قيء مستمر", "حمى مرتفعة"],
        "action": "urgent_care"
    },
    4: {
        "name": "Less Urgent",
        "ar": "أقل إلحاحاً",
        "time_to_physician": "60 minutes",
        "description": "Conditions related to patient age, distress, or potential complications",
        "examples": [
            "Minor trauma",
            "Mild abdominal pain",
            "Cough and cold symptoms",
            "Minor lacerations"
        ],
        "keywords": ["إصابة بسيطة", "ألم خفيف", "سعال", "جرح صغير"],
        "action": "clinic_appointment"
    },
    5: {
        "name": "Non-urgent",
        "ar": "غير عاجل",
        "time_to_physician": "120 minutes",
        "description": "Conditions that may be acute but non-urgent or chronic",
        "examples": [
            "Minor symptoms",
            "Chronic conditions",
            "Prescription refills",
            "Health education"
        ],
        "keywords": ["أعراض بسيطة", "حالة مزمنة", "استشارة"],
        "action": "clinic_or_virtual"
    }
}

# Clinical Decision Support Rules
CLINICAL_DECISION_RULES = {
    "chest_pain_rule": {
        "name": "Chest Pain Decision Rule",
        "conditions": {
            "age_over_40": 1,
            "crushing_pain": 2,
            "radiating_pain": 2,
            "sweating": 1,
            "shortness_of_breath": 2,
            "nausea": 1,
            "previous_cardiac_history": 2
        },
        "thresholds": {
            "high_risk": 5,  # CTAS 1
            "moderate_risk": 3,  # CTAS 2
            "low_risk": 0  # CTAS 3
        }
    },
    
    "stroke_rule": {
        "name": "FAST (Face, Arms, Speech, Time)",
        "conditions": {
            "facial_droop": 3,
            "arm_weakness": 3,
            "speech_difficulty": 3,
            "sudden_onset": 2
        },
        "thresholds": {
            "high_risk": 3,  # CTAS 1
            "moderate_risk": 0,
            "low_risk": 0
        }
    },
    
    "sepsis_rule": {
        "name": "qSOFA (Quick Sequential Organ Failure Assessment)",
        "conditions": {
            "altered_mental_status": 1,
            "respiratory_rate_high": 1,
            "low_blood_pressure": 1,
            "fever": 1
        },
        "thresholds": {
            "high_risk": 2,  # CTAS 1
            "moderate_risk": 1,  # CTAS 2
            "low_risk": 0
        }
    },
    
    "trauma_rule": {
        "name": "Trauma Assessment",
        "conditions": {
            "mechanism_high_energy": 2,
            "multiple_injuries": 2,
            "head_injury": 2,
            "chest_injury": 2,
            "abdominal_injury": 2,
            "limb_deformity": 1
        },
        "thresholds": {
            "high_risk": 4,  # CTAS 1
            "moderate_risk": 2,  # CTAS 2
            "low_risk": 0  # CTAS 3
        }
    }
}

# Red Flag Symptoms (Always require immediate attention)
RED_FLAG_SYMPTOMS = {
    "cardiovascular": [
        "crushing_chest_pain",
        "chest_pain_with_sweating",
        "severe_shortness_of_breath",
        "sudden_collapse",
        "irregular_heartbeat_with_dizziness"
    ],
    "neurological": [
        "sudden_severe_headache",
        "loss_of_consciousness",
        "seizure",
        "facial_droop",
        "arm_weakness",
        "speech_difficulty",
        "confusion_altered_mental_status"
    ],
    "respiratory": [
        "unable_to_speak_full_sentences",
        "blue_lips_or_face",
        "severe_difficulty_breathing",
        "coughing_blood"
    ],
    "gastrointestinal": [
        "vomiting_blood",
        "severe_abdominal_pain",
        "rigid_abdomen",
        "black_tarry_stools"
    ],
    "infectious": [
        "high_fever_with_rash",
        "stiff_neck_with_fever",
        "severe_dehydration",
        "signs_of_sepsis"
    ],
    "trauma": [
        "major_bleeding",
        "suspected_fracture",
        "head_injury_with_confusion",
        "penetrating_injury"
    ]
}

# Age-Specific Considerations
AGE_MODIFIERS = {
    "infant": {
        "age_range": [0, 1],
        "severity_multiplier": 1.5,
        "special_considerations": [
            "Higher risk for dehydration",
            "Fever in infants <3 months always urgent",
            "Difficulty breathing more serious",
            "Lethargy concerning"
        ]
    },
    "child": {
        "age_range": [1, 12],
        "severity_multiplier": 1.3,
        "special_considerations": [
            "Assess hydration status carefully",
            "Consider developmental milestones",
            "Parent concern is important"
        ]
    },
    "adult": {
        "age_range": [18, 65],
        "severity_multiplier": 1.0,
        "special_considerations": [
            "Consider chronic conditions",
            "Medication interactions"
        ]
    },
    "elderly": {
        "age_range": [65, 120],
        "severity_multiplier": 1.4,
        "special_considerations": [
            "Atypical presentations common",
            "Higher risk for complications",
            "Consider polypharmacy",
            "Falls risk assessment"
        ]
    }
}

# Common Medical Conditions Database
MEDICAL_CONDITIONS = {
    "diabetes": {
        "ar": "السكري",
        "risk_factors": ["hyperglycemia", "hypoglycemia", "infection"],
        "complications": ["DKA", "HHS", "foot_ulcers"],
        "urgency_modifiers": {
            "confusion": +2,
            "severe_hyperglycemia": +2,
            "infection": +1
        }
    },
    "hypertension": {
        "ar": "ارتفاع ضغط الدم",
        "risk_factors": ["stroke", "MI", "kidney_disease"],
        "complications": ["hypertensive_emergency", "stroke", "MI"],
        "urgency_modifiers": {
            "severe_headache": +2,
            "chest_pain": +2,
            "vision_changes": +1
        }
    },
    "asthma": {
        "ar": "الربو",
        "risk_factors": ["respiratory_infection", "allergens"],
        "complications": ["status_asthmaticus", "respiratory_failure"],
        "urgency_modifiers": {
            "unable_to_speak": +3,
            "severe_wheezing": +2,
            "no_relief_from_inhaler": +1
        }
    },
    "heart_disease": {
        "ar": "أمراض القلب",
        "risk_factors": ["MI", "CHF", "arrhythmia"],
        "complications": ["MI", "CHF_exacerbation", "sudden_death"],
        "urgency_modifiers": {
            "chest_pain": +3,
            "shortness_of_breath": +2,
            "palpitations": +1
        }
    }
}

# Medication Interactions and Considerations
MEDICATION_CONSIDERATIONS = {
    "anticoagulants": {
        "examples": ["warfarin", "rivaroxaban", "apixaban"],
        "concerns": ["bleeding_risk", "trauma", "falls"],
        "urgency_modifier": +1
    },
    "immunosuppressants": {
        "examples": ["prednisone", "methotrexate", "biologics"],
        "concerns": ["infection_risk", "fever"],
        "urgency_modifier": +1
    },
    "insulin": {
        "examples": ["insulin", "oral_hypoglycemics"],
        "concerns": ["hypoglycemia", "confusion"],
        "urgency_modifier": +1
    }
}

def get_symptom_info(symptom_key):
    """Get detailed information about a symptom"""
    return SYMPTOM_DATABASE.get(symptom_key, {})

def get_ctas_guideline(level):
    """Get CTAS guideline for a specific level"""
    return CTAS_GUIDELINES.get(level, {})

def check_red_flags(symptoms):
    """Check if any red flag symptoms are present"""
    red_flags_found = []
    for category, flags in RED_FLAG_SYMPTOMS.items():
        for symptom in symptoms:
            if symptom in flags:
                red_flags_found.append({
                    "symptom": symptom,
                    "category": category
                })
    return red_flags_found

def apply_age_modifier(base_ctas, age):
    """Apply age-based severity modifier"""
    for age_group, data in AGE_MODIFIERS.items():
        age_range = data["age_range"]
        if age_range[0] <= age <= age_range[1]:
            multiplier = data["severity_multiplier"]
            # Adjust CTAS level based on age (lower number = more urgent)
            if multiplier > 1.0 and base_ctas > 1:
                return max(1, base_ctas - 1)
    return base_ctas

def evaluate_clinical_rule(rule_name, patient_data):
    """Evaluate a clinical decision rule"""
    rule = CLINICAL_DECISION_RULES.get(rule_name)
    if not rule:
        return None
    
    score = 0
    for condition, points in rule["conditions"].items():
        if patient_data.get(condition, False):
            score += points
    
    thresholds = rule["thresholds"]
    if score >= thresholds["high_risk"]:
        return 1
    elif score >= thresholds["moderate_risk"]:
        return 2
    else:
        return 3
