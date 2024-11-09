import uuid
from django.db import models # type: ignore
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # type: ignore
from django.core.validators import RegexValidator # type: ignore
from datetime import date


def save_dir(instance, filename):
    return f'./static/images/user/{instance.id}-{filename}'


class Address(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    state_code = models.CharField(max_length=5)
    postal_code = models.CharField(max_length=20)
    coordinates = models.JSONField()  # to store latitude and longitude as a dictionary
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.country}"


class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password = None, phone_number = None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name: # type: ignore
            raise ValueError("Users must have a first_name")

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email=self.normalize_email(email),
            phone_number= phone_number,
            **extra_fields # type: ignore
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_pro', True)

        user = self.create_user(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            password=password,
            **extra_fields
            )
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Primary key
    USER_ROLES = (
        ('vendor', 'vendor'),
        ('customer', 'customer'),
        ('seller', 'seller'),
    )

    USER_GENDER = (
        ('Female', 'female'),
        ('Male', 'male'),
        ('Other', 'other')
    )

    first_name = models.CharField(max_length=150, default='Unknown')
    last_name = models.CharField(max_length=150, default='Unknown')
    age = models.IntegerField(null=True, blank=True, editable=False)
    gender = models.CharField(max_length=50, choices=USER_GENDER, default='customer')
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        unique=True,
        null=True,
        blank=True
    )
    birthDate = models.DateField(null=True, blank=True)
    image = models.ImageField(upload_to=save_dir, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    user_type = models.CharField(max_length=50, choices=USER_ROLES, default='customer')  # Default role
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

    is_staff = models.BooleanField(default=False)  # if staff
    is_pro = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use username as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Email is required, but not the username

    def __str__(self):
        # Get all fields except 'password'
        # user_data = {k: v for k, v in self.__dict__.items() if k != 'password' and not k.startswith('_')}
        # return str(user_data)
        return self.email # type: ignore

    def calculate_age(self):
        today = date.today()
        age = today.year - self.birthDate.year
        if today.month < self.birthDate.month or (today.month == self.birthDate.month and today.day < self.birthDate.day):
            age -= 1
        return age

    def save(self, *args, **kwargs):
        # Update the age field based on birthDate before saving
        if self.birthDate:
            self.age = self.calculate_age()
        super().save(*args, **kwargs)


