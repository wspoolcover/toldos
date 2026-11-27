"""Planta alta sobre la distribución deseada (27-11-2026): 3 dormitorios, 2 baños, salida a la terraza sobre el salón.
Los tabiques de arriba van sobre los tabiques de abajo. Comprueba qué hay debajo de cada pared de la planta alta.
Genera: planta_alta_27nov.png, dos_plantas_3d.png, dos_plantas.step/.glb, planta_alta.dxf y tabla_apoyo.md (se pega en el doc 24).
Esquema, no al milímetro. Cálculo de estructura: lo hace el técnico."""
import sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle
from shapely.geometry import LineString, Point, box
from shapely.ops import unary_union
import distribucion_deseada as DD
import plano_realidad as PR

HPA = 2.70                      # altura libre de planta alta (PL-11)
ZF = 3.30                       # cota del suelo de la planta alta (forjado 25+5 cm sobre 3,0 m)
XP, XPN, X2, Y3, Y4, YN = DD.XP, DD.XPN, DD.X2, DD.Y3, DD.Y4, DD.YN
HUECO_ESC = (XPN + .035, 4.40, XPN + .035 + 0.955, 7.30)   # hueco de la escalera en el forjado

# ----------------------------------------------------------------- paredes de la planta alta (centro, espesor)
PA_EXT = [("Sur", [(0, 0), (9.20, 0)], .14), ("Oeste", [(0, 0), (0, 8.80)], .14), ("Este, tramo sur", [(9.21, 0), (9.21, 4.20)], .14),
          ("Este, tramo del saliente", [(9.27, 4.20), (9.27, 7.20)], .14), ("Este, tramo norte", [(9.27, 7.20), (9.27, 8.90)], .29),
          ("Norte, hasta x = 7,30", [(0, YN), (7.30, YN)], .29), ("Norte, balconera", [(7.30, YN), (9.27, YN)], .14),
          ("Central E-O", [(0, 4.20), (9.27, 4.20)], .14)]
PA_INT = [("T1 x = 4,40 (dormitorio 1 | dormitorio 2)", [(XP, 0.07), (XP, 4.055)], "NS"),
          ("T2 x = 3,10 (baños | dormitorio 3 y pasillo)", [(X2, 4.345), (X2, 8.675)], "NS"),
          ("T3 y = 5,485 (pasillo | dormitorio 3)", [(X2 + .035, Y3), (XPN - .035, Y3)], "EO"),
          ("T4 y = 6,335 (baño 1 | baño 2)", [(0.07, Y4), (X2 - .035, Y4)], "EO"),
          ("T5 x = 5,40 (dormitorio 3, este)", [(XPN, 5.52), (XPN, 8.675)], "NS")]
# huecos: (nombre, tipo, orientación, coord. fija, centro, ancho, z0, z1) — z relativa al suelo de la planta alta
HUECOS_PA = [("Va1", "ventana", "h", 0.0, 1.90, 1.30, 1.00, 2.20), ("Va2", "ventana", "h", 0.0, 5.90, 1.30, 1.00, 2.20),
             ("Va3", "ventana", "h", 0.0, 8.50, 1.10, 1.00, 2.20),
             ("Va4", "ventana", "h", YN, 4.25, 1.30, 1.00, 2.20), ("Va5", "ventana", "h", YN, 1.50, 0.60, 1.40, 2.20),
             ("Va6", "ventana", "h", YN, 5.90, 0.80, 1.00, 2.20), ("Bal", "puerta", "h", YN, 8.25, 1.60, 0, 2.20),
             ("Pa1", "puerta", "h", 4.20, 2.05, 0.80, 0, 2.05), ("Pa2", "puerta", "h", 4.20, 3.80, 0.80, 0, 2.05),
             ("Pa3", "puerta", "h", 4.20, 4.95, 0.80, 0, 2.05),
             ("Pa4", "puerta", "v", X2, 4.90, 0.80, 0, 2.05), ("Pa5", "puerta", "v", X2, 6.90, 0.80, 0, 2.05),
             ("Pa6", "puerta", "h", Y3, 4.60, 0.80, 0, 2.05)]
DD.ABRE.update({"Pa1": ("hi", (0, -1)), "Pa2": ("lo", (0, -1)), "Pa3": ("hi", (0, -1)), "Pa4": ("lo", (-1, 0)),
                "Pa5": ("hi", (1, 0)), "Pa6": ("hi", (0, 1)), "Bal": ("dbl", (0, 1))})

