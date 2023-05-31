from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404


from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.viewsets import ModelViewSet

from .models import Comment, Conversation, Garden, Message, Photo, User
from .permissions import (IsCommentOwnerPermission,
                          IsConversationMembersPermission,
                          IsConversationParticipant, IsGardenOwnerPermission,
                          IsGardenPhotoOwnerPermission)
from .serializers import (CommentSerializer, ConversationPostSerializer,
                          ConversationShowSerializer, GardenSerializer,
                          ListConversationSerializer, MessageSerializer,
                          PhotoSerializer)

""" Garden methods """

""" GardenViewset includes GET/POST/PUT/DELETE methods with or without params """


class GardenViewset(ModelViewSet):

    serializer_class = GardenSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsGardenOwnerPermission]

    queryset = Garden.objects.all()

    def get_permissions(self):
        if self.action in ["update", "partial_update"]:
            permission_classes = [IsGardenOwnerPermission]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset
        user_id = self.request.query_params.get("user_id")
        zipcode = self.request.query_params.get("zipcode")
        if user_id is not None:
            queryset = self.queryset.filter(user_id=user_id)
        if zipcode is not None:
            queryset = self.queryset.filter(zipcode=zipcode)
        return queryset


class PhotoViewset(ModelViewSet):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsGardenPhotoOwnerPermission]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Photo.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "delete"]:
            permission_classes = [IsAuthenticated,
                                  IsGardenPhotoOwnerPermission]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = self.queryset
        garden_id = self.request.query_params.get("garden_id")
        if garden_id is not None:
            queryset = self.queryset.filter(garden_id=garden_id)
        return queryset

    def perform_create(self, serializer):
        garden_id = self.request.data.get("garden_id")
        garden = get_object_or_404(Garden, id=garden_id)
        if garden.user_id.id != self.request.user.id:
            raise PermissionDenied(
                "You don't have permission to add photos to this garden."
            )
        serializer.save(garden_id=garden)


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwnerPermission]
    queryset = Comment.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        receiver_id = self.request.query_params.get("receiver_id")
        if receiver_id is not None:
            queryset = self.queryset.filter(receiver_id=receiver_id)
        return queryset


class ConversationViewset(ModelViewSet):
    permission_classes = [IsAuthenticated, IsConversationMembersPermission]
    queryset = Conversation.objects.all()

    def get_queryset(self):
        queryset = self.queryset
        current_user_id = self.request.query_params.get(
            'current_user_id', None)
        if current_user_id:
            try:
                queryset = self.queryset.filter(
                    Q(chat_receiver_id=current_user_id) | Q(
                        chat_sender_id=current_user_id)
                ).order_by("-updated_at")
            except User.DoesNotExist:
                raise ValidationError(
                    "User with the specified ID does not exist.")

        return queryset

    def perform_create(self, serializer):
        chat_sender = self.request.user
        chat_receiver_id = self.request.data.get("chat_receiver_id")
        chat_receiver = get_user_model().objects.get(id=chat_receiver_id)
        serializer.save(chat_sender_id=chat_sender,
                        chat_receiver_id=chat_receiver)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConversationShowSerializer
        elif self.action == "create":
            return ConversationPostSerializer
        return ListConversationSerializer


class MessageViewset(ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        conversation_id = self.request.data.get("conversation_id")
        conversation = get_object_or_404(Conversation, id=conversation_id)
        if (
            self.request.user != conversation.chat_sender_id
            and self.request.user != conversation.chat_receiver_id
        ):
            raise PermissionDenied(
                "You don't have permission to send message to this person."
            )
        serializer.save(sender_id=self.request.user,
                        conversation_id=conversation)
