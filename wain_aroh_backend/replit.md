# Wain Aroh - AI Healthcare Triage System

## Overview

**Wain Aroh** (وين أروح - "Where Should I Go") is an AI-powered healthcare navigation system that helps patients find the most appropriate healthcare facility based on their symptoms. The system uses OpenAI's GPT-4 for intelligent triage and symptom assessment according to the Canadian Triage and Acuity Scale (CTAS).

## Project Information

- **Type**: Flask Web Application (Python 3.11)
- **Frontend**: Pre-built React application (Arabic interface)
- **AI Engine**: OpenAI GPT-4.1-mini for triage, Whisper for voice transcription
- **Database**: SQLite (for user sessions and assessments)
- **Primary Language**: Arabic (RTL interface)

## Recent Changes

### October 13, 2025 - Replit Setup
- Installed Python 3.11 and all required dependencies (Flask, OpenAI, SQLAlchemy)
- Configured Flask app with cache control headers for Replit proxy compatibility
- Created `src/database/` directory for SQLite database
- Set up workflow to run Flask server on port 5000
- Configured deployment settings for autoscale deployment
- Updated .gitignore with Python and Replit-specific entries
- Added OPENAI_API_KEY to Replit Secrets

## Project Architecture

### Backend (Flask)
- **Entry Point**: `src/main.py`
- **API Routes**: 
  - `/api/chat` - Chat with AI assistant
  - `/api/analyze` - Symptom analysis and CTAS assessment
  - `/api/voice/transcribe` - Audio to text transcription
  - `/api/voice/speak` - Text to speech conversion
  - `/api/facilities` - Healthcare facility listings
  - `/api/dashboard/stats` - Dashboard statistics
- **Services**:
  - `src/services/ai_triage.py` - OpenAI integration for triage
  - `src/services/telephony.py` - Phone integration (Twilio)
- **Data**: `src/data/facilities.py` - Healthcare facility data

### Frontend
- Pre-built React application in `src/static/`
- Arabic RTL interface
- Voice chat capability using Web Speech API
- Dashboard for analytics

### Database
- SQLite database at `src/database/app.db`
- Stores user sessions and assessment records
- Managed by Flask-SQLAlchemy

## CTAS Classification System

The system implements the Canadian Triage and Acuity Scale:

| Level | Name (Arabic) | Description | Recommendation |
|-------|---------------|-------------|----------------|
| 1 | إنعاش (Resuscitation) | Life-threatening | Emergency Department |
| 2 | طارئ (Emergent) | Serious, potentially life-threatening | Emergency Department |
| 3 | عاجل (Urgent) | Serious but stable | UCC or Emergency |
| 4 | أقل عجلة (Less Urgent) | Non-urgent but needs care | Clinic or UCC |
| 5 | غير عاجل (Non-Urgent) | Minor issues | Clinic or Virtual OPD |

## Environment Variables

Required secrets (configured in Replit Secrets):
- `OPENAI_API_KEY` - OpenAI API key for GPT-4 and Whisper

Strongly Recommended for Production:
- `SECRET_KEY` - Flask secret key for session signing (a secure random key is auto-generated if not set, but sessions will be invalidated on restart. Set this in Replit Secrets for production!)

Optional:
- `FLASK_DEBUG` - Set to "true" for development mode (defaults to false for security)

Optional (for telephony features):
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `TWILIO_PHONE_NUMBER` - Twilio phone number

## Running the Application

### Development
The Flask development server runs automatically via the configured workflow:
```bash
python src/main.py
```

The server runs on `0.0.0.0:5000` and is accessible through the Replit webview.

### Production Deployment
The application is configured for autoscale deployment using **Gunicorn** (production WSGI server):
```bash
gunicorn --bind=0.0.0.0:5000 --workers=2 src.main:app
```

Click the "Publish" button in Replit to deploy to production. The deployment automatically uses Gunicorn for secure, production-ready serving.

## Key Features

1. **AI-Powered Triage**: Uses GPT-4 to assess symptoms and recommend appropriate care level
2. **Multi-Channel Access**: Web interface, voice chat, and phone call support
3. **Location-Based Recommendations**: Suggests nearest appropriate healthcare facilities
4. **Voice Integration**: Speech-to-text and text-to-speech in Arabic
5. **Admin Dashboard**: Real-time analytics and CTAS distribution
6. **Session Management**: Tracks patient conversations and assessments

## Development Notes

### Replit Configuration
- The Flask app is configured with cache control headers to ensure updates are visible in the Replit iframe proxy
- Port 5000 is used for the frontend (required by Replit)
- Host is set to `0.0.0.0` to accept connections from the Replit proxy

### File Structure
```
.
├── src/
│   ├── main.py              # Flask application entry point
│   ├── routes/              # API route blueprints
│   ├── services/            # Business logic (AI, telephony)
│   ├── models/              # Database models
│   ├── data/                # Static data (facilities)
│   ├── static/              # Frontend build files
│   └── database/            # SQLite database
├── requirements.txt         # Python dependencies
├── README.md               # Project documentation
└── TELEPHONY_SETUP.md      # Telephony integration guide
```

## Troubleshooting

### Application Not Loading
- Check that the workflow is running (should show "Server" as RUNNING)
- Verify OPENAI_API_KEY is set in Replit Secrets
- Check logs for any Python errors

### AI Not Responding
- Verify OPENAI_API_KEY is valid and has credits
- Check OpenAI API status and rate limits
- Review logs for API error messages

### Database Errors
- Ensure `src/database/` directory exists
- Check file permissions for database directory
- SQLite database will be created automatically on first run

## API Integration

The application can be integrated with:
- **Twilio/Vonage**: For phone call support (see TELEPHONY_SETUP.md)
- **SMS Services**: For sending facility information
- **Hospital Information Systems**: Via API endpoints

## Security

- All patient data is handled securely
- API keys stored in Replit Secrets (not in code)
- CORS enabled for API access
- Session data stored in-memory (prototype) or SQLite

## Future Enhancements

- Mobile app (iOS/Android)
- Multi-language support (English, Urdu)
- Integration with HIS systems
- Advanced analytics and ML
- Appointment booking
- Telemedicine integration

## Support

For technical issues or questions:
- Review README.md and TELEPHONY_SETUP.md
- Check GitHub issues: https://github.com/malneami/wain-aroh-prototype
- Contact development team

---

**Last Updated**: October 13, 2025
**Replit Setup**: Complete and Running
