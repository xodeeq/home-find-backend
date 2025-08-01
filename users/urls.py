from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterAPIView, VerifyUserEmail, LoginAPIView, PasswordResetRequestView, PasswordResetConfirmView, NewPasswordAPIView, LogoutAPIView


app_name = "users"

urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("verify-email/", VerifyUserEmail.as_view(), name="verify"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path("password-update/", NewPasswordAPIView.as_view(), name="password-update"),
    path("logout/", LogoutAPIView.as_view(), name="logout")
]