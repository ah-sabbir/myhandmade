from django.urls import path
from .views import UserRegisterView, UserLoginView, GetUser, VerifyEmail

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profiles', GetUser.as_view(), name='getuser'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
]
