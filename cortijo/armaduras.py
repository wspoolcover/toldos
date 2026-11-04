"""Lista de hierro para pedir: zunchos, riostras y mallazo del suelo (armados de docs/10_cimentacion_y_zunchos.md, propuesta a confirmar por el técnico).
Genera pedido_hierro_zunchos.xlsx y pdf/Pedido_hierro_zunchos.pdf. Longitudes tomadas de los polígonos del modelo (opciones.py)."""
import math, os, sys
from shapely.geometry import Polygon
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import opciones as o

KG = {6: 0.222, 8: 0.395, 12: 0.888, 14: 1.208, 16: 1.578}      # kg/m de barra corrugada B 500 S
BARRA = 12.0                                                    # longitud comercial
MARGEN_L = 1.10                                                 # +10 % en barras longitudinales: solapes (≈ 50 Ø), esquinas y mermas
MARGEN_C = 1.05                                                 # +5 % en cercos
GANCHO = 0.15                                                   # añadido al perímetro del cerco por los dos ganchos
RECUB = 0.03
T_CASA, T_SALON, EXTRA_MURO = 0.55, 0.25, 30.0                  # espesores de muro y metros extra pedidos para el muro exterior

SB, CASA = Polygon(o.SB_), Polygon(o.NB_FULL)
L_CASA = CASA.length - 4 * T_CASA - 5.55                        # eje de los muros de 55 cm, sin el tramo de la fachada interior (lo sustituye la viga HEB)
L_SALON = (7.32 + 7.33) + (SB.bounds[2] - 3.15 - 0.25)          # dos muros laterales + muro norte (ejes de 25 cm); sin restar el dintel de la cristalera
L_RIOSTRA = 2 * (9.55 - T_CASA) + 3 * (11.80 - 7.60)
A_SUELO = CASA.buffer(-T_CASA, join_style=2).area + SB.buffer(-T_SALON, join_style=2).area


def cerco(b, h, diam):
    """Corte de un cerco cuadrado/rectangular: interior (b − 2·recub) × (h − 2·recub) + ganchos."""
    ib, ih = b - 2 * RECUB, h - 2 * RECUB
    return ib, ih, 2 * (ib + ih) + GANCHO


# (nombre, nivel, longitud m, ancho m, canto m, nº barras, Ø long., Ø cerco, separación cercos, niveles que se repiten)
ZUNCHOS = [
    ("RI-1 riostras (entre zapatas y muros)", "suelo / cimentación", L_RIOSTRA, 0.40, 0.50, 8, 16, 8, 0.20, 1),
    ("ZH-1 zuncho de los muros de 55 cm: forjado de planta alta", "forjado", L_CASA, 0.55, 0.30, 8, 16, 8, 0.15, 1),
    ("ZH-2 zuncho de los muros del salón (terraza)", "forjado", L_SALON, 0.25, 0.30, 8, 16, 8, 0.15, 1),
    ("ZH-1 zuncho de los muros de 55 cm: cubierta", "cubierta", L_CASA, 0.55, 0.30, 8, 16, 8, 0.15, 1),
    (f"Muro exterior: {EXTRA_MURO:.0f} m más (25×30, como ZH-2)", "muro exterior", EXTRA_MURO, 0.25, 0.30, 8, 16, 8, 0.15, 1),
]
# armado ligero del primer dossier de obra (orientativo), solo para comparar el total
LIGERO = {"RI-1": (0.40, 0.40, 4, 12, 8, 0.25), "ZH-1": (0.55, 0.25, 6, 12, 6, 0.20), "ZH-2": (0.25, 0.25, 4, 12, 6, 0.20)}


def calcula(z):
    nombre, nivel, L, b, h, nb, dl, dc, s, rep = z
    bar_m = nb * L * rep
    bar_pedir = bar_m * MARGEN_L
    ib, ih, corte = cerco(b, h, dc)
    n_c = (math.ceil(L / s) + 1) * rep
    n_c_pedir = math.ceil(n_c * MARGEN_C)
    return dict(nombre=nombre, nivel=nivel, L=L, b=b, h=h, nb=nb, dl=dl, dc=dc, s=s, bar_m=bar_m, bar_pedir=bar_pedir,
                ib=ib, ih=ih, corte=corte, n_c=n_c, n_c_pedir=n_c_pedir, m_c=n_c_pedir * corte)


