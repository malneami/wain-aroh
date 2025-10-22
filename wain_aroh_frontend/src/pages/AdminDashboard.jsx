import { useState, useEffect } from 'react'
import './AdminDashboard.css'

export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('hospitals')
  const [statistics, setStatistics] = useState(null)
  const [hospitals, setHospitals] = useState([])
  const [organizations, setOrganizations] = useState([])
  const [clusters, setClusters] = useState([])
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(false)
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingItem, setEditingItem] = useState(null)

  useEffect(() => {
    loadStatistics()
    loadOrganizations()
    loadClusters()
    loadServices()
  }, [])

  useEffect(() => {
    if (activeTab === 'hospitals') {
      loadHospitals()
    }
  }, [activeTab])

  const loadStatistics = async () => {
    try {
      const response = await fetch('/api/admin/statistics')
      const data = await response.json()
      if (data.success) {
        setStatistics(data.statistics)
      }
    } catch (error) {
      console.error('Error loading statistics:', error)
    }
  }

  const loadHospitals = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/admin/hospitals?include_services=true')
      const data = await response.json()
      if (data.success) {
        setHospitals(data.hospitals)
      }
    } catch (error) {
      console.error('Error loading hospitals:', error)
    } finally {
      setLoading(false)
    }
  }

  const loadOrganizations = async () => {
    try {
      const response = await fetch('/api/admin/organizations')
      const data = await response.json()
      if (data.success) {
        setOrganizations(data.organizations)
      }
    } catch (error) {
      console.error('Error loading organizations:', error)
    }
  }

  const loadClusters = async () => {
    try {
      const response = await fetch('/api/admin/clusters')
      const data = await response.json()
      if (data.success) {
        setClusters(data.clusters)
      }
    } catch (error) {
      console.error('Error loading clusters:', error)
    }
  }

  const loadServices = async () => {
    try {
      const response = await fetch('/api/admin/services')
      const data = await response.json()
      if (data.success) {
        setServices(data.services)
      }
    } catch (error) {
      console.error('Error loading services:', error)
    }
  }

  const deleteHospital = async (id) => {
    if (!confirm('هل أنت متأكد من حذف هذا المستشفى؟')) return
    
    try {
      const response = await fetch(`/api/admin/hospitals/${id}`, {
        method: 'DELETE'
      })
      const data = await response.json()
      if (data.success) {
        loadHospitals()
        loadStatistics()
        alert('تم الحذف بنجاح')
      }
    } catch (error) {
      console.error('Error deleting hospital:', error)
      alert('حدث خطأ أثناء الحذف')
    }
  }

  return (
    <div className="admin-dashboard">
      <div className="admin-header">
        <h1>🏥 لوحة التحكم الإدارية</h1>
        <a href="/" className="btn-back">← العودة للرئيسية</a>
      </div>

      {/* Statistics Cards */}
      {statistics && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon">🏥</div>
            <div className="stat-info">
              <div className="stat-value">{statistics.total_hospitals}</div>
              <div className="stat-label">إجمالي المستشفيات</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🚑</div>
            <div className="stat-info">
              <div className="stat-value">{statistics.emergency_hospitals}</div>
              <div className="stat-label">مستشفيات الطوارئ</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🏢</div>
            <div className="stat-info">
              <div className="stat-value">{statistics.total_organizations}</div>
              <div className="stat-label">الجهات الصحية</div>
            </div>
          </div>
          <div className="stat-card">
            <div className="stat-icon">🔧</div>
            <div className="stat-info">
              <div className="stat-value">{statistics.total_services}</div>
              <div className="stat-label">الخدمات المتوفرة</div>
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="admin-tabs">
        <button 
          className={activeTab === 'hospitals' ? 'active' : ''}
          onClick={() => setActiveTab('hospitals')}
        >
          المستشفيات
        </button>
        <button 
          className={activeTab === 'organizations' ? 'active' : ''}
          onClick={() => setActiveTab('organizations')}
        >
          الجهات الصحية
        </button>
        <button 
          className={activeTab === 'clusters' ? 'active' : ''}
          onClick={() => setActiveTab('clusters')}
        >
          التجمعات الصحية
        </button>
        <button 
          className={activeTab === 'services' ? 'active' : ''}
          onClick={() => setActiveTab('services')}
        >
          الخدمات
        </button>
      </div>

      {/* Content */}
      <div className="admin-content">
        {activeTab === 'hospitals' && (
          <HospitalsTab 
            hospitals={hospitals}
            organizations={organizations}
            clusters={clusters}
            services={services}
            onDelete={deleteHospital}
            onRefresh={loadHospitals}
            onRefreshStats={loadStatistics}
            loading={loading}
          />
        )}
        
        {activeTab === 'organizations' && (
          <OrganizationsTab 
            organizations={organizations}
            onRefresh={loadOrganizations}
          />
        )}
        
        {activeTab === 'clusters' && (
          <ClustersTab 
            clusters={clusters}
            onRefresh={loadClusters}
          />
        )}
        
        {activeTab === 'services' && (
          <ServicesTab 
            services={services}
            onRefresh={loadServices}
          />
        )}
      </div>
    </div>
  )
}

