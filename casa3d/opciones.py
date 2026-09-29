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

# ---- puertas: (x, y, 'H'|'V', ancho, extremo_bisagra 0|1, giro +1|-1) ----
FRONT = (7.55, 0.55, "H", 1.40, 1, 1)         # puerta de entrada de 1,40 pegada al muro este, abre hacia dentro
COMMON_PB = [FRONT, (3.35, 9.50, "V", 0.90, 0, -1), (3.60, 11.75, "H", 0.80, 0, 1), (0.90, 11.75, "H", 0.80, 0, 1), (0.90, 13.15, "H", 0.80, 0, 1)]

OPCIONES = {
 "A": dict(
  titulo="Opción A — escalera y baño juntos al final del pasillo",
  ideas=["Al fin del pasillo se llega a una entrada amplia: a la derecha la escalera y, pegado, el baño grande (puerta junto al pie de la escalera).",
         "La sala de estar y comedor es el centro: cocina, oficina y dormitorio principal abren directamente a ella.",
         "Arriba no hay pasillo: la escalera llega a una sala familiar y de ella salen los tres dormitorios."],
  PB=[("Salón", "sala", SALON), ("Pasillo de entrada\n(murete a media altura)", "circ", R(7.55, 0.55, 9.00, 7.87)),
      ("Entrada", "circ", R(7.25, 7.87, 9.00, 8.95)), ("Escalera", "esc", R(7.25, 8.95, 9.00, 11.75)),
      ("Baño grande", "humedo", R(9.10, 8.85, 11.50, 11.25)), ("Sala de estar\ny comedor", "sala", R(3.45, 7.87, 7.15, 11.75)),
      ("Cocina", "cocina", R(5.05, 11.85, 9.00, 15.75)), ("Oficina", "priv", R(3.15, 11.85, 4.95, 15.75)),
      ("Dormitorio\nprincipal", "priv", R(0.55, 7.87, 3.35, 11.75)), ("Vestidor", "priv", R(0.55, 11.85, 3.05, 13.15)),
      ("Baño principal", "humedo", R(0.55, 13.25, 3.05, 15.75))],
  abPB=[(3.55, 7.87, 7.05, 7.87), (7.20, 7.97, 7.20, 8.90)], abPA=[(7.20, 7.97, 7.20, 8.90)],
  doorsPB=COMMON_PB + [(5.30, 11.75, "H", 1.80, 0, 0), (9.05, 9.20, "V", 0.80, 0, 1)],
  PA=[("Terraza sobre el salón", "terraza", SALON), ("Entrada", "circ", R(7.25, 7.87, 9.00, 8.95)), ("Escalera (hueco)", "esc", R(7.25, 8.95, 9.00, 11.75)),
      ("Baño", "humedo", R(9.10, 8.85, 11.50, 11.25)), ("Sala familiar\ny terraza", "sala", R(3.45, 7.87, 7.15, 11.75)),
      ("Dormitorio 1", "priv", R(0.55, 7.87, 3.35, 11.75)), ("Dormitorio 2", "priv", R(0.55, 11.85, 4.95, 15.75)),
      ("Dormitorio 3", "priv", R(5.05, 11.85, 9.00, 15.75))],
  doorsPA=[(3.35, 9.50, "V", 0.90, 0, -1), (3.60, 11.75, "H", 0.80, 0, 1), (5.50, 11.75, "H", 0.80, 0, 1), (9.05, 9.20, "V", 0.80, 0, 1)]),
 "B": dict(
  titulo="Opción B — escalera en el saliente y baño en la entrada",
  ideas=["La escalera pasa al saliente derecho (donde estaba el baño) y arranca justo al llegar desde el pasillo.",
         "El baño queda pegado a la entrada, con puerta desde el mismo recibidor que la escalera.",
         "Sala de estar y comedor más amplia (donde estaba la escalera); resto igual que A."],
  PB=[("Salón", "sala", SALON), ("Pasillo de entrada\n(murete a media altura)", "circ", R(7.55, 0.55, 9.00, 7.87)),
      ("Entrada", "circ", R(7.25, 7.87, 9.00, 9.60)), ("Baño", "humedo", R(7.25, 9.70, 9.00, 11.75)),
      ("Escalera", "esc", R(9.10, 8.85, 11.50, 11.25)), ("Sala de estar\ny comedor", "sala", R(3.45, 7.87, 7.15, 11.75)),
      ("Cocina", "cocina", R(5.05, 11.85, 9.00, 15.75)), ("Oficina", "priv", R(3.15, 11.85, 4.95, 15.75)),
      ("Dormitorio\nprincipal", "priv", R(0.55, 7.87, 3.35, 11.75)), ("Vestidor", "priv", R(0.55, 11.85, 3.05, 13.15)),
      ("Baño principal", "humedo", R(0.55, 13.25, 3.05, 15.75))],
  abPB=[(3.55, 7.87, 7.05, 7.87), (7.20, 7.97, 7.20, 9.55), (9.05, 9.00, 9.05, 9.90)], abPA=[(7.20, 7.97, 7.20, 9.55), (9.05, 9.00, 9.05, 9.90)],
  doorsPB=COMMON_PB + [(5.30, 11.75, "H", 1.80, 0, 0), (7.55, 9.60, "H", 0.80, 0, -1)],
  PA=[("Terraza sobre el salón", "terraza", SALON), ("Entrada", "circ", R(7.25, 7.87, 9.00, 9.60)), ("Baño", "humedo", R(7.25, 9.70, 9.00, 11.75)),
      ("Escalera (hueco)", "esc", R(9.10, 8.85, 11.50, 11.25)), ("Sala familiar\ny terraza", "sala", R(3.45, 7.87, 7.15, 11.75)),
      ("Dormitorio 1", "priv", R(0.55, 7.87, 3.35, 11.75)), ("Dormitorio 2", "priv", R(0.55, 11.85, 4.95, 15.75)),
      ("Dormitorio 3", "priv", R(5.05, 11.85, 9.00, 15.75))],
  doorsPA=[(3.35, 9.50, "V", 0.90, 0, -1), (3.60, 11.75, "H", 0.80, 0, 1), (5.50, 11.75, "H", 0.80, 0, 1), (7.55, 9.60, "H", 0.80, 0, -1)]),
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


def dibujar(ax, rooms, doors, planta, abiertos=()):
    ax.add_patch(MPoly(list(OUT.exterior.coords), closed=True, fc="#8d8d8d", ec="#222", lw=1.6, zorder=1))
    ax.add_patch(MPoly(list(INN.exterior.coords), closed=True, fc="white", ec="none", zorder=2))
    circ = 0; total = 0
    for nombre, tipo, poly in rooms:
        a = area(poly)
        ax.add_patch(MPoly(poly, closed=True, fc=COL[tipo], ec="#222", lw=1.3 if tipo != "terraza" else .8, ls="-" if tipo != "terraza" else "--", zorder=3, hatch="//" if tipo == "esc" else None))
        cx_, cy_ = Polygon(poly).centroid.coords[0]
        pequeno = Polygon(poly).bounds[2] - Polygon(poly).bounds[0] < 2.2
        ax.text(cx_, cy_, f"{nombre}\n{a:.1f} m²", ha="center", va="center", fontsize=6.6 if pequeno else 8, zorder=6, linespacing=1.15)
        if tipo == "circ": circ += a
        if tipo not in ("terraza", "esc"): total += a
    if planta == "PB":
        ax.add_patch(Rectangle((7.45, 0.55), 0.10, 6.77, fc="#666", ec="#222", zorder=4)); ax.text(7.33, 3.6, "murete media altura", rotation=90, ha="right", va="center", fontsize=6.5)
        ax.text(3.6, 7.65, "abierto: salón y comedor", fontsize=6.5, style="italic", zorder=6)
    for (x0, y0, x1, y1) in abiertos: ax.plot([x0, x1], [y0, y1], color="white", lw=5, solid_capstyle="butt", zorder=7)
    for d in doors: door(ax, d)
    ax.set_xlim(-0.6, 12.6); ax.set_ylim(-0.6, 16.9); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("PLANTA BAJA" if planta == "PB" else "PLANTA ALTA", fontsize=10, weight="bold")
    return circ, total


if __name__ == "__main__":
    for k, o in OPCIONES.items():
        fig = plt.figure(figsize=(13, 9.5)); fig.suptitle(o["titulo"], fontsize=14, weight="bold", x=0.02, ha="left")
        ax1 = fig.add_axes([0.02, 0.10, 0.46, 0.80]); ax2 = fig.add_axes([0.51, 0.10, 0.46, 0.80])
        c1, t1 = dibujar(ax1, o["PB"], o["doorsPB"], "PB", o["abPB"]); c2, t2 = dibujar(ax2, o["PA"], o["doorsPA"], "PA", o["abPA"])
        fig.text(0.02, 0.055, "\n".join("• " + t for t in o["ideas"]), fontsize=8.6, va="top")
        fig.text(0.98, 0.055, f"Circulación: {c1 + c2:.1f} m² (PB {c1:.1f} + PA {c2:.1f})\nNorte hacia abajo (supuesto). Medidas orientativas.", fontsize=8.6, va="top", ha="right")
        fig.savefig(f"opcion_{k}.png", dpi=110); plt.close(fig)
        print(k, f"circulación {c1 + c2:.1f} m²; útil PB {t1:.1f}, PA {t2:.1f}")
