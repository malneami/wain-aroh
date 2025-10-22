"""
Seed data for the database
"""

from src.models.user import db
from src.models.hospital import (
    Organization, RiyadhCluster, ServiceCategory, Service, Hospital
)

def seed_organizations():
    """Seed healthcare organizations"""
    organizations = [
        {
            'name_ar': 'وزارة الصحة',
            'name_en': 'Ministry of Health',
            'type': 'ministry'
        },
        {
            'name_ar': 'الحرس الوطني',
            'name_en': 'National Guard Health Affairs',
            'type': 'military'
        },
        {
            'name_ar': 'الخدمات الطبية للقوات المسلحة',
            'name_en': 'Armed Forces Medical Services',
            'type': 'military'
        },
        {
            'name_ar': 'وزارة الداخلية - الأمن العام',
            'name_en': 'Ministry of Interior - Public Security',
            'type': 'military'
        },
        {
            'name_ar': 'القطاع الخاص',
            'name_en': 'Private Sector',
            'type': 'private'
        },
        {
            'name_ar': 'مستشفيات جامعية',
            'name_en': 'University Hospitals',
            'type': 'independent'
        }
    ]
    
    for org_data in organizations:
        if not Organization.query.filter_by(name_en=org_data['name_en']).first():
            org = Organization(**org_data)
            db.session.add(org)
    
    db.session.commit()
    print("✓ Organizations seeded")


def seed_riyadh_clusters():
    """Seed Riyadh health clusters"""
    clusters = [
        {
            'name_ar': 'تجمع الرياض الصحي الأول',
            'name_en': 'Riyadh First Health Cluster',
            'cluster_number': 1,
            'description_ar': 'يخدم شمال الرياض',
            'description_en': 'Serves North Riyadh'
        },
        {
            'name_ar': 'تجمع الرياض الصحي الثاني',
            'name_en': 'Riyadh Second Health Cluster',
            'cluster_number': 2,
            'description_ar': 'يخدم وسط وشرق الرياض',
            'description_en': 'Serves Central and East Riyadh'
        },
        {
            'name_ar': 'تجمع الرياض الصحي الثالث',
            'name_en': 'Riyadh Third Health Cluster',
            'cluster_number': 3,
            'description_ar': 'يخدم جنوب وغرب الرياض',
            'description_en': 'Serves South and West Riyadh'
        }
    ]
    
    for cluster_data in clusters:
        if not RiyadhCluster.query.filter_by(cluster_number=cluster_data['cluster_number']).first():
            cluster = RiyadhCluster(**cluster_data)
            db.session.add(cluster)
    
    db.session.commit()
    print("✓ Riyadh clusters seeded")


