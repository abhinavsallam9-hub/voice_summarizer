@echo off
cd /d "%~dp0"
set HF_HUB_DISABLE_SYMLINKS_WARNING=1
echo Checking / installing required libraries (first time takes a few minutes)...
python -m pip install -q --user -r requirements.txt
echo Starting the app... it will open in your browser.
python -m streamlit run app.py
pause
