from django.contrib import admin
from django.urls import re_path, include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from apis.views import GardenViewset, PhotoViewset
from accounts.views import AuthViewSet, UserViewSet


# Ici nous créons notre routeur
router = routers.SimpleRouter(trailing_slash=False)
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register(r'api/gardens', GardenViewset, basename='gardens')
router.register(r'api/photos', PhotoViewset, basename='photos')
router.register(r'api/auth', AuthViewSet, basename='auth')
router.register(r'api/users', UserViewSet, basename='users')

"""
POST ${API_URL}/ - request a reset password token by using the email parameter
POST ${API_URL}/confirm/ - using a valid token, the users password is set to the provided password
POST ${API_URL}/validate_token/ - will return a 200 if a given token is valid
"""

urlpatterns = [
    path('', include(router.urls)),
    re_path('admin/', admin.site.urls),
    #  re_path('api/', include('apis.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     router.urls,
#     re_path('admin/', admin.site.urls),
# ]
