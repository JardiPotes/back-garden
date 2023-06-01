from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
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
        fields = ("id", "conversation_id", "content", "sender_id", "sent_at")
        read_only_fields = ("id", "sender_id", "sent_at")

    def create(self, validated_data):
        validated_data["sent_at"] = timezone.now()
        writable_fields = ["sender_id", "conversation_id", "content"]
        writable_validated_data = {
            key: validated_data[key] for key in validated_data if key in writable_fields
        }
        instance = super(MessageSerializer, self).create(
            writable_validated_data)
        return instance


class ListConversationSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()
    chat_sender_id = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = (
            "id",
            "chat_sender_id",
            "chat_receiver_id",
            "latest_message",
            "updated_at",
        )

    def get_chat_sender_id(self, obj):
        return obj.chat_sender_id.id

    def get_latest_message(self, obj):
        try:
            latest_message = Message.objects.filter(conversation_id=obj.id).latest(
                "sent_at"
            )
            serializer = MessageSerializer(latest_message)
            return serializer.data
        except ObjectDoesNotExist:
            return {}


class ConversationShowSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ("id", "chat_sender_id", "chat_receiver_id", "messages")

    def get_messages(self, obj):
        messages = Message.objects.filter(conversation_id=obj.id)
        if messages.exists():
            serializer = MessageSerializer(messages, many=True)
            return serializer.data
        else:
            return []


class ConversationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ("id", "chat_sender_id", "chat_receiver_id", "updated_at")
