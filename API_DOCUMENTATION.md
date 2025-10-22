# 📚 Wain Aroh API Documentation
## وثائق واجهة برمجة التطبيقات - نظام وين أروح

---

## Base URL
```
http://localhost:5000/api
```

---

## 🔍 Search APIs

### 1. Search Facilities
البحث عن المنشآت الصحية

**Endpoint:** `POST /search/facilities`

**Request Body:**
```json
{
  "specialties": ["قلب", "أطفال"],
  "location": {"lat": 24.7136, "lng": 46.6753},
  "max_distance_km": 20,
  "organizations": ["وزارة الصحة"],
  "clusters": ["تجمع الرياض الأول"],
  "min_rating": 4.0,
  "available_now": true,
  "accepts_emergency": false,
  "required_services": [],
  "sort_by": "relevance",
  "page": 1,
  "limit": 10
}
```

**Response:**
```json
{
  "success": true,
  "results": [...],
  "total_results": 15,
  "page": 1,
  "limit": 10,
  "total_pages": 2,
  "applied_filters": {...},
  "stats": {
    "avg_distance": 5.2,
    "avg_rating": 4.3,
    "avg_wait_time": 32,
    "available_count": 12
  },
  "search_time_ms": 45.2
}
```

### 2. Get Facility Details
الحصول على تفاصيل منشأة

**Endpoint:** `GET /search/facilities/{facility_id}`

**Response:**
```json
{
  "success": true,
  "facility": {
    "id": 1,
    "name": "مستشفى الملك فهد",
    "location": {"lat": 24.7136, "lng": 46.6753},
    "specialties": ["قلب", "جراحة"],
    "performance": {...}
  }
}
```

### 3. Compare Facilities
مقارنة المنشآت

**Endpoint:** `POST /search/facilities/compare`

**Request Body:**
```json
{
  "facility_ids": [1, 2, 3]
}
```

### 4. Get Available Filters
الحصول على الفلاتر المتاحة

**Endpoint:** `GET /search/filters`

**Response:**
```json
{
  "success": true,
  "filters": {
    "specialties": ["قلب", "أطفال", ...],
    "organizations": ["وزارة الصحة", ...],
    "clusters": ["تجمع الرياض الأول", ...],
    "services": [...],
    "sort_options": [...]
  }
}
```

### 5. Search Nearby
البحث عن الأقرب

**Endpoint:** `POST /search/nearby`

**Request Body:**
```json
{
  "location": {"lat": 24.7136, "lng": 46.6753},
  "radius_km": 10,
  "limit": 5
}
```

---

## 📊 Metrics APIs

### 1. Get Facility Dashboard
لوحة تحكم المنشأة

**Endpoint:** `GET /metrics/facility/{facility_id}/dashboard`

**Response:**
```json
{
  "success": true,
  "dashboard": {
    "facility_id": 1,
    "facility_name": "مستشفى الملك فهد",
    "kpis": [...],
    "statistics": {...},
    "charts": {...}
  }
}
```

### 2. Get Facility KPIs
مؤشرات الأداء

**Endpoint:** `GET /metrics/facility/{facility_id}/kpis`

**Response:**
```json
{
  "success": true,
  "kpis": [
    {
      "name": "معدل رضا المرضى",
      "value": 92.5,
      "unit": "%",
      "target": 90.0,
      "status": "good",
      "trend": "up"
    }
  ]
}
```

### 3. Get Real-time Status
الحالة الفورية

**Endpoint:** `GET /metrics/facility/{facility_id}/status`

**Response:**
```json
{
  "success": true,
  "status": {
    "facility_id": 1,
    "current_patients": 150,
    "waiting_patients": 25,
    "available_beds": 30,
    "available_doctors": 15,
    "current_wait_time": 35,
    "emergency_capacity": "متاح",
    "status": "normal"
  }
}
```

### 4. Get Historical Trends
الاتجاهات التاريخية

**Endpoint:** `GET /metrics/facility/{facility_id}/trends`

**Query Parameters:**
- `metric`: patient_satisfaction | wait_time | bed_occupancy
- `days`: عدد الأيام (default: 30)

**Response:**
```json
{
  "success": true,
  "trends": {
    "facility_id": 1,
    "metric": "patient_satisfaction",
    "period_days": 30,
    "dates": [...],
    "values": [...],
    "average": 88.5,
    "min": 82.0,
    "max": 94.0
  }
}
```

### 5. Compare Facilities Performance
مقارنة الأداء

**Endpoint:** `POST /metrics/compare`

**Request Body:**
```json
{
  "facility_ids": [1, 2, 3]
}
```

### 6. Get System Overview
نظرة عامة على النظام

**Endpoint:** `GET /metrics/overview`

**Response:**
```json
{
  "success": true,
  "overview": {
    "total_facilities": 50,
    "active_facilities": 48,
    "by_organization": {...},
    "by_cluster": {...},
    "system_health": "good"
  }
}
```

