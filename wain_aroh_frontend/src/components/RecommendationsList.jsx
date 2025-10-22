import React, { useState } from 'react';
import './RecommendationsList.css';

const RecommendationsList = ({ recommendations, onActionClick }) => {
  const [expandedId, setExpandedId] = useState(null);

  if (!recommendations || recommendations.length === 0) {
    return null;
  }

  const getUrgencyColor = (priority, isUrgent) => {
    if (isUrgent) return '#dc3545';
    switch (priority) {
      case 'high': return '#fd7e14';
      case 'medium': return '#ffc107';
      case 'low': return '#28a745';
      default: return '#6c757d';
    }
  };

  const handleActionClick = (recommendation) => {
    if (onActionClick) {
      onActionClick(recommendation);
    }
  };

  return (
    <div className="recommendations-container">
      <div className="recommendations-header">
        <h3>📋 التوصيات والإجراءات</h3>
        <p>اختر الإجراء المناسب لحالتك</p>
      </div>

      <div className="recommendations-list">
        {recommendations.map((rec, index) => (
          <div 
            key={index} 
            className={`recommendation-card ${rec.is_urgent ? 'urgent' : ''}`}
            style={{ borderRightColor: getUrgencyColor(rec.priority, rec.is_urgent) }}
          >
            <div className="recommendation-header">
              <div className="recommendation-icon">{rec.icon}</div>
              <div className="recommendation-title">
                <h4>{rec.title}</h4>
                {rec.is_urgent && <span className="urgent-badge">عاجل</span>}
                {rec.requires_doctor_approval && <span className="approval-badge">يتطلب موافقة</span>}
              </div>
            </div>

            <div className="recommendation-body">
              <p className="recommendation-description">{rec.description}</p>
              
              {expandedId === index && rec.action_data && (
                <div className="recommendation-details">
                  <h5>تفاصيل إضافية:</h5>
                  <ul>
                    {Object.entries(rec.action_data).map(([key, value]) => (
                      <li key={key}>
                        <strong>{key}:</strong> {typeof value === 'object' ? JSON.stringify(value) : value}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            <div className="recommendation-footer">
              <button
                className={`action-button ${rec.is_urgent ? 'urgent-action' : ''}`}
                onClick={() => handleActionClick(rec)}
              >
                {rec.button_text}
              </button>
              
              {rec.action_data && Object.keys(rec.action_data).length > 0 && (
                <button
                  className="details-button"
                  onClick={() => setExpandedId(expandedId === index ? null : index)}
                >
                  {expandedId === index ? 'إخفاء التفاصيل' : 'عرض التفاصيل'}
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      {recommendations.some(r => r.is_urgent) && (
        <div className="urgent-notice">
          ⚠️ <strong>تنبيه:</strong> لديك توصيات عاجلة تتطلب اهتماماً فورياً
        </div>
      )}
    </div>
  );
};

export default RecommendationsList;

