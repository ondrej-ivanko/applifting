#!/usr/bin/env bash

# -- i prefer this script to get access_token.sh. it's less language dependent and more os dependent. -- "
# Possible to run with: source <script_name.sh> and export variable in script to parent local terminal with 'export' kwd.
BASE_URL=https://applifting-python-excercise-ms.herokuapp.com/api/v1

# ACCESS_TOKEN=`curl -X POST --retry-connrefused --url $BASE_URL/auth | python3 -c "import sys,json;    print(json.dumps(json.load(sys.stdin)['access_token']))" | awk '{print $1}'`
ACCESS_TOKEN=`curl -X POST --retry-connrefused $BASE_URL/auth | awk -F'[{":]' '{print $6}'`
if grep -Fq "ACCESS_TOKEN=" .env_local_dev
then
    echo "ACCESS_TOKEN already in .env_local_dev file."
else
    printf "\nACCESS_TOKEN=$ACCESS_TOKEN\n" >> .env_local_dev
fi
if grep -Fq "BASE_URL=" .env_local_dev
then
    echo "BASE_URL already in .env_local_dev file."
else
    printf "\nBASE_URL=$BASE_URL\n" >> .env_local_dev
fi