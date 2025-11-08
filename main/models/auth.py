from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager


class CustomUserManager(UserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Foydalanuvchi nomi kiritilishi shart!")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'O‘quvchi'),
        ('teacher', 'O‘qituvchi'),
        ('admin', 'Admin'),
    ]

    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

