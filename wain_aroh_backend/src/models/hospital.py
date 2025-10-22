"""
Hospital and Healthcare Facility Models
"""

from src.models.user import db
from datetime import datetime

class Organization(db.Model):
    """Healthcare organization/entity"""
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # ministry, military, private, independent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hospitals = db.relationship('Hospital', backref='organization', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'type': self.type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class RiyadhCluster(db.Model):
    """Riyadh healthcare clusters (تجمعات الرياض الصحية)"""
    __tablename__ = 'riyadh_clusters'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(200), nullable=False)  # e.g., "تجمع الرياض الصحي الأول"
    name_en = db.Column(db.String(200), nullable=False)  # e.g., "Riyadh First Health Cluster"
    cluster_number = db.Column(db.Integer, nullable=False)  # 1, 2, 3, etc.
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    hospitals = db.relationship('Hospital', backref='cluster', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'cluster_number': self.cluster_number,
            'description_ar': self.description_ar,
            'description_en': self.description_en,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ServiceCategory(db.Model):
    """Medical service categories"""
    __tablename__ = 'service_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    icon = db.Column(db.String(50))  # Icon name for UI
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    services = db.relationship('Service', backref='category', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'icon': self.icon,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Service(db.Model):
    """Medical services offered"""
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'))
    is_emergency = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'description_ar': self.description_ar,
            'description_en': self.description_en,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'is_emergency': self.is_emergency,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


# Association table for many-to-many relationship between hospitals and services
hospital_services = db.Table('hospital_services',
    db.Column('hospital_id', db.Integer, db.ForeignKey('hospitals.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True),
    db.Column('available_24_7', db.Boolean, default=False),
    db.Column('waiting_time_minutes', db.Integer),
    db.Column('notes_ar', db.Text),
    db.Column('notes_en', db.Text)
)


class Hospital(db.Model):
    """Healthcare facilities"""
    __tablename__ = 'hospitals'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    
    # Organization and cluster
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    cluster_id = db.Column(db.Integer, db.ForeignKey('riyadh_clusters.id'), nullable=True)
    
    # Type and classification
    facility_type = db.Column(db.String(50), nullable=False)  # hospital, clinic, health_center, emergency_center
    is_emergency = db.Column(db.Boolean, default=False)
    is_24_7 = db.Column(db.Boolean, default=False)
    
    # Contact information
    phone = db.Column(db.String(50))
    phone_emergency = db.Column(db.String(50))
    email = db.Column(db.String(200))
    website = db.Column(db.String(200))
    
    # Location
    address_ar = db.Column(db.Text)
    address_en = db.Column(db.Text)
    city = db.Column(db.String(100))
    district_ar = db.Column(db.String(100))
    district_en = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    
    # Additional info
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    capacity_beds = db.Column(db.Integer)
    capacity_emergency_beds = db.Column(db.Integer)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    services = db.relationship('Service', secondary=hospital_services, lazy='subquery',
                              backref=db.backref('hospitals', lazy=True))
    
    def to_dict(self, include_services=False):
        result = {
            'id': self.id,
            'name_ar': self.name_ar,
            'name_en': self.name_en,
            'organization_id': self.organization_id,
            'organization': self.organization.to_dict() if self.organization else None,
            'cluster_id': self.cluster_id,
            'cluster': self.cluster.to_dict() if self.cluster else None,
            'facility_type': self.facility_type,
            'is_emergency': self.is_emergency,
            'is_24_7': self.is_24_7,
            'phone': self.phone,
            'phone_emergency': self.phone_emergency,
            'email': self.email,
            'website': self.website,
            'address_ar': self.address_ar,
            'address_en': self.address_en,
            'city': self.city,
            'district_ar': self.district_ar,
            'district_en': self.district_en,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description_ar': self.description_ar,
            'description_en': self.description_en,
            'capacity_beds': self.capacity_beds,
            'capacity_emergency_beds': self.capacity_emergency_beds,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_services:
            result['services'] = [service.to_dict() for service in self.services]
        
        return result

