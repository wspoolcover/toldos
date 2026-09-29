"""Distribución propuesta (esquema en planta). Coordenadas del croquis en metros; muros existentes de 0,55 m.
Abajo del croquis = NORTE (calle, entrada y salón); arriba = SUR (fachada del fondo: cocina y dormitorio principal)."""
import math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle, Arc
from shapely.geometry import Polygon, box as sbox

PTS = [(3.15, 0), (9.55, 0), (9.55, 8.30), (12.05, 8.30), (12.05, 11.80), (9.55, 11.80), (9.55, 16.30), (0, 16.30), (0, 7.32), (2.87, 7.32)]
OUT = Polygon(PTS)
NB_FULL = [(0, 7.32), (9.55, 7.32), (9.55, 8.30), (12.05, 8.30), (12.05, 11.80), (9.55, 11.80), (9.55, 16.30), (0, 16.30)]
SB_ = [(3.15, 0), (9.55, 0), (9.55, 7.32), (2.87, 7.32)]
INN = Polygon(NB_FULL).buffer(-0.55, join_style=2).union(Polygon(SB_).buffer(-0.25, join_style=2))   # casa existente 0,55 m; salón de ladrillo 0,25 m
OUT_PA = OUT.intersection(sbox(-1, -1, 10.85, 20)); INN_PA = INN.intersection(sbox(-1, -1, 10.55, 20))   # planta alta: el baño solo entra la mitad hacia el vecino
COL = {"sala": "#fff3c4", "priv": "#d6e6f5", "humedo": "#cfe8d5", "cocina": "#f9d9b8", "circ": "#e6e6e6", "esc": "#d9c3a5", "terraza": "#f4f4f4"}


def R(x0, y0, x1, y1): return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

# salón: se adelanta un poco hacia la sala de estar (rincón de la chimenea)
SALON_PB = [(3.40, 0.25), (7.75, 0.25), (7.75, 7.87), (5.55, 7.87), (5.55, 9.55), (3.45, 9.55), (3.45, 7.87), (3.12, 7.87)]
SALON_PA = [(3.40, 0.25), (9.30, 0.25), (9.30, 7.32), (3.12, 7.32)]
HUB = [(3.45, 9.65), (5.65, 9.65), (5.65, 7.87), (7.15, 7.87), (7.15, 11.75), (3.45, 11.75)]

PB = [("Salón con comedor", "sala", SALON_PB, (5.45, 4.6)), ("Pasillo de entrada\n(murete a media altura)", "circ", [(7.85, 0.25), (9.30, 0.25), (9.30, 7.32), (9.00, 7.32), (9.00, 7.87), (7.85, 7.87)]),
      ("Entrada", "circ", R(7.25, 7.87, 9.00, 8.95)), ("Escalera", "esc", R(7.25, 8.95, 9.00, 11.75)), ("Baño grande", "humedo", R(9.10, 8.85, 11.50, 11.25)),
      ("Sala de estar\ny paso", "sala", HUB, (5.15, 10.7)), ("Cocina", "cocina", R(5.05, 11.85, 9.00, 15.75)),
      ("Dormitorio principal", "priv", R(0.55, 11.85, 4.95, 15.75), (3.35, 14.55)), ("Vestidor", "priv", R(0.55, 9.45, 3.35, 11.75), (2.35, 10.6)),
      ("Baño", "humedo", R(0.55, 7.87, 3.35, 9.35), (1.95, 9.05))]
PB_DOORS = [(7.85, 0.25, "H", 1.40, 1, 1),            # puerta de entrada de 1,40, pegada al muro este, abre hacia dentro
            (9.05, 9.20, "V", 0.80, 0, 1), (5.30, 11.75, "H", 1.80, 0, 0),
            (3.35, 10.20, "V", 0.90, 0, -1),           # de la sala directamente al vestidor
            (1.50, 9.35, "H", 0.80, 0, -1),            # vestidor -> baño (a la izquierda)
            (1.50, 11.75, "H", 0.80, 0, 1),            # vestidor -> dormitorio (a la derecha)
            (7.50, 15.75, "H", 1.00, 0, -1)]           # cocina -> patio del fondo
PB_OPEN = [(5.60, 7.95, 5.60, 9.50), (5.70, 7.87, 7.05, 7.87), (7.20, 7.97, 7.20, 8.90)]
VENTANAS = [(1.00, 15.75, 1.20), (3.00, 15.75, 1.20), (5.55, 15.75, 1.20), (1.20, 7.32, 1.20)]      # (x, y de la cara interior del muro, ancho)
VENTANAS_E = [(9.00, 13.00, 1.60)]                                                                      # ventana de cocina al este

PA = [("Terraza sobre el salón", "terraza", SALON_PA), ("Entrada", "circ", R(7.25, 7.87, 9.00, 8.95)), ("Escalera (hueco)", "esc", R(7.25, 8.95, 9.00, 11.75)),
      ("Baño", "humedo", R(9.10, 8.85, 10.55, 11.25)), ("Sala familiar\ny terraza", "sala", R(3.45, 7.87, 7.15, 11.75)),
      ("Dormitorio 1", "priv", R(0.55, 7.87, 3.35, 11.75)), ("Dormitorio 2", "priv", R(0.55, 11.85, 4.95, 15.75)),
      ("Dormitorio 3\n(o despacho)", "priv", R(5.05, 11.85, 9.00, 15.75))]
