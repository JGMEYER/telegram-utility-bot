import logging
import os

"""Helpful functions for managing environment"""

# Do not use general logger!
#   1. log.py imports env - infinite import loop
logging.basicConfig(level=logging.INFO)
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
