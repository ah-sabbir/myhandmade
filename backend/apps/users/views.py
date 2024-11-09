from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.views import APIView # type: ignore
from django.core.mail import send_mail # type: ignore
from django.contrib.auth import authenticate # type: ignore
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer, UserUpdateSerializer
from rest_framework.authtoken.models import Token # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from django.urls import reverse # type: ignore
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated # type: ignore
from .models import User
from .tasks import send_verification_email
import json
import jwt

from django.core.mail import EmailMessage
import socket

from django.conf import settings



class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # token = RefreshToken.for_user(user).access_token
            # verification_link = request.build_absolute_uri(
            #             reverse('email-verify') + f'?token={str(token)}'
            #         )
            send_verification_email.delay(user.id)
            return Response({'email':user.email, 'message': 'An verification mail has been sent. Verify your email.'}, status=status.HTTP_201_CREATED) #,
            # return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                # checking if user authenticated or not
                isAuthenticated = authenticate(email=email, password=password)
                
                if isAuthenticated is not None:
                    token, _ = Token.objects.get_or_create(user=isAuthenticated)

                    # Serialize the authenticated user data
                    user_data = UserLoginSerializer(user).data

                    return Response({"token": token.key, "user": user_data}, status=status.HTTP_200_OK) # type: ignore
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
            except User.DoesNotExist:
                return Response({"error":"invalid user"}, status= status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get(self, request):
        users = User.objects.all()  # Get all users

        serializer = UserSerializer(users, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data

class VerifyEmail(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        token = request.GET.get('token')  # Get the token from the URL
        # email = request.GET.get('email')  # Get the email from the URL

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            user.email_verified = True
            user.save()
        except Exception as e:
            print(e)
            return Response({'status':'fail', 'message': 'something went wrong'}, status=status.HTTP_303_SEE_OTHER)

        return Response({'status': 'success', 'message': 'Email verified successfully!'}, status=status.HTTP_200_OK)


class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Assuming the user updates their profile

 