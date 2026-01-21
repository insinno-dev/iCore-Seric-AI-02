@echo off
REM Docker Validation Script for Windows
REM Checks if Docker setup is correct before deployment

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo   Docker Setup Validation Script
echo ==========================================
echo.

REM Check 1: Docker installed
echo [1/5] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('docker --version') do set docker_version=%%i
echo ✅ %docker_version%

REM Check 2: Docker Compose installed
echo [2/5] Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose not installed
    exit /b 1
)
for /f "tokens=*" %%i in ('docker-compose --version') do set compose_version=%%i
echo ✅ %compose_version%

REM Check 3: .env file exists
echo [3/5] Checking environment file...
if not exist .env (
    echo ⚠️ .env file not found
    echo    Creating from .env.example...
    if exist .env.example (
        copy .env.example .env >nul
        echo ✅ .env created from .env.example
        echo    ⚠️  UPDATE .env WITH YOUR API KEYS!
    ) else (
        echo ❌ .env.example not found
        exit /b 1
    )
) else (
    echo ✅ .env file exists
)

REM Check 4: Dockerfile exists
echo [4/5] Checking Dockerfile...
if not exist Dockerfile (
    echo ❌ Dockerfile not found
    exit /b 1
)
echo ✅ Dockerfile exists

REM Check 5: docker-compose.yml exists
echo [5/5] Checking docker-compose.yml...
if not exist docker-compose.yml (
    echo ❌ docker-compose.yml not found
    exit /b 1
)
echo ✅ docker-compose.yml exists

docker-compose config >nul 2>&1
if errorlevel 1 (
    echo ❌ docker-compose.yml has syntax errors
    docker-compose config
    exit /b 1
)
echo ✅ docker-compose.yml is valid

REM Check required files
echo.
echo Checking required application files...
setlocal enabledelayedexpansion
set missing_files=0
for %%f in (streamlit_app.py agents.py tasks.py rag_service.py requirements.txt) do (
    if not exist %%f (
        echo ❌ %%f not found
        set /a missing_files=!missing_files!+1
    )
)

if !missing_files! gtr 0 (
    exit /b 1
)
echo ✅ All required files present

echo.
echo ==========================================
echo ✅ All checks passed!
echo ==========================================
echo.
echo Next steps:
echo 1. Update .env with your API keys
echo 2. Run: docker-compose build
echo 3. Run: docker-compose up -d
echo 4. Access app at: http://localhost:8501
echo.
pause
