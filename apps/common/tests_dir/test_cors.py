from django.conf import settings


def test_cors_is_not_open_to_every_origin():
    assert (
        getattr(
            settings,
            "CORS_ALLOW_ALL_ORIGINS",
            False,
        )
        is not True
    )
