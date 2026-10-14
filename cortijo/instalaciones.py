"""Esquemas de instalaciones sobre la distribución v8: fontanería y saneamiento, electricidad, climatización (aerotermia, suelo radiante, splits) y cubierta solar."""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon as MPoly
import opciones as o

def base(ax, planta):
    rooms, doors, ab = (o.PB, o.PB_DOORS, o.PB_OPEN) if planta == "PB" else (o.PA, o.PA_DOORS, o.PA_OPEN)
    o.dibujar(ax, rooms, doors, planta, ab)
    for p in list(ax.patches):
        fc = p.get_facecolor()
        if isinstance(p, Rectangle) and p.get_hatch() == "||": p.set_alpha(.25)
        elif isinstance(p, Rectangle) and p.get_zorder() == 5: p.set_alpha(.25)
    for t in ax.texts:
        if t.get_fontsize() < 7: t.set_visible(False)

def linea(ax, pts, color, lw=1.6, ls="-", z=20): ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="round")
def punto(ax, x, y, color, txt="", r=.13, z=22, fs=5.5):
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.4, zorder=z)); ax.text(x, y, txt, ha="center", va="center", fontsize=fs, color=color, zorder=z + 1, weight="bold")
def caja(ax, x, y, dx, dy, color, txt, z=21, fs=5.5):
    ax.add_patch(Rectangle((x, y), dx, dy, fc="white", ec=color, lw=1.4, zorder=z)); ax.text(x + dx / 2, y + dy / 2, txt, ha="center", va="center", fontsize=fs, color=color, zorder=z + 1, weight="bold")

AZ, RO, MA, VE, NA, GR = "#1f6fb5", "#c0392b", "#7d3c98", "#1e8449", "#d35400", "#555"

def fontaneria(ax, planta):
    base(ax, planta)
    if planta == "PB":
        ax.set_ylim(-4.6, 19.0)
        # acometida de agua por el NORTE, junto a la puerta corredera de 7 m del camino (dato del propietario): contador fuera, tubería enterrada por el pasillo de entrada
        caja(ax, 8.0, -1.9, 1.3, 0.45, AZ, "contador", fs=5); linea(ax, [(8.6, -1.45), (8.6, 8.5), (6.9, 8.5), (6.9, 12.2)], AZ, 2.2); ax.text(9.5, -1.0, "acometida de agua\n(norte, junto a la\npuerta corredera)", fontsize=5.5, color=AZ, va="center")
        caja(ax, 7.30, 10.85, 0.75, 1.30, GR, "módulo\nhidr. +\nACS 200 L", fs=4.2); linea(ax, [(6.9, 11.4), (7.30, 11.4)], AZ)                      # armario técnico bajo el tramo de vuelta de la escalera
        linea(ax, [(6.9, 12.2), (6.2, 12.2), (6.2, 15.95), (5.6, 15.95), (5.6, 15.45)], AZ)                                                  # cocina (fregadero bajo la ventana)
        linea(ax, [(6.9, 12.2), (3.0, 12.2), (3.0, 9.4), (1.6, 9.4), (1.6, 8.3)], AZ); linea(ax, [(8.6, 8.5), (9.05, 8.5), (9.05, 11.0), (9.3, 11.0)], AZ)   # suite; baño grande por el tabique junto a la entrada
        linea(ax, [(7.25, 11.2), (7.0, 11.2), (7.0, 12.35)], RO, 1.6)                                                    # agua caliente: sale del módulo y se reparte por el falso techo de la sala
        linea(ax, [(7.02, 12.35), (3.12, 12.35), (3.12, 9.52), (1.72, 9.52), (1.72, 8.42)], RO); linea(ax, [(8.05, 11.12), (9.02, 11.12), (9.3, 11.12)], RO); linea(ax, [(7.02, 12.35), (6.32, 12.35), (6.32, 16.05), (5.72, 16.05), (5.72, 15.55)], RO)
        ax.text(8.55, 11.55, "vaina bajo\nla escalera", fontsize=4.3, color=RO, ha="center", va="bottom", zorder=30)
        for x, y, t in ((9.3, 11.05, "B"), (5.6, 15.45, "C"), (1.6, 8.3, "B")): punto(ax, x, y, AZ, t)
        # aerotermia: la unidad exterior va sobre la cubierta (más seguro y lejos de la rambla); los tubos bajan por el hueco de la escalera hasta el armario técnico
        linea(ax, [(8.6, 12.1), (8.05, 12.1), (8.05, 11.8)], GR, 1.6, "--"); ax.text(8.3, 12.55, "tubos de aerotermia bajan\npor el hueco de la escalera", fontsize=4.5, color=GR)
        # saneamiento (verde): bajantes de los tres húmedos y colector enterrado bajo la solera hasta la fosa séptica del norte (PL-09)
        for x, y in ((1.9, 8.1), (9.3, 10.4), (5.4, 15.5)): punto(ax, x, y, VE, "Ø110", r=.22, fs=4.3)
        linea(ax, [(1.9, 8.1), (1.9, 8.0), (5.9, 8.0)], VE, 2, "--"); linea(ax, [(9.3, 10.4), (9.3, 12.1), (5.9, 12.1), (5.9, 8.0)], VE, 2, "--"); linea(ax, [(5.4, 15.5), (5.4, 12.1), (5.9, 12.1)], VE, 2, "--")
        linea(ax, [(5.9, 8.0), (5.9, -2.6)], VE, 2.6, "--"); caja(ax, 4.9, -4.0, 2.0, 1.3, VE, "fosa séptica\n(norte, terreno propio:\nrevisar capacidad)", fs=5)
        caja(ax, 5.55, 7.3, 0.7, 0.4, VE, "arqueta", fs=4.8)
        ax.text(0.2, 17.3, "tuberías PPR por el falso techo; el colector Ø150 va enterrado bajo la solera por el eje del salón (como en el proyecto original)", fontsize=5.6, color=GR)
        ax.text(1.0, 5.8, "drenaje perimetral\n+ geotextil", fontsize=5.5, color=VE, rotation=90, va="center")
        linea(ax, [(-0.2, 7.2), (-0.2, 16.5), (9.75, 16.5), (9.75, 12.0)], VE, 1.0, ":")
        ax.set_title("FONTANERÍA Y SANEAMIENTO · planta baja", fontsize=10, weight="bold")
    else:
        for col, d in ((AZ, 0), (RO, .12)): linea(ax, [(9.3, 8.6 + d), (9.3, 11.0 + d)], col)
        punto(ax, 9.3, 11.0, AZ, "B"); punto(ax, 9.3, 10.4, VE, "Ø110", r=.2, fs=4.5)
        ax.text(7.3, 7.6, "montantes desde la planta baja\npor el saliente del baño\n(sobre el baño de abajo)", fontsize=5.5, color=GR)
        for x, y in ((4.0, 12.6), (6.5, 12.6), (2.0, 10.6), (2.0, 14.6)): ax.add_patch(Circle((x, y), .12, fc=AZ, ec="none", zorder=22))
        ax.text(4.0, 12.3, "sumideros de pluviales (bajantes PVC Ø90, 4 uds.)", fontsize=5.5, color=AZ, ha="left", va="top")
        ax.set_title("FONTANERÍA · planta alta (baño sobre baño: una sola columna)", fontsize=10, weight="bold")

