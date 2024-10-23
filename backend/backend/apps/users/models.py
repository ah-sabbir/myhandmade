import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone = None, password = None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            first_name = self.first_name,
            last_name = self.last_name,
            email=self.normalize_email(email),
            phone = self.phone
            **extra_fields
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(first_name, last_name, email, password)
        user.role = 'admin'  # Set the role to admin
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Primary key
    USER_ROLES = (
        ('vendor', 'Vendor'),
        ('customer', 'customer'),
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$')],
        unique=True,
        null=True,
        blank=True
    )
    phone_verified = models.BooleanField(default=False)
    # password_hash = models.CharField(max_length=128)
    role = models.CharField(max_length=6, choices=USER_ROLES, default='customer')  # Default role
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    objects = CustomUserManager()

    USER_ID_FIELD = 'user_id'  # Use username as the unique identifier
    REQUIRED_FIELDS = ['email']  # Email is required, but not the username

    def __str__(self):
        return self.user_id
