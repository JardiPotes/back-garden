class GardenFactory:
    def create_garden(
        userId: str = "1",
        title: str = "ma plantation",
        description: str = "un joli jardin",
        address: str = "chez Isciane",
        zipcode: str = "75000",
    ):
        return locals()
