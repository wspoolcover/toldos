"""Dossier PDF para obra: cimentación, estructura de acero, zunchos y forjados. BORRADOR preliminar."""
import math, json, datetime
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon as MPoly
from shapely.geometry import Polygon
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import casa_v3 as h
from perfiles import SECC

E = h.E
AVISO = "BORRADOR PRELIMINAR · NO CONSTRUIR SIN CÁLCULO Y FIRMA DE UN TÉCNICO COMPETENTE"

# ---------------------------------------------------------------- figura 1: cimentación
def fig_cimentacion():
    fig, ax = plt.subplots(figsize=(7.4, 9.6))
    Z = h.E["zapata"]["lado"]
    ax.add_patch(MPoly(h.PTS, closed=True, fc="#f7f4ee", ec="#222", lw=1.0, zorder=1))
    casa = Polygon(h.NB_FULL); sal = Polygon(h.SB)
    def banda(p, ancho, t):
        ext = p.buffer((ancho - t) / 2, join_style=2); inn = p.buffer(-(t + (ancho - t) / 2), join_style=2)
        return ext.difference(inn)
    for g, fc, ec, ls, lab in ((banda(casa, 1.10, h.T), "#e9e2d6", "#7a6a55", "--", "cimentación de la casa: NO conocida, se supone 1,10 m (hay que descubrirla)"),
                               (banda(sal, 0.60, h.T_S), "#cfd8e3", "#1f4e79", "-", "cimentación existente del salón: 0,60 m de ancho")):
        for gg in getattr(g, "geoms", [g]):
            ax.add_patch(MPoly(list(gg.exterior.coords), closed=True, fc=fc, ec=ec, ls=ls, lw=1.2, zorder=2, label=lab))
            for ring in gg.interiors: ax.add_patch(MPoly(list(ring.coords), closed=True, fc="white", ec=ec, ls=ls, lw=1.0, zorder=3))
    ax.add_patch(MPoly(list(casa.buffer(-h.T, join_style=2).exterior.coords), closed=True, fc="none", ec="#999", lw=.6, zorder=4))
    # riostras
    for cy in h.COL_Y: ax.add_patch(Rectangle((h.T / 2, cy - .2), h.XE - h.T, .4, fc="#b9b9b9", ec="#333", hatch="//", lw=.8, zorder=5))
    for lx in h.LINES_X: ax.add_patch(Rectangle((lx - .2, h.COL_Y[0]), .4, h.COL_Y[1] - h.COL_Y[0], fc="#b9b9b9", ec="#333", hatch="//", lw=.8, zorder=5))
    ax.add_patch(Rectangle((0, 0), 0, 0, fc="#b9b9b9", ec="#333", hatch="//", label="riostras de hormigón 0,40 × 0,40 m entre zapatas"))
    n = 1
    for cy in h.COL_Y:
        for lx in h.LINES_X:
            ax.add_patch(Rectangle((lx - Z / 2, cy - Z / 2), Z, Z, fc="#f2c94c", ec="#8a6d00", lw=1.4, zorder=6))
            ax.add_patch(Rectangle((lx - .07, cy - .07), .14, .14, fc="#d9601e", ec="#000", lw=.8, zorder=7))
            ax.text(lx, cy - Z / 2 - .10, f"Z{n}", ha="center", va="top", fontsize=8, weight="bold", zorder=8); n += 1
    ax.add_patch(Rectangle((0, 0), 0, 0, fc="#f2c94c", ec="#8a6d00", label=f"zapatas de pilar {Z:.2f} × {Z:.2f} m, canto 0,60 m (pilar HEB 120 en el centro)"))
    ax.annotate("", xy=(3.10 - Z / 2, 6.55), xytext=(3.10 + Z / 2, 6.55), arrowprops=dict(arrowstyle="<->", lw=.9)); ax.text(3.10, 6.35, f"{Z:.2f}", ha="center", va="top", fontsize=8)
    ax.text(-0.9, 15.6, "Ejes: x desde el muro oeste de la casa,\ny desde la fachada de la calle (abajo).\nMedidas en metros.", fontsize=7, va="top")
    ax.text(-0.9, 17.0, "CIMENTACIÓN · planta (calle abajo)", fontsize=10, weight="bold")
    ax.text(4.55, -0.9, "calle · NORTE", ha="center", fontsize=8, color="#555"); ax.text(4.55, 17.1, "fondo · SUR", ha="center", fontsize=8, color="#555") if False else None
    ax.legend(loc="lower left", fontsize=6.6, framealpha=.95, bbox_to_anchor=(0.0, 0.0))
    ax.set_xlim(-1.0, 13.3); ax.set_ylim(-1.0, 17.4); ax.set_aspect("equal"); ax.grid(True, ls=":", lw=.4, alpha=.5); ax.tick_params(labelsize=7)
    fig.tight_layout(); fig.savefig("pdf_cimentacion.png", dpi=170); plt.close(fig)


