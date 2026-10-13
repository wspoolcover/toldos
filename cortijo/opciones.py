"""Distribución propuesta (esquema en planta). Coordenadas del croquis en metros; muros existentes de 0,55 m.
Abajo del croquis = NORTE (acceso por el camino, puerta corredera de 7 m, acometida de agua; entrada y salón); arriba = SUR (fachada ancha con la CGP, hacia la rambla de Albox: cocina y dormitorio principal)."""
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
SALON_PB = [(3.40, 0.25), (7.75, 0.25), (7.75, 7.87), (3.12, 7.87)]
SALON_PA = [(3.40, 0.25), (9.30, 0.25), (9.30, 7.32), (3.12, 7.32)]
HUB = [(3.15, 9.65), (5.65, 9.65), (5.65, 7.87), (7.15, 7.87), (7.15, 11.75), (3.15, 11.75)]
# v8: escalera en U de 17 contrahuellas (huella 22 cm), pie en y = 9,65 (el baño grande y la entrada quedan libres) y meseta al sur, que entra 51 cm en el dormitorio del este
Y0_ESC, T_ESC, X_LANE = 9.65, 0.22, 8.125
LAND = 0.88                                             # fondo de la meseta (>= ancho de cada tramo, 0,875)
Y_FIN = Y0_ESC + 8 * T_ESC + LAND                       # 12,29: fin de la meseta
ESC_PB = R(7.25, Y0_ESC, 9.00, Y_FIN)
Y_HALL_PA = Y0_ESC + T_ESC                              # 9,87: el tramo de bajada tiene 7 huellas y la última contrahuella llega al propio suelo de la planta alta
Y_PAD = Y0_ESC + 5 * T_ESC                              # hasta aquí el suelo de la planta alta cubre los 5 primeros escalones con altura libre de sobra
HUECO_PA = [(7.25, Y_HALL_PA), (X_LANE, Y_HALL_PA), (X_LANE, Y_PAD), (9.00, Y_PAD), (9.00, Y_FIN), (7.25, Y_FIN)]
DORM_E = [(6.25, 11.85), (7.15, 11.85), (7.15, Y_FIN + 0.10), (9.00, Y_FIN + 0.10), (9.00, 15.75), (6.25, 15.75)]

PB = [("Salón con comedor", "sala", SALON_PB, (4.55, 4.15)), ("Pasillo de entrada\n(murete a media altura)", "circ", [(7.85, 0.25), (9.30, 0.25), (9.30, 7.32), (9.00, 7.32), (9.00, 7.87), (7.85, 7.87)]),
      ("Entrada", "circ", R(7.25, 7.87, 9.00, Y0_ESC)), ("Escalera", "esc", ESC_PB, (8.56, 11.85)), ("Baño grande", "humedo", R(9.10, 8.85, 11.50, 11.25)),
      ("Sala de estar\ny paso", "sala", HUB, (5.15, 10.7)), ("Cocina\n(abierta a la sala)", "cocina", R(3.75, 11.85, 6.15, 15.75), (4.95, 13.2)), ("Dormitorio 2", "priv", DORM_E, (7.9, 14.4)), ("Despacho", "priv", R(3.15, 7.97, 5.55, 9.55), (4.6, 8.2)),
      ("Dormitorio principal", "priv", R(0.55, 11.85, 3.65, 15.75), (2.25, 12.55)), ("Vestidor", "priv", R(0.55, 9.45, 3.05, 11.75), (2.0, 10.6)),
      ("Baño", "humedo", R(0.55, 7.87, 3.05, 9.35), (1.85, 9.05))]
PB_DOORS = [(7.85, 0.25, "H", 1.40, 1, 1),            # puerta de entrada de 1,40, pegada al muro este, abre hacia dentro
            (9.05, 8.90, "V", 0.75, 0, 1),             # baño grande, desde la entrada (a la izquierda del pie de la escalera)
            (6.35, 11.75, "H", 0.80, 0, 1),            # sala -> dormitorio 2

            (3.05, 10.20, "V", 0.90, 0, -1),           # de la sala directamente al vestidor
            (1.60, 9.35, "H", 0.80, 0, 0),            # vestidor -> baño (corredera)
            (1.40, 11.75, "H", 0.80, 0, 1),
            (4.35, 9.55, "H", 0.85, 0, 1),             # sala de estar -> despacho
            (3.85, 15.75, "H", 0.90, 0, -1)]           # cocina -> patio sur (puerta de servicio, hacia la rambla)
