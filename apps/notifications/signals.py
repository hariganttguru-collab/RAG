from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Notification
from apps.chat.models import Stakeholder


@receiver(post_save, sender=User)
def send_welcome_notification(sender, instance, created, **kwargs):
    """Send welcome notification from Senior Manager when user is created"""
    if created:
        # Get or create Senior Manager stakeholder
        senior_manager = Stakeholder.objects.filter(
            stakeholder_type='senior_manager'
        ).first()
        
        if senior_manager:
            Notification.objects.create(
                user=instance,
                notification_type='message',
                title='Welcome! New Project Kickoff',
                message=f'Hi {instance.username}! I\'m {senior_manager.name}, your Senior Project Manager. I have an exciting new project for you! Click here to start the conversation.',
                stakeholder=senior_manager,
            )

