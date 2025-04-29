from django.db import models
from django.urls import reverse, NoReverseMatch
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

class MenuItem(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Item Name",
        help_text="Display name for the menu item"
    )
    named_url = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Named URL",
        help_text="Django URL name for reverse resolution"
    )
    url = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Direct URL",
        help_text="Absolute or relative URL path"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="Parent Item",
        help_text="Parent item in the menu hierarchy"
    )
    menu_name = models.CharField(
        max_length=100,
        verbose_name="Menu Name",
        help_text="Identifier for the menu system this item belongs to"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Sort Order",
        help_text="Position in the menu sequence"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"
        constraints = [
            models.UniqueConstraint(
                fields=['menu_name', 'name'],
                name='unique_menu_item_name'
            )
        ]

    def clean(self):
        if self.parent:
            current = self.parent
            while current:
                if current == self:
                    raise ValidationError("Circular reference detected in menu hierarchy!")
                current = current.parent

    def get_absolute_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch as e:
                logger.warning(f"Named URL '{self.named_url}' not found: {str(e)}")
        
        return self.url if self.url else '#'

    def __str__(self):
        return f"{self.name} ({self.menu_name})"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)