import json
from chat.models import GroupChat,Message
from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async
from .models import Forbidden


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.user = self.scope['user']
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat = await self.get_chat()
        self.chat_room_id = f"chat_{self.chat_id}"
        if self.chat:
            await self.channel_layer.group_add(
                self.chat_room_id,
                self.channel_name
            )
            await self.send({
                'type': 'websocket.accept'
            })
        else:
            await self.send({
                'type': 'websocket.close'
            })

    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room_id,
            self.channel_name
        )
        raise StopConsumer()

    async def websocket_receive(self, event):
        text_data = event.get('text', None)
        if text_data:
            text_data_json = json.loads(text_data)
            text = text_data_json['text']
            bads = []
            async for obj in Forbidden.objects.filter(active_flag=True):
                bads.append(obj.Forbiden_msg)
            editedtext = text
            for i in bads:
                if i in text:
                    editedtext = text.replace(i, '****')
                    print(text.replace(i, '****'))

            print(editedtext)
            await self.create_message(editedtext)
            await self.channel_layer.group_send(
                self.chat_room_id,
                {
                    'type': 'chat_message',
                    'message': json.dumps({'type': "msg", 'sender': self.user.username, 'text': editedtext}),
                    'sender_channel_name': self.channel_name
                }
            )

    async def chat_message(self, event):
        message = event['message']
        if self.channel_name != event['sender_channel_name']:
            await self.send({
                'type': 'websocket.send',
                'text': message
            })

    async def chat_activity(self, event):
        message = event['message']
        await self.send({
            'type': 'websocket.send',
            'text': message
        })

    @database_sync_to_async
    def get_chat(self):
        try:
            chat = GroupChat.objects.get(unique_code=self.chat_id)
            return chat
        except GroupChat.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, text):

        Message.objects.create(chat_id=self.chat.id, author_id=self.user.id, text=text)
