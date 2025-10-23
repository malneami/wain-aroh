# 🚀 دليل النشر الدائم | Permanent Deployment Guide

## خيارات النشر | Deployment Options

### 1. 🌐 Render.com (موصى به | Recommended)

#### الخطوات | Steps:

1. **إنشاء حساب على Render**
   - اذهب إلى: https://render.com
   - سجل دخول باستخدام GitHub

2. **إنشاء Web Service جديد**
   - اضغط "New +" → "Web Service"
   - اختر repository: `malneami/wain-aroh`
   - الإعدادات:
     - **Name**: `wain-aroh`
     - **Region**: Oregon (US West)
     - **Branch**: `main`
     - **Runtime**: Python 3
     - **Build Command**:
       ```bash
       cd wain_aroh_backend && pip install -r requirements.txt && python populate_hospitals.py && cd ../wain_aroh_frontend && npm install -g pnpm && pnpm install && pnpm run build && cp -r dist/* ../wain_aroh_backend/static/
       ```
     - **Start Command**:
       ```bash
       cd wain_aroh_backend && gunicorn --chdir src main:app --bind 0.0.0.0:$PORT
       ```

3. **إضافة Environment Variables**
   - `OPENAI_API_KEY`: مفتاح OpenAI الخاص بك
   - `PYTHON_VERSION`: 3.11.0

4. **النشر**
   - اضغط "Create Web Service"
   - انتظر حتى يكتمل البناء (5-10 دقائق)
   - ستحصل على رابط دائم مثل: `https://wain-aroh.onrender.com`

---

### 2. 🔷 Railway.app

#### الخطوات:

1. اذهب إلى: https://railway.app
2. سجل دخول بـ GitHub
3. "New Project" → "Deploy from GitHub repo"
4. اختر `malneami/wain-aroh`
5. Railway سيكتشف التطبيق تلقائياً
6. أضف Environment Variables:
   - `OPENAI_API_KEY`
7. انتظر النشر

---

### 3. ☁️ Vercel (Frontend فقط)

للنشر السريع لـ Frontend فقط:

```bash
cd wain_aroh_frontend
npm install -g vercel
vercel deploy
```

ملاحظة: ستحتاج لنشر Backend منفصل.

---

### 4. 🐳 Docker Deployment

#### إنشاء Dockerfile:

**Backend Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY wain_aroh_backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wain_aroh_backend/ .

RUN python populate_hospitals.py

EXPOSE 5000

CMD ["gunicorn", "--chdir", "src", "main:app", "--bind", "0.0.0.0:5000"]
```

#### تشغيل Docker:
```bash
docker build -t wain-aroh .
docker run -p 5000:5000 -e OPENAI_API_KEY=your_key wain-aroh
```

---

### 5. 🌍 Heroku

#### الخطوات:

1. تثبيت Heroku CLI:
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. تسجيل الدخول:
```bash
heroku login
```

3. إنشاء تطبيق:
```bash
cd wain_aroh_backend
heroku create wain-aroh
```

4. إضافة Environment Variables:
```bash
heroku config:set OPENAI_API_KEY=your_key
```

5. النشر:
```bash
git push heroku main
```

---

## 🔧 إعدادات مهمة | Important Settings

### Environment Variables المطلوبة:

```env
OPENAI_API_KEY=sk-...
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///wain_aroh.db
```

### Port Configuration:

التطبيق يستخدم `PORT` من environment variable:
```python
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)
```

---

## 📊 مقارنة الخدمات | Services Comparison

| الخدمة | مجاني | سهولة | سرعة | قاعدة بيانات |
|--------|-------|-------|------|--------------|
| **Render** | ✅ | ⭐⭐⭐⭐⭐ | سريع | SQLite |
| **Railway** | ✅ (محدود) | ⭐⭐⭐⭐ | سريع جداً | SQLite/PostgreSQL |
| **Vercel** | ✅ | ⭐⭐⭐⭐⭐ | سريع جداً | خارجي فقط |
| **Heroku** | ❌ (مدفوع) | ⭐⭐⭐ | متوسط | PostgreSQL |
| **Docker** | يعتمد | ⭐⭐⭐ | يعتمد | أي نوع |

---

## ✅ التوصية | Recommendation

**للنشر السريع والمجاني**: استخدم **Render.com**

### المميزات:
- ✅ مجاني بالكامل
- ✅ نشر تلقائي من GitHub
- ✅ SSL مجاني
- ✅ دعم Python و Node.js
- ✅ قاعدة بيانات SQLite تعمل
- ✅ رابط دائم

### العيوب:
- ⚠️ يتوقف بعد 15 دقيقة من عدم النشاط (Free tier)
- ⚠️ يستغرق 30-60 ثانية للتشغيل بعد التوقف

---

## 🔗 الروابط بعد النشر

بعد النشر الناجح، ستحصل على:

- **الموقع الرئيسي**: `https://your-app.onrender.com`
- **المحادثة**: `https://your-app.onrender.com/chat`
- **البحث**: `https://your-app.onrender.com/search`
- **API**: `https://your-app.onrender.com/api/`

---

## 🆘 حل المشاكل | Troubleshooting

### المشكلة: Build يفشل
**الحل**: تأكد من وجود جميع الملفات:
- `requirements.txt`
- `Procfile`
- `runtime.txt`

### المشكلة: قاعدة البيانات فارغة
**الحل**: تأكد من تشغيل `populate_hospitals.py` في Build Command

### المشكلة: OPENAI_API_KEY غير موجود
**الحل**: أضف Environment Variable في إعدادات الخدمة

---

## 📝 ملاحظات | Notes

1. **قاعدة البيانات**: SQLite تعمل على Render لكن البيانات قد تُفقد عند إعادة النشر. للإنتاج الحقيقي، استخدم PostgreSQL.

2. **الملفات الكبيرة**: ملف الصوت (60MB) قد يبطئ البناء. يمكن استبعاده إذا لم تحتج للميزة الصوتية.

3. **التحديثات التلقائية**: عند push إلى GitHub، سيتم إعادة النشر تلقائياً.

---

## 🎉 النشر الناجح

بعد النشر الناجح:
1. ✅ افتح الرابط
2. ✅ جرب المحادثة
3. ✅ جرب البحث
4. ✅ تأكد من عمل جميع الميزات

---

**للدعم**: افتح Issue على GitHub
**للتحديثات**: راقب Repository

**حظاً موفقاً! 🚀**

