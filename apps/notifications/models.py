from django.db import models
from django.contrib.auth.models import User
from apps.chat.models import Stakeholder


class Notification(models.Model):
    """User notifications"""
    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('project', 'Project Update'),
        ('document', 'Document Shared'),
        ('system', 'System Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    stakeholder = models.ForeignKey(Stakeholder, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

