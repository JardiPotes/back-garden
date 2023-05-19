from django.db import transaction
from rest_framework import serializers

from accounts.models import User

from .models import Comment, Conversation, Garden, Message, Photo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "experience", "profile_image", "nickname")


class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        fields = ("id", "user_id", "title", "description", "zipcode")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ("id", "garden_id", "image", "is_main_photo", "season")


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(required=False, source="author_id")

    class Meta:
        model = Comment
        fields = (
            "id",
            "author_id",
            "author",
            "receiver_id",
            "content",
            "created_at",
            "updated_at",
        )


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "conversation_id", "sender_id", "content", "sent_at")


class ListConversationSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "id",
            "chat_sender_id",
            "chat_receiver_id",
            "latest_message",
            "updated_at",
        )

    def get_latest_message(self, obj):
        latest_message = Message.objects.filter(conversation_id=obj.id).latest(
            "sent_at"
        )
        serializer = MessageSerializer(latest_message)
        return serializer.data


class ConversationShowSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, source="conversation_id")

    class Meta:
        model = Conversation
        fields = ("id", "chat_sender_id", "chat_receiver_id", "messages")
