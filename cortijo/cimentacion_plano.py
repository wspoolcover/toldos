"""Plano de cimentación y de zunchos (propuesta generosa: más hormigón y más acero donde cuesta poco). Genera cimentacion_planos.png y cimentacion_v7.dxf."""
import json, math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, PathPatch, Circle
from matplotlib.path import Path
from shapely.geometry import Polygon, box as sbox, LineString
import ezdxf
import opciones as o

E = json.load(open("estructura.json")); LX = E["lineas_x"]; CY = [7.60, 11.80]
ZAP, CANTO = 1.60, 0.60                                   # lado de zapata aislada y canto: se redondea hacia arriba (cálculo: 1,50 con 130 kPa)
T_S, T = 0.25, 0.55
SB = Polygon(o.SB_); HOUSE = Polygon(o.NB_FULL)
SALON_WALL = SB.difference(SB.buffer(-T_S, join_style=2)); HOUSE_WALL = HOUSE.difference(HOUSE.buffer(-T, join_style=2))
ZS = [(LX[0], cy) for cy in CY]; ZC = [((LX[1] + LX[2]) / 2, cy) for cy in CY]                  # aisladas bajo x = 3,10 y combinadas bajo x = 5,55 y 7,20
LC = (LX[2] - LX[1]) + ZAP                                                                     # largo de la zapata combinada
RIO_W, RIO_H = 0.40, 0.50
AZ, VI, MA, GR, RO, VE = "#1f6fb5", "#7d3c98", "#8c4a2f", "#555", "#c0392b", "#2d6a4f"

def paint(ax, poly, **kw):
    for g in getattr(poly, "geoms", [poly]):
        if g.is_empty: continue
        v, c = [], []
        for ring in [g.exterior] + list(g.interiors):
            pts = list(ring.coords); v += pts; c += [Path.MOVETO] + [Path.LINETO] * (len(pts) - 2) + [Path.CLOSEPOLY]
        ax.add_patch(PathPatch(Path(v, c), **kw))

def ejes(ax, title):
    ax.set_xlim(-1.0, 13.2); ax.set_ylim(-1.6, 17.6); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=11, weight="bold", loc="left")
    ax.annotate("", xy=(-0.4, -0.9), xytext=(-0.4, 1.2), arrowprops=dict(arrowstyle="-|>", lw=1.4), annotation_clip=False); ax.text(-0.4, 1.4, "N", ha="center", fontsize=10, weight="bold")
    ax.text(6.0, 17.2, "sur · CALLE (fachada con CGP y rejas)", ha="center", fontsize=7, color=GR); ax.text(6.0, -1.3, "norte · terreno propio (entrada)", ha="center", fontsize=7, color=GR)
    ax.text(-0.9, 12.0, "casa vecina (oeste)", rotation=90, fontsize=7, color=RO, va="center"); ax.text(12.9, 10.0, "casa vecina (este)", rotation=90, fontsize=7, color=RO, va="center")

