"""
Populate Service Schedules
Add sample service configurations and schedules to existing hospitals
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import time, date, datetime, timedelta
from src.main import app
from src.models.user import db
from src.models.hospital import Hospital
from src.services.schedule_manager import ScheduleManager

def populate_services():
    """Add services and schedules to existing hospitals"""
    
    with app.app_context():
        print("🏥 Populating Service Schedules for Jazan Health Cluster...")
        print("")
        
        # Get all hospitals in Jazan
        hospitals = Hospital.query.filter(Hospital.city.like('%جازان%')).all()
        
        if not hospitals:
            print("❌ No hospitals found in Jazan. Please run populate_hospitals.py first.")
            return
        
        print(f"Found {len(hospitals)} hospitals in Jazan")
        print("")
        
        services_added = 0
        schedules_added = 0
        
        for hospital in hospitals:
            print(f"Adding services to: {hospital.name_ar}")
            
            # Determine services based on hospital type
            if hospital.facility_type == "urgent_care_center":
                # Urgent care centers - basic services
                services_config = [
                    {
                        'service_type': 'emergency',
                        'service_name_ar': 'الطوارئ',
                        'service_name_en': 'Emergency',
                        'description_ar': 'خدمات الطوارئ والحالات العاجلة',
                        'description_en': 'Emergency and urgent care services',
                        'capacity': 20,
                        'average_wait_time': 15,
                        'hours': '24/7' if hospital.is_24_7 else 'limited'
                    },
                    {
                        'service_type': 'laboratory',
                        'service_name_ar': 'المختبر',
                        'service_name_en': 'Laboratory',
                        'description_ar': 'خدمات الفحوصات المخبرية',
                        'description_en': 'Laboratory testing services',
                        'capacity': 50,
                        'average_wait_time': 10,
                        'hours': '24/7' if hospital.is_24_7 else 'limited'
                    },
                    {
                        'service_type': 'radiology',
                        'service_name_ar': 'الأشعة',
                        'service_name_en': 'Radiology',
                        'description_ar': 'خدمات الأشعة التشخيصية',
                        'description_en': 'Diagnostic imaging services',
                        'capacity': 30,
                        'average_wait_time': 20,
                        'hours': '24/7' if hospital.is_24_7 else 'limited'
                    },
                    {
                        'service_type': 'pharmacy',
                        'service_name_ar': 'الصيدلية',
                        'service_name_en': 'Pharmacy',
                        'description_ar': 'صرف الأدوية',
                        'description_en': 'Medication dispensing',
                        'capacity': 100,
                        'average_wait_time': 5,
                        'hours': '24/7' if hospital.is_24_7 else 'limited'
                    }
                ]
            else:
                # General hospitals - comprehensive services
                services_config = [
                    {
                        'service_type': 'emergency',
                        'service_name_ar': 'الطوارئ',
                        'service_name_en': 'Emergency',
                        'description_ar': 'خدمات الطوارئ والحالات الحرجة',
                        'description_en': 'Emergency and critical care services',
                        'capacity': 50,
                        'average_wait_time': 20,
                        'hours': '24/7'
                    },
                    {
                        'service_type': 'cardiology',
                        'service_name_ar': 'أمراض القلب',
                        'service_name_en': 'Cardiology',
                        'description_ar': 'تشخيص وعلاج أمراض القلب',
                        'description_en': 'Heart disease diagnosis and treatment',
                        'capacity': 20,
                        'average_wait_time': 30,
                        'requires_appointment': True,
                        'hours': 'business'
                    },
                    {
                        'service_type': 'pediatrics',
                        'service_name_ar': 'طب الأطفال',
                        'service_name_en': 'Pediatrics',
                        'description_ar': 'رعاية صحة الأطفال',
                        'description_en': 'Children healthcare',
                        'capacity': 30,
                        'average_wait_time': 25,
                        'hours': '24/7'
                    },
                    {
                        'service_type': 'surgery',
                        'service_name_ar': 'الجراحة',
                        'service_name_en': 'Surgery',
                        'description_ar': 'العمليات الجراحية',
                        'description_en': 'Surgical operations',
                        'capacity': 10,
                        'average_wait_time': 60,
                        'requires_appointment': True,
                        'has_on_call_coverage': True,
                        'hours': 'on_call'
                    },
                    {
                        'service_type': 'laboratory',
                        'service_name_ar': 'المختبر',
                        'service_name_en': 'Laboratory',
                        'description_ar': 'الفحوصات المخبرية الشاملة',
                        'description_en': 'Comprehensive laboratory testing',
                        'capacity': 100,
                        'average_wait_time': 15,
                        'hours': '24/7'
                    },
                    {
                        'service_type': 'radiology',
                        'service_name_ar': 'الأشعة',
                        'service_name_en': 'Radiology',
                        'description_ar': 'الأشعة التشخيصية المتقدمة',
                        'description_en': 'Advanced diagnostic imaging',
                        'capacity': 40,
                        'average_wait_time': 25,
                        'hours': '24/7'
                    },
                    {
                        'service_type': 'pharmacy',
                        'service_name_ar': 'الصيدلية',
                        'service_name_en': 'Pharmacy',
                        'description_ar': 'صرف الأدوية والمستلزمات الطبية',
                        'description_en': 'Medication and medical supplies',
                        'capacity': 200,
                        'average_wait_time': 10,
                        'hours': '24/7'
                    }
                ]
            
            # Add services
            for service_config in services_config:
                try:
                    # Create service
                    service_data = {
                        'service_type': service_config['service_type'],
                        'service_name_ar': service_config['service_name_ar'],
                        'service_name_en': service_config['service_name_en'],
                        'description_ar': service_config['description_ar'],
                        'description_en': service_config['description_en'],
                        'capacity': service_config['capacity'],
                        'average_wait_time': service_config['average_wait_time'],
                        'requires_appointment': service_config.get('requires_appointment', False),
                        'has_on_call_coverage': service_config.get('has_on_call_coverage', False),
                        'phone': hospital.phone
                    }
                    
                    service = ScheduleManager.create_service(
                        hospital_id=hospital.id,
                        service_data=service_data,
                        created_by='system'
                    )
                    services_added += 1
                    
                    # Create schedule based on hours
                    hours_type = service_config['hours']
                    
                    if hours_type == '24/7':
                        # 24/7 schedule
                        schedule = ScheduleManager.create_24_7_schedule(
                            service_id=service.id,
                            created_by='system'
                        )
                        schedules_added += 1
                    
                    elif hours_type == 'business':
                        # Business hours (Sunday-Thursday 8am-4pm)
                        weekly_hours = {
                            6: (time(8, 0), time(16, 0)),  # Sunday
                            0: (time(8, 0), time(16, 0)),  # Monday
                            1: (time(8, 0), time(16, 0)),  # Tuesday
                            2: (time(8, 0), time(16, 0)),  # Wednesday
                            3: (time(8, 0), time(16, 0)),  # Thursday
                        }
                        schedules = ScheduleManager.create_weekly_schedule(
                            service_id=service.id,
                            weekly_hours=weekly_hours,
                            created_by='system'
                        )
                        schedules_added += len(schedules)
                    
                    elif hours_type == 'on_call':
                        # On-call 24/7
                        schedule_data = {
                            'schedule_type': 'on_call',
                            'day_of_week': None,
                            'start_time': time(0, 0),
                            'end_time': time(23, 59),
                            'availability_status': 'on_call_only',
                            'on_call_doctor': 'طبيب مناوب',
                            'on_call_phone': hospital.phone,
                            'response_time_minutes': 30
                        }
                        schedule = ScheduleManager.create_schedule(
                            service_id=service.id,
                            schedule_data=schedule_data,
                            created_by='system'
                        )
                        schedules_added += 1
                    
                    elif hours_type == 'limited':
                        # Limited hours (8am-11pm daily)
                        schedule_data = {
                            'schedule_type': 'regular',
                            'day_of_week': None,
                            'start_time': time(8, 0),
                            'end_time': time(23, 0),
                            'availability_status': 'available'
                        }
                        schedule = ScheduleManager.create_schedule(
                            service_id=service.id,
                            schedule_data=schedule_data,
                            created_by='system'
                        )
                        schedules_added += 1
                    
                    print(f"  ✓ Added {service_config['service_name_en']} ({hours_type})")
                    
                except Exception as e:
                    print(f"  ✗ Error adding {service_config['service_name_en']}: {e}")
            
            print("")
        
        print("=" * 60)
        print(f"✅ Successfully added:")
        print(f"   - {services_added} services")
        print(f"   - {schedules_added} schedules")
        print(f"   - Across {len(hospitals)} hospitals")
        print("=" * 60)

if __name__ == '__main__':
    populate_services()
