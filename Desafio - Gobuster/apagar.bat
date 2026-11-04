@echo off
rem Detiene y elimina el contenedor del desafio.
docker rm -f orion7 >nul 2>&1 && echo [ok] Desafio apagado. || echo [i] El desafio no estaba corriendo.
pause
