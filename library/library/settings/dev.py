import logging

from library.settings.base import *  # noqa: F401, F403

logger = logging.getLogger("app")
logger.info("Run in debug regime")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS.append("debug_toolbar")  # noqa: F405

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware"
] + MIDDLEWARE  # noqa: F405


INTERNAL_IPS = [
    "127.0.0.1",
]
