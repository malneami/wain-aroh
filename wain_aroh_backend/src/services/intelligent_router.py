"""
Intelligent Hospital Routing Service
Routes patients to the nearest hospital with required service available
Ranking: Availability → Distance → Hospital Level
"""

from datetime import datetime
from typing import List, Dict, Optional, Tuple
from sqlalchemy import and_, or_, func
from ..models.user import db
from ..models.hospital import Hospital
from ..models.service_schedule import (
    HospitalService, ServiceSchedule, ScheduleOverride,
    ServiceRequest, is_service_available
)
import math

class IntelligentRouter:
    """Routes patients to appropriate hospitals based on service availability and location"""
    
    # Hospital level priorities (higher = better)
    HOSPITAL_LEVEL_PRIORITY = {
        "central": 100,
        "specialized": 90,
        "general": 80,
        "district": 70,
        "urgent_care_center": 60,
        "clinic": 50
    }
    
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two points using Haversine formula
        Returns distance in kilometers
        """
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return round(distance, 2)
    
    @staticmethod
    def find_nearest_with_service(
        patient_lat: float,
        patient_lon: float,
        service_type: str,
        check_datetime: datetime = None,
        max_distance_km: float = 50.0,
        limit: int = 10,
        patient_city: str = None,
        ctas_level: int = None
    ) -> List[Dict]:
        """
        Find nearest hospitals with required service available
        
        Args:
            patient_lat: Patient latitude
            patient_lon: Patient longitude
            service_type: Required service type
            check_datetime: DateTime to check availability (default: now)
            max_distance_km: Maximum search radius in km
            limit: Maximum number of results
            patient_city: Patient city (for logging)
            ctas_level: CTAS level (1-5) for priority routing
        
        Returns:
            List of hospitals with availability, distance, and ranking
        """
        if check_datetime is None:
            check_datetime = datetime.now()
        
        # Get all hospitals with the required service
        services = db.session.query(HospitalService, Hospital).join(
            Hospital, HospitalService.hospital_id == Hospital.id
        ).filter(
            HospitalService.service_type == service_type,
            HospitalService.is_active == True,
            Hospital.is_active == True
        ).all()
        
        results = []
        
        for service, hospital in services:
            # Calculate distance
            distance = IntelligentRouter.calculate_distance(
                patient_lat, patient_lon,
                hospital.latitude, hospital.longitude
            )
            
            # Skip if too far
            if distance > max_distance_km:
                continue
            
            # Check availability
            availability = is_service_available(service.id, check_datetime)
            
            # Calculate ranking score
            ranking_score = IntelligentRouter._calculate_ranking_score(
                availability=availability,
                distance=distance,
                hospital=hospital,
                ctas_level=ctas_level
            )
            
            results.append({
                "hospital_id": hospital.id,
                "hospital_name_ar": hospital.name_ar,
                "hospital_name_en": hospital.name_en,
                "hospital_type": hospital.facility_type,
                "address_ar": hospital.address_ar,
                "address_en": hospital.address_en,
                "city": hospital.city,
                "phone": hospital.phone,
                "latitude": hospital.latitude,
                "longitude": hospital.longitude,
                "distance_km": distance,
                "service_id": service.id,
                "service_name_ar": service.service_name_ar,
                "service_name_en": service.service_name_en,
                "available": availability["available"],
                "availability_status": availability["status"],
                "availability_reason": availability.get("reason"),
                "on_call": availability.get("on_call"),
                "capacity": availability.get("capacity"),
                "wait_time_minutes": availability.get("wait_time"),
                "requires_appointment": service.requires_appointment,
                "service_phone": service.phone,
                "service_extension": service.extension,
                "ranking_score": ranking_score,
                "ranking_breakdown": {
                    "availability_score": IntelligentRouter._get_availability_score(availability),
                    "distance_score": IntelligentRouter._get_distance_score(distance),
                    "hospital_level_score": IntelligentRouter._get_hospital_level_score(hospital),
                    "ctas_priority_bonus": IntelligentRouter._get_ctas_priority_bonus(ctas_level, hospital)
                }
            })
        
        # Sort by ranking score (descending)
        results.sort(key=lambda x: x["ranking_score"], reverse=True)
        
        # Limit results
        results = results[:limit]
        
        # Log the request
        if results:
            best_result = results[0]
            IntelligentRouter._log_request(
                service_type=service_type,
                patient_lat=patient_lat,
                patient_lon=patient_lon,
                patient_city=patient_city,
                recommended_hospital_id=best_result["hospital_id"],
                recommended_service_id=best_result["service_id"],
                distance_km=best_result["distance_km"],
                was_available=best_result["available"],
                availability_status=best_result["availability_status"],
                wait_time_minutes=best_result.get("wait_time_minutes")
            )
        
        return results
    
    @staticmethod
    def _calculate_ranking_score(
        availability: dict,
        distance: float,
        hospital: Hospital,
        ctas_level: int = None
    ) -> float:
        """
        Calculate ranking score for a hospital
        Priority: Availability (60%) → Distance (30%) → Hospital Level (10%)
        """
        # Availability score (0-600 points)
        availability_score = IntelligentRouter._get_availability_score(availability)
        
        # Distance score (0-300 points)
        distance_score = IntelligentRouter._get_distance_score(distance)
        
        # Hospital level score (0-100 points)
        hospital_level_score = IntelligentRouter._get_hospital_level_score(hospital)
        
        # CTAS priority bonus (0-100 points for critical cases)
        ctas_bonus = IntelligentRouter._get_ctas_priority_bonus(ctas_level, hospital)
        
        total_score = availability_score + distance_score + hospital_level_score + ctas_bonus
        
        return round(total_score, 2)
    
    @staticmethod
    def _get_availability_score(availability: dict) -> float:
        """Calculate availability score (0-600 points)"""
        if not availability["available"]:
            return 0
        
        status = availability["status"]
        
        if status == "available":
            base_score = 600
        elif status == "limited":
            base_score = 400
        elif status == "on_call_only":
            base_score = 300
        else:
            return 0
        
        # Reduce score based on wait time
        wait_time = availability.get("wait_time", 0)
        if wait_time:
            # Reduce 1 point per minute of wait time (max 100 points reduction)
            wait_penalty = min(wait_time, 100)
            base_score -= wait_penalty
        
        return max(base_score, 0)
    
    @staticmethod
    def _get_distance_score(distance: float) -> float:
        """Calculate distance score (0-300 points)"""
        # Closer is better
        # 0 km = 300 points
        # 10 km = 200 points
        # 20 km = 100 points
        # 50+ km = 0 points
        
        if distance <= 0:
            return 300
        elif distance <= 10:
            return 300 - (distance * 10)
        elif distance <= 20:
            return 200 - ((distance - 10) * 10)
        elif distance <= 50:
            return 100 - ((distance - 20) * 3.33)
        else:
            return 0
    
    @staticmethod
    def _get_hospital_level_score(hospital: Hospital) -> float:
        """Calculate hospital level score (0-100 points)"""
        facility_type = hospital.facility_type or "clinic"
        return IntelligentRouter.HOSPITAL_LEVEL_PRIORITY.get(facility_type, 50)
    
    @staticmethod
    def _get_ctas_priority_bonus(ctas_level: int, hospital: Hospital) -> float:
        """Calculate CTAS priority bonus (0-100 points)"""
        if not ctas_level:
            return 0
        
        # Critical cases (CTAS 1-2) get bonus for emergency hospitals
        if ctas_level <= 2:
            if hospital.is_emergency:
                return 100
            else:
                return 0
        
        # Urgent cases (CTAS 3) get bonus for urgent care centers
        elif ctas_level == 3:
            if hospital.facility_type == "urgent_care_center":
                return 50
            elif hospital.is_emergency:
                return 30
            else:
                return 0
        
        # Less urgent cases (CTAS 4-5) prefer clinics/UCCs
        else:
            if hospital.facility_type in ["clinic", "urgent_care_center"]:
                return 30
            else:
                return 0
    
    @staticmethod
    def find_alternative_services(
        hospital_id: int,
        service_type: str,
        check_datetime: datetime = None,
        max_distance_km: float = 30.0
    ) -> List[Dict]:
        """
        Find alternative hospitals when primary hospital service is unavailable
        """
        # Get primary hospital location
        hospital = Hospital.query.get(hospital_id)
        if not hospital:
            return []
        
        # Find nearest alternatives
        return IntelligentRouter.find_nearest_with_service(
            patient_lat=hospital.latitude,
            patient_lon=hospital.longitude,
            service_type=service_type,
            check_datetime=check_datetime,
            max_distance_km=max_distance_km,
            limit=5
        )
    
    @staticmethod
    def get_service_coverage_map(
        service_type: str,
        check_datetime: datetime = None
    ) -> Dict:
        """
        Get a map of service coverage across all hospitals
        Returns: Dict with hospitals grouped by city and availability
        """
        if check_datetime is None:
            check_datetime = datetime.now()
        
        # Get all hospitals with the service
        services = db.session.query(HospitalService, Hospital).join(
            Hospital, HospitalService.hospital_id == Hospital.id
        ).filter(
            HospitalService.service_type == service_type,
            HospitalService.is_active == True,
            Hospital.is_active == True
        ).all()
        
        coverage_map = {}
        
        for service, hospital in services:
            city = hospital.city or "Unknown"
            
            if city not in coverage_map:
                coverage_map[city] = {
                    "city": city,
                    "total_facilities": 0,
                    "available_now": 0,
                    "limited_availability": 0,
                    "unavailable": 0,
                    "facilities": []
                }
            
            # Check availability
            availability = is_service_available(service.id, check_datetime)
            
            coverage_map[city]["total_facilities"] += 1
            
            if availability["available"]:
                if availability["status"] == "available":
                    coverage_map[city]["available_now"] += 1
                elif availability["status"] == "limited":
                    coverage_map[city]["limited_availability"] += 1
            else:
                coverage_map[city]["unavailable"] += 1
            
            coverage_map[city]["facilities"].append({
                "hospital_id": hospital.id,
                "hospital_name_ar": hospital.name_ar,
                "hospital_name_en": hospital.name_en,
                "available": availability["available"],
                "status": availability["status"],
                "latitude": hospital.latitude,
                "longitude": hospital.longitude
            })
        
        return coverage_map
    
    @staticmethod
    def _log_request(
        service_type: str,
        patient_lat: float,
        patient_lon: float,
        patient_city: str,
        recommended_hospital_id: int,
        recommended_service_id: int,
        distance_km: float,
        was_available: bool,
        availability_status: str,
        wait_time_minutes: int = None,
        session_id: str = None,
        user_id: int = None
    ):
        """Log a service request for analytics"""
        request = ServiceRequest(
            service_type=service_type,
            patient_latitude=patient_lat,
            patient_longitude=patient_lon,
            patient_city=patient_city,
            recommended_hospital_id=recommended_hospital_id,
            recommended_service_id=recommended_service_id,
            distance_km=distance_km,
            was_available=was_available,
            availability_status=availability_status,
            wait_time_minutes=wait_time_minutes,
            session_id=session_id,
            user_id=user_id
        )
        
        db.session.add(request)
        db.session.commit()
    
    @staticmethod
    def get_routing_analytics(
        start_date: datetime = None,
        end_date: datetime = None,
        service_type: str = None,
        city: str = None
    ) -> Dict:
        """Get analytics for routing decisions"""
        query = ServiceRequest.query
        
        if start_date:
            query = query.filter(ServiceRequest.request_datetime >= start_date)
        if end_date:
            query = query.filter(ServiceRequest.request_datetime <= end_date)
        if service_type:
            query = query.filter(ServiceRequest.service_type == service_type)
        if city:
            query = query.filter(ServiceRequest.patient_city == city)
        
        requests = query.all()
        
        if not requests:
            return {
                "total_requests": 0,
                "availability_rate": 0,
                "average_distance": 0,
                "average_wait_time": 0,
                "acceptance_rate": 0
            }
        
        total = len(requests)
        available = sum(1 for r in requests if r.was_available)
        accepted = sum(1 for r in requests if r.patient_accepted)
        total_distance = sum(r.distance_km for r in requests if r.distance_km)
        wait_times = [r.wait_time_minutes for r in requests if r.wait_time_minutes]
        
        return {
            "total_requests": total,
            "availability_rate": round((available / total) * 100, 2),
            "average_distance": round(total_distance / total, 2),
            "average_wait_time": round(sum(wait_times) / len(wait_times), 2) if wait_times else 0,
            "acceptance_rate": round((accepted / total) * 100, 2) if accepted > 0 else 0,
            "by_service_type": IntelligentRouter._group_by_field(requests, "service_type"),
            "by_city": IntelligentRouter._group_by_field(requests, "patient_city"),
            "by_status": IntelligentRouter._group_by_field(requests, "availability_status")
        }
    
    @staticmethod
    def _group_by_field(requests: List[ServiceRequest], field: str) -> Dict:
        """Group requests by a field and count"""
        groups = {}
        for request in requests:
            value = getattr(request, field, "Unknown")
            if value not in groups:
                groups[value] = 0
            groups[value] += 1
        return groups
