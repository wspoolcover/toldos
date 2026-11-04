"""Orden de ejecución de la zanja perimetral por bataches alternos, con los muros que siguen en pie y su zona de peligro (altura del muro, unos 6 m).
Genera cimentacion_bataches.png. Es una guía de trabajo: la secuencia y el apeo los aprueba el técnico."""
import math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from shapely.geometry import LineString, Polygon, box as sbox
from shapely.ops import substring
import opciones as o
from anillos_cimentacion import ANILLO, CIERRE, L_ANILLO, L_CIERRE, pintar

T = 0.55
HOUSE, SB = Polygon(o.NB_FULL), Polygon(o.SB_)
LARGO_BATACHE = 1.5
ALTURA = 6.0
AZ, NA, GRIS, RO = "#1f6fb5", "#d9822b", "#555", "#c0392b"


def tramos():
    """Parte cada lado del anillo en bataches de ≈ 1,5 m y los numera a lo largo del perímetro."""
    out = []
    for s in ANILLO:
        n = max(1, math.ceil(s.length / LARGO_BATACHE))
        for i in range(n):
            out.append(substring(s, s.length * i / n, s.length * (i + 1) / n))
    return out


def main():
    fig, ax = plt.subplots(figsize=(11.5, 10.5))
    ax.set_xlim(-1.5, 15.5); ax.set_ylim(1.2, 17.6); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Zanja perimetral por bataches alternos y muros en pie (guía de trabajo)", fontsize=12, weight="bold", loc="left")
    ax.annotate("", xy=(-0.9, 5.4), xytext=(-0.9, 7.2), arrowprops=dict(arrowstyle="-|>", lw=1.4)); ax.text(-0.9, 7.5, "N", ha="center", fontsize=10, weight="bold")
    pintar(ax, HOUSE.difference(HOUSE.buffer(-T, join_style=2)), fc="#e6e1d6", ec="#222", lw=1, zorder=1)
    # zona de peligro: altura del muro por dentro de los muros que siguen en pie (este y sur) y, por confirmar, oeste
    interior = HOUSE.buffer(-T, join_style=2)
    este = sbox(9.0, 7.3, 9.6, 16.4).buffer(ALTURA).intersection(interior)
    sur = sbox(0, 15.8, 9.6, 16.4).buffer(ALTURA).intersection(interior)
    peligro = este.union(sur)
    pintar(ax, peligro, fc="#f6c9c3", ec="none", alpha=.55, zorder=0.5, hatch="///")
    ax.text(3.2, 10.0, "zona de peligro de los muros en pie\n(la altura del muro, unos 6 m):\nabarca casi toda la casa", fontsize=8.5, color=RO, weight="bold", ha="center", zorder=9,
            bbox=dict(fc="white", ec="none", alpha=.85, pad=2))
    # muros en pie (marca del propietario) y muro oeste por confirmar
    ax.plot([9.275, 9.275], [7.6, 16.0], color=RO, lw=4, alpha=.85, zorder=6, solid_capstyle="butt")
    ax.plot([0.275, 9.275], [16.025, 16.025], color=RO, lw=4, alpha=.85, zorder=6, solid_capstyle="butt")
    ax.plot([0.275, 0.275], [7.6, 16.0], color="#e67e22", lw=4, alpha=.85, ls=(0, (2, 1.2)), zorder=6, solid_capstyle="butt")
    ax.text(9.6, 13.0, "muro este\n(en pie;\nmedianera)", fontsize=7.5, color=RO, weight="bold", va="center")
    ax.text(4.5, 16.5, "muro sur (en pie)", fontsize=7.5, color=RO, weight="bold", ha="center")
    ax.text(-1.3, 12.0, "oeste: por\nconfirmar", fontsize=7.5, color="#e67e22", weight="bold", va="center", ha="left")
    ax.text(3.0, 6.95, "muro norte y muro central: caídos", fontsize=7.5, color=GRIS, ha="center", zorder=9)
    # bataches alternos
    ts = tramos()
    for i, t in enumerate(ts):
        c = NA if i % 2 == 0 else AZ
        pintar(ax, t.buffer(0.2, cap_style=2, join_style=2), fc=c, ec="white", lw=.8, alpha=.9, zorder=5)
        m = t.interpolate(0.5, normalized=True)
        ax.text(m.x, m.y, f"{i // 2 + 1}" if i % 2 == 0 else f"{i // 2 + 1}'", ha="center", va="center", fontsize=6, color="white", weight="bold", zorder=8)
    pintar(ax, CIERRE.buffer(0.2, cap_style=2, join_style=2), fc="#cfd8dc", ec=GRIS, lw=.8, zorder=5)
    ax.text(10.0, 9.9, "cierre del\nsaliente\n(al final)", fontsize=6.8, color=GRIS, ha="left")
    # riostras interiores
    for cy in (7.60, 11.80): ax.add_patch(Rectangle((0.275, cy - 0.2), 9.0, 0.4, fc="#e6d7ef", ec="#7d3c98", lw=.8, zorder=3))
    for lx in (3.10, 5.55, 7.20): ax.add_patch(Rectangle((lx - 0.2, 7.6), 0.4, 4.2, fc="#e6d7ef", ec="#7d3c98", lw=.8, zorder=3))
    ax.text(0.2, 6.2, ("Naranja: 1.ª tanda (1, 2, 3…): se excava, se arma y se hormigona cada batache de ≈ 1,5 m, uno sí y uno no.\n"
                        "Azul: 2.ª tanda (1', 2', 3'…): los huecos que quedan, cuando la 1.ª ha endurecido (plazo, el que fije el técnico).\n"
                        "Nunca hay dos bataches contiguos abiertos. Cada batache se hormigona el mismo día en que se abre.\n"
                        "Antes de abrir uno junto a un muro: cata para ver su zapata; no se baja de la cota de su base; apeo en pie.\n"
                        "La zanja y el hormigón de abajo NO sujetan la parte alta de los muros: eso lo hacen los puntales ahora y el zuncho de arriba después."),
            fontsize=7.6, va="top", color="#222")
    fig.savefig("cimentacion_bataches.png", dpi=130, bbox_inches="tight", facecolor="white")
    print(len(ts), "bataches;", f"{L_ANILLO:.1f} m de zanja; peligro cubre {peligro.area / interior.area * 100:.0f} % del interior")


if __name__ == "__main__":
    main()
