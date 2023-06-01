from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

from accounts.views import AuthViewSet, UserViewSet
from apis.views import (CommentViewset, ConversationViewset, GardenViewset,
                        MessageViewset, PhotoViewset)

schema_view = get_schema_view(
    openapi.Info(
        title="JardiPotes API", default_version="v1", description="JardiPotes API Docs"
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Ici nous créons notre routeur
router = routers.SimpleRouter(trailing_slash=False)
# Puis lui déclarons une url basée sur le mot clé ‘category’ et notre view
# afin que l’url générée soit celle que nous souhaitons ‘/api/category/’
router.register(r"api/messages", MessageViewset, basename="messages")
router.register(r"api/conversations", ConversationViewset, basename="conversations")
router.register(r"api/comments", CommentViewset, basename="comments")
router.register(r"api/gardens", GardenViewset, basename="gardens")
router.register(r"api/photos", PhotoViewset, basename="photos")
router.register(r"api/auth", AuthViewSet, basename="auth")
router.register(r"api/users", UserViewSet, basename="users")

"""
POST ${API_URL}/ - request a reset password token by using the email parameter
POST ${API_URL}/confirm/ - using a valid token, the users password is set to the provided password
POST ${API_URL}/validate_token/ - will return a 200 if a given token is valid
"""

urlpatterns = [
    path("", include(router.urls)),
    re_path("admin/", admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