PB_OPEN = [(5.60, 7.95, 5.60, 9.50), (5.70, 7.87, 7.05, 7.87), (7.20, 7.97, 7.20, 9.55),    # salón <-> sala, y entrada <-> sala (paso libre de 1,58 m)
           (3.85, 11.80, 5.45, 11.80)]                                                                 # sala de estar <-> cocina: paso libre de 1,60 m entre los pilares x=3,10 y x=5,55
VENTANAS = [(0.75, 15.75, 1.10), (2.35, 15.75, 1.10), (5.05, 15.75, 1.00), (6.45, 15.75, 1.00)]      # (x, y de la cara interior del muro, ancho)
VENTANAS_E = []                                                                                         # medianeras este y oeste: sin ventanas
VENTANAS_W = []                                                                      # ventana de cocina al este

PA = [("Terraza sobre el salón", "terraza", SALON_PA), ("Entrada", "circ", R(7.25, 7.87, 9.00, Y_HALL_PA)), ("Escalera (hueco)", "esc", HUECO_PA, (8.15, 11.55)),
      ("Baño", "humedo", R(9.10, 8.85, 10.55, 11.25)), ("Sala familiar\ny terraza", "sala", R(4.05, 7.87, 7.15, 11.75)),
      ("Dormitorio 1", "priv", R(0.55, 7.87, 3.95, 11.75)), ("Dormitorio 2", "priv", R(0.55, 11.85, 4.85, 15.75)),
      ("Dormitorio 3\n(o despacho)", "priv", [(4.95, 11.85), (7.15, 11.85), (7.15, Y_FIN + 0.10), (9.00, Y_FIN + 0.10), (9.00, 15.75), (4.95, 15.75)], (7.0, 14.2))]