PA_DOORS = [(3.35, 9.50, "V", 0.90, 0, -1), (3.60, 11.75, "H", 0.80, 0, 1), (5.50, 11.75, "H", 0.80, 0, 1), (9.05, 9.20, "V", 0.80, 0, 1)]
PA_OPEN = [(7.20, 7.97, 7.20, 8.90)]


def area(poly): return Polygon(poly).area


def door(ax, d):
    x, y, o, w, he, s = d
    blanco = dict(color="white", lw=5, solid_capstyle="butt", zorder=7)
    if o == "H": ax.plot([x, x + w], [y, y], **blanco)
    else: ax.plot([x, x], [y, y + w], **blanco)
    if s == 0: return
    if o == "H": hg = (x if he == 0 else x + w, y); al = (1 if he == 0 else -1, 0); pe = (0, s)
    else: hg = (x, y if he == 0 else y + w); al = (0, 1 if he == 0 else -1); pe = (s, 0)
    a1, a2 = math.degrees(math.atan2(al[1], al[0])), math.degrees(math.atan2(pe[1], pe[0]))
    t1, t2 = (a1, a2) if (a2 - a1) % 360 == 90 else (a2, a1)
    ax.add_patch(Arc(hg, 2 * w, 2 * w, theta1=t1, theta2=t2, color="#333", lw=.9, zorder=8))
    ax.plot([hg[0], hg[0] + pe[0] * w], [hg[1], hg[1] + pe[1] * w], color="#333", lw=1.2, zorder=8)


def r(ax, x, y, dx, dy, fc="#fff", hatch=None, z=5): ax.add_patch(Rectangle((x, y), dx, dy, fc=fc, ec="#333", lw=.8, hatch=hatch, zorder=z))


def muebles_pb(ax):
    # salón: sofá en U abierto hacia la pantalla, mesa baja, pantalla grande en el muro oeste, chimenea en el rincón, mesa de comedor
    r(ax, 6.75, 1.05, 0.75, 3.30, "#c9b79c"); r(ax, 5.35, 3.65, 1.40, 0.70, "#c9b79c"); r(ax, 5.35, 1.05, 1.40, 0.70, "#c9b79c")       # sofá en U
    r(ax, 5.65, 2.05, 0.80, 1.35, "#efe6d6")                                                                                              # mesa baja
    r(ax, 3.60, 1.60, 0.16, 1.90, "#222"); ax.text(3.98, 3.60, "pantalla", fontsize=6.3, color="#333", va="bottom", zorder=8)              # televisión
    r(ax, 3.50, 8.75, 1.15, 0.80, "#d8d0c8"); r(ax, 3.65, 8.98, 0.85, 0.35, "#f4a742"); ax.text(4.05, 8.62, "chimenea", fontsize=6.3, color="#a33", ha="center", va="top", zorder=8)
    r(ax, 4.55, 5.25, 1.00, 2.05, "#e8d5c0")
    for y in (5.4, 6.1, 6.8): r(ax, 4.27, y, .22, .4); r(ax, 5.61, y, .22, .4)
    ax.plot([3.55, 5.45], [4.9, 4.9], color="#a58", lw=.8, ls=":", zorder=6); ax.text(3.6, 5.0, "comedor", fontsize=6.3, color="#a58", va="bottom", zorder=8)
    # suite: cama contra el muro oeste, armarios en el vestidor, baño
    r(ax, 0.55, 13.15, 2.00, 1.60, "#f7b98a"); r(ax, 0.60, 12.60, .45, .45); r(ax, 0.60, 14.85, .45, .45)
    r(ax, 0.55, 9.55, 0.60, 2.05, "#e8d5c0", "||"); r(ax, 1.15, 11.20, 2.15, 0.50, "#e8d5c0", "||")
    r(ax, 0.65, 7.97, 1.75, 0.70); r(ax, 2.55, 7.97, 0.75, 0.45); r(ax, 2.45, 8.55, 0.45, 0.40)
    # cocina: isla y fregadero junto a la fachada del fondo
    r(ax, 6.0, 13.2, 2.2, 0.8, "#eadcc4"); r(ax, 5.15, 15.2, 3.7, 0.5, "#eadcc4")


