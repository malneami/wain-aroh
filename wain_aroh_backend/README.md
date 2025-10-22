# وين أروح (Wain Aroh) - AI-Powered Healthcare Navigation System

## Overview

**Wain Aroh** (Where Should I Go) is an intelligent healthcare navigation system that helps patients find the most appropriate healthcare facility based on their symptoms. The system uses AI-powered triage to assess patient conditions and recommend whether they should visit an Emergency Department, Urgent Care Center (UCC), Clinic, or use Virtual OPD services.

## Key Features

### 1. Multi-Channel Access
- **Web Interface**: Responsive web application with chat interface
- **Voice Chat**: Browser-based voice interaction
- **Phone Calls**: Call a fixed number (e.g., 937) for voice assistance
- **Mobile-Friendly**: Optimized for smartphones and tablets

### 2. AI-Powered Triage
- **CTAS Classification**: Canadian Triage and Acuity Scale (Levels 1-5)
- **Symptom Analysis**: Natural language understanding in Arabic
- **Smart Recommendations**: Location-based facility suggestions
- **Follow-up Questions**: Intelligent conversation flow

### 3. Voice Integration
- **Speech-to-Text**: Convert patient voice to text
- **Text-to-Speech**: AI responds with natural Arabic voice
- **Call Recording**: All calls recorded for quality assurance
- **Real-time Transcription**: Automatic transcription of conversations

### 4. Facility Recommendation
- **Location-Based**: Find nearest appropriate facility
- **Working Hours**: Real-time availability information
- **Facility Details**: Name, address, phone, services
- **SMS Notifications**: Send facility details via SMS

### 5. Admin Dashboard
- **Real-time Analytics**: Monitor system usage and performance
- **CTAS Distribution**: Visualize triage levels
- **Call Records**: Access call recordings and transcriptions
- **KPI Tracking**: Average assessment time, accuracy, satisfaction

## System Architecture

```
┌─────────────────┐
│   Patient       │
│  (Web/Phone)    │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Frontend (React)              │
│   - Chat Interface              │
│   - Voice Recording             │
│   - Dashboard                   │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│   Backend API (Flask)           │
│   - Chat Endpoints              │
│   - Telephony Webhooks          │
│   - Triage Logic                │
└────────┬────────────────────────┘
         │
         ├──────────┬──────────────┬─────────────┐
         ▼          ▼              ▼             ▼
    ┌────────┐ ┌────────┐    ┌─────────┐  ┌──────────┐
    │ OpenAI │ │Telephony│   │Database │  │  SMS     │
    │  GPT-4 │ │Provider │   │ SQLite  │  │ Service  │
    │ Whisper│ │(Twilio) │   │         │  │          │
    └────────┘ └────────┘    └─────────┘  └──────────┘
```

## Technology Stack

### Frontend
- **Framework**: React 18 with Vite
- **UI Library**: Tailwind CSS + shadcn/ui
- **State Management**: React Hooks
- **HTTP Client**: Fetch API
- **Voice**: Web Speech API

### Backend
- **Framework**: Flask (Python 3.11)
- **AI/LLM**: OpenAI GPT-4.1-mini
- **Speech**: OpenAI Whisper API
- **Database**: SQLite
- **Telephony**: Twilio/Vonage (configurable)

### Deployment
- **Platform**: Cloud-based (supports any Python hosting)
- **Web Server**: Gunicorn/uWSGI
- **Reverse Proxy**: Nginx (recommended)

## Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- OpenAI API Key
- Twilio Account (for phone integration)

### Backend Setup

```bash
# Clone repository
git clone https://github.com/malneami/wain-aroh-prototype.git
cd wain-aroh-prototype

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY=your_openai_key_here
export TWILIO_ACCOUNT_SID=your_twilio_sid
export TWILIO_AUTH_TOKEN=your_twilio_token

# Run development server
python src/main.py
```

### Frontend Setup (for development)

```bash
# Navigate to frontend directory
cd wain_aroh_frontend

# Install dependencies
pnpm install

# Run development server
pnpm run dev
```

### Production Deployment

```bash
# Build frontend
cd wain_aroh_frontend
pnpm run build

# Copy to backend static folder
cp -r dist/* ../wain_aroh_backend/src/static/

# Run backend in production mode
cd ../wain_aroh_backend
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-...

# Telephony Configuration (Optional)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+966xxxxxxxxx

# Application Settings
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/app.db

# SMS Configuration (Optional)
SMS_PROVIDER=twilio
SMS_FROM_NUMBER=+966xxxxxxxxx
```

### Facility Data

Edit `src/data/facilities.py` to add your healthcare facilities:

```python
FACILITIES = [
    {
        "id": 1,
        "name": "مستشفى الملك فهد",
        "type": "emergency",
        "location": "الرياض، شارع الملك فهد",
        "coordinates": {"lat": 24.7136, "lng": 46.6753},
        "phone": "+966xxxxxxxxx",
        "hours": "24/7",
        "services": ["emergency", "ucc", "clinic"]
    },
    # Add more facilities...
]
```

## Usage

### Web Interface

1. Visit the application URL
2. Click "ابدأ المحادثة الآن" (Start Chat Now)
3. Type or speak your symptoms
4. Answer follow-up questions
5. Receive facility recommendation
6. Get SMS with details

### Phone Call

