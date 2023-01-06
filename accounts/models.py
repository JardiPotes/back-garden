from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.timezone import now

"""The User Model is an extension of the default one from Django. Username is set as email
    """


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email can not be null.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="email address", unique=True)
    nickname = models.CharField(max_length=100, null=True)
    profile_image = models.URLField(null=True)
    bio = models.TextField(blank=True, null=True)
    has_garden = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Garden(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100)
    address = models.TextField()  # todo address
    # todo specific Geo models ? https://pypi.org/project/django-address/
    zipcode = models.CharField(max_length=5)  # TODO: check best practices
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.title


class Photo(models.Model):
    SEASONS = (
        (0, "Printemps"),
        (1, "Été"),
        (2, "Automne"),
        (3, "Hiver"),
    )
    gardenId = models.ForeignKey(Garden, on_delete=models.CASCADE)
    photoUrl = models.URLField(max_length=300)
    isMainPhoto = models.BooleanField(default=False)
    season = models.PositiveSmallIntegerField(max_value=3, choices=SEASONS, null=True)
