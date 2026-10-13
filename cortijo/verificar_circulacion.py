"""Comprueba sobre el GLB (casa_v8) que se puede ir de una estancia a otra sin atravesar muros, escalera ni muebles:
cortes horizontales entre 0,30 y 2,00 m sobre cada planta, espacio libre = interior - obstáculos, y un 'cuerpo' de 0,70 m de ancho (radio 0,35) que debe poder pasar."""
import sys, numpy as np, trimesh
from shapely.geometry import Polygon, Point, box as sbox, MultiPolygon
from shapely.ops import unary_union
import casa_v8 as h

GLB = sys.argv[1] if len(sys.argv) > 1 else "casa_v8.glb"
sc = trimesh.load(GLB)
def corte(nombres, z):
    """Contornos del corte horizontal a cota z de cada pieza. El GLB va en float32 y parte cada sólido en caras sueltas (nombre, nombre_1, ...):
    se juntan los segmentos de todas las caras de la pieza, se redondean al milímetro y se cierran los contornos."""
    import re
    from trimesh.intersections import mesh_plane
    from shapely.geometry import LineString
    from shapely.ops import polygonize
    polys = []
    for n in nombres:
        segs = []
        for gn, g in sc.geometry.items():
            if not re.fullmatch(re.escape(n) + r"(_\d+)?", gn): continue
            seg = mesh_plane(g, [0, 0, 1], [0, 0, z])
            segs += [LineString(np.round(s_[:, :2], 3)) for s_ in seg if np.linalg.norm(s_[0, :2] - s_[1, :2]) > 1e-6]
        if not segs: continue
        polys += [p for p in polygonize(unary_union(segs)) if p.area > 1e-6]
    return polys

def libre(planta):
    z0 = 0.0 if planta == "PB" else h.Z_PA                                  # se cuenta como obstáculo todo lo macizo entre 0,30 m y 2,00 m sobre el suelo (peldaños incluidos)
    nombres = (["muros_PB", "muros_salon", "tabiques_PB", "murete_pasillo", "escalera", "mobiliario", "chimenea", "acero_pilares"] if planta == "PB"
               else ["muros_PA", "tabiques_PA", "mobiliario", "acero_pilares", "cristal_PA", "carpinteria_terraza"])
    obst = unary_union([p for dz in (0.30, 0.65, 1.00, 1.35, 1.70, 2.00) for p in corte(nombres, z0 + dz)])
    if planta == "PA":
        for (x0, y0, x1, y1) in h.HUECO_BOXES: obst = obst.union(sbox(x0, y0, x1, y1))
        ext = Polygon(h.NB_PA).union(Polygon(h.SB)); obst = obst.union(sbox(-5, -5, 20, 20).difference(ext))
    else:
        ext = Polygon(h.NB_FULL).union(Polygon(h.SB)); obst = obst.union(sbox(-5, -5, 20, 20).difference(ext))
    return sbox(-5, -5, 20, 20).difference(obst)

ESTANCIAS = {"PB": ["Salón con comedor", "Pasillo entrada", "Entrada", "Sala de estar y paso", "Cocina", "Dormitorio 2", "Baño grande", "Despacho", "Vestidor", "Baño principal", "Dormitorio principal"],
             "PA": ["Entrada", "Sala familiar", "Baño", "Dormitorio 1", "Dormitorio 2", "Dormitorio 3 / despacho", "Terraza sobre salón"]}
ok = True
for pl in ("PB", "PA"):
    L = libre(pl)
    for radio in (0.35, 0.40):
        R = L.buffer(-radio)                                    # sitio por donde puede pasar el centro del cuerpo
        comps = list(R.geoms) if isinstance(R, MultiPolygon) else [R]
        grupos = {}
        for nombre in ESTANCIAS[pl]:
            rects = [r for (p, n, rs) in h.ROOMS if p == pl and n == nombre for r in rs]
            area_est = unary_union([sbox(*r) for r in rects])
            # mejor trozo de la estancia: el de mayor superficie libre dentro de ella
            cand = [(c.intersection(area_est).area, i) for i, c in enumerate(comps) if c.intersection(area_est).area > 0.02]
            if not cand: grupos.setdefault("sin sitio para pasar", []).append(nombre); continue
            grupos.setdefault(max(cand)[1], []).append(nombre)
        print(f"\n{pl}  cuerpo de {2*radio:.2f} m:")
        for i, ks in grupos.items(): print("   ", f"zona {i}:" if not isinstance(i, str) else i.upper() + ":", ", ".join(ks))
        zonas = [i for i in grupos if not isinstance(i, str)]
        if radio == 0.35 and (len(zonas) > 1 or "sin sitio para pasar" in grupos): ok = False
print("\nRESULTADO:", "todo conectado con 0,70 m de paso" if ok else "HAY ESTANCIAS INCOMUNICADAS")

# altura libre bajo la escalera (tramo de vuelta: losa de 22 cm)
print("\naltura libre bajo el tramo de vuelta (m) según y:")
for j in range(7):
    y = h.Y0_ESC + 8 * h.TREAD - (j + 1) * h.TREAD; top = (10 + j) * h.RISE
    print(f"   y {y:5.2f}-{y + h.TREAD:5.2f}: {top - 0.22:4.2f}", "← paso libre ≥ 2,05" if top - 0.22 >= 2.05 else "← armario / sin paso")
