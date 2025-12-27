import uuid
from django.utils.deprecation import MiddlewareMixin

class AnonymousSessionMiddleware(MiddlewareMixin):
    COOKIE_NAME = "anonymous_session_id"

    def process_request(self, request):
        session_id = request.COOKIES.get(self.COOKIE_NAME)

        if not session_id:
            session_id = str(uuid.uuid4())
            request.new_session_id = session_id
        else:
            request.new_session_id = None

        request.session_id = session_id

    def process_response(self, request, response):
        if hasattr(request, "new_session_id") and request.new_session_id:
            response.set_cookie(
                self.COOKIE_NAME,
                request.new_session_id,
                max_age=60 * 60 * 24,  # 24 hours
                httponly=True,
                samesite="Lax",
            )
        return response
