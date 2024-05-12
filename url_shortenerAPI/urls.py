from django.urls import path
from . import views

urlpatterns = [
    path('', views.shorten_url_view, name='short_url'),
    path('<str:short_url>', views.get_original_url_view, name='redirect_url'),
]