FILAS = [calcula(z) for z in ZUNCHOS]
tot = {}
for f in FILAS:
    t = tot.setdefault(f["dl"], 0.0); tot[f["dl"]] = t + f["bar_pedir"]
    t = tot.setdefault(f["dc"], 0.0); tot[f["dc"]] = t + f["m_c"]
print("Longitudes (m): riostras", round(L_RIOSTRA, 1), "casa", round(L_CASA, 1), "salón", round(L_SALON, 1), "| suelo neto", round(A_SUELO, 1), "m²")
for f in FILAS:
    print(f"{f['nombre'][:55]:55s} L={f['L']:6.1f}  barras net={f['bar_m']:7.1f} m  pedir={f['bar_pedir']:7.1f}  cercos={f['n_c_pedir']:4d} de {f['corte']:.2f} m = {f['m_c']:6.1f} m")
barras16 = math.ceil(tot[16] / BARRA); kg16 = tot[16] * KG[16]
m8 = tot[8]; kg8 = m8 * KG[8]
print("Ø16:", round(tot[16]), "m →", barras16, "barras de 12 m,", round(kg16), "kg | Ø8 cercos:", round(m8), "m,", round(kg8), "kg")

# mallazo del suelo
PANEL = 2.20 * 6.00
paneles = math.ceil(A_SUELO * 1.10 / PANEL)
print("mallazo 15×15 Ø6:", paneles, "paneles de 2,20×6,00 (", round(A_SUELO * 1.10, 1), "m² con +10 %)")

# otros hierros del mismo pedido (zapatas y pilares de atado)
def parrilla(a, b, paso=0.15, rec=0.05, pat=0.40):
    n_a = math.floor((b - 2 * rec) / paso) + 1; n_b = math.floor((a - 2 * rec) / paso) + 1
    return n_a * ((a - 2 * rec) + pat) + n_b * ((b - 2 * rec) + pat)
Z1 = parrilla(1.60, 1.60); Z2 = parrilla(3.25, 1.60)
m12 = (2 * Z1 + 2 * Z2) * 1.05
N_PA = 22
m14 = N_PA * 4 * (3.3 + 0.6) * 1.05
m6 = N_PA * (math.ceil(3.3 / 0.15) + 1) * (4 * (0.25 - 2 * RECUB) + GANCHO) * 1.05
print("zapatas Ø12/15:", round(m12), "m | pilares de atado Ø14:", round(m14), "m, cercos Ø6:", round(m6), "m")

# comparación con el armado ligero (solo zunchos y riostras, sin extra)
kg_ligero = 0.0
for clave, L, rep in (("RI-1", L_RIOSTRA, 1), ("ZH-1", L_CASA, 2), ("ZH-2", L_SALON, 1)):
    b, h, nb, dl, dc, s = LIGERO[clave]
    ib, ih, corte = cerco(b, h, dc)
    kg_ligero += nb * L * rep * MARGEN_L * KG[dl] + math.ceil(L / s + 1) * rep * MARGEN_C * corte * KG[dc]
kg_gen = sum(f["bar_pedir"] * KG[f["dl"]] + f["m_c"] * KG[f["dc"]] for f in FILAS if "Muro exterior" not in f["nombre"])
print("kg zunchos+riostras: generoso", round(kg_gen), "| ligero", round(kg_ligero))

if "--solo-calculo" in sys.argv:
    raise SystemExit

# ---------------- Excel ----------------
AZ = PatternFill("solid", fgColor="DCE6F1"); NA = PatternFill("solid", fgColor="FFF2CC"); NEG = Font(bold=True)
fino = Side(style="thin", color="BBBBBB"); BORDE = Border(left=fino, right=fino, top=fino, bottom=fino)
wb = Workbook()


def hoja(ws, filas, anchos, cab=1):
    for r in filas: ws.append(r)
    for c, a in enumerate(anchos, 1): ws.column_dimensions[get_column_letter(c)].width = a
    for c in ws[cab]: c.font = NEG; c.fill = AZ; c.alignment = Alignment(wrap_text=True, vertical="center")
    for row in ws.iter_rows(min_row=cab, max_row=ws.max_row):
        for c in row: c.border = BORDE


