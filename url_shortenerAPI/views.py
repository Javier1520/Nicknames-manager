from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import redirect
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

@api_view(['GET'])
def get_original_url_view(request, short_url):
    original_url = get_original_url(short_url)
    if original_url:
        return redirect(original_url)
        # return Response({'original_url': original_url}, status=301)
    else:
        return Response({'error': 'Invalid short URL'}, status=404)