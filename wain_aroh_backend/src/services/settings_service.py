"""
User Settings Service
Manages user preferences for hospitals, services, and notifications
"""

import json
from datetime import datetime

class SettingsService:
    """
    Manages user settings and preferences
    """
    
    def __init__(self):
        # In-memory storage (for prototype)
        # In production, use database
        self.user_settings = {}
    
    def get_user_settings(self, user_id):
        """Get user settings"""
        if user_id not in self.user_settings:
            # Return default settings
            return self.get_default_settings()
        return self.user_settings[user_id]
    
    def get_default_settings(self):
        """Default settings for new users"""
        return {
            "preferred_hospitals": [
                {
                    "id": 1,
                    "name": "مستشفى الحرس الوطني - الرياض",
                    "priority": 1,
                    "enabled": True
                }
            ],
            "preferred_services": {
                "emergency": True,
                "ucc": True,
                "clinic": True,
                "virtual_opd": True
            },
            "preferences": {
                "auto_direct": True,  # Automatically direct to preferred hospital
                "consider_waiting_time": True,  # Consider wait times in recommendations
                "max_waiting_time": 60,  # Max acceptable wait time (minutes)
                "max_distance": 20,  # Max distance willing to travel (km)
                "language": "ar",  # Arabic
                "voice_enabled": True
            },
            "notifications": {
                "sms_enabled": True,
                "email_enabled": False,
                "doctor_alerts": True  # Alert doctor for critical cases
            },
            "medical_info": {
                "has_insurance": True,
                "insurance_provider": "NGHA",
                "chronic_conditions": [],
                "allergies": [],
                "assigned_doctor": None  # Will be set if patient has assigned doctor
            }
        }
    
    def update_user_settings(self, user_id, settings):
        """Update user settings"""
        self.user_settings[user_id] = settings
        return {
            "success": True,
            "message": "تم تحديث الإعدادات بنجاح",
            "settings": settings
        }
    
    def add_preferred_hospital(self, user_id, hospital_id, hospital_name):
        """Add hospital to preferred list"""
        settings = self.get_user_settings(user_id)
        
        # Check if already in list
        for h in settings["preferred_hospitals"]:
            if h["id"] == hospital_id:
                return {
                    "success": False,
                    "error": "المستشفى موجود بالفعل في القائمة المفضلة"
                }
        
        # Add to list
        settings["preferred_hospitals"].append({
            "id": hospital_id,
            "name": hospital_name,
            "priority": len(settings["preferred_hospitals"]) + 1,
            "enabled": True
        })
        
        self.user_settings[user_id] = settings
        
        return {
            "success": True,
            "message": f"تمت إضافة {hospital_name} إلى المستشفيات المفضلة"
        }
    
    def set_assigned_doctor(self, user_id, doctor_info):
        """Set assigned doctor for patient"""
        settings = self.get_user_settings(user_id)
        settings["medical_info"]["assigned_doctor"] = doctor_info
        self.user_settings[user_id] = settings
        
        return {
            "success": True,
            "message": f"تم تعيين الطبيب: {doctor_info['name']}"
        }
    
    def should_auto_direct(self, user_id):
        """Check if auto-direct is enabled"""
        settings = self.get_user_settings(user_id)
        return settings["preferences"]["auto_direct"]
    
    def get_preferred_hospitals(self, user_id):
        """Get list of preferred hospitals"""
        settings = self.get_user_settings(user_id)
        return [h for h in settings["preferred_hospitals"] if h["enabled"]]
    
    def get_max_waiting_time(self, user_id):
        """Get max acceptable waiting time"""
        settings = self.get_user_settings(user_id)
        return settings["preferences"]["max_waiting_time"]
    
    def get_assigned_doctor(self, user_id):
        """Get assigned doctor info"""
        settings = self.get_user_settings(user_id)
        return settings["medical_info"]["assigned_doctor"]

# Global instance
settings_service = SettingsService()

