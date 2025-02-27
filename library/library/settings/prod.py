import logging

from library.settings.base import *  # noqa: F401, F403

logger = logging.getLogger("app")
logger.info("Run in prod regime")

DEBUG = False

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)
