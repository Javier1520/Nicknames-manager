from django.urls import path
from . import views

urlpatterns = [
    path('', views.shorten_url_view, name='short_url'),
    path('csrf', views.get_csrf_token),
]
