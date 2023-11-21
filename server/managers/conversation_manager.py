"""
    Class to manage the conversations listeners
"""
from server.models.conversation import Conversation
from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder


class ConversationManager:
    """ conversationsManager class to manager the conversations listeners """

    def __init__(self):
        self.conversation_listeners: set[WebSocket] = set([])

    async def add_conversation_listner(self, websocket: WebSocket):
        """ Adds the websocket connection to the conversations listeners """
        await websocket.accept()
        self.conversation_listeners.add(websocket)

    async def remove_conversation_listner(self, websocket: WebSocket):
        """ Removes the websocket connection from the conversations listeners """
        self.conversation_listeners.remove(websocket)

    async def send_conversation_to(self, websocket: WebSocket, conversation: Conversation):
        """ Sends the conversation to a specific client """
        json_conversation = jsonable_encoder(conversation.to_dict())
        await websocket.send_json(json_conversation)

    async def broadcast_conversation(self, conversation: Conversation):
        """ Sends the conversation to all the clients """
        json_conversation = jsonable_encoder(conversation.to_dict())
        print(f"Brodcasting to {len(self.conversation_listeners)} clients")
        print(f"Broadcasting conversation: {json_conversation}")
        bad_clients = []
        for client in self.conversation_listeners:
            try:
                await client.send_json(json_conversation)
            except Exception:
                bad_clients.append(client)

        for client in bad_clients:
            self.conversation_listeners.remove(client)
