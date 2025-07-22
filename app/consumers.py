# app/consumers.py

import json

from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.group_name = f"notifications_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def notify(self, event):
        # This method is called when a message is sent to the group
        await self.send(
            text_data=json.dumps(
                {
                    "message": event["message"],
                    "url": event.get("url"),
                    "sender_avatar_url": event.get("sender_avatar_url"),
                }
            )
        )
