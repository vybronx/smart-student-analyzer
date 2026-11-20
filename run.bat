@echo off
echo ====================================================
echo   SMART STUDENT ANALYZER
echo   A Smart System for Student Performance Analysis
echo ====================================================
echo.
echo [1/2] Checking Python environment...
python --version
if errorlevel 1 (
    echo Python is not installed or not in PATH! Please install Python 3.x.
    pause
    exit /b
)

echo.
echo [2/2] Launching Flask Development Server on http://127.0.0.1:5000...
python app.py
pause
