import json

from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from chat.models import Thread


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)
        await self.send({
            'type': 'websocket.accept'
        })
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)
        # await asyncio.sleep(10)

    async def websocket_receive(self, event):
        print('receive', event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            print(msg)
            user = self.scope['user']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            my_response = {
                'message': msg,
                'username': username
            }
            await self.send({
                'type': 'websocket.send',
                'text': json.dumps(my_response)
            })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)[0]
