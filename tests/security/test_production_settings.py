import importlib


def test_production_debug_is_disabled():
    production = importlib.import_module("config.settings.production")

    assert production.DEBUG is False


def test_secure_cookie_configuration():
    production = importlib.import_module("config.settings.production")

    assert production.SESSION_COOKIE_SECURE is True
    assert production.CSRF_COOKIE_SECURE is True


def test_production_ssl_redirect_enabled():
    production = importlib.import_module("config.settings.production")

    assert production.SECURE_SSL_REDIRECT is True
