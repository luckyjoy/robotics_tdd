@echo off
setlocal enabledelayedexpansion

echo =========================================================
echo Running Robotics TDD Docker Simulation Tests...
echo Docker Image: robotics-tdd-local:latest
echo =========================================================

:: Check Docker service
echo Checking Docker service and version...
docker --version
IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker is not installed or not running.
    exit /b 1
)

:: Optional: Prune builder cache
echo Pruning Docker builder cache...
docker builder prune -f

:: Build Docker image
echo Building Docker image...
docker build -t robotics-tdd-local:latest .

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker image build failed.
    exit /b 1
)

:: Run Docker container
echo Running Docker container...
docker run --rm robotics-tdd-local:latest

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Docker container execution failed.
    exit /b 1
)

echo =========================================================
echo Simulation completed successfully.
echo =========================================================
endlocal