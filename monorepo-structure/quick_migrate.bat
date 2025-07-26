@echo off
echo ========================================
echo  SpectraAI Monorepo Migration Script
echo ========================================
echo.

echo Creating target directory structure...
mkdir ..\SpectraAI-Monorepo 2>nul
cd ..\SpectraAI-Monorepo

echo Creating monorepo folders...
mkdir spectra-core\src 2>nul
mkdir spectra-core\tests 2>nul
mkdir spectra-core\data 2>nul
mkdir spectra-api\src\api 2>nul
mkdir spectra-api\src\websockets 2>nul
mkdir spectra-api\src\middleware 2>nul
mkdir spectra-api\src\models 2>nul
mkdir spectra-api\src\utils 2>nul
mkdir spectra-api\tests 2>nul
mkdir spectra-ui\public 2>nul
mkdir spectra-ui\src\components 2>nul
mkdir spectra-ui\src\services 2>nul
mkdir spectra-ui\src\hooks 2>nul
mkdir spectra-ui\src\utils 2>nul
mkdir spectra-ui\src\types 2>nul
mkdir spectra-tools\setup 2>nul
mkdir spectra-tools\scripts 2>nul
mkdir spectra-tools\docker 2>nul
mkdir spectra-tools\ci 2>nul
mkdir spectra-dev-notes\research 2>nul
mkdir spectra-dev-notes\todos 2>nul
mkdir spectra-dev-notes\logs 2>nul
mkdir spectra-dev-notes\ui-mockups 2>nul
mkdir docs 2>nul

echo.
echo Copying core AI files...
copy ..\spectra\core\*.py spectra-core\src\ >nul 2>&1
copy ..\spectra\logic\*.py spectra-core\src\ >nul 2>&1
copy ..\spectra\config\settings.py spectra-core\src\config.py >nul 2>&1
copy ..\spectra\config\openai_config.py spectra-core\src\ >nul 2>&1

echo Copying data files...
copy ..\spectra\data\memory_store.json spectra-core\data\ >nul 2>&1
copy ..\spectra\requirements.txt spectra-core\ >nul 2>&1

echo Copying test files...
copy ..\spectra\tests\*.py spectra-core\tests\ >nul 2>&1

echo Copying tools and scripts...
copy ..\spectra\setup_local_ai.py spectra-tools\setup\install_models.py >nul 2>&1
copy ..\spectra\setup.bat spectra-tools\scripts\ >nul 2>&1
copy ..\spectra\launcher.py spectra-tools\scripts\ >nul 2>&1
copy ..\spectra\spectra_cleanup.py spectra-tools\scripts\cleanup.py >nul 2>&1

echo.
echo Creating configuration files...

REM Create root package.json
echo {> package.json
echo   "name": "spectra-ai-monorepo",>> package.json
echo   "version": "1.0.0",>> package.json
echo   "private": true,>> package.json
echo   "workspaces": ["spectra-ui"],>> package.json
echo   "scripts": {>> package.json
echo     "setup:all": "npm install && cd spectra-ui && npm install",>> package.json
echo     "dev": "concurrently \"npm run dev:api\" \"npm run dev:ui\"",>> package.json
echo     "dev:api": "cd spectra-api && python src/main.py",>> package.json
echo     "dev:ui": "cd spectra-ui && npm start">> package.json
echo   },>> package.json
echo   "devDependencies": {>> package.json
echo     "concurrently": "^8.2.0">> package.json
echo   }>> package.json
echo }>> package.json

REM Create API requirements.txt
echo fastapi^>=0.104.1> spectra-api\requirements.txt
echo uvicorn[standard]^>=0.24.0>> spectra-api\requirements.txt
echo websockets^>=12.0>> spectra-api\requirements.txt
echo pydantic^>=2.5.0>> spectra-api\requirements.txt
echo python-multipart^>=0.0.6>> spectra-api\requirements.txt
echo python-dotenv^>=1.0.0>> spectra-api\requirements.txt

REM Create basic UI package.json
echo {> spectra-ui\package.json
echo   "name": "spectra-ui",>> spectra-ui\package.json
echo   "version": "1.0.0",>> spectra-ui\package.json
echo   "dependencies": {>> spectra-ui\package.json
echo     "@mui/material": "^5.15.0",>> spectra-ui\package.json
echo     "@mui/icons-material": "^5.15.0",>> spectra-ui\package.json
echo     "react": "^18.2.0",>> spectra-ui\package.json
echo     "react-dom": "^18.2.0",>> spectra-ui\package.json
echo     "react-scripts": "5.0.1",>> spectra-ui\package.json
echo     "typescript": "^4.9.5">> spectra-ui\package.json
echo   },>> spectra-ui\package.json
echo   "scripts": {>> spectra-ui\package.json
echo     "start": "react-scripts start",>> spectra-ui\package.json
echo     "build": "react-scripts build">> spectra-ui\package.json
echo   },>> spectra-ui\package.json
echo   "proxy": "http://localhost:8000">> spectra-ui\package.json
echo }>> spectra-ui\package.json

echo.
echo ========================================
echo  Migration Complete! 
echo ========================================
echo.
echo Next steps:
echo 1. cd SpectraAI-Monorepo
echo 2. npm install
echo 3. Review the copied files
echo 4. Follow MIGRATION_GUIDE.md for next steps
echo.
echo Your original project is preserved in the 'spectra' folder.
echo.
pause
