""" Model class for chat rooms """
import datetime
from pydantic import BaseModel

from server.utils.common_utils import hash_user_ids


class Conversation (BaseModel):
    """
        Conversation dataclass for the chat
    """

    name: str
    description: str
    users: list = []
    is_group: bool = False
    hashed_user_ids: str = None if is_group else hash_user_ids(users)
    updated_at: str = datetime.datetime.now()

    def to_dict(self):
        """
            Converts the room to a dictionary
        """
        return {
            'name': self.name,
            'description': self.description,
            'users': self.users,
            'updated_at': self.updated_at,
            'hashed_user_ids': self.hashed_user_ids
        }


class UserConversationMap(BaseModel):
    """
        UserConversationMap dataclass for the chat
    """

    user_id: str
    conversion_id: str
    updated_at: str = datetime.datetime.now()

    def to_dict(self):
        """
            Converts the room to a dictionary
        """
        return {
            'user_id': self.user_id,
            'conversion_id': self.conversion_id,
            'updated_at': self.updated_at
        }