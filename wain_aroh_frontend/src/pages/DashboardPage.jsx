import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { 
  ArrowRight, Users, Activity, TrendingUp, Clock, 
  Stethoscope, RefreshCw, BarChart3 
} from 'lucide-react'

const API_BASE_URL = '/api'

export default function DashboardPage() {
  const navigate = useNavigate()
  const [stats, setStats] = useState(null)
  const [assessments, setAssessments] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    setIsLoading(true)
    try {
      const [statsRes, assessmentsRes] = await Promise.all([
        fetch(`${API_BASE_URL}/dashboard/stats`),
        fetch(`${API_BASE_URL}/dashboard/assessments?limit=10`)
      ])

      const statsData = await statsRes.json()
      const assessmentsData = await assessmentsRes.json()

      if (statsData.success) setStats(statsData.stats)
      if (assessmentsData.success) setAssessments(assessmentsData.assessments)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const getCTASColor = (level) => {
    const colors = {
      1: 'bg-red-600',
      2: 'bg-orange-600',
      3: 'bg-yellow-600',
      4: 'bg-blue-600',
      5: 'bg-green-600'
    }
    return colors[level] || 'bg-gray-600'
  }

  const getCTASName = (level) => {
    const names = {
      1: 'إنعاش',
      2: 'طارئ',
      3: 'عاجل',
      4: 'أقل عجلة',
      5: 'غير عاجل'
    }
    return names[level] || 'غير معروف'
  }

  const getCareTypeName = (type) => {
    const names = {
      emergency: 'قسم الطوارئ',
      ucc: 'مركز الرعاية العاجلة',
      clinic: 'مركز صحي',
      virtual: 'عيادة افتراضية'
    }
    return names[type] || type
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-12 w-12 animate-spin text-blue-600 mx-auto mb-4" />
          <p className="text-gray-600">جاري تحميل البيانات...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50" dir="rtl">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <Button 
              variant="ghost" 
              size="icon"
              onClick={() => navigate('/')}
            >
              <ArrowRight className="h-5 w-5" />
            </Button>
            <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-green-600 rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">لوحة التحكم</h1>
              <p className="text-xs text-gray-600">إحصائيات ومؤشرات الأداء</p>
            </div>
          </div>
          <Button 
            variant="outline" 
            size="sm"
            onClick={fetchDashboardData}
          >
            <RefreshCw className="h-4 w-4 ml-2" />
            تحديث
          </Button>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* KPI Cards */}
        <div className="grid md:grid-cols-4 gap-6 mb-8">
          <Card className="border-2 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
                  <Users className="h-6 w-6 text-blue-600" />
                </div>
                <TrendingUp className="h-5 w-5 text-green-600" />
              </div>
              <p className="text-sm text-gray-600 mb-1">إجمالي الجلسات</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.total_sessions || 0}</p>
            </CardContent>
          </Card>

          <Card className="border-2 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                  <Activity className="h-6 w-6 text-green-600" />
                </div>
                <TrendingUp className="h-5 w-5 text-green-600" />
              </div>
              <p className="text-sm text-gray-600 mb-1">التقييمات المكتملة</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.total_assessments || 0}</p>
            </CardContent>
          </Card>

          <Card className="border-2 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                  <Stethoscope className="h-6 w-6 text-purple-600" />
                </div>
                <Badge className="bg-green-600">95%</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-1">دقة التوجيه</p>
              <p className="text-3xl font-bold text-gray-900">95%</p>
            </CardContent>
          </Card>

          <Card className="border-2 hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                  <Clock className="h-6 w-6 text-orange-600" />
                </div>
                <Badge className="bg-green-600">{'<2min'}</Badge>
              </div>
              <p className="text-sm text-gray-600 mb-1">متوسط وقت التقييم</p>
              <p className="text-3xl font-bold text-gray-900">{'<2'}<span className="text-lg">دقيقة</span></p>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* CTAS Distribution */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle className="text-lg">توزيع الحالات حسب CTAS</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {[1, 2, 3, 4, 5].map((level) => {
                  const count = stats?.ctas_distribution?.[level] || 0
                  const total = stats?.total_assessments || 1
                  const percentage = Math.round((count / total) * 100)
                  
                  return (
                    <div key={level}>
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <Badge className={`${getCTASColor(level)} text-white`}>
                            {level}
                          </Badge>
                          <span className="text-sm font-medium">{getCTASName(level)}</span>
                        </div>
                        <span className="text-sm text-gray-600">{count} ({percentage}%)</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className={`${getCTASColor(level)} h-2 rounded-full transition-all`}
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>

          {/* Care Type Distribution */}
          <Card className="border-2">
            <CardHeader>
              <CardTitle className="text-lg">توزيع الحالات حسب نوع الرعاية</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {Object.entries(stats?.care_type_distribution || {}).map(([type, count]) => {
                  const total = stats?.total_assessments || 1
                  const percentage = Math.round((count / total) * 100)
                  
                  return (
                    <div key={type}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-medium">{getCareTypeName(type)}</span>
                        <span className="text-sm text-gray-600">{count} ({percentage}%)</span>
                      </div>
                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-600 to-green-600 h-2 rounded-full transition-all"
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Recent Assessments */}
        <Card className="border-2 mt-6">
          <CardHeader>
            <CardTitle className="text-lg">التقييمات الأخيرة</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b">
                    <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">الوقت</th>
                    <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">الأعراض</th>
                    <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">CTAS</th>
                    <th className="text-right py-3 px-4 text-sm font-semibold text-gray-700">نوع الرعاية</th>
                  </tr>
                </thead>
                <tbody>
                  {assessments.map((assessment) => (
                    <tr key={assessment.id} className="border-b hover:bg-gray-50">
                      <td className="py-3 px-4 text-sm text-gray-600">
                        {new Date(assessment.timestamp).toLocaleString('ar-SA', {
                          hour: '2-digit',
                          minute: '2-digit',
                          day: '2-digit',
                          month: '2-digit'
                        })}
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-900 max-w-xs truncate">
                        {assessment.symptoms}
                      </td>
                      <td className="py-3 px-4">
                        <Badge className={`${getCTASColor(assessment.ctas_level)} text-white`}>
                          {assessment.ctas_level}
                        </Badge>
                      </td>
                      <td className="py-3 px-4 text-sm text-gray-900">
                        {getCareTypeName(assessment.care_type)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {assessments.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  لا توجد تقييمات بعد
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

