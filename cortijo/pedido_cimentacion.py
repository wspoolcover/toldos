"""Pedido 1: hierro de la cimentación (parrilla de zapatas y riostras), con lista de cortes y barras de 12 m.
Genera pedido_1_hierro_cimentacion.xlsx y pdf/Pedido_1_hierro_cimentacion.pdf. Armados de docs/10 (propuesta; los confirma el técnico)."""
import math, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

KG = {8: 0.395, 12: 0.888, 16: 1.578}
BARRA = 12.0
T_CASA = 0.55
ZAP, LC = 1.60, 3.25
REC, PAT = 0.05, 0.20                        # recubrimiento lateral de la parrilla y patilla de cada extremo (desarrollo +0,40 m)
MARGEN_C = 1.05


def parrilla(a, b, paso=0.15):
    """Barras de una zapata a × b: n barras paralelas al lado a (largo a − 2·rec + 2·pat) y n barras paralelas al lado b."""
    n_a = math.floor((b - 2 * REC) / paso) + 1; n_b = math.floor((a - 2 * REC) / paso) + 1
    return [(round(a - 2 * REC + 2 * PAT, 2), n_a), (round(b - 2 * REC + 2 * PAT, 2), n_b)]


def corta(piezas, largo=BARRA, kerf=0.0):
    """Primera cabida decreciente: devuelve la lista de barras de 12 m, cada una con las piezas que salen de ella."""
    barras = []
    for p in sorted(piezas, reverse=True):
        for b in barras:
            if sum(b) + p + kerf * len(b) <= largo + 1e-9:
                b.append(p); break
        else:
            barras.append([p])
    return barras


def patrones(barras):
    """Agrupa barras iguales: [(nº de barras, piezas, sobrante)]."""
    cuenta = {}
    for b in barras:
        k = tuple(sorted(b, reverse=True)); cuenta[k] = cuenta.get(k, 0) + 1
    return [(n, list(k), BARRA - sum(k)) for k, n in sorted(cuenta.items(), key=lambda x: -x[1])]


def texto_patron(k):
    from collections import Counter
    return " + ".join(f"{n} × {l:.2f}" for l, n in sorted(Counter(k).items(), reverse=True))


# ---- Ø12: parrilla de las 4 zapatas (2 Z-1 de 1,60 × 1,60 y 2 Z-2 de 3,25 × 1,60)
p12 = []
for (a, b, uds) in ((ZAP, ZAP, 2), (LC, ZAP, 2)):
    for largo, n in parrilla(a, b):
        p12 += [largo] * (n * uds)
b12 = corta(p12)
c12 = {}
for l in p12: c12[l] = c12.get(l, 0) + 1

# ---- Ø16: riostras (8 barras en cada una: 4 arriba y 4 abajo)
L_EO, L_NS = 2 * 9.0, 3 * 4.2
p16 = [round(9.0 + 0.8, 2)] * 16 + [round(4.2 + 1.0, 2)] * 24            # E-O: eje a eje de muros + 0,40 m de anclaje por extremo; N-S: de zapata a zapata + 0,50 m por extremo
b16 = corta(p16)

# ---- Ø8: cercos de las riostras (40 × 50: interior 34 × 44, corte = perímetro + 15 cm de ganchos)
corte_c = 2 * (0.34 + 0.44) + 0.15
n_c = 2 * (math.floor(9.0 / 0.20) + 1) + 3 * (math.floor(4.2 / 0.20) + 1)
n_c_ped = math.ceil(n_c * MARGEN_C)
por_barra = math.floor(BARRA / corte_c)
b8 = math.ceil(n_c_ped / por_barra)

# ---- opcional: 30 m de zuncho del muro exterior (25 × 30, 4Ø16 + 4Ø16, cercos Ø8 cada 15 cm)
EXT = 30.0
b16_ext = math.ceil(EXT * 8 * 1.10 / BARRA)
c_ext = math.ceil((math.floor(EXT / 0.15) + 1) * MARGEN_C); corte_ext = 2 * (0.19 + 0.24) + 0.15
b8_ext = math.ceil(c_ext / math.floor(BARRA / corte_ext))

