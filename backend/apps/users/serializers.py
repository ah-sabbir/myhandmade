from rest_framework import serializers # type: ignore
from django.contrib.auth import get_user_model # type: ignore
from rest_framework.authtoken.models import Token # type: ignore
from django.contrib.auth.password_validation import validate_password # type: ignore
# from django.contrib.auth.models import User
# from django.contrib.auth.models import User

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'password2', 'phone_number', 'user_type')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data, **extra_fields):

        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email=validated_data['email'],
            **extra_fields,
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    is_staff = serializers.BooleanField(write_only=True, required=False)
    is_pro = serializers.BooleanField(write_only=True, required=False)
    class Meta:
        model = User
        fields = '__all__'  # Use all fields in the model
        extra_kwargs = {
            'password': {'write_only': True}  # Exclude 'password' from being exposed in the output
        }


class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = '__all__'

