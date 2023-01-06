import uuid

from django.utils import timezone

from accounts.models import User


class UserFactory:
    def create_user_dict(
        nickname="Teston",
        email: str = None,
        password: str = "s3cr3tP@SSW0RD",
        has_garden: bool = False,
        bio: str = "Cives, nos omnes amare debemus hortos nostros. Partire hortos nostros cum ceteris est bonum, quia ex hortis nostris crescere possunt fructus et herbas saporae et salubritatis. Sic, si tu habes hortum magnum et aliis non est hortus, tu debes cum illis partire hortum tuum. Si autem tu non habes hortum, petere hortum ad colendum ab amico potes. Laeti erimus omnes si hortos nostros inter nos partiamur!",
        profile_image="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        created_at=None,
        updated_at=None,
    ):
        params = locals()
        if not email:
            params["email"] = f"{uuid.uuid4()}@test.com"
        if not created_at:
            params["created_at"] = timezone.now()
        if not updated_at:
            params["updated_at"] = timezone.now()

        return params

    def create_user(**kwargs):
        return User.objects.create(**UserFactory.create_user_dict(**kwargs))