def cimentacion(ax):
    ejes(ax, "CIMENTACIÓN · escala aprox. 1:150")
    paint(ax, HOUSE.difference(HOUSE.buffer(-1.10, join_style=2)), fc="#ece8df", ec=GR, ls="--", lw=.8, hatch="..", zorder=1)             # zapata corrida de los muros de 55 cm: ancho supuesto 1,10 m hacia dentro (a comprobar con catas)
    paint(ax, SB.buffer(0.175, join_style=2).difference(SB.buffer(-T_S - 0.175, join_style=2)).intersection(sbox(-1, -1, 14, 7.2)), fc="#d9e8dc", ec=VE, lw=1.0, hatch="//", zorder=2)   # zapata corrida de 0,60 ya hecha bajo los muros del salón
    paint(ax, SALON_WALL, fc="#9b968b", ec="#222", lw=1, zorder=3); paint(ax, HOUSE_WALL, fc="#9b968b", ec="#222", lw=1, zorder=3)
    for (x, y) in ZS: ax.add_patch(Rectangle((x - ZAP / 2, y - ZAP / 2), ZAP, ZAP, fc="#cfd8e8", ec=AZ, lw=1.6, zorder=4)); ax.text(x, y - ZAP / 2 - .22, f"Z-1  {ZAP:.2f}×{ZAP:.2f}", ha="center", fontsize=6.5, color=AZ, weight="bold", zorder=9)
    for (x, y) in ZC: ax.add_patch(Rectangle((x - LC / 2, y - ZAP / 2), LC, ZAP, fc="#cfd8e8", ec=AZ, lw=1.6, zorder=4)); ax.text(x, y - ZAP / 2 - .22, f"Z-2 combinada  {LC:.2f}×{ZAP:.2f}", ha="center", fontsize=6.5, color=AZ, weight="bold", zorder=9)
    for (x, y) in ZS + [(LX[1], y) for y in CY] + [(LX[2], y) for y in CY]: ax.add_patch(Rectangle((x - .06, y - .06), .12, .12, fc="#202a44", ec="none", zorder=8))
    rio = lambda x0, y0, x1, y1: ax.add_patch(Rectangle((min(x0, x1) - (RIO_W / 2 if x0 == x1 else 0), min(y0, y1) - (RIO_W / 2 if y0 == y1 else 0)), abs(x1 - x0) + (RIO_W if x0 == x1 else 0), abs(y1 - y0) + (RIO_W if y0 == y1 else 0), fc="#e6d7ef", ec=VI, lw=1.0, zorder=3.5))
    for cy in CY: rio(T / 2, cy, 9.55 - T / 2, cy)
    for lx in LX: rio(lx, CY[0], lx, CY[1])
    ax.text(1.05, 9.6, "RI-1 riostra 40×50", fontsize=7, color=VI, weight="bold", bbox=dict(fc="white", ec="none", alpha=.85, pad=1))
    ax.text(5.9, 5.0, "zapata corrida 0,60 m ya hecha\n(bajo muros laterales del salón)", fontsize=7, color=VE, ha="center", bbox=dict(fc="white", ec="none", alpha=.8, pad=1))
    ax.text(1.4, 14.2, "zapata corrida de los muros de 55 cm: ancho\nsupuesto ≥ 1,10 m, a comprobar con catas", fontsize=6.5, color=GR, bbox=dict(fc="white", ec="none", alpha=.8, pad=1))
    ax.plot([5.9, 5.9], [8.0, -1.0], color=VE, lw=1.6, ls="--", zorder=6); ax.text(6.05, 0.6, "colector Ø150\nbajo solera → fosa", fontsize=6, color=VE)
    ax.text(0.1, -0.7, "medianeras (este y oeste): excavar por bataches alternos y no pasar de la línea de lindero", fontsize=6.5, color=RO)

def zunchos(ax):
    ejes(ax, "ZUNCHOS Y PILARES DE ATADO · nivel de forjado y de cubierta")
    HW = HOUSE_WALL.difference(sbox(3.45, 7.2, 9.0, 8.0))                      # en la fachada interior no hay muro ni zuncho: lo sustituye la viga de acero
    paint(ax, HW, fc="#cdb9e0", ec="#222", lw=1, zorder=2); paint(ax, SALON_WALL, fc="#d9c3a5", ec="#222", lw=1, zorder=2)
    for p in (HW, SALON_WALL): paint(ax, p.buffer(0.0), fc="none", ec=VI, lw=1.8, zorder=3)
    ax.text(0.8, 15.4, "ZH-1  zuncho 55×30 en los muros existentes\n4Ø16 sup. + 4Ø16 inf., cercos Ø8/15", fontsize=6.5, color=VI, bbox=dict(fc="white", ec="none", alpha=.85, pad=1))
    ax.text(5.9, 3.6, "ZH-2  zuncho 25×30 sobre cada muro lateral\ndel salón (lado este y lado oeste)\n4Ø16 sup. + 4Ø16 inf., cercos Ø8/15", fontsize=7, color=VI, ha="center", weight="bold", bbox=dict(fc="white", ec="none", alpha=.85, pad=1))
    ys = [0.40, 2.40, 4.40, 6.40, 7.10]                                            # pilares de atado de 25×25, separación ≤ 2,0 m en los laterales
    xw = lambda y: 3.15 - 0.28 * y / 7.32 + T_S / 2; xe = 9.55 - T_S / 2
    pts = [(xw(y), y) for y in ys] + [(xe, y) for y in ys] + [(3.55, 0.125), (7.70, 0.125), (9.42, 0.125)]
    for (x, y) in pts: ax.add_patch(Rectangle((x - .125, y - .125), .25, .25, fc="#3b2a1a", ec="white", lw=.5, zorder=6))
    for (x, y) in [(0.275, 7.60), (0.275, 11.8), (0.275, 15.9), (9.275, 15.9), (9.275, 12.2), (4.9, 15.9), (0.275, 9.7), (0.275, 13.8), (9.275, 8.3)]: ax.add_patch(Rectangle((x - .15, y - .15), .30, .30, fc="#3b2a1a", ec="white", lw=.5, zorder=6))
    ax.text(5.9, 1.3, "PA  pilar de atado 25×25 (4Ø14, cercos Ø6/15)", fontsize=6.5, color="#3b2a1a", ha="center", weight="bold")
    for (x, y) in ZS + [(LX[1], y) for y in CY] + [(LX[2], y) for y in CY]: ax.add_patch(Rectangle((x - .06, y - .06), .12, .12, fc="#202a44", ec="none", zorder=7))
    for lx in LX: ax.plot([lx, lx], [CY[0], 15.9], color="#202a44", lw=1.2, zorder=5)
    for cy in CY: ax.plot([0.3, 9.3], [cy, cy], color="#202a44", lw=1.2, zorder=5)
    ax.text(0.3, 6.6, "vigas de acero HEB bajo forjado (pilares ■)", fontsize=6.5, color="#202a44")
    ax.text(5.9, -0.3, "dintel de la cristalera apoyado en pilares de atado a cada lado", fontsize=6, color=GR, ha="center")

