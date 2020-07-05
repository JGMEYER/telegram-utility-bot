import logging
import os

"""Helpful functions for managing environment"""

# Do not use general logger!
#   1. log.py imports env - infinite import loop
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def getenv(var):
    """HACK get environment variable, i.e. use dev for running local
    unit/integration tests
    """
    if var in os.environ:
        return os.environ[var]

    log.warning(f"{var} missing, defaulting to {var}_DEV")

    try:
        return os.environ[f"{var}_DEV"]
    except KeyError:
        log.error(
            f"Failed to fetch {var}_DEV when defaulting to DEV. Make sure "
            "this variable is defined and you've refreshed the environment.",
            exc_info=True,
        )
        raise