// Hospitals Tab Component
function HospitalsTab({ hospitals, organizations, clusters, services, onDelete, onRefresh, onRefreshStats, loading }) {
  const [showAddModal, setShowAddModal] = useState(false)
  const [editingHospital, setEditingHospital] = useState(null)

  if (loading) {
    return <div className="loading">جاري التحميل...</div>
  }

  return (
    <div className="tab-content">
      <div className="tab-header">
        <h2>إدارة المستشفيات</h2>
        <button className="btn-primary" onClick={() => setShowAddModal(true)}>
          + إضافة مستشفى جديد
        </button>
      </div>

      <div className="hospitals-grid">
        {hospitals.map(hospital => (
          <div key={hospital.id} className="hospital-card">
            <div className="hospital-header">
              <h3>{hospital.name_ar}</h3>
              {hospital.is_emergency && <span className="badge emergency">طوارئ</span>}
              {hospital.is_24_7 && <span className="badge full-time">24/7</span>}
            </div>
            
            <div className="hospital-info">
              <p><strong>الجهة:</strong> {hospital.organization?.name_ar || 'غير محدد'}</p>
              <p><strong>التجمع:</strong> {hospital.cluster?.name_ar || 'غير محدد'}</p>
              <p><strong>الحي:</strong> {hospital.district_ar || 'غير محدد'}</p>
              <p><strong>الهاتف:</strong> {hospital.phone || 'غير محدد'}</p>
              {hospital.services && hospital.services.length > 0 && (
                <p><strong>الخدمات:</strong> {hospital.services.length} خدمة</p>
              )}
            </div>

            <div className="hospital-actions">
              <button 
                className="btn-edit"
                onClick={() => setEditingHospital(hospital)}
              >
                تعديل
              </button>
              <button 
                className="btn-delete"
                onClick={() => onDelete(hospital.id)}
              >
                حذف
              </button>
            </div>
          </div>
        ))}
      </div>

      {hospitals.length === 0 && (
        <div className="empty-state">
          <p>لا توجد مستشفيات مضافة بعد</p>
          <button className="btn-primary" onClick={() => setShowAddModal(true)}>
            إضافة أول مستشفى
          </button>
        </div>
      )}

      {(showAddModal || editingHospital) && (
        <HospitalModal
          hospital={editingHospital}
          organizations={organizations}
          clusters={clusters}
          services={services}
          onClose={() => {
            setShowAddModal(false)
            setEditingHospital(null)
          }}
          onSave={() => {
            setShowAddModal(false)
            setEditingHospital(null)
            onRefresh()
            onRefreshStats()
          }}
        />
      )}
    </div>
  )
}

