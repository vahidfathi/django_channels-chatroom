from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid
import json
from .models import Chatrooms, Messages, Profiles


class ChatConsumer(AsyncWebsocketConsumer):

    @database_sync_to_async
    def check_chat_exist(self, chatroom_id):
        try:
            result = User.objects.filter(id = chatroom_id).count()
        except ValueError:
            result = Chatrooms.objects.filter(id=chatroom_id).count()
            
        except ValidationError:
            return False
        finally:
            if result == 1:
                return True
            else:
                return False

    @database_sync_to_async
    def save_message(self, sender, message, reciecer, message_type=1, reciever_type=1):
        obj = Messages(
            sender=sender.profile,
            message=message,
            reciever_id=reciecer,
            reciever_type=reciever_type,
            message_type=message_type
        )
        obj.save()
        return obj.id
            


    async def connect(self):
        user = self.scope['user']
        self.chatroom_id = self.scope["url_route"]["kwargs"]["room_id"] 
        if not user.is_authenticated or not await self.check_chat_exist(self.chatroom_id):
            await self.close()
            return
        

        await self.channel_layer.group_add(
            self.chatroom_id,
            self.channel_name

        )

        # # Join room group
        # await self.channel_layer.group_add(
        #     self.room_group_name,
        #     self.channel_name
        # )

        await self.accept()
    

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.chatroom_id,
            self.channel_name
        )

    # Receive message from WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = dict()
        message["pm"] = text_data_json['message']
        user = self.scope["user"]
        message["user"] = user.username
        print(await self.save_message(user, text_data_json["message"], self.chatroom_id))


        # Send message to room group
        await self.channel_layer.group_send(
            self.chatroom_id,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))