"""Distribución deseada por el propietario (croquis del 27-11-2026) sobre la obra real: muros de 14/29 cm, tabiques de 7 cm,
puertas, ventanas, escalera y mobiliario. Genera:
  distribucion_deseada_27nov.png   plano (sur arriba, como en el croquis)
  distribucion_deseada_3d.png      maqueta seccionada a 1,5 m
  distribucion_deseada.step/.glb   modelo 3D (STEP se abre en FreeCAD)
  distribucion_deseada.dxf         plano 2D por capas
Esquema con las cifras del croquis: no es al milímetro. Las posiciones de los tabiques son de diseño, no de obra."""
import math
import sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle, PathPatch
from matplotlib.path import Path
from shapely.geometry import LineString, box, Polygon, MultiPolygon
from shapely.ops import unary_union
import plano_realidad as PR

H = 3.0                 # altura de muros y tabiques de planta baja (libre 3,01 m en PL-11)
XP = PR.XM              # tabique N-S de la suite/cocina y de la oficina, sobre el zuncho central N-S (x ≈ 4,40 m, aproximada)
XPN = 5.40              # en la mitad norte el tabique de la oficina y la escalera van 1 m más al este (decisión del propietario)
X2 = 3.10               # tabique N-S entre vestidor/baño y oficina
Y3, Y4 = 5.485, 6.335   # tabique S de la oficina y tabique vestidor | baño
X6 = 9.27               # tabique del baño grande (saliente)
YN = 8.82               # línea norte del bloque
XN = 7.30               # el muro norte llega hasta aquí; de ahí al este queda el paso al salón
YC = PR.YC

# ----------------------------------------------------------------- muros
EXIST = [m for m in PR.MUROS if m[0] != "norte, al oeste del salón"]
EXIST += [("norte, al oeste del salón", [(0, 8.80), (2.97, YN)], 0.29)]
PROP29 = [("norte del bloque (propuesto)", [(2.97, YN), (XN, YN)], 0.29),
          ("salón, norte (supuesto)", [(2.97, 15.55), (9.27, 15.55)], 0.29)]
TAB = [("T1 suite | cocina", [(XP, 0.07), (XP, 4.055)]),
       ("T5 oficina, este", [(XPN, 5.52), (XPN, 8.675)]),
       ("T2 vestidor-baño | oficina", [(X2, 4.345), (X2, 8.675)]),
       ("T3 oficina, sur", [(X2 + .035, Y3), (XPN - .035, Y3)]),
       ("T4 vestidor | baño", [(0.07, Y4), (X2 - .035, Y4)]),
       ("T6 baño grande", [(X6, 4.345), (X6, 7.055)]),
       ("T7 cierre del pasillo", [(4.20, 4.345), (4.20, Y3 - .035)])]

# huecos: (nombre, tipo, orientación del muro, coordenada fija, centro, ancho, z0, z1)
HUECOS = [("V2", "ventana", "h", 0.0, 1.90, 1.30, 1.00, 2.20), ("V1", "ventana", "h", 0.0, 5.90, 1.30, 1.00, 2.20),
          ("P1", "puerta", "h", 0.0, 8.50, 1.10, 0, 2.10),
          ("D1", "puerta", "h", YC, 3.75, 0.90, 0, 2.05), ("D2", "puerta", "v", X2, 4.90, 0.80, 0, 2.05), ("D8", "puerta", "v", 4.20, 4.8975, 1.00, 0, 2.05), ("D5", "puerta", "h", YC, 8.625, 0.85, 0, 2.05),
          ("D7", "puerta", "h", YC, 2.05, 0.80, 0, 2.05), ("D3", "puerta", "h", Y3, 3.70, 0.80, 0, 2.05),
          ("D4", "puerta", "h", Y4, 2.05, 0.80, 0, 2.05), ("D6", "puerta", "v", X6, 6.55, 0.80, 0, 2.05),
          ("PE", "puerta", "h", 15.55, 8.55, 1.00, 0, 2.10)]
