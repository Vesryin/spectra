@echo off
echo 🌟 SpectraAI Quick Setup
echo ========================

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo ✅ Dependencies installed!
echo.
echo 🔑 Next steps:
echo 1. Get your OpenAI API key from: https://platform.openai.com/api-keys
echo 2. Edit config/secrets.env and set your OPENAI_API_KEY
echo 3. Run: python launch.py
echo.
pause
