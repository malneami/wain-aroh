"""
Admin API Routes for Hospital and Service Management
"""

from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.hospital import (
    Hospital, Service, ServiceCategory, 
    Organization, RiyadhCluster, hospital_services
)
from functools import wraps

admin_api_bp = Blueprint('admin_api', __name__)

# Simple authentication decorator (replace with proper auth in production)
def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Implement proper authentication
        # For now, we'll allow all requests
        return f(*args, **kwargs)
    return decorated_function


# ==================== Organizations ====================

@admin_api_bp.route('/organizations', methods=['GET'])
@require_admin
def get_organizations():
    """Get all organizations"""
    try:
        organizations = Organization.query.all()
        return jsonify({
            'success': True,
            'organizations': [org.to_dict() for org in organizations]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/organizations', methods=['POST'])
@require_admin
def create_organization():
    """Create a new organization"""
    try:
        data = request.json
        org = Organization(
            name_ar=data['name_ar'],
            name_en=data['name_en'],
            type=data['type']
        )
        db.session.add(org)
        db.session.commit()
        return jsonify({
            'success': True,
            'organization': org.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/organizations/<int:org_id>', methods=['PUT'])
@require_admin
def update_organization(org_id):
    """Update an organization"""
    try:
        org = Organization.query.get_or_404(org_id)
        data = request.json
        
        if 'name_ar' in data:
            org.name_ar = data['name_ar']
        if 'name_en' in data:
            org.name_en = data['name_en']
        if 'type' in data:
            org.type = data['type']
        
        db.session.commit()
        return jsonify({
            'success': True,
            'organization': org.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/organizations/<int:org_id>', methods=['DELETE'])
@require_admin
def delete_organization(org_id):
    """Delete an organization"""
    try:
        org = Organization.query.get_or_404(org_id)
        db.session.delete(org)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Riyadh Clusters ====================

@admin_api_bp.route('/clusters', methods=['GET'])
@require_admin
def get_clusters():
    """Get all Riyadh clusters"""
    try:
        clusters = RiyadhCluster.query.order_by(RiyadhCluster.cluster_number).all()
        return jsonify({
            'success': True,
            'clusters': [cluster.to_dict() for cluster in clusters]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/clusters', methods=['POST'])
@require_admin
def create_cluster():
    """Create a new cluster"""
    try:
        data = request.json
        cluster = RiyadhCluster(
            name_ar=data['name_ar'],
            name_en=data['name_en'],
            cluster_number=data['cluster_number'],
            description_ar=data.get('description_ar'),
            description_en=data.get('description_en')
        )
        db.session.add(cluster)
        db.session.commit()
        return jsonify({
            'success': True,
            'cluster': cluster.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Service Categories ====================

@admin_api_bp.route('/service-categories', methods=['GET'])
@require_admin
def get_service_categories():
    """Get all service categories"""
    try:
        categories = ServiceCategory.query.all()
        return jsonify({
            'success': True,
            'categories': [cat.to_dict() for cat in categories]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/service-categories', methods=['POST'])
@require_admin
def create_service_category():
    """Create a new service category"""
    try:
        data = request.json
        category = ServiceCategory(
            name_ar=data['name_ar'],
            name_en=data['name_en'],
            icon=data.get('icon')
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'success': True,
            'category': category.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Services ====================

@admin_api_bp.route('/services', methods=['GET'])
@require_admin
def get_services():
    """Get all services"""
    try:
        services = Service.query.all()
        return jsonify({
            'success': True,
            'services': [service.to_dict() for service in services]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/services', methods=['POST'])
@require_admin
def create_service():
    """Create a new service"""
    try:
        data = request.json
        service = Service(
            name_ar=data['name_ar'],
            name_en=data['name_en'],
            description_ar=data.get('description_ar'),
            description_en=data.get('description_en'),
            category_id=data.get('category_id'),
            is_emergency=data.get('is_emergency', False)
        )
        db.session.add(service)
        db.session.commit()
        return jsonify({
            'success': True,
            'service': service.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/services/<int:service_id>', methods=['PUT'])
@require_admin
def update_service(service_id):
    """Update a service"""
    try:
        service = Service.query.get_or_404(service_id)
        data = request.json
        
        if 'name_ar' in data:
            service.name_ar = data['name_ar']
        if 'name_en' in data:
            service.name_en = data['name_en']
        if 'description_ar' in data:
            service.description_ar = data['description_ar']
        if 'description_en' in data:
            service.description_en = data['description_en']
        if 'category_id' in data:
            service.category_id = data['category_id']
        if 'is_emergency' in data:
            service.is_emergency = data['is_emergency']
        
        db.session.commit()
        return jsonify({
            'success': True,
            'service': service.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/services/<int:service_id>', methods=['DELETE'])
@require_admin
def delete_service(service_id):
    """Delete a service"""
    try:
        service = Service.query.get_or_404(service_id)
        db.session.delete(service)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Hospitals ====================

@admin_api_bp.route('/hospitals', methods=['GET'])
@require_admin
def get_hospitals():
    """Get all hospitals with optional filtering"""
    try:
        query = Hospital.query
        
        # Apply filters
        org_id = request.args.get('organization_id', type=int)
        cluster_id = request.args.get('cluster_id', type=int)
        facility_type = request.args.get('facility_type')
        is_emergency = request.args.get('is_emergency', type=bool)
        
        if org_id:
            query = query.filter_by(organization_id=org_id)
        if cluster_id:
            query = query.filter_by(cluster_id=cluster_id)
        if facility_type:
            query = query.filter_by(facility_type=facility_type)
        if is_emergency is not None:
            query = query.filter_by(is_emergency=is_emergency)
        
        hospitals = query.all()
        include_services = request.args.get('include_services', 'false').lower() == 'true'
        
        return jsonify({
            'success': True,
            'hospitals': [h.to_dict(include_services=include_services) for h in hospitals]
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/hospitals/<int:hospital_id>', methods=['GET'])
@require_admin
def get_hospital(hospital_id):
    """Get a specific hospital"""
    try:
        hospital = Hospital.query.get_or_404(hospital_id)
        return jsonify({
            'success': True,
            'hospital': hospital.to_dict(include_services=True)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/hospitals', methods=['POST'])
@require_admin
def create_hospital():
    """Create a new hospital"""
    try:
        data = request.json
        hospital = Hospital(
            name_ar=data['name_ar'],
            name_en=data['name_en'],
            organization_id=data.get('organization_id'),
            cluster_id=data.get('cluster_id'),
            facility_type=data['facility_type'],
            is_emergency=data.get('is_emergency', False),
            is_24_7=data.get('is_24_7', False),
            phone=data.get('phone'),
            phone_emergency=data.get('phone_emergency'),
            email=data.get('email'),
            website=data.get('website'),
            address_ar=data.get('address_ar'),
            address_en=data.get('address_en'),
            city=data.get('city'),
            district_ar=data.get('district_ar'),
            district_en=data.get('district_en'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            description_ar=data.get('description_ar'),
            description_en=data.get('description_en'),
            capacity_beds=data.get('capacity_beds'),
            capacity_emergency_beds=data.get('capacity_emergency_beds'),
            is_active=data.get('is_active', True)
        )
        db.session.add(hospital)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'hospital': hospital.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/hospitals/<int:hospital_id>', methods=['PUT'])
@require_admin
def update_hospital(hospital_id):
    """Update a hospital"""
    try:
        hospital = Hospital.query.get_or_404(hospital_id)
        data = request.json
        
        # Update fields
        updateable_fields = [
            'name_ar', 'name_en', 'organization_id', 'cluster_id', 'facility_type',
            'is_emergency', 'is_24_7', 'phone', 'phone_emergency', 'email', 'website',
            'address_ar', 'address_en', 'city', 'district_ar', 'district_en',
            'latitude', 'longitude', 'description_ar', 'description_en',
            'capacity_beds', 'capacity_emergency_beds', 'is_active'
        ]
        
        for field in updateable_fields:
            if field in data:
                setattr(hospital, field, data[field])
        
        db.session.commit()
        return jsonify({
            'success': True,
            'hospital': hospital.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/hospitals/<int:hospital_id>', methods=['DELETE'])
@require_admin
def delete_hospital(hospital_id):
    """Delete a hospital"""
    try:
        hospital = Hospital.query.get_or_404(hospital_id)
        db.session.delete(hospital)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Hospital Services ====================

@admin_api_bp.route('/hospitals/<int:hospital_id>/services', methods=['POST'])
@require_admin
def add_hospital_service(hospital_id):
    """Add a service to a hospital"""
    try:
        hospital = Hospital.query.get_or_404(hospital_id)
        data = request.json
        service = Service.query.get_or_404(data['service_id'])
        
        if service not in hospital.services:
            hospital.services.append(service)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'hospital': hospital.to_dict(include_services=True)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@admin_api_bp.route('/hospitals/<int:hospital_id>/services/<int:service_id>', methods=['DELETE'])
@require_admin
def remove_hospital_service(hospital_id, service_id):
    """Remove a service from a hospital"""
    try:
        hospital = Hospital.query.get_or_404(hospital_id)
        service = Service.query.get_or_404(service_id)
        
        if service in hospital.services:
            hospital.services.remove(service)
            db.session.commit()
        
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== Statistics ====================

@admin_api_bp.route('/statistics', methods=['GET'])
@require_admin
def get_statistics():
    """Get dashboard statistics"""
    try:
        stats = {
            'total_hospitals': Hospital.query.count(),
            'total_services': Service.query.count(),
            'total_organizations': Organization.query.count(),
            'total_clusters': RiyadhCluster.query.count(),
            'emergency_hospitals': Hospital.query.filter_by(is_emergency=True).count(),
            'active_hospitals': Hospital.query.filter_by(is_active=True).count(),
            'hospitals_by_type': {}
        }
        
        # Count hospitals by type
        from sqlalchemy import func
        type_counts = db.session.query(
            Hospital.facility_type,
            func.count(Hospital.id)
        ).group_by(Hospital.facility_type).all()
        
        stats['hospitals_by_type'] = {t[0]: t[1] for t in type_counts}
        
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