# ---------------- figura ----------------
fig = plt.figure(figsize=(21, 14.8)); fig.suptitle("Cortijo Albox · Cimentación y zunchos (propuesta, más hormigón y más acero; a confirmar por el técnico)", fontsize=15, weight="bold", x=.02, y=.985, ha="left")
cimentacion(fig.add_axes([.015, .35, .30, .60])); zunchos(fig.add_axes([.33, .35, .30, .60]))

# alzado del muro lateral del salón (lado este) y sección del zuncho
a = fig.add_axes([.655, .70, .335, .25]); a.set_xlim(-60, 880); a.set_ylim(-110, 420); a.set_aspect("equal"); a.axis("off"); a.set_title("Alzado del muro lateral del salón (escala 1:50): lo mismo en el lado este y en el oeste", fontsize=9, weight="bold", loc="left")
a.add_patch(Rectangle((-20, -60), 800, 60, fc="#d9e8dc", ec=VE, hatch="//")); a.text(380, -35, "zapata corrida 60 cm (ya hecha), cota de apoyo a confirmar con el geotécnico", fontsize=7, color=VE, ha="center", va="center")
a.add_patch(Rectangle((0, 0), 760, 330, fc="#d4b98b", ec="#333")); a.add_patch(Rectangle((0, 330), 760, 30, fc="#cdb9e0", ec=VI, lw=1.6)); a.text(380, 345, "zuncho 25×30 (4Ø16 + 4Ø16, Ø8/15)", fontsize=7, ha="center", va="center", color=VI, weight="bold")
for x in (0, 190, 380, 570, 735): a.add_patch(Rectangle((x, 0), 25, 330, fc="#3b2a1a", ec="white", lw=.5))
a.text(380, 165, "muro de ladrillo de 25 cm (30 cm si todavía se puede)", fontsize=8, ha="center", color="#222", bbox=dict(fc="#d4b98b", ec="none", pad=2)); a.text(380, -95, "pilares de atado 25×25 cada ≤ 2 m, armadura anclada en la zapata y en el zuncho", fontsize=7, ha="center", color="#3b2a1a")
a.add_patch(Rectangle((0, 360), 760, 22, fc="#c9c5bb", ec="#333")); a.text(380, 372, "forjado de vigueta y bovedilla de la terraza", fontsize=6.5, ha="center", va="center")

b = fig.add_axes([.655, .40, .16, .29]); b.set_xlim(-30, 110); b.set_ylim(-50, 170); b.set_aspect("equal"); b.axis("off"); b.set_title("Sección del zuncho (cm)", fontsize=9, weight="bold", loc="left")
b.add_patch(Rectangle((0, 0), 25, 30, fc="#cdb9e0", ec=VI, lw=1.6)); b.add_patch(Rectangle((3, 3), 19, 24, fc="none", ec=VI, lw=.8))
for (x, y) in [(5, 5), (10, 5), (15, 5), (20, 5), (5, 25), (10, 25), (15, 25), (20, 25)]: b.add_patch(Circle((x, y), 1.4, fc=VI, ec="none"))
b.add_patch(Rectangle((0, -60), 25, 60, fc="#d4b98b", ec="#333")); b.add_patch(Rectangle((-8, 30), 41, 14, fc="#c9c5bb", ec="#333"))
b.text(40, 15, "4Ø16 sup.\n4Ø16 inf.\ncercos Ø8/15\nrecub. 3 cm\nHA-25", fontsize=7, va="center"); b.text(12.5, -30, "muro 25", fontsize=7, ha="center")

