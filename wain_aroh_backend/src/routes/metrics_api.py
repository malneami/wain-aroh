"""
واجهة برمجة التطبيقات لمقاييس الأداء
Performance Metrics API Routes
"""

from flask import Blueprint, request, jsonify
from ..services.performance_metrics import metrics_service
from ..models.hospital import Hospital

# إنشاء Blueprint
metrics_bp = Blueprint('metrics', __name__, url_prefix='/api/metrics')


@metrics_bp.route('/facility/<int:facility_id>/dashboard', methods=['GET'])
def get_facility_dashboard(facility_id):
    """
    الحصول على بيانات لوحة التحكم للمنشأة
    Get facility dashboard data
    """
    try:
        # الحصول على المنشأة
        hospital = Hospital.query.get(facility_id)
        
        if not hospital:
            return jsonify({
                'success': False,
                'error': 'المنشأة غير موجودة'
            }), 404
        
        # الحصول على بيانات لوحة التحكم
        dashboard_data = metrics_service.get_facility_dashboard_data(
            facility_id,
            hospital.name
        )
        
        return jsonify({
            'success': True,
            'dashboard': dashboard_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@metrics_bp.route('/facility/<int:facility_id>/kpis', methods=['GET'])
def get_facility_kpis(facility_id):
    """
    الحصول على مؤشرات الأداء الرئيسية للمنشأة
    Get facility KPIs
    """
    try:
        hospital = Hospital.query.get(facility_id)
        
        if not hospital:
            return jsonify({
                'success': False,
                'error': 'المنشأة غير موجودة'
            }), 404
        
        kpis = metrics_service.generate_facility_kpis(facility_id, hospital.name)
        
        kpis_dict = [
            {
                "name": kpi.name,
                "value": round(kpi.value, 1),
                "unit": kpi.unit,
                "target": kpi.target,
                "status": kpi.status,
                "trend": kpi.trend,
                "description": kpi.description
            }
            for kpi in kpis
        ]
        
        return jsonify({
            'success': True,
            'kpis': kpis_dict
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@metrics_bp.route('/facility/<int:facility_id>/status', methods=['GET'])
def get_facility_status(facility_id):
    """
    الحصول على الحالة الفورية للمنشأة
    Get real-time facility status
    """
    try:
        hospital = Hospital.query.get(facility_id)
        
        if not hospital:
            return jsonify({
                'success': False,
                'error': 'المنشأة غير موجودة'
            }), 404
        
        status = metrics_service.get_real_time_status(facility_id)
        
        return jsonify({
            'success': True,
            'status': status
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@metrics_bp.route('/facility/<int:facility_id>/trends', methods=['GET'])
def get_facility_trends(facility_id):
    """
    الحصول على الاتجاهات التاريخية
    Get historical trends
    
    Query params:
    - metric: المقياس (patient_satisfaction, wait_time, bed_occupancy)
    - days: عدد الأيام (default: 30)
    """
    try:
        hospital = Hospital.query.get(facility_id)
        
        if not hospital:
            return jsonify({
                'success': False,
                'error': 'المنشأة غير موجودة'
            }), 404
        
        metric = request.args.get('metric', 'patient_satisfaction')
        days = int(request.args.get('days', 30))
        
        trends = metrics_service.get_historical_trends(facility_id, metric, days)
        
        return jsonify({
            'success': True,
            'trends': trends
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@metrics_bp.route('/compare', methods=['POST'])
def compare_facilities():
    """
    مقارنة أداء عدة منشآت
    Compare performance of multiple facilities
    
    Body:
    {
        "facility_ids": [1, 2, 3]
    }
    """
    try:
        data = request.json or {}
        facility_ids = data.get('facility_ids', [])
        
        if not facility_ids or len(facility_ids) < 2:
            return jsonify({
                'success': False,
                'error': 'يجب تحديد منشأتين على الأقل للمقارنة'
            }), 400
        
        # الحصول على المنشآت
        hospitals = Hospital.query.filter(Hospital.id.in_(facility_ids)).all()
        
        if len(hospitals) != len(facility_ids):
            return jsonify({
                'success': False,
                'error': 'بعض المنشآت غير موجودة'
            }), 404
        
        facility_names = [h.name for h in hospitals]
        
        comparison = metrics_service.compare_facilities_performance(
            facility_ids,
            facility_names
        )
        
        return jsonify({
            'success': True,
            'comparison': comparison
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@metrics_bp.route('/facility/<int:facility_id>/report', methods=['GET'])
def get_performance_report(facility_id):
    """
    الحصول على تقرير أداء شامل
    Get comprehensive performance report
    
    Query params:
    - period: الفترة (daily, weekly, monthly)
    """
    try:
        hospital = Hospital.query.get(facility_id)
        
        if not hospital:
            return jsonify({
                'success': False,
                'error': 'المنشأة غير موجودة'
            }), 404
        
        period = request.args.get('period', 'daily')
        
        report = metrics_service.generate_performance_report(
            facility_id,
            hospital.name,
            period
        )
        
        report_dict = {
            "facility_id": report.facility_id,
            "facility_name": report.facility_name,
            "report_date": report.report_date.isoformat(),
            "period": report.period,
            "kpis": [
                {
                    "name": kpi.name,
                    "value": round(kpi.value, 1),
                    "unit": kpi.unit,
                    "target": kpi.target,
                    "status": kpi.status,
                    "trend": kpi.trend,
                    "description": kpi.description
                }
                for kpi in report.kpis
            ],
            "statistics": {
                "total_patients": report.total_patients,
                "emergency_cases": report.emergency_cases,
                "scheduled_appointments": report.scheduled_appointments,
                "walk_ins": report.walk_ins,
                "avg_wait_time": round(report.avg_wait_time, 1),
                "avg_consultation_time": round(report.avg_consultation_time, 1),
                "patient_satisfaction": round(report.patient_satisfaction, 1),
                "bed_occupancy_rate": round(report.bed_occupancy_rate, 1),
                "staff_utilization": round(report.staff_utilization, 1),
                "readmission_rate": round(report.readmission_rate, 1),
                "complication_rate": round(report.complication_rate, 1),
                "mortality_rate": round(report.mortality_rate, 2),
            }
        }
        
        return jsonify({
            'success': True,
            'report': report_dict
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@metrics_bp.route('/overview', methods=['GET'])
def get_system_overview():
    """
    الحصول على نظرة عامة على النظام
    Get system overview
    """
    try:
        hospitals = Hospital.query.all()
        
        # حساب الإحصائيات العامة
        total_facilities = len(hospitals)
        active_facilities = sum(1 for h in hospitals if h.is_active)
        
        # تصنيف حسب الجهة
        org_counts = {}
        for h in hospitals:
            org = h.organization if hasattr(h, 'organization') else 'غير محدد'
            org_counts[org] = org_counts.get(org, 0) + 1
        
        # تصنيف حسب التجمع
        cluster_counts = {}
        for h in hospitals:
            cluster = h.cluster if hasattr(h, 'cluster') else 'غير محدد'
            cluster_counts[cluster] = cluster_counts.get(cluster, 0) + 1
        
        overview = {
            "total_facilities": total_facilities,
            "active_facilities": active_facilities,
            "inactive_facilities": total_facilities - active_facilities,
            "by_organization": org_counts,
            "by_cluster": cluster_counts,
            "system_health": "good",  # يمكن حسابه بناءً على المقاييس
            "last_updated": "2024-10-14T12:00:00"
        }
        
        return jsonify({
            'success': True,
            'overview': overview
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

