from accounts.models import Garden


class GardenFactory:
    def create_garden_dict(
        userId: str = "1",
        title: str = "ma plantation",
        description: str = "un joli jardin",
        address: str = "chez Isciane",
        zipcode: str = "75000",
    ):
        return locals()

    def create_garden(**kwargs):
        return Garden.objects.create(**GardenFactory.create_garden_dict(**kwargs))
