from django.db import models
from django.utils.timezone import now
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import datetime

"""The User Model is an extension of the default one from Django. Username is set as email
    """


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email can not be null.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    pass
    username = None
    email = models.EmailField(verbose_name='email address', unique=True)
    profile_image = models.URLField(null=True)
    bio = models.TextField(blank=True, null=True)
    has_garden = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


def __str__(self):
    return self.email
