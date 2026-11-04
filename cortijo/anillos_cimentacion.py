"""Plano de los anillos de atado de la cimentación: zanja perimetral de 40 × 40 cm en los muros exteriores de la casa, unida a las riostras RI-1
para que todo quede en recintos cerrados. Genera cimentacion_anillos.png y devuelve las longitudes (las usa pedido_cimentacion.py)."""
import json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch
from matplotlib.path import Path
from shapely.geometry import Polygon, LineString, box as sbox
import opciones as o

E = json.load(open("estructura.json")); LX = E["lineas_x"]; CY = [7.60, 11.80]
T = 0.55; ANCHO = 0.40
HOUSE, SB = Polygon(o.NB_FULL), Polygon(o.SB_)
EJE = HOUSE.buffer(-T / 2, join_style=2)                                  # eje de los muros de 55 cm
pts = list(EJE.exterior.coords)
ys_norte = min(p[1] for p in pts)                                          # lado del muro viejo que se quita entre el salón y la casa
NORTE = LineString([(0.275, ys_norte), (9.275, ys_norte)])
ANILLO = [LineString([pts[i], pts[i + 1]]) for i in range(len(pts) - 1)]
ANILLO = [s for s in ANILLO if not (abs(s.coords[0][1] - ys_norte) < 1e-6 and abs(s.coords[1][1] - ys_norte) < 1e-6)]
L_ANILLO = sum(s.length for s in ANILLO)                                   # lados que no son la riostra de y = 7,60
CIERRE = LineString([(9.275, 8.575), (9.275, 11.525)])                      # boca del saliente: sin muro, cierra el recinto
L_CIERRE = CIERRE.length
L_RIOSTRAS = 2 * (9.55 - T) + 3 * (CY[1] - CY[0])
ZAP, LC = 1.60, (LX[2] - LX[1]) + 1.60
NARANJA, MORADO, AZ, GRIS = "#d9822b", "#7d3c98", "#1f6fb5", "#555"


def pintar(ax, poly, **kw):
    for g in getattr(poly, "geoms", [poly]):
        if g.is_empty: continue
        v, c = [], []
        for ring in [g.exterior] + list(g.interiors):
            p = list(ring.coords); v += p; c += [Path.MOVETO] + [Path.LINETO] * (len(p) - 2) + [Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(v, c), **kw))


