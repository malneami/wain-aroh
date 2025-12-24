"""
GPS Location Service for Wain Aroh
Detects patient location and finds nearest facilities
"""

from src.data.facilities_ngh import (
    FACILITIES, 
    get_main_hospital,
    find_nearest_facilities,
    calculate_distance
)

class LocationService:
    def __init__(self):
        self.main_hospital = get_main_hospital()
    
    def request_location_permission(self):
        """Generate message to request GPS permission"""
        return {
            'message': """
لتوجيهك إلى أقرب مركز رعاية، نحتاج إلى معرفة موقعك الحالي.

يرجى السماح بالوصول إلى الموقع الجغرافي (GPS) أو مشاركة موقعك الحالي.

📍 سيتم استخدام موقعك فقط لتحديد أقرب مركز رعاية مناسب لحالتك.
🔒 معلومات موقعك محمية وآمنة.
""",
            'request_gps': True,
            'permission_required': True
        }
    
    def get_patient_location(self, gps_data):
        """Process GPS data from patient"""
        if not gps_data:
            return None
        
        # Extract coordinates
        lat = gps_data.get('latitude')
        lng = gps_data.get('longitude')
        
        if not lat or not lng:
            return None
        
        # Calculate distance from main hospital
        distance_from_main = calculate_distance(
            lat, lng,
            self.main_hospital['coordinates']['lat'],
            self.main_hospital['coordinates']['lng']
        )
        
        return {
            'latitude': lat,
            'longitude': lng,
            'distance_from_main_hospital_km': round(distance_from_main, 2),
            'within_5km_of_main': distance_from_main <= 5,
            'within_10km_of_main': distance_from_main <= 10
        }
    
    def find_best_facility(self, patient_location, ctas_level, preferred_type=None):
        """Find best facility based on location and CTAS level"""
        
        if not patient_location:
            # No location - default to main hospital for critical cases
            if ctas_level <= 2:
                return {
                    'facility': self.main_hospital,
                    'reason': 'حالة حرجة - يجب التوجه للطوارئ الرئيسية',
                    'distance_km': None
                }
            else:
                # Return main hospital as fallback
                return {
                    'facility': self.main_hospital,
                    'reason': 'لم يتم تحديد الموقع',
                    'distance_km': None
                }
        
        lat = patient_location['latitude']
        lng = patient_location['longitude']
        
        # Decision logic based on CTAS level
        if ctas_level == 1:
            # CTAS 1 (Resuscitation) - Always main hospital
            facility = self.main_hospital
            reason = "حالة حرجة جداً - يجب التوجه فوراً لطوارئ مستشفى الحرس الوطني"
        
        elif ctas_level == 2:
            # CTAS 2 (Emergent) - Main hospital or nearest ED
            distance_from_main = patient_location['distance_from_main_hospital_km']
            
            if distance_from_main <= 15:
                # Within 15km - go to main hospital
                facility = self.main_hospital
                reason = f"حالة طارئة - التوجه لطوارئ مستشفى الحرس الوطني (المسافة: {distance_from_main:.1f} كم)"
            else:
                # Too far - find nearest emergency
                facility = self.main_hospital  # For now, still recommend main
                reason = f"حالة طارئة - يُنصح بالتوجه لأقرب طوارئ أو الاتصال بالإسعاف 997"
        
        elif ctas_level == 3:
            # CTAS 3 (Urgent) - UCC if close, otherwise main hospital
            nearest_uccs = find_nearest_facilities(lat, lng, 'ucc', ctas_level, limit=3)
            
            if nearest_uccs and nearest_uccs[0]['distance_km'] <= 10:
                # UCC is close
                facility = nearest_uccs[0]
                reason = f"حالة عاجلة - يمكنك التوجه لمركز الرعاية العاجلة (المسافة: {facility['distance_km']:.1f} كم)"
            else:
                # UCC too far - main hospital
                facility = self.main_hospital
                reason = "حالة عاجلة - يُنصح بالتوجه لطوارئ مستشفى الحرس الوطني"
        
        elif ctas_level == 4:
            # CTAS 4 (Less Urgent) - UCC or clinic
            if preferred_type == 'clinic':
                nearest = find_nearest_facilities(lat, lng, 'clinic', ctas_level, limit=1)
            else:
                nearest = find_nearest_facilities(lat, lng, 'ucc', ctas_level, limit=1)
            
            if nearest:
                facility = nearest[0]
                reason = f"حالة غير عاجلة - يمكنك التوجه لأقرب مركز رعاية (المسافة: {facility['distance_km']:.1f} كم)"
            else:
                facility = self.main_hospital
                reason = "يمكنك التوجه لمستشفى الحرس الوطني"
        
        else:  # CTAS 5
            # CTAS 5 (Non-Urgent) - Clinic or virtual OPD
            if preferred_type == 'virtual':
                from src.data.facilities_ngh import get_virtual_opd
                facility = get_virtual_opd()
                reason = "حالة بسيطة - يمكنك استخدام العيادات الافتراضية"
            else:
                nearest_clinics = find_nearest_facilities(lat, lng, 'clinic', ctas_level, limit=1)
                if nearest_clinics:
                    facility = nearest_clinics[0]
                    reason = f"حالة بسيطة - يمكنك حجز موعد في العيادة (المسافة: {facility['distance_km']:.1f} كم)"
                else:
                    from src.data.facilities_ngh import get_virtual_opd
                    facility = get_virtual_opd()
                    reason = "حالة بسيطة - يُنصح بالعيادات الافتراضية"
        
        return {
            'facility': facility,
            'reason': reason,
            'distance_km': facility.get('distance_km'),
            'estimated_travel_time_minutes': self.estimate_travel_time(facility.get('distance_km'))
        }
    
    def estimate_travel_time(self, distance_km):
        """Estimate travel time based on distance"""
        if not distance_km:
            return None
        
        # Assume average speed of 40 km/h in Riyadh traffic
        time_hours = distance_km / 40
        time_minutes = int(time_hours * 60)
        
        return max(5, time_minutes)  # Minimum 5 minutes
    
    def get_directions_url(self, patient_location, facility):
        """Generate Google Maps directions URL"""
        if not patient_location:
            # Just show facility location
            return f"https://www.google.com/maps/search/?api=1&query={facility['coordinates']['lat']},{facility['coordinates']['lng']}"
        
        # Directions from patient to facility
        origin = f"{patient_location['latitude']},{patient_location['longitude']}"
        destination = f"{facility['coordinates']['lat']},{facility['coordinates']['lng']}"
        
        return f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=driving"
    
    def get_all_nearby_options(self, patient_location, ctas_level):
        """Get all nearby facility options"""
        if not patient_location:
            return []
        
        lat = patient_location['latitude']
        lng = patient_location['longitude']
        
        # Find all suitable facilities
        all_facilities = find_nearest_facilities(lat, lng, facility_type=None, ctas_level=ctas_level, limit=5)
        
        options = []
        for facility in all_facilities:
            options.append({
                'facility': facility,
                'distance_km': facility['distance_km'],
                'travel_time_minutes': self.estimate_travel_time(facility['distance_km']),
                'wait_time_minutes': facility.get('wait_time_minutes', 30),
                'total_time_minutes': self.estimate_travel_time(facility['distance_km']) + facility.get('wait_time_minutes', 30),
                'directions_url': self.get_directions_url(patient_location, facility)
            })
        
        # Sort by total time
        options.sort(key=lambda x: x['total_time_minutes'])
        
        return options
    
    def format_facility_recommendation(self, recommendation, patient_location=None):
        """Format facility recommendation as Arabic message"""
        
        facility = recommendation['facility']
        reason = recommendation['reason']
        distance = recommendation.get('distance_km')
        travel_time = recommendation.get('estimated_travel_time_minutes')
        
        message = f"""
📍 **التوجيه الطبي**

{reason}

**{facility['name']}**
📌 العنوان: {facility['location']}
📞 الهاتف: {facility['phone']}
⏰ ساعات العمل: {facility['hours']}
"""
        
        if distance:
            message += f"🚗 المسافة: {distance:.1f} كم\n"
        
        if travel_time:
            message += f"⏱️ الوقت المتوقع للوصول: {travel_time} دقيقة\n"
        
        if facility.get('wait_time_minutes'):
            message += f"⏳ وقت الانتظار المتوقع: {facility['wait_time_minutes']} دقيقة\n"
        
        # Add directions link
        if patient_location:
            directions_url = self.get_directions_url(patient_location, facility)
            message += f"\n🗺️ [اضغط هنا للحصول على الاتجاهات]({directions_url})\n"
        
        # Add special instructions based on CTAS
        if facility.get('is_main_hub'):
            message += "\n⚠️ **تعليمات مهمة:**\n"
            message += "- توجه مباشرة إلى قسم الطوارئ\n"
            message += "- أحضر بطاقة الهوية وبطاقة التأمين\n"
            message += "- إذا كانت حالتك حرجة، اتصل بالإسعاف 997\n"
        
        return message

# Initialize service
location_service = LocationService()

