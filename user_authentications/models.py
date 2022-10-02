from django.db import models
from django.utils.timezone import now
from datetime import datetime


class User(models.Model):

    username = models.CharField(
        max_length=25, blank=False, unique=True, null=False, default="test_user")
    first_name = models.CharField(max_length=25, blank=False, null=True)
    last_name = models.CharField(max_length=25, blank=False, null=True)
    email = models.EmailField(
        max_length=25, blank=False, unique=True, default="test@test.test")
    password = models.CharField(max_length=25, blank=False, default="testtest")
    password_updated_at = models.DateTimeField(default=now, null=True)
    profile_image = models.URLField(null=True)
    bio = models.TextField(blank=True, null=True)
    has_garden = models.BooleanField(default=False)


def __str__(self):
    return self.username
