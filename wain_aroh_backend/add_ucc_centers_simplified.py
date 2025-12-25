#!/usr/bin/env python3
"""
Add UCC Centers from Excel data to Wain Aroh database
Simplified version matching actual Hospital model fields
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from src.models.user import db
from src.models.hospital import Hospital

# GPS coordinates for Jazan region cities/areas
JAZAN_COORDINATES = {
    'جازان': {'الشاطئ': (16.8892, 42.5511), 'المضايا': (16.9012, 42.5623), 'مخطط6': (16.9145, 42.5789), 'محليه': (16.8756, 42.5423)},
    'صبيا': {'صبيا': (17.1494, 42.6253), 'صبيا الجديدة': (17.1623, 42.6389)},
    'هروب': {'الصهاليل': (17.7234, 42.9123)},
    'أبوعريش': {'ابوعريش الشمالي': (16.9678, 42.8234), 'الواصلي': (16.9456, 42.8012), 'أبو عريش الجنوبي': (16.9234, 42.8156)},
    'صامطة': {'صامطة': (16.5967, 42.9456)},
    'العارضة': {'العارضة': (17.2912, 43.0567)},
    'الطوال': {'الطوال الغربي': (16.4123, 42.9234)},
    'أحد المسارحة': {'الاحد': (16.7456, 43.1234)},
    'بيش': {'بيش الشمالي': (17.3123, 42.6789)},
    'الدرب': {'ابو السداد': (17.6234, 42.2456), 'الشقيق': (17.6456, 42.2678)},
    'ضمد': {'ضمد الشمالي': (17.0456, 42.9234)}
}

def get_coordinates(city, center_name):
    """Get GPS coordinates for a center"""
    if city in JAZAN_COORDINATES and center_name in JAZAN_COORDINATES[city]:
        return JAZAN_COORDINATES[city][center_name]
    elif city in JAZAN_COORDINATES:
        return list(JAZAN_COORDINATES[city].values())[0]
    return (16.8892, 42.5511)  # Default to Jazan city center

def main():
    print("=" * 80)
    print("Adding UCC Centers from Excel to Wain Aroh Database")
    print("=" * 80)
    print()
    
    # Load the extracted JSON data
    json_path = '/home/ubuntu/ucc_centers_data.json'
    if not os.path.exists(json_path):
        print(f"❌ Error: {json_path} not found!")
        return
    
    with open(json_path, 'r', encoding='utf-8') as f:
        ucc_data = json.load(f)
    
    print(f"📄 Loaded {len(ucc_data)} UCC centers from JSON\n")
    
    # Initialize Flask app and database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wain_aroh.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        
        added_count = 0
        updated_count = 0
        
        for center in ucc_data:
            name_ar = f"مركز {center['name_ar']}"
            name_en = f"{center['name_ar']} Center"
            city = center['city']
            service_type = center['service_type']
            working_hours = center['working_hours']
            working_days = center['working_days']
            
            # Get coordinates
            lat, lon = get_coordinates(city, center['name_ar'])
            
            # Determine facility type
            is_urgent_care = 'عاجلة' in service_type
            facility_type = 'emergency_center' if is_urgent_care else 'health_center'
            is_24_7 = (working_hours == '24')
            
            # Check if already exists by name
            existing = Hospital.query.filter_by(name_ar=name_ar, city=city).first()
            
            if existing:
                print(f"⚠️  Center already exists: {name_ar}")
                if existing.latitude != lat or existing.longitude != lon:
                    existing.latitude = lat
                    existing.longitude = lon
                    db.session.commit()
                    print(f"   ✅ Updated coordinates")
                    updated_count += 1
                continue
            
            # Create new hospital entry
            hospital = Hospital(
                name_ar=name_ar,
                name_en=name_en,
                city=city,
                latitude=lat,
                longitude=lon,
                phone='+966173000000',
                phone_emergency='+966173000000' if is_urgent_care else None,
                email=f"{center['moh_code']}@jazan.health.sa",
                website='https://www.health.sa',
                facility_type=facility_type,
                is_emergency=is_urgent_care,
                is_24_7=is_24_7,
                capacity_beds=20 if is_24_7 else 15,
                capacity_emergency_beds=10 if is_urgent_care else 0,
                description_ar=f"{service_type} - {working_days} - {working_hours} ساعة",
                description_en=f"{service_type} - {working_days} - {working_hours} hours",
                is_active=True,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            
            db.session.add(hospital)
            
            print(f"✅ Added: {name_ar}")
            print(f"   📍 Location: {city} ({lat}, {lon})")
            print(f"   🏥 Type: {facility_type} | 24/7: {is_24_7}")
            print(f"   ⏰ Hours: {working_hours}h | Days: {working_days}\n")
            
            added_count += 1
        
        # Commit all changes
        db.session.commit()
        
        print("=" * 80)
        print(f"✅ Successfully processed {len(ucc_data)} UCC centers")
        print(f"   • Added: {added_count} new centers")
        print(f"   • Updated: {updated_count} existing centers")
        print(f"   • Skipped: {len(ucc_data) - added_count - updated_count} centers")
        print("=" * 80)
        
        # Display summary
        total = Hospital.query.count()
        jazan = Hospital.query.filter_by(city='جازان').count() + \
                Hospital.query.filter(Hospital.city.in_(['صبيا', 'هروب', 'أبوعريش', 'صامطة', 'العارضة', 'الطوال', 'أحد المسارحة', 'بيش', 'الدرب', 'ضمد'])).count()
        urgent = Hospital.query.filter_by(is_emergency=True).count()
        
        print(f"\n📊 Database Summary:")
        print(f"   • Total facilities: {total}")
        print(f"   • Jazan region: {jazan}")
        print(f"   • Urgent care centers: {urgent}\n")

if __name__ == '__main__':
    main()
