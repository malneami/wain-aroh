"""
خدمة البحث المتقدم عن المراكز الطبية والعيادات المتخصصة
Advanced Search Service for Medical Centers and Specialized Clinics
"""

import math
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import asdict

from ..models.search import (
    SearchFilters, SearchResult, SearchResponse, FacilityProfile,
    PerformanceMetrics, SortBy, search_result_to_dict
)


class AdvancedSearchService:
    """خدمة البحث المتقدم"""
    
    def __init__(self):
        """تهيئة الخدمة"""
        self.facilities_cache = []
        self.last_cache_update = None
        
    def calculate_distance(self, loc1: Dict[str, float], loc2: Dict[str, float]) -> float:
        """
        حساب المسافة بين نقطتين باستخدام صيغة Haversine
        Calculate distance between two points using Haversine formula
        
        Args:
            loc1: الموقع الأول {"lat": ..., "lng": ...}
            loc2: الموقع الثاني {"lat": ..., "lng": ...}
            
        Returns:
            المسافة بالكيلومتر
        """
        # نصف قطر الأرض بالكيلومتر
        R = 6371.0
        
        lat1 = math.radians(loc1["lat"])
        lon1 = math.radians(loc1["lng"])
        lat2 = math.radians(loc2["lat"])
        lon2 = math.radians(loc2["lng"])
        
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return round(distance, 2)
    
    def calculate_relevance_score(
        self,
        facility: FacilityProfile,
        filters: SearchFilters,
        distance_km: float
    ) -> float:
        """
        حساب درجة الصلة للمنشأة
        Calculate relevance score for a facility
        
        Args:
            facility: المنشأة الصحية
            filters: فلاتر البحث
            distance_km: المسافة بالكيلومتر
            
        Returns:
            درجة الصلة (0-100)
        """
        score = 0.0
        max_score = 100.0
        
        # 1. تطابق التخصصات (30 نقطة)
        if filters.specialties:
            matched_specialties = set(facility.specialties) & set(filters.specialties)
            specialty_score = (len(matched_specialties) / len(filters.specialties)) * 30
            score += specialty_score
        else:
            score += 30  # إذا لم يحدد تخصص، أعط النقاط الكاملة
        
        # 2. القرب (25 نقطة)
        if distance_km <= 5:
            score += 25
        elif distance_km <= 10:
            score += 20
        elif distance_km <= 20:
            score += 15
        elif distance_km <= 30:
            score += 10
        else:
            score += max(0, 25 - (distance_km - 30) / 2)
        
        # 3. التقييم (20 نقطة)
        rating_score = (facility.performance.overall_rating / 5.0) * 20
        score += rating_score
        
        # 4. التوفر (15 نقطة)
        if filters.available_now:
            if facility.performance.current_occupancy < 80:
                score += 15
            elif facility.performance.current_occupancy < 90:
                score += 10
            else:
                score += 5
        else:
            score += 15
        
        # 5. وقت الانتظار (10 نقطة)
        if facility.performance.avg_wait_time_minutes <= 15:
            score += 10
        elif facility.performance.avg_wait_time_minutes <= 30:
            score += 7
        elif facility.performance.avg_wait_time_minutes <= 60:
            score += 5
        else:
            score += 2
        
        return round(min(score, max_score), 2)
    
    def apply_filters(
        self,
        facilities: List[FacilityProfile],
        filters: SearchFilters
    ) -> List[Tuple[FacilityProfile, float]]:
        """
        تطبيق الفلاتر على قائمة المنشآت
        Apply filters to facilities list
        
        Args:
            facilities: قائمة المنشآت
            filters: الفلاتر
            
        Returns:
            قائمة المنشآت المطابقة مع المسافة
        """
        filtered = []
        
        for facility in facilities:
            # التحقق من الحالة النشطة
            if not facility.is_active:
                continue
            
            # فلتر التخصصات
            if filters.specialties:
                if not any(spec in facility.specialties for spec in filters.specialties):
                    continue
            
            # فلتر الجهات
            if filters.organizations:
                if facility.organization not in filters.organizations:
                    continue
            
            # فلتر التجمعات
            if filters.clusters:
                if facility.cluster not in filters.clusters:
                    continue
            
            # فلتر الخدمات المطلوبة
            if filters.required_services:
                if not all(service in facility.services for service in filters.required_services):
                    continue
            
            # حساب المسافة
            distance_km = 0.0
            if filters.location:
                distance_km = self.calculate_distance(filters.location, facility.location)
                
                # فلتر المسافة القصوى
                if distance_km > filters.max_distance_km:
                    continue
            
            # فلتر التقييم الأدنى
            if facility.performance.overall_rating < filters.min_rating:
                continue
            
            # فلتر التوفر
            if filters.available_now:
                if facility.performance.current_occupancy >= 95:
                    continue
            
            # فلتر قبول الطوارئ
            if filters.accepts_emergency:
                if not facility.accepts_emergency:
                    continue
            
            # فلتر قبول المواعيد
            if filters.accepts_appointments:
                if not facility.accepts_appointments:
                    continue
            
            filtered.append((facility, distance_km))
        
        return filtered
    
    def sort_results(
        self,
        results: List[SearchResult],
        sort_by: SortBy
    ) -> List[SearchResult]:
        """
        ترتيب النتائج حسب المعيار المحدد
        Sort results by specified criteria
        
        Args:
            results: قائمة النتائج
            sort_by: معيار الترتيب
            
        Returns:
            قائمة النتائج المرتبة
        """
        if sort_by == SortBy.RELEVANCE:
            return sorted(results, key=lambda x: x.relevance_score, reverse=True)
        
        elif sort_by == SortBy.DISTANCE:
            return sorted(results, key=lambda x: x.distance_km)
        
        elif sort_by == SortBy.RATING:
            return sorted(results, key=lambda x: x.facility.performance.overall_rating, reverse=True)
        
        elif sort_by == SortBy.AVAILABILITY:
            return sorted(results, key=lambda x: x.facility.performance.current_occupancy)
        
        elif sort_by == SortBy.PERFORMANCE:
            # ترتيب حسب مجموعة من المقاييس
            return sorted(
                results,
                key=lambda x: (
                    x.facility.performance.overall_rating * 0.4 +
                    (100 - x.facility.performance.current_occupancy) * 0.3 +
                    x.facility.performance.patient_satisfaction * 0.3
                ),
                reverse=True
            )
        
        return results
    
    def generate_recommendation_reason(
        self,
        facility: FacilityProfile,
        filters: SearchFilters,
        distance_km: float,
        matched_specialties: List[str]
    ) -> str:
        """
        توليد سبب التوصية بالمنشأة
        Generate recommendation reason
        
        Args:
            facility: المنشأة
            filters: الفلاتر
            distance_km: المسافة
            matched_specialties: التخصصات المطابقة
            
        Returns:
            سبب التوصية
        """
        reasons = []
        
        # القرب
        if distance_km <= 5:
            reasons.append(f"قريب جداً ({distance_km} كم)")
        elif distance_km <= 10:
            reasons.append(f"قريب ({distance_km} كم)")
        
        # التقييم
        if facility.performance.overall_rating >= 4.5:
            reasons.append(f"تقييم ممتاز ({facility.performance.overall_rating}/5)")
        elif facility.performance.overall_rating >= 4.0:
            reasons.append(f"تقييم جيد ({facility.performance.overall_rating}/5)")
        
        # وقت الانتظار
        if facility.performance.avg_wait_time_minutes <= 15:
            reasons.append("وقت انتظار قصير")
        
        # التخصصات
        if matched_specialties:
            if len(matched_specialties) == 1:
                reasons.append(f"متخصص في {matched_specialties[0]}")
            else:
                reasons.append(f"يوفر {len(matched_specialties)} تخصصات مطلوبة")
        
        # التوفر
        if facility.performance.current_occupancy < 70:
            reasons.append("متوفر حالياً")
        
        # رضا المرضى
        if facility.performance.patient_satisfaction >= 90:
            reasons.append(f"رضا مرتفع ({facility.performance.patient_satisfaction}%)")
        
        if reasons:
            return " • " + " • ".join(reasons)
        else:
            return "منشأة موصى بها"
    
    def search(
        self,
        facilities: List[FacilityProfile],
        filters: SearchFilters
    ) -> SearchResponse:
        """
        تنفيذ البحث المتقدم
        Execute advanced search
        
        Args:
            facilities: قائمة المنشآت
            filters: فلاتر البحث
            
        Returns:
            نتائج البحث
        """
        start_time = datetime.now()
        
        # تطبيق الفلاتر
        filtered_facilities = self.apply_filters(facilities, filters)
        
        # إنشاء نتائج البحث
        results = []
        for facility, distance_km in filtered_facilities:
            # حساب درجة الصلة
            relevance_score = self.calculate_relevance_score(facility, filters, distance_km)
            
            # التخصصات المطابقة
            matched_specialties = []
            if filters.specialties:
                matched_specialties = list(set(facility.specialties) & set(filters.specialties))
            
            # الخدمات المطابقة
            matched_services = []
            if filters.required_services:
                matched_services = list(set(facility.services) & set(filters.required_services))
            
            # حساب التوفر
            is_available = facility.performance.current_occupancy < 90
            estimated_wait_time = facility.performance.avg_wait_time_minutes
            
            # توليد سبب التوصية
            recommendation_reason = self.generate_recommendation_reason(
                facility, filters, distance_km, matched_specialties
            )
            
            # إنشاء نتيجة البحث
            result = SearchResult(
                facility=facility,
                relevance_score=relevance_score,
                distance_km=distance_km,
                is_available=is_available,
                estimated_wait_time=estimated_wait_time,
                matched_specialties=matched_specialties,
                matched_services=matched_services,
                recommendation_reason=recommendation_reason
            )
            
            results.append(result)
        
        # ترتيب النتائج
        results = self.sort_results(results, filters.sort_by)
        
        # حساب الإحصائيات
        stats = {}
        if results:
            stats = {
                "avg_distance": round(sum(r.distance_km for r in results) / len(results), 2),
                "avg_rating": round(sum(r.facility.performance.overall_rating for r in results) / len(results), 2),
                "avg_wait_time": round(sum(r.estimated_wait_time for r in results) / len(results), 0),
                "available_count": sum(1 for r in results if r.is_available),
            }
        
        # التصفح (Pagination)
        total_results = len(results)
        total_pages = math.ceil(total_results / filters.limit)
        start_idx = (filters.page - 1) * filters.limit
        end_idx = start_idx + filters.limit
        paginated_results = results[start_idx:end_idx]
        
        # حساب وقت البحث
        search_time = (datetime.now() - start_time).total_seconds() * 1000
        
        # إنشاء الاستجابة
        response = SearchResponse(
            results=paginated_results,
            total_results=total_results,
            page=filters.page,
            limit=filters.limit,
            total_pages=total_pages,
            applied_filters={
                "specialties": filters.specialties,
                "organizations": filters.organizations,
                "clusters": filters.clusters,
                "min_rating": filters.min_rating,
                "max_distance_km": filters.max_distance_km,
                "sort_by": filters.sort_by.value,
            },
            stats=stats,
            search_time_ms=round(search_time, 2)
        )
        
        return response
    
    def get_facility_by_id(
        self,
        facilities: List[FacilityProfile],
        facility_id: int
    ) -> Optional[FacilityProfile]:
        """
        الحصول على منشأة بواسطة المعرف
        Get facility by ID
        
        Args:
            facilities: قائمة المنشآت
            facility_id: معرف المنشأة
            
        Returns:
            المنشأة أو None
        """
        for facility in facilities:
            if facility.id == facility_id:
                return facility
        return None
    
    def compare_facilities(
        self,
        facilities: List[FacilityProfile],
        facility_ids: List[int]
    ) -> Dict:
        """
        مقارنة بين عدة منشآت
        Compare multiple facilities
        
        Args:
            facilities: قائمة المنشآت
            facility_ids: معرفات المنشآت للمقارنة
            
        Returns:
            نتيجة المقارنة
        """
        selected_facilities = [
            f for f in facilities if f.id in facility_ids
        ]
        
        if not selected_facilities:
            return {"error": "لم يتم العثور على المنشآت المحددة"}
        
        comparison = {
            "facilities": [
                {
                    "id": f.id,
                    "name": f.name,
                    "organization": f.organization,
                }
                for f in selected_facilities
            ],
            "metrics": {
                "rating": [f.performance.overall_rating for f in selected_facilities],
                "wait_time": [f.performance.avg_wait_time_minutes for f in selected_facilities],
                "patient_satisfaction": [f.performance.patient_satisfaction for f in selected_facilities],
                "occupancy": [f.performance.current_occupancy for f in selected_facilities],
                "total_beds": [f.total_beds for f in selected_facilities],
                "total_doctors": [f.total_doctors for f in selected_facilities],
            }
        }
        
        # تحديد الأفضل
        best_idx = 0
        best_score = 0
        for i, f in enumerate(selected_facilities):
            score = (
                f.performance.overall_rating * 0.3 +
                (100 - f.performance.avg_wait_time_minutes) / 100 * 0.3 +
                f.performance.patient_satisfaction * 0.4
            )
            if score > best_score:
                best_score = score
                best_idx = i
        
        comparison["recommended"] = {
            "id": selected_facilities[best_idx].id,
            "name": selected_facilities[best_idx].name,
            "reason": "الأفضل حسب التقييم الشامل"
        }
        
        return comparison


# مثيل عام من الخدمة
search_service = AdvancedSearchService()

