#!/usr/bin/env python3
"""
Configure services and schedules for UCC Centers
Based on the service schedule management module
"""

import sys
import os
import json
from datetime import datetime, time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from src.models.user import db
from src.models.hospital import Hospital
from src.models.service_schedule import ServiceConfiguration, ServiceSchedule

def main():
    print("=" * 80)
    print("Configuring Services and Schedules for UCC Centers")
    print("=" * 80)
    print()
    
    # Initialize Flask app and database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wain_aroh.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        # Load UCC data to determine service types
        json_path = '/home/ubuntu/ucc_centers_data.json'
        with open(json_path, 'r', encoding='utf-8') as f:
            ucc_data = json.load(f)
        
        # Create a mapping of center names to their details
        ucc_map = {f"مركز {c['name_ar']}": c for c in ucc_data}
        
        # Get all UCC centers from database
        ucc_centers = Hospital.query.filter(
            Hospital.facility_type.in_(['emergency_center', 'health_center'])
        ).all()
        
        print(f"📋 Found {len(ucc_centers)} UCC centers in database\n")
        
        services_added = 0
        schedules_added = 0
        
        for hospital in ucc_centers:
            print(f"🏥 Configuring: {hospital.name_ar}")
            
            # Get UCC details
            ucc_details = ucc_map.get(hospital.name_ar, {})
            is_urgent_care = 'عاجلة' in ucc_details.get('service_type', '')
            working_hours = ucc_details.get('working_hours', '24')
            working_days = ucc_details.get('working_days', 'جميع ايام الاسبوع')
            
            # Define services based on type
            if is_urgent_care:
                service_types = [
                    ('emergency', 'خدمات الطوارئ', 'Emergency Services', 'critical'),
                    ('urgent_care', 'الرعاية العاجلة', 'Urgent Care', 'high'),
                    ('general_medicine', 'الطب العام', 'General Medicine', 'medium'),
                    ('pediatrics', 'طب الأطفال', 'Pediatrics', 'medium'),
                    ('laboratory', 'المختبر', 'Laboratory', 'medium'),
                    ('radiology', 'الأشعة', 'Radiology', 'medium'),
                    ('pharmacy', 'الصيدلية', 'Pharmacy', 'medium')
                ]
            else:
                service_types = [
                    ('general_medicine', 'الطب العام', 'General Medicine', 'medium'),
                    ('pediatrics', 'طب الأطفال', 'Pediatrics', 'medium'),
                    ('laboratory', 'المختبر', 'Laboratory', 'low'),
                    ('pharmacy', 'الصيدلية', 'Pharmacy', 'low')
                ]
            
            # Add services
            for service_type, name_ar, name_en, priority in service_types:
                # Check if service already exists
                existing = ServiceConfiguration.query.filter_by(
                    hospital_id=hospital.id,
                    service_type=service_type
                ).first()
                
                if existing:
                    print(f"   ⚠️  Service already exists: {name_ar}")
                    continue
                
                # Create service configuration
                service = ServiceConfiguration(
                    hospital_id=hospital.id,
                    service_type=service_type,
                    service_name_ar=name_ar,
                    service_name_en=name_en,
                    is_active=True,
                    priority=priority,
                    requires_appointment=False if is_urgent_care else True,
                    average_wait_time=15 if is_urgent_care else 30,
                    capacity_per_hour=12 if is_urgent_care else 8,
                    created_at=datetime.now()
                )
                
                db.session.add(service)
                db.session.flush()  # Get the service ID
                
                # Create schedule
                if working_hours == '24':
                    # 24/7 schedule
                    schedule = ServiceSchedule(
                        service_id=service.id,
                        schedule_type='24_7',
                        is_active=True,
                        created_at=datetime.now()
                    )
                elif 'جميع ايام الاسبوع' in working_days:
                    # Weekly schedule (all days, 16 hours)
                    schedule = ServiceSchedule(
                        service_id=service.id,
                        schedule_type='weekly',
                        days_of_week=[0, 1, 2, 3, 4, 5, 6],  # All days
                        start_time=time(7, 0),  # 7 AM
                        end_time=time(23, 0),   # 11 PM
                        is_active=True,
                        created_at=datetime.now()
                    )
                else:
                    # Sunday to Thursday (16 hours)
                    schedule = ServiceSchedule(
                        service_id=service.id,
                        schedule_type='weekly',
                        days_of_week=[6, 0, 1, 2, 3],  # Sun-Thu (0=Monday in Python)
                        start_time=time(7, 0),
                        end_time=time(23, 0),
                        is_active=True,
                        created_at=datetime.now()
                    )
                
                db.session.add(schedule)
                services_added += 1
                schedules_added += 1
                
                print(f"   ✅ Added: {name_ar} ({service_type})")
            
            print()
        
        # Commit all changes
        db.session.commit()
        
        print("=" * 80)
        print(f"✅ Configuration Complete!")
        print(f"   • Services added: {services_added}")
        print(f"   • Schedules created: {schedules_added}")
        print("=" * 80)
        
        # Summary
        total_services = ServiceConfiguration.query.count()
        total_schedules = ServiceSchedule.query.count()
        active_24_7 = ServiceSchedule.query.filter_by(schedule_type='24_7', is_active=True).count()
        
        print(f"\n📊 System Summary:")
        print(f"   • Total service configurations: {total_services}")
        print(f"   • Total schedules: {total_schedules}")
        print(f"   • 24/7 services: {active_24_7}")
        print(f"   • UCC centers configured: {len(ucc_centers)}\n")

if __name__ == '__main__':
    main()
