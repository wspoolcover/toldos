"""Zunchos que ya hay en el suelo (croquis del propietario del 27-11-2026): longitudes totales, esquema en planta y hierro que representan según el armado.
Genera cimentacion_zunchos_en_obra.png. El esquema se monta con las cifras del croquis (no está a escala exacta; la posición del zuncho central y las
medidas del saliente son aproximadas)."""
import math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# (nombre, longitud en m, dato): "croquis" = cifra amarilla del propietario; "estimada" = deducida del primer croquis (saliente)
ZUNCHOS = [
    ("Lado sur (E-O)", 9.20, "croquis"),
    ("Zuncho central E-O (llega hasta el saliente)", 11.55, "croquis"),
    ("Lado norte del bloque (E-O)", 9.27, "croquis"),
    ("Lado oeste (N-S)", 8.80, "croquis"),
    ("Zuncho central N-S (4,20 + 4,60)", 8.80, "croquis"),
    ("Lado este (N-S)", 8.90, "croquis"),
    ("Salón, lado oeste", 6.70, "croquis"),
    ("Salón, lado este", 6.70, "croquis"),
    ("Salón, lado norte", 6.30, "croquis"),
    ("Saliente, lado este (N-S)", 3.00, "estimada"),
    ("Saliente, lado norte (E-O)", 2.28, "estimada"),
]
TOTAL = sum(z[1] for z in ZUNCHOS)
TOTAL_CROQUIS = sum(z[1] for z in ZUNCHOS if z[2] == "croquis")
KG = {6: 0.222, 8: 0.395, 12: 0.888, 14: 1.208, 16: 1.578}


def cerco(b, h, rec):
    """Largo de corte de un cerco de una sección b × h (m) con recubrimiento rec por cada lado, más 15 cm de ganchos."""
    return 2 * ((b - 2 * rec) + (h - 2 * rec)) + 0.15


# (descripción, nº de barras, Ø de barra, Ø de cerco, separación de cercos, largo de cada cerco)
ARMADOS = [("lo que parece verse en las fotos: 2Ø12 + 2Ø12, cercos Ø6 cada 25 cm, sección ≈ 25 × 30", 4, 12, 6, 0.25, cerco(0.25, 0.30, 0.03)),
           ("2Ø16 + 2Ø16, cercos Ø8 cada 20 cm, sección ≈ 25 × 30", 4, 16, 8, 0.20, cerco(0.25, 0.30, 0.03)),
           ("el Z-1 del proyecto: 4Ø12 + 4Ø12, cercos Ø8 cada 20 cm, 40 × 30", 8, 12, 8, 0.20, cerco(0.40, 0.30, 0.03)),
           ("el de docs/10: 4Ø16 + 4Ø16, cercos Ø8 cada 15 cm, 40 × 40 con recubrimientos de PL-11", 8, 16, 8, 0.15, 2 * (0.24 + 0.32) + 0.15)]


def kg_por_m(nb, d, dc, sep, largo):
    return nb * KG[d] + (1 / sep) * largo * KG[dc]


