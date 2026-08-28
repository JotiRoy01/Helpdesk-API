from django.conf import settings


def test_testing_database_is_not_production_database():
    database_name = settings.DATABASES[
        "default"
    ]["NAME"]

    assert str(database_name).lower() not in {
        "production",
        "prod",
    }