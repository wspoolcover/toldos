"""Pedido 1: hierro de la cimentación (parrilla de zapatas, riostras y zanja perimetral de 40 × 40), con lista de cortes y barras de 12 m.
Genera pedido_1_hierro_cimentacion.xlsx y pdf/Pedido_1_hierro_cimentacion.pdf. Armados de docs/10 (propuesta; los confirma el técnico)."""
import math, os
from collections import Counter
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from anillos_cimentacion import L_ANILLO, L_CIERRE, L_RIOSTRAS

KG = {8: 0.395, 12: 0.888, 16: 1.578}
BARRA = 12.0
ZAP, LC = 1.60, 3.25
REC, PAT = 0.05, 0.20                        # recubrimiento lateral de la parrilla y patilla de cada extremo (desarrollo +0,40 m)
MARGEN_C = 1.05
LAP = 0.80                                   # solape de las barras de Ø16 (50 diámetros)


def parrilla(a, b, paso=0.15):
    n_a = math.floor((b - 2 * REC) / paso) + 1; n_b = math.floor((a - 2 * REC) / paso) + 1
    return [(round(a - 2 * REC + 2 * PAT, 2), n_a), (round(b - 2 * REC + 2 * PAT, 2), n_b)]


def corta(piezas, largo=BARRA):
    """Primera cabida decreciente: barras de 12 m con las piezas que salen de cada una."""
    barras = []
    for p in sorted(piezas, reverse=True):
        for b in barras:
            if sum(b) + p <= largo + 1e-9:
                b.append(p); break
        else:
            barras.append([p])
    return barras


def patrones(barras):
    cuenta = {}
    for b in barras:
        k = tuple(sorted(b, reverse=True)); cuenta[k] = cuenta.get(k, 0) + 1
    return [(n, list(k), BARRA - sum(k)) for k, n in sorted(cuenta.items(), key=lambda x: -x[1])]


def texto_patron(k):
    return " + ".join(f"{n} × {l:.2f}" for l, n in sorted(Counter(k).items(), reverse=True))


# ---- Ø12: parrilla de las 4 zapatas (2 Z-1 de 1,60 × 1,60 y 2 Z-2 de 3,25 × 1,60)
p12 = []
for (a, b, uds) in ((ZAP, ZAP, 2), (LC, ZAP, 2)):
    for largo, n in parrilla(a, b):
        p12 += [largo] * (n * uds)
b12 = corta(p12)
c12 = Counter(p12)

# ---- Ø16 de las riostras (8 barras en cada una: 4 arriba y 4 abajo)
p16 = [round(9.0 + 0.8, 2)] * 16 + [round(4.2 + 1.0, 2)] * 24
b16 = corta(p16)

# ---- Ø16 del anillo perimetral 40 × 40 (8 barras: 4 arriba y 4 abajo) y del cierre del saliente
n_tramos = math.ceil((L_ANILLO + 2 * LAP) / (BARRA - LAP))               # barras de 12 m por línea, con solape
b16_anillo = 8 * n_tramos
p_cierre = round(L_CIERRE + 0.8, 2)                                      # + 0,40 m de entrega en cada extremo
b16_cierre = math.ceil(8 / math.floor(BARRA / p_cierre))
b16_anillo_tot = b16_anillo + b16_cierre

# ---- Ø8: cercos de las riostras (40 × 50: interior 34 × 44) y del anillo (40 × 40: interior 34 × 34); corte = perímetro + 15 cm de ganchos
corte_r = 2 * (0.34 + 0.44) + 0.15
n_r = math.ceil((2 * (math.floor(9.0 / 0.20) + 1) + 3 * (math.floor(4.2 / 0.20) + 1)) * MARGEN_C)
corte_a = 2 * (0.34 + 0.34) + 0.15
n_a = math.ceil(((math.floor(L_ANILLO / 0.15) + 1) + (math.floor(L_CIERRE / 0.15) + 1)) * MARGEN_C)
b8_r = math.ceil(n_r / math.floor(BARRA / corte_r)); b8_a = math.ceil(n_a / math.floor(BARRA / corte_a))

tot = {12: len(b12), 16: len(b16) + b16_anillo_tot, 8: b8_r + b8_a}
kg = {d: n * BARRA * KG[d] for d, n in tot.items()}
total_kg = sum(kg.values())
kg_anillo = b16_anillo_tot * BARRA * KG[16] + b8_a * BARRA * KG[8]

