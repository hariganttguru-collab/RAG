from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.chat.models import Stakeholder
from apps.notifications.models import Notification
from apps.documents.models import Project


@login_required
def dashboard(request):
    """Virtual office dashboard"""
    stakeholders = Stakeholder.objects.filter(is_online=True)
    notifications = Notification.objects.filter(user=request.user, is_read=False)[:5]
    projects = Project.objects.filter(user=request.user)[:5]
    
    context = {
        'stakeholders': stakeholders,
        'notifications': notifications,
        'projects': projects,
    }
    return render(request, 'office/dashboard.html', context)

