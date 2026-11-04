# Resolución del desafío

## Reto 1: John the Ripper

Extrajimos el hash de `secreto.zip` y usamos el diccionario de Kali:

```bash
zip2john /home/kali/Desktop/secreto.zip > hash.txt
john --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show hash.txt
```

El archivo llamado `rockyou.txt` del escritorio contenía un hash, por lo que lo reemplazamos por el diccionario del sistema. Recuperamos la contraseña **Panda123** y abrimos `nota.txt`, cuyo contenido era: «Nota confidencial del curso de ciberseguridad».

## Reto 2: Hashcat

Intentamos un ataque de máscara para SHA-512 crypt: una mayúscula, cinco minúsculas y dos dígitos.

```powershell
.\hashcat.exe -O -m 1800 -a 3 h2.txt "?u?l?l?l?l?l?d?d"
```

En Kali instalamos PoCL para habilitar la CPU y usamos `-O` por falta de memoria. Luego ejecutamos Hashcat en Windows con una RTX 3070. El tiempo estimado bajó de aproximadamente un año a un día, pero **no completamos el reto 2 por el tiempo que requería la búsqueda**.

## Apoyo utilizado

Usé **ChatGPT** para interpretar los errores, corregir los comandos y configurar las herramientas durante la resolución.