c = fig.add_axes([.825, .40, .165, .29]); c.set_xlim(-130, 130); c.set_ylim(-110, 175); c.set_aspect("equal"); c.axis("off"); c.set_title("Zapata Z-1 con pilar HEB 120 (cm)", fontsize=9, weight="bold", loc="left")
c.add_patch(Rectangle((-90, -60), 180, 10, fc="#eee", ec="#999")); c.add_patch(Rectangle((-80, -50), 160, 60, fc="#cfd8e8", ec=AZ, lw=1.6, hatch="..")); c.add_patch(Rectangle((-80, -45), 160, 4, fc=AZ)); c.add_patch(Rectangle((-80, -40), 160, 2, fc=AZ))
c.add_patch(Rectangle((-15, 10), 30, 3, fc="#555")); c.add_patch(Rectangle((-6, 13), 12, 140, fc="#202a44", ec="none")); c.add_patch(Rectangle((-14, 140), 28, 3, fc="#555"))
for x in (-11, 11): c.add_patch(Rectangle((x - 1, -30), 2, 40, fc=RO))
c.text(0, -75, "hormigón de limpieza 10 cm", fontsize=6.5, ha="center"); c.text(0, 165, "pilar HEB 120", fontsize=7, ha="center"); c.text(-125, 35, "placa 30×30×2 con 4 pernos Ø20, L = 40", fontsize=6.5, color=RO); c.text(-125, -95, "parrilla Ø12/15 en los dos sentidos (abajo)", fontsize=6.5, color=AZ)

# tabla de elementos y cantidades
vol_z = len(ZS) * ZAP ** 2 * CANTO + len(ZC) * LC * ZAP * CANTO
long_r = 2 * (9.55 - T) + len(LX) * (CY[1] - CY[0]); vol_r = long_r * RIO_W * RIO_H
Lw = 2 * 7.6 + 6.4; vol_zh2 = Lw * 0.25 * 0.30; Lh = HOUSE.exterior.length; vol_zh1 = Lh * 0.55 * 0.30
rows = [("Zapatas aisladas Z-1", f"{len(ZS)} uds", f"{ZAP:.2f}×{ZAP:.2f}×{CANTO:.2f}", f"{len(ZS) * ZAP ** 2 * CANTO:.1f}", "parrilla Ø12/15"),
        ("Zapatas combinadas Z-2", f"{len(ZC)} uds", f"{LC:.2f}×{ZAP:.2f}×{CANTO:.2f}", f"{len(ZC) * LC * ZAP * CANTO:.1f}", "parrilla Ø12/15"),
        ("Riostras RI-1", f"{long_r:.0f} m", "0,40×0,50", f"{vol_r:.1f}", "4Ø16 + 4Ø16, Ø8/20"),
        ("Zunchos ZH-2 (muros del salón)", f"{Lw:.0f} m", "0,25×0,30", f"{vol_zh2:.1f}", "4Ø16 + 4Ø16, Ø8/15"),
        ("Zunchos ZH-1 (muros de 55 cm)", f"{Lh:.0f} m", "0,55×0,30", f"{vol_zh1:.1f}", "4Ø16 + 4Ø16, Ø8/15"),
        ("Pilares de atado PA", "≈ 20 uds", "0,25×0,25×3,3", "≈ 0,4", "4Ø14, Ø6/15")]
