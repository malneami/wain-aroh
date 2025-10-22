# Telephony Integration Setup Guide

## Overview

The **Wain Aroh** system now supports voice call integration, allowing patients to call a fixed phone number and interact with the AI assistant via voice.

## Features

1. **Incoming Call Handling**: Automated greeting in Arabic
2. **Voice Recording**: Records patient responses
3. **Real-time Transcription**: Converts speech to text
4. **AI-Powered Responses**: GPT-4 analyzes symptoms and provides guidance
5. **CTAS Triage**: Automated triage classification
6. **SMS Notifications**: Sends facility information via SMS
7. **Call Recording**: Stores calls for compliance and quality assurance

## Supported Telephony Providers

### 1. Twilio (Recommended)
- **Website**: https://www.twilio.com
- **Arabic TTS Support**: Yes
- **Recording**: Yes
- **Transcription**: Yes (English only, use Whisper for Arabic)

### 2. Vonage (Nexmo)
- **Website**: https://www.vonage.com
- **Arabic TTS Support**: Yes
- **Recording**: Yes
- **Transcription**: Limited

### 3. Plivo
- **Website**: https://www.plivo.com
- **Arabic TTS Support**: Yes
- **Recording**: Yes
- **Transcription**: No (use external service)

## Setup Instructions

### Step 1: Choose a Telephony Provider

We recommend **Twilio** for its comprehensive features and reliability.

### Step 2: Create Account and Get Phone Number

1. Sign up at https://www.twilio.com
2. Purchase a phone number (e.g., Saudi Arabia number)
3. Get your Account SID and Auth Token

### Step 3: Configure Webhooks

Configure the following webhooks in your Twilio console:

| Event | Webhook URL | Method |
|-------|-------------|--------|
| Incoming Call | `https://your-domain.com/api/telephony/incoming-call` | POST |
| Recording Status | `https://your-domain.com/api/telephony/process-recording` | POST |
| Transcription | `https://your-domain.com/api/telephony/transcription` | POST |
| Call Status | `https://your-domain.com/api/telephony/call-status` | POST |

### Step 4: Environment Variables

Add the following to your `.env` file:

```bash
# Telephony Configuration
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=+966xxxxxxxxx
TWILIO_WEBHOOK_BASE_URL=https://your-domain.com

# OpenAI for transcription (Whisper)
OPENAI_API_KEY=your_openai_key_here
```

### Step 5: Install Dependencies

```bash
pip install twilio
```

### Step 6: Test the Integration

1. **Test TwiML Generation**:
   ```bash
   curl https://your-domain.com/api/telephony/test-voice
   ```

2. **Make a Test Call**:
   - Call your Twilio phone number
   - Follow the voice prompts
   - Describe symptoms in Arabic

## API Endpoints

### 1. Incoming Call
**POST** `/api/telephony/incoming-call`

Handles incoming calls and provides initial greeting.

**Request** (from Twilio):
```
CallSid=CAxxxxx
From=+966xxxxxxxxx
To=+966xxxxxxxxx
CallStatus=ringing
```

**Response** (TwiML):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say language="ar-SA" voice="woman">مرحباً بك في خدمة وين أروح</Say>
    <Record maxLength="30" timeout="3" transcribe="true"/>
</Response>
```

### 2. Process Recording
**POST** `/api/telephony/process-recording`

Processes recorded audio and generates AI response.

### 3. Transcription Callback
**POST** `/api/telephony/transcription`

Receives transcription results and processes with AI.

### 4. End Call
**POST** `/api/telephony/end-call`

Ends call and sends SMS with facility information.

**Request Body**:
```json
{
  "call_sid": "CAxxxxx",
  "facility_info": {
    "name": "مستشفى الملك فهد",
    "location": "الرياض، شارع الملك فهد",
    "hours": "24/7",
    "phone": "+966xxxxxxxxx",
    "ctas_level": "CTAS 1"
  }
}
```

## Call Flow

```
1. Patient calls → Incoming Call Webhook
   ↓
