# urls.py

from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from .views import tenant_home  # Make sure this import exists
router = DefaultRouter()
router.register(r'companies', views.CompanyInfoViewSet, basename='company')
router.register(r'terms', views.TermsViewSet, basename='terms')
 # Define the route for the tenant home page
urlpatterns = [
    path('', tenant_home, name='tenant_home'), 
    path('api/', include(router.urls)),
    
]
