@echo off

echo Checking Python installation...

:: Check if Python is installed
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in your PATH environment variable.
    echo Please install Python and add it to your PATH.
    pause
    exit /b 1
)

echo Python is installed.

:: Get Python version
for /f "tokens=2 delims= " %%a in ('python --version 2^>^&1') do (
    echo Python version: %%a
    set PYTHON_VERSION=%%a
)

:: Check if a valid Python version was retrieved
if "%PYTHON_VERSION%"=="" (
    echo Error retrieving Python version.
    pause
    exit /b 1
)

echo Installing Python libraries from requirements.txt...

::Check for requirements.txt
if not exist requirements.txt (
    echo Error: requirements.txt not found!
    pause
    exit /b 1
)

pip install --upgrade pip

pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Error installing libraries! Check the requirements.txt file and your internet connection. :(
    pause
    exit /b %errorlevel%
)

echo Libraries have been successfully installed! :)
pause
exit
