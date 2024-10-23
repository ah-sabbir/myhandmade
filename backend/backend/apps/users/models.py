import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.role = 'admin'  # Set the role to admin
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    USER_ROLES = (
        ('vendor', 'Vendor'),
        ('customer', 'customer'),
        ('admin', 'Admin'),
    )

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Primary key
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    # password_hash = models.CharField(max_length=128)
    role = models.CharField(max_length=6, choices=USER_ROLES, default='buyer')  # Default role
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation

    objects = UserManager()

    USERNAME_FIELD = 'username'  # Use username as the unique identifier
    REQUIRED_FIELDS = ['email']  # Email is required, but not the username

    def __str__(self):
        return self.username
