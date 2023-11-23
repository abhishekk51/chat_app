import datetime
import uuid

from fastapi import WebSocket, WebSocketDisconnect, status, Response, APIRouter

from server.controllers.messaging_data import MessageData
from server.controllers.conversation_data import ConversationData
from server.managers.messaging_manager import MessagingManager
from server.managers.conversation_manager import ConversationManager
from server.models.chat_message import ChatMessage
from server.models.conversation_model import ConversationCreate

chat_manager = MessagingManager()
conversation_manager = ConversationManager()


conversation_router = APIRouter()


@conversation_router.post("/add-conversation/", status_code=status.HTTP_201_CREATED)
async def handle_add_conversation(conversation: ConversationCreate, response: Response):
    """
        Function to handle new conversation created by a client
    """
    conversation_data = ConversationData()
    conversation = conversation_data.add_conversation(conversation)
    if conversation:
        await conversation_manager.broadcast_conversation(conversation)
        print(conversation, 'conversation details')
        return {"message": "conversation added", "data": {"conversation_id": conversation}}
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": "conversation not added"}


@conversation_router.get("/conversations/{user_id}", status_code=status.HTTP_200_OK)
async def handle_new_connection_conversation(user_id: str, response: Response):
    conversation_data = ConversationData()
    conversation = conversation_data.get_all_conversation(user_id)
    print(conversation, 'conversation details')
    return {"message": None, "data": {"conversation_list": conversation}}


@conversation_router.websocket("/connect-conversation/{conversation_id}")
async def send_message(websocket: WebSocket, conversation_id: str):
    """
        Function to handle new conenctions to the conversation
        The function accepts the connection from the client
        and sends all the available conversation to the client
    """
    messages_data = MessageData()
    conversation_data = ConversationData()
    await chat_manager.connect(websocket, conversation_id)
    try:
        # await conversation_manager.add_conversation_listner(websocket)
        while True:
            # Receive the message from the client
            data = await websocket.receive_json()
            print(f"Received {data}")

            if "type" in data and data["type"] == "close":
                chat_manager.disconnect(websocket, conversation_id)
            else:
                message = ChatMessage(
                    message_id=str(uuid.uuid4()),
                    sender_id=data["sender_id"],
                    receiver_id=data["receiver_id"],
                    message=data["message"],
                    conversation_id=conversation_id,
                    updated_at=datetime.datetime.now().timestamp()
                )
                messages_data.add_message(message)
                conversation_data.update_conversation(conversation_id, {'last_message': data["message"]})

                # Send the message to all the clients
                await chat_manager.broadcast(message, conversation_id)
    except WebSocketDisconnect:
        chat_manager.disconnect(websocket, conversation_id)


@conversation_router.get("/get-messages/{conversation_id}", status_code=status.HTTP_200_OK)
async def handle_new_connection_conversation(conversation_id: str, response: Response):
    message_data = MessageData()
    messages = message_data.get_messages_of(conversation_id)
    print(messages, 'conversation details')
    return {"message": None, "data": {"message_list": messages}}