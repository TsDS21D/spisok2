from django.contrib import admin
from .models import NameEntry

@admin.register(NameEntry)
class NameEntryAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    ordering = ['order_number']