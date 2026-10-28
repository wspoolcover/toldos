"""Esquema de principio del saneamiento autónomo (fosa séptica + zanjas filtrantes) y comparación con el «pozo ciego».
Cotas orientativas: las define el técnico con el ensayo de infiltración y el nivel freático reales."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, Circle, FancyArrowPatch

VE, MA, GR, AZ, RO, TI = "#2e7d32", "#6d4c41", "#9e9e9e", "#1565c0", "#c62828", "#d7c4a3"


def seccion(ax):
    ax.set_xlim(-1, 41); ax.set_ylim(-5.4, 3.2); ax.axis("off")
    ax.add_patch(Rectangle((-1, -5.2), 42, 5.2, fc=TI, ec="none", alpha=.55, zorder=0))
    ax.plot([-1, 41], [0, 0], color=MA, lw=2, zorder=3)
    # casa
    ax.add_patch(Rectangle((-1, 0), 6.2, 3, fc="#f5f5f5", ec="k", lw=1.2, zorder=3))
    ax.text(2.1, 1.5, "CASA\nbaños y cocina", ha="center", va="center", fontsize=7.5, weight="bold", zorder=4)
    # colector con 2 % de pendiente
    x0, x1 = 3.5, 9.0
    ax.plot([x0, x1], [-0.45, -0.45 - 0.02 * (x1 - x0)], color=VE, lw=2.4, zorder=5)
    ax.text(7.2, -1.0, "colector Ø110–160\npendiente 1–2 %", ha="center", va="top", fontsize=6.3, color=VE)
    # arqueta de registro
    ax.add_patch(Rectangle((9.0, -1.1), 0.9, 1.1, fc="white", ec=VE, lw=1.4, zorder=4))
    ax.text(8.6, 1.6, "arqueta de\nregistro", ha="center", fontsize=6.3, color=VE)
    ax.plot([9.9, 12], [-0.62, -0.62], color=VE, lw=2.4, zorder=5)
    # fosa séptica de dos cámaras
    ax.add_patch(Rectangle((12, -2.3), 5.0, 2.0, fc="#e3f2fd", ec=AZ, lw=1.6, zorder=4))
    ax.plot([14.8, 14.8], [-2.3, -0.8], color=AZ, lw=1.6, zorder=5)
    ax.add_patch(Rectangle((12, -2.3), 2.8, 1.0, fc=AZ, alpha=.25, ec="none", zorder=4))
    ax.add_patch(Rectangle((14.8, -2.3), 2.2, 0.9, fc=AZ, alpha=.15, ec="none", zorder=4))
    ax.add_patch(Rectangle((12.0, -0.3), 5.0, 0.28, fc="#bdbdbd", ec="k", lw=.8, zorder=5))
    ax.text(12.9, 0.55, "FOSA SÉPTICA estanca\n(2 cámaras · 4–5 m³)", ha="center", fontsize=7, color=AZ, weight="bold")
    ax.plot([16.5, 16.5], [-0.3, 1.4], color=GR, lw=2.4, zorder=5); ax.text(16.8, 1.5, "ventilación", fontsize=6, color="#555", ha="left")
    ax.text(13.4, -1.95, "fangos", ha="center", fontsize=5.8, color=AZ)
    ax.text(15.9, -1.8, "agua\nclarificada", ha="center", fontsize=5.8, color=AZ)
    ax.add_patch(Rectangle((12.4, -0.3), 0.6, 0.28, fc="#9e9e9e", ec="k", lw=.8, zorder=5)); ax.text(12.7, -0.55, "tapa", fontsize=5.5, ha="center", va="top")
    # arqueta de reparto
    ax.plot([17.0, 19.2], [-1.1, -1.1], color=VE, lw=2.4, zorder=5)
    ax.add_patch(Rectangle((19.2, -1.6), 0.9, 1.6, fc="white", ec=VE, lw=1.4, zorder=4))
    ax.text(19.65, 0.55, "arqueta de\nreparto", ha="center", fontsize=6.3, color=VE)
    # zanja filtrante (sección longitudinal)
    ax.add_patch(Rectangle((20.1, -1.15), 19.9, 0.85, fc="#bcaaa4", ec=MA, lw=.8, zorder=2))
    ax.add_patch(Rectangle((20.1, -1.15), 19.9, 0.30, fc="#8d6e63", ec="none", alpha=.5, zorder=3))
    ax.plot([20.1, 40], [-1.0, -1.06], color=VE, lw=2.0, zorder=5)
    ax.text(30, 0.45, "ZANJA FILTRANTE (máx. 20 m por zanja)\ntubo drenante en grava, 0,6 m de fondo", ha="center", fontsize=7, color=MA, weight="bold")
    # nivel freático
    ax.plot([-1, 41], [-3.7, -3.7], color=AZ, lw=1.2, ls="--"); ax.text(40.8, -3.55, "nivel freático (en época de lluvias)", ha="right", va="bottom", fontsize=6.3, color=AZ)
    ax.annotate("", xy=(26, -3.7), xytext=(26, -1.15), arrowprops=dict(arrowstyle="<->", color=RO, lw=1.1))
    ax.text(26.4, -2.5, "≥ 1,2 m", fontsize=6.5, color=RO, weight="bold")
    # flujo
    ax.annotate("", xy=(20.0, -2.75), xytext=(3.0, -2.75), arrowprops=dict(arrowstyle="->", color="#555", lw=1))
    ax.text(11.5, -3.0, "el agua va por gravedad: la fosa y las zanjas tienen que quedar más bajas que la casa", ha="center", va="top", fontsize=6.3, color="#555")
    ax.text(20, -4.9, "el terreno acaba el trabajo: la tierra y los microbios de la capa de arriba depuran el agua", ha="center", fontsize=6.6, color=MA, style="italic")
    ax.set_title("SECCIÓN · recorrido del agua", fontsize=9, weight="bold", loc="left")


def planta(ax):
    ax.set_xlim(-2, 30); ax.set_ylim(-4, 17); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((-2, -4), 32, 21, fc=TI, ec="none", alpha=.35, zorder=0))
    ax.add_patch(Rectangle((0, 10), 9.5, 6.5, fc="#f5f5f5", ec="k", lw=1.3, zorder=3)); ax.text(4.75, 13.2, "CASA", ha="center", va="center", weight="bold", fontsize=8)
    ax.add_patch(Rectangle((12, 11.2), 4.2, 2.2, fc="#e3f2fd", ec=AZ, lw=1.5, zorder=3)); ax.text(14.1, 12.3, "fosa", ha="center", va="center", fontsize=7, color=AZ, weight="bold")
    ax.plot([9.5, 12], [12.3, 12.3], color=VE, lw=2.2)
    ax.plot([16.2, 18.2], [12.3, 12.3], color=VE, lw=2.2); ax.add_patch(Rectangle((18.2, 11.9), .8, .8, fc="white", ec=VE, lw=1.3, zorder=4))
    ax.text(18.6, 13.3, "reparto", ha="center", fontsize=6, color=VE)
    # 4 zanjas de 20 m con 1,8 m de separación
    ys = [9.3, 7.5, 5.7, 3.9]
    ax.plot([18.6, 18.6], [12.3, ys[-1]], color=VE, lw=2.0)
    ax.text(23.5, 2.2, "4 zanjas × 20 m = 80 m\nen una banda de 20 × 6 m (≈ 120 m²)\nmín. 2 zanjas · 1,8 m entre ejes", fontsize=6.8, color=MA, ha="center", va="top")
    for y in ys:
        ax.add_patch(Rectangle((19.0, y - 0.3), 11, 0.6, fc="#bcaaa4", ec=MA, lw=.8, zorder=2))
        ax.plot([18.6, 30], [y, y], color=VE, lw=1.6, zorder=4)
    # distancias
    ax.annotate("", xy=(30, 9.3), xytext=(30, 3.9), arrowprops=dict(arrowstyle="<->", lw=.9, color="#555"))
    ax.text(30.2, 6.6, "1,8", fontsize=6, va="center", rotation=90)
    # olivo
    for (x, y) in [(8, 4.5), (13, 0.5)]:
        ax.add_patch(Circle((x, y), 1.0, fc="#a5d6a7", ec=VE, lw=1, zorder=3))
    ax.text(8, 3.3, "olivo (≥ 3 m)", ha="center", va="top", fontsize=6, color=VE)
    # pozo de agua
    ax.add_patch(Circle((5, -1.5), 0.6, fc="#90caf9", ec=AZ, lw=1.2, zorder=3)); ax.text(6.0, -1.5, "pozo de agua\n(≥ 15 m)", fontsize=6, color=AZ, va="center")
    # lindero
    ax.plot([-2, 30], [-3.2, -3.2], color="k", lw=1.2, ls="-."); ax.text(-1.8, -2.9, "lindero (≥ 1,5 m)", fontsize=6)
    ax.annotate("", xy=(16, -3.2), xytext=(16, 1.1), arrowprops=dict(arrowstyle="<->", lw=.9, color=RO)); ax.text(16.2, -1, "≥ 1,5 m", fontsize=6.3, color=RO)
    ax.set_title("PLANTA · ejemplo de zanjas filtrantes", fontsize=9, weight="bold", loc="left")


def detalle(ax):
    ax.set_xlim(-0.5, 5.8); ax.set_ylim(-0.3, 4.9); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 3.0, 3.8, fc="#d7ccc8", ec=MA, lw=1.2))
    ax.add_patch(Rectangle((0.15, 0.15), 2.7, 2.0, fc="#b0bec5", ec="#546e7a", lw=.8)); ax.text(1.5, 0.7, "grava 20–32 mm", ha="center", fontsize=6.5)
    ax.add_patch(Circle((1.5, 1.8), 0.32, fc="white", ec=VE, lw=1.6)); ax.text(1.5, 1.8, "Ø100", ha="center", va="center", fontsize=5.5, color=VE)
    ax.plot([0.15, 2.85], [2.15, 2.15], color="#2e2e2e", lw=1.6); ax.text(1.5, 2.28, "geotextil", ha="center", fontsize=6)
    ax.add_patch(Rectangle((0.15, 2.18), 2.7, 1.45, fc="#8d6e63", alpha=.6, ec="none")); ax.text(1.5, 3.0, "tierra\n(≈ 30 cm)", ha="center", fontsize=6.5)
    ax.annotate("", xy=(3.35, 0), xytext=(3.35, 3.8), arrowprops=dict(arrowstyle="<->", lw=.9)); ax.text(3.5, 1.9, "0,6 m", fontsize=6.5, rotation=90, va="center")
    ax.annotate("", xy=(0, -0.2), xytext=(3.0, -0.2), arrowprops=dict(arrowstyle="<->", lw=.9)); ax.text(1.5, -0.3, "0,6 m", fontsize=6.5, ha="center", va="top")
    ax.text(4.1, 4.0, "tubo con 2 líneas de\norificios hacia abajo", fontsize=5.8, color=VE, va="top")
    ax.set_title("detalle de la zanja", fontsize=8, weight="bold", loc="left")


def pozo():
    """Pozo filtrante de 5 m con anillos de hormigón perforados (Ø interior 1,5 m como ejemplo) y tabla de diámetros."""
    fig = plt.figure(figsize=(14, 8.4), dpi=110)
    ax = fig.add_axes([0.02, 0.05, 0.50, 0.85]); ax.set_xlim(-4.2, 4.8); ax.set_ylim(-6.1, 1.9); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((-4.2, -6.1), 9, 6.1, fc=TI, ec="none", alpha=.55))
    ax.plot([-4.2, 4.8], [0, 0], color=MA, lw=2)
    R, e, g = 0.75, 0.18, 0.40          # radio interior, pared, corona de grava
    # excavación y grava
    ax.add_patch(Rectangle((-(R + e + g), -5.5), 2 * (R + e + g), 5.5, fc="#cfd8dc", ec=MA, lw=1, ls="--", zorder=1))
    # anillos
    for i in range(5):
        z1, z0 = -i, -i - 1
        perf = i >= 1
        for s in (-1, 1):
            ax.add_patch(Rectangle((s * R if s > 0 else -(R + e), z0), e, 1, fc="#bdbdbd" if not perf else "#a1887f", ec="k", lw=1, zorder=3))
        if perf:
            for s in (-1, 1):
                xc = s * (R + e / 2)
                for dz in (0.25, 0.75):
                    ax.add_patch(Circle((xc, z0 + dz), 0.05, fc="white", ec="k", lw=.6, zorder=4))
        ax.text(0, z0 + 0.5, f"anillo {i + 1}" + (" · liso" if not perf else " · perforado"), ha="center", va="center", fontsize=7, zorder=5)
    # fondo de grava
    ax.add_patch(Rectangle((-(R + e + g), -5.5), 2 * (R + e + g), 0.5, fc="#b0bec5", ec="none", zorder=2)); ax.text(0, -5.25, "grava 0,5 m (sin solera)", ha="center", fontsize=6.5)
    ax.text(-(R + e + g) - 0.15, -3.0, "grava 40–80 mm\n+ geotextil\n(corona de 0,4 m)", fontsize=6.5, color="#37474f", ha="right", va="center")
    # losa
    ax.add_patch(Rectangle((-(R + e + 0.35), 0.0), 2 * (R + e + 0.35), 0.22, fc="#9e9e9e", ec="k", lw=1.1, zorder=6)); ax.add_patch(Rectangle((-0.3, 0.22), 0.6, 0.12, fc="#616161", ec="k", zorder=6))
    ax.text(0, 0.75, "losa de cierre con boca Ø 60 cm y tapa", ha="center", fontsize=7)
    # entrada
    ax.plot([-4.2, -(R + e)], [-0.75, -0.75], color=VE, lw=3, zorder=7); ax.text(-4.1, -0.5, "desde la fosa\n(agua ya decantada)", fontsize=6.5, color=VE)
    # medidas
    ax.annotate("", xy=(R + e + g + .55, -5.0), xytext=(R + e + g + .55, 0), arrowprops=dict(arrowstyle="<->", color=RO, lw=1.2)); ax.text(R + e + g + .7, -2.6, "≈ 5 m", fontsize=8, color=RO, weight="bold", rotation=90, va="center")
    ax.annotate("", xy=(R + e + g + 1.1, -5.0), xytext=(R + e + g + 1.1, -1.0), arrowprops=dict(arrowstyle="<->", color=AZ, lw=1.0)); ax.text(R + e + g + 1.25, -3.0, "4 m perforados\n(los que infiltran)", fontsize=6.5, color=AZ, va="center", rotation=90)
    ax.annotate("", xy=(-R, -5.9), xytext=(R, -5.9), arrowprops=dict(arrowstyle="<->", lw=1)); ax.text(0, -6.05, "Ø interior 1,5 m (ejemplo)", ha="center", va="top", fontsize=7)
    ax.annotate("", xy=(0, -5.0), xytext=(0, -5.0))
    ax.plot([-4.2, 4.8], [-5.9 - 0.0, -5.9 - 0.0], alpha=0)
    ax.set_title("POZO FILTRANTE de 5 m con anillos de hormigón · sección", fontsize=9.5, weight="bold", loc="left")
    # tabla
    tx = fig.add_axes([0.54, 0.05, 0.45, 0.85]); tx.axis("off"); tx.set_xlim(0, 1); tx.set_ylim(0, 1)
    tx.text(0, 1, "Qué diámetro y cuánto necesita infiltrar", fontsize=10, weight="bold", va="top")
    cab = ["Ø interior\nanillo", "peso aprox.\n1 anillo de 1 m", "pared filtrante\n(4 m)", "tasa mínima del terreno\n1.200 L/d · 1.500 L/d"]
    filas = [("1,2 m", "≈ 1,6 t", "15 m²", "80 · 100 L/m²·d"),
             ("1,5 m", "≈ 2,3 t", "19 m²", "64 · 80 L/m²·d"),
             ("1,8 m", "≈ 2,9 t", "23 m²", "53 · 66 L/m²·d"),
             ("2,0 m", "≈ 3,3 t", "25 m²", "48 · 60 L/m²·d")]
    xs = [0.0, 0.2, 0.42, 0.62]
    for x, c in zip(xs, cab):
        tx.text(x, 0.92, c, fontsize=7.4, weight="bold", va="top")
    for i, f in enumerate(filas):
        y = 0.80 - i * 0.075
        tx.plot([0, 1], [y + 0.04, y + 0.04], color="#bbb", lw=.6)
        for x, c in zip(xs, f):
            tx.text(x, y, c, fontsize=8, va="center")
    tx.text(0, 0.47, ("Cómo leerlo\n"
                      "• Caudal de la casa: 8–10 personas × 150 L = 1.200–1.500 L/día.\n"
                      "• Valores de diseño habituales para el terreno: 18–48 L/m²·día\n"
                      "   (de «lento pero válido» a «muy permeable»).\n"
                      "• Con un solo pozo de 5 m solo se llega si el terreno es muy\n"
                      "   permeable (grava o arena). Con limo o arcilla no hay\n"
                      "   diámetro que lo arregle: harían falta más pozos o zanjas.\n"
                      "• Pesos: estimados con la pared del anillo de 16–20 cm; el\n"
                      "   dato de partida es un catálogo de precios: Ø 1,2 m, 16 cm,\n"
                      "   1 m de alto = 1.600 kg. El fabricante da el peso exacto.\n"
                      "• 5 m de profundidad = 5 anillos de 1 m + losa. El primero\n"
                      "   va liso; los otros cuatro, perforados."), fontsize=7.6, va="top", linespacing=1.4)
    fig.suptitle("Pozo filtrante: diámetro, número de anillos y qué tiene que cumplir el terreno", fontsize=11, weight="bold", y=0.98)
    fig.savefig("pozo_filtrante_5m.png", bbox_inches="tight", facecolor="white")


def main():
    pozo()
    fig = plt.figure(figsize=(15, 9.6), dpi=110)
    gs = fig.add_gridspec(2, 3, width_ratios=[1.35, 1, 0.55], height_ratios=[1, 0.74], hspace=0.12, wspace=0.05)
    seccion(fig.add_subplot(gs[0, 0:2]))
    planta(fig.add_subplot(gs[1, 0:2]))
    detalle(fig.add_subplot(gs[1, 2]))
    ax = fig.add_subplot(gs[0, 2]); ax.axis("off")
    ax.text(0, 1, "Qué es cada cosa", fontsize=10, weight="bold", va="top")
    t = ("FOSA SÉPTICA\nTanque cerrado y estanco. Aquí los sólidos se hunden y se\ndescomponen en parte. Sale agua turbia, todavía sucia.\n\n"
         "ZANJAS FILTRANTES\nTubo agujereado enterrado en grava poco profundo. El agua se\nfiltra por el fondo y la capa viva del suelo la depura.\n\n"
         "POZO FILTRANTE\nPozo con las paredes agujereadas. Hace lo mismo que las zanjas,\npero más hondo (más cerca del agua subterránea).\n\n"
         "POZO CIEGO / NEGRO\nPozo sin tratamiento previo: todo va directo al terreno.\nEs lo que el cortijo antiguo tenía y lo que hoy no se\nautoriza para una vivienda nueva.\n\n"
         "DEPÓSITO ESTANCO\nTanque cerrado sin salida: un camión lo vacía.\nSin vertido, pero con coste fijo cada mes.")
    ax.text(0, 0.93, t, fontsize=7.2, va="top", linespacing=1.35)
    fig.suptitle("Saneamiento autónomo del cortijo · esquema de principio (cotas a definir con el ensayo de infiltración y el técnico)", fontsize=11, weight="bold", y=0.98)
    fig.savefig("fosa_septica_esquema.png", bbox_inches="tight", facecolor="white")


if __name__ == "__main__":
    main()