# puertas: nombre -> (bisagra 'lo'|'hi', hacia dónde abre (dx, dy), hoja doble)
ABRE = {"D1": ("hi", (0, -1)), "D2": ("hi", (-1, 0)), "D8": ("lo", (1, 0)), "D5": ("hi", (0, 1)), "D7": ("slide_lo", (0, -1)), "D3": ("lo", (0, 1)), "D4": ("hi", (0, -1)),
        "D6": ("hi", (1, 0)), "PE": ("lo", (0, -1)), "P1": ("dbl", (0, 1))}


def hueco_box(h, grosor=0.6):
    n, t, o, f, c, w, z0, z1 = h
    return box(c - w / 2, f - grosor / 2, c + w / 2, f + grosor / 2) if o == "h" else box(f - grosor / 2, c - w / 2, f + grosor / 2, c + w / 2)


def banda(pts, esp):
    return LineString(pts).buffer(esp / 2, cap_style=2, join_style=2)


def poligonos(g):
    return [g] if isinstance(g, Polygon) else list(g.geoms) if isinstance(g, MultiPolygon) else []


# ----------------------------------------------------------------- estancias (caras interiores)
S = [("Dormitorio suite", 0.07, 0.07, XP - .035, 4.055), ("Cocina", XP + .035, 0.07, 9.14, 4.055),
     ("Vestidor", 0.07, 4.345, X2 - .035, Y4 - .035), ("Baño suite", 0.07, Y4 + .035, X2 - .035, 8.675),
     ("Oficina", X2 + .035, Y3 + .035, XPN - .035, 8.675), ("Baño grande", X6 + .035, 4.345, 11.48, 7.055),
     ("Salón", 3.115, 8.965, 9.125, 15.405)]
ESC = (XPN + .035, 4.40, XPN + .035 + 0.955, 8.675)              # escalera: tramo recto + descansillo
ESC_IZQ = (XPN + .035 + 0.955, 7.72, XPN + .035 + 0.955 + 0.765, 8.675)   # 3 peldaños de arranque hacia el este
AREA_ESC = (ESC[2] - ESC[0]) * (ESC[3] - ESC[1]) + (ESC_IZQ[2] - ESC_IZQ[0]) * (ESC_IZQ[3] - ESC_IZQ[1])
PASILLO = (X2 + .035, 4.345, XPN + .035 + 0.955, 5.45)         # pasillo hacia suite, vestidor, oficina; bajo la escalera
DISTR = (XPN + .035 + 0.955, 4.345, X6 - .035, 8.675)
AREA_DISTR = (DISTR[2] - DISTR[0]) * (DISTR[3] - DISTR[1]) - (ESC_IZQ[2] - ESC_IZQ[0]) * (ESC_IZQ[3] - ESC_IZQ[1])
AREAS = {n: (x1 - x0) * (y1 - y0) for n, x0, y0, x1, y1 in S}
AREAS["Pasillo (bajo la escalera)"] = (PASILLO[2] - PASILLO[0]) * (PASILLO[3] - PASILLO[1])
AREAS["Escalera"] = AREA_ESC
AREAS["Comedor / distribuidor"] = AREA_DISTR

