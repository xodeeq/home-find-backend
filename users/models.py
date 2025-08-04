import jwt

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed

from users.managers import CustomUserManager

class User(AbstractUser):
    EMAIL = 'email'
    GOOGLE = 'google'
    FACEBOOK = 'facebook'

    AUTH_PROVIDERS = {
        EMAIL: "Email",
        GOOGLE: "Google",
        FACEBOOK: "Facebook",
    }

    username = None
    email = models.EmailField(_("email address"), unique=True, blank=False)
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_verified = models.BooleanField(_('Has user email been verified'), default=False)
    is_agent = models.BooleanField(_('Is user an agent'), default=False)
    auth_provider = models.CharField(max_length=8, choices=AUTH_PROVIDERS, default=EMAIL)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def __str__(self):
        return str(self.get_full_name)
    
    @property
    def get_full_name(self):
        return super().get_full_name()

    def tokens(self):
        if not self.is_active:
            raise AuthenticationFailed("User is not active")

        refresh = RefreshToken.for_user(self)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'access_token_exp': datetime.fromtimestamp(refresh.access_token['exp'])
        }
    


class OneTimePassword(models.Model):
    """User activation code, expires in 30 minutes!"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(
        max_length=6, help_text="A 6-character alphanumeric code")
    expires_at = models.DateTimeField(help_text="code validity period")

    def __str__(self):
        return f"Passcode for {self.user.first_name}"