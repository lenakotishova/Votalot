from django.urls import path, reverse, include, reverse_lazy
from . import views
from django.views import View
from django.contrib.auth import views as auth_views

from .views import Register

app_name = 'users'

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('login/', views.login_view, name='login'),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(), name='reset_password_done'),
    path('reset/<str:uidb64>/<str:token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
