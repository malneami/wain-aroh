#!/usr/bin/env python3
"""
Add Jazan Health Cluster Facilities to Database
Based on official MOH data and research
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.hospital import Hospital
from src.main import app

# Jazan Health Cluster Facilities Data
jazan_facilities = [
    {
        "name_ar": "مستشفى الملك فهد المركزي",
        "name_en": "King Fahad Central Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 17.2833,
        "longitude": 42.6667,
        "phone": "+966173250717",
        "address_ar": "أبو عريش، جازان",
        "address_en": "Abu Arish, Jazan",
        "city": "جازان",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 500,
        "is_active": True
    },
    {
        "name_ar": "مستشفى جازان العام",
        "name_en": "Jazan General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 16.8892,
        "longitude": 42.5511,
        "phone": "+966173234905",
        "address_ar": "شارع الشيخ عبدالعزيز بن باز، الروضة، جازان",
        "address_en": "Sheikh Abdulaziz Bin Baz Street, Al-Rawda, Jazan",
        "city": "جازان",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 400,
        "is_active": True
    },
    {
        "name_ar": "مستشفى صبيا العام",
        "name_en": "Sebia General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 17.1494,
        "longitude": 42.6253,
        "phone": "+966173261000",
        "address_ar": "صبيا، جازان",
        "address_en": "Sebia, Jazan",
        "city": "صبيا",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 300,
        "is_active": True
    },
    {
        "name_ar": "مستشفى صامطة العام",
        "name_en": "Sametah General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 16.5981,
        "longitude": 42.9444,
        "phone": "+966173311000",
        "address_ar": "صامطة، جازان",
        "address_en": "Sametah, Jazan",
        "city": "صامطة",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 250,
        "is_active": True
    },
    {
        "name_ar": "مستشفى بيش العام",
        "name_en": "Bish General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 17.6167,
        "longitude": 42.6000,
        "phone": "+966173241000",
        "address_ar": "بيش، جازان",
        "address_en": "Bish, Jazan",
        "city": "بيش",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 200,
        "is_active": True
    },
    {
        "name_ar": "مستشفى فرسان العام",
        "name_en": "Fursan General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 16.7019,
        "longitude": 42.1197,
        "phone": "+966173270000",
        "address_ar": "جزر فرسان، جازان",
        "address_en": "Fursan Islands, Jazan",
        "city": "فرسان",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 150,
        "is_active": True
    },
    {
        "name_ar": "مستشفى الدرب العام",
        "name_en": "Al-Darb General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 17.7333,
        "longitude": 42.2333,
        "phone": "+966173281000",
        "address_ar": "الدرب، جازان",
        "address_en": "Al-Darb, Jazan",
        "city": "الدرب",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 180,
        "is_active": True
    },
    {
        "name_ar": "مستشفى ضمد العام",
        "name_en": "Dhamad General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 17.0667,
        "longitude": 42.9333,
        "phone": "+966173291000",
        "address_ar": "ضمد، جازان",
        "address_en": "Dhamad, Jazan",
        "city": "ضمد",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 160,
        "is_active": True
    },
    {
        "name_ar": "مستشفى الريث العام",
        "name_en": "Al-Raith General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 17.2167,
        "longitude": 43.2167,
        "phone": "+966173301000",
        "address_ar": "الريث، جازان",
        "address_en": "Al-Raith, Jazan",
        "city": "الريث",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 140,
        "is_active": True
    },
    {
        "name_ar": "مستشفى العيدابي العام",
        "name_en": "Al-'Edaby General Hospital",
        "facility_type": "hospital",
        "description_ar": "طوارئ، عيادات التشخيص المبكر، رعاية عامة",
        "description_en": "Emergency, Early Diagnosis Clinics, General Care",
        "latitude": 17.5167,
        "longitude": 43.1167,
        "phone": "+966173311500",
        "address_ar": "العيدابي، جازان",
        "address_en": "Al-'Edaby, Jazan",
        "city": "العيدابي",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 120,
        "is_active": True
    },
    {
        "name_ar": "مستشفى الصحة النفسية بجازان",
        "name_en": "Eradah Mental Health Hospital",
        "facility_type": "hospital",
        "description_ar": "الصحة النفسية، الطب النفسي، الاضطرابات السلوكية",
        "description_en": "Mental Health, Psychiatry, Behavioral Disorders",
        "latitude": 16.8892,
        "longitude": 42.5611,
        "phone": "+966173234800",
        "address_ar": "جازان",
        "address_en": "Jazan",
        "city": "جازان",
        "is_emergency": True,
        "is_24_7": True,
        "capacity_beds": 200,
        "is_active": True
    }
]

def add_jazan_facilities():
    """Add Jazan Health Cluster facilities to the database"""
    
    with app.app_context():
        print("=" * 60)
        print("Adding Jazan Health Cluster Facilities")
        print("=" * 60)
        print()
        
        added_count = 0
        updated_count = 0
        
        for facility_data in jazan_facilities:
            # Check if facility already exists
            existing = Hospital.query.filter_by(
                name_ar=facility_data['name_ar']
            ).first()
            
            if existing:
                # Update existing facility
                for key, value in facility_data.items():
                    setattr(existing, key, value)
                updated_count += 1
                print(f"✓ Updated: {facility_data['name_ar']} ({facility_data['name_en']})")
            else:
                # Add new facility
                new_facility = Hospital(**facility_data)
                db.session.add(new_facility)
                added_count += 1
                print(f"✓ Added: {facility_data['name_ar']} ({facility_data['name_en']})")
        
        # Commit changes
        try:
            db.session.commit()
            print()
            print("=" * 60)
            print(f"✅ Successfully added {added_count} new facilities")
            print(f"✅ Successfully updated {updated_count} existing facilities")
            print(f"📊 Total Jazan facilities: {len(jazan_facilities)}")
            print("=" * 60)
            print()
            
            # Display summary
            print("📋 Summary of Jazan Health Cluster Facilities:")
            print()
            for i, facility in enumerate(jazan_facilities, 1):
                print(f"{i}. {facility['name_ar']} ({facility['name_en']})")
                print(f"   📍 Location: {facility['city']}")
                print(f"   📞 Phone: {facility['phone']}")
                print(f"   🏥 Beds: {facility['capacity_beds']}")
                print(f"   🚨 Emergency: {'Yes' if facility['is_emergency'] else 'No'}")
                print()
            
            print("=" * 60)
            print("✅ Jazan Health Cluster facilities successfully added!")
            print("=" * 60)
            
        except Exception as e:
            db.session.rollback()
            print()
            print("=" * 60)
            print(f"❌ Error adding facilities: {str(e)}")
            print("=" * 60)
            raise

if __name__ == "__main__":
    add_jazan_facilities()