2. System greets patient (Arabic TTS)
   ↓
3. Patient describes symptoms (Recording)
   ↓
4. System transcribes audio (Whisper API)
   ↓
5. AI analyzes symptoms (GPT-4)
   ↓
6. System asks follow-up questions
   ↓
7. Repeat steps 3-6 until assessment complete
   ↓
8. System provides CTAS classification
   ↓
9. System recommends facility
   ↓
10. System sends SMS with details
    ↓
11. Call ends
```

## Arabic Voice Support

### Text-to-Speech (TTS)
- **Language Code**: `ar-SA` (Saudi Arabic)
- **Voice**: `woman` or `man`
- **Provider**: Twilio, Google Cloud TTS, Amazon Polly

### Speech-to-Text (STT)
- **Recommended**: OpenAI Whisper API
- **Language**: Arabic (`ar`)
- **Accuracy**: ~95% for clear speech

## SMS Integration

After assessment, the system sends an SMS with:
- Recommended facility name
- Address and directions
- Working hours
- Contact number
- CTAS level

## Call Recording & Compliance

All calls are recorded for:
- Quality assurance
- Training purposes
- Compliance with healthcare regulations
- Dispute resolution

**Storage**: Recordings are stored securely and encrypted.

**Retention**: Configurable (default: 90 days)

**Access**: Restricted to authorized personnel only

## Testing

### Test Scenarios

1. **Emergency Case (CTAS 1)**:
   - Call and say: "أعاني من ألم شديد في الصدر وضيق في التنفس"
   - Expected: Immediate emergency recommendation

2. **Urgent Case (CTAS 2)**:
   - Call and say: "عندي حمى عالية وصداع شديد منذ يومين"
   - Expected: UCC or emergency recommendation

3. **Non-Urgent Case (CTAS 4-5)**:
   - Call and say: "عندي زكام خفيف وسعال"
   - Expected: Clinic or virtual OPD recommendation

### Test Numbers

For testing without charges, use Twilio test credentials:
- Test numbers start with `+15005550006`

## Monitoring & Analytics

Track the following metrics:
- Total calls received
- Average call duration
- CTAS distribution
- Facility recommendations
- Patient satisfaction (post-call survey)

## Troubleshooting

### Issue: Call not connecting
- Check webhook URLs are publicly accessible
- Verify Twilio phone number configuration
- Check firewall/security settings

### Issue: Arabic TTS not working
- Ensure language code is `ar-SA`
- Check voice availability in your region
- Try alternative TTS providers

### Issue: Transcription errors
- Use Whisper API for better Arabic support
- Ensure clear audio quality
- Check for background noise

## Cost Estimation

### Twilio Pricing (Approximate)
- **Phone Number**: $1-5/month
- **Incoming Call**: $0.0085/minute
- **Recording**: $0.0025/minute
- **TTS**: $0.04 per 1000 characters
- **SMS**: $0.05/message

**Example**: 1000 calls/month × 3 min avg = ~$30/month

## Security Considerations

1. **Webhook Authentication**: Validate Twilio signatures
2. **Data Encryption**: Encrypt all recordings and transcriptions
3. **Access Control**: Restrict access to call records
4. **HIPAA Compliance**: Use Twilio's HIPAA-compliant services if required
5. **PII Protection**: Anonymize patient data where possible

## Next Steps

1. Sign up for Twilio account
2. Configure webhooks
3. Test with sample calls
4. Train staff on call monitoring
5. Launch pilot program
6. Collect feedback and iterate

## Support

For technical support:
- **Email**: support@wain-aroh.com
- **Phone**: +966 xxx xxx xxxx
- **Documentation**: https://docs.wain-aroh.com

## Integration with 937 Service

To integrate with Saudi Arabia's 937 health service:

1. Contact Ministry of Health (MOH)
2. Request API access for 937 integration
3. Configure call forwarding or API webhooks
4. Test with MOH approval
5. Launch in production

---

**Last Updated**: October 2025
**Version**: 1.0.0

