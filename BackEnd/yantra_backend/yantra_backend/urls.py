"""yantra_backend URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

from User.views import CustomUserRegistrationAPIView, OTPVerificationAPIView, ResendOTPVerificationAPIView, CustomUserLoginAPIView, ResetPasswordAPIView
from File.views import FileUploadAPIView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register', CustomUserRegistrationAPIView.as_view(), name='register'),
    path('verify-otp', OTPVerificationAPIView.as_view(), name='verify-otp'),
    path('resend-otp', ResendOTPVerificationAPIView.as_view(), name='resend-otp'),
    path('login', CustomUserLoginAPIView.as_view(), name='login'),
    path('forgot-pass', ResendOTPVerificationAPIView.as_view(), name='forgot-pass'),
    path('reset-pass', ResetPasswordAPIView.as_view(), name='reset-pass'),
    path('upload-file', FileUploadAPIView.as_view(), name='upload-file')
]