tx = fig.add_axes([.015, .02, .62, .31]); tx.axis("off")
tx.text(0, 1.0, "Elementos y cantidades orientativas (hormigón HA-25 y acero B 500 S; hormigón de limpieza HL-150)", fontsize=10, weight="bold", va="top")
tb = tx.table(cellText=[list(r) for r in rows] + [("TOTAL hormigón estructural (sin limpieza)", "", "", f"≈ {vol_z + vol_r + vol_zh1 + vol_zh2 + .4:.0f}", "")], colLabels=["Elemento", "Cantidad", "Medidas (m)", "m³", "Armado orientativo"], cellLoc="left", loc="upper left", bbox=[0, 0.30, 1, 0.62], colWidths=[.34, .1, .16, .08, .2])
tb.auto_set_font_size(False); tb.set_fontsize(8.5)
tx.text(0, 0.24, "• Más hormigón y más acero que el cálculo mínimo: zapatas de 1,60 m (el cálculo da 1,50 con 130 kPa), riostras de 40×50 y zunchos con 4Ø16 arriba y abajo. Sobrecoste pequeño frente a la seguridad que da.\n"
         "• El muro lateral del salón queda en 25 cm (la cimentación de 60 cm ya está hecha); si todavía se puede, 30 cm da más margen. Zuncho de hormigón armado encima, en el lado este y en el lado oeste, atado a los pilares de atado.\n"
         "• El terreno admisible de 130 kPa es el del plano PL-11 del arquitecto: falta confirmarlo con un estudio geotécnico. Cota de apoyo recomendada ≥ 1,00 m bajo el terreno natural, en terreno firme.\n"
         "• Incluir en la cimentación antes de hormigonar: anillo de toma de tierra, pasamuros para agua, luz y saneamiento, y arqueta del colector hacia la fosa del norte.\n"
         "• Las armaduras, las secciones y las cotas son una propuesta y las confirma el técnico o ingeniero; los 55 cm de los muros existentes necesitan catas antes de decidir recalces.", fontsize=8.6, va="top", linespacing=1.55, wrap=True)
fig.savefig("cimentacion_planos.png", dpi=100)

# ---------------- DXF ----------------
doc = ezdxf.new("R2010"); msp = doc.modelspace()
for n, col in (("MUROS", 8), ("ZAPATAS", 5), ("RIOSTRAS", 6), ("ZUNCHOS", 6), ("PILARES_ATADO", 3), ("PILARES", 2), ("TEXTO", 7)): doc.layers.add(n, color=col)
poly = lambda p, layer: [msp.add_lwpolyline(list(g.exterior.coords), close=True, dxfattribs={"layer": layer}) for g in getattr(p, "geoms", [p])]
poly(HOUSE, "MUROS"); poly(SB, "MUROS"); poly(HOUSE.buffer(-T, join_style=2), "MUROS"); poly(SB.buffer(-T_S, join_style=2), "MUROS")
for (x, y) in ZS: msp.add_lwpolyline([(x - ZAP / 2, y - ZAP / 2), (x + ZAP / 2, y - ZAP / 2), (x + ZAP / 2, y + ZAP / 2), (x - ZAP / 2, y + ZAP / 2)], close=True, dxfattribs={"layer": "ZAPATAS"})
for (x, y) in ZC: msp.add_lwpolyline([(x - LC / 2, y - ZAP / 2), (x + LC / 2, y - ZAP / 2), (x + LC / 2, y + ZAP / 2), (x - LC / 2, y + ZAP / 2)], close=True, dxfattribs={"layer": "ZAPATAS"})
for cy in CY: msp.add_lwpolyline([(T / 2, cy - .2), (9.55 - T / 2, cy - .2), (9.55 - T / 2, cy + .2), (T / 2, cy + .2)], close=True, dxfattribs={"layer": "RIOSTRAS"})
for lx in LX: msp.add_lwpolyline([(lx - .2, CY[0]), (lx + .2, CY[0]), (lx + .2, CY[1]), (lx - .2, CY[1])], close=True, dxfattribs={"layer": "RIOSTRAS"})
for lx in LX:
    for cy in CY: msp.add_circle((lx, cy), .06, dxfattribs={"layer": "PILARES"})
for (x, y) in [(3.15 - .28 * yy / 7.32 + .125, yy) for yy in (0.4, 2.4, 4.4, 6.4, 7.1)] + [(9.425, yy) for yy in (0.4, 2.4, 4.4, 6.4, 7.1)]: msp.add_lwpolyline([(x - .125, y - .125), (x + .125, y - .125), (x + .125, y + .125), (x - .125, y + .125)], close=True, dxfattribs={"layer": "PILARES_ATADO"})
msp.add_text("Z-1 1,60x1,60x0,60 | Z-2 combinada 3,25x1,60x0,60 | RI-1 40x50 | ZH-2 25x30 4Ø16+4Ø16 Ø8/15 | PA 25x25 4Ø14 Ø6/15 (propuesta, a confirmar)", height=0.25, dxfattribs={"layer": "TEXTO"}).set_placement((0, -2.2))
doc.saveas("cimentacion_v7.dxf"); print("ok", round(vol_z, 1), round(vol_r, 1), round(vol_zh1, 1), round(vol_zh2, 1))