def electricidad(ax, planta):
    base(ax, planta)
    if planta == "PB":
        ax.set_ylim(-0.9, 19.0)
        caja(ax, 5.85, 16.25, 0.7, 0.35, NA, "CGP+cont.", fs=4.2); linea(ax, [(6.2, 18.6), (6.2, 16.6)], NA, 2.4); ax.text(6.45, 18.4, "acometida eléctrica TRIFÁSICA\n(CGP Cahors ya colocada en la fachada\nsur, 63 A; nicho entre las ventanas de\nla cocina y del dormitorio 2: confirmar)", fontsize=5.3, color=NA, va="top")
        linea(ax, [(6.20, 16.25), (6.20, 11.6)], NA, 2.0); caja(ax, 5.75, 11.15, 0.6, 0.32, NA, "cuadro", fs=4.6)                  # derivación individual dentro del tabique dormitorio 2 / cocina
        tramos = [[(6.20, 11.3), (6.50, 11.3), (6.50, 12.6), (8.5, 12.6), (8.5, 14.5)], [(5.2, 13.3), (4.2, 13.3), (4.2, 15.0)], [(6.35, 11.2), (5.0, 11.2), (5.0, 12.4), (5.2, 13.3)], [(6.35, 11.2), (3.15, 11.2), (3.15, 10.6), (2.0, 10.6), (2.0, 11.9), (2.0, 13.8)],
                  [(2.0, 10.6), (2.0, 9.0)], [(6.35, 10.2), (4.4, 10.2), (4.4, 9.55), (4.4, 8.8)], [(6.35, 9.8), (5.9, 9.8), (5.9, 7.5), (7.5, 7.5), (7.5, 1.5)], [(7.5, 4.5), (4.5, 4.5)], [(6.35, 10.8), (6.3, 10.0)]]
        for t in tramos: linea(ax, t, NA, 1.2)
        for x, y, t in ((5.2, 13.3, "C"), (8.5, 14.5, "D2"), (4.2, 15.0, "C"), (2.0, 13.8, "D1"), (2.0, 9.0, "V"), (7.5, 1.5, "S"), (4.5, 4.5, "TV"), (4.4, 8.8, "O"), (6.3, 10.0, "E"), (4.5, 1.2, "⌂")): punto(ax, x, y, NA, t, r=.19, fs=4.8)
        caja(ax, 3.55, 1.6, .25, 1.9, MA, "", fs=5); ax.text(3.95, 2.3, "TV 75\"\n2×RJ45\n4 tomas\ntubo Ø40", fontsize=5, color=MA)
        caja(ax, 7.3, 8.0, .8, .35, MA, "rack red", fs=5)
        ax.text(5.6, 17.3, "canalizaciones por falso techo y tabiques; registros en cada estancia", fontsize=5.6, color=GR, ha="center")
        ax.text(0.0, 18.6, "Leyenda: C cocina (6 mm² + 4 mm²) · S salón/comedor · TV multimedia · D dormitorios · V vestidor/baño · O despacho · E escalera y sala · ⌂ entrada/timbre", fontsize=5.0, color=NA)
        ax.set_title("ELECTRICIDAD Y RED · planta baja", fontsize=10, weight="bold")
    else:
        linea(ax, [(8.5, 8.9), (8.5, 11.9), (2.0, 11.9), (2.0, 13.8)], NA, 1.2); linea(ax, [(2.0, 11.9), (2.0, 9.5)], NA, 1.2); linea(ax, [(6.7, 11.9), (6.7, 13.8)], NA, 1.2); linea(ax, [(8.5, 11.9), (8.5, 15.8), (6.0, 15.8)], NA, 1.2)
        for x, y, t in ((2.0, 13.8, "D2"), (2.0, 9.5, "D1"), (6.7, 13.8, "D3"), (5.5, 9.5, "F"), (9.8, 10.0, "B")): punto(ax, x, y, NA, t, r=.19, fs=4.8)
        linea(ax, [(6.35, 11.6), (6.35, 12.4)], NA, 1.2); ax.text(6.45, 12.2, "subida desde el cuadro\n(planta baja)", fontsize=5.3, color=NA)
        caja(ax, 5.5, 15.9, 1.0, .45, NA, "inversor\nsolar", fs=4.8); ax.text(6.6, 16.1, "cables de los paneles bajan por el\nmuro este hasta el cuadro", fontsize=5.3, color=NA, va="center")
        ax.set_title("ELECTRICIDAD · planta alta", fontsize=10, weight="bold")

