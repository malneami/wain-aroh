# Healthcare facilities data for Jazan Health Cluster

FACILITIES = [
    {
        "id": 1,
        "name": "مستشفى الملك فهد المركزي",
        "name_en": "King Fahd Central Hospital",
        "type": "emergency",
        "services": ["emergency", "trauma", "surgery", "icu"],
        "ctas_levels": [1, 2, 3],
        "location": {
            "lat": 16.8892,
            "lng": 42.5511,
            "address": "جازان، المملكة العربية السعودية"
        },
        "working_hours": "24/7",
        "phone": "920003344",
        "capacity": "high"
    },
    {
        "id": 2,
        "name": "مركز الرعاية العاجلة - جازان",
        "name_en": "Jazan Urgent Care Center",
        "type": "ucc",
        "services": ["urgent_care", "minor_injuries", "x_ray", "lab"],
        "ctas_levels": [3, 4],
        "location": {
            "lat": 16.9000,
            "lng": 42.5600,
            "address": "حي الروضة، جازان"
        },
        "working_hours": "08:00 - 22:00",
        "phone": "920003345",
        "capacity": "medium"
    },
    {
        "id": 3,
        "name": "مركز صحي أبو عريش",
        "name_en": "Abu Arish Primary Health Center",
        "type": "clinic",
        "services": ["primary_care", "consultation", "pharmacy", "lab"],
        "ctas_levels": [4, 5],
        "location": {
            "lat": 16.9667,
            "lng": 42.8333,
            "address": "أبو عريش، جازان"
        },
        "working_hours": "08:00 - 16:00",
        "phone": "920003346",
        "capacity": "medium"
    },
    {
        "id": 4,
        "name": "مركز صحي صامطة",
        "name_en": "Samtah Primary Health Center",
        "type": "clinic",
        "services": ["primary_care", "consultation", "pharmacy", "vaccination"],
        "ctas_levels": [4, 5],
        "location": {
            "lat": 16.5833,
            "lng": 42.9500,
            "address": "صامطة، جازان"
        },
        "working_hours": "08:00 - 16:00",
        "phone": "920003347",
        "capacity": "medium"
    },
    {
        "id": 5,
        "name": "العيادات الافتراضية",
        "name_en": "Virtual OPD Clinics",
        "type": "virtual",
        "services": ["telemedicine", "consultation", "prescription", "follow_up"],
        "ctas_levels": [5],
        "location": {
            "lat": 0,
            "lng": 0,
            "address": "خدمة افتراضية عبر الإنترنت"
        },
        "working_hours": "08:00 - 20:00",
        "phone": "920003348",
        "capacity": "unlimited"
    }
]

# CTAS (Canadian Triage and Acuity Scale) definitions
CTAS_DEFINITIONS = {
    1: {
        "level": 1,
        "name": "إنعاش",
        "name_en": "Resuscitation",
        "description": "حالات تهدد الحياة وتحتاج إلى تدخل فوري",
        "response_time": "فوري",
        "recommended_care": "emergency",
        "examples": ["توقف القلب", "صعوبة تنفس شديدة", "نزيف حاد", "فقدان الوعي"]
    },
    2: {
        "level": 2,
        "name": "طارئ",
        "name_en": "Emergency",
        "description": "حالات خطيرة تحتاج إلى رعاية عاجلة",
        "response_time": "15 دقيقة",
        "recommended_care": "emergency",
        "examples": ["ألم صدر شديد", "كسور مفتوحة", "حروق شديدة", "سكتة دماغية"]
    },
    3: {
        "level": 3,
        "name": "عاجل",
        "name_en": "Urgent",
        "description": "حالات تحتاج إلى رعاية سريعة",
        "response_time": "30 دقيقة",
        "recommended_care": "ucc",
        "examples": ["كسور بسيطة", "جروح تحتاج خياطة", "حمى عالية", "ألم متوسط"]
    },
    4: {
        "level": 4,
        "name": "أقل عجلة",
        "name_en": "Less Urgent",
        "description": "حالات يمكن معالجتها في العيادات",
        "response_time": "60 دقيقة",
        "recommended_care": "clinic",
        "examples": ["التهاب حلق", "طفح جلدي", "ألم بسيط", "زكام"]
    },
    5: {
        "level": 5,
        "name": "غير عاجل",
        "name_en": "Non-Urgent",
        "description": "حالات روتينية يمكن معالجتها افتراضياً",
        "response_time": "120 دقيقة",
        "recommended_care": "virtual",
        "examples": ["استشارة عامة", "متابعة روتينية", "وصفة طبية", "نصيحة طبية"]
    }
}

def get_facilities_by_ctas(ctas_level):
    """Get facilities that can handle a specific CTAS level"""
    return [f for f in FACILITIES if ctas_level in f['ctas_levels']]

def get_facility_by_id(facility_id):
    """Get a specific facility by ID"""
    for facility in FACILITIES:
        if facility['id'] == facility_id:
            return facility
    return None

def get_recommended_care_type(ctas_level):
    """Get recommended care type based on CTAS level"""
    if ctas_level in CTAS_DEFINITIONS:
        return CTAS_DEFINITIONS[ctas_level]['recommended_care']
    return 'clinic'