PA_DOORS = [(3.95, 9.50, "V", 0.90, 0, -1), (4.05, 11.75, "H", 0.80, 0, -1), (5.80, 11.75, "H", 0.80, 0, 1), (9.05, 8.90, "V", 0.75, 0, 1)]
PA_OPEN = [(7.20, 7.97, 7.20, 9.80)]


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
    r(ax, 3.30, 6.20, 0.85, 1.30, "#d8d0c8"); r(ax, 3.45, 6.45, 0.45, 0.80, "#f4a742"); ax.text(3.75, 5.95, "chimenea", fontsize=6.3, color="#a33", ha="center", va="top", zorder=8)
    r(ax, 5.95, 5.25, 1.00, 2.05, "#e8d5c0")
    for y in (5.4, 6.1, 6.8): r(ax, 5.67, y, .22, .4); r(ax, 7.01, y, .22, .4)
    ax.plot([5.45, 7.45], [4.9, 4.9], color="#a58", lw=.8, ls=":", zorder=6); ax.text(5.5, 5.0, "comedor", fontsize=6.3, color="#a58", va="bottom", zorder=8)
    # suite como la referencia: cama con cabecero al fondo entre mesitas, banco a los pies, escritorio junto a la ventana, vestidor con armarios en L y baño con ducha, inodoro y lavabo doble
    r(ax, 1.65, 13.25, 2.00, 1.60, "#f7b98a"); r(ax, 3.20, 12.78, .42, .42); r(ax, 3.20, 14.90, .42, .42); r(ax, 1.20, 13.55, .38, 1.10, "#e9dcc8")   # cama (cabecero al este), mesitas, banco
    r(ax, 0.60, 13.10, 0.30, 1.30, "#e8d5c0", "||")                                                              # estantería del rincón de lectura
    r(ax, 0.70, 14.55, 0.75, 0.75, "#c7a7d9"); r(ax, 1.05, 15.25, 0.40, 0.40, "#e8d5c0"); ax.text(0.95, 14.40, "rincón de\nlectura", fontsize=5.6, color="#7a3", ha="left", va="top", zorder=12)   # sillón y mesita junto a la ventana
    # despacho íntimo pegado al vestidor: mesa contra el muro del baño, silla, estantería al este y cristal fijo hacia el salón
    r(ax, 3.20, 8.05, 0.60, 1.40, "#e8d5c0"); r(ax, 3.90, 8.45, 0.45, 0.45, "#c7a7d9"); r(ax, 5.22, 8.10, 0.28, 1.35, "#e8d5c0", "||")
    ax.add_patch(Rectangle((3.45, 7.84), 2.0, 0.10, fc="#bfe3f8", ec="#2f8fd0", lw=1.0, zorder=7))   # cristal fijo
    # dormitorio 2 (este): cama de 1,50 con cabecero contra la medianera, mesitas, armario en el rincón junto a la escalera
    r(ax, 7.05, 13.80, 1.95, 1.50, "#f7b98a"); r(ax, 8.60, 13.32, .40, .40); r(ax, 8.60, 15.32, .40, .40); r(ax, 7.40, 12.50, 1.60, 0.60, "#e8d5c0", "||")
    r(ax, 0.55, 9.55, 0.60, 2.10, "#e8d5c0", "||"); r(ax, 2.45, 9.50, 0.60, 0.65, "#e8d5c0", "||")              # vestidor: armarios al oeste y junto a la puerta de la sala; las puertas de la suite y del baño quedan libres
    r(ax, 0.60, 8.42, 0.90, 0.90, "#eef"); r(ax, 1.75, 7.92, 0.40, 0.40); r(ax, 2.50, 7.92, 0.50, 0.65); r(ax, 2.50, 8.62, 0.50, 0.65)   # ducha, inodoro contra el muro norte, doble lavabo contra el muro este: la puerta del vestidor queda libre
    # cocina abierta a la sala: dos hileras paralelas (nevera y columnas contra el tabique de la suite, fuegos al este) y fregadero bajo la ventana
    r(ax, 3.80, 12.40, 0.60, 2.75, "#eadcc4"); r(ax, 5.55, 12.40, 0.60, 2.75, "#eadcc4"); r(ax, 5.05, 15.15, 1.10, 0.60, "#eadcc4")                 # pasillo central de 1,15 m


