import random
from django.core.mail import send_mail
from django.conf import settings

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = "🔐 Your OTP for Joining Arjungeria Agni Sangha Football Club"
    message = f"Hi,\n\nYour OTP for joining the club is: {otp}\n\nThis OTP is valid for 5 minutes. Please enter it to complete your registration.\n\nBest regards,\nArjungeria Agni Sangha Football Club"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )