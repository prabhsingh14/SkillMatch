from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer
from .models import CustomUser, EmailOTP
import requests

#list all users -- admin only
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

#create user -- signup
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user, created = CustomUser.objects.get_or_create(email=email)

        otp = EmailOTP.objects.create(user=user)

        send_mail(
            subject='OTP for SkillMatch',
            message=f"Your OTP is {otp.code}. It is valid for 5 minutes.",
            from_email='prabhsingh1407@gmail.com',
            recipient_list=[email]
        )

        return Response({
            "detail": "OTP sent successfully"
        }, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        user = CustomUser.objects.get(email=email)
        try:
            otp = EmailOTP.objects.filter(user=user, code=code, is_used=False).latest('created_at')
        except EmailOTP.DoesNotExist:
            return Response({
                "error": "Invalid or expired OTP"
            }, status=status.HTTP_400_BAD_REQUEST)

        if timezone.now() - otp.created_at > timedelta(minutes=5):
            return Response({
                "error": "OTP expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        otp.is_used = True
        otp.save()

        #auto login
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "detail": "Login successful!"
        }, status=status.HTTP_200_OK)

class GoogleLoginView(APIView):
    def post(self, request):
        token = request.data.get('token') #from frontend, google will receive token
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        #token verification
        google_url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
        response = requests.get(google_url)
        if response.status_code != 200:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        email = data.get('email')
        name = data.get('name')

        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = CustomUser.objects.get_or_create(email=email, defaults={'phone': '', 'role': 'candidate'})

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": email,
            "name": user.first_name,
            "is_new_user": created
        }, status=status.HTTP_200_OK)