def escalera(ax, planta):
    """Peldaños de la escalera en U (v8). PB: tramo de subida por el lado este desde y=9,65, meseta al sur y tramo de vuelta por el oeste.
    Bajo el tramo de vuelta (altura libre > 2,05 m hasta y=10,85) queda un rincón con el armario técnico del agua caliente y la aerotermia."""
    if planta == "PB":
        for i in range(9): ax.plot([X_LANE, 9.00], [Y0_ESC + i * T_ESC] * 2, color="#555", lw=.6, zorder=6)
        for j in range(8): ax.plot([7.25, X_LANE], [Y0_ESC + 8 * T_ESC - j * T_ESC] * 2, color="#555", lw=.6, zorder=6, ls=":")
        ax.plot([X_LANE, X_LANE], [Y0_ESC, Y_FIN], color="#555", lw=.6, zorder=6)
        ax.annotate("", xy=(8.56, Y0_ESC + 1.5), xytext=(8.56, Y0_ESC + 0.1), arrowprops=dict(arrowstyle="-|>", color="#222", lw=1), zorder=9); ax.text(8.56, Y0_ESC - 0.12, "SUBE", fontsize=5.8, ha="center", va="top", zorder=9)
        ax.add_patch(Rectangle((7.30, 10.85), 0.75, 1.30, fc="#dcdcdc", ec="#333", lw=.8, zorder=7)); ax.text(7.675, 11.5, "armario\ntécnico", fontsize=4.9, ha="center", va="center", zorder=9)
    else:
        ax.plot([X_LANE, X_LANE, 9.00], [Y_HALL_PA, Y_PAD, Y_PAD], color="#222", lw=2.4, zorder=8, solid_capstyle="butt"); ax.text(8.55, 10.45, "barandilla", fontsize=4.8, ha="center", va="center", zorder=9)


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
    escalera(ax, planta)
    if planta == "PA":
        for (x, y, dx, dy) in ((0.60, 11.15, 2.60, 0.60), (0.60, 11.85, 0.60, 2.40), (4.95, 11.85, 0.60, 2.40)): r(ax, x, y, dx, dy, "#e8d5c0", "||")   # armarios empotrados
        r(ax, 1.3, 8.0, 1.5, 2.0, "#f7b98a"); r(ax, 1.6, 13.3, 1.6, 2.0, "#f7b98a"); r(ax, 6.6, 13.3, 1.6, 2.0, "#f7b98a"); r(ax, 6.30, 9.90, 0.85, 1.20, "#c9b79c")
        ax.add_patch(Rectangle((2.95, 7.32), 6.05, 0.55, fc="#bfe3f8", ec="#2f8fd0", lw=1.0, zorder=6)); ax.add_patch(Rectangle((5.68, 7.32), 1.42, 0.55, fc="white", ec="#2f8fd0", lw=1.0, zorder=7))
        ax.plot([5.68, 5.68 + 0.7], [7.32, 7.32 - 0.5], color="#333", lw=1, zorder=8); ax.plot([7.10, 7.10 - 0.7], [7.32, 7.32 - 0.5], color="#333", lw=1, zorder=8); ax.text(6.4, 7.05, "corredera 1,42 a la terraza", fontsize=5.6, ha="center", va="top", color="#1f6fa8", zorder=9)
    if planta == "PB":
        muebles_pb(ax)
        ax.add_patch(Rectangle((7.75, 0.25), 0.10, 7.07, fc="#666", ec="#222", zorder=4)); ax.text(7.65, 3.6, "murete media altura", rotation=90, ha="right", va="center", fontsize=6.5, zorder=9)
        ax.add_patch(Rectangle((3.55, 0.0), 4.00, 0.25, fc="#bfe3f8", ec="#2f8fd0", lw=1.4, zorder=6))
        ax.text(5.5, -0.15, "cristalera de suelo a techo (4,00 m) junto a la puerta", ha="center", va="top", fontsize=6.6, color="#1f6fa8", zorder=8)
        for (x, y, w) in VENTANAS: ax.add_patch(Rectangle((x, y), w, 0.55 if y > 10 else -0.55, fc="#bfe3f8", ec="#2f8fd0", lw=1.0, zorder=6))
        for (x, y, w) in VENTANAS_W: ax.add_patch(Rectangle((x, y), 0.28, w, fc="#bfe3f8", ec="#2f8fd0", lw=1.0, zorder=6))
        for (x, y, w) in VENTANAS_E: ax.add_patch(Rectangle((x, y), 0.55, w, fc="#bfe3f8", ec="#2f8fd0", lw=1.0, zorder=6))
    for (x0, y0, x1, y1) in abiertos: ax.plot([x0, x1], [y0, y1], color="white", lw=5, solid_capstyle="butt", zorder=7)
    for d in doors: door(ax, d)
    ax.annotate("", xy=(-0.1, -0.6), xytext=(-0.1, 1.6), arrowprops=dict(arrowstyle="-|>", color="#222", lw=1.6), annotation_clip=False)
    ax.text(-0.1, 1.85, "N", ha="center", fontsize=11, weight="bold"); ax.text(11.9, -0.4, "norte · acceso por el camino (puerta corredera de 7 m)", ha="right", fontsize=7, color="#555"); ax.text(11.9, 17.05, "sur · fachada con CGP (hacia la rambla de Albox)", ha="right", fontsize=7, color="#555")
    ax.set_xlim(-0.6, 12.6); ax.set_ylim(-0.9, 17.3); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("PLANTA BAJA" if planta == "PB" else "PLANTA ALTA", fontsize=10, weight="bold")
    return circ, total


