from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED

from users.serializers import UserRegisterSerializer, LoginSerializer, PasswordResetRequestSerializer, NewPasswordSerializer, TokenBlacklistSerializer
from users.utils import send_user_verification_code
from users.models import OneTimePassword


User = get_user_model()


# Create your views here.
class RegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    # renderer_classes = (UserRenderer,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.data
            send_user_verification_code(user_data['email'])

            # user = User.objects.get(email=user_data["email"])
            # # token = RefreshToken.for_user(user).access_token

            # code = Util.generate_code(6)
            # expiry_time = timezone.now() + timedelta(minutes=30)
            # ActivationCode.objects.create(
            #     user=user, code=code, expires_at=expiry_time)

            # # current_site = get_current_site(request).domain
            # # relative_link = reverse("users:email-verify")
            # # abs_url = f"http://{current_site}{relative_link}?token={str(token)}"
            # # email_body = f"Hi {user.get_short_name()},\nPlease use the link below to verify your email on TSAP.\n{abs_url}\nBest,\nBabatunde Xodeeq.\nThe Study Abroad Program"
            # email_body = f"Use {code} as your activation code, expires at {expiry_time.strftime('%I:%M %p')}"
            # data = {
            #     "to_emails": [user.email],
            #     "email_subject": "Your TSAP email verification",
            #     "email_body": email_body,
            # }
            # Util.send_email(data)
            return Response(user_data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

class VerifyUserEmail(GenericAPIView):
    queryset = OneTimePassword.objects.all()
    permission_classes = [AllowAny]

    def post(self, request):
        otp_code = request.data.get('otp')
        try:
            user_code_obj = OneTimePassword.objects.get(code=otp_code)
            user = user_code_obj.user
            if not user.is_verified or not user.is_active:
                user.is_verified = True
                user.is_active = True
                user.save()
                return Response({
                    'message': "Account email verified successfully"
                }, status=HTTP_200_OK)
            return Response({
                'message': 'Account already verified'
            }, status=HTTP_204_NO_CONTENT)
        except OneTimePassword.DoesNotExist:
            return Response({
                'message': 'Invalid passcode'
            }, status=HTTP_400_BAD_REQUEST)
            
            
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    # authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={ 'request': request })
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={ 'request': request })
        serializer.is_valid(raise_exception=True)
        return Response({ 'message': "A password reset link has been sent to your email." }, status=HTTP_200_OK)
    

class PasswordResetConfirmView(GenericAPIView):
    def get(self, request, uidb64, token):
        # TODO: Move into serializers later
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                """Checks if user used token or not"""
                return Response(
                    {"error": "Token is invalid or has expired"},
                    HTTP_401_UNAUTHORIZED,
                )
            return Response(
                {
                    "success": True,
                    "message": "Credentials valid",
                    "uidb64": uidb64,
                    "token": token,
                },
                status= HTTP_200_OK,
            )
        except DjangoUnicodeDecodeError as ude:
            return Response(
                {"error": "Token is invalid or has expired"},
                HTTP_401_UNAUTHORIZED,
            )
        

class NewPasswordAPIView(GenericAPIView):
    serializer_class = NewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "Password changed successfully"},
            status=HTTP_200_OK,
        )
    

class LogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = TokenBlacklistSerializer  

    def post(self, request):
        serializer = self.serializer_class(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)