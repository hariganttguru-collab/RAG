"""
Simple test consumer to verify WebSocket connectivity
"""
from channels.generic.websocket import AsyncWebsocketConsumer


class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="Connection successful!")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await self.send(text_data=f"Echo: {text_data}")