---

## 📅 Appointment APIs

### 1. Get Available Slots
الحصول على الفترات المتاحة

**Endpoint:** `POST /appointments/slots`

**Request Body:**
```json
{
  "facility_id": 1,
  "specialty": "قلب",
  "start_date": "2024-10-15",
  "days": 7
}
```

**Response:**
```json
{
  "success": true,
  "slots": [
    {
      "datetime": "2024-10-15T10:00:00",
      "date": "2024-10-15",
      "time": "10:00 AM",
      "day_name": "Tuesday",
      "doctor_name": "د. أحمد العمري",
      "specialty": "قلب",
      "available": true
    }
  ],
  "total_slots": 42
}
```

### 2. Book Appointment
حجز موعد

**Endpoint:** `POST /appointments/book`

**Request Body:**
```json
{
  "facility_id": 1,
  "patient_name": "أحمد محمد",
  "patient_phone": "0501234567",
  "patient_email": "ahmad@example.com",
  "specialty": "قلب",
  "doctor_name": "د. أحمد العمري",
  "appointment_datetime": "2024-10-15T10:00:00",
  "notes": "فحص دوري"
}
```

**Response:**
```json
{
  "success": true,
  "appointment": {
    "id": 123,
    "facility_name": "مستشفى الملك فهد",
    "patient_name": "أحمد محمد",
    "specialty": "قلب",
    "doctor_name": "د. أحمد العمري",
    "appointment_date": "2024-10-15T10:00:00",
    "status": "pending"
  },
  "confirmation": {
    "success": true,
    "message": "تم إرسال تأكيد الموعد"
  }
}
```

### 3. Get Appointment
الحصول على تفاصيل موعد

**Endpoint:** `GET /appointments/{appointment_id}`

### 4. Confirm Appointment
تأكيد موعد

**Endpoint:** `POST /appointments/{appointment_id}/confirm`

### 5. Cancel Appointment
إلغاء موعد

**Endpoint:** `POST /appointments/{appointment_id}/cancel`

### 6. Get Patient Appointments
مواعيد المريض

**Endpoint:** `GET /appointments/patient/{phone}`

### 7. Get Facility Appointments
مواعيد المنشأة

**Endpoint:** `GET /appointments/facility/{facility_id}`

**Query Parameters:**
- `date`: التاريخ (YYYY-MM-DD)

---

## 🏥 Admin APIs

### 1. Get All Hospitals
الحصول على جميع المستشفيات

**Endpoint:** `GET /admin/hospitals`

### 2. Get Hospital
الحصول على مستشفى

**Endpoint:** `GET /admin/hospitals/{hospital_id}`

### 3. Create Hospital
إنشاء مستشفى

**Endpoint:** `POST /admin/hospitals`

### 4. Update Hospital
تحديث مستشفى

**Endpoint:** `PUT /admin/hospitals/{hospital_id}`

### 5. Delete Hospital
حذف مستشفى

**Endpoint:** `DELETE /admin/hospitals/{hospital_id}`

### 6. Get Statistics
الإحصائيات

**Endpoint:** `GET /admin/statistics`

---

## 💬 Conversation APIs

### 1. Chat
المحادثة

**Endpoint:** `POST /conversation/chat`

**Request Body:**
```json
{
  "message": "عندي ألم في الصدر",
  "conversation_id": "optional-id"
}
```

### 2. Voice to Text
تحويل الصوت إلى نص

**Endpoint:** `POST /conversation/voice-to-text`

### 3. Text to Speech
تحويل النص إلى صوت

**Endpoint:** `POST /conversation/text-to-speech`

---

## 📋 Recommendations APIs

### 1. Get Recommendations
الحصول على التوصيات

**Endpoint:** `GET /recommendations`

### 2. Create Recommendation
إنشاء توصية

**Endpoint:** `POST /recommendations`

### 3. Update Recommendation Status
تحديث حالة التوصية

**Endpoint:** `PUT /recommendations/{recommendation_id}/status`

---

## 🔧 Settings APIs

### 1. Get Settings
الحصول على الإعدادات

**Endpoint:** `GET /settings`

### 2. Update Settings
تحديث الإعدادات

**Endpoint:** `PUT /settings`

---

## Error Responses

### Standard Error Format
```json
{
  "success": false,
  "error": "Error message in Arabic"
}
```

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request
- `404`: Not Found
- `500`: Internal Server Error

---

## Rate Limiting

- **Search APIs**: 100 requests/minute
- **Appointment APIs**: 50 requests/minute
- **Metrics APIs**: 200 requests/minute

---

## Authentication

Currently, the API is open for development. In production:
- Use JWT tokens
- Include `Authorization: Bearer {token}` header
- Tokens expire after 24 hours

---

## CORS

CORS is enabled for all origins in development.

---

**API Version**: 1.0  
**Last Updated**: October 14, 2024

