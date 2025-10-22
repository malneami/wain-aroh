"""
نماذج البحث المتقدم عن المراكز الطبية والعيادات المتخصصة
Advanced Search Models for Medical Centers and Specialized Clinics
"""

from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from enum import Enum


class SearchFilterType(Enum):
    """أنواع الفلاتر المتاحة للبحث"""
    SPECIALTY = "specialty"  # التخصص
    LOCATION = "location"  # الموقع
    ORGANIZATION = "organization"  # الجهة
    CLUSTER = "cluster"  # التجمع
    RATING = "rating"  # التقييم
    DISTANCE = "distance"  # المسافة
    AVAILABILITY = "availability"  # التوفر
    SERVICES = "services"  # الخدمات


class SortBy(Enum):
    """خيارات الترتيب"""
    RELEVANCE = "relevance"  # الأكثر صلة
    DISTANCE = "distance"  # الأقرب
    RATING = "rating"  # الأعلى تقييماً
    AVAILABILITY = "availability"  # الأكثر توفراً
    PERFORMANCE = "performance"  # الأفضل أداءً


@dataclass
class SearchFilters:
    """فلاتر البحث المتقدم"""
    # التخصصات المطلوبة
    specialties: List[str] = field(default_factory=list)
    
    # الموقع
    location: Optional[Dict[str, float]] = None  # {"lat": 24.7136, "lng": 46.6753}
    max_distance_km: float = 50.0  # المسافة القصوى بالكيلومتر
    
    # الجهات
    organizations: List[str] = field(default_factory=list)
    
    # التجمعات
    clusters: List[str] = field(default_factory=list)
    
    # التقييم الأدنى
    min_rating: float = 0.0
    
    # التوفر
    available_now: bool = False
    accepts_emergency: bool = False
    accepts_appointments: bool = True
    
    # الخدمات المطلوبة
    required_services: List[str] = field(default_factory=list)
    
    # الترتيب
    sort_by: SortBy = SortBy.RELEVANCE
    
    # الصفحة والحد الأقصى
    page: int = 1
    limit: int = 10


@dataclass
class PerformanceMetrics:
    """مقاييس الأداء للمنشأة الصحية"""
    # معدل التقييم العام
    overall_rating: float = 0.0  # من 5
    total_reviews: int = 0
    
    # أوقات الانتظار
    avg_wait_time_minutes: int = 0
    median_wait_time_minutes: int = 0
    
    # معدلات الرضا
    patient_satisfaction: float = 0.0  # من 100%
    
    # معدلات الأداء
    on_time_appointments: float = 0.0  # نسبة المواعيد في الوقت المحدد
    consultation_duration_minutes: int = 0  # متوسط مدة الاستشارة
    
    # الإشغال
    current_occupancy: float = 0.0  # نسبة الإشغال الحالية
    avg_daily_patients: int = 0
    
    # الاستجابة
    response_time_minutes: int = 0  # وقت الاستجابة للطوارئ
    
    # معدلات النجاح
    successful_treatments: float = 0.0  # نسبة العلاجات الناجحة
    readmission_rate: float = 0.0  # معدل إعادة الدخول
    
    # التوفر
    available_beds: int = 0
    available_doctors: int = 0
    
    # تقييمات مواقع التواصل الاجتماعي
    social_media_ratings: Optional[Dict] = None
    
    # آخر تحديث
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class FacilityProfile:
    """ملف تعريفي شامل للمنشأة الصحية"""
    # المعلومات الأساسية
    id: int
    name: str
    name_en: str
    type: str  # hospital, clinic, medical_center
    
    # الموقع
    location: Dict[str, float]  # {"lat": 24.7136, "lng": 46.6753}
    address: str
    city: str
    district: str
    
    # التصنيف
    organization: str
    cluster: str
    
    # التخصصات والخدمات
    specialties: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    
    # معلومات الاتصال
    phone: str = ""
    emergency_phone: str = ""
    email: str = ""
    website: str = ""
    
    # ساعات العمل
    working_hours: Dict[str, str] = field(default_factory=dict)
    # {"saturday": "08:00-20:00", "sunday": "08:00-20:00", ...}
    
    # القدرات
    total_beds: int = 0
    emergency_beds: int = 0
    icu_beds: int = 0
    
    # الأطباء
    total_doctors: int = 0
    specialist_doctors: int = 0
    
    # المعدات والمرافق
    equipment: List[str] = field(default_factory=list)
    facilities: List[str] = field(default_factory=list)
    
    # التأمين
    accepted_insurance: List[str] = field(default_factory=list)
    
    # مقاييس الأداء
    performance: PerformanceMetrics = field(default_factory=PerformanceMetrics)
    
    # الحالة
    is_active: bool = True
    accepts_emergency: bool = True
    accepts_appointments: bool = True
    
    # الصور
    images: List[str] = field(default_factory=list)
    
    # الوصف
    description: str = ""
    description_en: str = ""