# ----------------------------------------------------------------- mobiliario (nombre, x0, y0, x1, y1, alto, color)
MUEBLES = [
    ("cama 1,80×2,00", 0.07, 1.00, 2.07, 2.80, 0.50, "#d7c7a8"), ("mesilla", 0.07, 0.55, 0.52, 1.00, 0.50, "#c9b48f"),
    ("mesilla", 0.07, 2.80, 0.52, 3.25, 0.50, "#c9b48f"),
    ("encimera", XP + .035, 1.40, XP + .035 + 0.60, 3.455, 0.90, "#bdbdbd"), ("encimera", XP + .035, 3.455, 7.30, 4.055, 0.90, "#bdbdbd"),
    ("columna nevera", 7.30, 3.40, 7.90, 4.055, 2.00, "#9e9e9e"), ("barra bajo V1", 5.25, 0.07, 6.85, 0.57, 0.95, "#c9a46b"),
    ("armario", 0.07, 4.345, 0.62, 6.265, 2.40, "#c9b48f"), ("armario", 0.62, 4.345, 1.65, 4.895, 2.40, "#c9b48f"), ("armario", X2 - .035 - 0.50, 5.45, X2 - .035, 6.265, 2.40, "#c9b48f"),
    ("ducha", 0.07, 7.175, 0.97, 8.675, 0.05, "#90caf9"), ("inodoro", 1.20, 8.20, 1.58, 8.675, 0.40, "#eeeeee"),
    ("lavabo", X2 - .035 - 0.50, 6.65, X2 - .035, 8.05, 0.85, "#eeeeee"),
    ("escritorio", 3.50, 8.025, 4.90, 8.675, 0.75, "#c9a46b"), ("estantería", XPN - .035 - 0.30, 6.00, XPN - .035, 7.80, 1.80, "#c9b48f"),
    ("ducha", 10.58, 4.345, 11.48, 5.745, 0.05, "#90caf9"), ("inodoro", 9.70, 4.345, 10.10, 5.045, 0.40, "#eeeeee"),
    ("lavabo doble", 10.98, 5.90, 11.48, 7.055, 0.85, "#eeeeee"),
    ("mueble TV", 3.115, 11.00, 3.615, 12.90, 0.50, "#c9a46b"),
    ("sofá en C", 6.80, 10.40, 7.40, 13.60, 0.85, "#a1887f"), ("sofá en C", 5.60, 10.40, 6.80, 11.20, 0.85, "#a1887f"),
    ("sofá en C", 5.60, 12.80, 6.80, 13.60, 0.85, "#a1887f"), ("mesa de centro", 5.80, 11.55, 6.50, 12.45, 0.40, "#c9a46b"),
    ("mueble de entrada", 7.70, 10.60, 7.85, 15.20, 1.00, "#c9b48f"),
    ("mesa comedor", 6.75, 5.95, 8.35, 6.85, 0.75, "#c9a46b")] + [("silla", 6.65 + .70 * i, y0, 6.65 + .70 * i + .40, y0 + .40, 0.45, "#b08d57") for i in range(3) for y0 in (5.50, 6.95)]
CHIMENEA = [(3.115, 8.965), (4.30, 8.965), (3.115, 10.15)]
CONDUCTO = (3.115, 8.965, 3.565, 9.415)
TABURETES = [(5.45 + .55 * i, 0.95) for i in range(3)]


# ----------------------------------------------------------------- geometría 2D común
def geometria(cortar=True):
    m14 = unary_union([banda(p, e) for n, p, e in EXIST if e == 0.14])
    m29 = unary_union([banda(p, e) for n, p, e in EXIST + PROP29 if e == 0.29])
    t7 = unary_union([banda(p, .07) for n, p in TAB])
    cuts = unary_union([hueco_box(h) for h in HUECOS]) if cortar else Polygon()
    return m14.difference(cuts), m29.difference(cuts), t7.difference(cuts)


def path_de(g):
    verts, codes = [], []
    for p in poligonos(g):
        for ring in [p.exterior] + list(p.interiors):
            c = list(ring.coords)
            verts += c; codes += [Path.MOVETO] + [Path.LINETO] * (len(c) - 2) + [Path.CLOSEPOLY]
    return Path(verts, codes)


def pinta(ax, g, **kw):
    if not g.is_empty: ax.add_patch(PathPatch(path_de(g), **kw))


