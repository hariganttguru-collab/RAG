from django.contrib import admin
from .models import Project, Document


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'uploaded_by', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title']

