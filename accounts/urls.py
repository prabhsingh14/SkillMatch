from django.urls import path
from .views import UserListView, SendOTPView, VerifyOTPView, GoogleLoginView, UserDetailView, LogoutView, RoleAssignView, RoleListView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('users/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('users/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('users/google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('users/logout/', LogoutView.as_view(), name='logout'),
    path('users/roles/', RoleListView.as_view(), name='role-list'),
    path('users/assign-role/', RoleAssignView.as_view(), name='role-assign'),
]
