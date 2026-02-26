@echo off
REM Contact Automation - Scheduled Send Beats
REM Run this script via Windows Task Scheduler for monthly packs.
REM Use the full path to your project below.

set PROJECT_DIR=%~dp0..
cd /d "%PROJECT_DIR%"

REM Use system Python (or change to your venv path, e.g. %PROJECT_DIR%\venv\Scripts\python.exe)
python main.py send-beats

REM Optional: log exit code to a file for debugging
echo Last run: %date% %time% - Exit code: %ERRORLEVEL% >> logs\scheduled_send.log
