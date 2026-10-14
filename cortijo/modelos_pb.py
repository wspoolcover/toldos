"""Tres modelos de planta baja (A, B, C) con los cambios pedidos el 14-10-2026:
cocina más amplia con salida acristalada de aluminio al exterior, puerta del vestidor pegada al dormitorio (bisagra a la derecha, puerta de seguridad),
muros y accesos de dormitorios reforzados (hormigón/bloque armado de 15 cm, puertas RC3), dormitorio 2 más pequeño (o sin él) y asientos en las ventanas del sur.
Salón, pasillo, entrada, escalera, sala de estar, despacho y baño grande son los de la v8. Se dibujan solo las plantas bajas; el modelo 3D se hace con el que elijas.
Uso: python modelos_pb.py  ->  modelo_A_planta_baja.png, modelo_B_..., modelo_C_..., modelos_planta_baja.png"""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle, Circle
from shapely.geometry import Polygon
import opciones as o
from opciones import R, door, escalera, COL, OUT, INN, HUB, SALON_PB, ESC_PB, Y0_ESC, Y_FIN

NY = Y_FIN + 0.10                                   # 12,39: tabique sur del cierre de la escalera
MADERA, TELA, CAMA, PIEDRA = "#e8d5c0", "#c9b79c", "#f7b98a", "#cfc8bd"
VIDRIO, VIDRIO_EC = "#bfe3f8", "#2f8fd0"

# ---------------------------------------------------------------- piezas comunes (norte y zona de la suite)
COMUN = [("Salón con comedor", "sala", SALON_PB, (4.55, 4.15)), ("Pasillo de entrada\n(murete a media altura)", "circ", [(7.85, 0.25), (9.30, 0.25), (9.30, 7.32), (9.00, 7.32), (9.00, 7.87), (7.85, 7.87)]),
         ("Entrada", "circ", R(7.25, 7.87, 9.00, Y0_ESC)), ("Escalera", "esc", ESC_PB, (8.56, 11.85)), ("Baño grande", "humedo", R(9.10, 8.85, 11.50, 11.25)),
         ("Sala de estar\ny paso", "sala", HUB, (5.15, 10.7)), ("Despacho", "priv", R(3.15, 7.97, 5.55, 9.55), (4.6, 8.2)),
         ("Dormitorio principal", "priv", R(0.55, 11.90, 3.65, 15.75), (2.15, 12.6)), ("Vestidor", "priv", R(0.55, 9.45, 3.00, 11.75), (1.75, 10.55)), ("Baño", "humedo", R(0.55, 7.87, 3.00, 9.35), (1.85, 9.05))]
PUERTAS_COMUN = [(7.85, 0.25, "H", 1.40, 1, 1),            # entrada de 1,40 desde el pasillo
                 (9.05, 8.90, "V", 0.75, 0, 1),            # baño grande, desde la entrada
                 (4.35, 9.55, "H", 0.85, 0, 1),            # sala -> despacho
                 (1.60, 9.35, "H", 0.80, 0, 0),            # vestidor -> baño (corredera empotrada)
                 (1.40, 11.75, "H", 0.90, 0, 1),           # vestidor -> dormitorio principal: puerta de seguridad
                 (3.00, 10.78, "V", 0.90, 1, -1)]          # sala -> vestidor: pegada al dormitorio, bisagra a la derecha al entrar (lado sur), abre hacia dentro; puerta de seguridad
ABIERTOS_COMUN = [(5.60, 7.95, 5.60, 9.50), (5.70, 7.87, 7.05, 7.87), (7.20, 7.97, 7.20, 9.55)]
SEG_COMUN = [(3.00, 7.87, 3.15, 11.75), (3.65, 11.90, 3.80, 15.75)]          # pared del vestidor hacia la sala y pared de la suite hacia la cocina o el dormitorio 2


