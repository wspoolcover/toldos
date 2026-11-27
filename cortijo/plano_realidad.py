"""Plano en limpio de lo que dibuja el propietario (croquis del 27-11-2026): zunchos, muros por espesor y tabiques de 7 cm.
Genera plano_realidad_27nov.png. Esquema montado con las cifras del croquis; las posiciones de los tabiques interiores son aproximadas y las de los huecos no están."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly
from shapely.geometry import LineString

XM = 4.4                       # zuncho central N-S y tabique entre b1 y cocina (posición aproximada)
YC = 4.20                      # muro central E-O
# (nombre, puntos, espesor en m)
MUROS = [
    ("sur", [(0, 0), (9.20, 0)], 0.14), ("oeste", [(0, 0), (0, 8.80)], 0.14), ("este, tramo sur", [(9.20, 0), (9.22, 4.10)], 0.14),
    ("saliente, este", [(11.55, YC), (11.55, 7.20)], 0.14),
    ("central E-O", [(0, YC), (11.55, YC)], 0.29), ("norte, al oeste del salón", [(0, 8.80), (2.97, 8.82)], 0.29),
    ("salón, oeste", [(2.97, 8.85), (2.97, 15.55)], 0.29), ("salón, este", [(9.27, 8.90), (9.27, 15.55)], 0.29),
    ("este, entre saliente y salón", [(9.26, 7.20), (9.27, 8.90)], 0.29), ("saliente, norte", [(9.26, 7.20), (11.55, 7.20)], 0.29),
]
TABIQUES = [("b1 | cocina", [(XM, 0.07), (XM, YC - 0.14)]),
            ("fila larga (400)", [(0.14, 6.1), (4.0, 6.1)]), ("fila larga (400)", [(0.14, 7.5), (4.0, 7.5)]), ("fila larga (400)", [(4.0, 6.1), (4.0, 7.5)]),
            ("recinto central", [(4.0, 5.0), (5.9, 5.0)]), ("recinto central", [(5.9, 5.0), (5.9, 8.65)]), ("recinto central", [(4.0, 5.0), (4.0, 8.65)])]
ZUNCHOS = [[(0, 0), (9.20, 0)], [(0, 0), (0, 8.80)], [(9.20, 0), (9.27, 8.90)], [(0, 8.80), (9.27, 8.90)], [(0, YC), (11.55, YC)], [(XM, 0), (XM, 8.80)],
           [(2.97, 8.85), (2.97, 15.55)], [(9.27, 8.90), (9.27, 15.55)], [(2.97, 15.55), (9.27, 15.55)], [(11.55, YC), (11.55, 7.20)], [(9.27, 7.20), (11.55, 7.20)]]


def banda(ax, pts, esp, **kw):
    g = LineString(pts).buffer(esp / 2, cap_style=2, join_style=2)
    ax.add_patch(MPoly(list(g.exterior.coords), closed=True, **kw))


def main():
    fig, ax = plt.subplots(figsize=(10.5, 11.5))
    ax.set_xlim(-1.5, 13.5); ax.set_ylim(17.2, -2.2); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Lo que dibuja el propietario (27-11-2026): zunchos, muros y tabiques", fontsize=12, weight="bold", loc="left")
    for z in ZUNCHOS: banda(ax, z, 0.30, fc="#a5d6a7", ec="none", alpha=.8, zorder=1)
    for n, p, e in MUROS:
        if e == 0.14: banda(ax, p, e, fc="#e3edff", ec="#1a3fbf", hatch="////", lw=.8, zorder=3)
        else: banda(ax, p, e, fc="#1a3fbf", ec="#1a3fbf", lw=.8, zorder=3)
    for n, p in TABIQUES: banda(ax, p, 0.07, fc="white", ec="#4f6fd8", lw=1.0, zorder=4)
    ax.plot([2.97, 9.27], [15.55, 15.55], color="#1a3fbf", lw=1.2, ls="--", zorder=4)
    ax.text(6.1, 15.95, "lado norte del salón: sin marcar", ha="center", fontsize=7.8, color="#1a3fbf")
    ax.text(2.1, 2.1, "b1", fontsize=13, ha="center", color="#333", weight="bold"); ax.text(6.9, 2.1, "Cocina", fontsize=13, ha="center", color="#333", weight="bold")
    ax.text(2.0, 6.8, "400", fontsize=10, ha="center", color="#333"); ax.text(4.95, 6.8, "¿?", fontsize=12, ha="center", color="#333")
    ax.text(6.1, 11.8, "salón", ha="center", fontsize=11, color="#777"); ax.text(10.3, 5.7, "saliente", ha="center", fontsize=8, color="#777")
    ax.text(7.6, 6.2, "(abierto)", ha="center", fontsize=8, color="#777")
    ax.text(-1.4, 16.8, ("Hatch azul claro: ladrillo de 14 cm.   Azul macizo: ladrillo de 29 cm.   Fino con borde: ladrillo de 7 cm.   Verde: zuncho.\n"
                         "b1 y Cocina: etiquetas del croquis. «400»: el rectángulo largo mide 4,00 m. «¿?»: recinto de tabique de 7 cm sin etiqueta (¿escalera o baño?).\n"
                         "Esquema con las cifras del croquis: las posiciones de los tabiques son aproximadas y faltan los huecos (puertas y ventanas)."), fontsize=8, va="top", color="#222")
    fig.savefig("plano_realidad_27nov.png", dpi=130, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
