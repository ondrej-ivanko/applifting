"""
Utility helper functions.
"""
import os
import logging

logger = logging.getLogger(__name__)


def check_and_get_offers_token():
    access_token = os.getenv("ACCESS_TOKEN")
    assert access_token, logger.error(
        "ACCESS_TOKEN not yet received. Run get_offers_token.sh"
    )
    return access_token
