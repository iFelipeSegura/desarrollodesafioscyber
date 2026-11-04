# Desafío CTF: ORION-7

## Historia

ORION-7 es una instalación de datos subterránea (ficticia) que almacena información de nivel restringido. Su portal público se estaba migrando cuando el operador a cargo, K. Vidal, dejó la instalación. Antes de irse, la auditoría interna sospecha que dejó recursos olvidados en el servidor, fuera de la vista del público.

Tu misión: encontrar lo que el operador dejó escondido.

## Objetivo

Obtener la FLAG. Está dividida en **3 fragmentos** repartidos por el servidor. La FLAG final se arma así:

```
FLAG{fragmento1_fragmento2_fragmento3}
```

Cuidado: no todo lo que parece una FLAG lo es.

## Cómo levantar el desafío

Requisito: tener **Docker Desktop** (Windows/Mac) o **Docker** (Linux) instalado y corriendo.

- **Windows:** doble clic en `levantar.bat`.
- **Linux / Mac:** `sh levantar.sh`

Luego abre **http://localhost:8080**. Para apagarlo: `apagar.bat` o `sh apagar.sh`.

## Reglas

1. El **único objetivo autorizado** es `http://localhost:8080`, levantado en tu propio equipo.
2. El desafío se resuelve **desde fuera**, como lo haría un atacante. No vale inspeccionar la imagen ni el contenedor de Docker (`docker exec`, `docker cp`, abrir el `.tar`, etc.).
3. Herramienta principal: **gobuster**. Puedes complementar con el navegador, `curl` y herramientas de decodificación.
4. Diccionario recomendado: `common.txt` de SecLists (`Discovery/Web-Content/common.txt`).

## Pistas

Hay pistas escalonadas disponibles. Pídelas al equipo organizador. **Cada pista usada debe quedar registrada en el informe.**

## Entrega

Informe técnico según la pauta de resolución del curso: análisis inicial, metodología, herramientas y motivo de selección, comandos ejecutados, evidencias (capturas o salida de consola), pistas usadas y FLAG obtenida.
