import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Stakeholder, Message, ChatRoom
from apps.ai.agents import get_stakeholder_response


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            # Get user from scope
            self.user = self.scope.get("user")
            
            # Debug: Print scope information
            print(f"WebSocket connect attempt - User: {self.user}, Authenticated: {self.user.is_authenticated if self.user else False}")
            print(f"Scope keys: {list(self.scope.keys())}")
            print(f"URL route: {self.scope.get('url_route', {})}")
            
            # Check authentication
            if not self.user or not self.user.is_authenticated:
                print(f"WebSocket connection rejected: User not authenticated. User: {self.user}")
                # For debugging, let's see what happens if we accept anyway
                # await self.close(code=4001)
                # return
                # Temporarily allow for testing - REMOVE IN PRODUCTION
                print("WARNING: Allowing unauthenticated connection for debugging")
            
            # Get stakeholder ID from URL
            self.stakeholder_id = self.scope['url_route']['kwargs']['stakeholder_id']
            print(f"WebSocket connection attempt: User={self.user.username}, Stakeholder={self.stakeholder_id}")
            
            self.room_group_name = f'chat_{self.user.id}_{self.stakeholder_id}'
            
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            
            await self.accept()
            print(f"WebSocket connected: User={self.user.username}, Stakeholder={self.stakeholder_id}")
        except KeyError as e:
            print(f"WebSocket connection error - KeyError: {e}, Scope keys: {list(self.scope.keys())}")
            await self.close(code=4000)
        except Exception as e:
            print(f"WebSocket connection error: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            await self.close(code=4000)
    
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Receive message from WebSocket"""
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        
        # Get stakeholder
        stakeholder = await self.get_stakeholder(self.stakeholder_id)
        
        # Save user message
        user_message = await self.save_message(
            self.user,
            stakeholder,
            message_content,
            is_from_stakeholder=False
        )
        
        # Send user message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_message',
                'message': message_content,
                'user': self.user.username,
                'timestamp': user_message.created_at.isoformat(),
            }
        )
        
        # Get AI response
        ai_response = await self.get_ai_response(
            self.user,
            stakeholder,
            message_content
        )
        
        # Save AI message
        ai_message = await self.save_message(
            self.user,
            stakeholder,
            ai_response,
            is_from_stakeholder=True
        )
        
        # Send AI response to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'stakeholder_message',
                'message': ai_response,
                'stakeholder': stakeholder.name,
                'timestamp': ai_message.created_at.isoformat(),
            }
        )
    
    async def user_message(self, event):
        """Send user message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'user_message',
            'message': event['message'],
            'user': event['user'],
            'timestamp': event['timestamp'],
        }))
    
    async def stakeholder_message(self, event):
        """Send stakeholder message to WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'stakeholder_message',
            'message': event['message'],
            'stakeholder': event['stakeholder'],
            'timestamp': event['timestamp'],
        }))
    
    @database_sync_to_async
    def get_stakeholder(self, stakeholder_id):
        return Stakeholder.objects.get(id=stakeholder_id)
    
    @database_sync_to_async
    def save_message(self, user, stakeholder, content, is_from_stakeholder):
        # Update or create chat room
        chat_room, _ = ChatRoom.objects.get_or_create(
            user=user,
            stakeholder=stakeholder
        )
        
        return Message.objects.create(
            user=user,
            stakeholder=stakeholder,
            content=content,
            is_from_stakeholder=is_from_stakeholder
        )
    
    @database_sync_to_async
    def get_ai_response(self, user, stakeholder, user_message):
        """Get AI response from LangChain agent"""
        # Get conversation history
        recent_messages = Message.objects.filter(
            user=user,
            stakeholder=stakeholder
        ).order_by('-created_at')[:10]
        
        conversation_history = []
        for msg in reversed(recent_messages):
            role = "stakeholder" if msg.is_from_stakeholder else "user"
            conversation_history.append({
                'role': role,
                'content': msg.content
            })
        
        # Get AI response
        response = get_stakeholder_response(
            stakeholder=stakeholder,
            user_message=user_message,
            conversation_history=conversation_history
        )
        
        return response

