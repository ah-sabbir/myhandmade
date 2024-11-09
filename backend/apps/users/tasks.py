# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
import socket

User = get_user_model()

@shared_task
def send_verification_email(email=None, verification_link=None):
    if email and verification_link:
        # print("this is a token", email, verification_link)
    # print(verification_link)
        email = EmailMessage(
            'Verify Your Email',
            f'Click the link to verify your account: {verification_link}',
            settings.EMAIL_HOST_USER,
            [email]
        )
        email.fail_silently = False
        try:
            email.send()
        except socket.gaierror as e:
            print(e)
        except Exception as e:
            print(e)