def rect(ax, x, y, dx, dy, fc="#fff", hatch=None, z=5, lw=.8): ax.add_patch(Rectangle((x, y), dx, dy, fc=fc, ec="#333", lw=lw, hatch=hatch, zorder=z))
def txt(ax, x, y, s, fs=5.6, color="#333", ha="center", va="center", rot=0): ax.text(x, y, s, fontsize=fs, color=color, ha=ha, va=va, rotation=rot, zorder=12, linespacing=1.1)


def cama(ax, x, y, w, l, cabecera="n"):
    """Cama en planta: colchón, almohadas en la cabecera (n/s/e/o) y pie doblado."""
    rect(ax, x, y, w, l, CAMA)
    n = 2 if (w if cabecera in "ns" else l) > 1.2 else 1
    for k in range(n):
        if cabecera == "n": rect(ax, x + .08 + k * (w - .16) / n, y + .06, (w - .16) / n - .05, .30, "#fff", z=6)
        elif cabecera == "s": rect(ax, x + .08 + k * (w - .16) / n, y + l - .36, (w - .16) / n - .05, .30, "#fff", z=6)
        elif cabecera == "e": rect(ax, x + w - .36, y + .08 + k * (l - .16) / n, .30, (l - .16) / n - .05, "#fff", z=6)
        else: rect(ax, x + .06, y + .08 + k * (l - .16) / n, .30, (l - .16) / n - .05, "#fff", z=6)


def silla(ax, x, y, d=.40): ax.add_patch(Rectangle((x - d / 2, y - d / 2), d, d, fc="#d9b98f", ec="#555", lw=.6, zorder=6))
def mesa(ax, x, y, w, h, sillas=()):
    rect(ax, x, y, w, h, "#d9b98f", z=6)
    for (sx, sy) in sillas: silla(ax, sx, sy)


def asiento_ventana(ax, x, w, y0=15.75, prof=0.42):
    """Hueco de asiento en el muro de 55 cm: banco de obra de 45 cm de altura con cojín y la ventana pegada al exterior."""
    rect(ax, x, y0, w, prof, "#e9d7bd", z=6, lw=.9)
    ax.add_patch(Rectangle((x + .06, y0 + .06), w - .12, prof - .12, fc="#b9a07c", ec="none", alpha=.55, zorder=7))
    ax.add_patch(Rectangle((x, y0 + prof), w, 0.07, fc=VIDRIO, ec=VIDRIO_EC, lw=1.0, zorder=8))
    ax.add_patch(Rectangle((x, y0 + prof + .07), w, .06, fc="#555", ec="none", zorder=7))
    txt(ax, x + w / 2, y0 + prof / 2, "asiento", 4.8, "#6a4d2a")


def ventana(ax, x, w, y0=15.75):
    ax.add_patch(Rectangle((x, y0), w, 0.55, fc=VIDRIO, ec=VIDRIO_EC, lw=1.0, zorder=6))


def corredera_aluminio(ax, x, w, y0=15.75):
    """Salida acristalada de aluminio al patio sur: dos o tres hojas correderas de suelo a techo."""
    ax.add_patch(Rectangle((x, y0), w, 0.55, fc="#d6eefc", ec=VIDRIO_EC, lw=1.4, zorder=6))
    n = 3 if w > 2.0 else 2
    for k in range(n): ax.plot([x + k * w / n, x + (k + 1) * w / n], [y0 + .15 + .12 * (k % 2), y0 + .15 + .12 * (k % 2)], color="#0b4f7a", lw=1.4, zorder=8)
    txt(ax, x + w / 2, y0 + .78, f"corredera de aluminio {w:.2f} m".replace(".", ","), 5.0, "#1f6fa8", va="bottom")


def encimera(ax, x, y, dx, dy, nombre=None):
    rect(ax, x, y, dx, dy, "#eadcc4", z=6)
    if nombre: txt(ax, x + dx / 2, y + dy / 2, nombre, 4.6, "#6a4d2a", rot=90 if dy > dx else 0)


