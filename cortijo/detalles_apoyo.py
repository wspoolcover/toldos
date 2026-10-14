"""Esquema (no a escala) de cómo apoya la placa superior: sobre un zuncho de bloque en U, sobre una viga HEB y viga sobre un pilarete de bloque relleno, como en la obra de referencia.
Los armados y las medidas los define el técnico. Uso: python detalles_apoyo.py -> detalles_apoyo_placa.png"""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

GRIS, BLOQ, HORM, ACERO, LADR, PLACA, MORT = "#9a9a9a", "#bdb7ad", "#d6d2c8", "#2d4a73", "#c9694a", "#e6e1d6", "#f0d9a8"

def r(ax, x, y, w, h, fc, hatch=None, ec="#333", lw=.9, z=3): ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, hatch=hatch, zorder=z))
def nota(ax, x, y, s, tx, ty, fs=7): ax.annotate(s, xy=(x, y), xytext=(tx, ty), fontsize=fs, ha="left", va="center", arrowprops=dict(arrowstyle="-", lw=.6, color="#555"), zorder=9)

fig, axs = plt.subplots(1, 3, figsize=(16, 5.2))
def ajustar(ax, titulo, xl, yl):
    ax.set_xlim(*xl); ax.set_ylim(*yl); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(titulo, fontsize=10.5, weight="bold", loc="left", pad=6)

# ---- A) placa sobre zuncho de bloque en U (muros laterales del salón)
ax = axs[0]
r(ax, 0, 0, 25, 70, LADR, "...")                                                            # muro de ladrillo de 25 cm
r(ax, 0, 70, 25, 30, BLOQ); r(ax, 5, 72, 15, 26, HORM, "//")                                # bloque en U y hormigón de relleno
for dx in (7, 17): ax.plot([dx, dx], [74, 96], color="#222", lw=1.6, zorder=6)              # armadura longitudinal (esquema)
ax.plot([6, 19, 19, 6, 6], [73, 73, 97, 97, 73], color="#222", lw=.7, zorder=6)             # cerco
r(ax, 5, 100, 75, 20, PLACA, "o"); r(ax, 5, 120, 75, 5, HORM, "//")                        # placa alveolar sobre el zuncho y capa de compresión
ajustar(ax, "A · Placa sobre el muro del salón", (-10, 235), (-8, 140))
nota(ax, 60, 122.5, "capa de compresión con mallazo", 95, 130); nota(ax, 60, 110, "placa alveolar: el apoyo mínimo lo fija el fabricante", 95, 108)
nota(ax, 20, 85, "zuncho 25×30: bloque en U relleno de hormigón y armado", 95, 82); nota(ax, 12, 35, "muro de ladrillo de 25 cm sobre la\ncimentación corrida de 0,60 m", 95, 35)

# ---- B) placa sobre viga HEB (borde sur y vigas N-S), esquema ampliado
ax = axs[1]
r(ax, -14, 0, 28, 6, ACERO); r(ax, -2, 6, 4, 22, ACERO); r(ax, -14, 28, 28, 6, ACERO)    # HEB 140 en sección: alas de 14 cm
r(ax, -34, 0, 20, 6, ACERO); r(ax, 14, 0, 20, 6, ACERO)                                      # angulares soldados al ala inferior
r(ax, -90, 6, 76, 40, PLACA, "o"); r(ax, 14, 6, 76, 40, PLACA, "o")                          # placas a los dos lados, apoyadas en los angulares
r(ax, -14, 34, 28, 12, HORM, "//"); r(ax, -90, 46, 180, 10, HORM, "//")                    # hormigón sobre la viga y capa de compresión
ajustar(ax, "B · Placas sobre una viga de acero", (-95, 235), (-30, 100))
nota(ax, 0, 18, "viga HEB embebida en el canto del forjado", 105, 24); nota(ax, 24, 3, "angular soldado al ala: da apoyo a cada placa\n(con el ala sola, 7 cm por placa: poco)", 105, 0)
nota(ax, -60, 30, "placa alveolar", -90, 78); nota(ax, 0, 51, "hormigón de relleno y capa de compresión", 105, 52)
ax.text(-90, -22, "La viga se protege del fuego (R60): el hormigón que la\nrodea o un mortero proyectado.", fontsize=7, va="center")

