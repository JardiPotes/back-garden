from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

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

        user_id = self.request.query_params.get("user_id")
        zipcode = self.request.query_params.get("zipcode")
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        if zipcode is not None:
            queryset = queryset.filter(zipcode=zipcode)
        return queryset


# TODO check the pagination here
#   data = self.request.data
# mostRecent = self.request.GET.get('recent')
# if 'user_id' in data:
#     queryset = queryset.filter(user_id=data["user_id"])
# if 'zipcode' in data:
#     queryset = queryset.filter(zipcode=data["zipcode"])
# if mostRecent is not None:
#     queryset = queryset.order_by('created_at')[:10][::-1]
# return queryset


class PhotoViewset(ModelViewSet):
    serializer_class = PhotoSerializer
    # change to IsAuthenticated
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
    queryset = Photo.objects.all()

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
