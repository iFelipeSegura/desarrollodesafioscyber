# Resolución resumida: ORION-7

Pedí ayuda a ChatGPT porque no entendía bien cómo funcionaba Gobuster, cómo interpretar sus resultados ni cómo continuar con las rutas encontradas. Me ayudó a seleccionar comandos, revisar las capturas, decodificar una pista y reunir los fragmentos.

Gobuster prueba nombres de un diccionario para descubrir directorios y archivos. Opciones usadas: `-u` URL, `-w` diccionario, `-x` extensiones, `-t` hilos, `-o` archivo de resultados y `-a` User-Agent.

## Comandos principales utilizados

Enumeración inicial:

```bash
gobuster dir -u http://localhost:8080 -w /usr/share/wordlists/dirb/common.txt -x txt,html,json,bak,old,zip -t 20 -o gobuster-archivos.txt
```

Revisión de las rutas descubiertas:

```bash
curl -i http://localhost:8080/robots.txt
curl -i http://localhost:8080/archive/
curl -i http://localhost:8080/personal/
gobuster dir -u http://localhost:8080/archive/ -w /usr/share/wordlists/dirb/common.txt -x txt,html,json,bak,old,zip -t 20 -o gobuster-archive.txt
gobuster dir -u http://localhost:8080/personal/ -w /usr/share/wordlists/dirb/common.txt -x txt,html,json,bak,old,zip -t 20 -o gobuster-personal.txt
```

Lectura del respaldo y decodificación de su nota:

```bash
curl -i http://localhost:8080/archive/config.bak | tee evidencia-config.txt
curl -s http://localhost:8080/archive/config.bak | sed -n 's/^nota_operador *= *//p' | tr -d '\r' | base64 -d | tee nota-decodificada.txt
```

Acceso y enumeración con el agente indicado en la pista:

```bash
curl -i -A 'SENTINEL/2.1' http://localhost:8080/core/ | tee evidencia-core.txt
gobuster dir -u http://localhost:8080/core/ -a 'SENTINEL/2.1' -w /usr/share/wordlists/dirb/common.txt -x txt,html,json,bak,old,zip -t 20 -o gobuster-core.txt
curl -i -A 'SENTINEL/2.1' http://localhost:8080/core/console/ | tee evidencia-console.txt
gobuster dir -u http://localhost:8080/core/console/ -a 'SENTINEL/2.1' -w /usr/share/wordlists/dirb/common.txt -x txt,html,json,bak,old,zip -t 20 -o gobuster-console.txt
```

## Resultado

- `n4d4`: HTML de la respuesta 403 de `/archive/`.
- `3st4`: nota Base64 de `/archive/config.bak`.
- `0cult0`: `/core/console/`, usando el agente `SENTINEL/2.1`.

```text
FLAG{n4d4_3st4_0cult0}
```

Aprendí que un 403 puede impedir listar un directorio sin bloquear sus archivos, y que hay que repetir Gobuster dentro de las rutas descubiertas. Inicialmente usé `/DIRECTORIO/` literalmente y consulté `status.json`, que era solo un ejemplo; esas pruebas no dieron resultados útiles.
