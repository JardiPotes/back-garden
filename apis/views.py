from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from .models import Comment, Garden, Photo
from .permissions import IsCommentOwnerPermission, IsGardenOwnerPermission
from .serializers import CommentSerializer, GardenSerializer, PhotoSerializer

""" Garden methods """

""" GardenViewset includes GET/POST/PUT/DELETE methods with or without params """


class GardenViewset(ModelViewSet):

    serializer_class = GardenSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsGardenOwnerPermission]

    queryset = Garden.objects.all()

    def get_permissions(self):
        if self.action == "update" or self.action == "partial_update":
            permission_classes = [IsGardenOwnerPermission]
        else:
            permission_classes = [IsAuthenticatedOrReadOnly]
        res = [permission() for permission in permission_classes]
        return res

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
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Photo.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentOwnerPermission]
    queryset = Comment.objects.all()
