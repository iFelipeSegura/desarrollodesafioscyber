# Resolución del desafío Wireshark

Usé ChatGPT (Codex) para resolver el desafío. Me ayudó a automatizar la prueba, capturar el tráfico HTTP y analizar las credenciales.

Se ejecutó el servidor local incluido y se envió un login mediante un cliente Python. La captura se realizó con dumpcap y se analizó con TShark, herramientas de Wireshark.

- **IP de origen y destino:** `127.0.0.1`. Son iguales porque la prueba se realizó en el mismo equipo, sobre la interfaz loopback.
- **Puerto de destino:** `8090`.
- **Login identificado:** `POST /login`, paquete `20`.
- **Usuario:** `admin`.
- **Contraseña:** `admin123`.

Filtro para aislar el login:

```wireshark
tcp.port == 8090 && http.request.method == "POST"
```

El cuerpo de la petición mostró las credenciales sin cifrar:

```text
usuario=admin&password=admin123
```

**Conclusión:** HTTP transmite las credenciales en texto legible. HTTPS cifra la comunicación para protegerlas durante el transporte.

**Evidencias:** [captura real](evidencias/login_http.pcapng) y [flujo TCP con las credenciales](evidencias/flujo_login.txt).
