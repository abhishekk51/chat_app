"""
    Class to manage the messaging
"""
import asyncio
import json

from fastapi import WebSocket, BackgroundTasks
from fastapi.encoders import jsonable_encoder

from server.managers.redis_manager import RedisPubSubManager
from server.models.chat_message import ChatMessage


class MessagingManager:
    '''
        Manages the active connections
    '''

    def __init__(self) -> None:
        '''
            Initializes the active connections
        '''
        self.active_connections: dict[str, set[WebSocket]] = {}
        self.pubsub_client = RedisPubSubManager()

    async def connect(self, websocket: WebSocket, room_id: str):
        '''
            Adds the connection to the active connections
        '''
        # Accept the user connection
        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = set()
            await self.pubsub_client.connect()
            pubsub_subscriber = await self.pubsub_client.subscribe(room_id)
            task = asyncio.create_task(self._pubsub_data_reader(pubsub_subscriber))
            # BackgroundTasks().add_task(self._pubsub_data_reader, pubsub_subscriber)
        self.active_connections[room_id].add(websocket)

    async def disconnect(self, websocket: WebSocket, room_id: str):
        '''
            Removes the connection from the active connections
        '''
        self.active_connections[room_id].remove(websocket)
        if len(self.active_connections[room_id]) == 0:
            del self.active_connections[room_id]
            await self.pubsub_client.unsubscribe(room_id)

    async def send_message_to(self, websocket: WebSocket, message: ChatMessage):
        '''
            Sends the message to a specific client
        '''
        json_message = jsonable_encoder(message.to_dict())
        await websocket.send_json(json_message)

    async def broadcast(self, message: ChatMessage, room_id: str):
        '''
            Sends the message to all the clients
        '''
        # for connection in self.active_connections[room_id]:
        #     await self.send_message_to(connection, message)

        await self.pubsub_client._publish(room_id, message)

    async def _pubsub_data_reader(self, pubsub_subscriber):
        while True:
            message = await pubsub_subscriber.get_message(ignore_subscribe_messages=True)
            if message is not None:
                print(f"(Reader) Message Received: {message}")
                room_id = message['channel'].decode('utf-8')
                print('room_id', room_id)
                all_sockets = self.active_connections[room_id]
                for socket in all_sockets:
                    data = message['data'].decode('utf-8')
                    deserialized_message = json.loads(data)
                    await socket.send_text(data)