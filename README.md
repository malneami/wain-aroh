# 🏥 وين أروح - نظام التوجيه الذكي للرعاية الصحية

<div dir="rtl">

## نظرة عامة

**وين أروح** هو نظام ذكي متكامل لتوجيه المرضى إلى المنشآت الصحية المناسبة في الرياض، يجمع بين الذكاء الاصطناعي والبحث المتقدم والتقييمات من مواقع التواصل الاجتماعي.

</div>

---

## ✨ Features | الميزات

### 🤖 AI-Powered Triage System | نظام التصنيف الذكي
- Voice and text conversation with AI | محادثة صوتية ونصية مع الذكاء الاصطناعي
- Symptom analysis and CTAS assessment | تحليل الأعراض وتقييم CTAS
- Smart recommendations based on severity | توصيات ذكية حسب الخطورة
- Arabic language support | دعم كامل للغة العربية

### 🔍 Advanced Search System | نظام البحث المتقدم
- **Location-based search** | البحث حسب الموقع الجغرافي
- **Smart ranking algorithm** | خوارزمية ترتيب ذكية
- Multiple filters (specialty, distance, rating) | فلاتر متعددة
- Real-time availability | التوفر الفوري

### ⭐ Social Media Ratings | تقييمات مواقع التواصل
- Aggregated ratings from 4 platforms | تجميع التقييمات من 4 منصات
  - Google Maps
  - Twitter
  - Instagram
  - Facebook
- Sentiment analysis | تحليل المشاعر
- Popular keywords | الكلمات المفتاحية الشائعة

### 📊 Performance Metrics | مقاييس الأداء
- 8 Key Performance Indicators (KPIs) | 8 مؤشرات أداء رئيسية
- Real-time facility status | الحالة الفورية للمنشآت
- Comprehensive dashboards | لوحات تحكم شاملة

### 📅 Appointment Booking | حجز المواعيد
- Direct booking from search results | حجز مباشر من نتائج البحث
- Available slots display | عرض المواعيد المتاحة
- Instant confirmation | تأكيد فوري

---

## 🗄️ Database | قاعدة البيانات

<div dir="rtl">

النظام يحتوي على **10 منشآت طبية** حقيقية في الرياض:
- **7 مستشفيات** مع خدمات طوارئ 24/7
- **3 عيادات** ومراكز رعاية عاجلة

</div>

---

## 🚀 Quick Start | البدء السريع

### Prerequisites | المتطلبات
```bash
- Python 3.11+
- Node.js 22+
- pnpm
```

### Backend Setup | إعداد Backend
```bash
cd wain_aroh_backend
pip install -r requirements.txt
python populate_hospitals.py  # Add sample data
python src/main.py
```

### Frontend Setup | إعداد Frontend
```bash
cd wain_aroh_frontend
pnpm install
pnpm run dev
```

### Build for Production | البناء للإنتاج
```bash
cd wain_aroh_frontend
pnpm run build
cp -r dist/* ../wain_aroh_backend/static/
```

---

## 📁 Project Structure | هيكل المشروع

```
wain-aroh/
├── wain_aroh_backend/          # Flask Backend
│   ├── src/
│   │   ├── models/             # Database models
│   │   ├── services/           # Business logic
│   │   ├── routes/             # API endpoints
│   │   └── main.py             # Main application
│   ├── populate_hospitals.py   # Database seeding
│   └── wain_aroh.db            # SQLite database
│
├── wain_aroh_frontend/         # React Frontend
│   ├── src/
│   │   ├── pages/              # Page components
│   │   ├── components/         # Reusable components
│   │   └── App.jsx             # Main app
│   └── dist/                   # Built files
│
└── Documentation/              # Full documentation
    ├── FINAL_SYSTEM_DOCUMENTATION.md
    ├── ADVANCED_SEARCH_GUIDE.md
    ├── API_DOCUMENTATION.md
    └── README_ADVANCED_SEARCH.md
```

---

