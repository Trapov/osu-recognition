$RUNNABLE_PACKAGES_DIRECTORY = 'runnable_packages'
$REST_MODULE = 'rest.api'

$REST_RUNNABLE = "$($RUNNABLE_PACKAGES_DIRECTORY).$($REST_MODULE):app"

Write-Host -message "Running [Rest] ==>  $REST_RUNNABLE <== "

& uvicorn $REST_RUNNABLE