@dataclass
class SearchResult:
    """نتيجة بحث واحدة"""
    facility: FacilityProfile
    
    # معلومات الصلة
    relevance_score: float = 0.0  # درجة الصلة (0-100)
    distance_km: float = 0.0  # المسافة بالكيلومتر
    
    # التوفر
    is_available: bool = True
    next_available_slot: Optional[datetime] = None
    estimated_wait_time: int = 0  # بالدقائق
    
    # التطابق
    matched_specialties: List[str] = field(default_factory=list)
    matched_services: List[str] = field(default_factory=list)
    
    # التوصية
    recommendation_reason: str = ""  # سبب التوصية بهذه المنشأة


@dataclass
class SearchResponse:
    """استجابة البحث الكاملة"""
    results: List[SearchResult] = field(default_factory=list)
    
    # معلومات الصفحة
    total_results: int = 0
    page: int = 1
    limit: int = 10
    total_pages: int = 0
    
    # الفلاتر المطبقة
    applied_filters: Dict = field(default_factory=dict)
    
    # إحصائيات
    stats: Dict = field(default_factory=dict)
    # {
    #     "avg_distance": 5.2,
    #     "avg_rating": 4.5,
    #     "avg_wait_time": 30,
    #     "available_count": 8
    # }
    
    # وقت البحث
    search_time_ms: float = 0.0


@dataclass
class FacilityComparison:
    """مقارنة بين منشأتين أو أكثر"""
    facilities: List[FacilityProfile] = field(default_factory=list)
    
    # معايير المقارنة
    comparison_metrics: Dict[str, List] = field(default_factory=dict)
    # {
    #     "rating": [4.5, 4.2, 4.8],
    #     "wait_time": [30, 45, 20],
    #     "distance": [5.2, 8.1, 3.4]
    # }
    
    # التوصية
    recommended_facility_id: Optional[int] = None
    recommendation_reason: str = ""


# دوال مساعدة للتحويل

def facility_to_dict(facility: FacilityProfile) -> Dict:
    """تحويل ملف المنشأة إلى قاموس"""
    return {
        "id": facility.id,
        "name": facility.name,
        "name_en": facility.name_en,
        "type": facility.type,
        "location": facility.location,
        "address": facility.address,
        "city": facility.city,
        "district": facility.district,
        "organization": facility.organization,
        "cluster": facility.cluster,
        "specialties": facility.specialties,
        "services": facility.services,
        "phone": facility.phone,
        "emergency_phone": facility.emergency_phone,
        "email": facility.email,
        "website": facility.website,
        "working_hours": facility.working_hours,
        "total_beds": facility.total_beds,
        "emergency_beds": facility.emergency_beds,
        "icu_beds": facility.icu_beds,
        "total_doctors": facility.total_doctors,
        "specialist_doctors": facility.specialist_doctors,
        "equipment": facility.equipment,
        "facilities": facility.facilities,
        "accepted_insurance": facility.accepted_insurance,
        "performance": {
            "overall_rating": facility.performance.overall_rating,
            "total_reviews": facility.performance.total_reviews,
            "avg_wait_time_minutes": facility.performance.avg_wait_time_minutes,
            "patient_satisfaction": facility.performance.patient_satisfaction,
            "on_time_appointments": facility.performance.on_time_appointments,
            "current_occupancy": facility.performance.current_occupancy,
            "avg_daily_patients": facility.performance.avg_daily_patients,
            "available_beds": facility.performance.available_beds,
            "available_doctors": facility.performance.available_doctors,
        },
        "is_active": facility.is_active,
        "accepts_emergency": facility.accepts_emergency,
        "accepts_appointments": facility.accepts_appointments,
        "images": facility.images,
        "description": facility.description,
        "description_en": facility.description_en,
    }


def search_result_to_dict(result: SearchResult) -> Dict:
    """تحويل نتيجة البحث إلى قاموس"""
    return {
        "facility": facility_to_dict(result.facility),
        "relevance_score": result.relevance_score,
        "distance_km": result.distance_km,
        "is_available": result.is_available,
        "next_available_slot": result.next_available_slot.isoformat() if result.next_available_slot else None,
        "estimated_wait_time": result.estimated_wait_time,
        "matched_specialties": result.matched_specialties,
        "matched_services": result.matched_services,
        "recommendation_reason": result.recommendation_reason,
    }

