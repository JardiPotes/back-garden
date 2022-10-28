from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

"""TODO Write a url pattern for basic CRUD instead of hard coding them
    """


urlpatterns = [
    path('', views.list_users, name="users"),
    path('profile/<str:pk>/', views.get_user_detail, name="profile"),
    path('register', views.create_user, name="register"),
    path('login', views.user_login, name="login"),
    path('logout', views.user_logout, name="logout"),
    path('update_user/<str:pk>/', views.update_user, name="update"),
    path('delete/<str:pk>/', views.delete_user, name="delete"),
    path('auth/', obtain_auth_token),

]
