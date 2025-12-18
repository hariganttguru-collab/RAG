from django.db import models
from django.contrib.auth.models import User


class Stakeholder(models.Model):
    """AI-powered stakeholder profiles"""
    STAKEHOLDER_TYPES = [
        ('senior_manager', 'Senior Manager'),
        ('team_lead', 'Team Lead'),
        ('developer', 'Developer'),
        ('designer', 'Designer'),
        ('qa', 'QA Engineer'),
        ('client', 'Client'),
    ]
    
    name = models.CharField(max_length=100)
    stakeholder_type = models.CharField(max_length=20, choices=STAKEHOLDER_TYPES)
    avatar = models.CharField(max_length=200, blank=True, help_text="Avatar emoji or icon")
    description = models.TextField(blank=True)
    is_online = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Message(models.Model):
    """Chat messages between user and stakeholders"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    is_from_stakeholder = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.stakeholder.name} - {self.content[:50]}"


class ChatRoom(models.Model):
    """Represents a chat room between user and stakeholder"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_rooms')
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.CASCADE, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'stakeholder']
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.stakeholder.name}"

