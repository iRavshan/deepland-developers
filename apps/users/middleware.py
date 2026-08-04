from django.utils import timezone
from datetime import timedelta
from apps.users.models import UserSession

class ActiveUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Ensure user is authenticated and session_key is available
        if hasattr(request, 'user') and request.user.is_authenticated and request.session.session_key:
            session_key = request.session.session_key
            try:
                user_session = UserSession.objects.get(session_key=session_key)
                
                # Update last_activity if it's older than 1 minute to avoid DB spam on every request
                now = timezone.now()
                if now - user_session.last_activity > timedelta(minutes=1):
                    user_session.last_activity = now
                    # We use update() to avoid triggering post_save signals or overriding other changes
                    UserSession.objects.filter(id=user_session.id).update(last_activity=now)
            except UserSession.DoesNotExist:
                pass

        return response
