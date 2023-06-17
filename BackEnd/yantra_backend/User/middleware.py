from django.urls import reverse
from django.http import HttpResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


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
            if request.path not in self.EXEMPT_URLS:
                auth_header = request.headers.get('HTTP_AUTHORIZATION', '')
                print(auth_header)
                if auth_header.startswith('Bearer '):
                    token = auth_header.split(' ',1)[1]
                    print(token)
                    jwt_authentication = JWTAuthentication()
                    request.user, _ = jwt_authentication.authenticate_credentials(token)
                    print(request.user)
                    if not request.user.is_authenticated:
                        # Return unauthorized response if the user is not authenticated
                        return HttpResponse('Unauthorized', status=401)
            response = self.get_response(request)
            return response
        except Exception as e:
            # Handle any exceptions that may occur during middleware processing
            return HttpResponse('Internal Server Error', status=500)
