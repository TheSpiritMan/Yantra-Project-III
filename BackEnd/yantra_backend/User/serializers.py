from rest_framework import serializers
from .models import CustomUser
from django.utils import timezone
from datetime import timedelta
from random import randint
from django.core.mail import send_mail
from django.conf import settings

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)

        generate_otp(user)
        user.save()
        return user

def send_otp_verification_mail(email, otp):
    subject = 'Email OTP Verification'
    message = f'Your OTP is: {otp}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def generate_otp(user):
    otp_num = str(randint(100000,999999))
    otp_end = timezone.now() + timedelta(minutes=1, seconds=30)
    user.otp_num = otp_num
    user.otp_end = otp_end
    user.save()    

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(min_length=6, max_length=6)

class OTPRegenerateSerializer(serializers.Serializer):
    email = serializers.EmailField()