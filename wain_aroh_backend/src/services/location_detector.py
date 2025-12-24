"""
Automatic Location Detection Service
Seamlessly detects patient location and finds nearest appropriate facility
"""

from src.services.location_service import location_service
from src.data.facilities_ngh import FACILITIES, find_nearest_facilities
import json

class LocationDetector:
    """
    Handles automatic location detection and facility recommendation
    """
    
    def __init__(self):
        self.location_cache = {}
    
    def request_location_with_context(self, ctas_level, symptoms):
        """
        Generate contextual location request message based on patient condition
        """
        
        if ctas_level <= 2:
            # Emergency - urgent location request
            message = """⚠️ **هذه حالة طارئة**

لتوجيهك إلى أقرب طوارئ فوراً، أحتاج معرفة موقعك الحالي.

📍 **اضغط على زر "مشاركة موقعي" أدناه**

أو أخبرني في أي حي أنت الآن؟

⏱️ كل ثانية مهمة - شارك موقعك الآن."""

        elif ctas_level == 3:
            # Urgent - polite location request
            message = """لتوجيهك إلى أقرب مركز رعاية عاجلة، أحتاج معرفة موقعك الحالي.

📍 **اضغط على زر "مشاركة موقعي" أدناه**

سأستخدم موقعك فقط لإيجاد أقرب مركز رعاية مناسب لحالتك.

أو يمكنك إخباري في أي حي أنت الآن؟"""

        else:
            # Non-urgent - optional location request
            message = """لمساعدتك في إيجاد أقرب عيادة أو مركز رعاية، هل يمكنك مشاركة موقعك؟

📍 **اضغط على زر "مشاركة موقعي" أدناه**

أو أخبرني في أي حي تسكن؟

💡 مشاركة الموقع اختيارية، لكنها ستساعدني في إيجاد أقرب مركز لك."""

        return {
            'request_location': True,
            'message': message,
            'urgency': 'high' if ctas_level <= 2 else 'medium' if ctas_level == 3 else 'low',
            'auto_detect': ctas_level <= 2  # Auto-trigger GPS for emergencies
        }
    
    def detect_location_from_text(self, text):
        """
        Extract location from text (neighborhood name, area, etc.)
        """
        
        # Common Riyadh neighborhoods and their coordinates
        neighborhoods = {
            # North Riyadh
            'الملقا': {'latitude': 24.7767, 'longitude': 46.6106, 'name': 'Al Malqa'},
            'النخيل': {'latitude': 24.7900, 'longitude': 46.6200, 'name': 'Al Nakheel'},
            'الصحافة': {'latitude': 24.7650, 'longitude': 46.6250, 'name': 'Al Sahafa'},
            'الياسمين': {'latitude': 24.8000, 'longitude': 46.6300, 'name': 'Al Yasmin'},
            'الربيع': {'latitude': 24.7850, 'longitude': 46.6400, 'name': 'Al Rabie'},
            
            # Central Riyadh
            'العليا': {'latitude': 24.7100, 'longitude': 46.6700, 'name': 'Al Olaya'},
            'السليمانية': {'latitude': 24.7050, 'longitude': 46.6850, 'name': 'Al Sulaimaniyah'},
            'الملز': {'latitude': 24.6900, 'longitude': 46.7000, 'name': 'Al Malaz'},
            'المرسلات': {'latitude': 24.6850, 'longitude': 46.7100, 'name': 'Al Mursalat'},
            
            # West Riyadh
            'الربوة': {'latitude': 24.7300, 'longitude': 46.5900, 'name': 'Al Rabwa'},
            'الازدهار': {'latitude': 24.7400, 'longitude': 46.5800, 'name': 'Al Izdihar'},
            'النرجس': {'latitude': 24.7500, 'longitude': 46.5700, 'name': 'Al Narjis'},
            'الورود': {'latitude': 24.7200, 'longitude': 46.6000, 'name': 'Al Wurud'},
            
            # South Riyadh
            'العزيزية': {'latitude': 24.6500, 'longitude': 46.7200, 'name': 'Al Aziziyah'},
            'منفوحة': {'latitude': 24.6300, 'longitude': 46.7000, 'name': 'Manfuha'},
            'الشفا': {'latitude': 24.6400, 'longitude': 46.6800, 'name': 'Al Shifa'},
            
            # East Riyadh
            'الروضة': {'latitude': 24.7300, 'longitude': 46.7500, 'name': 'Al Rawdah'},
            'الريان': {'latitude': 24.7200, 'longitude': 46.7600, 'name': 'Al Rayyan'},
            'النهضة': {'latitude': 24.7100, 'longitude': 46.7700, 'name': 'Al Nahdah'},
        }
        
        # Search for neighborhood name in text
        text_lower = text.lower()
        
        for arabic_name, coords in neighborhoods.items():
            if arabic_name in text or coords['name'].lower() in text_lower:
                return {
                    'detected': True,
                    'method': 'text',
                    'neighborhood': arabic_name,
                    'latitude': coords['latitude'],
                    'longitude': coords['longitude'],
                    'accuracy': 'neighborhood'
                }
        
        return {
            'detected': False,
            'message': 'لم أتمكن من تحديد الحي. يرجى مشاركة موقعك عبر GPS أو ذكر اسم الحي بوضوح.'
        }
    
    def process_gps_location(self, latitude, longitude):
        """
        Process GPS coordinates and get detailed location info
        """
        
        location = location_service.get_patient_location({
            'latitude': latitude,
            'longitude': longitude
        })
        
        return {
            'detected': True,
            'method': 'gps',
            'latitude': latitude,
            'longitude': longitude,
            'accuracy': 'precise',
            'distance_from_main': location.get('distance_from_main_hospital_km'),
            'within_5km': location.get('within_5km_of_main'),
            'within_10km': location.get('within_10km_of_main')
        }
    
    def find_nearest_facility_for_patient(self, patient_location, ctas_level, condition=None):
        """
        Find the most appropriate nearest facility based on location and CTAS
        """
        
        # Get recommendation from location service
        recommendation = location_service.find_best_facility(
            patient_location,
            ctas_level
        )
        
        facility = recommendation['facility']
        
        # Calculate additional details
        distance_km = recommendation.get('distance_km', 0)
        travel_time = location_service.estimate_travel_time(distance_km)
        directions_url = location_service.get_directions_url(patient_location, facility)
        
        # Get alternative options
        all_nearby = find_nearest_facilities(
            patient_location['latitude'],
            patient_location['longitude'],
            ctas_level=ctas_level,
            limit=5
        )
        
        # Format comprehensive response
        response = {
            'primary_recommendation': {
                'facility': facility,
                'reason': recommendation['reason'],
                'distance_km': distance_km,
                'travel_time_minutes': travel_time,
                'directions_url': directions_url,
                'wait_time_minutes': facility.get('wait_time_minutes', 30)
            },
            'alternatives': []
        }
        
        # Add alternatives (excluding primary)
        for alt_facility in all_nearby[1:]:  # Skip first (primary)
            alt_distance = alt_facility.get('distance_km', 0)
            alt_travel_time = location_service.estimate_travel_time(alt_distance)
            alt_directions = location_service.get_directions_url(patient_location, alt_facility)
            
            response['alternatives'].append({
                'facility': alt_facility,
                'distance_km': alt_distance,
                'travel_time_minutes': alt_travel_time,
                'directions_url': alt_directions,
                'wait_time_minutes': alt_facility.get('wait_time_minutes', 30)
            })
        
        return response
    
    def format_location_confirmation(self, location_data):
        """
        Format a friendly confirmation message after location is detected
        """
        
        if location_data['method'] == 'gps':
            message = f"""✅ **تم تحديد موقعك**

📍 الموقع الحالي: تم الحصول عليه بدقة
📏 المسافة من المستشفى الرئيسي: {location_data['distance_from_main']:.1f} كم

جاري البحث عن أقرب مركز رعاية مناسب لحالتك..."""

        else:  # text/neighborhood
            message = f"""✅ **تم تحديد موقعك**

📍 الحي: {location_data['neighborhood']}

جاري البحث عن أقرب مركز رعاية مناسب..."""

        return message
    
    def format_facility_recommendation_detailed(self, recommendation_data, ctas_level):
        """
        Format detailed facility recommendation with alternatives
        """
        
        primary = recommendation_data['primary_recommendation']
        facility = primary['facility']
        
        # Build main recommendation message
        message = f"""📍 **التوجيه الطبي**

بناءً على حالتك وموقعك، أنصحك بالتوجه إلى:

🏥 **{facility['name']}**

{primary['reason']}

**📋 التفاصيل:**
📌 العنوان: {facility['location']}
📞 الهاتف: {facility['phone']}
⏰ ساعات العمل: {facility['hours']}
🚗 المسافة: {primary['distance_km']:.1f} كم
⏱️ الوقت المتوقع للوصول: {primary['travel_time_minutes']} دقيقة
⏳ وقت الانتظار المتوقع: {primary['wait_time_minutes']} دقيقة

🗺️ [اضغط هنا للحصول على الاتجاهات]({primary['directions_url']})
"""

        # Add special instructions for emergencies
        if ctas_level <= 2:
            message += f"""
⚠️ **تعليمات مهمة:**
- توجه فوراً - لا تتأخر
- إذا كانت حالتك حرجة جداً، اتصل بالإسعاف 997
- لا تقود بنفسك إذا كنت تشعر بدوار أو ضعف
- توجه مباشرة إلى قسم الطوارئ
"""

        # Add alternatives if available
        if recommendation_data['alternatives']:
            message += "\n**🏥 خيارات بديلة قريبة:**\n\n"
            
            for i, alt in enumerate(recommendation_data['alternatives'][:3], 1):
                alt_facility = alt['facility']
                message += f"{i}. **{alt_facility['name']}**\n"
                message += f"   📏 {alt['distance_km']:.1f} كم ({alt['travel_time_minutes']} دقيقة)\n"
                message += f"   ⏳ انتظار: {alt['wait_time_minutes']} دقيقة\n"
                message += f"   🗺️ [الاتجاهات]({alt['directions_url']})\n\n"
        
        # Add closing
        if ctas_level <= 2:
            message += "\n⚠️ **يرجى التوجه فوراً**"
        else:
            message += "\nهل هناك شيء آخر يمكنني مساعدتك فيه؟"
        
        return message
    
    def get_location_status_message(self, session_id):
        """
        Get current location detection status for a session
        """
        
        if session_id in self.location_cache:
            location = self.location_cache[session_id]
            
            if location['method'] == 'gps':
                return f"📍 الموقع الحالي: محدد بدقة ({location['distance_from_main']:.1f} كم من المستشفى الرئيسي)"
            else:
                return f"📍 الموقع الحالي: {location['neighborhood']}"
        
        return "📍 الموقع: غير محدد"
    
    def clear_location_cache(self, session_id):
        """
        Clear cached location for a session
        """
        if session_id in self.location_cache:
            del self.location_cache[session_id]
    
    def update_location_cache(self, session_id, location_data):
        """
        Update cached location for a session
        """
        self.location_cache[session_id] = location_data

# Initialize location detector
location_detector = LocationDetector()

