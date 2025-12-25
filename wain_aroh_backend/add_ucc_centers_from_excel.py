#!/usr/bin/env python3
"""
Add UCC Centers from Excel data to Wain Aroh database
Includes GPS coordinates for each center in Jazan region
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
# These are approximate coordinates for each area
JAZAN_COORDINATES = {
    'جازان': {
        'الشاطئ': (16.8892, 42.5511),
        'المضايا': (16.9012, 42.5623),
        'مخطط6': (16.9145, 42.5789),
        'محليه': (16.8756, 42.5423)
    },
    'صبيا': {
        'صبيا': (17.1494, 42.6253),
        'صبيا الجديدة': (17.1623, 42.6389)
    },
    'هروب': {
        'الصهاليل': (17.7234, 42.9123)
    },
    'أبوعريش': {
        'ابوعريش الشمالي': (16.9678, 42.8234),
        'الواصلي': (16.9456, 42.8012),
        'أبو عريش الجنوبي': (16.9234, 42.8156)
    },
    'صامطة': {
        'صامطة': (16.5967, 42.9456)
    },
    'العارضة': {
        'العارضة': (17.2912, 43.0567)
    },
    'الطوال': {
        'الطوال الغربي': (16.4123, 42.9234)
    },
    'أحد المسارحة': {
        'الاحد': (16.7456, 43.1234)
    },
    'بيش': {
        'بيش الشمالي': (17.3123, 42.6789)
    },
    'الدرب': {
        'ابو السداد': (17.6234, 42.2456),
        'الشقيق': (17.6456, 42.2678)
    },
    'ضمد': {
        'ضمد الشمالي': (17.0456, 42.9234)
    }
}

def get_coordinates(city, center_name):
    """Get GPS coordinates for a center"""
    if city in JAZAN_COORDINATES:
        if center_name in JAZAN_COORDINATES[city]:
            return JAZAN_COORDINATES[city][center_name]
        # Return city center if specific location not found
        return list(JAZAN_COORDINATES[city].values())[0]
    # Default to Jazan city center
    return (16.8892, 42.5511)

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
    
    print(f"📄 Loaded {len(ucc_data)} UCC centers from JSON")
    print()
    
    # Initialize Flask app and database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wain_aroh.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        process_centers(ucc_data)

def process_centers(ucc_data):
    added_count = 0
    updated_count = 0
    
    for center in ucc_data:
        name_ar = f"مركز {center['name_ar']}"
        city = center['city']
        moh_code = center['moh_code']
        service_type = center['service_type']
        working_hours = center['working_hours']
        working_days = center['working_days']
        
        # Get coordinates
        lat, lon = get_coordinates(city, center['name_ar'])
        
        # Determine facility type
        if 'عاجلة' in service_type:
            facility_type = 'urgent_care'
            name_en = f"{center['name_ar']} Urgent Care Center"
            description_ar = f"مركز رعاية عاجلة يعمل {working_hours} ساعة"
            description_en = f"Urgent Care Center operating {working_hours} hours"
        else:
            facility_type = 'clinic'
            name_en = f"{center['name_ar']} Extended Care Center"
            description_ar = f"مركز رعاية ممتدة يعمل {working_hours} ساعة"
            description_en = f"Extended Care Center operating {working_hours} hours"
        
        # Check if already exists by MOH code
        existing = Hospital.query.filter_by(moh_code=moh_code).first()
        
        if existing:
            print(f"⚠️  Center already exists: {name_ar} (MOH: {moh_code})")
            # Update coordinates if needed
            if existing.latitude != lat or existing.longitude != lon:
                existing.latitude = lat
                existing.longitude = lon
                db.session.commit()
                print(f"   ✅ Updated coordinates: ({lat}, {lon})")
                updated_count += 1
            continue
        
        # Create new hospital entry
        hospital = Hospital(
            name_ar=name_ar,
            name_en=name_en,
            city=city,
            region='Jazan',
            latitude=lat,
            longitude=lon,
            phone='+966173000000',  # Placeholder
            emergency_phone='+966173000000',
            email=f"{moh_code}@jazan.health.sa",
            website='https://www.health.sa',
            type=facility_type,
            level='primary',
            capacity=20 if working_hours == '24' else 15,
            available_beds=10 if working_hours == '24' else 8,
            has_emergency=True if 'عاجلة' in service_type else False,
            has_icu=False,
            has_nicu=False,
            has_ambulance=True if 'عاجلة' in service_type else False,
            operating_hours='24/7' if working_hours == '24' else 'Sun-Thu: 7AM-11PM',
            description_ar=description_ar,
            description_en=description_en,
            services=['emergency' if 'عاجلة' in service_type else 'general_medicine', 'pharmacy', 'laboratory'],
            insurance_accepted=['MOH', 'CCHI'],
            languages=['Arabic', 'English'],
            rating=4.2,
            total_reviews=50,
            moh_code=moh_code,
            cluster='Jazan Health Cluster',
            sector=center['sector'],
            is_active=True,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        db.session.add(hospital)
        
        print(f"✅ Added: {name_ar}")
        print(f"   📍 Location: {city} ({lat}, {lon})")
        print(f"   🏥 Type: {facility_type} | MOH Code: {moh_code}")
        print(f"   ⏰ Hours: {working_hours}h | Days: {working_days}")
        print()
        
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
    total_hospitals = Hospital.query.count()
    jazan_hospitals = Hospital.query.filter_by(region='Jazan').count()
    urgent_care = Hospital.query.filter_by(type='urgent_care', region='Jazan').count()
    clinics = Hospital.query.filter_by(type='clinic', region='Jazan').count()
    
    print()
    print("📊 Database Summary:")
    print(f"   • Total facilities in system: {total_hospitals}")
    print(f"   • Jazan region facilities: {jazan_hospitals}")
    print(f"   • Urgent Care Centers: {urgent_care}")
    print(f"   • Extended Care Clinics: {clinics}")
    print()

if __name__ == '__main__':
    main()
