from rest_framework import serializers
from django.core.cache import cache
from inventory.models import Category
from django.utils.translation import gettext as _  # I notice you're using _() but hadn't imported it

class CategorySerializer(serializers.ModelSerializer):
    parent_name = serializers.CharField(source='parent.name', read_only=True, allow_null=True)
    hierarchy = serializers.SerializerMethodField(read_only=True)
    url = serializers.URLField(source='get_absolute_url', read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('exclude_hierarchy', False):
            self.fields.pop('hierarchy', None)

    class Meta:
        model = Category
        fields = [
            'id',
            'name', 
            'slug',
            'description', 
            'is_active', 
            'parent',
            'parent_name',
            'hierarchy',
            'url',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
        extra_kwargs = {
            'name': {'required': True, 'trim_whitespace': True},
            'description': {'required': False, 'allow_blank': True},
            'parent': {'required': False, 'allow_null': True}
        }

    def get_hierarchy(self, obj):
        """
        Convert hierarchy to a JSON-serializable format
        """
        if not hasattr(obj, 'get_hierarchy'):
            return None
            
        hierarchy = obj.get_hierarchy()
        # Convert hierarchy to a list of dictionaries
        if isinstance(hierarchy, (list, tuple)):
            return [
                {
                    'id': item.id,
                    'name': item.name,
                    'slug': item.slug
                } if hasattr(item, 'id') else str(item)
                for item in hierarchy
            ]
        return str(hierarchy)  # Fallback to string representation

    # ... rest of your validation methods remain the same ...

class CategoryDetailSerializer(CategorySerializer):
    children = serializers.SerializerMethodField()
    total_items_count = serializers.IntegerField(
        source='inventory_items.count',
        read_only=True
    )
    active_items_count = serializers.IntegerField(read_only=True)
    
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + [
            'children',
            'total_items_count',
            'active_items_count'
        ]

    def get_children(self, obj):
        depth = self.context.get('children_depth', 1)
        if depth <= 0:
            return []
            
        children = obj.children.filter(is_active=True)
        new_context = {**self.context, 'children_depth': depth - 1}
        
        return CategorySerializer(
            children,
            many=True,
            context=new_context
        ).data

class CategoryTreeSerializer(CategorySerializer):
    children = serializers.SerializerMethodField()
    
    class Meta(CategorySerializer.Meta):
        fields = [
            'id',
            'name',
            'slug',
            'is_active',
            'children',
            'active_items_count'
        ]

    def get_children(self, obj):
        children = obj.children.all()
        return CategoryTreeSerializer(children, many=True).data