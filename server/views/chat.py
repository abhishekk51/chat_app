import uuid
import asyncio

from fastapi import WebSocket, WebSocketDisconnect, status, Response, APIRouter

from server.controllers.messaging_data import MessageData
from server.controllers.conversation_data import ConversationData
from server.managers.messaging_manager import MessagingManager
from server.managers.conversation_manager import ConversationManager
from server.models.chat_message import ChatMessage
from server.models.conversation import Conversation

chat_manager = MessagingManager()
conversation_manager = ConversationManager()


conversation_router = APIRouter()


@conversation_router.post("/add-conversation/", status_code=status.HTTP_201_CREATED)
async def handle_add_conversation(conversation: Conversation, response: Response):
    '''
        Function to handle new conversation created by a client
    '''
    conversation_data = ConversationData()
    conversation = conversation_data.add_conversation(conversation)
    if conversation:
        await conversation_manager.broadcast_conversation(conversation)
        print(conversation, 'conversation details')
        return {"message": "conversation added", "data": {"conversation_id": conversation}}
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": "conversation not added"}


@conversation_router.websocket("/connect-conversation/{conversation_id}")
async def handle_connect_to_conversation(websocket: WebSocket, conversation_id: str):
    '''
        Function to handle connections to a conversation
        The function accepts the connection from the client
        and sends the messages to the client
    '''
    # Accept the connection from the client
    messages_data = MessageData()
    await chat_manager.connect(websocket, conversation_id)

    # Sending the messages to the new client
    messages = messages_data.get_messages_of(conversation_id)
    for message in messages:
        print("Sending message to new client")
        await chat_manager.send_message_to(websocket, message)

    try:
        while True:
            # Receive the message from the client
            data = await websocket.receive_json()
            print(f"Received {data}")

            if "type" in data and data["type"] == "close":
                chat_manager.disconnect(websocket, conversation_id)
            else:
                message = ChatMessage(
                    message_id=str(uuid.uuid4()),
                    user_id=data["user_id"],
                    message=data["message"],
                    conversation_id=data["conversation_id"]
                )
                messages_data.add_message(message)
                # Send the message to all the clients
                await chat_manager.broadcast(message, conversation_id)

    except WebSocketDisconnect:
        # Remove the connection from the list of active connections
        print("Client disconnected")
        chat_manager.disconnect(websocket, conversation_id)


@conversation_router.websocket("/conversation")
async def handle_new_connection_conversation(websocket: WebSocket):
    '''
        Function to handle new conenctions to the conversation
        The function accepts the connection from the client
        and sends all the available conversation to the client
    '''
    conversation_data = ConversationData()
    try:
        await conversation_manager.add_conversation_listner(websocket)
        conversation = conversation_data.get_all_conversation()
        print(f"Sending conversation: {len(conversation)}")
        for conversation in conversation:
            await conversation_manager.send_conversation_to(websocket, conversation)
        while True:
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        await conversation_manager.remove_conversation_listner(websocket)