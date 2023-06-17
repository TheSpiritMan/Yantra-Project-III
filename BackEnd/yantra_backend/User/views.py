from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserRegistrationSerializer, OTPVerificationSerializer, OTPRegenerateSerializer, send_otp_verification_mail, generate_otp, CustomUserLoginSerializer, PasswordResetSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUserRegistrationAPIView(APIView):
    def post(self, request):
        try:
            serializer = CustomUserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()  
                send_otp_verification_mail(user.email, user.otp_num)
                return Response({'message': 'User registered successfully\n Check your email for OTP Verification'})
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=400)


class OTPVerificationAPIView(APIView):
    def post(self, request):
        try:
            serializer = OTPVerificationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            # Verification logic
            user = CustomUser.objects.get(email=email)
            if otp == user.otp_num:
                if(user.is_otp_valid()):
                    user.is_verified = True
                    user.otp_num=''
                    user.save()
                    return Response({'message': 'OTP verification successful'})
                else:
                    return Response({'message': 'OTP has expired'}, status=400)
            else:
                return Response({'message': 'Invalid OTP'})
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=400)


class ResendOTPVerificationAPIView(APIView):
    def post(self, request):
        try: 
            serializer = OTPRegenerateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']

            user = CustomUser.objects.get(email=email)
            generate_otp(user)
            send_otp_verification_mail(user.email, user.otp_num)
            return Response({'message': 'OTP Send successful'})
        except Exception as e:
            return Response({'message': str(e)}, status=400)

class CustomUserLoginAPIView(APIView):
    def post(self, request):
        try:
            serializer = CustomUserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Authenticate user using username
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_verified:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'message': 'Login successful',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
                else:
                    return Response({'message': 'User Not Verified'}, status=400)
            else:
                return Response({'message': 'Invalid username or password'}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=500)

class ResetPasswordAPIView(APIView):
    def post(self, request):
        try:
            serializer = PasswordResetSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']

            # Verification logic
            user = CustomUser.objects.get(email=email)
            if otp == user.otp_num:
                if(user.is_otp_valid()):
                    user.set_password(new_password)
                    user.otp_num=''
                    user.save()
                    return Response({'message': 'Password Changed Successfully'})
                else:
                    return Response({'message': 'OTP has expired'}, status=400)
            else:
                return Response({'message': 'Invalid OTP'})
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=400)
