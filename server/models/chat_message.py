"""
    Model class for chat messages
"""
import datetime

from pydantic import BaseModel


class ChatMessage(BaseModel):
    '''
        Chat message dataclass
    '''
    message: str
    message_id: str
    sender_id: str
    receiver_id: str
    conversation_id: str
    updated_at: float
    is_deleted: bool = False

    def to_dict(self):
        return {
            'message': self.message,
            'message_id': self.message_id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'conversation_id': self.conversation_id,
            'updated_at': self.updated_at,
            'is_deleted': self.is_deleted
        }