# comparación: anillo con el armado del arquitecto (4Ø12 en 40 × 30; aquí 4Ø12 con cercos Ø8 cada 20 cm)
b12_arq = math.ceil(4 * (L_ANILLO + L_CIERRE) * 1.10 / BARRA)
n_arq = math.ceil(((math.floor(L_ANILLO / 0.20) + 1) + (math.floor(L_CIERRE / 0.20) + 1)) * MARGEN_C)
b8_arq = math.ceil(n_arq / math.floor(BARRA / corte_a))
kg_anillo_arq = b12_arq * BARRA * KG[12] + b8_arq * BARRA * KG[8]
m3_anillo = (L_ANILLO + L_CIERRE) * 0.4 * 0.4

print("Ø12:", tot[12], "| Ø16:", tot[16], f"(riostras {len(b16)} + anillo {b16_anillo_tot})", "| Ø8:", tot[8], f"(riostras {b8_r} + anillo {b8_a})", "->", {d: round(k) for d, k in kg.items()}, "total", round(total_kg), "kg")
print(f"anillo {L_ANILLO:.1f} + cierre {L_CIERRE:.1f} m: Ø16 {b16_anillo_tot} barras ({n_tramos} por línea + {b16_cierre}), cercos {n_a} de {corte_a:.2f} m = {b8_a} barras; {round(kg_anillo)} kg; con 4Ø12: {round(kg_anillo_arq)} kg; {m3_anillo:.1f} m³")

# ---------------- Excel ----------------
AZ = PatternFill("solid", fgColor="DCE6F1"); NA = PatternFill("solid", fgColor="FFF2CC"); NEG = Font(bold=True)
fino = Side(style="thin", color="BBBBBB"); BORDE = Border(left=fino, right=fino, top=fino, bottom=fino)
wb = Workbook(); ws = wb.active; ws.title = "Pedido 1"
ws.append(["PEDIDO 1 · hierro de la cimentación (zapatas, riostras y zanja perimetral 40 × 40) · acero B 500 S"]); ws["A1"].font = Font(bold=True, size=12); ws.append([])
ws.append(["Qué", "Se pide en", "Cantidad", "Metros", "Kilos"])
for c in ws[3]: c.font = NEG; c.fill = AZ
ws.append(["Ø12 · parrilla de las 4 zapatas", "barras de 12 m", tot[12], tot[12] * 12, round(kg[12])])
ws.append([f"Ø16 · riostras ({len(b16)}) y zanja perimetral con su cierre ({b16_anillo_tot})", "barras de 12 m", tot[16], tot[16] * 12, round(kg[16])])
ws.append([f"Ø8 · cercos: {n_r} de riostra (34 × 44 cm) y {n_a} de zanja (34 × 34 cm), por dentro", "barras de 12 m para doblar, o cercos hechos", f"{tot[8]} barras ({n_r + n_a} cercos)", tot[8] * 12, round(kg[8])])
ws.append(["TOTAL", "", "", "", round(total_kg)])
for c in ws[ws.max_row]: c.font = NEG
ws.append([])
ws.append([f"De ellos, la zanja perimetral de 40 × 40 ({L_ANILLO:.1f} m + cierre del saliente {L_CIERRE:.1f} m, {m3_anillo:.1f} m³ de hormigón)", "", "", "", round(kg_anillo)])
ws.append(["Si la zanja llevara el armado del arquitecto (4Ø12 en total, cercos Ø8 cada 20 cm) pesaría", "", "", "", round(kg_anillo_arq)])
for r in (ws.max_row - 1, ws.max_row):
    for c in ws[r]: c.fill = NA
for col, a in zip("ABCDE", (86, 38, 26, 10, 10)): ws.column_dimensions[col].width = a
for row in ws.iter_rows(min_row=3, max_row=ws.max_row):
    for c in row:
        if c.column > 1 and c.value not in (None, ""): c.alignment = Alignment(horizontal="center")
w2 = wb.create_sheet("Cortes")
w2.append(["Ø", "Pieza (m)", "Nº de piezas", "Uso", "Doblado"])
for l, n in sorted(c12.items(), reverse=True):
    w2.append([12, l, n, "Zapatas Z-1 y Z-2" if l < 3 else "Zapatas Z-2, sentido largo", "patilla de 20 cm en cada extremo"])
