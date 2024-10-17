from django.urls import path
from .views import UserRegisterView, UserLoginView, GetUser

urlpatterns = [
    path('register', UserRegisterView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),
    path('profiles', GetUser.as_view(), name='GetUser'),
]
