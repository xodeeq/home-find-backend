from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls.base import reverse
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework import exceptions, serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from users.utils import send_email


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password", "is_agent")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(
        max_length=128, min_length=8, write_only=True)
    # full_name = serializers.ReadOnlyField(source="get_full_name")
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token_exp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = User
        fields = ("email", "full_name", "password", "access_token", "refresh_token", "access_token_exp")
        read_only_fields = ["full_name", "access_token", "refresh_token", "access_token_exp"]

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")
        
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        
        user_tokens = user.tokens()

        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh')),
            'access_token_exp': user_tokens.get('access_token_exp'),
        }
    

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get('email')

        if User.objects.filter(email=email).exists():
            user = user.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            sit_domain = get_current_site(request).domain
            relative_link = reverse(
                "users:password-reset-confirm",
                kwargs={"uidb64": uidb64, "token": token},
            )
            abs_url = f"https://{sit_domain}{relative_link}"
            email_body = f"Hello,\nPlease use the link below to reset your password, but only if you did request a password reset.\n{abs_url}\nBest,\nBabatunde."
            data = {
                "to_email": user.email,
                "email_subject": "Reset you Estate Link password",
                "email_body": email_body,
            }
            send_email(data)

        return super().validate(attrs)
    

class NewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password", None)
            token = attrs.get("token", None)
            uidb64 = attrs.get("uidb64", None)

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("The reset link is invalid", 401)

            user.set_password(password)
            user.save()

            return user

        except Exception as ex:
            return AuthenticationFailed("Unable to reset password", 401)
        

class TokenBlacklistSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(min_length=1, write_only=True)

    default_error_message = {
        'bad_token': ('Token is inalid or has expired')
    }

    class Meta:
        fields = ["refresh_token"]

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return super().validate(attrs)
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token ')