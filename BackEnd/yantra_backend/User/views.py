from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserRegistrationSerializer, OTPVerificationSerializer, OTPRegenerateSerializer, send_otp_verification_mail, generate_otp, CustomUserLoginSerializer, PasswordResetSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


class CustomUserRegistrationAPIView(APIView):
    def post(self, request):
        try:
            serializer = CustomUserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()  
                send_otp_verification_mail(user.email, user.otp_num)
                return Response({'message': 'User registered successfully. Check your email for OTP Verification'}, status=200)
            return Response(serializer.errors, status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=201)


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
                    return Response({'message': 'OTP verification successful'}, status=200)
                else:
                    return Response({'message': 'OTP has expired'}, status=201)
            else:
                return Response({'message': 'Invalid OTP'}, status=201)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=201)


class ResendOTPVerificationAPIView(APIView):
    def post(self, request):
        try: 
            serializer = OTPRegenerateSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']

            user = CustomUser.objects.get(email=email)
            generate_otp(user)
            send_otp_verification_mail(user.email, user.otp_num)
            return Response({'message': 'OTP Send successful'}, status=200)
        except Exception as e:
            return Response({'message': 'Email Not Exist'}, status=201)

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
                    }, status=200)
                else:
                    return Response({'message': 'User Not Verified'}, status=201)
            else:
                return Response({'message': 'Invalid username or password'}, status=201)
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
                    return Response({'message': 'Password Changed Successfully'}, status=200)
                else:
                    return Response({'message': 'OTP has expired'}, status=201)
            else:
                return Response({'message': 'Invalid OTP'}, status=201)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User not found'}, status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=201)


class CustomUserDetailsAPIView(APIView):
    def get(self, request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            user_data = {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email
            }
            return Response(user_data, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=201)

class CustomUserChangePasswordAPIView(APIView):
    def post(self, request):
        try:
            serializer = ChangePasswordSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = CustomUser.objects.get(id=request.user.id)
            new_password = serializer.validated_data['new_password']

            # Validate and update the password
            if new_password:
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=200)
            else:
                return Response({'error': 'Invalid or missing password'}, status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=201)