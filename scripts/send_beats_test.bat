@echo off
REM Contact Automation - TEST RUN (dry run, no emails sent)
REM Use this to verify the task runs correctly without sending real emails.

set PROJECT_DIR=%~dp0..
cd /d "%PROJECT_DIR%"

python main.py send-beats --dry-run

echo Last test run: %date% %time% - Exit code: %ERRORLEVEL% >> logs\scheduled_send.log
