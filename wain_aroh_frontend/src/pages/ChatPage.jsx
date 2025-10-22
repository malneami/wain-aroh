import { useState, useEffect, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card } from '@/components/ui/card';
import { Mic, Send, MapPin, Loader2, Paperclip, X, Volume2, VolumeX, Navigation, Phone, Calendar, Map } from 'lucide-react';

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [sessionId, setSessionId] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [location, setLocation] = useState(null);
  const [locationDetected, setLocationDetected] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentRecommendation, setCurrentRecommendation] = useState(null);
  const messagesEndRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const fileInputRef = useRef(null);
  const audioRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    startConversation();
    requestLocationPermission();
  }, []);

  const startConversation = async () => {
    try {
      const response = await fetch('/api/conversation/start', { method: 'POST' });
      const data = await response.json();
      setSessionId(data.session_id);
      const welcomeMsg = { role: 'assistant', content: data.message };
      setMessages([welcomeMsg]);
      
      if (voiceEnabled) {
        await speakText(data.message);
      }
    } catch (error) {
      console.error('Error:', error);
      const fallbackMsg = { role: 'assistant', content: 'مرحباً بك في خدمة "وين أروح" 👋\n\nكيف يمكنني مساعدتك؟' };
      setMessages([fallbackMsg]);
      if (voiceEnabled) await speakText(fallbackMsg.content);
    }
  };

  const speakText = async (text) => {
    if (!voiceEnabled || !text) return;
    
    try {
      setIsPlaying(true);
      
      const response = await fetch('/api/voice/text-to-speech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          text: text,
          voice: 'nova',
          speed: 1.0 
        })
      });
      
      if (!response.ok) {
        console.error('TTS failed');
        setIsPlaying(false);
        return;
      }
      
      const audioBlob = await response.blob();
      const audioUrl = URL.createObjectURL(audioBlob);
      
      const audio = new Audio(audioUrl);
      audioRef.current = audio;
      
      audio.onended = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };
      
      audio.onerror = () => {
        setIsPlaying(false);
        URL.revokeObjectURL(audioUrl);
      };
      
      await audio.play();
      
    } catch (error) {
      console.error('Error playing speech:', error);
      setIsPlaying(false);
    }
  };

  const stopSpeaking = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
      setIsPlaying(false);
    }
  };

  const toggleVoice = () => {
    if (voiceEnabled) {
      stopSpeaking();
    }
    setVoiceEnabled(!voiceEnabled);
  };

  const requestLocationPermission = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const locationData = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          };
          setLocation(locationData);
          setLocationDetected(true);
        },
        (error) => console.log('Location unavailable:', error)
      );
    }
  };

  const shareLocation = async () => {
    if (location) {
      await sendLocationToServer(location);
    } else {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          async (position) => {
            const locationData = {
              latitude: position.coords.latitude,
              longitude: position.coords.longitude
            };
            setLocation(locationData);
            setLocationDetected(true);
            await sendLocationToServer(locationData);
          },
          (error) => {
            const errorMsg = { role: 'system', content: '❌ لم نتمكن من الحصول على موقعك. يمكنك إخباري في أي حي أنت؟' };
            setMessages(prev => [...prev, errorMsg]);
          }
        );
      }
    }
  };

  const sendLocationToServer = async (locationData) => {
    if (!sessionId) return;
    try {
      setMessages(prev => [...prev, { role: 'user', content: '📍 [تم مشاركة الموقع]' }]);
      const response = await fetch('/api/conversation/location', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, gps_data: locationData })
      });
      const data = await response.json();
      if (data.success) {
        if (data.message) {
          setMessages(prev => [...prev, { role: 'assistant', content: data.message }]);
          if (voiceEnabled) await speakText(data.message);
        }
        if (data.facility_message) {
          setMessages(prev => [...prev, { role: 'assistant', content: data.facility_message }]);
          if (voiceEnabled) await speakText(data.facility_message);
        }
        if (data.recommendation) {
          setCurrentRecommendation(data.recommendation);
        }
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        const errorMsg = { role: 'system', content: '❌ حجم الملف كبير جداً. الحد الأقصى 10 ميجابايت.' };
        setMessages(prev => [...prev, errorMsg]);
        if (voiceEnabled) speakText(errorMsg.content);
        return;
      }
      setSelectedFile(file);
    }
  };

  const uploadFile = async () => {
    if (!selectedFile || !sessionId) return;
    setIsProcessing(true);
    try {
      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('session_id', sessionId);
      formData.append('context', messages.slice(-3).map(m => m.content).join('\n'));

      setMessages(prev => [...prev, { role: 'user', content: `📎 [تم رفع ملف: ${selectedFile.name}]` }]);

      const response = await fetch('/api/conversation/upload', { method: 'POST', body: formData });
      const data = await response.json();

      if (data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.message }]);
        if (voiceEnabled) await speakText(data.message);
        setSelectedFile(null);
      } else {
        const errorMsg = { role: 'system', content: `❌ ${data.error || 'فشل تحليل الملف'}` };
        setMessages(prev => [...prev, errorMsg]);
        if (voiceEnabled) await speakText(errorMsg.content);
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMsg = { role: 'system', content: '❌ حدث خطأ أثناء رفع الملف' };
      setMessages(prev => [...prev, errorMsg]);
      if (voiceEnabled) await speakText(errorMsg.content);
    } finally {
      setIsProcessing(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || !sessionId) return;
    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsProcessing(true);
    try {
      const response = await fetch('/api/conversation/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message: userMessage })
      });
      const data = await response.json();
      if (data.success) {
        if (data.location_confirmation) {
          const locMsg = { role: 'system', content: data.location_confirmation };
          setMessages(prev => [...prev, locMsg]);
          if (voiceEnabled) await speakText(locMsg.content);
        }
        if (data.message) {
          setMessages(prev => [...prev, { role: 'assistant', content: data.message }]);
          if (voiceEnabled) await speakText(data.message);
        }
        if (data.facility_message) {
          setMessages(prev => [...prev, { role: 'assistant', content: data.facility_message }]);
          if (voiceEnabled) await speakText(data.facility_message);
        }
        if (data.recommendation) {
          setCurrentRecommendation(data.recommendation);
        }
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: { echoCancellation: true, noiseSuppression: true, sampleRate: 44100 } 
      });
      const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) audioChunksRef.current.push(event.data);
      };
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        await processAudioRecording(audioBlob);
        stream.getTracks().forEach(track => track.stop());
      };
      mediaRecorder.start();
      setIsRecording(true);
      setMessages(prev => [...prev, { role: 'system', content: '🎤 جاري التسجيل...' }]);
    } catch (error) {
      console.error('Error:', error);
      const errorMsg = { role: 'system', content: '❌ لم نتمكن من الوصول إلى الميكروفون' };
      setMessages(prev => [...prev, errorMsg]);
      if (voiceEnabled) await speakText(errorMsg.content);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const processAudioRecording = async (audioBlob) => {
    setIsProcessing(true);
    try {
      const formData = new FormData();
      formData.append('audio', audioBlob, 'recording.webm');
      formData.append('session_id', sessionId);
      const response = await fetch('/api/voice/transcribe', { method: 'POST', body: formData });
      const data = await response.json();
      if (data.success && data.transcription) {
        setMessages(prev => [...prev, { role: 'user', content: data.transcription }]);
        const messageResponse = await fetch('/api/conversation/message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ session_id: sessionId, message: data.transcription })
        });
        const messageData = await messageResponse.json();
        if (messageData.success) {
          if (messageData.location_confirmation) {
            const locMsg = { role: 'system', content: messageData.location_confirmation };
            setMessages(prev => [...prev, locMsg]);
            if (voiceEnabled) await speakText(locMsg.content);
          }
          if (messageData.message) {
            setMessages(prev => [...prev, { role: 'assistant', content: messageData.message }]);
            if (voiceEnabled) await speakText(messageData.message);
          }
          if (messageData.facility_message) {
            setMessages(prev => [...prev, { role: 'assistant', content: messageData.facility_message }]);
            if (voiceEnabled) await speakText(messageData.facility_message);
          }
          if (messageData.recommendation) {
            setCurrentRecommendation(messageData.recommendation);
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleMicClick = () => {
    if (isRecording) stopRecording();
    else startRecording();
  };

  const handleActionClick = (action) => {
    if (!currentRecommendation) return;
    
    switch(action) {
      case 'navigate_ed':
        window.open(`https://www.google.com/maps/dir/?api=1&destination=${currentRecommendation.facility.coordinates.latitude},${currentRecommendation.facility.coordinates.longitude}`, '_blank');
        break;
      case 'navigate_ucc':
        window.open(`https://www.google.com/maps/dir/?api=1&destination=${currentRecommendation.facility.coordinates.latitude},${currentRecommendation.facility.coordinates.longitude}`, '_blank');
        break;
      case 'call_ambulance':
        window.location.href = 'tel:997';
        break;
      case 'call_facility':
        window.location.href = `tel:${currentRecommendation.facility.phone}`;
        break;
      case 'book_appointment':
        // Trigger booking flow
        setInput('أريد حجز موعد');
        sendMessage();
        break;
    }
  };

  const renderActionButtons = () => {
    if (!currentRecommendation) return null;
    
    const { ctas_level, care_type, facility } = currentRecommendation;
    
    return (
      <div className="mt-4 p-4 bg-white rounded-lg border-2 border-blue-200">
        <h3 className="text-lg font-bold text-gray-800 mb-3 text-center">⚡ إجراءات سريعة</h3>
        <div className="grid grid-cols-2 gap-2">
          {(ctas_level === 1 || ctas_level === 2) && (
            <>
              <Button onClick={() => handleActionClick('navigate_ed')} className="bg-red-600 hover:bg-red-700 text-white gap-2">
                <Navigation className="w-4 h-4" />
                توجيه للطوارئ
              </Button>
              <Button onClick={() => handleActionClick('call_ambulance')} className="bg-red-500 hover:bg-red-600 text-white gap-2">
                <Phone className="w-4 h-4" />
                اتصال بالإسعاف
              </Button>
            </>
          )}
          {ctas_level === 3 && care_type === 'UCC' && (
            <Button onClick={() => handleActionClick('navigate_ucc')} className="bg-orange-600 hover:bg-orange-700 text-white gap-2">
              <Navigation className="w-4 h-4" />
              توجيه للرعاية العاجلة
            </Button>
          )}
          {(ctas_level === 4 || ctas_level === 5) && (
            <Button onClick={() => handleActionClick('book_appointment')} className="bg-green-600 hover:bg-green-700 text-white gap-2">
              <Calendar className="w-4 h-4" />
              حجز موعد
            </Button>
          )}
          <Button onClick={() => handleActionClick('call_facility')} variant="outline" className="gap-2">
            <Phone className="w-4 h-4" />
            اتصال بالمركز
          </Button>
          <Button onClick={() => window.open(`https://www.google.com/maps/search/?api=1&query=${facility.coordinates.latitude},${facility.coordinates.longitude}`, '_blank')} variant="outline" className="gap-2">
            <Map className="w-4 h-4" />
            عرض على الخريطة
          </Button>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-green-50" dir="rtl">
      <div className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-green-500 rounded-xl flex items-center justify-center">
              <span className="text-white text-2xl">🏥</span>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-800">وين أروح؟</h1>
              <p className="text-sm text-gray-600">التوجيه الذكي للرعاية العاجلة</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            {locationDetected && (
              <div className="flex items-center gap-2 text-sm text-green-600">
                <MapPin className="w-4 h-4" />
                <span>تم تحديد الموقع</span>
              </div>
            )}
            <Button
              onClick={toggleVoice}
              variant="outline"
              size="sm"
              className={`gap-2 ${voiceEnabled ? 'bg-green-50 border-green-300' : 'bg-gray-50'}`}
            >
              {voiceEnabled ? <Volume2 className="w-4 h-4 text-green-600" /> : <VolumeX className="w-4 h-4 text-gray-600" />}
              <span className="text-xs">{voiceEnabled ? 'الصوت مفعّل' : 'الصوت متوقف'}</span>
            </Button>
          </div>
        </div>
      </div>
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <Card className="h-[calc(100vh-200px)] flex flex-col">
          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {messages.map((msg, index) => (
              <div key={index} className={`flex ${msg.role === 'user' ? 'justify-start' : 'justify-end'}`}>
                <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  msg.role === 'user' ? 'bg-gray-100 text-gray-800' :
                  msg.role === 'system' ? 'bg-blue-50 text-blue-800 border border-blue-200' :
                  'bg-gradient-to-br from-blue-500 to-green-500 text-white'
                }`}>
                  <div className="whitespace-pre-wrap text-right">{msg.content}</div>
                </div>
              </div>
            ))}
            {isProcessing && (
              <div className="flex justify-end">
                <div className="bg-gradient-to-br from-blue-500 to-green-500 text-white rounded-2xl px-4 py-3">
                  <div className="flex items-center gap-2">
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>جاري المعالجة...</span>
                  </div>
                </div>
              </div>
            )}
            {isPlaying && (
              <div className="flex justify-end">
                <div className="bg-green-50 border border-green-200 text-green-800 rounded-2xl px-4 py-2">
                  <div className="flex items-center gap-2">
                    <Volume2 className="w-4 h-4 animate-pulse" />
                    <span className="text-sm">🔊 يتحدث الآن...</span>
                  </div>
                </div>
              </div>
            )}
            {renderActionButtons()}
            <div ref={messagesEndRef} />
          </div>
          <div className="border-t p-4 bg-gray-50">
            {selectedFile && (
              <div className="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-lg flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Paperclip className="w-4 h-4 text-blue-600" />
                  <span className="text-sm text-blue-800">{selectedFile.name}</span>
                  <span className="text-xs text-blue-600">({(selectedFile.size / 1024).toFixed(0)} KB)</span>
                </div>
                <div className="flex gap-2">
                  <Button onClick={uploadFile} disabled={isProcessing} size="sm" className="bg-blue-600 hover:bg-blue-700">
                    رفع وتحليل
                  </Button>
                  <Button onClick={() => setSelectedFile(null)} size="sm" variant="ghost">
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            )}
            <div className="flex items-center gap-2">
              <Button onClick={handleMicClick} disabled={isProcessing} className={`rounded-full w-12 h-12 p-0 ${
                isRecording ? 'bg-red-500 hover:bg-red-600 animate-pulse' :
                'bg-gradient-to-br from-blue-500 to-green-500 hover:from-blue-600 hover:to-green-600'
              }`}>
                <Mic className="w-5 h-5 text-white" />
              </Button>
              <Button onClick={() => fileInputRef.current?.click()} disabled={isProcessing || isRecording}
                className="rounded-full w-12 h-12 p-0 bg-purple-500 hover:bg-purple-600">
                <Paperclip className="w-5 h-5 text-white" />
              </Button>
              <input ref={fileInputRef} type="file" onChange={handleFileSelect} accept="image/*,.pdf"
                className="hidden" />
              <Input value={input} onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !isProcessing && sendMessage()}
                placeholder="اكتب رسالتك هنا..." disabled={isProcessing || isRecording}
                className="flex-1 text-right" />
              <Button onClick={sendMessage} disabled={!input.trim() || isProcessing || isRecording}
                className="rounded-full w-12 h-12 p-0 bg-gray-600 hover:bg-gray-700">
                <Send className="w-5 h-5 text-white" />
              </Button>
            </div>
            {!locationDetected && (
              <div className="mt-3">
                <Button onClick={shareLocation} variant="outline" className="w-full gap-2">
                  <MapPin className="w-4 h-4" />
                  <span>مشاركة موقعي الحالي</span>
                </Button>
              </div>
            )}
            <p className="text-xs text-gray-500 text-center mt-2">
              🎤 تحدث | 📎 ارفع ملف | ✍️ اكتب رسالة | {voiceEnabled ? '🔊 الصوت مفعّل' : '🔇 الصوت متوقف'}
            </p>
          </div>
        </Card>
      </div>
    </div>
  );
}

