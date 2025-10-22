# National Guard Hospital Network - Riyadh
# Main hospital with surrounding UCCs and clinics

FACILITIES = [
    # ==========================================
    # MAIN HOSPITAL - National Guard Hospital
    # ==========================================
    {
        "id": 1,
        "name": "مستشفى الحرس الوطني - الرياض",
        "name_en": "National Guard Hospital - Riyadh",
        "type": "main_hospital",
        "location": "الرياض، طريق الملك عبدالعزيز، حي الملقا",
        "coordinates": {"lat": 24.7767, "lng": 46.6106},
        "phone": "+966-11-252-0088",
        "emergency_phone": "937",
        "hours": "24/7",
        "services": ["emergency", "ucc", "clinic", "icu", "surgery", "trauma", "cardiac", "stroke"],
        "ctas_levels": [1, 2, 3, 4, 5],
        "capacity": {
            "emergency_beds": 50,
            "icu_beds": 30,
            "general_beds": 500
        },
        "specialties": [
            "طوارئ عامة",
            "جراحة",
            "قلب وأوعية دموية",
            "أعصاب",
            "عظام",
            "أطفال",
            "نساء وولادة",
            "باطنية"
        ],
        "features": [
            "مركز صدمات متقدم",
            "وحدة عناية مركزة",
            "مختبر على مدار الساعة",
            "أشعة متقدمة (CT, MRI)",
            "صيدلية 24 ساعة",
            "خدمات الإسعاف"
        ],
        "wait_time_minutes": 15,
        "rating": 4.8,
        "is_main_hub": True
    },
    
    # ==========================================
    # UCCs AROUND NATIONAL GUARD HOSPITAL
    # ==========================================
    {
        "id": 2,
        "name": "مركز الرعاية العاجلة - الملقا",
        "name_en": "Urgent Care Center - Al Malqa",
        "type": "ucc",
        "location": "الرياض، حي الملقا، بالقرب من مستشفى الحرس الوطني",
        "coordinates": {"lat": 24.7850, "lng": 46.6180},
        "phone": "+966-11-252-1100",
        "hours": "6:00 AM - 12:00 AM",
        "services": ["ucc", "minor_emergency", "lab", "xray"],
        "ctas_levels": [3, 4, 5],
        "capacity": {
            "treatment_rooms": 10,
            "waiting_capacity": 30
        },
        "specialties": [
            "إصابات بسيطة",
            "حمى وعدوى",
            "آلام متوسطة",
            "فحوصات سريعة"
        ],
        "features": [
            "مختبر سريع",
            "أشعة عادية",
            "صيدلية",
            "تحويل سريع للطوارئ"
        ],
        "wait_time_minutes": 20,
        "rating": 4.5,
        "distance_from_main_km": 1.2,
        "main_hospital_id": 1
    },
    
    {
        "id": 3,
        "name": "مركز الرعاية العاجلة - النخيل",
        "name_en": "Urgent Care Center - Al Nakheel",
        "type": "ucc",
        "location": "الرياض، حي النخيل، شارع الأمير سلطان",
        "coordinates": {"lat": 24.7500, "lng": 46.6300},
        "phone": "+966-11-252-1200",
        "hours": "7:00 AM - 11:00 PM",
        "services": ["ucc", "minor_emergency", "lab", "xray"],
        "ctas_levels": [3, 4, 5],
        "capacity": {
            "treatment_rooms": 8,
            "waiting_capacity": 25
        },
        "specialties": [
            "إصابات بسيطة",
            "حمى وعدوى",
            "آلام متوسطة",
            "فحوصات سريعة"
        ],
        "features": [
            "مختبر سريع",
            "أشعة عادية",
            "صيدلية",
            "خدمة الأطفال"
        ],
        "wait_time_minutes": 25,
        "rating": 4.4,
        "distance_from_main_km": 3.5,
        "main_hospital_id": 1
    },
    
    {
        "id": 4,
        "name": "مركز الرعاية العاجلة - العليا",
        "name_en": "Urgent Care Center - Al Olaya",
        "type": "ucc",
        "location": "الرياض، حي العليا، طريق الملك فهد",
        "coordinates": {"lat": 24.7100, "lng": 46.6700},
        "phone": "+966-11-252-1300",
        "hours": "6:00 AM - 12:00 AM",
        "services": ["ucc", "minor_emergency", "lab", "xray"],
        "ctas_levels": [3, 4, 5],
        "capacity": {
            "treatment_rooms": 12,
            "waiting_capacity": 35
        },
        "specialties": [
            "إصابات بسيطة",
            "حمى وعدوى",
            "آلام متوسطة",
            "فحوصات سريعة"
        ],
        "features": [
            "مختبر متقدم",
            "أشعة عادية",
            "صيدلية",
            "خدمة سريعة"
        ],
        "wait_time_minutes": 18,
        "rating": 4.6,
        "distance_from_main_km": 8.2,
        "main_hospital_id": 1
    },
    
    {
        "id": 5,
        "name": "مركز الرعاية العاجلة - الربوة",
        "name_en": "Urgent Care Center - Al Rabwa",
        "type": "ucc",
        "location": "الرياض، حي الربوة، شارع الأمير محمد بن عبدالعزيز",
        "coordinates": {"lat": 24.7300, "lng": 46.5900},
        "phone": "+966-11-252-1400",
        "hours": "7:00 AM - 11:00 PM",
        "services": ["ucc", "minor_emergency", "lab", "xray"],
        "ctas_levels": [3, 4, 5],
        "capacity": {
            "treatment_rooms": 10,
            "waiting_capacity": 30
        },
        "specialties": [
            "إصابات بسيطة",
            "حمى وعدوى",
            "آلام متوسطة",
            "فحوصات سريعة"
        ],
        "features": [
            "مختبر سريع",
            "أشعة عادية",
            "صيدلية",
            "مواقف واسعة"
        ],
        "wait_time_minutes": 22,
        "rating": 4.3,
        "distance_from_main_km": 5.8,
        "main_hospital_id": 1
    },
    
    # ==========================================
    # CLINICS FOR NON-URGENT CARE
    # ==========================================
    {
        "id": 6,
        "name": "عيادات الحرس الوطني - الملقا",
        "name_en": "National Guard Clinics - Al Malqa",
        "type": "clinic",
        "location": "الرياض، حي الملقا، مجمع العيادات الخارجية",
        "coordinates": {"lat": 24.7800, "lng": 46.6150},
        "phone": "+966-11-252-2000",
        "hours": "8:00 AM - 8:00 PM",
        "services": ["clinic", "consultation", "follow_up", "lab", "pharmacy"],
        "ctas_levels": [4, 5],
        "capacity": {
            "consultation_rooms": 20,
            "daily_appointments": 200
        },
        "specialties": [
            "طب عام",
            "باطنية",
            "أطفال",
            "نساء",
            "عظام",
            "جلدية",
            "أنف وأذن وحنجرة"
        ],
        "features": [
            "حجز مواعيد إلكتروني",
            "مختبر",
            "صيدلية",
            "متابعة الأمراض المزمنة"
        ],
        "wait_time_minutes": 30,
        "rating": 4.5,
        "distance_from_main_km": 0.8,
        "main_hospital_id": 1,
        "booking_available": True,
        "booking_url": "https://ngh.med.sa/appointments"
    },
    
    {
        "id": 7,
        "name": "عيادات الحرس الوطني - العليا",
        "name_en": "National Guard Clinics - Al Olaya",
        "type": "clinic",
        "location": "الرياض، حي العليا، برج العيادات",
        "coordinates": {"lat": 24.7050, "lng": 46.6750},
        "phone": "+966-11-252-2100",
        "hours": "8:00 AM - 8:00 PM",
        "services": ["clinic", "consultation", "follow_up", "lab", "pharmacy"],
        "ctas_levels": [4, 5],
        "capacity": {
            "consultation_rooms": 15,
            "daily_appointments": 150
        },
        "specialties": [
            "طب عام",
            "باطنية",
            "قلب",
            "سكري",
            "ضغط"
        ],
        "features": [
            "حجز مواعيد إلكتروني",
            "مختبر",
            "صيدلية",
            "برنامج الأمراض المزمنة"
        ],
        "wait_time_minutes": 35,
        "rating": 4.4,
        "distance_from_main_km": 8.5,
        "main_hospital_id": 1,
        "booking_available": True,
        "booking_url": "https://ngh.med.sa/appointments"
    },
    
    # ==========================================
    # VIRTUAL OPD
    # ==========================================
    {
        "id": 8,
        "name": "العيادات الافتراضية - الحرس الوطني",
        "name_en": "Virtual OPD - National Guard",
        "type": "virtual_opd",
        "location": "خدمة عن بعد",
        "coordinates": {"lat": 24.7767, "lng": 46.6106},  # Same as main hospital
        "phone": "+966-11-252-3000",
        "hours": "24/7",
        "services": ["virtual_consultation", "prescription", "follow_up", "medical_advice"],
        "ctas_levels": [5],
        "capacity": {
            "concurrent_consultations": 50,
            "daily_capacity": 500
        },
        "specialties": [
            "استشارات عامة",
            "متابعة الأمراض المزمنة",
            "استشارات نفسية",
            "تغذية",
            "صحة الأطفال"
        ],
        "features": [
            "متاح 24/7",
            "استشارة فورية",
            "وصفات إلكترونية",
            "تطبيق الجوال"
        ],
        "wait_time_minutes": 5,
        "rating": 4.7,
        "distance_from_main_km": 0,
        "main_hospital_id": 1,
        "booking_available": True,
        "booking_url": "https://ngh.med.sa/virtual"
    }
]

