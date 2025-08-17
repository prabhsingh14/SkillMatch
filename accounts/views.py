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
from utils.get_tokens_for_users import get_tokens_for_user

#list all users -- admin only
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

#retrieve, update, delete user -- user detail view
class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

#send otp
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

#verify otp
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

        tokens = get_tokens_for_user(user)

        return Response({
            **tokens,
            "detail": "Login successful!",
        }, status=status.HTTP_200_OK)

#login via google
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

        tokens = get_tokens_for_user(user)

        return Response({
            **tokens,
            "email": email,
            "name": user.first_name,
            "is_new_user": created
        }, status=status.HTTP_200_OK)

#logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#list available roles
class RoleListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        roles = [choice[0] for choice in CustomUser.ROLE_CHOICES]
        return Response({"roles": roles}, status=status.HTTP_200_OK)

#assign or update logged-in user's role
class RoleAssignView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        role = request.data.get("role")
        if role not in dict(CustomUser.ROLE_CHOICES):
            return Response({
                "error": "Invalid role",
            }, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.role = role
        user.save()

        return Response({"detail": "Role updated successfully"}, status=status.HTTP_200_OK)