w2.append([16, 9.80, 16, "Riostras este-oeste (y = 7,60 y y = 11,80)", "ganchos de 40 cm en los extremos, si el técnico los pide"])
w2.append([16, 5.20, 24, "Riostras norte-sur (x = 3,10; 5,55; 7,20)", "recta; sobresale 50 cm dentro de cada zapata"])
w2.append([16, 12.00, b16_anillo, f"Zanja perimetral: {n_tramos} barras por cada una de las 8 líneas, solape de {LAP * 100:.0f} cm", "se doblan en las esquinas; empalmes siempre en tramos rectos y alternados"])
w2.append([16, p_cierre, 8, f"Cierre del saliente ({L_CIERRE:.1f} m + 40 cm de entrega por extremo)", "recta"])
w2.append([8, round(corte_r, 2), n_r, "Cercos de riostra, cada 20 cm", "34 × 44 cm por dentro, ganchos a 135°"])
w2.append([8, round(corte_a, 2), n_a, "Cercos de la zanja perimetral, cada 15 cm", "34 × 34 cm por dentro, ganchos a 135°"])
for c in w2[1]: c.font = NEG; c.fill = AZ
for col, a in zip("ABCDE", (6, 12, 14, 62, 62)): w2.column_dimensions[col].width = a
w3 = wb.create_sheet("Plan de corte")
w3.append(["Ø", "Barras de 12 m", "Cómo se corta cada una", "Sobrante por barra (m)"])
for d, bs in ((12, b12), (16, b16)):
    for n, k, s in patrones(bs):
        w3.append([d, n, texto_patron(k), round(s, 2)])
w3.append([16, b16_anillo, "entera (12,00)", 0])
w3.append([16, b16_cierre, f"{math.floor(BARRA / p_cierre)} × {p_cierre:.2f}", round(BARRA - math.floor(BARRA / p_cierre) * p_cierre, 2)])
for c in w3[1]: c.font = NEG; c.fill = AZ
for col, a in zip("ABCD", (6, 16, 60, 22)): w3.column_dimensions[col].width = a
w4 = wb.create_sheet("Notas")
for t in ("Parrilla: Ø12 cada 15 cm en los dos sentidos, 5 cm de recubrimiento lateral y patillas de 20 cm (desarrollo = largo + 0,40 m).",
          "Riostras RI-1 de 40 × 50 cm: 4Ø16 arriba + 4Ø16 abajo, cercos Ø8 cada 20 cm; longitudes: 2 × 9,00 m (este-oeste) + 3 × 4,20 m (norte-sur).",
          f"Zanja perimetral de 40 × 40 cm en los muros exteriores de la casa: {L_ANILLO:.1f} m (el lado norte, y = 7,60, lo hace la riostra) más {L_CIERRE:.1f} m de cierre en la boca del saliente. 4Ø16 arriba + 4Ø16 abajo, cercos Ø8 cada 15 cm, recubrimiento de 3 cm.",
          "La zanja y las riostras forman recintos cerrados R1–R6 (ver cimentacion_anillos.png). En cada cruce, las barras de la riostra entran 40 cm en la zanja con gancho; hormigonar el cruce en una sola tanda.",
          "Una zanja de 40 cm de hondo es un atado, no una zapata: no sustituye la cimentación de los muros de 55 cm, que sigue pendiente de catas.",
          "El plan de corte aprovecha cada barra de 12 m; los sobrantes cubren las mermas. Si el técnico cambia el armado, hay que recalcular (`python pedido_cimentacion.py`).",
          "No son hierro de armar, pero se piden en el mismo viaje: 24 pernos de anclaje Ø20 de 40 cm con placa de 30 × 30 × 2 cm (6 pilares), cable de cobre desnudo de 35 mm² para el anillo de tierra (unos 70 m; irá dentro de la zanja perimetral) y alambre de atar (unos 25 kg), más separadores de 5 cm (zapatas) y de 3 cm (riostras y zanja)."):
    w4.append([t])
w4.column_dimensions["A"].width = 170
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
      Paragraph("Zapatas, riostras y zanja perimetral de 40 × 40 cm. Acero corrugado B 500 S. Armados de la propuesta (docs/10); los confirma el técnico.", B), Spacer(1, 3), Paragraph("Lo que hay que pedir", H2)]
el.append(tabla([["Qué", "Se pide en", "Cantidad", "Kilos"],
                 ["Ø12 · parrilla de las 4 zapatas (cada 15 cm en los dos sentidos)", "barras de 12 m", f"<b>{tot[12]}</b>", round(kg[12])],
                 [f"Ø16 · riostras ({len(b16)} barras) y zanja perimetral con su cierre ({b16_anillo_tot} barras)", "barras de 12 m", f"<b>{tot[16]}</b>", round(kg[16])],
                 [f"Ø8 · cercos cuadrados: {n_r} de riostra (34 × 44 cm por dentro) y {n_a} de zanja (34 × 34 cm)", "barras de 12 m para doblar, o cercos hechos", f"<b>{tot[8]}</b> barras ({n_r + n_a} cercos)", round(kg[8])],
                 ["<b>TOTAL</b>", "", "", f"<b>{round(total_kg)}</b>"]],
                [92 * mm, 40 * mm, 34 * mm, 16 * mm]))