# estancias (caras interiores)
SA = [("Dormitorio 1", 0.07, 0.07, XP - .035, 4.055), ("Dormitorio 2", XP + .035, 0.07, 9.14, 4.055),
      ("Baño 1", 0.07, 4.345, X2 - .035, Y4 - .035), ("Baño 2", 0.07, Y4 + .035, X2 - .035, 8.675),
      ("Dormitorio 3", X2 + .035, Y3 + .035, XPN - .035, 8.675), ("Pasillo", X2 + .035, 4.345, XPN - .035, Y3 - .035)]
SALA = [(6.39, 4.345, 9.20, 8.675), (XPN + .035, 7.30, 6.39, 8.675)]            # sala de estar con salida a la terraza
AREAS = {n: (x1 - x0) * (y1 - y0) for n, x0, y0, x1, y1 in SA}
AREAS["Sala de estar (sale a la terraza)"] = sum((b[2] - b[0]) * (b[3] - b[1]) for b in SALA)
TERRAZA = (3.115, 8.965, 9.125, 15.405)
AREAS["Terraza sobre el salón"] = (TERRAZA[2] - TERRAZA[0]) * (TERRAZA[3] - TERRAZA[1])
AREAS["Hueco de la escalera (no cuenta)"] = (HUECO_ESC[2] - HUECO_ESC[0]) * (HUECO_ESC[3] - HUECO_ESC[1])
BARANDILLAS = [((6.39, 5.45), (6.39, 7.30)), ((XPN + .035, 7.30), (6.39, 7.30))]

# mobiliario (nombre, x0, y0, x1, y1, alto, color)
MUEB = [("cama", 0.07, 1.00, 2.07, 2.80, .50, "#d7c7a8"), ("mesilla", 0.07, 0.55, 0.52, 1.00, .50, "#c9b48f"), ("mesilla", 0.07, 2.80, 0.52, 3.25, .50, "#c9b48f"),
        ("armario", 3.915, 0.45, 4.365, 2.65, 2.40, "#c9b48f"),
        ("cama", 7.14, 1.10, 9.14, 2.90, .50, "#d7c7a8"), ("mesilla", 8.69, 0.65, 9.14, 1.10, .50, "#c9b48f"), ("mesilla", 8.69, 2.90, 9.14, 3.35, .50, "#c9b48f"),
        ("armario", 4.435, 0.50, 4.885, 3.00, 2.40, "#c9b48f"),
        ("cama", 4.00, 6.675, 5.365, 8.675, .50, "#d7c7a8"), ("armario", 3.135, 5.52, 4.00, 5.97, 2.40, "#c9b48f"),
        ("ducha", 0.07, 4.345, 0.97, 5.845, .05, "#90caf9"), ("lavabo", 1.00, 4.345, 1.60, 4.80, .85, "#eeeeee"), ("inodoro", 1.50, 5.85, 1.90, 6.30, .40, "#eeeeee"),
        ("ducha", 0.07, 7.175, 0.97, 8.675, .05, "#90caf9"), ("inodoro", 1.20, 8.20, 1.58, 8.675, .40, "#eeeeee"), ("lavabo", X2 - .035 - .50, 7.45, X2 - .035, 8.55, .85, "#eeeeee"),
        ("TV", 7.00, 4.345, 8.60, 4.75, .50, "#c9a46b"), ("sofá", 7.00, 6.10, 8.80, 6.95, .85, "#a1887f"), ("mesa de centro", 7.50, 5.30, 8.30, 5.80, .40, "#c9a46b")]
MUEB_T = [("mesa", 6.00, 12.00, 7.60, 12.90, .75, "#bcaaa4")] + [("silla", 6.10 + .45 * i, y0, 6.10 + .45 * i + .38, y0 + .38, .45, "#a1887f") for i in range(3) for y0 in (11.55, 12.95)] \
         + [("tumbona", 3.60, 10.00, 4.30, 11.90, .35, "#c5e1a5"), ("tumbona", 4.50, 10.00, 5.20, 11.90, .35, "#c5e1a5")]


