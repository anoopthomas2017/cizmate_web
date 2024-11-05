from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api.views.category_view import CategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
app_name = 'inventory'
urlpatterns = [
    path('api/', include(router.urls)),
    
    # Optional: Direct category URLs
   
]