el.append(Paragraph("Lista de cortes (para que el proveedor corte y doble)", H2))
filas = [["Ø", "Largo", "Piezas", "Dónde", "Doblado"]]
for l, n in sorted(c12.items(), reverse=True):
    filas.append(["12", f"{l:.2f} m", n, "Zapatas Z-2, sentido largo" if l > 3 else "Zapatas Z-1 y Z-2", "patilla de 20 cm en cada extremo"])
filas += [["16", "9,80 m", 16, "Riostras este-oeste (y = 7,60 y y = 11,80)", "recta o con gancho de 40 cm"],
          ["16", "5,20 m", 24, "Riostras norte-sur (x = 3,10; 5,55; 7,20)", "recta"],
          ["16", "12,00 m", b16_anillo, f"Zanja perimetral: {n_tramos} por cada una de las 8 líneas, solape de 80 cm", "doblar en esquinas; empalmes en tramo recto"],
          ["16", f"{p_cierre:.2f} m", 8, f"Cierre del saliente ({L_CIERRE:.1f} m + 40 cm por extremo)", "recta"],
          ["8", f"{corte_r:.2f} m", n_r, "Cercos de riostra, cada 20 cm", "34 × 44 cm por dentro, ganchos a 135°"],
          ["8", f"{corte_a:.2f} m", n_a, "Cercos de la zanja perimetral, cada 15 cm", "34 × 34 cm por dentro, ganchos a 135°"]]
el.append(tabla(filas, [9 * mm, 18 * mm, 15 * mm, 84 * mm, 56 * mm]))
el.append(Paragraph("Cómo salen de las barras de 12 m", H2))
filas = [["Ø", "Barras", "Cada barra da", "Sobra"]]
for d, bs in ((12, b12), (16, b16)):
    for n, k, s in patrones(bs):
        filas.append([d, n, texto_patron(k), f"{s:.2f} m"])
filas.append([16, b16_anillo, "entera, para la zanja perimetral", "—"])
filas.append([16, b16_cierre, f"{math.floor(BARRA / p_cierre)} × {p_cierre:.2f}", f"{BARRA - math.floor(BARRA / p_cierre) * p_cierre:.2f} m"])
filas.append([8, tot[8], f"{math.floor(BARRA / corte_r)} cercos de {corte_r:.2f} m (riostra) o {math.floor(BARRA / corte_a)} de {corte_a:.2f} m (zanja)", "≈ 0,03–1,4 m"])
el.append(tabla(filas, [9 * mm, 18 * mm, 120 * mm, 35 * mm]))
el.append(Spacer(1, 4))
for t in (f"<b>Zanja perimetral de 40 × 40:</b> {L_ANILLO:.1f} m en los muros exteriores de la casa (el lado norte, y = 7,60, lo hace la riostra) más {L_CIERRE:.1f} m de cierre en la boca del saliente, unos {m3_anillo:.1f} m³ de hormigón. Con el armado del arquitecto (4Ø12 en total) pesaría {round(kg_anillo_arq)} kg en vez de {round(kg_anillo)} kg.",
          "<b>Para pedir en el mismo viaje (no es hierro de armar):</b> 24 pernos de anclaje Ø20 de 40 cm con placa de 30 × 30 × 2 cm (6 pilares); cable de cobre desnudo de 35 mm² para el anillo de tierra (unos 70 m, dentro de la zanja); alambre de atar (unos 25 kg); separadores de 5 cm (zapatas) y de 3 cm (riostras y zanja).",
          "<b>Antes de hormigonar la línea y = 7,60</b> hay que resolver tres puntos (ver la comprobación): la cimentación existente que coincide con las zapatas, el colector Ø150 que cruza la riostra y la zapata Z-2, y la escalera, que no tiene cimentación prevista. El hierro de este pedido no cambia por ello; los cortes sí podrían cambiar en las zapatas de esa línea."):
    el.append(Paragraph(t, B)); el.append(Spacer(1, 2))
el += [PageBreak(), Paragraph("Cómo quedan los anillos", H1), Image("cimentacion_anillos.png", width=178 * mm, height=178 * mm * 1174 / 937)]
doc.build(el)
print("ok: pedido_1_hierro_cimentacion.xlsx y pdf/Pedido_1_hierro_cimentacion.pdf")
