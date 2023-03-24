from django.db import models
from django.utils.timezone import now

from accounts.models import User

user = User


class Garden(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gardens")
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
    garden_id = models.ForeignKey(Garden, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name=str, default="")
    image = models.ImageField(default="", upload_to="apis/images")
    isMainPhoto = models.BooleanField()
    season = models.IntegerField()


class Comment(models.Model):
    author_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_id"
    )
    receiver_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver_id"
    )
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)
