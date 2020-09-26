from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json


class TableConsumer(WebsocketConsumer):
    def connect(self):
        self.table_number = self.scope['url_route']['kwargs']['table_number']
        self.restoran_id = self.scope['url_route']['kwargs']['restoran_id']
        self.room_group_name = str('restoran_' + str(self.restoran_id) + '_table_'+str(self.table_number))

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # username = text_data_json['username']
        print('receive')

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                # 'username': username
            }
        )

    def chat_message(self, event):
        message = event['message']
        # username = event['username']
        print('chat_message')
        self.send(text_data=json.dumps({
            'event': "Send",
            'message': message,
            # 'username': username
        }))