def puerta(ax, h):
    n, t, o, f, c, w, z0, z1 = h
    lo, hi = c - w / 2, c + w / 2
    def p(a, b): return (a, f) if o == "h" else (f, a)
    def hoja(hinge, jamb, d, ww):
        hx, hy = hinge; jx, jy = jamb
        tip = (hx + d[0] * ww, hy + d[1] * ww)
        a0, a1 = math.atan2(jy - hy, jx - hx), math.atan2(d[1], d[0])
        diff = (a1 - a0 + math.pi) % (2 * math.pi) - math.pi
        pts = [(hx + ww * math.cos(a0 + diff * k / 24), hy + ww * math.sin(a0 + diff * k / 24)) for k in range(25)]
        ax.plot([hx, tip[0]], [hy, tip[1]], color="#222", lw=1.3, zorder=7)
        ax.plot(*zip(*pts), color="#555", lw=.7, ls=(0, (3, 2)), zorder=7)
    side, d = ABRE[n]
    if side.startswith("slide"):
        off = 0.10
        yy = lambda a: p(a, 0)
        def ln(a0, a1, **kw):
            (x0, y0), (x1, y1) = p(a0, 0), p(a1, 0)
            ax.plot([x0 + d[0] * off, x1 + d[0] * off], [y0 + d[1] * off, y1 + d[1] * off], **kw)
        ln(lo, hi, color="#222", lw=2.2, zorder=7)
        g = -w if side == "slide_lo" else w
        ln(lo + g, hi + g, color="#555", lw=1.0, ls=(0, (3, 2)), zorder=7)
        return
    if side == "dbl":
        hoja(p(lo, 0), p(c, 0), d, w / 2); hoja(p(hi, 0), p(c, 0), d, w / 2)
    else:
        hinge, jamb = (p(lo, 0), p(hi, 0)) if side == "lo" else (p(hi, 0), p(lo, 0))
        hoja(hinge, jamb, d, w)


def ventana(ax, h):
    n, t, o, f, c, w, z0, z1 = h
    for off in (-.04, 0, .04):
        if o == "h": ax.plot([c - w / 2, c + w / 2], [f + off, f + off], color="#1565c0", lw=1.0, zorder=6)
        else: ax.plot([f + off, f + off], [c - w / 2, c + w / 2], color="#1565c0", lw=1.0, zorder=6)


def escalera_2d(ax):
    x0, y0, x1, y1 = ESC
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#eceff1", ec="#37474f", lw=1.0, zorder=4))
    ax.add_patch(Rectangle((ESC_IZQ[0], ESC_IZQ[1]), ESC_IZQ[2] - ESC_IZQ[0], ESC_IZQ[3] - ESC_IZQ[1], fc="#eceff1", ec="#37474f", lw=1.0, zorder=4))
    for k in range(13):                                  # 13 huellas de 0,255 desde el descansillo hacia el sur
        y = 7.715 - 0.255 * k
        ax.plot([x0, x1], [y, y], color="#37474f", lw=.7, zorder=5)
    for k in range(3):                                   # 3 peldaños de arranque
        x = ESC_IZQ[0] + 0.255 * (k + 1)
        ax.plot([x, x], [ESC_IZQ[1], ESC_IZQ[3]], color="#37474f", lw=.7, zorder=5)
    ax.annotate("", xy=(x0 + .48, 4.55), xytext=(x0 + .48, 7.2), arrowprops=dict(arrowstyle="->", color="#37474f"), zorder=6)
    ax.text(x0 + .48, 8.2, "escalera\nsube", fontsize=6.5, ha="center", color="#37474f", zorder=6)


