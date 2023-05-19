from django.db import models
from django.utils import timezone

from accounts.models import User

user = User


class Garden(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="gardens")
    description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=100)
    address = models.TextField()  # todo address
    # todo specific Geo models ? https://pypi.org/project/django-address/
    zipcode = models.CharField(max_length=5)  # TODO: check best practices
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.title


class Photo(models.Model):
    garden_id = models.ForeignKey(Garden, on_delete=models.CASCADE)
    image = models.ImageField(default="", upload_to="apis/images")
    is_main_photo = models.BooleanField()
    season = models.IntegerField(default=0)


class Comment(models.Model):
    author_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_id"
    )
    receiver_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="receiver_id"
    )
    content = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(default=timezone.now())
    updated_at = models.DateTimeField(default=timezone.now())


class Conversation(models.Model):
    chat_sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_sender_id"
    )
    chat_receiver_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="chat_receiver_id"
    )
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    conversation_id = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="conversation_id"
    )
    sender_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender_id"
    )
    content = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now())

    def save(self, *args, **kwargs):
        update_conversation = False
        if self.pk is None:
            update_conversation = True
        else:
            old_message = Message.objects.get(pk=self.pk)
            if old_message.sent_at != self.sent_at:
                update_conversation = True

        super().save(*args, **kwargs)

        if update_conversation:
            conversation = self.conversation_id
            conversation.updated_at = timezone.now()
            conversation.save()
