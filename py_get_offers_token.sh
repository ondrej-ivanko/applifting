#!/usr/bin/env python

import os
import sys
import requests
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://applifting-python-excercise-ms.herokuapp.com/api/v1"

# make sure your .env file is in the BASE_DIR of your project
with open(".env_local_dev", "r+") as env:
    contents = env.read()
    if "ACCESS_TOKEN" in contents:
        logger.info("ACCESS_TOKEN already in .env_local_dev file.")
    else:
        try:
            response = requests.post(url=f"{BASE_URL}/auth")
        except Exception as exc:
            logger.error(f"Could not connect to Offers microservice because of this exception: {exc}")
        else:
            if response.status_code != 201:
                logger.error("Unexpected response")
                response.raise_for_status()
            else:
                env.write(f"\nACCESS_TOKEN={response.json()['access_token']}\n")

    if not "BASE_URL" in contents:
        env.write(f"\nBASE_URL={BASE_URL}\n")
    else:
        sys.stdout.write("BASE_URL already in .env_local_dev file.")

