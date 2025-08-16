from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .serializers import UserSerializer, SendOTPSerializer, VerifyOTPSerializer
from .models import CustomUser, EmailOTP

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