def seed_service_categories():
    """Seed service categories"""
    categories = [
        {'name_ar': 'الطوارئ', 'name_en': 'Emergency', 'icon': 'emergency'},
        {'name_ar': 'العيادات الخارجية', 'name_en': 'Outpatient Clinics', 'icon': 'clinic'},
        {'name_ar': 'الجراحة', 'name_en': 'Surgery', 'icon': 'surgery'},
        {'name_ar': 'الأشعة والتصوير', 'name_en': 'Radiology & Imaging', 'icon': 'radiology'},
        {'name_ar': 'المختبر', 'name_en': 'Laboratory', 'icon': 'lab'},
        {'name_ar': 'الولادة والنساء', 'name_en': 'Obstetrics & Gynecology', 'icon': 'maternity'},
        {'name_ar': 'طب الأطفال', 'name_en': 'Pediatrics', 'icon': 'pediatrics'},
        {'name_ar': 'القلب', 'name_en': 'Cardiology', 'icon': 'cardiology'},
        {'name_ar': 'العناية المركزة', 'name_en': 'Intensive Care', 'icon': 'icu'},
        {'name_ar': 'الصيدلية', 'name_en': 'Pharmacy', 'icon': 'pharmacy'}
    ]
    
    for cat_data in categories:
        if not ServiceCategory.query.filter_by(name_en=cat_data['name_en']).first():
            category = ServiceCategory(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    print("✓ Service categories seeded")


def seed_services():
    """Seed medical services"""
    # Get categories
    emergency_cat = ServiceCategory.query.filter_by(name_en='Emergency').first()
    clinic_cat = ServiceCategory.query.filter_by(name_en='Outpatient Clinics').first()
    surgery_cat = ServiceCategory.query.filter_by(name_en='Surgery').first()
    radiology_cat = ServiceCategory.query.filter_by(name_en='Radiology & Imaging').first()
    lab_cat = ServiceCategory.query.filter_by(name_en='Laboratory').first()
    
    services = [
        {
            'name_ar': 'طوارئ عامة',
            'name_en': 'General Emergency',
            'description_ar': 'خدمات الطوارئ العامة على مدار الساعة',
            'description_en': '24/7 general emergency services',
            'category_id': emergency_cat.id if emergency_cat else None,
            'is_emergency': True
        },
        {
            'name_ar': 'طوارئ القلب',
            'name_en': 'Cardiac Emergency',
            'description_ar': 'طوارئ أمراض القلب والأوعية الدموية',
            'description_en': 'Cardiovascular emergency services',
            'category_id': emergency_cat.id if emergency_cat else None,
            'is_emergency': True
        },
        {
            'name_ar': 'طوارئ الأطفال',
            'name_en': 'Pediatric Emergency',
            'description_ar': 'طوارئ الأطفال المتخصصة',
            'description_en': 'Specialized pediatric emergency',
            'category_id': emergency_cat.id if emergency_cat else None,
            'is_emergency': True
        },
        {
            'name_ar': 'عيادة الباطنة',
            'name_en': 'Internal Medicine Clinic',
            'category_id': clinic_cat.id if clinic_cat else None,
            'is_emergency': False
        },
        {
            'name_ar': 'عيادة الجراحة',
            'name_en': 'Surgery Clinic',
            'category_id': clinic_cat.id if clinic_cat else None,
            'is_emergency': False
        },
        {
            'name_ar': 'جراحة عامة',
            'name_en': 'General Surgery',
            'category_id': surgery_cat.id if surgery_cat else None,
            'is_emergency': False
        },
        {
            'name_ar': 'الأشعة السينية',
            'name_en': 'X-Ray',
            'category_id': radiology_cat.id if radiology_cat else None,
            'is_emergency': False
        },
        {
            'name_ar': 'الأشعة المقطعية',
            'name_en': 'CT Scan',
            'category_id': radiology_cat.id if radiology_cat else None,
            'is_emergency': False
        },
        {
            'name_ar': 'التحاليل الطبية',
            'name_en': 'Medical Laboratory',
            'category_id': lab_cat.id if lab_cat else None,
            'is_emergency': False
        }
    ]
    
    for service_data in services:
        if not Service.query.filter_by(name_en=service_data['name_en']).first():
            service = Service(**service_data)
            db.session.add(service)
    
    db.session.commit()
    print("✓ Services seeded")


def seed_sample_hospitals():
    """Seed sample hospitals"""
    # Get references
    moh = Organization.query.filter_by(name_en='Ministry of Health').first()
    ng = Organization.query.filter_by(name_en='National Guard Health Affairs').first()
    cluster1 = RiyadhCluster.query.filter_by(cluster_number=1).first()
    cluster2 = RiyadhCluster.query.filter_by(cluster_number=2).first()
    
    hospitals = [
        {
            'name_ar': 'مستشفى الملك فهد الجامعي',
            'name_en': 'King Fahd University Hospital',
            'organization_id': moh.id if moh else None,
            'cluster_id': cluster2.id if cluster2 else None,
            'facility_type': 'hospital',
            'is_emergency': True,
            'is_24_7': True,
            'phone': '0112889999',
            'phone_emergency': '0112889911',
            'city': 'Riyadh',
            'district_ar': 'الملز',
            'district_en': 'Al Malaz',
            'latitude': 24.6854,
            'longitude': 46.7208,
            'capacity_beds': 800,
            'capacity_emergency_beds': 50,
            'is_active': True
        },
        {
            'name_ar': 'مستشفى الملك عبدالعزيز الطبي',
            'name_en': 'King Abdulaziz Medical City',
            'organization_id': ng.id if ng else None,
            'facility_type': 'hospital',
            'is_emergency': True,
            'is_24_7': True,
            'phone': '0118011111',
            'phone_emergency': '0118011111',
            'city': 'Riyadh',
            'district_ar': 'الحرس الوطني',
            'district_en': 'National Guard',
            'latitude': 24.8138,
            'longitude': 46.7089,
            'capacity_beds': 1500,
            'capacity_emergency_beds': 100,
            'is_active': True
        }
    ]
    
    for hospital_data in hospitals:
        if not Hospital.query.filter_by(name_en=hospital_data['name_en']).first():
            hospital = Hospital(**hospital_data)
            db.session.add(hospital)
    
    db.session.commit()
    print("✓ Sample hospitals seeded")


def seed_all():
    """Seed all data"""
    print("Starting database seeding...")
    seed_organizations()
    seed_riyadh_clusters()
    seed_service_categories()
    seed_services()
    seed_sample_hospitals()
    print("✓ Database seeding completed!")


if __name__ == '__main__':
    from src.main import app
    with app.app_context():
        seed_all()

