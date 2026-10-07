@echo off
setlocal
cd /d "%~dp0"

echo ======================================================
echo              PHISHLENS 2.0 LAUNCHER
echo ======================================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher ^(py^) was not found.
  echo Install Python 3.11+ from https://www.python.org/downloads/
  pause
  exit /b 1
)

echo Checking Python version...
py -c "import sys; v=sys.version_info; print(f'Python {v.major}.{v.minor}.{v.micro}')"

where node >nul 2>nul
if errorlevel 1 (
  echo Node.js was not found.
  echo Install Node.js LTS from https://nodejs.org/
  pause
  exit /b 1
)

if not exist "backend\.venv\Scripts\python.exe" (
  echo Creating Python virtual environment...
  py -m venv backend\.venv
  if errorlevel 1 (
    echo Could not create the Python virtual environment.
    pause
    exit /b 1
  )
)

echo.
echo Upgrading pip...
backend\.venv\Scripts\python.exe -m pip install --upgrade pip
if errorlevel 1 (
  echo Pip upgrade failed. Continuing with the existing pip version...
)

echo.
echo Installing/checking backend dependencies using pre-built wheels...
echo This release supports Python 3.11 through 3.14 on Windows.
echo PostgreSQL driver: psycopg 3.3.6 with Windows CPython 3.14 wheels.
backend\.venv\Scripts\python.exe -m pip install --only-binary=:all: -r backend\requirements.txt
if errorlevel 1 (
  echo.
  echo Backend dependency installation failed.
  echo If a previous virtual environment is broken, close this window,
  echo delete backend\.venv, and double-click START-PHISHLENS.cmd again.
  echo.
  pause
  exit /b 1
)

if not exist "frontend\node_modules" (
  echo.
  echo Installing frontend dependencies...
  pushd frontend
  call npm.cmd install
  if errorlevel 1 (
    popd
    echo Frontend dependency installation failed.
    pause
    exit /b 1
  )
  popd
)

start "PhishLens Backend" powershell -NoExit -Command "Set-Location '%~dp0backend'; .\.venv\Scripts\python.exe -m uvicorn app.main:app --reload"
start "PhishLens Frontend" powershell -NoExit -Command "Set-Location '%~dp0frontend'; npm.cmd run dev"

timeout /t 4 /nobreak >nul
start http://localhost:5173

echo.
echo PhishLens is starting.
echo Backend:  http://127.0.0.1:8000/docs
echo Frontend: http://localhost:5173
echo.
pause
