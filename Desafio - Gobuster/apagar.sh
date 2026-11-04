#!/bin/sh
# Detiene y elimina el contenedor del desafío.
if docker rm -f orion7 >/dev/null 2>&1; then
  echo "[ok] Desafío apagado."
else
  echo "[i] El desafío no estaba corriendo."
fi
