import uvicorn

RUNNABLE_PACKAGES_DIRECTORY = 'runnable_packages'
REST_MODULE = 'rest.api'

what_package_to_run = f'{RUNNABLE_PACKAGES_DIRECTORY}.{REST_MODULE}:app'
uvicorn.run(what_package_to_run, host="0.0.0.0")