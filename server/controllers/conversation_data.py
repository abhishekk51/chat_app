"""Module providing the conversationData class to interact with the conversation controllers"""
from pymongo.collection import Collection

from databases import MongoDBConnection
from server.models.conversation import Conversation, UserConversationMap


class ConversationData:
    """
    conversationData class
    """

    def __init__(self):
        # use pymongo to connect to the database
        self.client = MongoDBConnection().client
        self.data_base = self.client["chat"]
        self.conversion_collection: Collection[Conversation] = self.data_base["conversation"]
        self.user_conversion_collection: Collection[Conversation] = self.data_base["user_conversation_map"]

    def add_conversation(self, conversation: Conversation):
        """
            Adds a conversation to the database
        """
        # use pymongo to insert the conversation to the database
        # ensure document is updated if it already exists
        print("Adding conversation to the database")
        try:
            valid_conversation = Conversation(**conversation.to_dict())
            if not valid_conversation:
                print("Invalid conversation")
                return None
            result = self.conversion_collection.update_one(
                {"hashed_user_ids": valid_conversation.hashed_user_ids},
                {'$set': valid_conversation.to_dict()},
                upsert=True
            )
            for user in valid_conversation.users:
                valid_user_conversation = UserConversationMap(
                    **{'user_id': user, 'conversion_id': result.upserted_id})
                result = self.user_conversion_collection.update_one(
                    {"conversion_id": valid_user_conversation.conversion_id},
                    {'$set': valid_user_conversation.to_dict()},
                    upsert=True
                )
                if not result:
                    print("Invalid user conversation")
                    return None

            print("conversation added to the database")
            return valid_conversation
        except Exception as error:
            print(error)
            return None

    def get_all_conversation(self):
        """
            Gets all conversation from the database
        """
        # use pymongo to get the conversation from the database
        try:
            print("Getting all conversation from the database")
            conversation_cursor = self.conversion_collection.find()
            return [Conversation(**conversation) for conversation in conversation_cursor]
        except Exception as error:
            print(error)
            return None