def muebles_comunes(ax, despacho_h=True):
    # salón: sofá en U, mesa baja, pantalla, chimenea y comedor
    rect(ax, 6.75, 1.05, .75, 3.30, TELA); rect(ax, 5.35, 3.65, 1.40, .70, TELA); rect(ax, 5.35, 1.05, 1.40, .70, TELA); rect(ax, 5.65, 2.05, .80, 1.35, "#efe6d6")
    rect(ax, 3.60, 1.60, .16, 1.90, "#222"); txt(ax, 3.98, 3.60, "pantalla", 6.3, ha="left", va="bottom")
    rect(ax, 3.30, 6.20, .85, 1.30, "#d8d0c8"); rect(ax, 3.45, 6.45, .45, .80, "#f4a742"); txt(ax, 3.75, 5.95, "chimenea", 6.3, "#a33", va="top")
    mesa(ax, 5.95, 5.25, 1.00, 2.05, [(5.78, y) for y in (5.6, 6.3, 7.0)] + [(7.12, y) for y in (5.6, 6.3, 7.0)])
    # despacho íntimo y cristal fijo hacia el salón (versión horizontal de la v8)
    if despacho_h:
        rect(ax, 3.20, 8.05, .60, 1.40, MADERA); silla(ax, 4.10, 8.65); rect(ax, 5.22, 8.10, .28, 1.35, MADERA, "||")
        ax.add_patch(Rectangle((3.45, 7.84), 2.0, 0.10, fc=VIDRIO, ec=VIDRIO_EC, lw=1.0, zorder=7))
    # vestidor: armarios al oeste y junto a la puerta de la sala; puertas libres
    rect(ax, 0.55, 9.55, .60, 2.10, MADERA, "||"); rect(ax, 2.40, 9.50, .60, .65, MADERA, "||")
    # baño de la suite: ducha, inodoro contra el muro norte y doble lavabo contra el muro este
    rect(ax, .60, 8.42, .90, .90, "#eef"); rect(ax, 1.75, 7.92, .40, .40); rect(ax, 2.45, 7.92, .50, .65); rect(ax, 2.45, 8.62, .50, .65)
    # suite: cama con cabecero al este, mesitas, banco a los pies, estantería y asiento de lectura en la ventana
    cama(ax, 1.65, 13.25, 2.00, 1.60, "e"); rect(ax, 3.20, 12.75, .42, .42); rect(ax, 3.20, 14.95, .42, .42); rect(ax, 1.20, 13.55, .38, 1.10, "#e9dcc8")
    rect(ax, 0.60, 12.30, 0.30, 1.30, MADERA, "||"); txt(ax, 1.05, 12.05, "estantería", 4.8, ha="left", va="top")
    # baño grande
    rect(ax, 9.25, 9.0, .80, .45); rect(ax, 10.1, 8.95, .55, .55); rect(ax, 10.8, 9.0, .60, 1.60, "#eef"); rect(ax, 9.25, 10.6, .55, .75)


