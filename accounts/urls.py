from django.urls import path
from .views import UserListView, UserCreateView, SendOTPView, VerifyOTPView, GoogleLoginView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/register/', UserCreateView.as_view(), name='user-register'),
    path('users/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('users/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('users/google-login/', GoogleLoginView.as_view(), name='google-login'),
]
