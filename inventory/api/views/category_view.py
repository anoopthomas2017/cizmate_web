# inventory/views/category_view.py
from django.forms import ValidationError

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core.cache import cache
from django.utils.translation import gettext_lazy as _

from inventory.models import Category
from .category_serializers import CategorySerializer, CategoryDetailSerializer, CategoryTreeSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [ filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'parent']
    search_fields = [ 'name', 'description']
    ordering_fields = [ 'name', 'created_at']
    ordering = ['name']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['retrieve', 'update', 'partial_update']:
            return queryset.select_related('parent').prefetch_related('children')
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        if self.action == 'tree':
            return CategoryTreeSerializer
        return CategorySerializer

    def _clear_category_cache(self, instance=None):
        """Clear category-related cache"""
        cache.delete('category_tree')
        if instance:
            cache.delete(f'category_hierarchy_{instance.id}')

    def perform_create(self, serializer):
        instance = serializer.save()
        self._clear_category_cache()

    def perform_update(self, serializer):
        instance = serializer.save()
        self._clear_category_cache(instance)

    def perform_destroy(self, instance):
        """
        Delete category if it has no children
        TODO: Add these checks when implementing Product model:
        - Check for related products/inventory items
        - Add validation for products using this category
        - Consider soft delete option
        """
        if instance.children.exists():
            raise ValidationError(_("Cannot delete category with subcategories"))
        # TODO: Uncomment when Product model is implemented
        # if instance.inventory_items.exists():
        #     raise ValidationError(_("Cannot delete category with items"))
        self._clear_category_cache(instance)
        instance.delete()

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        Return category tree structure
        TODO: Add product counts in tree response
        TODO: Add stock value calculations
        TODO: Add category level statistics
        """
        cache_key = 'category_tree'
        tree = cache.get(cache_key)
        if tree is None:
            categories = Category.objects.filter(parent=None)
            serializer = CategoryTreeSerializer(categories, many=True)
            tree = serializer.data
            cache.set(cache_key, tree, timeout=3600)
        return Response(tree)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Return only active categories"""
        categories = Category.objects.active()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)