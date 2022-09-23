from django.db import models

# Create your models here.


class Users(models.Model):
    user_name = models.CharField(max_length=25, blank=False, null=True)
    first_name = models.CharField(max_length=25, blank=False, null=True)
    last_name = models.CharField(max_length=25, blank=False, null=True)
    email = models.EmailField(
        max_length=25, blank=False, default="test@test.test")
    password = models.CharField(max_length=25, blank=False, default="testtest")
    password_updated_at = models.DateField(null=True)
    profile_image = models.URLField(null=True)
    bio = models.TextField(blank=True)
    has_garden = models.BooleanField
