import uuid


class UserFactory():
    def create_user(
        first_name: str = 'Claudie',
        last_name: str = 'Teston',
        email: str = (lambda: f"{uuid.uuid4()}@test.com")(),
        password: str = 's3cr3tP@SSW0RD',
        has_garden: bool = False,
        bio: str = 'Cives, nos omnes amare debemus hortos nostros. Partire hortos nostros cum ceteris est bonum, quia ex hortis nostris crescere possunt fructus et herbas saporae et salubritatis. Sic, si tu habes hortum magnum et aliis non est hortus, tu debes cum illis partire hortum tuum. Si autem tu non habes hortum, petere hortum ad colendum ab amico potes. Laeti erimus omnes si hortos nostros inter nos partiamur!',
        profile_image="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"
    ):
        return locals()
