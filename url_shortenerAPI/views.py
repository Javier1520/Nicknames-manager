from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from .redis_urls import *

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def shorten_url_view(request):
    original_url = request.data.get('original_url')
    user_id = request.user.id
    short_url = shorten_url(original_url, user_id)
    return Response( {'shortened_url': short_url})

from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})
