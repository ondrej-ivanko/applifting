#!/usr/bin/env python
import os
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# os.getenv() can't for some reason locate ENV VAR BASE_URL, so fallback option set
BASE_URL = os.getenv("BASE_URL", "https://applifting-python-excercise-ms.herokuapp.com/api/v1")

# make sure your .env file is in the BASE_DIR of your project
with open(".env_local_dev", "r+") as env:
    if "access_token" in env.read():
        logger.warn("Token already present in the '.env_local_dev' file.")
    else:
        try:
            response = requests.post(url=f"{BASE_URL}/auth")
            if response.status_code != 201:
                logger.error("Unexpected response")
                response.raise_for_status()
            else:
                env.write(f"access_token={response.json()['access_token']}")
        except Exception as exc:
            logger.error(f"Could not connect to Offers microservice because of this exception: {exc}")