def dibujar(ax, m, recorte=False):
    ax.add_patch(MPoly(list(OUT.exterior.coords), closed=True, fc="#8d8d8d", ec="#222", lw=1.6, zorder=1))
    for g in getattr(INN, "geoms", [INN]): ax.add_patch(MPoly(list(g.exterior.coords), closed=True, fc="white", ec="none", zorder=2))
    ax.add_patch(Rectangle((10.85, 8.30), 1.20, 3.50, fc="none", ec="#a33", ls="--", lw=.9, zorder=4)); txt(ax, 11.45, 8.05, "casa vecina\n(1.ª planta)\nencima de esta mitad", 5.4, "#a33", va="top")
    tot = {}
    sust = m.get("sustituye", {})
    for room in [sust.get(r[0], r) for r in COMUN] + m["rooms"]:
        nombre, tipo, poly = room[:3]; lpos = room[3] if len(room) > 3 else None
        pol = Polygon(poly); a = pol.area; cx, cy = lpos or pol.centroid.coords[0]
        ax.add_patch(MPoly(poly, closed=True, fc=COL[tipo], ec="#222", lw=1.3, zorder=3, hatch="//" if tipo == "esc" else None))
        peq = pol.bounds[2] - pol.bounds[0] < 2.2
        ax.text(cx, cy, f"{nombre}\n{a:.1f} m²", ha="center", va="center", fontsize=6.3 if peq else 7.8, zorder=9, linespacing=1.15); tot[nombre.splitlines()[0]] = a
    for (x0, y0, x1, y1) in m["seg"] + SEG_COMUN: ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="#5b5b5b", ec="#111", lw=.8, hatch="xx", zorder=4))
    escalera(ax, "PB")
    muebles_comunes(ax, not m.get("despacho_v")); m["muebles"](ax)
    ax.add_patch(Rectangle((7.75, 0.25), 0.10, 7.07, fc="#666", ec="#222", zorder=4)); txt(ax, 7.65, 3.6, "murete media altura", 6.0, ha="right", rot=90)
    ax.add_patch(Rectangle((3.55, 0.0), 4.00, 0.25, fc=VIDRIO, ec=VIDRIO_EC, lw=1.4, zorder=6)); txt(ax, 5.5, -0.15, "cristalera de suelo a techo (4,00 m) junto a la puerta", 6.2, "#1f6fa8", va="top")
    for (x, w) in m["ventanas"]: ventana(ax, x, w)
    for (x, w) in m["asientos"]: asiento_ventana(ax, x, w)
    for (x, w) in m["correderas"]: corredera_aluminio(ax, x, w)
    for (x0, y0, x1, y1) in [a for a in ABIERTOS_COMUN if a not in m.get("quita_abiertos", [])] + m["abiertos"]: ax.plot([x0, x1], [y0, y1], color="white", lw=5, solid_capstyle="butt", zorder=7)
    for d in [p for p in PUERTAS_COMUN if p not in m.get("quita_puertas", [])] + m["puertas"]: door(ax, d)
    txt(ax, 3.55, 11.33, "puerta de\nseguridad", 4.4, "#7a1f1f")
    ax.annotate("", xy=(-0.1, -0.6), xytext=(-0.1, 1.6), arrowprops=dict(arrowstyle="-|>", color="#222", lw=1.6), annotation_clip=False); ax.text(-0.1, 1.85, "N", ha="center", fontsize=11, weight="bold")
    ax.text(11.9, -0.4, "norte · acceso por el camino", ha="right", fontsize=6.5, color="#555"); ax.text(11.9, 17.05, "sur · patio y rambla de Albox", ha="right", fontsize=6.5, color="#555")
    ax.set_xlim(-0.6, 12.6); ax.set_ylim(*((6.9, 17.2) if recorte else (-0.9, 17.4))); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(m["titulo"], fontsize=(8.6 if recorte else 10.5), weight="bold", loc="left", pad=6)
    if recorte:
        for t in ax.texts:
            if t.get_position()[1] < 6.9 or t.get_position()[1] > 17.2: t.set_visible(False)
    return tot


# ---------------------------------------------------------------- modelo A: dormitorio 2 compacto en el centro, cocina-comedor al este
def muebles_A(ax):
    cama(ax, 4.80, 11.95, 0.95, 1.95, "n"); rect(ax, 3.85, 13.0, .42, 1.60, MADERA, "||"); silla(ax, 4.55, 15.35, .36)                      # cama individual, armario de 45 cm, asiento del rincón
    encimera(ax, 5.95, 12.50, .62, 2.65, "nevera, columnas y fuegos"); encimera(ax, 5.95, 15.15, 1.20, .60, "fregadero")
    mesa(ax, 7.55, 13.35, 1.25, 1.15, [(7.35, 13.9), (8.99, 13.9), (8.17, 13.17), (8.17, 14.67)]); rect(ax, 8.25, 12.45, .65, .30, MADERA, "||"); txt(ax, 8.58, 12.62, "despensa baja", 4.2)

