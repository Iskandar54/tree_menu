from django.contrib import admin
from .models import MenuItem

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "menu_name", "parent", "order")
    list_filter = ("menu_name",)
    search_fields = ("name",)
    ordering = ("menu_name", "order")  