# ---------------------------------------------------------------- figura 2: secciones tipo
def fig_secciones():
    fig, axs = plt.subplots(1, 3, figsize=(13, 6.6))
    def r(ax, x, y, w, hh, fc, hatch=None, ec="#222", lw=1.0): ax.add_patch(Rectangle((x, y), w, hh, fc=fc, ec=ec, lw=lw, hatch=hatch))
    def dim(ax, x0, y0, x1, y1, txt, off=0.0, vert=False):
        ax.annotate("", xy=(x0, y0), xytext=(x1, y1), arrowprops=dict(arrowstyle="<->", lw=.8))
        ax.text((x0 + x1) / 2 + (off if vert else 0), (y0 + y1) / 2 + (0 if vert else off), txt, ha="center", va="center", fontsize=7.5, rotation=90 if vert else 0, bbox=dict(fc="white", ec="none", pad=.5))
    # A) muro de ladrillo del salón
    a = axs[0]; a.set_title("A · Muro del salón (ladrillo 25 cm)", fontsize=10, weight="bold")
    r(a, -0.30, -0.60, 0.60, 0.60, "#cfd8e3", "..")                       # zapata corrida 60
    r(a, -0.125, 0, 0.25, 3.02, "#d9a066", "--")                           # muro
    r(a, -0.125, 3.02, 0.25, 0.25, "#8c8c8c", "xx")                        # zuncho superior
    r(a, 0.125, 3.04, 1.0, 0.22, "#c9c9d0", "||")                          # forjado (parte)
    r(a, -0.125, 0.0, 0.25, 0.04, "#333")
    a.plot([-1.2, 1.4], [0, 0], color="#6b5a3d", lw=1.4); a.text(1.38, 0.05, "terreno / suelo", fontsize=7, ha="right")
    dim(a, -0.30, -0.75, 0.30, -0.75, "0,60"); dim(a, -0.42, -0.60, -0.42, 0, "≥ 0,60 (comprobar)", vert=True, off=-0.15); dim(a, 0.45, 0, 0.45, 3.02, "≈ 3,0 libre", vert=True, off=0.15)
    a.annotate("zuncho superior 25×25\n4Ø12 + cercos Ø6/20\n(orientativo)", xy=(0.125, 3.15), xytext=(-1.25, 3.7), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    a.annotate("forjado vigueta pretensada\n(25+5) apoyada ≥ 10 cm", xy=(0.6, 3.15), xytext=(0.15, 3.85), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    a.annotate("pilar de atado 25×25\n(esquinas y cada 3,5-4 m)", xy=(-0.125, 1.4), xytext=(-1.25, 1.6), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    a.set_xlim(-1.4, 1.6); a.set_ylim(-1.1, 4.4); a.set_aspect("equal"); a.axis("off")
    # B) muro de la casa
    b = axs[1]; b.set_title("B · Muro existente de la casa (mampostería 55 cm)", fontsize=10, weight="bold")
    r(b, -0.55, -0.60, 1.10, 0.60, "#e9e2d6", "..", ec="#7a6a55")
    r(b, -0.275, 0, 0.55, 2.95, "#cdbfa5", "oo")
    r(b, -0.275, 2.95, 0.55, 0.30, "#8c8c8c", "xx")
    r(b, 0.275, 2.98, 1.0, 0.27, "#c9c9d0", "||")
    b.plot([-1.3, 1.5], [0, 0], color="#6b5a3d", lw=1.4)
    dim(b, -0.55, -0.75, 0.55, -0.75, "1,10 (supuesta)"); dim(b, -0.275, 3.45, 0.275, 3.45, "0,55")
    b.annotate("zuncho superior 55×25\n6Ø12 + cercos Ø6/20\n(orientativo)", xy=(0.275, 3.1), xytext=(0.5, 3.75), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    b.annotate("la cimentación existente hay que\ndescubrirla y medirla antes de cargar", xy=(0.55, -0.3), xytext=(0.7, -0.6), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    b.set_xlim(-1.4, 2.2); b.set_ylim(-1.1, 4.4); b.set_aspect("equal"); b.axis("off")
    # C) pilar HEB 120 + zapata + viga embebida
    c = axs[2]; c.set_title("C · Pilar HEB 120, zapata y riostra", fontsize=10, weight="bold")
    r(c, -0.65, -0.60, 1.30, 0.60, "#f2c94c", "..", ec="#8a6d00")
    r(c, -0.20, -0.50, 0.40, 0.40, "#b9b9b9", "//")                                           # riostra (sección)
    c.add_patch(Rectangle((-0.06, 0.02), 0.12, 3.0, fc="#d9601e", ec="#000", lw=1.0)); r(c, -0.15, 0.0, 0.30, 0.02, "#333")     # pilar y placa base
    r(c, -0.55, 2.95, 1.10, 0.22, "#c9c9d0", "||")                                           # forjado
    r(c, -0.07, 2.99, 0.14, 0.14, "#d9601e")                                                 # viga HEB 140 embebida (ala)
    c.plot([-1.3, 1.5], [0, 0], color="#6b5a3d", lw=1.4)
    dim(c, -0.65, -0.75, 0.65, -0.75, "1,30"); dim(c, 0.78, -0.60, 0.78, 0, "0,60", vert=True, off=0.13)
    c.annotate("placa base y anclajes:\nlos define el técnico", xy=(0, 0.03), xytext=(0.35, 0.5), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    c.annotate("HEB 120 (pilar, oculto\nen tabique o muro)", xy=(0.06, 1.6), xytext=(0.3, 1.9), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    c.annotate("viga HEB 140 embebida\nen el forjado", xy=(0.07, 3.05), xytext=(-1.25, 3.55), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    c.annotate("riostra 40×40\n4Ø12 + cercos Ø8/25\n(orientativo)", xy=(-0.2, -0.3), xytext=(-1.28, -0.35), fontsize=7.5, arrowprops=dict(arrowstyle="-", lw=.6))
    c.set_xlim(-1.4, 1.6); c.set_ylim(-1.1, 4.4); c.set_aspect("equal"); c.axis("off")
    fig.tight_layout(); fig.savefig("pdf_secciones.png", dpi=170); plt.close(fig)


# ---------------------------------------------------------------- despiece de acero
def despiece():
    filas = {}
    def add(nombre, sec, L):
        k = (nombre, sec, round(L, 2)); filas[k] = filas.get(k, 0) + 1
    hb = SECC[E["viga_cub"]["perfil"]][0] / 1000
    for g in h.STEEL["pilares"]: add("Pilar", g[2], h.zt2 - hb)
    for cat, niv in (("vigas_forjado", "forjado"), ("vigas_cubierta", "cubierta")):
        for xa, ya, xb, yb, sec in h.STEEL[cat]:
            L = math.hypot(xb - xa, yb - ya)
            nom = "Viga N-S continua" if abs(xa - xb) < 1e-6 and L > 6 else ("Viga de borde del saliente" if abs(xa - xb) < 1e-6 else "Viga de fachada (tramo)")
            add(f"{nom} · {niv}", sec, L)
    for g in h.STEEL["dintel"]: add("Dintel de la cristalera", g[4], math.hypot(g[2] - g[0], g[3] - g[1]))
    for g in h.STEEL["dinteles"]: add("Dintel de puerta o ventana", g[4], math.hypot(g[2] - g[0], g[3] - g[1]))
    tabla = []; total = 0
    for i, ((nom, sec, L), n) in enumerate(sorted(filas.items(), key=lambda kv: (kv[0][0], kv[0][1], -kv[0][2])), 1):
        kg = SECC[sec][7] * L * n; total += kg
        tabla.append([f"M{i}", nom, sec, str(n), f"{L:.2f}", f"{kg:.0f}"])
    return tabla, total


# ---------------------------------------------------------------- PDF
def build():
    fig_cimentacion(); fig_secciones()
    tabla, total = despiece()
    ss = getSampleStyleSheet()
    H1 = ParagraphStyle("H1", parent=ss["Heading1"], fontSize=17, spaceAfter=4, textColor=colors.HexColor("#1f2d3a"))
    H2 = ParagraphStyle("H2", parent=ss["Heading2"], fontSize=12, spaceBefore=6, spaceAfter=3)
    B = ParagraphStyle("B", parent=ss["BodyText"], fontSize=9.4, leading=12.4)
    S = ParagraphStyle("S", parent=B, fontSize=8, leading=10, textColor=colors.HexColor("#444"))
    W = ParagraphStyle("W", parent=B, fontSize=10.5, leading=14, textColor=colors.HexColor("#8b1a10"), backColor=colors.HexColor("#fdeceb"), borderPadding=6, spaceBefore=4, spaceAfter=6)
    pw, ph = landscape(A4)
    def pie(c, d):
        c.saveState(); c.setFont("Helvetica-Bold", 8); c.setFillColor(colors.HexColor("#b02a1a")); c.drawString(12 * mm, ph - 8 * mm, AVISO)
        c.setFillColor(colors.HexColor("#555")); c.setFont("Helvetica", 8)
        c.drawString(12 * mm, 6 * mm, "Vivienda unifamiliar · Pol. 33, parc. 198, San Roque, Albox (Almería) · Medidas en metros salvo indicación · Acero S275JR · Hormigón HA-25")
        c.drawRightString(pw - 12 * mm, 6 * mm, f"Hoja {d.page}"); c.restoreState()
    doc = BaseDocTemplate("dossier_obra.pdf", pagesize=landscape(A4), leftMargin=12 * mm, rightMargin=12 * mm, topMargin=13 * mm, bottomMargin=11 * mm, title="Dossier de obra: cimentación, estructura, zunchos", author="Borrador de diseño")
    doc.addPageTemplates([PageTemplate(id="p", frames=[Frame(12 * mm, 11 * mm, pw - 24 * mm, ph - 24 * mm, id="f", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], onPage=pie)])
    def tb(data, widths, head=True, fs=8.4):
        cs = ParagraphStyle("c", parent=B, fontSize=fs, leading=fs + 2.2)
        data = [[Paragraph(str(c), cs) if isinstance(c, str) else c for c in row] for row in data]
        t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
        st = [("FONTSIZE", (0, 0), (-1, -1), fs), ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#999")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
              ("TOPPADDING", (0, 0), (-1, -1), 2.4), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4)]
        if head: st += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e9ee")), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]
        t.setStyle(TableStyle(st)); return t
    P = lambda t, s=B: Paragraph(t, s)
    el = []
    # 1 · portada
    el += [P("Dossier de obra: cimentación, estructura de acero y zunchos", H1),
           P("Vivienda unifamiliar en Albox · Salón nuevo de ladrillo, casa existente de mampostería, dos plantas y cubierta plana", B),
           P("ESTE DOCUMENTO ES UN BORRADOR PRELIMINAR. Las secciones del acero, las zapatas y los armados salen de un predimensionado sin verificar por un técnico. No se debe hormigonar ni montar acero solo con esta hoja: primero un arquitecto o ingeniero tiene que calcularlo, comprobar el terreno y firmarlo.", W),
           P("Qué contiene", H2),
           tb([["Hoja", "Contenido"], ["2", "Cimentación: zapatas, riostras y suelo"], ["3", "Secciones tipo: muros, zunchos, zapata y pilar"],
               ["4", "Estructura de acero: vigas HEB en forjado y cubierta"], ["5", "Lista de piezas de acero (despiece) con longitudes y pesos"],
               ["6", "Forjados, zunchos, orden de obra y puntos que confirmar"]], [20 * mm, 150 * mm]),
           Spacer(1, 6),
           P("Resumen de la obra", H2),
           tb([["Elemento", "Dato"],
               ["Muros laterales del salón", "Ladrillo de 25 cm, ya con cimentación corrida de 60 cm (a comprobar en obra: ancho y profundidad)"],
               ["Casa existente", "Muros de mampostería de 50-60 cm; cimentación no conocida"],
               ["Forjados", "Vigueta pretensada y bovedilla de poliestireno: (25+5)×71 en el salón, (17+5)×71 en la casa y la cubierta"],
               ["Acero", f"Pilares HEB 120 ×6, vigas HEB 140/160/120 y dinteles IPE: unos {total:.0f} kg"],
               ["Atado", "Zuncho superior de hormigón armado en cada nivel, riostras entre zapatas y pilares de atado en el ladrillo"],
               ["Terreno", "Se ha supuesto una tensión admisible de 150 kPa. Sin estudio geotécnico no está comprobada"]], [55 * mm, 205 * mm]),
           PageBreak()]
    # 2 · cimentación (plano a la izquierda, notas a la derecha)
    zs = []; n = 1
    for cy in h.COL_Y:
        for lx in h.LINES_X: zs.append([f"Z{n}", f"{lx:.2f}", f"{cy:.2f}"]); n += 1
    der = [P("Hoja 2 · Cimentación", H1),
           tb([["Elemento", "Medidas y notas"],
               ["Cimentación corrida del salón", "0,60 m de ancho (ya hecha). Carga de servicio ≈ 40 kN/m → ≈ 67 kPa; cumple frente a 150 kPa supuestos. Comprobar en obra ancho y profundidad"],
               ["Zapatas Z1-Z6", "1,30 × 1,30 m, canto 0,60 m, hormigón de limpieza de 10 cm. Malla inferior en dos direcciones (orientativo Ø12 cada 20 cm)"],
               ["Riostras", "0,40 × 0,40 m entre las 6 zapatas y con la cimentación de los muros (orientativo 4Ø12 + cercos Ø8 cada 25 cm)"],
               ["Cimentación de la casa", "No conocida: descubrirla en varios puntos, medir ancho y profundidad y comprobar antes de cargar más los muros"],
               ["Hormigón y acero", "HA-25, B500S, a confirmar por el técnico"]], [34 * mm, 82 * mm], fs=7.6),
           Spacer(1, 3),
           P("<b>Terreno:</b> 150 kPa es una suposición para suelo normal. Ver el terreno abierto y, si hay dudas (rellenos, arcillas, agua), pedir estudio geotécnico. Apoyar siempre en terreno firme, nunca en relleno. Albox está en zona sísmica: las riostras no se omiten.", ParagraphStyle("t", parent=B, fontSize=8, leading=10)),
           Spacer(1, 3),
           tb([["Zapata", "x (m)", "y (m)"]] + zs, [24 * mm, 30 * mm, 30 * mm], fs=7.6)]
    izq = Image("pdf_cimentacion.png", width=137 * mm, height=137 * mm * 9.6 / 7.4)
    t2 = Table([[izq, der]], colWidths=[142 * mm, 120 * mm]); t2.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 2)]))
    el += [t2, PageBreak()]
    # 3 · secciones
    el += [P("Hoja 3 · Secciones tipo: muros, zunchos, zapata y pilar", H1), Image("pdf_secciones.png", width=250 * mm, height=250 * mm * 6.6 / 13),
           P("Los armados marcados como orientativos son valores habituales para hacerse una idea. No están calculados: los fija el técnico.", S), PageBreak()]
    # 4 · estructura
    el += [P("Hoja 4 · Estructura de acero: vigas y pilares", H1), Image("estructura_planos.png", width=192 * mm, height=192 * mm * 9.8 / 13),
           P("Las tres vigas largas norte-sur son de una sola pieza continua sobre el pilar central. Las vigas HEB quedan embebidas en el canto del forjado: las viguetas pretensadas apoyan en el ala inferior y el hormigón las cubre. Los pilares van ocultos en muros y tabiques.", S), PageBreak()]
    # 5 · despiece
    el += [P("Hoja 5 · Lista de piezas de acero (S275JR)", H1),
           tb([["Marca", "Elemento", "Perfil", "Uds.", "Longitud (m)", "Peso total (kg)"]] + tabla + [["", "TOTAL", "", "", "", f"{total:.0f}"]],
              [18 * mm, 100 * mm, 28 * mm, 16 * mm, 32 * mm, 34 * mm], fs=8),
           Spacer(1, 4), P("Longitudes de corte teóricas: hay que sumar apoyos, placas y mermas según el taller. Las uniones y las placas de anclaje no están diseñadas. Protección: imprimación antioxidante como mínimo; si el proyecto exige resistencia al fuego, la protección la define el técnico.", S), PageBreak()]
    # 6 · zunchos, forjados, orden
    el += [P("Hoja 6 · Forjados, zunchos y orden de obra", H1),
           tb([["Elemento", "Descripción"],
               ["Zuncho superior (cada nivel)", "Banda de hormigón armado en la coronación de todos los muros, a la altura del forjado. Ancho igual al del muro (25 o 55 cm) y unos 25 cm de canto. Continuo, sin cortes; se hormigona a la vez que el forjado. Orientativo: 4Ø12 (6Ø12 en muro de 55) con cercos Ø6 cada 20 cm"],
               ["Zuncho inferior", "Las riostras entre zapatas (0,40 × 0,40 m) atan la cimentación. Sobre las zapatas corridas de los muros conviene un encadenado inferior continuo si el técnico lo pide"],
               ["Pilares de atado (ladrillo)", "Pilares de hormigón de 25 × 25 cm en las esquinas y cada 3,5-4 m de muro (unos 3 por muro lateral del salón), unidos al zuncho superior e inferior"],
               ["Forjado del salón", "Vigueta pretensada T-2 y bovedilla de poliestireno, (25+5)×71, luz 5,75 m. Datos de la ficha del fabricante Prearcon (T-18): el fabricante debe confirmar esa luz y el armado"],
               ["Forjado de la casa y de la cubierta", "Vigueta T-1 y bovedilla de poliestireno, (17+5)×71, apoyada en las vigas HEB o en los zunchos"],
               ["Dinteles de huecos", "Perfiles IPE 100/120 según la lista de piezas, con 20 cm de apoyo a cada lado"]], [55 * mm, 205 * mm]),
           P("Orden de obra recomendado", H2),
           P("1) Replantear y abrir las zapatas Z1-Z6; ver el terreno. 2) Zapatas, riostras y arranque de pilares. 3) Descubrir y comprobar la cimentación de la casa existente. 4) Muros de ladrillo del salón con pilares de atado. 5) Montar pilares y vigas de acero. 6) Zuncho superior y forjado del salón. 7) Muros y forjado de la casa; zuncho. 8) Forjado de cubierta y zuncho superior.", B),
           P("Antes de empezar, que un técnico confirme", H2),
           P("· Tensión admisible del terreno y cotas de cimentación. · Estado real de los muros de mampostería. · Refuerzo frente a sismo en Albox, sobre todo en la dirección este-oeste (cruces de acero, pantallas de hormigón o mallazo con mortero). · Armados de zunchos, zapatas y riostras. · Placas base, anclajes y uniones del acero. · Luz del forjado del salón con el fabricante. · Resistencia al fuego exigida.", B)]
    doc.build(el)
    print("ok", round(total))

if __name__ == "__main__": build()
