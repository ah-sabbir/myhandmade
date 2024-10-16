from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .models import User

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully", "user": serializer.data}, status=status.HTTP_201_CREATED)
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
            except User.DoesNotExist:
                return Response({"error":"invalid user"}, status= status.HTTP_401_UNAUTHORIZED)
            
            # checking if user authenticated or not
            user = authenticate(username=user.username, password=password)
            
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({"token": token.key}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUser(APIView):
    def get(self, request):
        users = User.objects.all()  # Get all users
        serializer = UserSerializer(users, many=True)  # Serialize the queryset
        return Response(serializer.data, status=status.HTTP_200_OK)  # Return serialized data
    # queryset = User.objects.all()

    # def get(self, request):
    #     return Response({"user":User.objects.all()})
    # serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated, IsVendor]

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


# from django.shortcuts import render, redirect
# from .forms import UserRegistrationForm
# from .models import User

# from django.contrib.auth import authenticate, login as auth_login
# from django.contrib import messages

# def register(request):
#     if request.method == 'POST':
#         user_form = UserRegistrationForm(request.POST)

#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             user.set_password(user_form.cleaned_data['password'])  # Hash the password
#             user.save()  # Save the user to the database

#             auth_login(request, user)  # Automatically log in the user
#             return redirect('home')  # Redirect to home or another page

#     else:
#         user_form = UserRegistrationForm()

#     return render(request, 'users/register.html', {'user_form': user_form})



# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             auth_login(request, user)
#             return redirect('home')  # Redirect to home or another page
#         else:
#             messages.error(request, 'Invalid username or password')

#     return render(request, 'users/login.html')

