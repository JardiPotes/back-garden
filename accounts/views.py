import json

from django.contrib.auth import login
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Garden, User
from .serializers import GardenSerializer, UserSerializer

"""Create a user

    Raises:
        ValidationError: 400 Bad request when an email already exists

    Returns:
        201: Created with a token
    """


@api_view(["POST"])
@permission_classes([AllowAny])
def create_user(request):

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        account = serializer.save()
        account.is_active = True
        account.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """TO DISCUSS

   Should return a list of all users. Check if we want to detail this function or not. I.E. should user need to be logged in to see all users?
    """


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_detail(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)


"""
 TODO create a method only for updating password
"""


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


""" password reset method """


@api_view(["POST"])
@permission_classes([AllowAny])
@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    # reset password confirmation url looks like this: host/api/users/password_reset/?token=TOKEN
    context = {
        "current_user": reset_password_token.user,
        "first_name": reset_password_token.user.first_name,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse("password_reset:reset-password-confirm")
            ),
            reset_password_token.key,
        ),
    }

    # render email text
    email_html_message = render_to_string("user_reset_password.html", context)
    email_plaintext_message = render_to_string("user_reset_password.txt", context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(
            title="R??initialiser le code secret pour JardiPotes"
        ),
        # message:
        email_plaintext_message,
        # from:
        "sadefryt@gmail.com",
        # to:
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_user(request, pk):
    user = User.objects.get(id=pk)
    user.delete()

    return Response("Deleted")


"""
 User login with a token. For now, there's no expiration set.
"""


@api_view(["POST"])
@permission_classes([AllowAny])
def user_login(request):
    data = {}
    reqBody = json.loads(request.body)
    email = reqBody["email"]
    password = reqBody["password"]
    try:
        account = User.objects.get(email=email)
    except BaseException as err:
        raise ValidationError({"400": f"{str(err)}"})

    token = Token.objects.get_or_create(user=account)[0].key
    if not check_password(password, account.password):
        raise ValidationError({"message": "Incorrect Login credentials"})

    if account:
        if account.is_active:
            login(request, account)
            data["message"] = "user logged in"
            data["email"] = account.email

            res = {"data": data, "token": token}

            return Response(res)

        else:
            raise ValidationError({"400": "Account not active"})

    else:
        raise ValidationError({"400": "Account doesnt exist"})


"""
When calling this method, we need to provide this info in the header:
key                          Value
Authorization                Token xxxxxxxxxxxx


"""


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_logout(request):

    request.user.auth_token.delete()

    return Response("User Logged out successfully")


""" Garden methods """

""" Get 10 last gardens """


@api_view(["GET"])
@permission_classes([AllowAny])
def list_gardens(request):
    gardens = Garden.objects.all().order_by("created_at")[:10][::-1]
    serializer = GardenSerializer(gardens, many=True)

    return Response(serializer.data)


""" Get one garden """


@api_view(["GET"])
@permission_classes([AllowAny])
def get_garden_detail(request, pk):
    garden = Garden.objects.get(id=pk)
    serializer = GardenSerializer(garden, many=False)
    return Response(serializer.data)


""" Create one garden """


@api_view(["POST"])
@permission_classes([AllowAny])
def create_garden(request):

    serializer = GardenSerializer(data=request.data)
    if serializer.is_valid():
        garden = serializer.save()
        garden.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


""" Delete one garden """


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_garden(request, pk):
    garden = Garden.objects.get(id=pk)
    garden.delete()

    return Response("Deleted")


""" Update one garden """


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_garden(request, pk):
    garden = Garden.objects.get(id=pk)
    serializer = GardenSerializer(instance=garden, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