tot = {12: len(b12), 16: len(b16), 8: b8}
kg = {d: n * BARRA * KG[d] for d, n in tot.items()}
print("Ø12:", len(b12), "barras;", "Ø16:", len(b16), "barras;", "Ø8:", b8, "barras ->", {d: round(k) for d, k in kg.items()}, "total", round(sum(kg.values())), "kg")
print("cercos:", n_c, "→", n_c_ped, "de", round(corte_c, 2), "m;", por_barra, "por barra | extra muro exterior:", b16_ext, "barras Ø16 +", b8_ext, "Ø8")
print("patrones Ø12:", [(n, texto_patron(k), round(s, 2)) for n, k, s in patrones(b12)])
print("patrones Ø16:", [(n, texto_patron(k), round(s, 2)) for n, k, s in patrones(b16)])

# ---------------- Excel ----------------
AZ = PatternFill("solid", fgColor="DCE6F1"); NA = PatternFill("solid", fgColor="FFF2CC"); NEG = Font(bold=True)
fino = Side(style="thin", color="BBBBBB"); BORDE = Border(left=fino, right=fino, top=fino, bottom=fino)
wb = Workbook(); ws = wb.active; ws.title = "Pedido 1"
ws.append(["PEDIDO 1 · hierro de la cimentación (zapatas y riostras) · acero B 500 S"]); ws["A1"].font = Font(bold=True, size=12); ws.append([])
ws.append(["Qué", "Se pide en", "Cantidad", "Metros", "Kilos"])
for c in ws[3]: c.font = NEG; c.fill = AZ
ws.append(["Ø12 · parrilla de las 4 zapatas", "barras de 12 m", tot[12], tot[12] * 12, round(kg[12])])
ws.append(["Ø16 · riostras (8 barras en cada una)", "barras de 12 m", tot[16], tot[16] * 12, round(kg[16])])
ws.append(["Ø8 · cercos de las riostras (cuadrados, 34 × 44 cm de medida interior)", "barras de 12 m para doblar, o cercos hechos", f"{b8} barras ({n_c_ped} cercos)", b8 * 12, round(kg[8])])
ws.append(["TOTAL", "", "", "", round(sum(kg.values()))])
for c in ws[ws.max_row]: c.font = NEG
ws.append([]); ws.append(["Opcional: 30 m de zuncho del muro exterior (25 × 30, 4Ø16 + 4Ø16, cercos Ø8 cada 15 cm)", "", "", "", ""])
for c in ws[ws.max_row]: c.font = NEG; c.fill = NA
ws.append(["Ø16", "barras de 12 m", b16_ext, b16_ext * 12, round(b16_ext * 12 * KG[16])])
ws.append(["Ø8 cercos (19 × 24 cm)", "barras de 12 m para doblar", f"{b8_ext} barras ({c_ext} cercos)", b8_ext * 12, round(b8_ext * 12 * KG[8])])
for col, a in zip("ABCDE", (70, 38, 24, 10, 10)): ws.column_dimensions[col].width = a
for row in ws.iter_rows(min_row=3, max_row=ws.max_row):
    for c in row:
        if c.column > 1 and c.value not in (None, ""): c.alignment = Alignment(horizontal="center")
w2 = wb.create_sheet("Cortes")
w2.append(["Ø", "Pieza (m)", "Nº de piezas", "Uso", "Doblado"])
for l, n in sorted(c12.items(), reverse=True):
    w2.append([12, l, n, "Zapatas Z-1 y Z-2" if l < 3 else "Zapatas Z-2, sentido largo", "patilla de 20 cm en cada extremo"])