# Helper functions
def get_main_hospital():
    """Get the main National Guard Hospital"""
    return next(f for f in FACILITIES if f.get('is_main_hub'))

def get_uccs_near_main():
    """Get all UCCs around the main hospital"""
    return [f for f in FACILITIES if f['type'] == 'ucc']

def get_clinics():
    """Get all clinics"""
    return [f for f in FACILITIES if f['type'] == 'clinic']

def get_virtual_opd():
    """Get virtual OPD service"""
    return next(f for f in FACILITIES if f['type'] == 'virtual_opd')

def get_facilities_by_ctas(ctas_level):
    """Get facilities that can handle specific CTAS level"""
    return [f for f in FACILITIES if ctas_level in f['ctas_levels']]

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two coordinates in km"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth radius in km
    
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def find_nearest_facilities(patient_lat, patient_lng, facility_type=None, ctas_level=None, limit=3):
    """Find nearest facilities based on patient location"""
    
    # Filter by type and CTAS if specified
    filtered = FACILITIES
    if facility_type:
        filtered = [f for f in filtered if f['type'] == facility_type]
    if ctas_level:
        filtered = [f for f in filtered if ctas_level in f['ctas_levels']]
    
    # Calculate distances
    for facility in filtered:
        facility['distance_km'] = calculate_distance(
            patient_lat, patient_lng,
            facility['coordinates']['lat'],
            facility['coordinates']['lng']
        )
    
    # Sort by distance and return top N
    sorted_facilities = sorted(filtered, key=lambda x: x['distance_km'])
    return sorted_facilities[:limit]

