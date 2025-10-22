"""
واجهة برمجة التطبيقات للبحث المتقدم
Advanced Search API Routes
"""

from flask import Blueprint, request, jsonify
from typing import List, Dict
from datetime import datetime

from ..models.search import (
    SearchFilters, SortBy, FacilityProfile, PerformanceMetrics,
    search_result_to_dict, facility_to_dict
)
from ..services.advanced_search import search_service
from ..services.social_media_service import social_media_service
from ..models.hospital import Hospital
# Database is imported from models.user
# from ..database.db import db

# إنشاء Blueprint
search_bp = Blueprint('search', __name__, url_prefix='/api/search')


def hospital_to_facility_profile(hospital: Hospital) -> FacilityProfile:
    """
    تحويل نموذج المستشفى إلى ملف المنشأة
    Convert Hospital model to FacilityProfile
    """
    # استخراج الموقع
    location = {"lat": 24.7136, "lng": 46.6753}  # موقع افتراضي (الرياض)
    if hasattr(hospital, 'latitude') and hasattr(hospital, 'longitude'):
        if hospital.latitude and hospital.longitude:
            location = {
                "lat": float(hospital.latitude),
                "lng": float(hospital.longitude)
            }
    
    # إنشاء مقاييس الأداء
    # الحصول على التقييمات من مواقع التواصل الاجتماعي
    social_ratings = social_media_service.generate_mock_ratings(
        hospital.id,
        hospital.name_ar if hasattr(hospital, 'name_ar') else str(hospital.id),
        hospital.facility_type if hasattr(hospital, 'facility_type') else 'hospital'
    )
    
    # استخدام التقييم المجمع من مواقع التواصل
    overall_rating = social_ratings['aggregate']['overall_rating']
    total_reviews = social_ratings['aggregate']['total_reviews']
    
    performance = PerformanceMetrics(
        overall_rating=overall_rating,
        total_reviews=total_reviews,
        avg_wait_time_minutes=hospital.avg_wait_time if hasattr(hospital, 'avg_wait_time') else 30,
        patient_satisfaction=hospital.patient_satisfaction if hasattr(hospital, 'patient_satisfaction') else 85.0,
        on_time_appointments=hospital.on_time_rate if hasattr(hospital, 'on_time_rate') else 90.0,
        current_occupancy=hospital.occupancy if hasattr(hospital, 'occupancy') else 75.0,
        avg_daily_patients=hospital.daily_patients if hasattr(hospital, 'daily_patients') else 100,
        available_beds=hospital.available_beds if hasattr(hospital, 'available_beds') else 50,
        available_doctors=hospital.available_doctors if hasattr(hospital, 'available_doctors') else 20,
        social_media_ratings=social_ratings
    )
    
    # التخصصات
    specialties = []
    if hasattr(hospital, 'specialties') and hospital.specialties:
        if isinstance(hospital.specialties, str):
            specialties = [s.strip() for s in hospital.specialties.split(',')]
        else:
            specialties = hospital.specialties
    
    # الخدمات
    services = []
    if hasattr(hospital, 'services') and hospital.services:
        if isinstance(hospital.services, str):
            services = [s.strip() for s in hospital.services.split(',')]
        else:
            services = hospital.services
    
    # إنشاء ملف المنشأة
    facility = FacilityProfile(
        id=hospital.id,
        name=hospital.name_ar if hasattr(hospital, 'name_ar') else str(hospital.id),
        name_en=hospital.name_en if hasattr(hospital, 'name_en') else '',
        type=hospital.facility_type if hasattr(hospital, 'facility_type') else 'hospital',
        location=location,
        address=hospital.address_ar if hasattr(hospital, 'address_ar') else '',
        city=hospital.city if hasattr(hospital, 'city') else 'الرياض',
        district=hospital.district_ar if hasattr(hospital, 'district_ar') else '',
        organization=hospital.organization.name_ar if hospital.organization else '',
        cluster=hospital.cluster.name_ar if hospital.cluster else '',
        specialties=specialties,
        services=services,
        phone=hospital.phone if hasattr(hospital, 'phone') else '',
        emergency_phone=hospital.phone_emergency if hasattr(hospital, 'phone_emergency') else '',
        email=hospital.email if hasattr(hospital, 'email') else '',
        website=hospital.website if hasattr(hospital, 'website') else '',
        total_beds=hospital.capacity_beds if hasattr(hospital, 'capacity_beds') else 0,
        emergency_beds=hospital.capacity_emergency_beds if hasattr(hospital, 'capacity_emergency_beds') else 0,
        icu_beds=0,
        total_doctors=0,
        performance=performance,
        is_active=hospital.is_active if hasattr(hospital, 'is_active') else True,
        accepts_emergency=hospital.is_emergency if hasattr(hospital, 'is_emergency') else True,
        accepts_appointments=True,
        description=hospital.description_ar if hasattr(hospital, 'description_ar') else '',
    )
    
    return facility


