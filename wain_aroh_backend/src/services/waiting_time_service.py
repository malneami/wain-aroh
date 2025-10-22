"""
Waiting Time Service
Provides real-time waiting time estimates for facilities
"""

import random
from datetime import datetime, time

class WaitingTimeService:
    """
    Calculates and provides waiting time estimates
    """
    
    def __init__(self):
        # Simulated real-time data (in production, integrate with hospital systems)
        self.current_waiting_times = {}
    
    def get_waiting_time(self, facility_id, ctas_level, current_time=None):
        """
        Get estimated waiting time for a facility
        
        Args:
            facility_id: Facility ID
            ctas_level: CTAS level (1-5)
            current_time: Current time (for time-based estimates)
        
        Returns:
            Estimated waiting time in minutes
        """
        if current_time is None:
            current_time = datetime.now()
        
        # Base waiting times by CTAS level
        base_times = {
            1: 0,   # Immediate
            2: 5,   # < 15 min
            3: 20,  # < 30 min
            4: 45,  # < 60 min
            5: 60   # < 120 min
        }
        
        base_time = base_times.get(ctas_level, 30)
        
        # Adjust for time of day
        hour = current_time.hour
        
        # Peak hours (8am-12pm, 4pm-8pm)
        if (8 <= hour < 12) or (16 <= hour < 20):
            multiplier = 1.5
        # Night hours (8pm-6am)
        elif hour >= 20 or hour < 6:
            multiplier = 0.7
        # Normal hours
        else:
            multiplier = 1.0
        
        # Adjust for facility type
        facility_adjustments = {
            1: 1.0,   # Main hospital - standard
            2: 0.8,   # UCC Al Malqa - less busy
            3: 0.9,   # UCC Al Nakheel
            4: 0.7,   # UCC Al Olaya - least busy
            5: 0.85   # UCC Al Rabwa
        }
        
        facility_mult = facility_adjustments.get(facility_id, 1.0)
        
        # Calculate final estimate
        estimated_time = int(base_time * multiplier * facility_mult)
        
        # Add some randomness for realism
        estimated_time += random.randint(-5, 10)
        
        # Ensure minimum values
        if ctas_level == 1:
            estimated_time = 0
        elif estimated_time < 5:
            estimated_time = 5
        
        return max(0, estimated_time)
    
    def get_all_waiting_times(self, facilities, ctas_level):
        """Get waiting times for all facilities"""
        waiting_times = {}
        current_time = datetime.now()
        
        for facility in facilities:
            facility_id = facility.get('id')
            wait_time = self.get_waiting_time(facility_id, ctas_level, current_time)
            waiting_times[facility_id] = {
                "wait_time_minutes": wait_time,
                "wait_time_text": self.format_wait_time(wait_time),
                "status": self.get_status(wait_time, ctas_level)
            }
        
        return waiting_times
    
    def format_wait_time(self, minutes):
        """Format waiting time as text"""
        if minutes == 0:
            return "فوري"
        elif minutes < 15:
            return f"~{minutes} دقيقة"
        elif minutes < 60:
            return f"~{minutes} دقيقة"
        else:
            hours = minutes // 60
            mins = minutes % 60
            if mins == 0:
                return f"~{hours} ساعة"
            else:
                return f"~{hours} ساعة و {mins} دقيقة"
    
    def get_status(self, wait_time, ctas_level):
        """Get status indicator based on wait time"""
        # For critical cases (CTAS 1-2), any wait is concerning
        if ctas_level <= 2:
            if wait_time == 0:
                return "excellent"
            elif wait_time < 10:
                return "good"
            else:
                return "warning"
        
        # For urgent cases (CTAS 3)
        elif ctas_level == 3:
            if wait_time < 20:
                return "excellent"
            elif wait_time < 40:
                return "good"
            else:
                return "warning"
        
        # For less urgent (CTAS 4-5)
        else:
            if wait_time < 30:
                return "excellent"
            elif wait_time < 60:
                return "good"
            else:
                return "warning"
    
    def get_best_facility_by_wait_time(self, facilities, ctas_level, max_wait_time=None):
        """
        Find facility with shortest wait time
        
        Args:
            facilities: List of facilities
            ctas_level: CTAS level
            max_wait_time: Maximum acceptable wait time (optional)
        
        Returns:
            Best facility with wait time info
        """
        waiting_times = self.get_all_waiting_times(facilities, ctas_level)
        
        # Filter by max wait time if specified
        if max_wait_time:
            facilities = [f for f in facilities 
                         if waiting_times[f['id']]['wait_time_minutes'] <= max_wait_time]
        
        if not facilities:
            return None
        
        # Sort by wait time
        best_facility = min(facilities, 
                           key=lambda f: waiting_times[f['id']]['wait_time_minutes'])
        
        return {
            "facility": best_facility,
            "wait_time": waiting_times[best_facility['id']]
        }
    
    def update_waiting_time(self, facility_id, wait_time):
        """Update waiting time (for real-time integration)"""
        self.current_waiting_times[facility_id] = {
            "time": datetime.now(),
            "wait_time": wait_time
        }

# Global instance
waiting_time_service = WaitingTimeService()

