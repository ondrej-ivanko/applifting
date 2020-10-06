#!/usr/bin/env python
import os
import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "https://applifting-python-excercise-ms.herokuapp.com/api/v1")

# make sure your .env file is in the BASE_DIR of your project
try:
    response = requests.post(url=f"{BASE_URL}/auth")
    if response.status_code != 201:
        logger.error("Unexpected response")
        response.raise_for_status()
    token = response.json()["access_token"]
except Exception as exc:
    logger.error(f"Could not connect to Offers microservice because of this exception: {exc}")
else:
    os.environ["access_token"] = token