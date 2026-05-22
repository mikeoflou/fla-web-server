@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0publish_to_vps.ps1" -User root
pause
