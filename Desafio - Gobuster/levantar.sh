#!/bin/sh
# Levanta el desafío ORION-7 en este equipo (solo accesible desde localhost).
# Uso: sh levantar.sh            (puerto 8080)
#      PUERTO=9090 sh levantar.sh
PUERTO="${PUERTO:-8080}"
cd "$(dirname "$0")" || exit 1

if ! docker info >/dev/null 2>&1; then
  echo "[x] Docker no está corriendo (o falta sudo). Inícialo y vuelve a intentar."
  exit 1
fi

echo "Cargando imagen del desafío..."
docker load -i orion7.tar >/dev/null || { echo "[x] No se pudo cargar orion7.tar"; exit 1; }

docker rm -f orion7 >/dev/null 2>&1
docker run -d --name orion7 \
  --read-only --tmpfs /var/cache/nginx --tmpfs /var/run --tmpfs /tmp \
  --cap-drop ALL --cap-add CHOWN --cap-add SETUID --cap-add SETGID \
  --security-opt no-new-privileges \
  -p "127.0.0.1:${PUERTO}:8080" orion7:1.0 >/dev/null \
  || { echo "[x] No se pudo iniciar. Revisa si el puerto ${PUERTO} está ocupado."; exit 1; }

echo
echo "[ok] Desafío listo en http://localhost:${PUERTO}"
echo "     Para apagarlo: sh apagar.sh"
