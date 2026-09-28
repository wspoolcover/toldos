"""Plantas y secciones DXF (mm) cortando los sólidos de casa.py."""
import ezdxf, cadquery as cq
import casa as c

CAPAS = {"cimentacion": 8, "muros_PB": 7, "muros_PA": 7, "MURO_CENTRAL": 1, "tabiques": 3,
         "forjado_PB_PA": 5, "escalera": 30, "losa_terraza": 5, "pilares": 4, "antepecho": 7,
         "forjado_cubierta": 5, "cubierta": 6}

def contornos(solid, eje, valor):
    """Devuelve lista de polilíneas (en m) del corte. eje 'z' -> planta; 'y'/'x' -> sección."""
    s = solid
    if eje == "y":   s = s.rotate((0, 0, 0), (1, 0, 0), 90)   # z' = y ; dibuja (x, -y')
    elif eje == "x": s = s.rotate((0, 0, 0), (0, 1, 0), -90)  # z' = x ; dibuja (-x', y)
    try:
        cara = cq.Workplane("XY").add(s).section(valor).vals()
    except Exception:
        return []
    out = []
    for f in cara:
        for e in f.Edges():
            pts = [(p.x, p.y) for p in e.sample(0.0)] if False else [(v.x, v.y) for v in (e.positionAt(t) for t in ([0, 1] if e.geomType() == "LINE" else [i / 16 for i in range(17)]))]
            out.append(pts)
    return out

def dibujar(nombre, eje, valor, titulo, ejes_tf):
    doc = ezdxf.new("R2010", setup=True); doc.units = ezdxf.units.MM
    msp = doc.modelspace()
    for n, col in CAPAS.items():
        doc.layers.add(n, color=col)
    doc.layers.add("TEXTO", color=2)
    xs, ys = [], []
    for n, sol, _ in c.partes:
        for pl in contornos(sol.val(), eje, valor):
            pl = [ejes_tf(p) for p in pl]
            pl = [(x * 1000, y * 1000) for x, y in pl]
            msp.add_lwpolyline(pl, dxfattribs={"layer": n})
            xs += [p[0] for p in pl]; ys += [p[1] for p in pl]
    if xs:
        x0, x1, y0 = min(xs), max(xs), min(ys)
        msp.add_text(titulo, height=200, dxfattribs={"layer": "TEXTO", "insert": (x0, y0 - 800)})
        msp.add_linear_dim(base=(x0, y0 - 400), p1=(x0, y0), p2=(x1, y0), dimstyle="EZDXF").render()
    doc.saveas(nombre)
    print(nombre, len(xs) // 2 if xs else 0)

zpb, zpa = 1.20, c.Z_PA + 1.20
dibujar("planta_baja.dxf", "z", zpb, "PLANTA BAJA (corte a 1.20 m)  esc. 1/50", lambda p: p)
dibujar("planta_alta.dxf", "z", zpa, f"PLANTA ALTA (corte a {zpa:.2f} m)  esc. 1/50", lambda p: p)
# sección transversal X-X' (plano x = 4.45, pasa por hueco central) y longitudinal por el muro central
dibujar("seccion_transversal.dxf", "x", 4.45, "SECCION TRANSVERSAL x=4.45 m  esc. 1/50", lambda p: (p[1], -p[0]))
dibujar("seccion_longitudinal_muro_central.dxf", "y", c.Y_CEN + c.T_CEN / 2, "SECCION LONGITUDINAL por muro central  esc. 1/50", lambda p: (p[0], -p[1]))
