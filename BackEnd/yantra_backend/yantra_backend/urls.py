"""yantra_backend URL Configuration
"""

from django.contrib import admin
from django.urls import path, include

from User.views import CustomUserRegistrationAPIView, OTPVerificationAPIView, ResendOTPVerificationAPIView, CustomUserLoginAPIView, ResetPasswordAPIView, CustomUserDetailsAPIView, CustomUserChangePasswordAPIView
from File.views import FileUploadAPIView, UserFileListAPIView, FileDownloadAPIView, FileDeleteAPIView
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('register', CustomUserRegistrationAPIView.as_view(), name='register'),
    path('verify-otp', OTPVerificationAPIView.as_view(), name='verify-otp'),
    path('resend-otp', ResendOTPVerificationAPIView.as_view(), name='resend-otp'),
    path('login', CustomUserLoginAPIView.as_view(), name='login'),
    path('logout', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('forgot-pass', ResendOTPVerificationAPIView.as_view(), name='forgot-pass'),
    path('reset-pass', ResetPasswordAPIView.as_view(), name='reset-pass'),
    path('upload-file', FileUploadAPIView.as_view(), name='upload-file'),
    path('getAllFiles', UserFileListAPIView.as_view(), name='get-all-files'),
    path('download/<uuid:file_id>/', FileDownloadAPIView.as_view(),name='download-result-file'),
    path('delete/<uuid:file_id>/', FileDeleteAPIView.as_view(),name='delete-file'),
    path('me', CustomUserDetailsAPIView.as_view(), name='me'),
    path('change-pass', CustomUserChangePasswordAPIView.as_view(), name='change-pass'),
]
