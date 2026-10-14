"""Descarga muebles y objetos libres (licencia CC0) de Poly Haven (polyhaven.com) en glTF de 1k a assets/poly_haven/<nombre>/.
Uso: python descargar_muebles.py [nombre ...]   (sin argumentos: la lista MUEBLES). Los archivos no se suben al repositorio (ver .gitignore); este script los vuelve a bajar."""
import json, os, subprocess, sys

UA = "cortijo-design/1.0"
MUEBLES = {
    # asientos
    "sofa_02": "sofá de piel/tela", "sofa_03": "sofá clásico", "painted_wooden_sofa": "sofá-banco de madera pintada", "painted_wooden_bench": "banco de madera pintada",
    "painted_wooden_chair_01": "silla de cocina", "painted_wooden_chair_02": "silla rústica", "wooden_stool_02": "taburete", "modern_arm_chair_01": "sillón de lectura",
    "mid_century_lounge_chair": "butaca", "vintage_day_bed": "diván", "Ottoman_01": "puf",
    # mesas y almacenaje
    "painted_wooden_table": "mesa de cocina", "wooden_table_02": "mesa rural", "round_wooden_table_01": "mesa redonda", "coffee_table_round_01": "mesa de centro redonda",
    "painted_wooden_nightstand": "mesilla", "side_table_01": "mesa auxiliar", "painted_wooden_cabinet": "aparador", "vintage_cabinet_01": "alacena", "painted_wooden_shelves": "estantería",
    "wooden_bookshelf_worn": "librería", "drawer_cabinet": "cómoda", "GothicBed_01": "cama de madera tallada", "old_bed_frame": "cama de hierro",
    # cocina y decoración
    "electric_stove": "cocina", "brass_pot_01": "olla de latón", "pot_enamel_01": "olla esmaltada", "jug_01": "jarra", "wicker_basket_01": "cesta", "wooden_bowl_01": "frutero",
    "throw_pillows_01": "cojines", "potted_plant_01": "planta", "potted_plant_04": "suculenta", "ceramic_vase_02": "jarrón", "lantern_chandelier_01": "lámpara de techo",
    "ceiling_fan": "ventilador de techo", "ornate_mirror_01": "espejo", "Shelf_01": "estante",
}

def curl_json(url):
    return json.loads(subprocess.run(["curl", "-sS", "-m", "60", "-A", UA, url], capture_output=True, check=True).stdout)

def bajar(nombre, dest="assets/poly_haven"):
    d = f"{dest}/{nombre}"
    if os.path.exists(f"{d}/{nombre}_1k.gltf"): return "ya estaba"
    info = curl_json(f"https://api.polyhaven.com/files/{nombre}")["gltf"]["1k"]["gltf"]
    os.makedirs(d, exist_ok=True)
    items = [(info["url"], f"{nombre}_1k.gltf")] + [(v["url"], rel) for rel, v in info["include"].items()]
    for url, rel in items:
        ruta = f"{d}/{rel}"; os.makedirs(os.path.dirname(ruta), exist_ok=True)
        subprocess.run(["curl", "-sS", "-m", "120", "-A", UA, "-o", ruta, url], check=True)
    return "ok"

if __name__ == "__main__":
    for n in (sys.argv[1:] or MUEBLES):
        try: print(f"{n:28s} {bajar(n)}")
        except Exception as e: print(f"{n:28s} FALLO {e}")
