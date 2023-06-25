import json
from channels.generic.websocket import WebsocketConsumer
from bot.chatbot import get_response, predict_class
from django.utils import timezone

intents = json.loads(open('chatbot_files/intents.json').read())


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # accept connection
        self.accept()

    def disconnect(self, close_code):
        pass

    # receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        me_now = timezone.now()
        ints = predict_class(message)
        res = get_response(ints, intents)
        bot_now = timezone.now()
        # send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'res': res,
            'mydatetime': me_now.isoformat(),
            'botdatetime': bot_now.isoformat(),
        }))