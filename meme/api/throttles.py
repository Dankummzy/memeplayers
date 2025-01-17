# throttles.py
from rest_framework.throttling import UserRateThrottle

class VoteThrottle(UserRateThrottle):
    scope = "vote"  # Custom scope for voting

class PostThrottle(UserRateThrottle):
    scope = "post"  # Custom scope for posting
