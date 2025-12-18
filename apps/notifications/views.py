from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Notification


@login_required
@require_http_methods(["GET"])
def get_notifications(request):
    """Get unread notifications"""
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:10]
    
    data = [{
        'id': n.id,
        'title': n.title,
        'message': n.message,
        'type': n.notification_type,
        'created_at': n.created_at.isoformat(),
    } for n in notifications]
    
    return JsonResponse({'notifications': data})


@login_required
@require_http_methods(["POST"])
def mark_read(request, notification_id):
    """Mark notification as read"""
    notification = Notification.objects.get(
        id=notification_id,
        user=request.user
    )
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})

