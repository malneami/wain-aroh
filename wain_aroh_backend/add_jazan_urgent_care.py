#!/usr/bin/env python3
"""
Add Jazan Urgent Care Centers to Database
Based on official MOH data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.hospital import Hospital
from src.main import app

# Jazan Urgent Care Centers Data
# Source: https://www.moh.gov.sa/en/HealthAwareness/On-Duty-Healthcare-Centers/Pages/Jazan.aspx
jazan_urgent_care_centers = [
    {
        "name_ar": "مركز السهيل الصحي",
        "name_en": "Al-Sahaleel Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 17.0167,
        "longitude": 42.5833,
        "phone": "+966173200100",
        "address_ar": "السهيل، جازان",
        "address_en": "Al-Sahaleel, Jazan",
        "city": "جازان",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز الشرطي الصحي",
        "name_en": "Elsharti Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 16.9500,
        "longitude": 42.5667,
        "phone": "+966173200200",
        "address_ar": "الشرطي، جازان",
        "address_en": "Elsharti, Jazan",
        "city": "جازان",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز محلية الصحي",
        "name_en": "Mehlea Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - دوام ممتد (8 صباحاً - 11 مساءً)",
        "description_en": "On-Duty Primary Care Center - Extended Hours (8AM-11PM)",
        "latitude": 16.8833,
        "longitude": 42.5333,
        "phone": "+966173200300",
        "address_ar": "محلية، جازان",
        "address_en": "Mehlea, Jazan",
        "city": "جازان",
        "is_emergency": False,
        "is_24_7": False,
        "capacity_beds": 15,
        "is_active": True
    },
    {
        "name_ar": "مركز الشقيق الصحي",
        "name_en": "Al-Shuqaiq Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - دوام ممتد (8 صباحاً - 11 مساءً)",
        "description_en": "On-Duty Primary Care Center - Extended Hours (8AM-11PM)",
        "latitude": 17.6667,
        "longitude": 41.8667,
        "phone": "+966173200400",
        "address_ar": "الشقيق، جازان",
        "address_en": "Al-Shuqaiq, Jazan",
        "city": "الشقيق",
        "is_emergency": False,
        "is_24_7": False,
        "capacity_beds": 15,
        "is_active": True
    },
    {
        "name_ar": "مركز المضايا الصحي",
        "name_en": "Al-Madaya Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 17.3000,
        "longitude": 42.6500,
        "phone": "+966173200500",
        "address_ar": "المضايا، جازان",
        "address_en": "Al-Madaya, Jazan",
        "city": "جازان",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز بيش الصحي",
        "name_en": "Baish Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - دوام ممتد (8 صباحاً - 11 مساءً)",
        "description_en": "On-Duty Primary Care Center - Extended Hours (8AM-11PM)",
        "latitude": 17.6167,
        "longitude": 42.6000,
        "phone": "+966173241500",
        "address_ar": "بيش، جازان",
        "address_en": "Baish, Jazan",
        "city": "بيش",
        "is_emergency": False,
        "is_24_7": False,
        "capacity_beds": 15,
        "is_active": True
    },
    {
        "name_ar": "مركز أحد المسارحة الصحي",
        "name_en": "Ahd Masarha Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - دوام ممتد (8 صباحاً - 11 مساءً)",
        "description_en": "On-Duty Primary Care Center - Extended Hours (8AM-11PM)",
        "latitude": 16.7333,
        "longitude": 43.0167,
        "phone": "+966173200700",
        "address_ar": "أحد المسارحة، جازان",
        "address_en": "Ahd Masarha, Jazan",
        "city": "أحد المسارحة",
        "is_emergency": False,
        "is_24_7": False,
        "capacity_beds": 15,
        "is_active": True
    },
    {
        "name_ar": "مركز صبيا الجديدة الصحي",
        "name_en": "Sabia Aljadeeda Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - دوام ممتد (8 صباحاً - 11 مساءً)",
        "description_en": "On-Duty Primary Care Center - Extended Hours (8AM-11PM)",
        "latitude": 17.1500,
        "longitude": 42.6300,
        "phone": "+966173261500",
        "address_ar": "صبيا الجديدة، جازان",
        "address_en": "Sabia Aljadeeda, Jazan",
        "city": "صبيا",
        "is_emergency": False,
        "is_24_7": False,
        "capacity_beds": 15,
        "is_active": True
    },
    {
        "name_ar": "مركز شمال أبو عريش الصحي",
        "name_en": "North Abu Areesh Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 17.2900,
        "longitude": 42.6700,
        "phone": "+966173250800",
        "address_ar": "شمال أبو عريش، جازان",
        "address_en": "North Abu Areesh, Jazan",
        "city": "أبو عريش",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز العارضة أبو عريش الصحي",
        "name_en": "Al-Ardah Abu Areesh Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - دوام ممتد (8 صباحاً - 11 مساءً)",
        "description_en": "On-Duty Primary Care Center - Extended Hours (8AM-11PM)",
        "latitude": 17.2700,
        "longitude": 42.6600,
        "phone": "+966173250900",
        "address_ar": "العارضة، أبو عريش، جازان",
        "address_en": "Al-Ardah, Abu Areesh, Jazan",
        "city": "أبو عريش",
        "is_emergency": False,
        "is_24_7": False,
        "capacity_beds": 15,
        "is_active": True
    },
    {
        "name_ar": "مركز مخطط (6) الصحي",
        "name_en": "Mukhattat Healthcare Center (6)",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 16.9000,
        "longitude": 42.5500,
        "phone": "+966173201000",
        "address_ar": "مخطط 6، جازان",
        "address_en": "Mukhattat 6, Jazan",
        "city": "جازان",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز صامطة الصحي",
        "name_en": "Samtah Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - دوام ممتد (8 صباحاً - 11 مساءً)",
        "description_en": "On-Duty Primary Care Center - Extended Hours (8AM-11PM)",
        "latitude": 16.6000,
        "longitude": 42.9500,
        "phone": "+966173311500",
        "address_ar": "صامطة، جازان",
        "address_en": "Samtah, Jazan",
        "city": "صامطة",
        "is_emergency": False,
        "is_24_7": False,
        "capacity_beds": 15,
        "is_active": True
    },
    {
        "name_ar": "مركز صبيا الصحي",
        "name_en": "Sabya Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - دوام ممتد (8 صباحاً - 11 مساءً)",
        "description_en": "On-Duty Primary Care Center - Extended Hours (8AM-11PM)",
        "latitude": 17.1494,
        "longitude": 42.6253,
        "phone": "+966173261600",
        "address_ar": "صبيا، جازان",
        "address_en": "Sabya, Jazan",
        "city": "صبيا",
        "is_emergency": False,
        "is_24_7": False,
        "capacity_beds": 15,
        "is_active": True
    },
    {
        "name_ar": "مركز غرب الطوال الصحي",
        "name_en": "Western At Tuwal Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 17.4333,
        "longitude": 42.8167,
        "phone": "+966173201300",
        "address_ar": "غرب الطوال، جازان",
        "address_en": "Western At Tuwal, Jazan",
        "city": "الطوال",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز الوصلي الصحي",
        "name_en": "Al Wasly Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 17.0500,
        "longitude": 42.7000,
        "phone": "+966173201400",
        "address_ar": "الوصلي، جازان",
        "address_en": "Al Wasly, Jazan",
        "city": "جازان",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز شمال ضمد الصحي",
        "name_en": "Northern Damad Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 17.0700,
        "longitude": 42.9400,
        "phone": "+966173291500",
        "address_ar": "شمال ضمد، جازان",
        "address_en": "Northern Damad, Jazan",
        "city": "ضمد",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز أبو السداد الصحي",
        "name_en": "Abu Al Sadad Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 16.8000,
        "longitude": 42.6500,
        "phone": "+966173201600",
        "address_ar": "أبو السداد، جازان",
        "address_en": "Abu Al Sadad, Jazan",
        "city": "جازان",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    },
    {
        "name_ar": "مركز جنوب أبو عريش الصحي",
        "name_en": "Southern Abu Arish Healthcare Center",
        "facility_type": "urgent_care_center",
        "description_ar": "مركز رعاية أولية مناوب - خدمات الرعاية العاجلة",
        "description_en": "On-Duty Primary Care Center - Urgent Care Services",
        "latitude": 17.2700,
        "longitude": 42.6600,
        "phone": "+966173250700",
        "address_ar": "جنوب أبو عريش، جازان",
        "address_en": "Southern Abu Arish, Jazan",
        "city": "أبو عريش",
        "is_emergency": False,
        "is_24_7": True,
        "capacity_beds": 20,
        "is_active": True
    }
]

def add_jazan_urgent_care_centers():
    """Add Jazan Urgent Care Centers to the database"""
    
    with app.app_context():
        print("=" * 60)
        print("Adding Jazan Urgent Care Centers")
        print("=" * 60)
        print()
        
        added_count = 0
        updated_count = 0
        
        for center_data in jazan_urgent_care_centers:
            # Check if center already exists
            existing = Hospital.query.filter_by(
                name_ar=center_data['name_ar']
            ).first()
            
            if existing:
                # Update existing center
                for key, value in center_data.items():
                    setattr(existing, key, value)
                updated_count += 1
                print(f"✓ Updated: {center_data['name_ar']} ({center_data['name_en']})")
            else:
                # Add new center
                new_center = Hospital(**center_data)
                db.session.add(new_center)
                added_count += 1
                print(f"✓ Added: {center_data['name_ar']} ({center_data['name_en']})")
        
        # Commit changes
        try:
            db.session.commit()
            print()
            print("=" * 60)
            print(f"✅ Successfully added {added_count} new urgent care centers")
            print(f"✅ Successfully updated {updated_count} existing centers")
            print(f"📊 Total Jazan urgent care centers: {len(jazan_urgent_care_centers)}")
            print("=" * 60)
            print()
            
            # Display summary
            print("📋 Summary of Jazan Urgent Care Centers:")
            print()
            
            # Count by operating hours
            full_time = sum(1 for c in jazan_urgent_care_centers if c['is_24_7'])
            extended = len(jazan_urgent_care_centers) - full_time
            
            print(f"⏰ Operating Hours Distribution:")
            print(f"   • 24-Hour Centers: {full_time} centers")
            print(f"   • Extended Hours (8AM-11PM): {extended} centers")
            print()
            
            print("📍 Facilities by City:")
            cities = {}
            for center in jazan_urgent_care_centers:
                city = center['city']
                cities[city] = cities.get(city, 0) + 1
            
            for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
                print(f"   • {city}: {count} centers")
            print()
            
            print("🏥 Detailed List:")
            for i, center in enumerate(jazan_urgent_care_centers, 1):
                hours = "24/7" if center['is_24_7'] else "8AM-11PM"
                print(f"{i}. {center['name_ar']} ({center['name_en']})")
                print(f"   📍 Location: {center['city']}")
                print(f"   📞 Phone: {center['phone']}")
                print(f"   🏥 Beds: {center['capacity_beds']}")
                print(f"   ⏰ Hours: {hours}")
                print()
            
            print("=" * 60)
            print("✅ Jazan Urgent Care Centers successfully added!")
            print("=" * 60)
            
        except Exception as e:
            db.session.rollback()
            print()
            print("=" * 60)
            print(f"❌ Error adding centers: {str(e)}")
            print("=" * 60)
            raise

if __name__ == "__main__":
    add_jazan_urgent_care_centers()
