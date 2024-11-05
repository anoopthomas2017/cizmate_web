# apps/inventory/models/category.py
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def with_item_count(self):
        return self.annotate(item_count=models.Count('inventory_items'))

    def with_related(self):
        return self.select_related('parent').prefetch_related('children')

class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        unique=True,
        verbose_name=_("Category Name")
    )
    slug = models.SlugField(
        max_length=120, 
        unique=True, 
        editable=False
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name=_("Description")
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active Status")
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='children',
        verbose_name=_("Parent Category")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ['name']
        indexes = [
           
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
        ]
        unique_together = [['parent', 'name']]  # Prevent duplicate names under same parent

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent and self.parent == self:
            raise ValidationError(_("A category cannot be its own parent."))
        if self.parent and not self.parent.is_active:
            raise ValidationError(_("Parent category must be active."))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.full_clean()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('inventory:category-detail', kwargs={'pk': self.pk})

    @property
    def active_items_count(self):
        return self.inventory_items.filter(is_active=True).count()

    def get_hierarchy(self):
        """Returns list of parent categories in order."""
        hierarchy = []
        current = self
        while current is not None:
            hierarchy.append(current)
            current = current.parent
        return reversed(hierarchy)