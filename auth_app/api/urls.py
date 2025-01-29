from django.urls import path

from auth_app.api.views import LoginView, RegistrationView, loginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='register'),
]