MODELO_A = dict(
    titulo="MODELO A · dormitorio 2 pequeño en el centro y cocina-comedor al este",
    rooms=[("Dormitorio 2", "priv", R(3.80, 11.90, 5.75, 15.75), (4.78, 14.2)),
           ("Cocina-comedor", "cocina", [(5.90, 11.75), (7.15, 11.75), (7.15, NY), (9.00, NY), (9.00, 15.75), (5.90, 15.75)], (7.45, 13.55))],
    seg=[(0.55, 11.75, 5.90, 11.90), (5.75, 11.90, 5.90, 15.75)], muebles=muebles_A,
    ventanas=[(2.55, 0.90), (6.05, 0.80)], asientos=[(0.70, 1.30), (4.05, 1.00)], correderas=[(7.30, 1.60)],
    abiertos=[(5.95, 11.82, 7.10, 11.82)], puertas=[(3.90, 11.75, "H", 0.90, 0, 1), (8.25, NY - 0.05, "H", 0.70, 0, -1)])


# ---------------------------------------------------------------- modelo B: cocina-comedor grande, sin dormitorio 2 abajo
def muebles_B(ax):
    encimera(ax, 8.40, 12.95, .60, 2.25, "fuegos y fregadero"); encimera(ax, 3.85, 12.40, .60, 1.40, "nevera"); rect(ax, 6.10, 13.10, 1.05, 1.60, "#eadcc4", z=6); txt(ax, 6.62, 13.9, "isla", 5.0)
    for k in range(3): silla(ax, 5.85, 13.35 + k * .5)
    mesa(ax, 4.45, 14.15, 1.30, .95, [(4.25, 14.3), (4.25, 14.95), (5.95, 14.3), (5.95, 14.95)])
    rect(ax, 8.25, 12.45, .65, .30, MADERA, "||"); txt(ax, 8.58, 12.62, "despensa baja", 4.2)

MODELO_B = dict(
    titulo="MODELO B · cocina-comedor grande abierta a la sala (sin dormitorio 2 abajo)",
    rooms=[("Cocina-comedor", "cocina", [(3.80, 11.75), (7.15, 11.75), (7.15, NY), (9.00, NY), (9.00, 15.75), (3.80, 15.75)], (5.9, 12.35))],
    seg=[(0.55, 11.75, 3.80, 11.90)], muebles=muebles_B,
    ventanas=[(2.55, 0.90), (8.05, 0.80)], asientos=[(0.70, 1.30), (3.95, 0.90)], correderas=[(5.05, 2.40)],
    abiertos=[(3.85, 11.82, 5.45, 11.82), (5.65, 11.82, 7.10, 11.82)], puertas=[(8.25, NY - 0.05, "H", 0.70, 0, -1)])


# ---------------------------------------------------------------- modelo C: cocina central con despensa y lavadero al este
def muebles_C(ax):
    encimera(ax, 3.85, 12.40, .60, 2.70, "nevera, columnas y fuegos"); encimera(ax, 6.60, 12.40, .55, 1.70, "fregadero")
    mesa(ax, 4.75, 13.0, 1.30, 1.00, [(4.55, 13.3), (4.55, 13.8), (6.25, 13.3), (6.25, 13.8)])
    rect(ax, 7.30, 12.50, 1.65, .30, MADERA, "||"); rect(ax, 7.30, 14.40, .60, 1.30, "#eef"); rect(ax, 8.10, 14.40, .55, .60, "#dfe6ea"); txt(ax, 7.6, 14.05, "lavadora", 4.4); txt(ax, 8.12, 12.95, "estantes", 4.4)

