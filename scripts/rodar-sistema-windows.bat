@echo off
setlocal

cd /d "%~dp0.."

mvn javafx:run

endlocal