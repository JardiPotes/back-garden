from apis.models import Garden
import string
import random


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


class TestHelper:

    def random_string_more_than_hundred_char(size):
        basic_str = string.ascii_letters
        res = ''.join(random.choices(basic_str, k=size))
        return res