def dibujo():
    m14, m29, t7 = geometria()
    fig, ax = plt.subplots(figsize=(11.5, 13.5))
    ax.set_xlim(-1.2, 13.0); ax.set_ylim(17.7, -2.4); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Distribución deseada sobre la obra real (croquis 27-11-2026), planta baja — esquema, no al milímetro",
                 fontsize=11.5, weight="bold", loc="left")
    for z in PR.ZUNCHOS: ax.add_patch(MPoly(list(banda(z, 0.30).exterior.coords), closed=True, fc="#c8e6c9", ec="none", alpha=.7, zorder=1))
    for n, x0, y0, x1, y1 in S: ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#fffdf5", ec="none", zorder=0))
    for r in (ESC, PASILLO, DISTR): ax.add_patch(Rectangle((r[0], r[1]), r[2] - r[0], r[3] - r[1], fc="#fffdf5", ec="none", zorder=0))
    pinta(ax, m14, fc="#e3edff", ec="#1a3fbf", hatch="////", lw=.8, zorder=3)
    pinta(ax, m29, fc="#1a3fbf", ec="#1a3fbf", lw=.8, zorder=3)
    pinta(ax, t7, fc="white", ec="#4f6fd8", lw=1.0, zorder=4)
    for n, x0, y0, x1, y1, h, col in MUEBLES: ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=col, ec="#555", lw=.5, zorder=5))
    ax.add_patch(MPoly(CHIMENEA, closed=True, fc="#ffcc80", ec="#e65100", lw=1, zorder=5))
    ax.add_patch(Rectangle(CONDUCTO[:2], CONDUCTO[2] - CONDUCTO[0], CONDUCTO[3] - CONDUCTO[1], fc="#8d6e63", ec="#4e342e", zorder=6))
    for x, y in TABURETES: ax.add_patch(Circle((x, y), .17, fc="#c9a46b", ec="#555", lw=.5, zorder=5))
    escalera_2d(ax)
    for h in HUECOS: (puerta if h[1] == "puerta" else ventana)(ax, h)
    ax.plot([2.97, 9.27], [15.55, 15.55], color="#1a3fbf", lw=0)           # fuerza el encuadre
    POS = {"Dormitorio suite": (3.3, 1.9, True), "Cocina": (7.7, 2.2, True), "Vestidor": (1.1, 5.6, False),
           "Baño suite": (1.1, 6.85, False), "Oficina": (4.1, 6.9, True), "Baño grande": (9.85, 5.6, False), "Salón": (5.3, 14.55, True)}
    for n, x0, y0, x1, y1 in S:
        a = AREAS[n]; px, py, dims = POS[n]
        txt = f"{n}\n{x1 - x0:.2f} × {y1 - y0:.2f} m\n{a:.1f} m²" if dims else f"{n}\n{a:.1f} m²"
        ax.text(px, py, txt, ha="center", va="center", fontsize=8.5 if dims else 7.8, weight="bold", color="#222", zorder=8)
    ax.text(7.45, 4.95, f"Comedor /\ndistribuidor\n{AREA_DISTR:.1f} m²", ha="center", va="center", fontsize=7.8, weight="bold", color="#222", zorder=8)
    ax.text(4.1, 4.9, "pasillo\n(bajo la escalera)", ha="center", va="center", fontsize=6.8, color="#222", zorder=8)
    ax.text(8.25, 14.1, "entrada", ha="center", fontsize=8, color="#222", rotation=90, zorder=8)
    ax.text(8.55, 16.2, "Puerta de entrada", ha="center", fontsize=8, weight="bold", zorder=8)
    ax.text(4.40, 9.45, "chimenea\nde esquina", fontsize=6.8, color="#e65100", zorder=8)
    for n, t, o, f, c, w, z0, z1 in HUECOS:
        if o == "h" and f < 1: ax.text(c, -0.55, n, ha="center", fontsize=8, color="#1565c0", weight="bold")
    ax.text(-1.1, -1.7, "SUR ↑ (como en los planos del proyecto y en tu croquis)", fontsize=8, color="#555")
    ax.text(-1.1, 17.4, ("Hatch: ladrillo de 14 cm.  Azul macizo: de 29 cm.  Fino con borde: tabique de 7 cm (diseño).  Verde: zunchos en el suelo.\n"
                        "Ya está en obra: muros marcados en el croquis de espesores. Propuesto/supuesto: muro de 29 cm de la línea norte del bloque (hasta x = 7,30 m) y lado norte del salón.\n"
                        "Dimensiones interiores entre caras de muro. Los huecos (puertas, ventanas) y el mobiliario son de diseño; la posición del zuncho central N-S es aproximada."),
            fontsize=7.6, va="top", color="#222")
    fig.savefig("distribucion_deseada_27nov.png", dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ----------------------------------------------------------------- DXF
def dxf():
    import ezdxf
    m14, m29, t7 = geometria()
    d = ezdxf.new("R2010"); msp = d.modelspace()
    for nom, col in [("MUROS14", 5), ("MUROS29", 1), ("TABIQUES7", 4), ("ZUNCHOS", 3), ("HUECOS", 6), ("MOBILIARIO", 8), ("TEXTO", 7)]:
        d.layers.add(nom, color=col)
    def poli(g, layer):
        for p in poligonos(g):
            for ring in [p.exterior] + list(p.interiors): msp.add_lwpolyline(list(ring.coords), close=True, dxfattribs={"layer": layer})
    poli(m14, "MUROS14"); poli(m29, "MUROS29"); poli(t7, "TABIQUES7")
    for z in PR.ZUNCHOS: poli(banda(z, .30), "ZUNCHOS")
    for h in HUECOS: poli(hueco_box(h, .1), "HUECOS")
    for n, x0, y0, x1, y1, hh, col in MUEBLES: msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "MOBILIARIO"})
    msp.add_lwpolyline(CHIMENEA, close=True, dxfattribs={"layer": "MOBILIARIO"})
    for n, x0, y0, x1, y1 in S:
        msp.add_text(f"{n} {AREAS[n]:.1f} m2", height=.18, dxfattribs={"layer": "TEXTO"}).set_placement(((x0 + x1) / 2, (y0 + y1) / 2), align=ezdxf.enums.TextEntityAlignment.MIDDLE_CENTER)
    d.saveas("distribucion_deseada.dxf")