1. Call the configured phone number (e.g., 937)
2. Listen to the greeting in Arabic
3. Describe your symptoms after the beep
4. Answer follow-up questions
5. Receive facility recommendation via voice
6. Get SMS with details

### Admin Dashboard

1. Navigate to `/dashboard`
2. View real-time statistics
3. Monitor CTAS distribution
4. Access call recordings
5. Export reports

## API Documentation

### Chat Endpoint

**POST** `/api/chat`

```json
{
  "message": "أعاني من ألم في الصدر",
  "conversation_history": []
}
```

**Response**:
```json
{
  "response": "هل الألم شديد؟...",
  "assessment": null
}
```

### Triage Endpoint

**POST** `/api/triage`

```json
{
  "symptoms": "ألم في الصدر، ضيق تنفس، دوخة",
  "conversation": [...]
}
```

**Response**:
```json
{
  "ctas_level": 1,
  "severity": "critical",
  "recommendation": "emergency",
  "facility": {...}
}
```

### Telephony Webhooks

See `TELEPHONY_SETUP.md` for detailed telephony API documentation.

## CTAS Classification

| Level | Name | Description | Response Time | Recommendation |
|-------|------|-------------|---------------|----------------|
| 1 | إنعاش (Resuscitation) | Life-threatening | Immediate | Emergency Department |
| 2 | طارئ (Emergent) | Serious, potentially life-threatening | 15 minutes | Emergency Department |
| 3 | عاجل (Urgent) | Serious but stable | 30 minutes | UCC or Emergency |
| 4 | أقل عجلة (Less Urgent) | Non-urgent but needs care | 60 minutes | Clinic or UCC |
| 5 | غير عاجل (Non-Urgent) | Minor issues | 120 minutes | Clinic or Virtual OPD |

## Sample Conversations

### Example 1: Emergency Case

**Patient**: "أعاني من ألم شديد في الصدر وضيق في التنفس"

**AI**: "هذا الأمر يبدو خطيراً. هل الألم بدأ فجأة؟ وهل تشعر بألم في الذراع أو الفك؟"

**Patient**: "نعم، بدأ فجأة منذ نصف ساعة وأشعر بألم في الذراع الأيسر"

**AI**: "بناءً على الأعراض، حالتك تصنف كـ CTAS 1 (إنعاش). يجب التوجه فوراً إلى قسم الطوارئ. أقرب مستشفى هو مستشفى الملك فهد..."

### Example 2: Non-Urgent Case

**Patient**: "عندي زكام وسعال خفيف"

**AI**: "متى بدأت الأعراض؟ وهل لديك حمى؟"

**Patient**: "منذ يومين، وليس لدي حمى"

**AI**: "حالتك تصنف كـ CTAS 5 (غير عاجل). يمكنك حجز موعد في العيادة أو استشارة طبيب عبر الإنترنت..."

## Monitoring & Analytics

### Key Performance Indicators (KPIs)

- **Total Sessions**: Number of patient interactions
- **Completed Assessments**: Successful triage completions
- **Average Assessment Time**: Time to complete triage
- **Triage Accuracy**: Validation against actual diagnoses
- **Patient Satisfaction**: Post-interaction surveys
- **System Uptime**: Service availability

### Dashboard Metrics

- CTAS level distribution
- Care type recommendations (Emergency/UCC/Clinic/Virtual)
- Peak usage times
- Geographic distribution
- Call duration statistics
- Transcription accuracy

## Security & Compliance

### Data Protection
- All patient data encrypted at rest and in transit
- HIPAA-compliant storage (if applicable)
- Regular security audits
- Access control and authentication

### Privacy
- No personally identifiable information (PII) stored without consent
- Call recordings anonymized
- Data retention policies enforced
- GDPR/PDPL compliance

### Audit Trail
- All interactions logged
- Call recordings stored securely
- Transcriptions archived
- Access logs maintained

## Troubleshooting

### Common Issues

**Issue**: AI not responding
- Check OpenAI API key is valid
- Verify internet connectivity
- Check API rate limits

**Issue**: Voice not working
- Enable microphone permissions
- Check browser compatibility (Chrome/Edge recommended)
- Verify HTTPS connection

**Issue**: Phone calls not connecting
- Verify Twilio configuration
- Check webhook URLs are accessible
- Review Twilio console logs

## Support & Contact

- **GitHub**: https://github.com/malneami/wain-aroh-prototype
- **Documentation**: See `TELEPHONY_SETUP.md` for phone integration
- **Issues**: Report bugs on GitHub Issues

## Roadmap

### Phase 1 (Current)
- ✅ Web chat interface
- ✅ AI-powered triage
- ✅ Voice interaction (browser)
- ✅ Phone call integration
- ✅ Admin dashboard

### Phase 2 (Planned)
- [ ] Mobile app (iOS/Android)
- [ ] Multi-language support (English, Urdu)
- [ ] Integration with HIS systems
- [ ] Advanced analytics and ML
- [ ] Appointment booking
- [ ] Telemedicine integration

### Phase 3 (Future)
- [ ] Video consultation
- [ ] Prescription management
- [ ] Follow-up reminders
- [ ] Patient portal
- [ ] Provider dashboard

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is proprietary software. All rights reserved.

## Acknowledgments

- OpenAI for GPT-4 and Whisper APIs
- Twilio for telephony services
- Saudi Ministry of Health for 937 service inspiration

---

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Developed by**: Healthcare Innovation Team