def dibujar():
    fig, ax = plt.subplots(figsize=(11.5, 10.5))
    ax.set_xlim(-1.2, 14.8); ax.set_ylim(-1.8, 17.8); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Anillos de atado de la cimentación · zanja perimetral de 40 × 40 cm unida a las riostras", fontsize=12, weight="bold", loc="left")
    ax.annotate("", xy=(-0.5, -1.0), xytext=(-0.5, 1.2), arrowprops=dict(arrowstyle="-|>", lw=1.4)); ax.text(-0.5, 1.5, "N", ha="center", fontsize=10, weight="bold")
    ax.text(6.0, 17.4, "sur · fachada con CGP (hacia la rambla de Albox)", ha="center", fontsize=7.5, color=GRIS)
    ax.text(6.0, -1.5, "norte · acceso por el camino · el salón (abajo) no entra en este anillo", ha="center", fontsize=7.5, color=GRIS)
    pintar(ax, HOUSE.difference(HOUSE.buffer(-T, join_style=2)), fc="#cfcac0", ec="#222", lw=1, zorder=2)
    pintar(ax, SB.difference(SB.buffer(-0.25, join_style=2)), fc="#e8e4dc", ec="#777", lw=.8, zorder=1)
    # recintos cerrados
    recintos = {"R1": (0.275, 7.60, 3.10, 11.80), "R2": (3.10, 7.60, 5.55, 11.80), "R3": (5.55, 7.60, 7.20, 11.80), "R4": (7.20, 7.60, 9.275, 11.80),
                "R5": (0.275, 11.80, 9.275, 16.025), "R6": (9.275, 8.575, 11.775, 11.525)}
    for i, (n, (x0, y0, x1, y1)) in enumerate(recintos.items()):
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc=("#fdf1e3" if i % 2 == 0 else "#eef4fb"), ec="none", zorder=0.5))
        ax.text((x0 + x1) / 2, (y0 + y1) / 2, n, ha="center", va="center", fontsize=11, color="#999", weight="bold", zorder=0.8)
    # riostras RI-1
    for cy in CY: ax.add_patch(Rectangle((0.275, cy - 0.2), 9.0, 0.4, fc="#e6d7ef", ec=MORADO, lw=1.2, zorder=4))
    for lx in LX: ax.add_patch(Rectangle((lx - 0.2, CY[0]), 0.4, CY[1] - CY[0], fc="#e6d7ef", ec=MORADO, lw=1.2, zorder=4))
    # anillo perimetral 40 × 40
    for s in ANILLO + [CIERRE]:
        pintar(ax, s.buffer(ANCHO / 2, cap_style=2, join_style=2), fc="#f7d5a8", ec=NARANJA, lw=1.6, zorder=5)
    # zapatas
    for lx, cy in [(LX[0], c) for c in CY]: ax.add_patch(Rectangle((lx - ZAP / 2, cy - ZAP / 2), ZAP, ZAP, fc="none", ec=AZ, lw=1.4, ls="--", zorder=3))
    for cy in CY: ax.add_patch(Rectangle(((LX[1] + LX[2]) / 2 - LC / 2, cy - ZAP / 2), LC, ZAP, fc="none", ec=AZ, lw=1.4, ls="--", zorder=3))
    for lx in LX:
        for cy in CY: ax.add_patch(Rectangle((lx - .06, cy - .06), .12, .12, fc="#202a44", zorder=6))
    # etiquetas
    ax.text(0.9, 15.3, f"ZANJA PERIMETRAL 40 × 40\n4Ø16 arriba + 4Ø16 abajo, cercos Ø8 cada 15 cm\n{L_ANILLO:.1f} m", fontsize=8, color=NARANJA, weight="bold", bbox=dict(fc="white", ec="none", alpha=.9, pad=1.5), zorder=9)
    ax.annotate(f"cierre del saliente\n{L_CIERRE:.1f} m (no hay muro)", xy=(9.275, 10.0), xytext=(11.0, 6.7), fontsize=7.5, color=NARANJA, arrowprops=dict(arrowstyle="-", color=NARANJA, lw=.8), zorder=9)
    ax.text(4.0, 6.2, "RI-1 riostra 40×50", fontsize=7.5, color=MORADO, weight="bold", bbox=dict(fc="white", ec="none", alpha=.85, pad=1), zorder=9)
    ax.text(9.9, 5.4, "y = 7,60: la riostra hace de\nlado norte del anillo (donde se\nquita el muro viejo)", fontsize=7, color=MORADO, zorder=9)
    ax.text(12.9, 10.0, "casa vecina", rotation=90, fontsize=7, color="#c0392b", va="center")
    ax.text(-1.0, 12.0, "casa vecina", rotation=90, fontsize=7, color="#c0392b", va="center")
    # leyenda
    t = (f"Recintos cerrados R1–R6: cada uno queda rodeado por zanja o riostra.\n"
         f"Zanja perimetral nueva: {L_ANILLO:.1f} m + cierre del saliente {L_CIERRE:.1f} m = {L_ANILLO + L_CIERRE:.1f} m (≈ {(L_ANILLO + L_CIERRE) * ANCHO ** 2:.1f} m³ de hormigón)\n"
         f"Riostras RI-1 que ya estaban: {L_RIOSTRAS:.1f} m.  En cada cruce las barras de la riostra entran 40 cm en el anillo con gancho.\n"
         "Azul discontinuo: zapatas Z-1 y Z-2.  Hormigonar anillo, riostras y zapatas en la misma tanda en cada cruce.")
    ax.text(-1.1, -1.75, t, fontsize=7.8, va="top", color="#222")
    fig.savefig("cimentacion_anillos.png", dpi=130, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    dibujar()
    print(f"anillo {L_ANILLO:.2f} m + cierre {L_CIERRE:.2f} m; riostras {L_RIOSTRAS:.2f} m; lado norte (riostra y = {ys_norte:.3f}) {NORTE.length:.2f} m")