def clima(ax, planta):
    base(ax, planta)
    if planta == "PB":
        for (x0, y0, x1, y1), t in (((3.4, 0.4, 7.7, 7.7), "SR salón 33 m²"), ((3.3, 9.7, 7.1, 11.7), "SR sala 11 m²"), ((0.6, 11.9, 3.6, 15.7), "SR dorm. ppal."), ((3.8, 11.9, 6.1, 15.7), "SR cocina"), ((6.3, 12.5, 8.9, 15.7), "SR dorm. 2"), ((7.3, 7.95, 8.95, 9.55), "SR entrada"), ((3.2, 8.0, 5.5, 9.5), "SR desp."), ((0.6, 9.5, 3.0, 11.7), "SR vest."), ((0.6, 7.95, 3.0, 9.3), "SR baño")):
            for k in range(int((y1 - y0) / .3)): linea(ax, [(x0 + .1, y0 + .15 + k * .3), (x1 - .1, y0 + .15 + k * .3)], RO, .7, z=18)
            ax.text((x0 + x1) / 2, (y0 + y1) / 2, t, fontsize=5.5, color=RO, ha="center", va="center", zorder=25, bbox=dict(fc="white", ec="none", alpha=.8, pad=1))
        caja(ax, 7.30, 10.85, .75, 1.30, RO, "módulo +\ncolector SR\n(armario\ntécnico)", fs=3.9); linea(ax, [(7.25, 11.3), (6.6, 11.3)], RO, 2)
        ax.set_ylim(-0.9, 18.0); ax.text(8.3, 12.55, "unidad exterior 8 kW\nsobre la cubierta", fontsize=4.5, color=GR)
        ax.text(2.0, 5.5, "suelo radiante (SR) en toda la planta baja: 109 m², tubo PE-X paso 15 cm, mortero 5 cm\n+ 3 cm de aislamiento bajo el tubo. Calefacción en invierno y refrescamiento suave en verano.", fontsize=5.6, color=RO, ha="center")
        ax.text(3.75, 6.2, "chimenea\ninsert 7 kW", fontsize=5.3, color="#a33", ha="center")
        ax.set_title("CLIMATIZACIÓN · planta baja (aerotermia + suelo radiante)", fontsize=10, weight="bold")
    else:
        for x, y in ((3.6, 11.5), (1.2, 15.4), (8.6, 15.4), (6.9, 11.5)): caja(ax, x - .45, y - .12, .9, .25, AZ, "split", fs=4.8)
        ax.text(2.0, 13.0, "4 unidades interiores de pared (2,5 kW)\nconectadas a una exterior multisplit\nen la terraza (detrás del parapeto)", fontsize=5.6, color=AZ, ha="center")
        caja(ax, 7.0, 6.9, 1.0, .5, AZ, "exterior\nmultisplit", fs=4.8); linea(ax, [(7.5, 7.4), (7.5, 8.0)], AZ, 1.2, "--")
        ax.text(6.0, 4.5, "Arriba NO suelo radiante: los dormitorios\nnecesitan frío en verano y el forjado\nde vigueta no admite 6 cm más sin recalcular.", fontsize=5.8, color=GR, ha="center")
        ax.set_title("CLIMATIZACIÓN · planta alta (multisplit frío/calor)", fontsize=10, weight="bold")

