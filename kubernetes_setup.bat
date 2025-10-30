@echo off
SETLOCAL EnableDelayedExpansion

echo Enabling Kubernetes...
echo Verifying Kubernetes...

:: Check if Kubernetes is running
kubectl cluster-info >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Kubernetes is not running or misconfigured.
    echo Please ensure Kubernetes is enabled in Docker Desktop and fully started.
    exit /b 1
)

echo Kubernetes is running.
echo.

:: Deploy sample app
SET DEPLOYMENT_FILE=sample-deployment.yaml
IF NOT EXIST "%DEPLOYMENT_FILE%" (
    echo ERROR: Deployment file "%DEPLOYMENT_FILE%" not found.
    exit /b 1
)

echo Deploying sample app...
kubectl apply -f "%DEPLOYMENT_FILE%"

echo Waiting for pods to start...
timeout /t 10 /nobreak >nul

echo Checking pods and services...
kubectl get pods
kubectl get svc

echo.
echo Open http://localhost:30080 in your browser to view the app.

ENDLOCAL