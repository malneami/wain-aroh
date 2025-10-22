import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { Mic, MicOff, Send, MapPin, Phone, Navigation, Map, Volume2, VolumeX, Loader2 } from 'lucide-react'
import { Textarea } from '@/components/ui/textarea'
import RecommendationsList from '../components/RecommendationsList'

export default function ChatPageContinuous() {
  const navigate = useNavigate()
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isSpeaking, setIsSpeaking] = useState(false)
  const [voiceEnabled, setVoiceEnabled] = useState(true)
  const [continuousMode, setContinuousMode] = useState(false)
  const [sessionId] = useState(() => `session_${Date.now()}`)
  const [recommendations, setRecommendations] = useState([])
  
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const messagesEndRef = useRef(null)
  const audioRef = useRef(null)
  const silenceTimeoutRef = useRef(null)
  const audioContextRef = useRef(null)
  const analyserRef = useRef(null)

  useEffect(() => {
    // Welcome message
    const welcomeMsg = {
      role: 'assistant',
      content: 'مرحباً بك في خدمة "وين أروح" 👋\n\nأنا هنا لمساعدتك في معرفة المكان المناسب للرعاية الصحية.\n\n💡 **نصيحة**: فعّل وضع المحادثة المستمرة للتحدث معي بشكل طبيعي بدون الحاجة للنقر على الميكروفون كل مرة!\n\nكيف يمكنني مساعدتك اليوم؟'
    }
    setMessages([welcomeMsg])
    
    // Speak welcome if voice enabled
    if (voiceEnabled) {
      speakText(welcomeMsg.content)
    }
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  const speakText = async (text) => {
    if (!voiceEnabled) return
    if (!text || text.trim().length === 0) return
    
    try {
      setIsSpeaking(true)
      
      // Clean text for TTS (remove markdown, emojis, special formatting)
      const cleanText = text
        .replace(/\*\*(.+?)\*\*/g, '$1')  // Remove bold
        .replace(/\*(.+?)\*/g, '$1')      // Remove italic
        .replace(/#{1,6}\s/g, '')         // Remove headers
        .replace(/[📍📎💡👋🎤❌]/g, '')      // Remove emojis
        .replace(/\n{2,}/g, ' ')          // Replace multiple newlines with space
        .trim()
      
      if (!cleanText) {
        setIsSpeaking(false)
        return
      }
      
      const response = await fetch('/api/voice/text-to-speech', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: cleanText })
      })
      
      if (response.ok) {
        const audioBlob = await response.blob()
        const audioUrl = URL.createObjectURL(audioBlob)
        
        if (audioRef.current) {
          audioRef.current.pause()
          audioRef.current = null
        }
        
        const audio = new Audio(audioUrl)
        audioRef.current = audio
        
        audio.onended = () => {
          setIsSpeaking(false)
          URL.revokeObjectURL(audioUrl)
          
          // Auto-start recording in continuous mode
          if (continuousMode && !isRecording) {
            setTimeout(() => startRecording(), 500)
          }
        }
        
        audio.onerror = () => {
          setIsSpeaking(false)
          URL.revokeObjectURL(audioUrl)
        }
        
        await audio.play()
      } else {
        setIsSpeaking(false)
      }
    } catch (error) {
      console.error('TTS Error:', error)
      setIsSpeaking(false)
    }
  }

  const detectSilence = (stream) => {
    audioContextRef.current = new (window.AudioContext || window.webkitAudioContext)()
    analyserRef.current = audioContextRef.current.createAnalyser()
    const source = audioContextRef.current.createMediaStreamSource(stream)
    source.connect(analyserRef.current)
    
    analyserRef.current.fftSize = 2048
    const bufferLength = analyserRef.current.frequencyBinCount
    const dataArray = new Uint8Array(bufferLength)
    
    const checkAudioLevel = () => {
      if (!isRecording) return
      
      analyserRef.current.getByteTimeDomainData(dataArray)
      
      let sum = 0
      for (let i = 0; i < bufferLength; i++) {
        const value = dataArray[i] - 128
        sum += value * value
      }
      const rms = Math.sqrt(sum / bufferLength)
      
      // If speaking (above threshold)
      if (rms > 5) {
        // Clear silence timeout
        if (silenceTimeoutRef.current) {
          clearTimeout(silenceTimeoutRef.current)
          silenceTimeoutRef.current = null
        }
      } else {
        // If silent and no timeout set
        if (!silenceTimeoutRef.current && continuousMode) {
          silenceTimeoutRef.current = setTimeout(() => {
            stopRecording()
          }, 2000) // Stop after 2 seconds of silence
        }
      }
      
      requestAnimationFrame(checkAudioLevel)
    }
    
    checkAudioLevel()
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        } 
      })
      
      audioChunksRef.current = []
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm'
      })
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
        await transcribeAudio(audioBlob)
        
        stream.getTracks().forEach(track => track.stop())
        
        if (audioContextRef.current) {
          audioContextRef.current.close()
          audioContextRef.current = null
        }
      }
      
      mediaRecorderRef.current = mediaRecorder
      mediaRecorder.start()
      setIsRecording(true)
      
      // Add system message
      setMessages(prev => [...prev, {
        role: 'system',
        content: '🎤 جاري التسجيل...'
      }])
      scrollToBottom()
      
      // Start silence detection in continuous mode
      if (continuousMode) {
        detectSilence(stream)
      }
      
    } catch (error) {
      console.error('Microphone Error:', error)
      let errorMsg = 'حدث خطأ في الوصول إلى الميكروفون'
      
      if (error.name === 'NotAllowedError') {
        errorMsg = 'تم رفض الإذن للوصول إلى الميكروفون. يرجى السماح بالوصول من إعدادات المتصفح.'
      } else if (error.name === 'NotFoundError') {
        errorMsg = 'لم يتم العثور على ميكروفون. يرجى التأكد من توصيل ميكروفون بجهازك.'
      }
      
      setMessages(prev => [...prev, {
        role: 'system',
        content: `❌ ${errorMsg}`
      }])
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      
      if (silenceTimeoutRef.current) {
        clearTimeout(silenceTimeoutRef.current)
        silenceTimeoutRef.current = null
      }
      
      // Remove recording message
      setMessages(prev => prev.filter(msg => msg.content !== '🎤 جاري التسجيل...'))
    }
  }

  const transcribeAudio = async (audioBlob) => {
    setIsProcessing(true)
    
    try {
      const formData = new FormData()
      formData.append('audio', audioBlob, 'recording.webm')
      
      const response = await fetch('/api/voice/transcribe', {
        method: 'POST',
        body: formData
      })
      
      const data = await response.json()
      
      if (data.success && data.text) {
        // Add user message
        setMessages(prev => [...prev, {
          role: 'user',
          content: data.text
        }])
        
        // Send to AI (skip adding message since we already added it above)
        await sendMessage(data.text, true)
      } else {
        setMessages(prev => [...prev, {
          role: 'system',
          content: '❌ لم أتمكن من فهم ما قلته. يرجى المحاولة مرة أخرى.'
        }])
      }
    } catch (error) {
      console.error('Transcription Error:', error)
      setMessages(prev => [...prev, {
        role: 'system',
        content: '❌ حدث خطأ في معالجة الصوت'
      }])
    } finally {
      setIsProcessing(false)
    }
  }

  const handleRecommendationAction = async (recommendation) => {
    try {
      const response = await fetch('/api/recommendations/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recommendation_id: recommendation.id,
          action_type: recommendation.action_type,
          action_data: {
            ...recommendation.action_data,
            patient_id: sessionId,
            conversation_id: sessionId
          }
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        // Add system message about the action
        setMessages(prev => [...prev, {
          role: 'system',
          content: data.message
        }])
        
        // Speak the message
        if (voiceEnabled) {
          await speakText(data.message)
        }
      }
    } catch (error) {
      console.error('Recommendation action error:', error)
      setMessages(prev => [...prev, {
        role: 'system',
        content: '❌ حدث خطأ في تنفيذ الإجراء'
      }])
    }
  }

  const sendMessage = async (text = inputMessage, skipAddingMessage = false) => {
    if (!text.trim()) return
    
    // Only add message if not already added (e.g., from transcription)
    if (!skipAddingMessage && !text.includes('🎤')) {
      setMessages(prev => [...prev, {
        role: 'user',
        content: text
      }])
    }
    
    setInputMessage('')
    setIsProcessing(true)
    
    try {
      const response = await fetch('/api/conversation/message', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: text
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        const aiResponse = data.response || data.message
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: aiResponse
        }])
        
        // Update recommendations if available
        if (data.recommendations && data.recommendations.length > 0) {
          setRecommendations(data.recommendations)
        }
        
        // Speak response
        if (voiceEnabled) {
          await speakText(aiResponse)
        } else if (continuousMode && !isRecording) {
          // If voice disabled but continuous mode on, restart recording
          setTimeout(() => startRecording(), 500)
        }
      }
    } catch (error) {
      console.error('Send Error:', error)
      setMessages(prev => [...prev, {
        role: 'system',
        content: '❌ حدث خطأ في الاتصال'
      }])
    } finally {
      setIsProcessing(false)
    }
  }

  const toggleVoice = () => {
    setVoiceEnabled(!voiceEnabled)
    if (voiceEnabled && audioRef.current) {
      audioRef.current.pause()
      setIsSpeaking(false)
    }
  }

  const toggleContinuousMode = () => {
    const newMode = !continuousMode
    setContinuousMode(newMode)
    
    if (newMode) {
      // Start continuous mode
      setMessages(prev => [...prev, {
        role: 'system',
        content: '✅ تم تفعيل وضع المحادثة المستمرة. تحدث بشكل طبيعي وسأستمع لك!'
      }])
      setTimeout(() => startRecording(), 1000)
    } else {
      // Stop continuous mode
      if (isRecording) {
        stopRecording()
      }
      setMessages(prev => [...prev, {
        role: 'system',
        content: '⏸️ تم إيقاف وضع المحادثة المستمرة.'
      }])
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50" dir="rtl">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-10">
        <div className="container mx-auto px-4 py-3 flex justify-between items-center">
          <Button variant="ghost" onClick={() => navigate('/')}>
            ← العودة
          </Button>
          <h1 className="text-xl font-bold text-gray-900">المحادثة</h1>
          <div className="flex gap-2">
            <Button
              variant={continuousMode ? "default" : "outline"}
              size="sm"
              onClick={toggleContinuousMode}
              className={continuousMode ? "bg-green-600 hover:bg-green-700" : ""}
            >
              {continuousMode ? '🔴 محادثة مستمرة' : '⚪ محادثة عادية'}
            </Button>
            <Button
              variant={voiceEnabled ? "default" : "outline"}
              size="sm"
              onClick={toggleVoice}
            >
              {voiceEnabled ? <Volume2 className="w-4 h-4 ml-1" /> : <VolumeX className="w-4 h-4 ml-1" />}
              {voiceEnabled ? 'الصوت مفعّل' : 'الصوت متوقف'}
            </Button>
          </div>
        </div>
      </header>

      {/* Chat Area */}
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <div className="space-y-4 mb-24">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === 'user' ? 'justify-start' : 'justify-end'}`}
            >
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3 ${
                  msg.role === 'user'
                    ? 'bg-gray-200 text-gray-900'
                    : msg.role === 'system'
                    ? 'bg-yellow-100 text-yellow-900 text-sm'
                    : 'bg-gradient-to-r from-blue-600 to-green-600 text-white'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.content}</p>
              </div>
            </div>
          ))}
          
          {isSpeaking && (
            <div className="flex justify-end">
              <div className="bg-green-100 text-green-900 rounded-2xl px-4 py-3 text-sm">
                🔊 يتحدث الآن...
              </div>
            </div>
          )}
          
          {isProcessing && (
            <div className="flex justify-end">
              <div className="bg-blue-100 text-blue-900 rounded-2xl px-4 py-3 text-sm flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin" />
                جاري المعالجة...
              </div>
            </div>
          )}
          
          {/* Recommendations */}
          {recommendations.length > 0 && (
            <RecommendationsList 
              recommendations={recommendations}
              onActionClick={handleRecommendationAction}
            />
          )}
          
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t shadow-lg">
        <div className="container mx-auto px-4 py-4 max-w-4xl">
          <div className="flex gap-2 items-end">
            {!continuousMode && (
              <Button
                size="lg"
                variant={isRecording ? "destructive" : "default"}
                className={`rounded-full w-14 h-14 flex-shrink-0 ${
                  isRecording ? 'animate-pulse' : ''
                }`}
                onClick={isRecording ? stopRecording : startRecording}
                disabled={isProcessing || isSpeaking}
              >
                {isRecording ? <MicOff className="w-6 h-6" /> : <Mic className="w-6 h-6" />}
              </Button>
            )}
            
            {continuousMode && (
              <div className="flex-shrink-0 w-14 h-14 rounded-full bg-green-600 flex items-center justify-center animate-pulse">
                <Mic className="w-6 h-6 text-white" />
              </div>
            )}
            
            <Textarea
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="اكتب رسالتك هنا..."
              className="flex-1 min-h-[56px] max-h-32 resize-none"
              disabled={isProcessing || isSpeaking || continuousMode}
            />
            
            <Button
              size="lg"
              className="rounded-full w-14 h-14 flex-shrink-0 bg-gradient-to-r from-blue-600 to-green-600"
              onClick={() => sendMessage()}
              disabled={!inputMessage.trim() || isProcessing || isSpeaking || continuousMode}
            >
              <Send className="w-5 h-5" />
            </Button>
          </div>
          
          <p className="text-xs text-gray-500 text-center mt-2">
            {continuousMode 
              ? '🔴 وضع المحادثة المستمرة مفعّل - تحدث بشكل طبيعي'
              : 'اضغط على المايكروفون للتحدث أو اكتب رسالتك'
            }
          </p>
        </div>
      </div>
    </div>
  )
}