def dibujar():
    xm = 4.6                                           # posición aproximada del zuncho central N-S
    fig, ax = plt.subplots(figsize=(10.5, 11.5))
    ax.set_xlim(-1.8, 13.8); ax.set_ylim(17.4, -2.2); ax.set_aspect("equal"); ax.axis("off")      # sur arriba, como en los demás planos
    ax.set_title("Zunchos que hay ahora en el suelo (croquis del 27-11-2026)", fontsize=12, weight="bold", loc="left")
    az, na = "#2e7d32", "#c0392b"

    def tramo(p, q, txt, off=(0, 0), ang=0, est=False):
        ax.plot([p[0], q[0]], [p[1], q[1]], color=az, lw=5, alpha=.55, solid_capstyle="butt", ls=("--" if est else "-"), zorder=3)
        ax.text((p[0] + q[0]) / 2 + off[0], (p[1] + q[1]) / 2 + off[1], txt, ha="center", va="center", fontsize=8.5, color="#a66a00", weight="bold", rotation=ang,
                bbox=dict(fc="white", ec="none", alpha=.85, pad=1.2), zorder=6)
    # bloque principal
    tramo((0, 0), (9.20, 0), "9,20", (0, -0.45))
    tramo((0, 0), (0, 8.80), "8,80", (-0.55, 0), 90)
    tramo((9.20, 0), (9.27, 8.90), "8,90", (0.62, -2.6), 90)
    tramo((0, 8.80), (9.27, 8.90), "9,27", (0, 0.45))
    tramo((0, 4.20), (11.55, 4.20), "11,55", (-2.2, -0.45))
    tramo((xm, 0), (xm, 4.20), "4,20", (-0.5, 0), 90)
    tramo((xm, 4.20), (xm, 8.80), "4,60", (-0.5, 0), 90)
    # salón
    tramo((2.97, 8.85), (2.97, 15.55), "6,70", (-0.55, 0), 90)
    tramo((9.27, 8.90), (9.27, 15.55), "6,70", (0.6, 0), 90)
    tramo((2.97, 15.55), (9.27, 15.55), "6,30  (5,70 entre zunchos)", (0, 0.5))
    # saliente (cifras estimadas)
    tramo((11.55, 4.20), (11.55, 7.20), "≈ 3,00", (0.7, 0), 90, est=True)
    tramo((9.27, 7.20), (11.55, 7.20), "≈ 2,28", (0, 0.45), est=True)
    # marcas X del croquis (esquinas, cruces y mitad de los lados del salón)
    xs = [(0, 0), (xm, 0), (9.20, 0), (0, 4.20), (xm, 4.20), (9.22, 4.20), (0, 8.80), (2.97, 8.82), (9.27, 8.90), (2.97, 12.2), (9.27, 12.2), (2.97, 15.55), (9.27, 15.55)]
    for (x, y) in xs:
        ax.add_patch(Rectangle((x - .25, y - .25), .5, .5, fc="#fff3cd", ec=na, lw=1.6, zorder=7))
        ax.plot([x - .2, x + .2], [y - .2, y + .2], color=na, lw=1.2, zorder=8); ax.plot([x - .2, x + .2], [y + .2, y - .2], color=na, lw=1.2, zorder=8)
    ax.text(6.0, 2.1, "bloque principal", ha="center", fontsize=9, color="#777"); ax.text(6.1, 11.8, "salón", ha="center", fontsize=10, color="#777")
    ax.text(10.4, 5.7, "saliente", ha="center", fontsize=8.5, color="#777")
    ax.text(-1.7, 16.6, (f"Total de zunchos: {TOTAL:.1f} m  ({TOTAL_CROQUIS:.1f} m de cifras del croquis + {TOTAL - TOTAL_CROQUIS:.1f} m estimados del saliente)\n"
                         "Verde: zuncho colocado.  Discontinuo: medida estimada.  Cuadro con X: marca del croquis (¿pilar o «pie»?, 13 marcas).\n"
                         "Esquema montado con las cifras del croquis; la posición del zuncho central N-S es aproximada."), fontsize=8.2, va="top", color="#222")
    fig.savefig("cimentacion_zunchos_en_obra.png", dpi=130, bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    dibujar()
    for n, l, d in ZUNCHOS: print(f"{l:6.2f}  {d:9s} {n}")
    print(f"TOTAL {TOTAL:.2f} m  (croquis {TOTAL_CROQUIS:.2f}, estimados {TOTAL - TOTAL_CROQUIS:.2f})")
    for nombre, nb, dm, dc, sep, largo in ARMADOS:
        k = kg_por_m(nb, dm, dc, sep, largo)
        barras = math.ceil(nb * TOTAL * 1.10 / 12)
        cercos = math.ceil((TOTAL / sep + len(ZUNCHOS)) * 1.05)
        print(f"{nombre}: {k:.1f} kg/m → {k * TOTAL:.0f} kg; {barras} barras de 12 m de Ø{dm}; {cercos} cercos de {largo:.2f} m (Ø{dc})")
