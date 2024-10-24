import uuid
from django.db import models # type: ignore
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin # type: ignore
from django.core.validators import RegexValidator # type: ignore

class CustomUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number = None, password = None):
        if not email:
            raise ValueError("Users must have an email address")
        if not first_name: # type: ignore
            raise ValueError("Users must have a first_name")

        user = self.model(
            first_name = self.first_name,
            last_name = self.last_name,
            email=self.normalize_email(email),
            phone_number = self.phone_number
            **extra_fields # type: ignore
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Primary key
    USER_ROLES = (
        ('vendor', 'Vendor'),
        ('customer', 'customer'),
    )

    first_name = models.CharField(max_length=150, default='Unknown')
    last_name = models.CharField(max_length=150, default='Unknown')
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
    role = models.CharField(max_length=50, choices=USER_ROLES, default='customer')  # Default role
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # Use username as the unique identifier
    REQUIRED_FIELDS = ['first_name', 'phone']  # Email is required, but not the username

    def __str__(self):
        # Get all fields except 'password'
        user_data = {k: v for k, v in self.__dict__.items() if k != 'password' and not k.startswith('_')}
        return str(user_data)