IDEAS = ["Suite como la referencia: vestidor con armarios (por eso el dormitorio no lleva armario), baño con ducha, inodoro y lavabo doble, y en el dormitorio un rincón de lectura junto a la ventana. Las puertas del vestidor (suite, baño y sala) quedan libres.",
         "Cocina de 9,4 m² abierta a la sala de estar por un paso libre de 1,60 m entre los pilares (se puede cerrar con una corredera), con puerta de servicio y ventana al patio sur. Las paredes este y oeste son medianeras (casas vecinas pegadas): sin ventanas; los baños se ventilan con extractor. Salón con comedor, sofá en U, pantalla grande y chimenea en la esquina oeste.",
         "Escalera en U de 17 peldaños (19,2 x 22 cm, 87,5 cm de ancho) con el pie junto a la entrada: ya no tapa la cocina ni el baño grande. Bajo el tramo de vuelta queda un paso libre y el armario técnico (agua caliente y aerotermia). Abajo: suite, dormitorio 2 al este y despacho íntimo junto al vestidor; arriba: sala familiar con salida a la terraza y 3 dormitorios."]

if __name__ == "__main__":
    fig = plt.figure(figsize=(13, 9.5)); fig.suptitle("Distribución propuesta", fontsize=14, weight="bold", x=0.02, ha="left")
    ax1 = fig.add_axes([0.02, 0.10, 0.46, 0.80]); ax2 = fig.add_axes([0.51, 0.10, 0.46, 0.80])
    c1, t1 = dibujar(ax1, PB, PB_DOORS, "PB", PB_OPEN); c2, t2 = dibujar(ax2, PA, PA_DOORS, "PA", PA_OPEN)
    import textwrap
    fig.text(0.02, 0.075, "\n".join(textwrap.fill("• " + t, 150, subsequent_indent="  ") for t in IDEAS), fontsize=8.2, va="top")
    fig.text(0.98, 0.955, f"Circulación: {c1 + c2:.1f} m² · Norte abajo (acceso y agua) · sur arriba (CGP, rambla) · Medidas orientativas", fontsize=8, va="top", ha="right", color="#555")
    fig.savefig("distribucion.png", dpi=110)
    for room in PB:
        b=Polygon(room[2]).bounds; print(f"{room[0].splitlines()[0]:22s} {b[2]-b[0]:.2f} x {b[3]-b[1]:.2f} = {area(room[2]):.1f} m²")
    print(f"circulación {c1 + c2:.1f} m²; útil PB {t1:.1f}, PA {t2:.1f}")


def suite_png():
    fig, ax = plt.subplots(figsize=(6.4, 10.4))
    dibujar(ax, PB, PB_DOORS, "PB", PB_OPEN)
    ax.set_aspect("equal", adjustable="box"); ax.set_xlim(0.0, 6.0); ax.set_ylim(7.3, 16.5)
    for txt, xy in (("Escritorio", (0.95, 14.0)), ("Cama 1,60 × 2,00", (3.35, 12.95)), ("Armarios en L", (1.85, 11.95)), ("Ducha", (1.0, 8.2))):
        ax.text(*xy, txt, fontsize=8, color="#7a3", ha="center", weight="bold", zorder=12)
    x0,x1=ax.get_xlim(); y0,y1=ax.get_ylim()
    for t in list(ax.texts)+list(ax.patches)+list(ax.lines):
        try:
            if hasattr(t,"get_position"):
                px,py=t.get_position()
                if not(x0<=px<=x1 and y0<=py<=y1): t.set_visible(False)
            t.set_clip_on(True)
        except Exception: pass
    for t in ax.texts:
        if t.get_text() in ("Escritorio","Ducha","Armarios en L","Cama 1,60 × 2,00"): t.set_visible(False)
    ax.set_title("Suite principal (detalle): dormitorio 12 m², vestidor 5,8 m², baño 3,7 m²", fontsize=11, weight="bold")
    fig.savefig("suite.png", dpi=120, bbox_inches="tight"); plt.close(fig)

if __name__ == "__main__": suite_png()
