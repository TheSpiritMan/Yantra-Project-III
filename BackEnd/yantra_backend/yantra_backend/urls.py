"""yantra_backend URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

from User.views import UserRegistrationAPIView, OTPVerificationAPIView, ResendOTPVerificationAPIView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register', UserRegistrationAPIView.as_view()),
    path('verify-otp', OTPVerificationAPIView.as_view()),
    path('resend-otp', ResendOTPVerificationAPIView.as_view())
]