ws = wb.active; ws.title = "Pedido"
ws.append(["PEDIDO DE HIERRO · zunchos, riostras y suelo (acero B 500 S; propuesta de docs/10, a confirmar por el técnico)"]); ws["A1"].font = Font(bold=True, size=12)
ws.append([])
ws.append(["Qué", "Medida", "Cantidad a pedir", "Metros", "Kilos aprox."])
for c in ws[3]: c.font = NEG; c.fill = AZ
ws.append(["Barra corrugada Ø16 (zunchos y riostras, con +10 %)", "barras de 12 m", barras16, round(tot[16]), round(kg16)])
ws.append(["Cercos Ø8 (cortados y doblados; los cortes están en la hoja «Cercos»)", "cercos", sum(f["n_c_pedir"] for f in FILAS), round(m8), round(kg8)])
ws.append(["Mallazo electrosoldado 15×15 Ø6 (suelo de planta baja, 113,8 m² + 10 %)", "paneles de 2,20 × 6,00 m", paneles, "", round(paneles * PANEL * 2.96)])
ws.append([])
ws.append(["Aparte (mismo pedido, si se necesita)", "", "", "", ""])
for c in ws[ws.max_row]: c.font = NEG; c.fill = NA
ws.append(["Parrilla de zapatas: Ø12 cada 15 cm en los dos sentidos (2 Z-1 y 2 Z-2, +5 %)", "metros de Ø12", math.ceil(m12 / BARRA), round(m12), round(m12 * KG[12])])
ws.append([f"Pilares de atado (≈ {N_PA} uds): 4Ø14 de 3,9 m (con la espera)", "metros de Ø14", math.ceil(m14 / BARRA), round(m14), round(m14 * KG[14])])
ws.append([f"Cercos de los pilares de atado: Ø6 cada 15 cm", "metros de Ø6", "", round(m6), round(m6 * KG[6])])
ws.append([])
ws.append(["Las barras se piden en tramos de 12 m (la cantidad de la columna C son barras para Ø16 y Ø12/Ø14, y cercos para Ø8)."])
ws.append([f"Comparación: con el armado ligero del primer dossier (4Ø12 / 6Ø12, cercos Ø6–Ø8) los zunchos y riostras pesarían unos {round(kg_ligero)} kg, frente a {round(kg_gen)} kg del armado de docs/10 (sin los {EXTRA_MURO:.0f} m del muro exterior)."])
for col, a in zip("ABCDE", (78, 26, 18, 12, 14)): ws.column_dimensions[col].width = a
for row in ws.iter_rows(min_row=3, max_row=ws.max_row):
    for c in row:
        if c.column > 1 and c.value not in (None, ""): c.alignment = Alignment(horizontal="center")

w2 = wb.create_sheet("Zunchos")
w2.append(["Elemento", "Nivel", "Largo (m)", "Sección (m)", "Barras Ø16", "Metros de barra (neto)", "Metros a pedir (+10 %)", "Cercos Ø8 cada (m)", "Nº de cercos (+5 %)"])
for f in FILAS:
    w2.append([f["nombre"], f["nivel"], round(f["L"], 1), f"{f['b']:.2f} × {f['h']:.2f}", f["nb"], round(f["bar_m"], 1), round(f["bar_pedir"], 1), f["s"], f["n_c_pedir"]])
w2.append(["TOTAL", "", round(sum(f["L"] for f in FILAS), 1), "", "", round(sum(f["bar_m"] for f in FILAS), 1), round(sum(f["bar_pedir"] for f in FILAS), 1), "", sum(f["n_c_pedir"] for f in FILAS)])
hoja(w2, [], (62, 20, 11, 14, 11, 16, 16, 14, 14))
for c in w2[w2.max_row]: c.font = NEG
w2.append([]); w2.append(["El ZH-1 de la casa se hormigona dos veces (forjado de planta alta y cubierta). Si ahora solo haces el suelo, pide solo las filas «suelo» y «forjado». El zuncho de los muros del salón incluye el muro norte; si el dintel de la cristalera hace de zuncho, resta unos 4,4 m."])

w3 = wb.create_sheet("Cercos")
w3.append(["Zuncho", "Medida interior del cerco (cm)", "Largo de corte de cada cerco (m)", "Nº de cercos", "Metros de Ø8"])
vistos = set()
for f in FILAS:
    w3.append([f["nombre"], f"{f['ib'] * 100:.0f} × {f['ih'] * 100:.0f}", round(f["corte"], 2), f["n_c_pedir"], round(f["m_c"], 1)])
