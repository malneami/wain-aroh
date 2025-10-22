"""
Social Media Ratings Service
خدمة تقييمات مواقع التواصل الاجتماعي
"""

import random
import json
from datetime import datetime, timedelta


class SocialMediaService:
    """Service for managing social media ratings"""
    
    def __init__(self):
        self.platforms = ['twitter', 'google_maps', 'instagram', 'facebook']
        
        # Common positive keywords in Arabic
        self.positive_keywords_ar = [
            'ممتاز', 'رائع', 'نظيف', 'سريع', 'محترف', 'طاقم ممتاز',
            'خدمة جيدة', 'أطباء مهرة', 'تعامل راقي', 'مستشفى نظيف'
        ]
        
        # Common negative keywords in Arabic
        self.negative_keywords_ar = [
            'انتظار طويل', 'ازدحام', 'بطيء', 'سيء', 'غير منظم',
            'خدمة سيئة', 'موظفين غير متعاونين', 'مواعيد متأخرة'
        ]
    
    def generate_mock_ratings(self, hospital_id, hospital_name, facility_type='hospital'):
        """
        Generate mock social media ratings for a facility
        
        Args:
            hospital_id: Hospital ID
            hospital_name: Hospital name
            facility_type: Type of facility
            
        Returns:
            Dictionary with ratings data
        """
        # Base rating varies by facility type
        if facility_type == 'hospital':
            base_rating = random.uniform(3.8, 4.7)
        elif facility_type == 'clinic':
            base_rating = random.uniform(4.0, 4.8)
        else:
            base_rating = random.uniform(3.5, 4.5)
        
        ratings = {}
        
        for platform in self.platforms:
            # Generate platform-specific rating
            platform_rating = base_rating + random.uniform(-0.3, 0.3)
            platform_rating = max(1.0, min(5.0, platform_rating))  # Clamp between 1-5
            
            # Generate review counts
            if platform == 'google_maps':
                total_reviews = random.randint(150, 500)
            elif platform == 'twitter':
                total_reviews = random.randint(50, 200)
            elif platform == 'instagram':
                total_reviews = random.randint(30, 150)
            else:  # facebook
                total_reviews = random.randint(40, 180)
            
            # Calculate positive/negative/neutral distribution
            positive_ratio = (platform_rating - 1) / 4  # 0-1 scale
            positive_reviews = int(total_reviews * positive_ratio * random.uniform(0.85, 0.95))
            negative_reviews = int(total_reviews * (1 - positive_ratio) * random.uniform(0.3, 0.5))
            neutral_reviews = total_reviews - positive_reviews - negative_reviews
            
            # Sentiment score (-1 to 1)
            sentiment_score = (platform_rating - 3) / 2
            
            # Select random keywords
            num_positive = random.randint(3, 5)
            num_negative = random.randint(2, 4)
            
            positive_keywords = random.sample(self.positive_keywords_ar, num_positive)
            negative_keywords = random.sample(self.negative_keywords_ar, num_negative)
            
            ratings[platform] = {
                'platform': platform,
                'platform_url': self._generate_platform_url(platform, hospital_name),
                'overall_rating': round(platform_rating, 1),
                'total_reviews': total_reviews,
                'positive_reviews': positive_reviews,
                'negative_reviews': negative_reviews,
                'neutral_reviews': neutral_reviews,
                'sentiment_score': round(sentiment_score, 2),
                'common_positive_keywords': json.dumps(positive_keywords, ensure_ascii=False),
                'common_negative_keywords': json.dumps(negative_keywords, ensure_ascii=False),
                'last_updated': datetime.now().isoformat()
            }
        
        # Calculate aggregate rating
        aggregate = self._calculate_aggregate_rating(ratings)
        
        return {
            'hospital_id': hospital_id,
            'platforms': ratings,
            'aggregate': aggregate
        }
    
    def _generate_platform_url(self, platform, hospital_name):
        """Generate mock platform URL"""
        if platform == 'google_maps':
            return f"https://www.google.com/maps/search/{hospital_name.replace(' ', '+')}"
        elif platform == 'twitter':
            return f"https://twitter.com/search?q={hospital_name.replace(' ', '+')}"
        elif platform == 'instagram':
            return f"https://www.instagram.com/explore/tags/{hospital_name.replace(' ', '')}"
        else:  # facebook
            return f"https://www.facebook.com/search/top?q={hospital_name.replace(' ', '+')}"
    
    def _calculate_aggregate_rating(self, platform_ratings):
        """Calculate aggregate rating from all platforms"""
        total_rating = 0
        total_reviews = 0
        total_positive = 0
        total_negative = 0
        total_neutral = 0
        sentiment_scores = []
        
        for platform_data in platform_ratings.values():
            # Weight by number of reviews
            weight = platform_data['total_reviews']
            total_rating += platform_data['overall_rating'] * weight
            total_reviews += platform_data['total_reviews']
            total_positive += platform_data['positive_reviews']
            total_negative += platform_data['negative_reviews']
            total_neutral += platform_data['neutral_reviews']
            sentiment_scores.append(platform_data['sentiment_score'])
        
        avg_rating = total_rating / total_reviews if total_reviews > 0 else 0
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        
        return {
            'overall_rating': round(avg_rating, 1),
            'total_reviews': total_reviews,
            'positive_reviews': total_positive,
            'negative_reviews': total_negative,
            'neutral_reviews': total_neutral,
            'sentiment_score': round(avg_sentiment, 2),
            'platforms_count': len(platform_ratings)
        }
    
    def get_recent_reviews(self, hospital_id, limit=10):
        """
        Get recent reviews for a facility
        
        Args:
            hospital_id: Hospital ID
            limit: Number of reviews to return
            
        Returns:
            List of recent reviews
        """
        reviews = []
        
        # Generate mock reviews
        platforms = random.sample(self.platforms, k=random.randint(2, 4))
        
        for i in range(limit):
            platform = random.choice(platforms)
            rating = random.uniform(3.0, 5.0)
            sentiment = 'positive' if rating >= 4.0 else ('negative' if rating < 3.0 else 'neutral')
            
            # Generate review text based on sentiment
            if sentiment == 'positive':
                review_text = random.choice([
                    'خدمة ممتازة وطاقم محترف',
                    'تعامل راقي ومستشفى نظيف',
                    'أطباء مهرة وخدمة سريعة',
                    'تجربة رائعة والحمد لله'
                ])
            elif sentiment == 'negative':
                review_text = random.choice([
                    'انتظار طويل جداً',
                    'ازدحام شديد',
                    'خدمة بطيئة',
                    'تنظيم غير جيد'
                ])
            else:
                review_text = random.choice([
                    'خدمة عادية',
                    'تجربة متوسطة',
                    'يحتاج تحسين',
                    'مقبول'
                ])
            
            review_date = datetime.now() - timedelta(days=random.randint(1, 90))
            
            reviews.append({
                'id': i + 1,
                'hospital_id': hospital_id,
                'platform': platform,
                'author_name': f'مستخدم {i+1}',
                'review_text': review_text,
                'rating': round(rating, 1),
                'sentiment': sentiment,
                'sentiment_score': round((rating - 3) / 2, 2),
                'review_date': review_date.isoformat(),
                'created_at': review_date.isoformat()
            })
        
        # Sort by date descending
        reviews.sort(key=lambda x: x['review_date'], reverse=True)
        
        return reviews


# Global instance
social_media_service = SocialMediaService()

