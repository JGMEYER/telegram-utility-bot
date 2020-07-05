import logging
import os

from .log import setup_logger

"""Helpful functions for managing environment"""

setup_logger(__name__)
log = logging.getLogger(__name__)


def getenv(env):
    """HACK get environment variable, i.e. use dev for running local
    unit/integration tests
    """
    try:
        return os.environ[env]
    except KeyError:
        log.warning(f"{env} missing, defaulting to {env}_DEV")
        return os.environ[env + "_DEV"]
