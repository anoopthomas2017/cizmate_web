# urls.py

from django.urls import path
from .views import tenant_home  # Make sure this import exists

urlpatterns = [
    path('', tenant_home, name='tenant_home'),  # Define the route for the tenant home page
]