def dibujar(ax, rooms, doors, planta, abiertos=()):
    out, inn = (OUT, INN) if planta == "PB" else (OUT_PA, INN_PA)
    ax.add_patch(MPoly(list(out.exterior.coords), closed=True, fc="#8d8d8d", ec="#222", lw=1.6, zorder=1))
    for g in getattr(inn, "geoms", [inn]): ax.add_patch(MPoly(list(g.exterior.coords), closed=True, fc="white", ec="none", zorder=2))
    ax.add_patch(Rectangle((10.85, 8.30), 1.20, 3.50, fc="#f0e0e0" if planta == "PA" else "none", ec="#a33", ls="--", lw=.9, zorder=1 if planta == "PA" else 4))
    ax.text(11.45, 10.05 if planta == "PA" else 8.05, "casa vecina\n(1.ª planta)" + ("\nsobre el baño\nde abajo" if planta == "PA" else "\nencima de esta mitad"), ha="center", va="center" if planta == "PA" else "top", fontsize=5.8, color="#a33")
    circ = total = 0
    for room in rooms:
        nombre, tipo, poly = room[:3]; lpos = room[3] if len(room) > 3 else None
        a = area(poly); pol = Polygon(poly)
        ax.add_patch(MPoly(poly, closed=True, fc=COL[tipo], ec="#222", lw=1.3 if tipo != "terraza" else .8, ls="-" if tipo != "terraza" else "--", zorder=3, hatch="//" if tipo == "esc" else None))
        cx_, cy_ = lpos or pol.centroid.coords[0]
        pequeno = pol.bounds[2] - pol.bounds[0] < 2.2
        ax.text(cx_, cy_, f"{nombre}\n{a:.1f} m²", ha="center", va="center", fontsize=6.6 if pequeno else 8, zorder=9, linespacing=1.15)
        if tipo == "circ": circ += a
        if tipo not in ("terraza", "esc"): total += a
    if planta == "PB":
        muebles_pb(ax)
        ax.add_patch(Rectangle((7.75, 0.25), 0.10, 7.07, fc="#666", ec="#222", zorder=4)); ax.text(7.65, 3.6, "murete media altura", rotation=90, ha="right", va="center", fontsize=6.5, zorder=9)
        ax.add_patch(Rectangle((3.55, 0.0), 4.00, 0.25, fc="#bfe3f8", ec="#2f8fd0", lw=1.4, zorder=6))
        ax.text(5.5, -0.15, "cristalera de suelo a techo (4,00 m) junto a la puerta", ha="center", va="top", fontsize=6.6, color="#1f6fa8", zorder=8)
        for (x, y, w) in VENTANAS: ax.add_patch(Rectangle((x, y), w, 0.55 if y > 10 else -0.55, fc="#bfe3f8", ec="#2f8fd0", lw=1.0, zorder=6))
        for (x, y, w) in VENTANAS_E: ax.add_patch(Rectangle((x, y), 0.55, w, fc="#bfe3f8", ec="#2f8fd0", lw=1.0, zorder=6))
    for (x0, y0, x1, y1) in abiertos: ax.plot([x0, x1], [y0, y1], color="white", lw=5, solid_capstyle="butt", zorder=7)
    for d in doors: door(ax, d)
    ax.annotate("", xy=(-0.1, -0.6), xytext=(-0.1, 1.6), arrowprops=dict(arrowstyle="-|>", color="#222", lw=1.6), annotation_clip=False)
    ax.text(-0.1, 1.85, "N", ha="center", fontsize=11, weight="bold"); ax.text(11.9, -0.4, "calle · NORTE", ha="right", fontsize=7, color="#555"); ax.text(11.9, 17.05, "fondo · SUR", ha="right", fontsize=7, color="#555")
    ax.set_xlim(-0.6, 12.6); ax.set_ylim(-0.9, 17.3); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("PLANTA BAJA" if planta == "PB" else "PLANTA ALTA", fontsize=10, weight="bold")
    return circ, total


IDEAS = ["Suite: se entra desde la sala directamente al vestidor; a la izquierda el baño y a la derecha el dormitorio, arriba, con tres ventanas al fondo.",
         "Cocina de 15 m² con puerta y ventana al fondo y ventana al este. Salón con comedor, sofá en U, pantalla grande y chimenea en el rincón.",
         "Sin oficina abajo: el Dormitorio 3 de arriba (15 m²) puede ser despacho. Arriba sin pasillo: la escalera da a una sala familiar."]

if __name__ == "__main__":
    fig = plt.figure(figsize=(13, 9.5)); fig.suptitle("Distribución propuesta", fontsize=14, weight="bold", x=0.02, ha="left")
    ax1 = fig.add_axes([0.02, 0.10, 0.46, 0.80]); ax2 = fig.add_axes([0.51, 0.10, 0.46, 0.80])
    c1, t1 = dibujar(ax1, PB, PB_DOORS, "PB", PB_OPEN); c2, t2 = dibujar(ax2, PA, PA_DOORS, "PA", PA_OPEN)
    fig.text(0.02, 0.06, "\n".join("• " + t for t in IDEAS), fontsize=8.6, va="top")
    fig.text(0.98, 0.012, f"Circulación: {c1 + c2:.1f} m² · Norte abajo (calle) · sur arriba (fondo) · Medidas orientativas", fontsize=8, va="bottom", ha="right", color="#555")
    fig.savefig("distribucion.png", dpi=110)
    print(f"circulación {c1 + c2:.1f} m²; útil PB {t1:.1f}, PA {t2:.1f}")
