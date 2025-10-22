"""
Script to populate database with sample hospitals in Riyadh
"""

import sys
import os
sys.path.insert(0, '/home/ubuntu/wain_aroh_backend')
os.chdir('/home/ubuntu/wain_aroh_backend')

from flask import Flask
from src.models.user import db
from src.models.hospital import Hospital, Organization, RiyadhCluster

# Create minimal Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wain_aroh.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Sample hospitals data with real locations in Riyadh
hospitals_data = [
    {
        'name_ar': 'مستشفى الملك فهد',
        'name_en': 'King Fahd Hospital',
        'facility_type': 'hospital',
        'is_emergency': True,
        'is_24_7': True,
        'phone': '0112345678',
        'phone_emergency': '0112345679',
        'email': 'info@kfh.sa',
        'website': 'www.kfh.sa',
        'address_ar': 'طريق الملك فهد، العليا',
        'address_en': 'King Fahd Road, Al Olaya',
        'city': 'الرياض',
        'district_ar': 'العليا',
        'district_en': 'Al Olaya',
        'latitude': 24.7136,
        'longitude': 46.6753,
        'description_ar': 'مستشفى متخصص يقدم خدمات طبية متميزة',
        'description_en': 'Specialized hospital providing excellent medical services',
        'capacity_beds': 200,
        'capacity_emergency_beds': 50,
        'is_active': True
    },
    {
        'name_ar': 'مستشفى الملك فيصل التخصصي',
        'name_en': 'King Faisal Specialist Hospital',
        'facility_type': 'hospital',
        'is_emergency': True,
        'is_24_7': True,
        'phone': '0114647272',
        'phone_emergency': '0114647272',
        'email': 'info@kfshrc.edu.sa',
        'website': 'www.kfshrc.edu.sa',
        'address_ar': 'طريق الملك عبدالعزيز، المربع',
        'address_en': 'King Abdulaziz Road, Al Murabba',
        'city': 'الرياض',
        'district_ar': 'المربع',
        'district_en': 'Al Murabba',
        'latitude': 24.6408,
        'longitude': 46.7728,
        'description_ar': 'مستشفى تخصصي رائد في الرعاية الصحية',
        'description_en': 'Leading specialist hospital in healthcare',
        'capacity_beds': 500,
        'capacity_emergency_beds': 100,
        'is_active': True
    },
    {
        'name_ar': 'مستشفى الحرس الوطني',
        'name_en': 'National Guard Hospital',
        'facility_type': 'hospital',
        'is_emergency': True,
        'is_24_7': True,
        'phone': '0118011111',
        'phone_emergency': '937',
        'email': 'info@ngha.med.sa',
        'website': 'www.ngha.med.sa',
        'address_ar': 'طريق الملك عبدالعزيز، الملقا',
        'address_en': 'King Abdulaziz Road, Al Malqa',
        'city': 'الرياض',
        'district_ar': 'الملقا',
        'district_en': 'Al Malqa',
        'latitude': 24.7857,
        'longitude': 46.6193,
        'description_ar': 'مستشفى الحرس الوطني بالرياض',
        'description_en': 'National Guard Hospital Riyadh',
        'capacity_beds': 800,
        'capacity_emergency_beds': 150,
        'is_active': True
    },
    {
        'name_ar': 'مستشفى الملك خالد الجامعي',
        'name_en': 'King Khalid University Hospital',
        'facility_type': 'hospital',
        'is_emergency': True,
        'is_24_7': True,
        'phone': '0114672222',
        'phone_emergency': '0114672222',
        'email': 'info@kkuh.sa',
        'website': 'www.kkuh.sa',
        'address_ar': 'طريق الملك سعود، المربع',
        'address_en': 'King Saud Road, Al Murabba',
        'city': 'الرياض',
        'district_ar': 'المربع',
        'district_en': 'Al Murabba',
        'latitude': 24.7235,
        'longitude': 46.6247,
        'description_ar': 'مستشفى جامعي تابع لجامعة الملك سعود',
        'description_en': 'University hospital affiliated with King Saud University',
        'capacity_beds': 600,
        'capacity_emergency_beds': 120,
        'is_active': True
    },
    {
        'name_ar': 'مستشفى الملك سلمان',
        'name_en': 'King Salman Hospital',
        'facility_type': 'hospital',
        'is_emergency': True,
        'is_24_7': True,
        'phone': '0114777777',
        'phone_emergency': '0114777777',
        'email': 'info@ksh.sa',
        'website': 'www.ksh.sa',
        'address_ar': 'طريق الخرج، الرحمانية',
        'address_en': 'Al Kharj Road, Al Rahmaniyah',
        'city': 'الرياض',
        'district_ar': 'الرحمانية',
        'district_en': 'Al Rahmaniyah',
        'latitude': 24.6478,
        'longitude': 46.7119,
        'description_ar': 'مستشفى حديث بأحدث التقنيات الطبية',
        'description_en': 'Modern hospital with latest medical technologies',
        'capacity_beds': 400,
        'capacity_emergency_beds': 80,
        'is_active': True
    },
    {
        'name_ar': 'مركز الرعاية العاجلة - العليا',
        'name_en': 'Urgent Care Center - Al Olaya',
        'facility_type': 'clinic',
        'is_emergency': False,
        'is_24_7': True,
        'phone': '0112223344',
        'phone_emergency': '',
        'email': 'info@ucc-olaya.sa',
        'website': 'www.ucc-olaya.sa',
        'address_ar': 'شارع التحلية، العليا',
        'address_en': 'Tahlia Street, Al Olaya',
        'city': 'الرياض',
        'district_ar': 'العليا',
        'district_en': 'Al Olaya',
        'latitude': 24.7070,
        'longitude': 46.6770,
        'description_ar': 'مركز رعاية عاجلة لحالات غير الطوارئ',
        'description_en': 'Urgent care center for non-emergency cases',
        'capacity_beds': 20,
        'capacity_emergency_beds': 0,
        'is_active': True
    },
    {
        'name_ar': 'مركز الرعاية العاجلة - الملقا',
        'name_en': 'Urgent Care Center - Al Malqa',
        'facility_type': 'clinic',
        'is_emergency': False,
        'is_24_7': True,
        'phone': '0113334455',
        'phone_emergency': '',
        'email': 'info@ucc-malqa.sa',
        'website': 'www.ucc-malqa.sa',
        'address_ar': 'طريق الملك عبدالله، الملقا',
        'address_en': 'King Abdullah Road, Al Malqa',
        'city': 'الرياض',
        'district_ar': 'الملقا',
        'district_en': 'Al Malqa',
        'latitude': 24.7700,
        'longitude': 46.6100,
        'description_ar': 'مركز رعاية عاجلة قريب من مستشفى الحرس الوطني',
        'description_en': 'Urgent care center near National Guard Hospital',
        'capacity_beds': 15,
        'capacity_emergency_beds': 0,
        'is_active': True
    },
    {
        'name_ar': 'عيادات الملقا الطبية',
        'name_en': 'Al Malqa Medical Clinics',
        'facility_type': 'clinic',
        'is_emergency': False,
        'is_24_7': False,
        'phone': '0114445566',
        'phone_emergency': '',
        'email': 'info@malqa-clinics.sa',
        'website': 'www.malqa-clinics.sa',
        'address_ar': 'شارع الأمير سلطان، الملقا',
        'address_en': 'Prince Sultan Street, Al Malqa',
        'city': 'الرياض',
        'district_ar': 'الملقا',
        'district_en': 'Al Malqa',
        'latitude': 24.7800,
        'longitude': 46.6200,
        'description_ar': 'عيادات متخصصة متعددة التخصصات',
        'description_en': 'Multi-specialty medical clinics',
        'capacity_beds': 0,
        'capacity_emergency_beds': 0,
        'is_active': True
    },
    {
        'name_ar': 'مستشفى الدكتور سليمان الحبيب',
        'name_en': 'Dr. Sulaiman Al Habib Hospital',
        'facility_type': 'hospital',
        'is_emergency': True,
        'is_24_7': True,
        'phone': '0112888888',
        'phone_emergency': '0112888888',
        'email': 'info@hmg.com',
        'website': 'www.hmg.com',
        'address_ar': 'طريق العروبة، العليا',
        'address_en': 'Al Urubah Road, Al Olaya',
        'city': 'الرياض',
        'district_ar': 'العليا',
        'district_en': 'Al Olaya',
        'latitude': 24.7200,
        'longitude': 46.6800,
        'description_ar': 'مستشفى خاص رائد في الرعاية الصحية',
        'description_en': 'Leading private hospital in healthcare',
        'capacity_beds': 300,
        'capacity_emergency_beds': 60,
        'is_active': True
    },
    {
        'name_ar': 'مستشفى المملكة',
        'name_en': 'Kingdom Hospital',
        'facility_type': 'hospital',
        'is_emergency': True,
        'is_24_7': True,
        'phone': '0112999999',
        'phone_emergency': '0112999999',
        'email': 'info@kingdom-hospital.sa',
        'website': 'www.kingdom-hospital.sa',
        'address_ar': 'طريق الملك فهد، الورود',
        'address_en': 'King Fahd Road, Al Wurud',
        'city': 'الرياض',
        'district_ar': 'الورود',
        'district_en': 'Al Wurud',
        'latitude': 24.7500,
        'longitude': 46.6500,
        'description_ar': 'مستشفى خاص بمعايير عالمية',
        'description_en': 'Private hospital with international standards',
        'capacity_beds': 250,
        'capacity_emergency_beds': 50,
        'is_active': True
    }
]

def populate_database():
    """Populate database with sample hospitals"""
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Check if hospitals already exist
        existing_count = Hospital.query.count()
        if existing_count > 0:
            print(f"Database already has {existing_count} hospitals. Skipping...")
            return
        
        # Add hospitals
        for hospital_data in hospitals_data:
            hospital = Hospital(**hospital_data)
            db.session.add(hospital)
        
        # Commit all changes
        db.session.commit()
        
        print(f"✅ Successfully added {len(hospitals_data)} hospitals to the database!")
        
        # Print summary
        total = Hospital.query.count()
        emergency = Hospital.query.filter_by(is_emergency=True).count()
        clinics = Hospital.query.filter_by(facility_type='clinic').count()
        
        print(f"\n📊 Database Summary:")
        print(f"   Total facilities: {total}")
        print(f"   Emergency hospitals: {emergency}")
        print(f"   Clinics: {clinics}")

if __name__ == '__main__':
    populate_database()

