from django.utils.deprecation import MiddlewareMixin
from .models import Notification

class NotificationMiddleware(MiddlewareMixin):
    """
    Middleware to add unread notifications count to the request context
    for authenticated users.
    """
    
    def process_request(self, request):
        if request.user.is_authenticated:
            # Add unread notifications count to request
            request.unread_notifications_count = Notification.objects.filter(
                user=request.user, 
                is_read=False
            ).count()
        return None