// Hospital Modal Component
function HospitalModal({ hospital, organizations, clusters, services, onClose, onSave }) {
  const [formData, setFormData] = useState(hospital || {
    name_ar: '',
    name_en: '',
    organization_id: '',
    cluster_id: '',
    facility_type: 'hospital',
    is_emergency: false,
    is_24_7: false,
    phone: '',
    phone_emergency: '',
    email: '',
    website: '',
    address_ar: '',
    city: 'Riyadh',
    district_ar: '',
    latitude: '',
    longitude: '',
    capacity_beds: '',
    is_active: true
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    try {
      const url = hospital 
        ? `/api/admin/hospitals/${hospital.id}`
        : '/api/admin/hospitals'
      
      const method = hospital ? 'PUT' : 'POST'
      
      // Clean up form data - convert empty strings to null for optional fields
      console.log('Form data before cleaning:', formData);
      console.log('organization_id:', formData.organization_id, 'type:', typeof formData.organization_id);
      console.log('cluster_id:', formData.cluster_id, 'type:', typeof formData.cluster_id);
      const cleanedData = {
        ...formData,
        organization_id: formData.organization_id ?? null,
        cluster_id: formData.cluster_id ?? null,
        latitude: formData.latitude || null,
        longitude: formData.longitude || null,
        capacity_beds: formData.capacity_beds || null
      };
      console.log('Cleaned data:', cleanedData);
      
      const response = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(cleanedData)
      })
      
      const data = await response.json()
      
      if (data.success) {
        alert(hospital ? 'تم التحديث بنجاح' : 'تمت الإضافة بنجاح')
        onSave()
      } else {
        alert('حدث خطأ: ' + data.error)
      }
    } catch (error) {
      console.error('Error saving hospital:', error)
      alert('حدث خطأ أثناء الحفظ')
    }
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{hospital ? 'تعديل المستشفى' : 'إضافة مستشفى جديد'}</h2>
          <button className="btn-close" onClick={onClose}>×</button>
        </div>
        
        <form onSubmit={handleSubmit} className="hospital-form">
          <div className="form-row">
            <div className="form-group">
              <label>الاسم بالعربية *</label>
              <input
                type="text"
                value={formData.name_ar}
                onChange={e => setFormData({...formData, name_ar: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>الاسم بالإنجليزية *</label>
              <input
                type="text"
                value={formData.name_en}
                onChange={e => setFormData({...formData, name_en: e.target.value})}
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>الجهة الصحية</label>
              <select
                value={formData.organization_id || ''}
                onChange={e => {
                  const newValue = e.target.value ? parseInt(e.target.value) : null;
                  console.log('Organization changed:', e.target.value, '->', newValue);
                  setFormData({...formData, organization_id: newValue});
                }}
              >
                <option value="">اختر الجهة</option>
                {organizations.map(org => (
                  <option key={org.id} value={org.id}>{org.name_ar}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>التجمع الصحي</label>
              <select
                value={formData.cluster_id || ''}
                onChange={e => {
                  const newValue = e.target.value ? parseInt(e.target.value) : null;
                  console.log('Cluster changed:', e.target.value, '->', newValue);
                  setFormData({...formData, cluster_id: newValue});
                }}
              >
                <option value="">اختر التجمع</option>
                {clusters.map(cluster => (
                  <option key={cluster.id} value={cluster.id}>{cluster.name_ar}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>نوع المنشأة *</label>
              <select
                value={formData.facility_type}
                onChange={e => setFormData({...formData, facility_type: e.target.value})}
                required
              >
                <option value="hospital">مستشفى</option>
                <option value="clinic">عيادة</option>
                <option value="health_center">مركز صحي</option>
                <option value="emergency_center">مركز طوارئ</option>
              </select>
            </div>
            <div className="form-group">
              <label>الحي</label>
              <input
                type="text"
                value={formData.district_ar}
                onChange={e => setFormData({...formData, district_ar: e.target.value})}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>الهاتف</label>
              <input
                type="tel"
                value={formData.phone}
                onChange={e => setFormData({...formData, phone: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>هاتف الطوارئ</label>
              <input
                type="tel"
                value={formData.phone_emergency}
                onChange={e => setFormData({...formData, phone_emergency: e.target.value})}
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>خط العرض (Latitude)</label>
              <input
                type="number"
                step="any"
                value={formData.latitude}
                onChange={e => setFormData({...formData, latitude: e.target.value})}
              />
            </div>
            <div className="form-group">
              <label>خط الطول (Longitude)</label>
              <input
                type="number"
                step="any"
                value={formData.longitude}
                onChange={e => setFormData({...formData, longitude: e.target.value})}
              />
            </div>
          </div>

          <div className="form-checkboxes">
            <label>
              <input
                type="checkbox"
                checked={formData.is_emergency}
                onChange={e => setFormData({...formData, is_emergency: e.target.checked})}
              />
              يوجد طوارئ
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.is_24_7}
                onChange={e => setFormData({...formData, is_24_7: e.target.checked})}
              />
              يعمل 24/7
            </label>
            <label>
              <input
                type="checkbox"
                checked={formData.is_active}
                onChange={e => setFormData({...formData, is_active: e.target.checked})}
              />
              نشط
            </label>
          </div>

          <div className="form-actions">
            <button type="button" className="btn-secondary" onClick={onClose}>
              إلغاء
            </button>
            <button type="submit" className="btn-primary">
              {hospital ? 'تحديث' : 'إضافة'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

// Organizations Tab Component
function OrganizationsTab({ organizations, onRefresh }) {
  return (
    <div className="tab-content">
      <div className="tab-header">
        <h2>الجهات الصحية</h2>
      </div>
      <div className="simple-list">
        {organizations.map(org => (
          <div key={org.id} className="list-item">
            <div>
              <h4>{org.name_ar}</h4>
              <p>{org.name_en}</p>
            </div>
            <span className="badge">{org.type}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

// Clusters Tab Component
function ClustersTab({ clusters, onRefresh }) {
  return (
    <div className="tab-content">
      <div className="tab-header">
        <h2>التجمعات الصحية بالرياض</h2>
      </div>
      <div className="simple-list">
        {clusters.map(cluster => (
          <div key={cluster.id} className="list-item">
            <div>
              <h4>{cluster.name_ar}</h4>
              <p>{cluster.name_en}</p>
            </div>
            <span className="badge">التجمع {cluster.cluster_number}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

// Services Tab Component
function ServicesTab({ services, onRefresh }) {
  return (
    <div className="tab-content">
      <div className="tab-header">
        <h2>الخدمات الطبية</h2>
      </div>
      <div className="simple-list">
        {services.map(service => (
          <div key={service.id} className="list-item">
            <div>
              <h4>{service.name_ar}</h4>
              <p>{service.name_en}</p>
            </div>
            {service.is_emergency && <span className="badge emergency">طوارئ</span>}
          </div>
        ))}
      </div>
    </div>
  )
}

