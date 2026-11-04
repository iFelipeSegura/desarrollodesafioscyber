@echo off
rem Levanta el desafio ORION-7 en este PC (solo accesible desde localhost).
rem Si el puerto 8080 esta ocupado, cambia el numero de abajo.
set PUERTO=8080
cd /d "%~dp0"

docker info >nul 2>&1 || (echo [x] Docker no esta corriendo. Abre Docker Desktop, espera que inicie y vuelve a ejecutar este archivo. & pause & exit /b 1)

echo Cargando imagen del desafio...
docker load -i orion7.tar >nul || (echo [x] No se pudo cargar orion7.tar & pause & exit /b 1)

docker rm -f orion7 >nul 2>&1
docker run -d --name orion7 --read-only --tmpfs /var/cache/nginx --tmpfs /var/run --tmpfs /tmp --cap-drop ALL --cap-add CHOWN --cap-add SETUID --cap-add SETGID --security-opt no-new-privileges -p 127.0.0.1:%PUERTO%:8080 orion7:1.0 >nul || (echo [x] No se pudo iniciar. Revisa si el puerto %PUERTO% esta ocupado. & pause & exit /b 1)

echo.
echo [ok] Desafio listo en http://localhost:%PUERTO%
echo      Para apagarlo, ejecuta apagar.bat
echo.
pause
