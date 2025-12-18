from django.contrib import admin
from .models import Stakeholder, Message, ChatRoom


@admin.register(Stakeholder)
class StakeholderAdmin(admin.ModelAdmin):
    list_display = ['name', 'stakeholder_type', 'is_online', 'created_at']
    list_filter = ['stakeholder_type', 'is_online']
    search_fields = ['name']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'stakeholder', 'content', 'is_from_stakeholder', 'created_at']
    list_filter = ['is_from_stakeholder', 'created_at']
    search_fields = ['content']


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['user', 'stakeholder', 'created_at', 'updated_at']
    list_filter = ['created_at']