@search_bp.route('/facilities', methods=['POST'])
def search_facilities():
    """
    البحث المتقدم عن المنشآت الصحية
    Advanced search for healthcare facilities
    
    Body:
    {
        "specialties": ["قلب", "أطفال"],
        "location": {"lat": 24.7136, "lng": 46.6753},
        "max_distance_km": 20,
        "organizations": ["وزارة الصحة"],
        "clusters": ["تجمع الرياض الأول"],
        "min_rating": 4.0,
        "available_now": true,
        "sort_by": "relevance",
        "page": 1,
        "limit": 10
    }
    """
    try:
        data = request.json or {}
        
        # إنشاء الفلاتر
        filters = SearchFilters(
            specialties=data.get('specialties', []),
            location=data.get('location'),
            max_distance_km=data.get('max_distance_km', 50.0),
            organizations=data.get('organizations', []),
            clusters=data.get('clusters', []),
            min_rating=data.get('min_rating', 0.0),
            available_now=data.get('available_now', False),
            accepts_emergency=data.get('accepts_emergency', False),
            accepts_appointments=data.get('accepts_appointments', True),
            required_services=data.get('required_services', []),
            sort_by=SortBy(data.get('sort_by', 'relevance')),
            page=data.get('page', 1),
            limit=data.get('limit', 10)
        )
        
        # الحصول على المستشفيات من قاعدة البيانات
        hospitals = Hospital.query.all()
        
        # تحويل إلى ملفات المنشآت
        facilities = [hospital_to_facility_profile(h) for h in hospitals]
        
        # تنفيذ البحث
        response = search_service.search(facilities, filters)
        
        # تحويل النتائج إلى JSON
        return jsonify({
            'success': True,
            'results': [search_result_to_dict(r) for r in response.results],
            'total_results': response.total_results,
            'page': response.page,
            'limit': response.limit,
            'total_pages': response.total_pages,
            'applied_filters': response.applied_filters,
            'stats': response.stats,
            'search_time_ms': response.search_time_ms
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@search_bp.route('/facilities/<int:facility_id>', methods=['GET'])
def get_facility_details(facility_id):
    """
    الحصول على تفاصيل منشأة محددة
    Get details of a specific facility
    """
    try:
        hospital = Hospital.query.get(facility_id)
        
        if not hospital:
            return jsonify({
                'success': False,
                'error': 'المنشأة غير موجودة'
            }), 404
        
        facility = hospital_to_facility_profile(hospital)
        
        return jsonify({
            'success': True,
            'facility': facility_to_dict(facility)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@search_bp.route('/facilities/compare', methods=['POST'])
def compare_facilities():
    """
    مقارنة بين عدة منشآت
    Compare multiple facilities
    
    Body:
    {
        "facility_ids": [1, 2, 3]
    }
    """
    try:
        data = request.json or {}
        facility_ids = data.get('facility_ids', [])
        
        if not facility_ids:
            return jsonify({
                'success': False,
                'error': 'يجب تحديد منشأتين على الأقل للمقارنة'
            }), 400
        
        # الحصول على المستشفيات
        hospitals = Hospital.query.filter(Hospital.id.in_(facility_ids)).all()
        
        # تحويل إلى ملفات المنشآت
        facilities = [hospital_to_facility_profile(h) for h in hospitals]
        
        # تنفيذ المقارنة
        comparison = search_service.compare_facilities(facilities, facility_ids)
        
        return jsonify({
            'success': True,
            'comparison': comparison
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@search_bp.route('/specialties', methods=['GET'])
def get_specialties():
    """
    الحصول على قائمة التخصصات المتوفرة
    Get list of available specialties
    """
    try:
        # الحصول على جميع المستشفيات
        hospitals = Hospital.query.all()
        
        # جمع التخصصات
        specialties_set = set()
        for hospital in hospitals:
            if hasattr(hospital, 'specialties') and hospital.specialties:
                if isinstance(hospital.specialties, str):
                    specs = [s.strip() for s in hospital.specialties.split(',')]
                    specialties_set.update(specs)
                else:
                    specialties_set.update(hospital.specialties)
        
        specialties = sorted(list(specialties_set))
        
        return jsonify({
            'success': True,
            'specialties': specialties
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@search_bp.route('/organizations', methods=['GET'])
def get_organizations():
    """
    الحصول على قائمة الجهات الصحية
    Get list of healthcare organizations
    """
    try:
        hospitals = Hospital.query.all()
        
        organizations_set = set()
        for hospital in hospitals:
            if hasattr(hospital, 'organization') and hospital.organization:
                organizations_set.add(hospital.organization)
        
        organizations = sorted(list(organizations_set))
        
        return jsonify({
            'success': True,
            'organizations': organizations
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@search_bp.route('/clusters', methods=['GET'])
def get_clusters():
    """
    الحصول على قائمة التجمعات الصحية
    Get list of healthcare clusters
    """
    try:
        hospitals = Hospital.query.all()
        
        clusters_set = set()
        for hospital in hospitals:
            if hasattr(hospital, 'cluster') and hospital.cluster:
                clusters_set.add(hospital.cluster)
        
        clusters = sorted(list(clusters_set))
        
        return jsonify({
            'success': True,
            'clusters': clusters
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@search_bp.route('/filters', methods=['GET'])
def get_available_filters():
    """
    الحصول على جميع الفلاتر المتاحة
    Get all available filters
    """
    try:
        hospitals = Hospital.query.all()
        
        # جمع التخصصات
        specialties_set = set()
        organizations_set = set()
        clusters_set = set()
        services_set = set()
        
        for hospital in hospitals:
            # التخصصات
            if hasattr(hospital, 'specialties') and hospital.specialties:
                if isinstance(hospital.specialties, str):
                    specs = [s.strip() for s in hospital.specialties.split(',')]
                    specialties_set.update(specs)
            
            # الجهات
            if hasattr(hospital, 'organization') and hospital.organization:
                organizations_set.add(hospital.organization)
            
            # التجمعات
            if hasattr(hospital, 'cluster') and hospital.cluster:
                clusters_set.add(hospital.cluster)
            
            # الخدمات
            if hasattr(hospital, 'services') and hospital.services:
                if isinstance(hospital.services, str):
                    servs = [s.strip() for s in hospital.services.split(',')]
                    services_set.update(servs)
        
        return jsonify({
            'success': True,
            'filters': {
                'specialties': sorted(list(specialties_set)),
                'organizations': sorted(list(organizations_set)),
                'clusters': sorted(list(clusters_set)),
                'services': sorted(list(services_set)),
                'sort_options': [
                    {'value': 'relevance', 'label': 'الأكثر صلة'},
                    {'value': 'distance', 'label': 'الأقرب'},
                    {'value': 'rating', 'label': 'الأعلى تقييماً'},
                    {'value': 'availability', 'label': 'الأكثر توفراً'},
                    {'value': 'performance', 'label': 'الأفضل أداءً'},
                ]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@search_bp.route('/nearby', methods=['POST'])
def search_nearby():
    """
    البحث عن أقرب المنشآت
    Search for nearby facilities
    
    Body:
    {
        "location": {"lat": 24.7136, "lng": 46.6753},
        "radius_km": 10,
        "limit": 5
    }
    """
    try:
        data = request.json or {}
        
        location = data.get('location')
        if not location:
            return jsonify({
                'success': False,
                'error': 'يجب تحديد الموقع'
            }), 400
        
        radius_km = data.get('radius_km', 10)
        limit = data.get('limit', 5)
        
        # إنشاء فلاتر بسيطة
        filters = SearchFilters(
            location=location,
            max_distance_km=radius_km,
            sort_by=SortBy.DISTANCE,
            limit=limit
        )
        
        # الحصول على المستشفيات
        hospitals = Hospital.query.all()
        facilities = [hospital_to_facility_profile(h) for h in hospitals]
        
        # تنفيذ البحث
        response = search_service.search(facilities, filters)
        
        return jsonify({
            'success': True,
            'results': [search_result_to_dict(r) for r in response.results],
            'total_results': response.total_results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

