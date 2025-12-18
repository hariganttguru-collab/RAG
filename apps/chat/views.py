from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Stakeholder, Message, ChatRoom
from apps.notifications.models import Notification


@login_required
def chat_list(request):
    """List of stakeholders to chat with"""
    stakeholders = Stakeholder.objects.filter(is_online=True)
    return render(request, 'chat/chat_list.html', {'stakeholders': stakeholders})


@login_required
def chat_room(request, stakeholder_id):
    """Chat room with a specific stakeholder"""
    stakeholder = get_object_or_404(Stakeholder, id=stakeholder_id)
    chat_room, created = ChatRoom.objects.get_or_create(
        user=request.user,
        stakeholder=stakeholder
    )
    messages = Message.objects.filter(
        user=request.user,
        stakeholder=stakeholder
    ).order_by('created_at')
    
    # Send initial welcome message from Senior Manager if this is first time
    if stakeholder.stakeholder_type == 'senior_manager' and messages.count() == 0:
        welcome_message = (
            f"Hi {request.user.username}! 👋\n\n"
            "I'm Sarah Chen, your Senior Project Manager. I'm excited to kick off a new project with you!\n\n"
            "We have a new client project that needs your attention. I've prepared a project brief document "
            "that outlines the key requirements and objectives.\n\n"
            "Your task is to:\n"
            "1. Review the project requirements\n"
            "2. Collaborate with the team to create a project estimation\n"
            "3. Develop a budget proposal\n\n"
            "Feel free to chat with me or any of the other stakeholders to gather information. "
            "Let's start by discussing the project scope. What questions do you have?"
        )
        Message.objects.create(
            user=request.user,
            stakeholder=stakeholder,
            content=welcome_message,
            is_from_stakeholder=True
        )
        # Refresh messages
        messages = Message.objects.filter(
            user=request.user,
            stakeholder=stakeholder
        ).order_by('created_at')
    
    context = {
        'stakeholder': stakeholder,
        'messages': messages,
        'chat_room': chat_room,
    }
    return render(request, 'chat/chat.html', context)


@login_required
@require_http_methods(["POST"])
def send_message(request, stakeholder_id):
    """API endpoint to send a message"""
    stakeholder = get_object_or_404(Stakeholder, id=stakeholder_id)
    content = request.POST.get('content', '').strip()
    
    if not content:
        return JsonResponse({'error': 'Message content is required'}, status=400)
    
    # Save user message
    message = Message.objects.create(
        user=request.user,
        stakeholder=stakeholder,
        content=content,
        is_from_stakeholder=False
    )
    
    # Get AI response (will be handled by WebSocket consumer)
    # For now, return success
    return JsonResponse({
        'success': True,
        'message_id': message.id,
        'content': message.content,
        'created_at': message.created_at.isoformat(),
    })