w2.append([16, 9.80, 16, "Riostras este-oeste (y = 7,60 y y = 11,80)", "ganchos de 40 cm en los extremos, si el técnico los pide"])
w2.append([16, 5.20, 24, "Riostras norte-sur (x = 3,10; 5,55; 7,20)", "recta; sobresale 50 cm dentro de cada zapata"])
w2.append([8, round(corte_c, 2), n_c_ped, "Cercos de riostra, cada 20 cm", "cuadrado de 34 × 44 cm de medida interior, ganchos a 135°"])
for c in w2[1]: c.font = NEG; c.fill = AZ
for col, a in zip("ABCDE", (6, 12, 14, 48, 56)): w2.column_dimensions[col].width = a
w3 = wb.create_sheet("Plan de corte")
w3.append(["Ø", "Barras de 12 m", "Cómo se corta cada una", "Sobrante por barra (m)"])
for d, bs in ((12, b12), (16, b16)):
    for n, k, s in patrones(bs):
        w3.append([d, n, texto_patron(k), round(s, 2)])
for c in w3[1]: c.font = NEG; c.fill = AZ
for col, a in zip("ABCD", (6, 16, 60, 22)): w3.column_dimensions[col].width = a
w4 = wb.create_sheet("Notas")
for t in ("Parrilla: Ø12 cada 15 cm en los dos sentidos, 5 cm de recubrimiento lateral y patillas de 20 cm (desarrollo = largo + 0,40 m).",
          "Riostras RI-1 de 40 × 50 cm: 4Ø16 arriba + 4Ø16 abajo, cercos Ø8 cada 20 cm; longitudes: 2 × 9,00 m (este-oeste) + 3 × 4,20 m (norte-sur).",
          "El plan de corte aprovecha cada barra de 12 m; los sobrantes cubren las mermas y los solapes. No hay margen añadido sobre el plan de corte.",
          "Si el técnico cambia el armado, hay que recalcular (`python pedido_cimentacion.py`).",
          "No son hierro de armar, pero se piden en el mismo viaje: 24 pernos de anclaje Ø20 de 40 cm con placa de 30 × 30 × 2 cm (6 pilares), cable de cobre desnudo de 35 mm² para el anillo de tierra (unos 70 m) y alambre de atar (unos 15 kg), más separadores de 5 cm (para las zapatas) y de 3 cm (para las riostras)."):
    w4.append([t])
w4.column_dimensions["A"].width = 160
wb.save("pedido_1_hierro_cimentacion.xlsx")

# ---------------- PDF ----------------
FUENTES = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LS", FUENTES + "LiberationSans-Regular.ttf")); pdfmetrics.registerFont(TTFont("LS-B", FUENTES + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFontFamily("LS", normal="LS", bold="LS-B", italic="LS", boldItalic="LS-B")
H1 = ParagraphStyle("h1", fontName="LS-B", fontSize=15, leading=18, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="LS-B", fontSize=10.5, leading=13, spaceBefore=7, spaceAfter=3)
B = ParagraphStyle("b", fontName="LS", fontSize=8.6, leading=11)
C = ParagraphStyle("c", fontName="LS", fontSize=8.4, leading=10.2)


