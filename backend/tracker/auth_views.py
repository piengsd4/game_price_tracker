from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

@api_view(["GET"])
def get_csrf(request):
    csrf_token = get_token(request)
    return Response({ "csrfToken": csrf_token })

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_protect
def register_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    
    if not username or not password:
        return Response({"error": "Username and password are required"}, status=400)
    
    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
    except IntegrityError:
        return Response({"error": "Username already exists"}, status=400)
    
    login(request._request, user)
    return Response({ "ok": True, "username": user.username }, status=201)

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_protect
def login_view(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    user = authenticate(
        request._request, 
        username=username, 
        password=password,
    )
    
    if not user:
        return Response({ "error": "Authentication failed" }, status=status.HTTP_400_BAD_REQUEST)
    
    login(request._request, user)
    return Response({ "ok": True, "username": user.username })

@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@csrf_protect
def logout_view(request):
    logout(request)
    return Response({ "ok": True })

@api_view(["GET"])
@authentication_classes([])
@permission_classes([AllowAny])
def session_view(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            "authenticated": True,
            "username": user.username
        })

    return Response({
        "authenticated": False
    })