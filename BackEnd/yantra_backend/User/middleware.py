from django.urls import reverse
from django.http import HttpResponse

class JWTMiddleware:
    EXEMPT_URLS = [
        reverse('register'),  
        reverse('verify-otp'),
        reverse('resend-otp'),
        reverse('login'),
        reverse('forgot-pass'),
        reverse('reset-pass'),
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if not request.user.is_authenticated and request.path not in self.EXEMPT_URLS:
                # Return unauthorized response if the user is not authenticated and the URL is not exempted
                return HttpResponse('Unauthorized', status=401)

            response = self.get_response(request)
            return response
        except Exception as e:
            # Handle any exceptions that may occur during middleware processing
            return HttpResponse('Internal Server Error', status=500)
