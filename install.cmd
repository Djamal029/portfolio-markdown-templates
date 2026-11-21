@echo off
rem Double-cliquez sur ce fichier pour installer et ouvrir le portfolio (Windows).
rem Variante : install.cmd preview   ou   install.cmd preview-all
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0install.ps1" %*
echo.
pause
