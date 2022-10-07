from django.db import models
from django.shortcuts import render, redirect
from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def listUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getUserDetail(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def createUser(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors)


@api_view(['PATCH'])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(['DELETE'])
def deleteUser(request, pk):
    user = User.objects.get(id=pk)
    user.delete()

    return Response('Deleted')
