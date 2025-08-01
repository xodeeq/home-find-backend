import random
from datetime import datetime, timedelta

from django.utils import timezone
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.conf import settings

from users.models import OneTimePassword


User = get_user_model()


def send_email(data):
    email = EmailMessage(
        from_email = settings.EMAIL_HOST_USER,
        to=[data["to_email"]],
        subject=data["email_subject"],
        body=data["email_body"],
    )
    email.send()


def generateOTP():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1, 9))
    return otp

def send_user_verification_code(email):
    subject = "One time passcode for Email verification"
    otp_code = generateOTP()
    print(otp_code)
    user = User.objects.get(email=email)
    current_site = "Estate Link"
    expiry_time = timezone.now() + timedelta(minutes=30)
    email_body = f"Hello {user.first_name},\nWelcome to {current_site} \nUse the code {otp_code} to verify your account. Only valid till {expiry_time.strftime('%I:%M %p')}"
    from_email = settings.DEFAULT_FROM_EMAIL

    OneTimePassword.objects.create(
        user=user, code=otp_code, expires_at=expiry_time
    )
    email_message = EmailMessage(
        to=[email],
        subject=subject,
        body=email_body,
        from_email=from_email
    )
    email_message.send(fail_silently=True)