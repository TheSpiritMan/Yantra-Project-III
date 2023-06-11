from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, OTPVerificationSerializer, OTPRegenerateSerializer, send_otp_verification_mail, generate_otp

class UserRegistrationAPIView(APIView):
    def post(self, request):
        try:
            serializer = CustomUserSerializer(data=request.data)
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