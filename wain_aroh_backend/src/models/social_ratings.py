"""
Social Media Ratings Model
تقييمات مواقع التواصل الاجتماعي
"""

from src.models.user import db
from datetime import datetime


class SocialMediaRating(db.Model):
    """Social media ratings and reviews for facilities"""
    __tablename__ = 'social_media_ratings'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    
    # Platform information
    platform = db.Column(db.String(50), nullable=False)  # twitter, instagram, google_maps, facebook
    platform_url = db.Column(db.String(500))
    
    # Rating information
    overall_rating = db.Column(db.Float)  # 0-5
    total_reviews = db.Column(db.Integer, default=0)
    positive_reviews = db.Column(db.Integer, default=0)
    negative_reviews = db.Column(db.Integer, default=0)
    neutral_reviews = db.Column(db.Integer, default=0)
    
    # Sentiment analysis
    sentiment_score = db.Column(db.Float)  # -1 to 1
    
    # Common keywords from reviews
    common_positive_keywords = db.Column(db.Text)  # JSON array
    common_negative_keywords = db.Column(db.Text)  # JSON array
    
    # Timestamps
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    hospital = db.relationship('Hospital', backref=db.backref('social_ratings', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'platform': self.platform,
            'platform_url': self.platform_url,
            'overall_rating': self.overall_rating,
            'total_reviews': self.total_reviews,
            'positive_reviews': self.positive_reviews,
            'negative_reviews': self.negative_reviews,
            'neutral_reviews': self.neutral_reviews,
            'sentiment_score': self.sentiment_score,
            'common_positive_keywords': self.common_positive_keywords,
            'common_negative_keywords': self.common_negative_keywords,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class FacilityReview(db.Model):
    """Individual reviews from social media"""
    __tablename__ = 'facility_reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    
    # Review information
    platform = db.Column(db.String(50), nullable=False)
    author_name = db.Column(db.String(200))
    review_text = db.Column(db.Text)
    rating = db.Column(db.Float)  # 0-5
    
    # Sentiment
    sentiment = db.Column(db.String(20))  # positive, negative, neutral
    sentiment_score = db.Column(db.Float)  # -1 to 1
    
    # Timestamps
    review_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    hospital = db.relationship('Hospital', backref=db.backref('reviews', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'hospital_id': self.hospital_id,
            'platform': self.platform,
            'author_name': self.author_name,
            'review_text': self.review_text,
            'rating': self.rating,
            'sentiment': self.sentiment,
            'sentiment_score': self.sentiment_score,
            'review_date': self.review_date.isoformat() if self.review_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