# ----------------------------------------------------------------- comprobación: qué hay debajo de cada pared
def apoyo():
    m14c, m29c, t7c = DD.geometria(True)
    m14f, m29f, t7f = DD.geometria(False)
    muro = unary_union([m14c, m29c]); tab = t7c; todo = unary_union([m14f, m29f, t7f])
    filas = []
    paredes = [(n, p, e, "ext", None) for n, p, e in PA_EXT] + [(n, p, .07, "int", o) for n, p, o in PA_INT]
    for n, p, e, k, o in paredes:
        ls = LineString(p); L = ls.length; N = max(int(L / 0.05), 2)
        c = {"muro": 0, "tabique": 0, "hueco": 0, "vacío": 0}
        for i in range(N):
            pt = ls.interpolate((i + .5) / N, normalized=True)
            if muro.contains(pt): c["muro"] += 1
            elif tab.contains(pt): c["tabique"] += 1
            elif todo.contains(pt): c["hueco"] += 1
            else: c["vacío"] += 1
        pc = {a: 100 * b / N for a, b in c.items()}
        if o is None: o = "NS" if abs(p[0][0] - p[1][0]) < abs(p[0][1] - p[1][1]) else "EO"
        if pc["vacío"] >= 20: est = "✗ sin apoyo: jácena (viga) debajo"
        elif k == "ext" and pc["tabique"] >= 20: est = "⚠ sobre tabique de 7 cm: jácena o muro debajo"
        elif k == "int" and pc["muro"] + pc["tabique"] + pc["hueco"] >= 90: est = "✓ tabique sobre tabique" + ("; vigueta doble (las viguetas van N-S)" if o == "NS" else "")
        elif pc["hueco"] >= 5: est = "✓ con dintel en el hueco de abajo"
        else: est = "✓ sobre muro"
        filas.append(dict(nombre=n, L=L, e=e, k=k, o=o, esb=HPA / e, **pc, estado=est))
    return filas


def tabla_md(filas):
    s = "| Pared de la planta alta | Largo (m) | Espesor | Esbeltez h/e | Debajo: muro | tabique | hueco | vacío | Resultado |\n|---|---|---|---|---|---|---|---|---|\n"
    for f in filas:
        s += (f"| {f['nombre']} | {f['L']:.2f} | {int(round(f['e'] * 100))} cm | {f['esb']:.0f} | {f['muro']:.0f} % | {f['tabique']:.0f} % | "
              f"{f['hueco']:.0f} % | {f['vacío']:.0f} % | {f['estado']} |\n")
    return s


# ----------------------------------------------------------------- plano
def geometria_pa():
    m14 = unary_union([DD.banda(p, e) for n, p, e in PA_EXT if e == .14])
    m29 = unary_union([DD.banda(p, e) for n, p, e in PA_EXT if e == .29])
    t7 = unary_union([DD.banda(p, .07) for n, p, o in PA_INT])
    cuts = unary_union([DD.hueco_box(h) for h in HUECOS_PA])
    return m14.difference(cuts), m29.difference(cuts), t7.difference(cuts)


