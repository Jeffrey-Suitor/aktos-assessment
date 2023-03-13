from rest_framework.throttling import UserRateThrottle

# Default values are configured in settings.py
class BurstThrottle(UserRateThrottle):
    scope = 'burst'
    
class ContinousThrottle(UserRateThrottle):
    scope = 'continous'