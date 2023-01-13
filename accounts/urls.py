from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

"""TODO Write a url pattern for basic CRUD instead of hard coding them
    """


urlpatterns = [
    # users
    path("users", views.list_users, name="users"),
    path("profile/<str:pk>/", views.get_user_detail, name="profile"),
    path("register", views.create_user, name="register"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("update_user/<str:pk>/", views.update_user, name="update"),
    path("delete_user/<str:pk>/", views.delete_user, name="delete"),
    path("auth/", obtain_auth_token),
    path(
        "password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    # gardens
    # path('gardens/', include(router.urls)),
    # path('garden/<str:pk>/', views.get_garden_detail),
    # path('create_garden/', views.create_garden, name="create_garden"),
    # path('update_garden/<str:pk>/', views.update_garden, name="update_garden"),
    # path('delete_garden/<str:pk>/', views.delete_garden, name="delete_garden")
]
