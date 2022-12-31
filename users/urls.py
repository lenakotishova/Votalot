from django.urls import path, include
from . import views
from django.views import View

from .views import Register

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
]