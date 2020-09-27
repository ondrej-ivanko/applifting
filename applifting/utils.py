"""
Utility helper functions.
"""
import os
import logging

logger = logging.getLogger(__name__)


def check_and_get_offers_token():
    access_token = os.getenv("access_token")
    assert access_token, logger.error(
        "access_token not yet received. Run get_offers_token.sh"
    )
    return access_token
