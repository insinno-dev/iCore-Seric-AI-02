@echo off
REM Device Support Service - Docker Deployment Script for Windows
REM This script simplifies Docker deployment for the application

setlocal enabledelayedexpansion

REM Colors (Windows 10+)
for /F %%A in ('echo prompt $H ^| cmd') do set "BS=%%A"

:menu
cls
echo.
echo Device Support Service - Docker Management
echo =========================================
echo 1) Check prerequisites
echo 2) Check/Create .env configuration
echo 3) Build Docker image
echo 4) Start services
echo 5) Stop services
echo 6) View logs
echo 7) Service status
echo 8) Clean up (remove containers and volumes)
echo 9) Full deployment (check, build, start)
echo 0) Exit
echo.
set /p choice="Select an option (0-9): "

if "%choice%"=="1" goto check_prereq
if "%choice%"=="2" goto check_env
if "%choice%"=="3" goto build
if "%choice%"=="4" goto start_services
if "%choice%"=="5" goto stop_services
if "%choice%"=="6" goto logs
if "%choice%"=="7" goto status
if "%choice%"=="8" goto cleanup
if "%choice%"=="9" goto full_deploy
if "%choice%"=="0" goto exit_script
goto menu

:check_prereq
echo.
echo [INFO] Checking prerequisites...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed. Please install Docker first.
    pause
    goto menu
)
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed. Please install Docker Compose first.
    pause
    goto menu
)
echo [INFO] Docker and Docker Compose are installed ✓
pause
goto menu

:check_env
echo.
if not exist ".env" (
    echo [WARN] .env file not found. Creating from .env.example...
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [INFO] Created .env file. Please edit it with your API keys.
    ) else (
        echo [ERROR] Neither .env nor .env.example found.
        pause
        goto menu
    )
) else (
    echo [INFO] .env file found ✓
)
pause
goto menu

:build
echo.
echo [INFO] Building Docker image...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Failed to build image.
    pause
    goto menu
)
echo [INFO] Docker image built successfully ✓
pause
goto menu

:start_services
echo.
echo [INFO] Starting services...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services.
    pause
    goto menu
)
echo [INFO] Services started ✓
echo.
echo [INFO] Waiting for services to be ready...
timeout /t 5 /nobreak
echo [INFO] Services ready ✓
echo.
echo Access the application at:
echo   Web UI: http://localhost:8501
echo   Qdrant: http://localhost:6333/dashboard
pause
goto menu

:stop_services
echo.
echo [INFO] Stopping services...
docker-compose down
echo [INFO] Services stopped ✓
pause
goto menu

:logs
echo.
echo [INFO] Viewing logs (press Ctrl+C to exit)...
docker-compose logs -f app
goto menu

:status
echo.
echo [INFO] Service Status:
docker-compose ps
pause
goto menu

:cleanup
echo.
set /p confirm="[WARN] This will remove all data. Are you sure? (y/n): "
if /i "%confirm%"=="y" (
    echo [INFO] Cleaning up containers and volumes...
    docker-compose down -v
    echo [INFO] Cleanup complete ✓
) else (
    echo [INFO] Cleanup cancelled
)
pause
goto menu

:full_deploy
echo.
echo [INFO] Running full deployment...
echo.

echo [INFO] Checking prerequisites...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed.
    pause
    goto menu
)
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker Compose is not installed.
    pause
    goto menu
)
echo [INFO] Prerequisites OK ✓

echo.
if not exist ".env" (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo [INFO] Created .env file. Please review and edit if needed.
    )
)

echo.
echo [INFO] Building Docker image...
docker-compose build --no-cache
if errorlevel 1 (
    echo [ERROR] Failed to build image.
    pause
    goto menu
)

echo.
echo [INFO] Starting services...
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start services.
    pause
    goto menu
)

echo.
timeout /t 5 /nobreak

echo.
echo =========================================
echo Deployment Complete! 
echo =========================================
echo.
echo Access the application at:
echo   Web UI: http://localhost:8501
echo   Qdrant: http://localhost:6333/dashboard
echo.
echo View logs: docker-compose logs -f app
echo Stop services: docker-compose down
echo.
pause
goto menu

:exit_script
echo.
echo Exiting...
exit /b 0
