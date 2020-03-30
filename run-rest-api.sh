#!/bin/bash
# GNU bash, version 4.3.46

RUNNABLE_PACKAGES_DIRECTORY="runnable_packages"
REST_MODULE="rest.api"

REST_RUNNABLE=$RUNNABLE_PACKAGES_DIRECTORY.$REST_MODULE:app

echo "Running [Rest] ==>" $REST_RUNNABLE " <== "

uvicorn $REST_RUNNABLE