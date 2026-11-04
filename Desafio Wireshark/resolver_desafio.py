"""Genera tráfico HTTP local y captura evidencia real con Wireshark."""
import importlib.util
import json
from pathlib import Path
import subprocess
import threading
import time
from urllib.request import ProxyHandler, Request, build_opener

ROOT = Path(__file__).resolve().parent
WS = Path(r"C:\Program Files\Wireshark")
OUT = ROOT / "evidencias"


def main():
    OUT.mkdir(exist_ok=True)
    capture = OUT / "login_http.pcapng"
    if capture.exists():
        raise SystemExit("Ya existe la captura; no se sobrescribe.")
    spec = importlib.util.spec_from_file_location("demo", ROOT / "Codigo_levantar_http_local.py")
    demo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(demo)
    server = demo.HTTPServer((demo.HOST, demo.PORT), demo.Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    proc = None
    try:
        with (OUT / "captura.log").open("w", encoding="utf-8") as log:
            proc = subprocess.Popen(
                [str(WS / "dumpcap.exe"), "-i", r"\Device\NPF_Loopback",
                 "-f", "tcp port 8090", "-a", "duration:12", "-w", str(capture)],
                stdout=log, stderr=log,
            )
            deadline = time.monotonic() + 8
            while True:
                if proc.poll() is not None:
                    raise RuntimeError("Falló dumpcap; revisa evidencias/captura.log")
                if "Capturing on" in (OUT / "captura.log").read_text(encoding="utf-8", errors="replace"):
                    break
                if time.monotonic() > deadline:
                    raise RuntimeError("La captura no se inició a tiempo.")
                time.sleep(0.2)
            time.sleep(1)
            client = build_opener(ProxyHandler({}))
            with client.open("http://127.0.0.1:8090/", timeout=5) as response:
                response.read()
            request = Request("http://127.0.0.1:8090/login",
                              data=b"usuario=admin&password=admin123",
                              headers={"Content-Type": "application/x-www-form-urlencoded"})
            with client.open(request, timeout=5) as response:
                page = response.read().decode("utf-8")
                assert "Acceso concedido" in page, "El servidor rechazó el login"
                (OUT / "respuesta_login.html").write_text(page, encoding="utf-8")
            if proc.wait(timeout=20) != 0:
                raise RuntimeError("dumpcap terminó con error")
    finally:
        if proc is not None and proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=5)
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    base = [str(WS / "tshark.exe"), "-n", "-r", str(capture), "-d", "tcp.port==8090,http"]
    result = subprocess.run(base + ["-Y", 'http.request.method == "POST"', "-T", "json"],
                            capture_output=True, text=True, encoding="utf-8", check=True, timeout=30)
    (OUT / "login_post.json").write_text(result.stdout, encoding="utf-8")
    packets = json.loads(result.stdout)
    assert len(packets) == 1, f"Se esperaba un POST: {len(packets)}"
    layers = packets[0]["_source"]["layers"]
    stream = layers["tcp"]["tcp.stream"]
    follow = subprocess.run(base + ["-q", "-z", f"follow,tcp,ascii,{stream}"],
                            capture_output=True, text=True, encoding="utf-8", check=True, timeout=30)
    assert "usuario=admin&password=admin123" in follow.stdout
    (OUT / "flujo_login.txt").write_text(follow.stdout, encoding="utf-8")
    details = subprocess.run(base + ["-Y", 'http.request.method == "POST"', "-V"],
                             capture_output=True, text=True, encoding="utf-8", check=True, timeout=30)
    (OUT / "detalle_post.txt").write_text(details.stdout, encoding="utf-8")
    print(json.dumps({"captura": str(capture), "paquete_post": layers["frame"]["frame.number"],
                      "origen": layers["ip"]["ip.src"], "destino": layers["ip"]["ip.dst"],
                      "puerto_origen": layers["tcp"]["tcp.srcport"],
                      "puerto_destino": layers["tcp"]["tcp.dstport"], "flujo_tcp": stream}, indent=2))


if __name__ == "__main__":
    main()
