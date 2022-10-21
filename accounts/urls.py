from django.urls import path
from . import views

urlpatterns = [
    path('', views.listUsers, name="users"),
    path('profile/<str:pk>/', views.getUserDetail, name="profile"),
    path('register', views.createUser, name="register"),
    path('update_user/<str:pk>/', views.updateUser, name="update"),
    path('delete/<str:pk>/', views.deleteUser, name="delete")
]
