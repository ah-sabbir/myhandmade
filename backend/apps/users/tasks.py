# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@shared_task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    token = RefreshToken.for_user(user).access_token
    verification_link = request.build_absolute_uri(
                reverse('email-verify') + f'?token={str(token)}'
            )
    token = RefreshToken.for_user(user).access_token
    print("this is a token", token)
    # print(verification_link)
    # email = EmailMessage(
    #     'Verify Your Email',
    #     f'Click the link to verify your account: {verification_link}',
    #     settings.EMAIL_HOST_USER,
    #     [user.email]
    # )
    # email.fail_silently = False
    # try:
    #     email.send()
    # except socket.gaierror as e:
    #     print(e)
    # except Exception as e:
    #     pass