## 🔌 API Endpoints

### Conversation API
```
POST /api/conversation/start          # Start new conversation
POST /api/conversation/message         # Send message
POST /api/conversation/location        # Share location
POST /api/conversation/booking/search  # Search appointments
POST /api/conversation/booking/confirm # Confirm booking
```

### Search API
```
POST /api/search/facilities            # Search facilities
GET  /api/search/facilities/:id        # Get facility details
POST /api/search/facilities/compare    # Compare facilities
GET  /api/search/filters               # Get available filters
GET  /api/search/specialties           # Get specialties
```

### Metrics API
```
GET  /api/metrics/facility/:id         # Get facility metrics
POST /api/metrics/facility/:id/update  # Update metrics
GET  /api/metrics/comparison           # Compare metrics
GET  /api/metrics/dashboard            # Metrics dashboard
```

### Appointments API
```
POST /api/appointments/search          # Search appointments
POST /api/appointments/book            # Book appointment
GET  /api/appointments/:id             # Get appointment
PUT  /api/appointments/:id             # Update appointment
DELETE /api/appointments/:id           # Cancel appointment
```

---

## 🎯 Smart Ranking Algorithm | خوارزمية الترتيب الذكية

<div dir="rtl">

**حساب درجة الصلة (0-100):**

1. **تطابق التخصصات** (30 نقطة)
2. **القرب الجغرافي** (25 نقطة)
3. **التقييم** (20 نقطة)
4. **التوفر** (15 نقطة)
5. **وقت الانتظار** (10 نقاط)

</div>

---

## 🛠️ Tech Stack | التقنيات المستخدمة

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **OpenAI API** - AI conversations
- **Python 3.11**

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **React Router** - Navigation
- **Lucide Icons** - Icons

### Database
- **SQLite** - Database

---

## 📖 Documentation | التوثيق

<div dir="rtl">

للحصول على التوثيق الكامل، راجع:
- **التوثيق الشامل**: `FINAL_SYSTEM_DOCUMENTATION.md`
- **دليل البحث المتقدم**: `ADVANCED_SEARCH_GUIDE.md`
- **توثيق API**: `API_DOCUMENTATION.md`
- **دليل البدء السريع**: `README_ADVANCED_SEARCH.md`

</div>

---

## 🌟 Key Features Highlights | أبرز الميزات

✅ **Smart Conversation Flow** | تدفق محادثة ذكي  
✅ **Location-Based Search** | بحث حسب الموقع  
✅ **Social Media Ratings** | تقييمات مواقع التواصل  
✅ **Real-time Availability** | التوفر الفوري  
✅ **Performance Metrics** | مقاييس الأداء  
✅ **Direct Booking** | حجز مباشر  
✅ **Fully Arabic Interface** | واجهة عربية بالكامل  
✅ **Responsive Design** | تصميم متجاوب  

---

## 📊 Statistics | الإحصائيات

- **10** Medical facilities | منشآت طبية
- **7** Emergency hospitals | مستشفيات طوارئ
- **3** Urgent care clinics | عيادات رعاية عاجلة
- **4** Social media platforms | منصات تواصل
- **8** Performance KPIs | مؤشرات أداء
- **5** Ranking options | خيارات ترتيب

---

## 🤝 Contributing | المساهمة

Contributions are welcome! Please feel free to submit a Pull Request.

<div dir="rtl">
المساهمات مرحب بها! لا تتردد في إرسال Pull Request.
</div>

---

## 📄 License | الترخيص

This project is licensed under the MIT License.

---

## 👥 Authors | المطورون

**Wain Aroh Team** | فريق وين أروح

---

## 📞 Support | الدعم

For support and inquiries, please open an issue on GitHub.

<div dir="rtl">
للدعم والاستفسارات، يرجى فتح issue على GitHub.
</div>

---

<div align="center">

**Made with ❤️ for better healthcare navigation**

**صُنع بـ ❤️ لتوجيه صحي أفضل**

</div>