def cubierta(ax):
    import opciones as o
    ax.add_patch(MPoly(list(o.OUT_PA.exterior.coords), closed=True, fc="#d9d9d9", ec="#222", lw=1.4))
    for g in getattr(o.INN_PA, "geoms", [o.INN_PA]): ax.add_patch(MPoly(list(g.exterior.coords), closed=True, fc="#e9e9e9", ec="none"))
    ax.add_patch(MPoly([(3.4, .25), (9.3, .25), (9.3, 7.32), (3.12, 7.32)], closed=True, fc="#f4f4f4", ec="#555", ls="--", lw=.8)); ax.text(6.2, 3.8, "terraza del salón\n(pérgola de aluminio opcional)", ha="center", fontsize=6.5, color="#555")
    for f in range(3):
        for c in range(6):
            if c >= 5 and f <= 1: continue
            ax.add_patch(Rectangle((1.0 + c * 1.15, 8.6 + f * 2.1), 1.05, 1.75, fc="#1c2a4a", ec="#9ab", lw=.6))
    ax.add_patch(Rectangle((7.25, o.Y_HALL_PA), 1.75, o.Y_FIN - o.Y_HALL_PA, fc="#bfe3f8", ec="#2f8fd0", hatch="//")); ax.text(8.1, 11.0, "lucernario\nescalera", ha="center", va="center", fontsize=5.5)
    ax.add_patch(Rectangle((8.25, 12.55), .95, .45, fc="#d0d0d4", ec="#555", lw=1)); ax.text(8.7, 13.1, "aerotermia\n8 kW", ha="center", fontsize=5.5, color="#333")
    ax.add_patch(Rectangle((3.40, 6.55), .5, .5, fc="#a33")); ax.text(3.65, 7.2, "humero", fontsize=5.5, ha="center", color="#a33")
    for x, y in ((4.0, 12.6), (6.5, 12.6), (2.0, 10.6), (2.0, 14.6)): ax.add_patch(Circle((x, y), .12, fc=AZ)); 
    ax.text(5.0, 15.9, "16 paneles de 450 W = 7,2 kWp, orientados al SUR (inclinación 25-30°), sobre soportes lastrados\nsobre grava + sedum. Pendiente 1,5 % a 4 sumideros. Aislamiento XPS 10 cm invertido.", ha="center", fontsize=5.8)
    ax.text(5.0, 17.0, "sur · hacia la rambla", ha="center", fontsize=7, color="#555"); ax.text(5.0, -0.5, "norte · acceso", ha="center", fontsize=7, color="#555")
    ax.set_xlim(-0.6, 12.6); ax.set_ylim(-0.9, 17.5); ax.set_aspect("equal"); ax.axis("off"); ax.set_title("CUBIERTA: fotovoltaica, sedum y pluviales", fontsize=10, weight="bold")

if __name__ == "__main__":
    fig = plt.figure(figsize=(19, 13.5)); fig.suptitle("Instalaciones (esquema de intenciones, no proyecto de ejecución)", fontsize=14, weight="bold", x=.02, y=.995, ha="left")
    pos = [[.02, .52, .31, .44], [.35, .52, .31, .44], [.68, .52, .31, .44], [.02, .04, .31, .44], [.35, .04, .31, .44], [.68, .04, .31, .44]]
    fns = [lambda a: fontaneria(a, "PB"), lambda a: electricidad(a, "PB"), lambda a: clima(a, "PB"), lambda a: fontaneria(a, "PA"), lambda a: electricidad(a, "PA"), lambda a: clima(a, "PA")]
    for p, f in zip(pos, fns): f(fig.add_axes(p))
    fig.savefig("instalaciones.png", dpi=int(os.environ.get("DPI", 105)))
    fig2, ax = plt.subplots(figsize=(8, 10)); cubierta(ax); fig2.savefig("cubierta_solar.png", dpi=110, bbox_inches="tight")
    print("ok")
