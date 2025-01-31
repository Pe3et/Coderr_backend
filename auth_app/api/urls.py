from django.urls import path

from auth_app.api.views import LoginView, RegistrationView, SingleProfileView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', SingleProfileView.as_view(), name='profile-detail')
]