hoja(w3, [], (62, 26, 24, 14, 14))
w3.append([]); w3.append(["Medida interior = ancho y canto del zuncho menos 3 cm de recubrimiento por cada lado. Largo de corte = perímetro + 15 cm de ganchos. Se puede pedir ya cortado y doblado (ferralla elaborada)."])

w4 = wb.create_sheet("Muro exterior")
w4.append(["Calculadora: cambia los metros de zuncho del muro exterior (celda B2)"]); w4["A1"].font = NEG
w4.append(["Metros de zuncho", EXTRA_MURO]); w4["B2"].fill = NA
w4.append(["Barras Ø16 (8 por metro), metros a pedir (+10 %)", "=B2*8*1.1"])
w4.append(["Barras de 12 m", "=ROUNDUP(B3/12,0)"])
w4.append(["Kilos de Ø16", "=B3*1.578"])
w4.append(["Cercos Ø8 (cada 15 cm, +5 %)", "=ROUNDUP((ROUNDUP(B2/0.15,0)+1)*1.05,0)"])
w4.append(["Metros de Ø8 de cercos (1,01 m cada uno)", "=B6*1.01"])
w4.append(["Kilos de Ø8", "=B7*0.395"])
w4.append([]); w4.append(["Supone un zuncho de 25 × 30 con 4Ø16 arriba y 4Ø16 abajo, como el ZH-2. Si el muro exterior lleva otro armado, dime la sección y lo recalculo."])
w4.column_dimensions["A"].width = 56; w4.column_dimensions["B"].width = 16

w5 = wb.create_sheet("Hipótesis")
for t in (
    "Longitudes: ejes de los muros del modelo (casa 55 cm, salón 25 cm). ZH-1 sin el tramo de la fachada interior (5,55 m), que sustituye la viga HEB.",
    "Armados: los de docs/10_cimentacion_y_zunchos.md (4Ø16 arriba + 4Ø16 abajo; cercos Ø8 cada 15 cm en zunchos y cada 20 cm en riostras). Propuesta: la confirma el técnico.",
    "Barras en tramos de 12 m; +10 % por solapes (≈ 50 diámetros), esquinas y mermas; +5 % en cercos.",
    "Pesos: Ø6 0,222 kg/m; Ø8 0,395; Ø12 0,888; Ø14 1,208; Ø16 1,578. Mallazo 15×15 Ø6 ≈ 2,96 kg/m² (confirmar con la ficha del proveedor).",
    "El mallazo del suelo es una suposición (15×15 Ø6 sobre la solera); el proyecto no fija el armado de la solera. Si el técnico pide otro, se cambia.",
    "Si los zunchos son solo los del suelo y el forjado, quita la fila de cubierta y los 30 m del muro exterior.",
):
    w5.append([t])
w5.column_dimensions["A"].width = 150
wb.save("pedido_hierro_zunchos.xlsx")

# ---------------- PDF de una página ----------------
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
FUENTES = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("LS", FUENTES + "LiberationSans-Regular.ttf")); pdfmetrics.registerFont(TTFont("LS-B", FUENTES + "LiberationSans-Bold.ttf"))
pdfmetrics.registerFontFamily("LS", normal="LS", bold="LS-B", italic="LS", boldItalic="LS-B")
H1 = ParagraphStyle("h1", fontName="LS-B", fontSize=15, leading=18, spaceAfter=3)
H2 = ParagraphStyle("h2", fontName="LS-B", fontSize=10.5, leading=13, spaceBefore=7, spaceAfter=3)
B = ParagraphStyle("b", fontName="LS", fontSize=8.6, leading=11)
C = ParagraphStyle("c", fontName="LS", fontSize=8.4, leading=10.2)


