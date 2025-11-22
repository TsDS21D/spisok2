import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import NameEntry

class NamesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Группа для всех подключенных клиентов
        self.room_group_name = 'names_updates'
        
        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Отправляем текущий список имен новому подключению
        names_list = await self.get_names_list()
        await self.send(text_data=json.dumps({
            'type': 'initial_data',
            'names': names_list
        }))

    async def disconnect(self, close_code):
        # Покидаем группу при отключении
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Получаем сообщение от WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')
        
        if message_type == 'new_name_added':
            # Когда новое имя добавлено, рассылаем обновление всем
            names_list = await self.get_names_list()
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'names_update',
                    'names': names_list
                }
            )

    # Получаем сообщение из группы
    async def names_update(self, event):
        names = event['names']
        
        # Отправляем обновленный список всем подключенным клиентам
        await self.send(text_data=json.dumps({
            'type': 'names_updated',
            'names': names
        }))

    @sync_to_async
    def get_names_list(self):
        """Асинхронно получаем список имен из базы данных"""
        names = NameEntry.objects.all().order_by('order_number')
        return [
            {
                'id': name.id,
                'order_number': name.order_number,
                'name': name.name,
                'created_at': name.created_at.isoformat()
            }
            for name in names
        ]