from .base import *

STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"

DEBUG = False

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_REFERRER_POLICY = "same-origin"

SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=[])
if "healthcheck.railway.app" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("healthcheck.railway.app")

ALLOWED_HOSTS = env.list(
    "DJANGO_ALLOWED_HOSTS",
)

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

if SECRET_KEY.startswith("unsafe-"):
    raise RuntimeError("A secure DJANGO_SECRET_KEY is required in production.")
