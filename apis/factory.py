import random
import string

from apis.models import Conversation, Garden, Message


class GardenFactory:
    def create_garden_dict(
        user_id: str = "1",
        title: str = "ma plantation",
        description: str = "un joli jardin",
        address: str = "chez Isciane",
        zipcode: str = "75000",
    ):
        return locals()

    def create_garden(**kwargs):
        return Garden.objects.create(**GardenFactory.create_garden_dict(**kwargs))


class ConversationFactory:
    def create_conversation_dict(
        chat_sender_id: str = "1", chat_receiver_id: str = "2"
    ):
        return locals()

    def create_conversation(**kwargs):
        return Conversation.objects.create(
            **ConversationFactory.create_conversation_dict(**kwargs)
        )


class MessageFactory:
    def create_message_dict(
        conversation_id: str = "1",
        sender_id: str = "1",
        content: str = "Testing Testing",
    ):
        return locals()

    def create_message(**kwargs):
        return Message.objects.create(**MessageFactory.create_message_dict(**kwargs))


class TestHelper:
    def random_string_more_than_hundred_char(size):
        basic_str = string.ascii_letters
        res = "".join(random.choices(basic_str, k=size))
        return res