# ----------------------------------------------------------------- 3D
def modelo3d(alto=H):
    import cadquery as cq
    def extruye(g, z0, z1):
        res = None
        for p in poligonos(g):
            s = cq.Workplane("XY").workplane(offset=z0).polyline(list(p.exterior.coords)[:-1]).close().extrude(z1 - z0)
            for r in p.interiors: s = s.cut(cq.Workplane("XY").workplane(offset=z0 - .1).polyline(list(r.coords)[:-1]).close().extrude(z1 - z0 + .2))
            res = s if res is None else res.union(s)
        return res
    def caja(x0, y0, x1, y1, z0, z1): return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))
    def muros(items):
        g = unary_union([banda(p, e) for n, p, e in items] if items and isinstance(items[0], tuple) and len(items[0]) == 3 else [banda(p, .07) for n, p in items])
        s = extruye(g, 0, alto)
        for h in HUECOS:
            n, t, o, f, c, w, z0, z1 = h
            hb = hueco_box(h, .6).bounds
            s = s.cut(caja(hb[0], hb[1], hb[2], hb[3], z0, z1))
        return s
    parts = {}
    solera = unary_union([box(-0.07, -0.07, 9.28, 8.97), box(2.825, 8.82, 9.415, 15.695), box(9.20, 4.055, 11.62, 7.345)])
    parts["solera"] = (extruye(solera, -0.08, 0), (0.86, 0.84, 0.78))
    parts["zunchos"] = (extruye(unary_union([banda(z, .30) for z in PR.ZUNCHOS]), -0.30, 0), (0.45, 0.75, 0.45))
    parts["muros_14cm"] = (muros([m for m in EXIST if m[2] == .14]), (0.78, 0.82, 0.95))
    parts["muros_29cm"] = (muros([m for m in EXIST + PROP29 if m[2] == .29]), (0.30, 0.38, 0.75))
    parts["tabiques_7cm"] = (muros(TAB), (0.95, 0.95, 0.95))
    # escalera: aviso, tramo recto en losa con intradós inclinado; descansillo y arranque macizos
    R, T, ZP = 0.181, 0.255, 0.724
    x0, x1 = ESC[0], ESC[2]
    pts = [(7.715, ZP - .02)]
    for k in range(1, 14):
        ys, z = 7.715 - T * (k - 1), ZP + R * k
        pts += [(ys, z), (ys - T, z)]
    pts += [(4.40, ZP + R * 13 - .22)]
    pts = [(y, z) for y, z in pts]
    # sección en el plano YZ, extruida a lo largo de X
    flight = cq.Workplane("YZ").workplane(offset=x0).polyline(pts).close().extrude(x1 - x0)
    st = flight.union(caja(x0, 7.715, x1, 8.675, 0, ZP))
    for k in range(3):
        xa = ESC_IZQ[0] + T * k
        st = st.union(caja(xa, 7.72, xa + T, 8.675, 0, R * (3 - k)))
    parts["escalera"] = (st, (0.62, 0.62, 0.64))
    mue = None
    for n, ax0, ay0, ax1, ay1, hh, col in MUEBLES:
        b = caja(ax0, ay0, ax1, ay1, 0, hh); mue = b if mue is None else mue.union(b)
    mue = mue.union(cq.Workplane("XY").polyline([(a, b) for a, b in CHIMENEA]).close().extrude(.25)).union(caja(*CONDUCTO, 0, alto))
    for x, y in TABURETES: mue = mue.union(cq.Workplane("XY").circle(.17).extrude(.65).translate((x, y, 0)))
    parts["mobiliario"] = (mue, (0.72, 0.58, 0.40))
    return parts