def tabla(datos, anchos, cab=True):
    t = Table([[Paragraph(str(x), C) for x in fila] for fila in datos], colWidths=anchos, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#999999")), ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce6f1")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2)]))
    return t


os.makedirs("pdf", exist_ok=True)
doc = SimpleDocTemplate("pdf/Pedido_hierro_zunchos.pdf", pagesize=A4, leftMargin=14 * mm, rightMargin=14 * mm, topMargin=12 * mm, bottomMargin=10 * mm, title="Pedido de hierro: zunchos y suelo")
el = [Paragraph("Pedido de hierro · zunchos, riostras y suelo", H1),
      Paragraph("Acero corrugado B 500 S. Armados de la propuesta (docs/10); los confirma el técnico. Longitudes sacadas del modelo de la casa.", B), Spacer(1, 3), Paragraph("Lo que hay que pedir", H2)]
el.append(tabla([["Qué", "Se pide en", "Cantidad", "Metros", "Kilos"],
                 ["Barra corrugada Ø16 (zunchos y riostras)", "barras de 12 m", barras16, round(tot[16]), round(kg16)],
                 ["Cercos Ø8 (cuadrados, cortados y doblados)", "cercos", sum(f["n_c_pedir"] for f in FILAS), round(m8), round(kg8)],
                 ["Mallazo 15×15 Ø6 (suelo PB, 113,8 m² + 10 %)", "paneles 2,20 × 6,00", paneles, "—", round(paneles * PANEL * 2.96)]],
                [88 * mm, 32 * mm, 20 * mm, 20 * mm, 20 * mm]))
el.append(Paragraph("Por zuncho", H2))
filas = [["Elemento", "Largo", "Sección", "Ø16 a pedir", "Cercos Ø8"]]
for f in FILAS:
    filas.append([f["nombre"], f"{f['L']:.1f} m", f"{f['b'] * 100:.0f} × {f['h'] * 100:.0f} cm", f"{f['bar_pedir']:.0f} m", f"{f['n_c_pedir']} de {f['corte']:.2f} m"])
filas.append(["<b>TOTAL</b>", f"<b>{sum(f['L'] for f in FILAS):.1f} m</b>", "", f"<b>{sum(f['bar_pedir'] for f in FILAS):.0f} m</b>", f"<b>{sum(f['n_c_pedir'] for f in FILAS)}</b>"])
el.append(tabla(filas, [88 * mm, 18 * mm, 24 * mm, 24 * mm, 26 * mm]))
el.append(Paragraph("Medida de los cercos", H2))
filas = [["Zuncho", "Medida interior (cm)", "Largo de corte", "Armado"]]
for f, a in zip(FILAS, ("4Ø16 + 4Ø16, cercos cada 20 cm", "4Ø16 + 4Ø16, cercos cada 15 cm", "4Ø16 + 4Ø16, cercos cada 15 cm", "4Ø16 + 4Ø16, cercos cada 15 cm", "4Ø16 + 4Ø16, cercos cada 15 cm")):
    filas.append([f["nombre"], f"{f['ib'] * 100:.0f} × {f['ih'] * 100:.0f}", f"{f['corte']:.2f} m", a])
el.append(tabla(filas, [76 * mm, 30 * mm, 24 * mm, 52 * mm]))
el.append(Paragraph("Aparte, si se necesita en el mismo pedido", H2))
el.append(tabla([["Qué", "Metros", "Barras de 12 m", "Kilos"],
                 ["Parrilla de las 4 zapatas: Ø12 cada 15 cm en los dos sentidos", round(m12), math.ceil(m12 / BARRA), round(m12 * KG[12])],
                 [f"Pilares de atado (≈ {N_PA} uds): 4Ø14 de 3,9 m", round(m14), math.ceil(m14 / BARRA), round(m14 * KG[14])],
                 ["Cercos Ø6 de los pilares de atado (cada 15 cm)", round(m6), "—", round(m6 * KG[6])]], [100 * mm, 22 * mm, 30 * mm, 22 * mm]))
el.append(Spacer(1, 4))
for t in ("<b>Cómo está calculado:</b> barras con +10 % por solapes (unos 50 diámetros, 80 cm en Ø16), esquinas y mermas; cercos con +5 %; medida interior del cerco = ancho y canto menos 3 cm de recubrimiento por lado, y largo de corte = perímetro + 15 cm de ganchos.",
          f"<b>Los {EXTRA_MURO:.0f} m del muro exterior</b> están calculados como zuncho de 25 × 30 con 4Ø16 + 4Ø16 (como el del salón). Si lleva otro armado, hay que recalcularlo.",
          "<b>El zuncho de los muros de 55 cm</b> se hormigona en dos niveles (forjado de planta alta y cubierta). Si ahora haces solo el suelo, pide las filas de suelo y forjado.",
          f"<b>Más ligero:</b> con el armado del primer dossier (4Ø12 / 6Ø12) zunchos y riostras pesarían unos {round(kg_ligero)} kg, frente a {round(kg_gen)} kg de este armado."):
    el.append(Paragraph(t, B)); el.append(Spacer(1, 2))
doc.build(el)
print("ok: pedido_hierro_zunchos.xlsx y pdf/Pedido_hierro_zunchos.pdf")
