from rest_framework import serializers
from .models import CustomUser, EmailOTP

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'is_staff', 'is_active', 'date_joined']

class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = CustomUser.objects.get(email=data['email'])
            otp = EmailOTP.objects.get(user=user, code=data['code'], is_used=False)

        except (CustomUser.DoesNotExist, EmailOTP.DoesNotExist):
            raise serializers.ValidationError("Invalid email or OTP code.")
        
        return data