def dibujo(filas):
    m14, m29, t7 = geometria_pa()
    pb14, pb29, pbt = DD.geometria()
    fig, ax = plt.subplots(figsize=(11.5, 13.5))
    ax.set_xlim(-1.2, 13.0); ax.set_ylim(17.7, -2.4); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Planta alta (3 dormitorios, 2 baños, salida a la terraza) sobre la planta baja — esquema, no al milímetro", fontsize=11.5, weight="bold", loc="left")
    # terraza sobre el salón
    t = TERRAZA
    ax.add_patch(Rectangle((t[0], t[1]), t[2] - t[0], t[3] - t[1], fc="#e3efd6", ec="none", zorder=0))
    for n, x0, y0, x1, y1 in SA: ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#fffdf5", ec="none", zorder=0))
    for b in SALA: ax.add_patch(Rectangle((b[0], b[1]), b[2] - b[0], b[3] - b[1], fc="#fffdf5", ec="none", zorder=0))
    # planta baja de referencia (muros y tabiques de abajo, en gris)
    DD.pinta(ax, pb14.union(pb29), fc="#d9d9d9", ec="#bbbbbb", lw=.5, zorder=1, alpha=.55)
    DD.pinta(ax, pbt, fc="#cfcfcf", ec="#9e9e9e", lw=.5, zorder=1, alpha=.7)
    # paredes de arriba
    DD.pinta(ax, m14, fc="#e3edff", ec="#1a3fbf", hatch="////", lw=.8, zorder=3)
    DD.pinta(ax, m29, fc="#1a3fbf", ec="#1a3fbf", lw=.8, zorder=3)
    DD.pinta(ax, t7, fc="white", ec="#4f6fd8", lw=1.0, zorder=4)
    # antepecho de la terraza: muros del salón a +1,0 m
    for n, p, e in DD.EXIST + DD.PROP29:
        if n.startswith("salón"): DD.pinta(ax, DD.banda(p, e), fc="#7986cb", ec="#303f9f", lw=.8, zorder=2)
    # resultado de la comprobación sobre cada tabique
    col = {"✓": "#2e7d32", "⚠": "#ef6c00", "✗": "#c62828"}
    for f in filas:
        pass
    for (n, p, o), f in zip(PA_INT, [x for x in filas if x["k"] == "int"]):
        ax.add_patch(MPoly(list(DD.banda(p, .07).buffer(.03).exterior.coords), closed=True, fc="none", ec=col[f["estado"][0]], lw=1.2, zorder=5))
    for f, (n, p, e) in zip([x for x in filas if x["k"] == "ext"], PA_EXT):
        if f["estado"][0] != "✓": ax.plot(*zip(*p), color=col[f["estado"][0]], lw=2.2, ls=(0, (4, 3)), zorder=6)
    for n, x0, y0, x1, y1, h, c in MUEB: ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, ec="#555", lw=.5, zorder=5))
    for n, x0, y0, x1, y1, h, c in MUEB_T: ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=c, ec="#555", lw=.5, zorder=5))
    # hueco de la escalera
    h = HUECO_ESC
    ax.add_patch(Rectangle((h[0], h[1]), h[2] - h[0], h[3] - h[1], fc="#cfd8dc", ec="#37474f", hatch="xx", lw=1.0, zorder=4, alpha=.8))
    for a, b in BARANDILLAS: ax.plot([a[0], b[0]], [a[1], b[1]], color="#212121", lw=2.6, zorder=6)
    ax.text((h[0] + h[2]) / 2, 6.0, "escalera\n(baja)", ha="center", va="center", fontsize=7.5, color="#263238", zorder=7)
    ax.annotate("", xy=(h[0] - .45, 4.95), xytext=(h[0] + .2, 4.95), arrowprops=dict(arrowstyle="->", color="#37474f"), zorder=7)
    ax.annotate("", xy=(h[2] + .45, 4.95), xytext=(h[2] - .2, 4.95), arrowprops=dict(arrowstyle="->", color="#37474f"), zorder=7)
    ax.text((h[0] + h[2]) / 2, 5.25, "salidas", ha="center", fontsize=6.5, color="#37474f", zorder=7)
    for hh in HUECOS_PA: (DD.puerta if hh[1] == "puerta" else DD.ventana)(ax, hh)
    POS = {"Dormitorio 1": (2.7, 1.9, True), "Dormitorio 2": (6.1, 3.0, True), "Baño 1": (1.55, 5.1, False), "Baño 2": (1.9, 7.0, False),
           "Dormitorio 3": (3.55, 7.7, False), "Pasillo": (4.25, 4.9, False)}
    for n, x0, y0, x1, y1 in SA:
        px, py, dims = POS[n]; a = AREAS[n]
        txt = f"{n}\n{x1 - x0:.2f} × {y1 - y0:.2f} m\n{a:.1f} m²" if dims else f"{n}\n{a:.1f} m²"
        if n == "Dormitorio 3": txt = "Dorm. 3\n7,0 m²"
        if n == "Pasillo": txt = "pasillo\n(arriba de la escalera)"
        ax.text(px, py, txt, ha="center", va="center", fontsize=8.5 if dims else 7.6, weight="bold", color="#222", zorder=8)
    ax.text(7.8, 7.55, f"Sala de estar\n{AREAS['Sala de estar (sale a la terraza)']:.1f} m²\nsale a la terraza", ha="center", va="center", fontsize=8, weight="bold", zorder=8)
    ax.text(5.95, 15.0, f"TERRAZA sobre el salón\n{AREAS['Terraza sobre el salón']:.1f} m², antepecho de 1,0 m", ha="center", fontsize=9, weight="bold", color="#33691e", zorder=8, bbox=dict(fc="white", ec="none", alpha=.85, pad=2))
    ax.text(5.5, 9.45, "Bal", fontsize=1, alpha=0)
    for hh in HUECOS_PA:
        if hh[2] == "h" and hh[3] < 1: ax.text(hh[4], -0.55, hh[0], ha="center", fontsize=8, color="#1565c0", weight="bold")
    ax.text(-1.1, -1.7, "SUR ↑ (como en la planta baja)", fontsize=8, color="#555")
    ax.text(-1.1, 17.4, ("Gris: paredes y tabiques de la planta baja, debajo. Azul: paredes de arriba (hatch 14 cm, macizo 29 cm, fino 7 cm).\n"
                        "Contorno de los tabiques: verde = sobre otro tabique de abajo; naranja o rojo = sin apoyo directo. Línea discontinua naranja o roja en muros de fachada = sin muro debajo.\n"
                        "Las viguetas del forjado van N-S, perpendiculares al muro central (lámina PL-11): los tabiques N-S (x = 3,10; 4,40; 5,40) llevan vigueta doble."), fontsize=7.6, va="top", color="#222")
    fig.savefig("planta_alta_27nov.png", dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------- DXF
def dxf():
    import ezdxf
    m14, m29, t7 = geometria_pa()
    d = ezdxf.new("R2010"); msp = d.modelspace()
    for nom, col in [("PA_MUROS14", 5), ("PA_MUROS29", 1), ("PA_TABIQUES7", 4), ("PA_HUECOS", 6), ("PA_MOBILIARIO", 8), ("PA_TEXTO", 7), ("PA_ESCALERA", 3)]:
        d.layers.add(nom, color=col)
    def poli(g, layer):
        for p in DD.poligonos(g):
            for ring in [p.exterior] + list(p.interiors): msp.add_lwpolyline(list(ring.coords), close=True, dxfattribs={"layer": layer})
    poli(m14, "PA_MUROS14"); poli(m29, "PA_MUROS29"); poli(t7, "PA_TABIQUES7")
    for hh in HUECOS_PA: poli(DD.hueco_box(hh, .1), "PA_HUECOS")
    for n, x0, y0, x1, y1, h, c in MUEB + MUEB_T: msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "PA_MOBILIARIO"})
    h = HUECO_ESC; msp.add_lwpolyline([(h[0], h[1]), (h[2], h[1]), (h[2], h[3]), (h[0], h[3])], close=True, dxfattribs={"layer": "PA_ESCALERA"})
    for n, x0, y0, x1, y1 in SA:
        msp.add_text(f"{n} {AREAS[n]:.1f} m2", height=.18, dxfattribs={"layer": "PA_TEXTO"}).set_placement(((x0 + x1) / 2, (y0 + y1) / 2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    d.saveas("planta_alta.dxf")


# ----------------------------------------------------------------- 3D (planta baja + forjado + planta alta + terraza)
def modelo_dos_plantas(alto_pa=HPA):
    import cadquery as cq
    parts = dict(DD.modelo3d(DD.H))
    def extruye(g, z0, z1):
        res = None
        for p in DD.poligonos(g):
            s = cq.Workplane("XY").workplane(offset=z0).polyline(list(p.exterior.coords)[:-1]).close().extrude(z1 - z0)
            for r in p.interiors: s = s.cut(cq.Workplane("XY").workplane(offset=z0 - .1).polyline(list(r.coords)[:-1]).close().extrude(z1 - z0 + .2))
            res = s if res is None else res.union(s)
        return res
    def caja(x0, y0, x1, y1, z0, z1): return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
    losa = unary_union([box(-0.07, -0.07, 9.34, 8.97), box(2.825, 8.82, 9.415, 15.695)]).difference(box(*HUECO_ESC)).difference(box(*DD.CONDUCTO))
    parts["forjado"] = (extruye(losa, ZF - 0.30, ZF), (0.85, 0.85, 0.85))
    def muros(bandas, alto):
        s = extruye(unary_union(bandas), ZF, ZF + alto)
        for hh in HUECOS_PA:
            b = DD.hueco_box(hh, .6).bounds
            s = s.cut(caja(b[0], b[1], b[2], b[3], ZF + hh[6], ZF + hh[7]))
        return s
    parts["PA_muros_14cm"] = (muros([DD.banda(p, e) for n, p, e in PA_EXT if e == .14], alto_pa), (0.78, 0.82, 0.95))
    parts["PA_muros_29cm"] = (muros([DD.banda(p, e) for n, p, e in PA_EXT if e == .29], alto_pa), (0.30, 0.38, 0.75))
    parts["PA_tabiques_7cm"] = (muros([DD.banda(p, .07) for n, p, o in PA_INT], alto_pa), (0.95, 0.95, 0.95))
    par = [DD.banda(p, e) for n, p, e in DD.EXIST + DD.PROP29 if n.startswith("salón")]
    parts["antepecho_terraza"] = (extruye(unary_union(par), ZF, ZF + 1.0), (0.30, 0.38, 0.75))
    bar = None
    for a, b in BARANDILLAS:
        x0, x1 = sorted((a[0], b[0])); y0, y1 = sorted((a[1], b[1]))
        c = caja(x0 - .02, y0 - .02, x1 + .02, y1 + .02, ZF, ZF + 1.05); bar = c if bar is None else bar.union(c)
    parts["barandilla_escalera"] = (bar, (0.2, 0.2, 0.2))
    parts["chimenea_sube"] = (caja(*DD.CONDUCTO, DD.H, ZF + 3.0), (0.55, 0.42, 0.36))
    mue = None
    for n, x0, y0, x1, y1, h, c in MUEB:
        b = caja(x0, y0, x1, y1, ZF, ZF + h); mue = b if mue is None else mue.union(b)
    parts["PA_mobiliario"] = (mue, (0.72, 0.58, 0.40))
    ter = None
    for n, x0, y0, x1, y1, h, c in MUEB_T:
        b = caja(x0, y0, x1, y1, ZF, ZF + h); ter = b if ter is None else ter.union(b)
    parts["terraza_mobiliario"] = (ter, (0.55, 0.65, 0.45))
    return parts


def exporta3d():
    import cadquery as cq, trimesh
    parts = modelo_dos_plantas()
    asm = cq.Assembly(name="dos_plantas")
    for n, (s, col) in parts.items(): asm.add(s, name=n, color=cq.Color(*col))
    asm.save("dos_plantas.step")
    scene = trimesh.Scene()
    for n, (s, col) in parts.items():
        v, f = s.val().tessellate(0.005)
        m = trimesh.Trimesh([(p.x, p.y, p.z) for p in v], f)
        m.visual.face_colors = [int(c * 255) for c in col] + [255]
        scene.add_geometry(m, node_name=n)
    scene.export("dos_plantas.glb")


def render3d():
    import numpy as np
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    parts = modelo_dos_plantas(1.3)
    fig = plt.figure(figsize=(12, 10)); ax = fig.add_subplot(111, projection="3d"); ax.set_proj_type("ortho")
    ax.view_init(elev=48, azim=60)
    luz = np.array([-0.4, 0.5, 0.8]); luz /= np.linalg.norm(luz)
    T, C = [], []
    for n, (s, col) in parts.items():
        v, f = s.val().tessellate(0.02)
        V = np.array([(p.x, p.y, p.z) for p in v]); F = np.array(f)
        tri = V[F]; nor = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); ln = np.linalg.norm(nor, axis=1); ln[ln == 0] = 1
        nor = nor / ln[:, None]; sh = 0.55 + 0.45 * np.abs(nor @ luz)
        T.append(tri); C += [tuple(np.clip(np.array(col) * k, 0, 1)) + (1,) for k in sh]
    ax.add_collection3d(Poly3DCollection(np.concatenate(T), facecolors=C, edgecolors=(0, 0, 0, .10), linewidths=.2))
    ax.set_xlim(-1, 12.5); ax.set_ylim(-1, 16.5); ax.set_zlim(-0.5, 7)
    ax.set_box_aspect((13.5, 17.5, 7.5)); ax.axis("off")
    ax.set_title("Dos plantas: planta baja completa, forjado, planta alta cortada a 1,3 m y terraza sobre el salón (vista desde el norte)", fontsize=10, loc="left")
    fig.savefig("dos_plantas_3d.png", dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def resumen(filas):
    print("ÁREAS planta alta (m², caras interiores):")
    for n, a in AREAS.items(): print(f"  {n:38s} {a:6.2f}")
    util = sum(a for n, a in AREAS.items() if not n.startswith(("Terraza", "Hueco")))
    print(f"  {'Total útil planta alta (sin terraza ni hueco)':38s} {util:6.2f}")
    for f in filas: print(f"  {f['nombre'][:44]:44s} L={f['L']:5.2f} muro {f['muro']:3.0f} tab {f['tabique']:3.0f} hueco {f['hueco']:3.0f} vacío {f['vacío']:3.0f}  {f['estado']}")


if __name__ == "__main__":
    filas = apoyo()
    resumen(filas)
    open("tabla_apoyo.md", "w").write(tabla_md(filas))
    dibujo(filas)
    dxf()
    if "--sin3d" not in sys.argv:
        exporta3d(); render3d()
