from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Garden, Photo
from .serializers import GardenSerializer, PhotoSerializer


""" Garden methods """

""" GardenViewset includes GET/POST/PUT/DELETE methods with or without params """


class GardenViewset(ModelViewSet):

    serializer_class = GardenSerializer
    # change to isAuthenticated when needed
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Garden.objects.all()

        user_id = self.request.query_params.get('user_id')
        zipcode = self.request.query_params.get('zipcode')
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        if zipcode is not None:
            queryset = queryset.filter(zipcode=zipcode)
        return queryset


class PhotoViewset(ModelViewSet):
    serializer_class = PhotoSerializer
# change to IsAuthenticated
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Photo.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