MODELO_C = dict(
    titulo="MODELO C · cocina central de 13 m² con despensa y lavadero al este",
    rooms=[("Cocina", "cocina", R(3.80, 11.75, 7.15, 15.75), (5.5, 12.4)),
           ("Despensa", "humedo", R(7.25, NY, 9.00, 13.55), (8.12, 12.95)), ("Lavadero", "humedo", R(7.25, 13.65, 9.00, 15.75), (8.12, 15.15))],
    seg=[(0.55, 11.75, 3.80, 11.90)], muebles=muebles_C,
    ventanas=[(2.55, 0.90), (7.70, 0.90)], asientos=[(0.70, 1.30), (3.95, 0.90)], correderas=[(5.30, 1.60)],
    abiertos=[(3.85, 11.82, 5.45, 11.82), (5.65, 11.82, 7.10, 11.82)], puertas=[(7.15, 12.65, "V", 0.80, 0, 1), (7.15, 14.45, "V", 0.80, 0, 1)])

# ---------------------------------------------------------------- modelo C2: el C con el despacho girado, de la puerta del vestidor a la chimenea
DESP_V = R(3.15, 7.97, 4.95, 10.62)                                                         # 1,80 x 2,65 m, a lo largo de la pared del vestidor
HUB_V = [(5.05, 7.87), (7.15, 7.87), (7.15, 11.75), (3.15, 11.75), (3.15, 10.72), (5.05, 10.72)]


def muebles_C2(ax):
    muebles_C(ax)
    rect(ax, 3.20, 8.15, .65, 1.55, MADERA); silla(ax, 4.20, 8.95, .42)                                 # mesa larga contra la pared del vestidor y silla
    rect(ax, 4.65, 8.05, .28, 1.30, MADERA, "||"); rect(ax, 3.25, 9.88, .62, .55, "#c7a7d9"); txt(ax, 3.56, 9.52, "sillón", 4.6)   # estantería junto a la puerta y sillón de lectura
    ax.add_patch(Rectangle((3.25, 7.84), 1.60, 0.10, fc=VIDRIO, ec=VIDRIO_EC, lw=1.0, zorder=7)); txt(ax, 4.05, 7.62, "cristal fijo hacia el salón y la chimenea", 4.6, "#1f6fa8")

MODELO_C2 = dict(MODELO_C, titulo="MODELO C2 · cocina central de 13 m² y despacho girado hasta la chimenea", muebles=muebles_C2, despacho_v=True,
                 sustituye={"Despacho": ("Despacho", "priv", DESP_V, (4.05, 9.3)), "Sala de estar\ny paso": ("Sala de estar\ny paso", "sala", HUB_V, (6.15, 9.2))},
                 quita_puertas=[(4.35, 9.55, "H", 0.85, 0, 1)], quita_abiertos=[(5.60, 7.95, 5.60, 9.50)],
                 puertas=MODELO_C["puertas"] + [(4.95, 9.70, "V", 0.85, 0, 1)])

MODELOS = {"A": MODELO_A, "B": MODELO_B, "C": MODELO_C}
EXTRA = {"C2": MODELO_C2}

if __name__ == "__main__":
    res = {}
    for k, m in list(MODELOS.items()) + list(EXTRA.items()):
        fig, ax = plt.subplots(figsize=(7.2, 9.4)); res[k] = dibujar(ax, m); fig.tight_layout(); fig.savefig(f"modelo_{k}_planta_baja.png", dpi=int(os.environ.get("DPI", 130))); plt.close(fig)
    fig, axs = plt.subplots(1, 3, figsize=(21, 7.4))                      # comparación: solo la mitad sur, que es la que cambia
    for ax, (k, m) in zip(axs, MODELOS.items()): dibujar(ax, m, recorte=True)
    fig.tight_layout(); fig.savefig("modelos_planta_baja.png", dpi=int(os.environ.get("DPI", 105)), bbox_inches="tight"); plt.close(fig)
    for k, t in res.items(): print(k, {n: round(a, 1) for n, a in t.items() if n in ("Cocina-comedor", "Cocina", "Dormitorio 2", "Despensa", "Lavadero", "Despacho", "Sala de estar")})
