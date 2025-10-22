import { useState, useEffect } from 'react';
import { Search, MapPin, Filter, Star, Clock, TrendingUp, Phone, Navigation, Calendar, X } from 'lucide-react';
import './SearchPage.css';

const SearchPage = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [filters, setFilters] = useState({
    specialties: [],
    organizations: [],
    clusters: [],
    minRating: 0,
    maxDistance: 50,
    availableNow: false,
    acceptsEmergency: false,
    sortBy: 'relevance'
  });
  
  const [availableFilters, setAvailableFilters] = useState({
    specialties: [],
    organizations: [],
    clusters: [],
    services: [],
    sortOptions: []
  });
  
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showFilters, setShowFilters] = useState(false);
  const [userLocation, setUserLocation] = useState(null);
  const [stats, setStats] = useState(null);
  const [selectedFacility, setSelectedFacility] = useState(null);

  // الحصول على الفلاتر المتاحة
  useEffect(() => {
    fetchAvailableFilters();
    getUserLocation();
  }, []);

  const getUserLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const location = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          };
          setUserLocation(location);
          // البحث تلقائياً بعد الحصول على الموقع
          performSearch(location);
        },
        (error) => {
          console.log('Could not get location:', error);
          // استخدام موقع افتراضي (الرياض)
          const defaultLocation = { lat: 24.7136, lng: 46.6753 };
          setUserLocation(defaultLocation);
          // البحث تلقائياً بالموقع الافتراضي
          performSearch(defaultLocation);
        }
      );
    } else {
      const defaultLocation = { lat: 24.7136, lng: 46.6753 };
      setUserLocation(defaultLocation);
      performSearch(defaultLocation);
    }
  };

  const performSearch = async (location) => {
    setLoading(true);
    try {
      const searchData = {
        ...filters,
        location: location,
        sortBy: 'distance', // ترتيب حسب المسافة افتراضياً
        page: 1,
        limit: 20
      };

      const response = await fetch('/api/search/facilities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(searchData)
      });

      const data = await response.json();
      if (data.success) {
        setSearchResults(data.results);
        setStats(data.stats);
      }
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAvailableFilters = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/search/filters');
      const data = await response.json();
      if (data.success) {
        setAvailableFilters(data.filters);
      }
    } catch (error) {
      console.error('Error fetching filters:', error);
    }
  };

  const handleSearch = async () => {
    if (!userLocation) {
      alert('جاري تحديد موقعك...');
      return;
    }
    performSearch(userLocation);
  };

  const toggleFilter = (filterType, value) => {
    setFilters(prev => {
      const currentValues = prev[filterType];
      const newValues = currentValues.includes(value)
        ? currentValues.filter(v => v !== value)
        : [...currentValues, value];
      return { ...prev, [filterType]: newValues };
    });
  };

  const getRatingStars = (rating) => {
    const stars = [];
    for (let i = 0; i < 5; i++) {
      stars.push(
        <Star
          key={i}
          size={16}
          className={i < Math.floor(rating) ? 'star-filled' : 'star-empty'}
          fill={i < Math.floor(rating) ? '#fbbf24' : 'none'}
        />
      );
    }
    return stars;
  };

  const getStatusBadge = (isAvailable) => {
    return isAvailable ? (
      <span className="status-badge available">متاح الآن</span>
    ) : (
      <span className="status-badge busy">مشغول</span>
    );
  };

  const viewFacilityDetails = async (facilityId) => {
    try {
      const response = await fetch(`http://localhost:5000/api/search/facilities/${facilityId}`);
      const data = await response.json();
      if (data.success) {
        setSelectedFacility(data.facility);
      }
    } catch (error) {
      console.error('Error fetching facility details:', error);
    }
  };

  return (
    <div className="search-page">
      {/* Header */}
      <div className="search-header">
        <h1>🔍 البحث عن المراكز الطبية المتخصصة</h1>
        <p>ابحث عن أفضل المنشآت الصحية القريبة منك</p>
      </div>

      {/* Search Bar */}
      <div className="search-bar-container">
        <div className="search-input-wrapper">
          <Search className="search-icon" size={20} />
          <input
            type="text"
            placeholder="ابحث عن تخصص، خدمة، أو منشأة..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            className="search-input"
          />
          <button 
            className="filter-toggle-btn"
            onClick={() => setShowFilters(!showFilters)}
          >
            <Filter size={20} />
            فلاتر
          </button>
        </div>
        <button className="search-btn" onClick={handleSearch} disabled={loading}>
          {loading ? 'جاري البحث...' : 'بحث'}
        </button>
      </div>

      {/* Filters Panel */}
      {showFilters && (
        <div className="filters-panel">
          <div className="filters-header">
            <h3>الفلاتر</h3>
            <button onClick={() => setShowFilters(false)}>
              <X size={20} />
            </button>
          </div>

          <div className="filters-grid">
            {/* التخصصات */}
            <div className="filter-group">
              <h4>التخصصات</h4>
              <div className="filter-options">
                {availableFilters.specialties.map(spec => (
                  <label key={spec} className="filter-checkbox">
                    <input
                      type="checkbox"
                      checked={filters.specialties.includes(spec)}
                      onChange={() => toggleFilter('specialties', spec)}
                    />
                    <span>{spec}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* الجهات */}
            <div className="filter-group">
              <h4>الجهة الصحية</h4>
              <div className="filter-options">
                {availableFilters.organizations.map(org => (
                  <label key={org} className="filter-checkbox">
                    <input
                      type="checkbox"
                      checked={filters.organizations.includes(org)}
                      onChange={() => toggleFilter('organizations', org)}
                    />
                    <span>{org}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* التجمعات */}
            <div className="filter-group">
              <h4>التجمع الصحي</h4>
              <div className="filter-options">
                {availableFilters.clusters.map(cluster => (
                  <label key={cluster} className="filter-checkbox">
                    <input
                      type="checkbox"
                      checked={filters.clusters.includes(cluster)}
                      onChange={() => toggleFilter('clusters', cluster)}
                    />
                    <span>{cluster}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* التقييم */}
            <div className="filter-group">
              <h4>التقييم الأدنى</h4>
              <select
                value={filters.minRating}
                onChange={(e) => setFilters({...filters, minRating: parseFloat(e.target.value)})}
                className="filter-select"
              >
                <option value="0">الكل</option>
                <option value="3">3 نجوم فأكثر</option>
                <option value="4">4 نجوم فأكثر</option>
                <option value="4.5">4.5 نجوم فأكثر</option>
              </select>
            </div>

            {/* المسافة */}
            <div className="filter-group">
              <h4>المسافة القصوى: {filters.maxDistance} كم</h4>
              <input
                type="range"
                min="5"
                max="100"
                value={filters.maxDistance}
                onChange={(e) => setFilters({...filters, maxDistance: parseInt(e.target.value)})}
                className="filter-range"
              />
            </div>

            {/* الترتيب */}
            <div className="filter-group">
              <h4>الترتيب حسب</h4>
              <select
                value={filters.sortBy}
                onChange={(e) => setFilters({...filters, sortBy: e.target.value})}
                className="filter-select"
              >
                {availableFilters.sortOptions.map(opt => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>

            {/* خيارات إضافية */}
            <div className="filter-group">
              <h4>خيارات إضافية</h4>
              <label className="filter-checkbox">
                <input
                  type="checkbox"
                  checked={filters.availableNow}
                  onChange={(e) => setFilters({...filters, availableNow: e.target.checked})}
                />
                <span>متاح الآن</span>
              </label>
              <label className="filter-checkbox">
                <input
                  type="checkbox"
                  checked={filters.acceptsEmergency}
                  onChange={(e) => setFilters({...filters, acceptsEmergency: e.target.checked})}
                />
                <span>يقبل الطوارئ</span>
              </label>
            </div>
          </div>

          <button className="apply-filters-btn" onClick={handleSearch}>
            تطبيق الفلاتر
          </button>
        </div>
      )}

      {/* Stats */}
      {stats && (
        <div className="search-stats">
          <div className="stat-item">
            <span className="stat-label">النتائج:</span>
            <span className="stat-value">{searchResults.length}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">متوسط المسافة:</span>
            <span className="stat-value">{stats.avg_distance} كم</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">متوسط التقييم:</span>
            <span className="stat-value">{stats.avg_rating} ⭐</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">متوسط الانتظار:</span>
            <span className="stat-value">{stats.avg_wait_time} دقيقة</span>
          </div>
        </div>
      )}

      {/* Results */}
      <div className="search-results">
        {loading ? (
          <div className="loading-spinner">جاري البحث...</div>
        ) : searchResults.length > 0 ? (
          searchResults.map((result, index) => (
            <div key={index} className="result-card">
              <div className="result-header">
                <div className="result-title-section">
                  <h3>{result.facility.name}</h3>
                  <div className="result-rating">
                    {getRatingStars(result.facility.performance.overall_rating)}
                    <span className="rating-value">
                      {result.facility.performance.overall_rating.toFixed(1)}
                    </span>
                  </div>
                </div>
                {getStatusBadge(result.is_available)}
              </div>

              <div className="result-info">
                <div className="info-item">
                  <MapPin size={16} />
                  <span>{result.distance_km} كم • {result.facility.district}</span>
                </div>
                <div className="info-item">
                  <Clock size={16} />
                  <span>وقت الانتظار: {result.estimated_wait_time} دقيقة</span>
                </div>
                <div className="info-item">
                  <TrendingUp size={16} />
                  <span>درجة التطابق: {result.relevance_score}%</span>
                </div>
              </div>

              {result.matched_specialties.length > 0 && (
                <div className="matched-specialties">
                  <strong>التخصصات المتوفرة:</strong>
                  <div className="specialty-tags">
                    {result.matched_specialties.map((spec, i) => (
                      <span key={i} className="specialty-tag">{spec}</span>
                    ))}
                  </div>
                </div>
              )}

              <div className="result-recommendation">
                <span className="recommendation-icon">💡</span>
                <span>{result.recommendation_reason}</span>
              </div>

              <div className="result-actions">
                <button 
                  className="action-btn primary"
                  onClick={() => viewFacilityDetails(result.facility.id)}
                >
                  <Calendar size={16} />
                  حجز موعد
                </button>
                <button className="action-btn secondary">
                  <Phone size={16} />
                  اتصال
                </button>
                <button className="action-btn secondary">
                  <Navigation size={16} />
                  التوجيه
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="no-results">
            <p>لا توجد نتائج. جرب تعديل الفلاتر أو البحث بكلمات مختلفة.</p>
          </div>
        )}
      </div>

      {/* Facility Details Modal */}
      {selectedFacility && (
        <div className="modal-overlay" onClick={() => setSelectedFacility(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{selectedFacility.name}</h2>
              <button onClick={() => setSelectedFacility(null)}>
                <X size={24} />
              </button>
            </div>
            <div className="modal-body">
              <div className="facility-detail-section">
                <h3>معلومات الاتصال</h3>
                <p>📞 {selectedFacility.phone}</p>
                <p>🚨 طوارئ: {selectedFacility.emergency_phone}</p>
                <p>📧 {selectedFacility.email}</p>
              </div>
              <div className="facility-detail-section">
                <h3>الموقع</h3>
                <p>{selectedFacility.address}</p>
                <p>{selectedFacility.district}, {selectedFacility.city}</p>
              </div>
              <div className="facility-detail-section">
                <h3>التصنيف</h3>
                <p>الجهة: {selectedFacility.organization}</p>
                <p>التجمع: {selectedFacility.cluster}</p>
              </div>
              <div className="facility-detail-section">
                <h3>القدرات</h3>
                <p>الأسرّة: {selectedFacility.total_beds}</p>
                <p>الأطباء: {selectedFacility.total_doctors}</p>
                <p>الإشغال: {selectedFacility.performance.current_occupancy}%</p>
              </div>
            </div>
            <div className="modal-footer">
              <button className="modal-btn primary">حجز موعد</button>
              <button className="modal-btn secondary">اتصال</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchPage;

