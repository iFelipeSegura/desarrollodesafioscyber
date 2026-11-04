from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

HOST = "127.0.0.1"
PORT = 8090

USUARIO_OK = "admin"
PASS_OK = "admin123"

FORM = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Login demo</title>
  <style>
    body {{ font-family: sans-serif; display:flex; justify-content:center;
           align-items:center; height:100vh; margin:0; background:#111; color:#eee; }}
    form {{ background:#1e1e1e; padding:2rem; border-radius:10px; width:280px; }}
    input {{ width:100%; padding:.6rem; margin:.4rem 0; box-sizing:border-box;
             border:1px solid #444; border-radius:6px; background:#000; color:#fff; }}
    button {{ width:100%; padding:.6rem; margin-top:.6rem; border:0; border-radius:6px;
              background:#3b82f6; color:#fff; font-weight:bold; cursor:pointer; }}
    .msg {{ margin-bottom:.8rem; font-size:.9rem; }}
    .ok {{ color:#4ade80; }}
    .err {{ color:#f87171; }}
  </style>
</head>
<body>
  <form method="POST" action="/login">
    <h2>Iniciar sesion</h2>
    <div class="msg {clase}">{mensaje}</div>
    <input type="text" name="usuario" placeholder="Usuario" autofocus>
    <input type="password" name="password" placeholder="Contrasena">
    <button type="submit">Entrar</button>
  </form>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):

    def _html(self, body, code=200):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._html(FORM.format(clase="", mensaje="Ingresa tus credenciales"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        campos = parse_qs(raw)
        usuario = campos.get("usuario", [""])[0]
        password = campos.get("password", [""])[0]

        print(f"[LOGIN] usuario={usuario!r}  password={password!r}")

        if usuario == USUARIO_OK and password == PASS_OK:
            self._html(FORM.format(clase="ok", mensaje="Acceso concedido ✔"))
        else:
            self._html(FORM.format(clase="err", mensaje="Usuario o contrasena incorrectos"))

    def log_message(self, fmt, *args):
        # silencia el log por defecto; dejamos solo el print del login
        pass


if __name__ == "__main__":
    srv = HTTPServer((HOST, PORT), Handler)
    print(f"Servidor en http://{HOST}:{PORT}  (Ctrl+C para parar)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nAdios.")
        srv.server_close()
