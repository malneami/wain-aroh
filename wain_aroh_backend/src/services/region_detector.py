"""
Region Detector Service
Detects patient region (Jazan, Riyadh, etc.) based on GPS coordinates or city name
"""

class RegionDetector:
    """Detects which region a patient is in based on location"""
    
    # Region boundaries (approximate)
    REGIONS = {
        "jazan": {
            "name_ar": "جازان",
            "name_en": "Jazan",
            "lat_min": 16.0,
            "lat_max": 18.0,
            "lon_min": 42.0,
            "lon_max": 43.5,
            "cities": [
                "جازان", "jazan", "jizan",
                "صبيا", "sabya",
                "أبو عريش", "abu arish", "abu areesh",
                "صامطة", "samtah",
                "بيش", "bish", "beish",
                "الدرب", "al darb", "darb",
                "ضمد", "damad",
                "العارضة", "al aridah", "aridah",
                "فرسان", "farasan",
                "الريث", "al raith", "raith",
                "العيدابي", "al aidabi", "aidabi",
                "الطوال", "al twal", "twal",
                "أحد المسارحة", "ahad al masarihah",
                "الحرث", "al harth", "harth",
                "بني مالك", "bani malik",
                "فيفا", "fifa",
                "الموسم", "al mawsim", "mawsim"
            ]
        },
        "riyadh": {
            "name_ar": "الرياض",
            "name_en": "Riyadh",
            "lat_min": 24.0,
            "lat_max": 25.5,
            "lon_min": 46.0,
            "lon_max": 47.5,
            "cities": [
                "الرياض", "riyadh",
                "الملقا", "malqa",
                "العليا", "olaya",
                "النخيل", "nakheel",
                "الربوة", "rabwa",
                "الملز", "malaz",
                "الديرة", "deira"
            ]
        }
    }
    
    @staticmethod
    def detect_region_by_coordinates(latitude: float, longitude: float) -> dict:
        """
        Detect region based on GPS coordinates
        
        Args:
            latitude: Patient latitude
            longitude: Patient longitude
            
        Returns:
            dict with region info or None if not in any region
        """
        for region_code, region_data in RegionDetector.REGIONS.items():
            if (region_data["lat_min"] <= latitude <= region_data["lat_max"] and
                region_data["lon_min"] <= longitude <= region_data["lon_max"]):
                return {
                    "code": region_code,
                    "name_ar": region_data["name_ar"],
                    "name_en": region_data["name_en"],
                    "confidence": "high"
                }
        
        return {
            "code": "unknown",
            "name_ar": "غير محدد",
            "name_en": "Unknown",
            "confidence": "none"
        }
    
    @staticmethod
    def detect_region_by_city(city_name: str) -> dict:
        """
        Detect region based on city name
        
        Args:
            city_name: City name in Arabic or English
            
        Returns:
            dict with region info or None if not found
        """
        city_lower = city_name.lower().strip()
        
        for region_code, region_data in RegionDetector.REGIONS.items():
            if city_lower in [c.lower() for c in region_data["cities"]]:
                return {
                    "code": region_code,
                    "name_ar": region_data["name_ar"],
                    "name_en": region_data["name_en"],
                    "confidence": "high"
                }
        
        return {
            "code": "unknown",
            "name_ar": "غير محدد",
            "name_en": "Unknown",
            "confidence": "none"
        }
    
    @staticmethod
    def detect_region(latitude: float = None, longitude: float = None, city: str = None) -> dict:
        """
        Detect region using available information
        
        Args:
            latitude: Patient latitude (optional)
            longitude: Patient longitude (optional)
            city: City name (optional)
            
        Returns:
            dict with region info
        """
        # Try coordinates first (most accurate)
        if latitude and longitude:
            region = RegionDetector.detect_region_by_coordinates(latitude, longitude)
            if region["code"] != "unknown":
                return region
        
        # Try city name
        if city:
            region = RegionDetector.detect_region_by_city(city)
            if region["code"] != "unknown":
                return region
        
        # Unknown region
        return {
            "code": "unknown",
            "name_ar": "غير محدد",
            "name_en": "Unknown",
            "confidence": "none"
        }
    
    @staticmethod
    def get_region_facilities_count(region_code: str) -> dict:
        """Get facility counts for a region"""
        facility_counts = {
            "jazan": {
                "hospitals": 22,
                "ucc_centers": 18,
                "total": 40,
                "emergency_24_7": 22,
                "cities_covered": 17
            },
            "riyadh": {
                "hospitals": 7,
                "ucc_centers": 3,
                "total": 10,
                "emergency_24_7": 7,
                "cities_covered": 5
            }
        }
        
        return facility_counts.get(region_code, {
            "hospitals": 0,
            "ucc_centers": 0,
            "total": 0,
            "emergency_24_7": 0,
            "cities_covered": 0
        })
    
    @staticmethod
    def get_region_message(region_code: str, ctas_level: int = None) -> str:
        """
        Get appropriate message for patient based on region and CTAS level
        
        Args:
            region_code: Region code (jazan, riyadh, unknown)
            ctas_level: CTAS level (1-5)
            
        Returns:
            Arabic message for the patient
        """
        if region_code == "jazan":
            if ctas_level and ctas_level <= 2:
                return """أنت في منطقة جازان. لديك 22 مستشفى بأقسام طوارئ متاحة 24/7.

سأوجهك إلى أقرب مستشفى طوارئ مناسب لحالتك."""
            elif ctas_level == 3:
                return """أنت في منطقة جازان. لديك 18 مركز رعاية عاجلة و22 مستشفى متاحة.

سأوجهك إلى أقرب مركز رعاية عاجلة أو مستشفى مناسب لحالتك."""
            else:
                return """أنت في منطقة جازان. لديك 18 مركز رعاية وعيادات متعددة متاحة.

سأوجهك إلى أقرب مركز رعاية مناسب لحالتك."""
        
        elif region_code == "riyadh":
            if ctas_level and ctas_level <= 2:
                return """أنت في منطقة الرياض. لديك عدة مستشفيات بأقسام طوارئ متاحة 24/7.

سأوجهك إلى أقرب مستشفى طوارئ مناسب لحالتك."""
            elif ctas_level == 3:
                return """أنت في منطقة الرياض. لديك 3 مراكز رعاية عاجلة ومستشفيات متعددة.

سأوجهك إلى أقرب مركز رعاية عاجلة أو مستشفى مناسب لحالتك."""
            else:
                return """أنت في منطقة الرياض. لديك عيادات ومراكز رعاية متعددة متاحة.

سأوجهك إلى أقرب مركز رعاية مناسب لحالتك."""
        
        else:
            return """عذراً، لم أتمكن من تحديد منطقتك بدقة.

حالياً نغطي منطقتي جازان (22 مستشفى + 18 مركز) والرياض (7 مستشفيات + 3 مراكز).

هل يمكنك تحديد المدينة التي أنت فيها؟"""

# Create singleton instance
region_detector = RegionDetector()
