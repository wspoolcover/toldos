"""Monta el visor web (un solo HTML) a partir de visor_tpl.html: incrusta casa_v8.glb y las imágenes (renders, plantas, instalaciones) en base64.
Uso: python visor_build.py [salida.html]  (tras generar los renders con render_blender.py y las plantas con opciones.py e instalaciones.py)."""
import base64, io, sys
from PIL import Image

def jpg(src, w, q):
    im = Image.open(src).convert("RGB")
    if im.width > w: im = im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q, optimize=True); return base64.b64encode(b.getvalue()).decode()

OUT = sys.argv[1] if len(sys.argv) > 1 else "visor_v8.html"
datos = {"R_NORTE": jpg("render_exterior_norte.png", 1400, 82), "R_SUR": jpg("render_exterior_sur.png", 1400, 82), "R_SALON": jpg("render_salon_interior.png", 1400, 82),
         "R_PB": jpg("render_planta_baja_abierta.png", 1400, 82), "R_COCINA": jpg("render_sala_a_cocina.png", 1400, 82), "R_ESC": jpg("render_entrada_escalera.png", 1400, 82),
         "PLANTAS": jpg("distribucion.png", 1800, 85), "SUITE": jpg("suite.png", 900, 85), "INST": jpg("instalaciones.png", 2000, 85), "CUB": jpg("cubierta_solar.png", 800, 85),
         "GLB": base64.b64encode(open("casa_v8.glb", "rb").read()).decode()}
t = open("visor_tpl.html", encoding="utf-8").read()
for k, v in datos.items(): t = t.replace("{{" + k + "}}", v)
assert "{{" not in t, "quedan marcas sin sustituir"
open(OUT, "w", encoding="utf-8").write(t); print(OUT, round(len(t) / 1e6, 2), "MB")