def tabla(datos, anchos):
    t = Table([[Paragraph(str(x), C) for x in fila] for fila in datos], colWidths=anchos, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#999999")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce6f1")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    return t


os.makedirs("pdf", exist_ok=True)
doc = SimpleDocTemplate("pdf/Pedido_1_hierro_cimentacion.pdf", pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm, topMargin=12 * mm, bottomMargin=10 * mm, title="Pedido 1: hierro de la cimentación")
el = [Paragraph("Pedido 1 · hierro de la cimentación", H1),
      Paragraph("Zapatas y riostras. Acero corrugado B 500 S. Armados de la propuesta (docs/10); los confirma el técnico.", B), Spacer(1, 3), Paragraph("Lo que hay que pedir", H2)]
el.append(tabla([["Qué", "Se pide en", "Cantidad", "Kilos"],
                 ["Ø12 · parrilla de las 4 zapatas (cada 15 cm en los dos sentidos)", "barras de 12 m", f"<b>{tot[12]}</b>", round(kg[12])],
                 ["Ø16 · riostras (4 arriba + 4 abajo en cada una)", "barras de 12 m", f"<b>{tot[16]}</b>", round(kg[16])],
                 ["Ø8 · cercos de las riostras (cuadrados, 34 × 44 cm por dentro)", "barras de 12 m para doblar, o cercos hechos", f"<b>{b8}</b> barras ({n_c_ped} cercos de {corte_c:.2f} m)", round(kg[8])],
                 ["<b>TOTAL</b>", "", "", f"<b>{round(sum(kg.values()))}</b>"]],
                [88 * mm, 42 * mm, 36 * mm, 16 * mm]))
el.append(Paragraph("Lista de cortes (para que el proveedor corte y doble)", H2))
filas = [["Ø", "Largo", "Piezas", "Dónde", "Doblado"]]
for l, n in sorted(c12.items(), reverse=True):
    filas.append(["12", f"{l:.2f} m", n, "Zapatas Z-1 y Z-2" if l < 3 else "Zapatas Z-2, sentido largo", "patilla de 20 cm en cada extremo"])
filas += [["16", "9,80 m", 16, "Riostras este-oeste (y = 7,60 y y = 11,80)", "recta o con gancho de 40 cm"],
          ["16", "5,20 m", 24, "Riostras norte-sur (x = 3,10; 5,55; 7,20)", "recta"],
          ["8", f"{corte_c:.2f} m", n_c_ped, "Cercos de las riostras, cada 20 cm", "cuadrado de 34 × 44 cm por dentro, ganchos a 135°"]]
el.append(tabla(filas, [10 * mm, 20 * mm, 18 * mm, 72 * mm, 62 * mm]))
el.append(Paragraph("Cómo salen de las barras de 12 m", H2))
filas = [["Ø", "Barras", "Cada barra da", "Sobra"]]
for d, bs in ((12, b12), (16, b16)):
    for n, k, s in patrones(bs):
        filas.append([d, n, texto_patron(k), f"{s:.2f} m"])
filas.append([8, b8, f"{por_barra} cercos de {corte_c:.2f} m", f"{BARRA - por_barra * corte_c:.2f} m"])
el.append(tabla(filas, [10 * mm, 20 * mm, 112 * mm, 40 * mm]))
el.append(Paragraph("Opcional: 30 m de zuncho del muro exterior", H2))
el.append(tabla([["Qué", "Barras de 12 m", "Kilos"],
                 ["Ø16 (4 arriba + 4 abajo, 25 × 30 cm, con solapes)", b16_ext, round(b16_ext * 12 * KG[16])],
                 [f"Ø8 cercos de 19 × 24 cm ({c_ext} cercos de {corte_ext:.2f} m, cada 15 cm)", b8_ext, round(b8_ext * 12 * KG[8])]], [110 * mm, 36 * mm, 30 * mm]))
el.append(Spacer(1, 4))
for t in ("<b>Para pedir en el mismo viaje (no es hierro de armar):</b> 24 pernos de anclaje Ø20 de 40 cm con placa de 30 × 30 × 2 cm (6 pilares); cable de cobre desnudo de 35 mm² para el anillo de tierra (unos 70 m); alambre de atar (unos 15 kg); separadores de 5 cm para las zapatas y de 3 cm para las riostras.",
          "<b>Antes de hormigonar la línea y = 7,60</b> hay que resolver tres puntos (ver la comprobación): la cimentación existente que coincide con las zapatas, el colector Ø150 que cruza la riostra y la zapata Z-2, y la escalera, que no tiene cimentación prevista. El hierro de este pedido no cambia por ello; los cortes sí podrían cambiar en las zapatas de esa línea."):
    el.append(Paragraph(t, B)); el.append(Spacer(1, 2))
doc.build(el)
print("ok: pedido_1_hierro_cimentacion.xlsx y pdf/Pedido_1_hierro_cimentacion.pdf")