def exporta3d():
    import cadquery as cq, trimesh, numpy as np
    parts = modelo3d(H)
    asm = cq.Assembly(name="distribucion_deseada")
    for n, (s, col) in parts.items(): asm.add(s, name=n, color=cq.Color(*col))
    asm.save("distribucion_deseada.step")
    scene = trimesh.Scene()
    for n, (s, col) in parts.items():
        v, f = s.val().tessellate(0.005)
        m = trimesh.Trimesh([(p.x, p.y, p.z) for p in v], f)
        m.visual.face_colors = [int(c * 255) for c in col] + [255]
        scene.add_geometry(m, node_name=n)
    scene.export("distribucion_deseada.glb")
    return parts


def render3d():
    import numpy as np
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    parts = modelo3d(1.5)
    fig = plt.figure(figsize=(12, 10)); ax = fig.add_subplot(111, projection="3d"); ax.set_proj_type("ortho")
    ax.view_init(elev=52, azim=70)
    luz = np.array([-0.4, 0.5, 0.8]); luz /= np.linalg.norm(luz)
    T, C = [], []
    for n, (s, col) in parts.items():
        v, f = s.val().tessellate(0.02)
        V = np.array([(p.x, p.y, p.z) for p in v]); F = np.array(f)
        tri = V[F]; nor = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0]); ln = np.linalg.norm(nor, axis=1); ln[ln == 0] = 1
        nor = nor / ln[:, None]; sh = 0.55 + 0.45 * np.abs(nor @ luz)
        T.append(tri); C += [tuple(np.clip(np.array(col) * k, 0, 1)) + (1,) for k in sh]
    ax.add_collection3d(Poly3DCollection(np.concatenate(T), facecolors=C, edgecolors=(0, 0, 0, .10), linewidths=.2))
    ax.set_xlim(-1, 12.5); ax.set_ylim(-1, 16.5); ax.set_zlim(-0.5, 6)
    ax.set_box_aspect((13.5, 17.5, 6.5)); ax.axis("off")
    ax.set_title("Maqueta seccionada a 1,5 m (la planta real llega a 3,0 m), vista desde el norte: muros, tabiques, escalera y mobiliario", fontsize=10, loc="left")
    fig.savefig("distribucion_deseada_3d.png", dpi=130, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def resumen():
    tab_len = sum(LineString(p).length for n, p in TAB)
    puertas_tab = sum(h[5] for h in HUECOS if h[0] in ("D2", "D3", "D4", "D6", "D8"))
    print("ÁREAS (m², caras interiores):")
    for n, a in AREAS.items(): print(f"  {n:30s} {a:6.2f}")
    print(f"  {'TOTAL':30s} {sum(AREAS.values()):6.2f}")
    for n, p in TAB: print(f"  tabique {n:30s} {LineString(p).length:5.2f} m")
    print(f"TABIQUES 7 cm: {tab_len:.2f} m de longitud; {tab_len * H:.1f} m² brutos; {tab_len * H - puertas_tab * 2.05:.1f} m² netos de puertas")
    l29 = sum(LineString(p).length for n, p, e in PROP29)
    print(f"MUROS 29 cm propuestos/supuestos: {l29:.2f} m ({l29 * H:.1f} m²)")


if __name__ == "__main__":
    resumen()
    dibujo()
    dxf()
    if "--sin3d" not in sys.argv:
        exporta3d(); render3d()
