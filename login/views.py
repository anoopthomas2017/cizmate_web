from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import status
from .forms import CreateUserForm
import json

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return JsonResponse({
                'success': True,
                'access': response.data['access'],
                'refresh': response.data['refresh']
            })
        return response

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data['email']
        password = data['password']
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)
    
    user = authenticate(request, username=email, password=password)
    
    if user:
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'success': True,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'email': user.email,
                'username': user.username
            }
        })
    return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    return JsonResponse({
        'username': request.user.username,
        'email': request.user.email
    })

@csrf_exempt
@api_view(['POST'])
def register_view(request):
    data = json.loads(request.body.decode('utf-8'))
    form = CreateUserForm(data)
    if form.is_valid():
        user = form.save()
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'success': True,
            'message': 'User registered successfully',
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }, status=201)
    else:
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'error': errors}, status=400)