# ---- C) viga sobre pilarete de bloque relleno (como en el vídeo)
ax = axs[2]
r(ax, 0, 0, 20, 100, BLOQ); r(ax, 5, 0, 10, 100, HORM, "//")                                # pilarete de bloque relleno
for dx in (7, 13): ax.plot([dx, dx], [2, 98], color="#222", lw=1.6, zorder=6)
r(ax, -4, 100, 28, 3, ACERO, z=5); r(ax, -2, 103, 24, 3, MORT, z=4)                          # placa de apoyo y mortero sin retracción
r(ax, -4, 106, 70, 4, ACERO); r(ax, -4, 110, 70, 3, ACERO)                                  # viga (ala y alma, esquema)
r(ax, 0, 113, 20, 18, BLOQ); r(ax, 4, 115, 12, 14, HORM, "//")                              # hilada de bloque en U sobre la viga
r(ax, 20, 0, 40, 70, LADR, "...")
ajustar(ax, "C · Viga sobre pilarete de bloque (el del vídeo)", (-15, 235), (-8, 145))
nota(ax, 10, 50, "pilarete de bloque relleno de hormigón\ny armado, anclado a la cimentación", 85, 45); nota(ax, 10, 101.5, "placa de apoyo y mortero sin retracción\n(apoyo ≥ 12 cm en fábrica maciza o perforada)", 85, 80)
nota(ax, 45, 111, "viga de acero (dintel de la cristalera)", 85, 108); nota(ax, 10, 124, "hilada de bloque en U: une viga y zuncho,\nla placa apoya encima", 85, 130)
fig.suptitle("Apoyo de la placa superior (esquemas sin escala; armados y medidas: los define el técnico)", fontsize=11, weight="bold", x=.01, ha="left")
fig.tight_layout(); fig.savefig("detalles_apoyo_placa.png", dpi=int(os.environ.get("DPI", 130)), bbox_inches="tight")
print("ok")


# ---------------------------------------------------------------- segunda lámina: viga o dintel de hormigón hecho con bloque en U
fig, axs = plt.subplots(1, 2, figsize=(14, 5.2), gridspec_kw=dict(width_ratios=[1, 1.5]))
ax = axs[0]
r(ax, 0, 0, 25, 20, BLOQ); r(ax, 3, 3, 19, 17, HORM, "//")                                   # bloque en U y hormigón de relleno
r(ax, 0, 0, 3, 20, BLOQ, z=4); r(ax, 22, 0, 3, 20, BLOQ, z=4)
ax.plot([5, 20, 20, 5, 5], [5, 5, 17, 17, 5], color="#222", lw=.8, zorder=6)                  # cerco
for (x, y) in ((6.5, 6.5), (18.5, 6.5), (6.5, 15.5), (18.5, 15.5)): ax.add_patch(plt.Circle((x, y), 1.1, fc="#222", zorder=7))   # barras longitudinales
r(ax, -2, 20, 29, 5, HORM, "//")                                                             # capa de compresión del forjado por encima
ajustar(ax, "Sección de la viga", (-15, 150), (-14, 35))
nota(ax, 12, 3, "bloque en U: hace de encofrado\ny queda como parte de la viga", 40, -8); nota(ax, 6.5, 6.5, "barras longitudinales y cercos", 40, 8)
nota(ax, 12.5, 12, "hormigón de relleno (vibrado)", 40, 21); nota(ax, 12.5, 22.5, "capa de compresión del forjado", 40, 32)

ax = axs[1]
r(ax, 0, 0, 40, 90, LADR, "..."); r(ax, 160, 0, 40, 90, LADR, "...")                         # muros a los lados del hueco
r(ax, 0, 90, 40, 20, BLOQ); r(ax, 160, 90, 40, 20, BLOQ); r(ax, 20, 90, 160, 20, BLOQ, z=2)   # hilada de bloque en U sobre el hueco, apoyada 20 cm por lado
for k in range(1, 10): ax.plot([20 + k * 16, 20 + k * 16], [90, 110], color="#777", lw=.6, zorder=4)   # juntas entre bloques
r(ax, 4, 92, 192, 16, HORM, "//", z=5, lw=.4); ax.plot([6, 194], [96, 96], color="#222", lw=1.6, zorder=7); ax.plot([6, 194], [104, 104], color="#222", lw=1.6, zorder=7)
for x in (60, 100, 140): ax.plot([x, x], [0, 88], color="#e0a800", lw=3.2, zorder=6); ax.plot([x - 8, x + 8], [88, 88], color="#e0a800", lw=3.2, zorder=6)  # puntales
ajustar(ax, "Dintel sobre un hueco (alzado)", (-10, 290), (-10, 135))
nota(ax, 170, 102, "apoyo de 20 cm o más a cada lado\n(lo fija el técnico)", 215, 122); nota(ax, 150, 106, "hilada de bloques en U, armada y rellena", 215, 100)
nota(ax, 140, 40, "puntales hasta que el hormigón\nalcance la resistencia (plazo del técnico)", 215, 55); nota(ax, 180, 30, "muro de ladrillo o de bloque", 215, 20)
ax.text(100, -5, "hueco libre: hasta unos 2 m con este sistema; más luz, viga de acero o de hormigón calculada", ha="center", fontsize=7.5)
fig.suptitle("Viga o dintel de hormigón hecho con bloque en U (esquemas sin escala; armado y hormigón: los define el técnico)", fontsize=11, weight="bold", x=.01, ha="left")
fig.tight_layout(); fig.savefig("viga_bloque_u.png", dpi=int(os.environ.get("DPI", 130)), bbox_inches="tight")
print("ok 2")
