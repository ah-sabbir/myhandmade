from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore
from rest_framework.views import APIView # type: ignore
from django.core.mail import send_mail # type: ignore
from django.contrib.auth import authenticate # type: ignore
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token # type: ignore
from rest_framework.permissions import AllowAny # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from django.urls import reverse # type: ignore
from .models import User
import json
import resend

from supabase import create_client
from django.conf import settings



class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = RefreshToken.for_user(user).access_token
            verification_link = request.build_absolute_uri(
                reverse('email-verify') + f'?token={str(token)}'+f'?email={str(user.email)}'
            )
            print(verification_link)
            # send_mail(
            #     'Verify your email',
            #     f'Click the link to verify your account: {verification_link}',
            #     'onboarding@resend.dev',
            #     [user.email],
            #     fail_silently=False,
            # )
            return Response({'email':user.email, 'message': 'User created. Verify your email.', 'url':verification_link}, status=status.HTTP_201_CREATED) #,
            # return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
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
        email = request.GET.get('email')  # Get the email from the URL

        # Initialize Supabase client
        supabase_url = settings.SUPABASE_URL  # Set this in your Django settings
        supabase_key = settings.SUPABASE_KEY  # Set this in your Django settings
        supabase = create_client(supabase_url, supabase_key)

        # Verify the email using the Supabase client
        # response = supabase.auth.verify_email(token, email)
        response = supabase.auth.sign_in_with_email(email)
        print(response)
        if response.get('error'):
            return JsonResponse({'status': 'error', 'message': response['error']['message']})

        return JsonResponse({'status': 'success', 'message': 'Email verified successfully!'})

 