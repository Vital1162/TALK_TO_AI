import json
from channels.generic.websocket import WebsocketConsumer
from django.core.cache import cache

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        self.send(text_data = json.dumps({
            'type': "connection established",
            'message': 'You are connected'
        }))
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["prompt"]
        top_p = text_data_json["top_p"]
        top_k = text_data_json["top_k"]
        temperature = text_data_json["temperature"]
        max_output_tokens = text_data_json["max_output_tokens"]

        print('prompt: ', message)
        
        #save to cache
        cache.set('adjustment', text_data_json)
        
        self.send(text_data=json.dumps({
            'type':'chat',
            'message': message,
            'top_p': top_p,
            'top_k': top_k,
            'temperature': temperature,
            'max_output_tokens': max_output_tokens,
        }))