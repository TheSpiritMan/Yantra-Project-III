from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
import uuid
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, otp_num='', otp_end='', **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        user = self.model(username=username, email=email, otp_num=otp_num, otp_end=otp_end, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, otp_num='', otp_end='', **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, otp_num, otp_end, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=15, null=False)
    last_name = models.CharField(max_length=25, null=False)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    otp_num = models.CharField(max_length=255, default='')
    otp_end = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    class Meta:
        db_table = 'custom_user'

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def is_otp_valid(self):
        if self.otp_end > timezone.now():
            return True
        return False