import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { MessageCircle, MapPin, Clock, Activity, Phone, Stethoscope } from 'lucide-react'

export default function HomePage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50" dir="rtl">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-green-600 rounded-xl flex items-center justify-center">
              <Stethoscope className="w-7 h-7 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">وين أروح؟</h1>
              <p className="text-sm text-gray-600">التوجيه الذكي للرعاية العاجلة</p>
            </div>
          </div>
          <Button 
            variant="outline" 
            onClick={() => navigate('/dashboard')}
            className="text-sm"
          >
            لوحة التحكم
          </Button>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <div className="max-w-3xl mx-auto">
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            نساعدك في الوصول إلى الرعاية الصحية المناسبة
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            مساعد ذكي يوجهك إلى المركز الصحي الأنسب لحالتك باستخدام الذكاء الاصطناعي
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Button 
              size="lg" 
              className="bg-gradient-to-r from-blue-600 to-green-600 hover:from-blue-700 hover:to-green-700 text-white px-8 py-6 text-lg rounded-xl shadow-lg hover:shadow-xl transition-all"
              onClick={() => navigate('/chat')}
            >
              <MessageCircle className="ml-2 h-6 w-6" />
              ابدأ المحادثة الآن
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              className="px-8 py-6 text-lg rounded-xl shadow-lg hover:shadow-xl transition-all border-2"
              onClick={() => navigate('/search')}
            >
              <MapPin className="ml-2 h-6 w-6" />
              ابحث عن مركز طبي
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-12">
        <div className="grid md:grid-cols-3 gap-6 max-w-5xl mx-auto">
          <Card className="border-2 hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <MessageCircle className="w-6 h-6 text-blue-600" />
              </div>
              <CardTitle className="text-xl">محادثة صوتية ذكية</CardTitle>
              <CardDescription className="text-base">
                تحدث مع المساعد الذكي بصوتك وصف أعراضك بشكل طبيعي
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
                <Activity className="w-6 h-6 text-green-600" />
              </div>
              <CardTitle className="text-xl">تقييم دقيق للحالة</CardTitle>
              <CardDescription className="text-base">
                تحليل الأعراض وتصنيف الحالة حسب نظام CTAS الطبي
              </CardDescription>
            </CardHeader>
          </Card>

          <Card className="border-2 hover:shadow-lg transition-shadow">
            <CardHeader>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <MapPin className="w-6 h-6 text-purple-600" />
              </div>
              <CardTitle className="text-xl">توجيه للمركز الأقرب</CardTitle>
              <CardDescription className="text-base">
                اقتراح المركز الصحي الأنسب والأقرب لموقعك
              </CardDescription>
            </CardHeader>
          </Card>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-4 py-16 bg-white/50 rounded-3xl my-12">
        <h3 className="text-3xl font-bold text-center mb-12 text-gray-900">كيف يعمل النظام؟</h3>
        <div className="max-w-4xl mx-auto grid md:grid-cols-4 gap-8">
          <div className="text-center">
            <div className="w-16 h-16 bg-blue-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              1
            </div>
            <h4 className="font-semibold text-lg mb-2">ابدأ المحادثة</h4>
            <p className="text-gray-600">تحدث مع المساعد الذكي عن أعراضك</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-green-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              2
            </div>
            <h4 className="font-semibold text-lg mb-2">التقييم الذكي</h4>
            <p className="text-gray-600">تحليل الحالة وتحديد مستوى الخطورة</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-purple-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              3
            </div>
            <h4 className="font-semibold text-lg mb-2">التوصية</h4>
            <p className="text-gray-600">الحصول على توصية بالمركز المناسب</p>
          </div>

          <div className="text-center">
            <div className="w-16 h-16 bg-orange-600 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
              4
            </div>
            <h4 className="font-semibold text-lg mb-2">رسالة نصية</h4>
            <p className="text-gray-600">استلام تفاصيل المركز عبر SMS</p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-16 text-center">
        <Card className="max-w-2xl mx-auto bg-gradient-to-br from-blue-600 to-green-600 text-white border-0">
          <CardContent className="pt-12 pb-12">
            <h3 className="text-3xl font-bold mb-4">هل تحتاج إلى رعاية صحية الآن؟</h3>
            <p className="text-lg mb-8 text-blue-50">
              دعنا نساعدك في العثور على المكان المناسب لحالتك
            </p>
            <Button 
              size="lg" 
              variant="secondary"
              className="bg-white text-blue-600 hover:bg-gray-100 px-8 py-6 text-lg rounded-xl shadow-lg"
              onClick={() => navigate('/chat')}
            >
              <Phone className="ml-2 h-6 w-6" />
              ابدأ الآن
            </Button>
          </CardContent>
        </Card>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-8 mt-16">
        <div className="container mx-auto px-4 text-center">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-green-600 rounded-lg flex items-center justify-center">
              <Stethoscope className="w-6 h-6 text-white" />
            </div>
            <h4 className="text-xl font-bold">وين أروح؟</h4>
          </div>
          <div className="mt-2 text-sm text-gray-400">
            <span>© 2025 جميع الحقوق محفوظة</span>
          </div>
        </div>
      </footer>
    </div>
  )
}

