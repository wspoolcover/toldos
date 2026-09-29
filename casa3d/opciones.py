"""Opciones de distribución (esquemas en planta). Coordenadas del croquis en metros; muros existentes de 0,55 m.
Arriba del croquis = sur (cocina); derecha = este; el pasillo de entrada va por el lado derecho del salón."""
import math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle, Arc
from shapely.geometry import Polygon

XE, Y_TOP, Y_JUNC = 9.55, 16.30, 7.32
PTS = [(3.15, 0), (9.55, 0), (9.55, 8.30), (12.05, 8.30), (12.05, 11.80), (9.55, 11.80), (9.55, 16.30), (0, 16.30), (0, 7.32), (2.87, 7.32)]
OUT = Polygon(PTS); INN = OUT.buffer(-0.55, join_style=2)
COL = {"sala": "#fff3c4", "priv": "#d6e6f5", "humedo": "#cfe8d5", "cocina": "#f9d9b8", "circ": "#e6e6e6", "esc": "#d9c3a5", "terraza": "#f4f4f4"}
SALON = [(3.68, 0.55), (7.45, 0.55), (7.45, 7.87), (3.42, 7.87)]


def R(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

# ---- puertas: (x, y, 'H'|'V', ancho, extremo_bisagra 0|1, giro +1|-1; giro 0 = paso libre) ----
FRONT = (7.55, 0.55, "H", 1.40, 1, 1)          # puerta de entrada de 1,40 pegada al muro este, abre hacia dentro
PTS_PA = [(3.15, 0), (9.55, 0), (9.55, 8.30), (10.85, 8.30), (10.85, 11.80), (9.55, 11.80), (9.55, 16.30), (0, 16.30), (0, 7.32), (2.87, 7.32)]
from shapely.geometry import box as sbox
OUT_PA = OUT.intersection(sbox(-1, -1, 10.85, 20)); INN_PA = INN.intersection(sbox(-1, -1, 10.55, 20))   # en planta alta el baño solo entra la mitad hacia el vecino
COMUN_PB = [("Pasillo de entrada\n(murete a media altura)", "circ", R(7.55, 0.55, 9.00, 7.87)), ("Entrada", "circ", R(7.25, 7.87, 9.00, 8.95)),
            ("Escalera", "esc", R(7.25, 8.95, 9.00, 11.75)), ("Baño grande", "humedo", R(9.10, 8.85, 11.50, 11.25)),
            ("Cocina", "cocina", R(5.05, 11.85, 9.00, 15.75)), ("Salón", "sala", SALON)]
COMUN_DOORS = [FRONT, (9.05, 9.20, "V", 0.80, 0, 1), (5.30, 11.75, "H", 1.80, 0, 0)]
BASE_PA = [("Terraza sobre el salón", "terraza", SALON), ("Entrada", "circ", R(7.25, 7.87, 9.00, 8.95)), ("Escalera (hueco)", "esc", R(7.25, 8.95, 9.00, 11.75)),
           ("Baño", "humedo", R(9.10, 8.85, 10.55, 11.25)), ("Sala familiar\ny terraza", "sala", R(3.45, 7.87, 7.15, 11.75)),
           ("Dormitorio 1", "priv", R(0.55, 7.87, 3.35, 11.75)), ("Dormitorio 2", "priv", R(0.55, 11.85, 4.95, 15.75)), ("Dormitorio 3", "priv", R(5.05, 11.85, 9.00, 15.75))]
DOORS_PA = [(3.35, 9.50, "V", 0.90, 0, -1), (3.60, 11.75, "H", 0.80, 0, 1), (5.50, 11.75, "H", 0.80, 0, 1), (9.05, 9.20, "V", 0.80, 0, 1)]


def F(ax, kind, *a, **k):
    z = 5
    if kind == "rect": ax.add_patch(Rectangle((a[0], a[1]), a[2], a[3], fc=k.get("fc", "#fff"), ec="#333", lw=.8, hatch=k.get("hatch"), zorder=z))


def muebles_1(ax):       # suite compacta al norte-oeste, oficina en el ala oeste
    F(ax, "rect", 2.30, 13.25, 1.6, 2.0, fc="#f7b98a")                      # cama, cabecero al fondo
    for x in (1.85, 3.95): F(ax, "rect", x, 15.3, .4, .4)
    F(ax, "rect", 0.60, 14.20, 0.45, 1.5, fc="#e8d5c0", hatch="||"); F(ax, "rect", 1.50, 14.20, 0.40, 1.5, fc="#e8d5c0", hatch="||")   # armarios
    F(ax, "rect", 0.65, 11.95, 0.75, 0.55); F(ax, "rect", 1.50, 12.00, 0.40, 0.40); F(ax, "rect", 0.65, 12.60, 0.55, 0.9, fc="#eef")     # inodoro, lavabo, ducha
    F(ax, "rect", 1.00, 8.30, 1.90, 0.65, fc="#e8d5c0"); F(ax, "rect", 1.20, 9.3, 0.6, 0.5)                                               # mesa de trabajo y silla


def muebles_2(ax):       # suite en línea (dormitorio - paso de vestidor - baño), oficina al norte
    F(ax, "rect", 0.55, 8.70, 2.0, 1.6, fc="#f7b98a")                       # cama con cabecero contra el muro oeste
    F(ax, "rect", 0.60, 8.20, .45, .45); F(ax, "rect", 0.60, 10.35, .45, .45)
    F(ax, "rect", 0.55, 11.95, 0.55, 1.35, fc="#e8d5c0", hatch="||"); F(ax, "rect", 2.50, 11.95, 0.55, 1.35, fc="#e8d5c0", hatch="||")  # armarios a ambos lados
    F(ax, "rect", 0.65, 13.60, 0.75, 1.7); F(ax, "rect", 2.55, 13.60, 0.45, 1.2); F(ax, "rect", 0.65, 15.35, 0.8, 0.30, fc="#eef"); F(ax, "rect", 1.75, 15.30, 0.45, 0.40)
    F(ax, "rect", 3.30, 14.9, 1.4, 0.65, fc="#e8d5c0"); F(ax, "rect", 3.75, 14.2, 0.55, 0.5)                                            # mesa y silla de la oficina


OPCIONES = {
 "1": dict(
  titulo="Opción 1 — oficina en el ala oeste y suite compacta",
  ideas=["La oficina (10,9 m²) ocupa el ala oeste, con puerta desde la sala de estar; ya no hay nada raro en el salón, que queda entero.",
         "Suite al norte-oeste: dormitorio de 11 m², vestidor y baño en una franja al lado. Es la más ajustada de las dos.",
         "Pasillo de entrada con murete, entrada amplia con escalera y baño; todo abre a la sala. Arriba sin pasillo."],
  PB=COMUN_PB + [("Sala de estar\ny comedor", "sala", R(3.45, 7.87, 7.15, 11.75)), ("Oficina", "priv", R(0.55, 7.87, 3.35, 11.75)),
                 ("Dormitorio\nprincipal", "priv", R(2.05, 11.85, 4.95, 15.75), (3.55, 12.7)), ("Vestidor", "priv", R(0.55, 14.15, 1.95, 15.75), (1.25, 14.95)),
                 ("Baño", "humedo", R(0.55, 11.85, 1.95, 14.05), (1.25, 12.85))],
  doorsPB=COMUN_DOORS + [(3.35, 9.50, "V", 0.90, 0, -1), (3.70, 11.75, "H", 0.80, 0, 1), (1.95, 14.40, "V", 0.80, 0, 1), (0.80, 14.05, "H", 0.80, 0, -1)],
  abPB=[(3.55, 7.87, 7.05, 7.87), (7.20, 7.97, 7.20, 8.90)], muebles=muebles_1, PA=BASE_PA, doorsPA=DOORS_PA, abPA=[(7.20, 7.97, 7.20, 8.90)]),
 "2": dict(
  titulo="Opción 2 — suite en línea y oficina acristalada al sur",
  vidrios=[("hueco", 3.20, 15.75, 1.70, 0.55, "cristalera de suelo a techo"), ("linea", 5.00, 12.00, 5.00, 15.60), ("linea", 3.15, 12.00, 3.15, 15.60)],
  ideas=["Suite en línea: dormitorio de 13 m² → paso de vestidor con armarios a ambos lados → baño de 5,8 m² con bañera y doble lavabo.",
         "La oficina (7 m²) es un cuarto acristalado: cristalera de suelo a techo en la fachada sur y tabiques de vidrio hacia la cocina y la suite para que pase la luz.",
         "La sala de estar se estrecha un poco (12 m²) pero sigue abierta al salón entero. Arriba igual que la opción 1."],
  PB=COMUN_PB + [("Sala de estar\ny comedor", "sala", R(4.05, 7.87, 7.15, 11.75)), ("Dormitorio\nprincipal", "priv", R(0.55, 7.87, 3.95, 11.75), (2.65, 10.45)),
                 ("Vestidor", "priv", R(0.55, 11.85, 3.05, 13.35), (1.8, 12.6)), ("Baño principal", "humedo", R(0.55, 13.45, 3.05, 15.75), (1.9, 14.4)),
                 ("Oficina\nacristalada", "priv", R(3.15, 11.85, 4.95, 15.75))],
  doorsPB=COMUN_DOORS + [(3.95, 9.50, "V", 0.90, 0, -1), (1.50, 11.75, "H", 0.80, 0, 1), (1.50, 13.35, "H", 0.80, 0, 1), (4.15, 11.75, "H", 0.80, 0, 1)],
  abPB=[(4.15, 7.87, 7.05, 7.87), (7.20, 7.97, 7.20, 8.90)], muebles=muebles_2, PA=BASE_PA, doorsPA=DOORS_PA, abPA=[(7.20, 7.97, 7.20, 8.90)]),
}


def area(poly): return Polygon(poly).area


def door(ax, d):
    x, y, o, w, he, s = d
    if s == 0:                                                     # paso libre
        (ax.plot([x, x + w], [y, y], color="white", lw=5, solid_capstyle="butt", zorder=7) if o == "H" else ax.plot([x, x], [y, y + w], color="white", lw=5, solid_capstyle="butt", zorder=7)); return
    if o == "H": hg = (x if he == 0 else x + w, y); al = (1 if he == 0 else -1, 0); pe = (0, s)
    else: hg = (x, y if he == 0 else y + w); al = (0, 1 if he == 0 else -1); pe = (s, 0)
    (ax.plot([x, x + w], [y, y], color="white", lw=5, solid_capstyle="butt", zorder=7) if o == "H" else ax.plot([x, x], [y, y + w], color="white", lw=5, solid_capstyle="butt", zorder=7))
    a1, a2 = math.degrees(math.atan2(al[1], al[0])), math.degrees(math.atan2(pe[1], pe[0]))
    t1, t2 = (a1, a2) if (a2 - a1) % 360 == 90 else (a2, a1)
    ax.add_patch(Arc(hg, 2 * w, 2 * w, theta1=t1, theta2=t2, color="#333", lw=.9, zorder=8))
    ax.plot([hg[0], hg[0] + pe[0] * w], [hg[1], hg[1] + pe[1] * w], color="#333", lw=1.2, zorder=8)


def mueble_suite(ax):
    z = 5
    ax.add_patch(Rectangle((2.05, 13.75), 1.6, 2.0, fc="#f7b98a", ec="#333", lw=.9, zorder=z))               # cama (cabecero contra el muro del fondo)
    for x in (1.55, 3.7): ax.add_patch(Rectangle((x, 15.25), .4, .45, fc="#fff", ec="#333", lw=.7, zorder=z))
    for y0 in (9.55, 11.20): ax.add_patch(Rectangle((0.55, y0), 2.8, .55, fc="#e8d5c0", ec="#333", lw=.8, hatch="||", zorder=z))   # armarios a ambos lados del paso
    ax.add_patch(Rectangle((0.65, 8.0), 1.75, 0.75, fc="#fff", ec="#333", lw=.9, zorder=z))                  # bañera
    ax.add_patch(Rectangle((2.75, 8.0), 0.55, 1.15, fc="#fff", ec="#333", lw=.9, zorder=z))                  # doble lavabo
    ax.add_patch(Rectangle((0.65, 8.85), 0.9, 0.5, fc="#eef", ec="#333", lw=.9, zorder=z))                   # ducha
    ax.add_patch(Rectangle((1.75, 8.95), 0.45, 0.4, fc="#fff", ec="#333", lw=.9, zorder=z))                  # inodoro


LABEL_POS = {"Dormitorio\nprincipal": (3.9, 12.75), "Vestidor": (1.95, 10.65), "Baño principal": (1.95, 9.15)}


MUEBLES = None
VIDRIOS = []


def dibujar(ax, rooms, doors, planta, abiertos=()):
    out, inn = (OUT, INN) if planta == "PB" else (OUT_PA, INN_PA)
    ax.add_patch(MPoly(list(out.exterior.coords), closed=True, fc="#8d8d8d", ec="#222", lw=1.6, zorder=1))
    ax.add_patch(MPoly(list(inn.exterior.coords), closed=True, fc="white", ec="none", zorder=2))
    if planta == "PB":
        ax.add_patch(Rectangle((10.85, 8.30), 1.20, 3.50, fc="none", ec="#a33", ls="--", lw=.9, zorder=4)); ax.text(11.45, 8.05, "vecino (1.ª planta)\nencima de esta mitad", ha="center", va="top", fontsize=5.8, color="#a33")
    if planta == "PA":
        ax.add_patch(Rectangle((10.85, 8.30), 1.20, 3.50, fc="#f0e0e0", ec="#a33", ls="--", lw=.9, zorder=1)); ax.text(11.45, 10.05, "casa vecina\n(1.ª planta)\nsobre el baño\nde abajo", ha="center", va="center", fontsize=6, color="#a33")
    circ = 0; total = 0
    for room in rooms:
        nombre, tipo, poly = room[:3]; lpos = room[3] if len(room) > 3 else None
        a = area(poly)
        ax.add_patch(MPoly(poly, closed=True, fc=COL[tipo], ec="#222", lw=1.3 if tipo != "terraza" else .8, ls="-" if tipo != "terraza" else "--", zorder=3, hatch="//" if tipo == "esc" else None))
        cx_, cy_ = lpos or Polygon(poly).centroid.coords[0]
        pequeno = Polygon(poly).bounds[2] - Polygon(poly).bounds[0] < 2.2
        ax.text(cx_, cy_, f"{nombre}\n{a:.1f} m²", ha="center", va="center", fontsize=6.6 if pequeno else 8, zorder=6, linespacing=1.15)
        if tipo == "circ": circ += a
        if tipo not in ("terraza", "esc"): total += a
    if planta == "PB":
        ax.add_patch(Rectangle((7.45, 0.55), 0.10, 6.77, fc="#666", ec="#222", zorder=4)); ax.text(7.33, 3.6, "murete media altura", rotation=90, ha="right", va="center", fontsize=6.5)
        ax.text(3.6, 7.65, "abierto: salón y comedor", fontsize=6.5, style="italic", zorder=6)
    if planta == "PB" and MUEBLES: MUEBLES(ax)
    if planta == "PB":
        for v in VIDRIOS:
            if v[0] == "hueco": ax.add_patch(Rectangle((v[1], v[2]), v[3], v[4], fc="#bfe3f8", ec="#2f8fd0", lw=1.2, zorder=6)); ax.text(v[1] + v[3] / 2, v[2] + v[4] + 0.15, v[5], ha="center", va="bottom", fontsize=6.5, color="#1f6fa8", zorder=8)
            else: ax.plot([v[1], v[3]], [v[2], v[4]], color="#2f8fd0", lw=3, zorder=6, solid_capstyle="butt")
    for (x0, y0, x1, y1) in abiertos: ax.plot([x0, x1], [y0, y1], color="white", lw=5, solid_capstyle="butt", zorder=7)
    for d in doors: door(ax, d)
    ax.set_xlim(-0.6, 12.6); ax.set_ylim(-0.6, 16.9); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("PLANTA BAJA" if planta == "PB" else "PLANTA ALTA", fontsize=10, weight="bold")
    return circ, total


if __name__ == "__main__":
    for k, o in OPCIONES.items():
        MUEBLES = o["muebles"]; VIDRIOS = o.get("vidrios", [])
        fig = plt.figure(figsize=(13, 9.5)); fig.suptitle(o["titulo"], fontsize=14, weight="bold", x=0.02, ha="left")
        ax1 = fig.add_axes([0.02, 0.10, 0.46, 0.80]); ax2 = fig.add_axes([0.51, 0.10, 0.46, 0.80])
        c1, t1 = dibujar(ax1, o["PB"], o["doorsPB"], "PB", o["abPB"]); c2, t2 = dibujar(ax2, o["PA"], o["doorsPA"], "PA", o["abPA"])
        fig.text(0.02, 0.055, "\n".join("• " + t for t in o["ideas"]), fontsize=8.6, va="top")
        fig.text(0.98, 0.055, f"Circulación: {c1 + c2:.1f} m² (PB {c1:.1f} + PA {c2:.1f})\nNorte hacia abajo (supuesto). Medidas orientativas.", fontsize=8.6, va="top", ha="right")
        fig.savefig(f"opcion_{k}.png", dpi=110); plt.close(fig)
        print(k, f"circulación {c1 + c2:.1f} m²; útil PB {t1:.1f}, PA {t2:.1f}")
