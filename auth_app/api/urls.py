from django.urls import path
from rest_framework import routers

from auth_app.api.views import LoginView, RegistrationView, single_profile_view


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', single_profile_view, name='profile-detail')
]