"""
خدمة مقاييس الأداء والمؤشرات الرئيسية للمنشآت الصحية
Performance Metrics and KPI Tracking Service for Healthcare Facilities
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import random


@dataclass
class KPI:
    """مؤشر أداء رئيسي"""
    name: str
    value: float
    unit: str
    target: float
    status: str  # "good", "warning", "critical"
    trend: str  # "up", "down", "stable"
    description: str


@dataclass
class PerformanceReport:
    """تقرير أداء شامل"""
    facility_id: int
    facility_name: str
    report_date: datetime
    period: str  # "daily", "weekly", "monthly"
    
    # المؤشرات الرئيسية
    kpis: List[KPI] = field(default_factory=list)
    
    # الإحصائيات
    total_patients: int = 0
    emergency_cases: int = 0
    scheduled_appointments: int = 0
    walk_ins: int = 0
    
    # الأداء
    avg_wait_time: float = 0.0
    avg_consultation_time: float = 0.0
    patient_satisfaction: float = 0.0
    
    # الموارد
    bed_occupancy_rate: float = 0.0
    staff_utilization: float = 0.0
    
    # الجودة
    readmission_rate: float = 0.0
    complication_rate: float = 0.0
    mortality_rate: float = 0.0


class PerformanceMetricsService:
    """خدمة مقاييس الأداء"""
    
    def __init__(self):
        """تهيئة الخدمة"""
        self.metrics_cache = {}
    
    def calculate_kpi_status(self, value: float, target: float, higher_is_better: bool = True) -> str:
        """
        حساب حالة المؤشر
        Calculate KPI status
        
        Args:
            value: القيمة الحالية
            target: القيمة المستهدفة
            higher_is_better: هل القيمة الأعلى أفضل؟
            
        Returns:
            الحالة: "good", "warning", "critical"
        """
        if higher_is_better:
            if value >= target:
                return "good"
            elif value >= target * 0.8:
                return "warning"
            else:
                return "critical"
        else:
            if value <= target:
                return "good"
            elif value <= target * 1.2:
                return "warning"
            else:
                return "critical"
    
    def calculate_trend(self, current: float, previous: float) -> str:
        """
        حساب الاتجاه
        Calculate trend
        
        Args:
            current: القيمة الحالية
            previous: القيمة السابقة
            
        Returns:
            الاتجاه: "up", "down", "stable"
        """
        change_percent = ((current - previous) / previous * 100) if previous > 0 else 0
        
        if abs(change_percent) < 5:
            return "stable"
        elif change_percent > 0:
            return "up"
        else:
            return "down"
    
    def generate_facility_kpis(self, facility_id: int, facility_name: str) -> List[KPI]:
        """
        توليد مؤشرات الأداء للمنشأة
        Generate KPIs for a facility
        
        Args:
            facility_id: معرف المنشأة
            facility_name: اسم المنشأة
            
        Returns:
            قائمة المؤشرات
        """
        # في بيئة الإنتاج، هذه البيانات ستأتي من قاعدة البيانات
        # For production, this data would come from the database
        
        kpis = [
            KPI(
                name="معدل رضا المرضى",
                value=random.uniform(80, 95),
                unit="%",
                target=90.0,
                status="good",
                trend="up",
                description="نسبة المرضى الراضين عن الخدمة"
            ),
            KPI(
                name="متوسط وقت الانتظار",
                value=random.uniform(15, 45),
                unit="دقيقة",
                target=30.0,
                status="good",
                trend="down",
                description="متوسط وقت انتظار المريض"
            ),
            KPI(
                name="معدل إشغال الأسرّة",
                value=random.uniform(60, 90),
                unit="%",
                target=80.0,
                status="good",
                trend="stable",
                description="نسبة إشغال الأسرّة المتاحة"
            ),
            KPI(
                name="معدل المواعيد في الوقت",
                value=random.uniform(75, 95),
                unit="%",
                target=85.0,
                status="good",
                trend="up",
                description="نسبة المواعيد التي تمت في الوقت المحدد"
            ),
            KPI(
                name="معدل إعادة الدخول",
                value=random.uniform(3, 8),
                unit="%",
                target=5.0,
                status="warning",
                trend="stable",
                description="نسبة المرضى الذين عادوا خلال 30 يوم"
            ),
            KPI(
                name="وقت الاستجابة للطوارئ",
                value=random.uniform(5, 15),
                unit="دقيقة",
                target=10.0,
                status="good",
                trend="down",
                description="متوسط وقت الاستجابة لحالات الطوارئ"
            ),
            KPI(
                name="معدل استخدام الكادر",
                value=random.uniform(70, 90),
                unit="%",
                target=80.0,
                status="good",
                trend="stable",
                description="نسبة استخدام الكادر الطبي"
            ),
            KPI(
                name="معدل العلاجات الناجحة",
                value=random.uniform(85, 98),
                unit="%",
                target=90.0,
                status="good",
                trend="up",
                description="نسبة العلاجات الناجحة"
            ),
        ]
        
        # حساب الحالة والاتجاه لكل مؤشر
        for kpi in kpis:
            higher_is_better = kpi.name not in ["متوسط وقت الانتظار", "معدل إعادة الدخول", "وقت الاستجابة للطوارئ"]
            kpi.status = self.calculate_kpi_status(kpi.value, kpi.target, higher_is_better)
        
        return kpis
    
    def generate_performance_report(
        self,
        facility_id: int,
        facility_name: str,
        period: str = "daily"
    ) -> PerformanceReport:
        """
        توليد تقرير أداء شامل
        Generate comprehensive performance report
        
        Args:
            facility_id: معرف المنشأة
            facility_name: اسم المنشأة
            period: الفترة الزمنية
            
        Returns:
            تقرير الأداء
        """
        kpis = self.generate_facility_kpis(facility_id, facility_name)
        
        report = PerformanceReport(
            facility_id=facility_id,
            facility_name=facility_name,
            report_date=datetime.now(),
            period=period,
            kpis=kpis,
            total_patients=random.randint(100, 500),
            emergency_cases=random.randint(20, 100),
            scheduled_appointments=random.randint(50, 300),
            walk_ins=random.randint(30, 100),
            avg_wait_time=random.uniform(15, 45),
            avg_consultation_time=random.uniform(10, 30),
            patient_satisfaction=random.uniform(80, 95),
            bed_occupancy_rate=random.uniform(60, 90),
            staff_utilization=random.uniform(70, 90),
            readmission_rate=random.uniform(3, 8),
            complication_rate=random.uniform(1, 5),
            mortality_rate=random.uniform(0.5, 2),
        )
        
        return report
    
    def get_facility_dashboard_data(self, facility_id: int, facility_name: str) -> Dict:
        """
        الحصول على بيانات لوحة التحكم للمنشأة
        Get dashboard data for a facility
        
        Args:
            facility_id: معرف المنشأة
            facility_name: اسم المنشأة
            
        Returns:
            بيانات لوحة التحكم
        """
        report = self.generate_performance_report(facility_id, facility_name)
        
        # تحويل المؤشرات إلى قاموس
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
            for kpi in report.kpis
        ]
        
        # بيانات الرسوم البيانية
        # في بيئة الإنتاج، هذه البيانات ستأتي من قاعدة البيانات
        chart_data = {
            "patient_flow": {
                "labels": ["السبت", "الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة"],
                "data": [
                    random.randint(80, 150) for _ in range(7)
                ]
            },
            "wait_times": {
                "labels": ["8-10", "10-12", "12-14", "14-16", "16-18", "18-20"],
                "data": [
                    random.randint(15, 45) for _ in range(6)
                ]
            },
            "satisfaction_trend": {
                "labels": ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو"],
                "data": [
                    random.uniform(80, 95) for _ in range(6)
                ]
            },
            "bed_occupancy": {
                "labels": ["الطوارئ", "العناية المركزة", "الجراحة", "الباطنية", "الأطفال"],
                "data": [
                    random.uniform(60, 90) for _ in range(5)
                ]
            }
        }
        
        return {
            "facility_id": facility_id,
            "facility_name": facility_name,
            "report_date": report.report_date.isoformat(),
            "period": report.period,
            "kpis": kpis_dict,
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
            },
            "charts": chart_data
        }
    
    def compare_facilities_performance(
        self,
        facility_ids: List[int],
        facility_names: List[str]
    ) -> Dict:
        """
        مقارنة أداء عدة منشآت
        Compare performance of multiple facilities
        
        Args:
            facility_ids: معرفات المنشآت
            facility_names: أسماء المنشآت
            
        Returns:
            بيانات المقارنة
        """
        reports = [
            self.generate_performance_report(fid, fname)
            for fid, fname in zip(facility_ids, facility_names)
        ]
        
        comparison = {
            "facilities": [
                {"id": fid, "name": fname}
                for fid, fname in zip(facility_ids, facility_names)
            ],
            "metrics": {
                "patient_satisfaction": [round(r.patient_satisfaction, 1) for r in reports],
                "avg_wait_time": [round(r.avg_wait_time, 1) for r in reports],
                "bed_occupancy_rate": [round(r.bed_occupancy_rate, 1) for r in reports],
                "readmission_rate": [round(r.readmission_rate, 1) for r in reports],
                "total_patients": [r.total_patients for r in reports],
            },
            "rankings": {
                "best_satisfaction": max(range(len(reports)), key=lambda i: reports[i].patient_satisfaction),
                "lowest_wait_time": min(range(len(reports)), key=lambda i: reports[i].avg_wait_time),
                "best_occupancy": min(range(len(reports)), key=lambda i: abs(reports[i].bed_occupancy_rate - 80)),
                "lowest_readmission": min(range(len(reports)), key=lambda i: reports[i].readmission_rate),
            }
        }
        
        return comparison
    
    def get_real_time_status(self, facility_id: int) -> Dict:
        """
        الحصول على الحالة الفورية للمنشأة
        Get real-time status of a facility
        
        Args:
            facility_id: معرف المنشأة
            
        Returns:
            الحالة الفورية
        """
        return {
            "facility_id": facility_id,
            "timestamp": datetime.now().isoformat(),
            "current_patients": random.randint(50, 200),
            "waiting_patients": random.randint(10, 50),
            "available_beds": random.randint(10, 50),
            "available_doctors": random.randint(5, 20),
            "current_wait_time": random.randint(15, 60),
            "emergency_capacity": random.choice(["متاح", "محدود", "ممتلئ"]),
            "status": random.choice(["normal", "busy", "critical"]),
            "alerts": []
        }
    
    def get_historical_trends(
        self,
        facility_id: int,
        metric: str,
        days: int = 30
    ) -> Dict:
        """
        الحصول على الاتجاهات التاريخية
        Get historical trends
        
        Args:
            facility_id: معرف المنشأة
            metric: المقياس المطلوب
            days: عدد الأيام
            
        Returns:
            بيانات الاتجاه
        """
        dates = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days-1, -1, -1)]
        
        # توليد بيانات عشوائية للتوضيح
        if metric == "patient_satisfaction":
            values = [random.uniform(80, 95) for _ in range(days)]
        elif metric == "wait_time":
            values = [random.uniform(15, 45) for _ in range(days)]
        elif metric == "bed_occupancy":
            values = [random.uniform(60, 90) for _ in range(days)]
        else:
            values = [random.uniform(0, 100) for _ in range(days)]
        
        return {
            "facility_id": facility_id,
            "metric": metric,
            "period_days": days,
            "dates": dates,
            "values": [round(v, 1) for v in values],
            "average": round(sum(values) / len(values), 1),
            "min": round(min(values), 1),
            "max": round(max(values), 1),
        }


# مثيل عام من الخدمة
metrics_service = PerformanceMetricsService()

