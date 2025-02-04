from django.urls import path

from auth_app.api.views import BusinessListView, CustomerListView, LoginView, RegistrationView, SingleProfileView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='register'),
    path('profile/<int:pk>/', SingleProfileView.as_view(), name='profile-detail'),
    path('profiles/business/', BusinessListView.as_view(), name='business-list'),
    path('profiles/customer/', CustomerListView.as_view(), name='customer-list')
]