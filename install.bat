@echo off
echo Installing GameLogger...

:: Check Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found. Please install Python and try again.
    pause
    exit /b
)

:: Check pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip not found. Please install pip and try again.
    pause
    exit /b
)

:: Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

:: Create GameLogger folder
echo Creating C:\GameLogger...
mkdir "C:\GameLogger" 2>nul

:: Create templates folder
mkdir "C:\GameLogger\templates" 2>nul

:: Copy files
echo Copying files...
copy "check_game.py" "C:\GameLogger\check_game.py"
copy "check_game.bat" "C:\GameLogger\check_game.bat"
copy "dashboard.py" "C:\GameLogger\dashboard.py"
copy "launch_dashboard.bat" "C:\GameLogger\launch_dashboard.bat"
copy "templates\index.html" "C:\GameLogger\templates\index.html"

:: Create .env template if one doesn't already exist
if not exist "C:\GameLogger\.env" (
    echo Creating .env template...
    (
        echo RAWG_API_KEY=your_rawg_api_key
        echo DB_HOST=localhost
        echo DB_PORT=5432
        echo DB_NAME=gamelogger
        echo DB_USER=postgres
        echo DB_PASSWORD=your_postgres_password
    ) > "C:\GameLogger\.env"
    echo .env template created. Please fill in your credentials at C:\GameLogger\.env before using GameLogger.
) else (
    echo .env file already exists, skipping...
)

:: Register context menu
echo Registering right-click context menu...
regedit /s "install.reg"

echo.
echo Installation complete!
echo Remember to fill in your credentials in C:\GameLogger\.env if you haven't already.
pause