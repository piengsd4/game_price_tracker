from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

@api_view(["GET"])
def get_csrf(request):
    csrf_token = get_token(request)
    return Response({ "csrfToken": csrf_token })

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