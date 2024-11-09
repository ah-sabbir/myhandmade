from django.urls import path # type: ignore
from .views import UserRegisterView, UserLoginView, GetUser, VerifyEmail, UserUpdateView
from rest_framework.authtoken.views import obtain_auth_token # type: ignore

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profiles', GetUser.as_view(), name='getuser'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('update', UserUpdateView.as_view(), name= 'user-update' )
    # path('email-verify/<str:token>', VerifyEmail.as_view(), name='email-verify'),
    # path('token', obtain_auth_token, name='api_token_auth'),
]
