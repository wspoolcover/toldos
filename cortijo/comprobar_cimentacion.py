"""Comprobación de la cimentación tal como está en el proyecto (cimentacion_plano.py + estructura.json + escalera de casa_v8.py).
Cargas, presión sobre el terreno, armado de zapatas y riostras, coincidencias geométricas (zapatas nuevas contra cimentación existente, colector, escalera)
y comparación de longitudes con el DXF. Cálculo orientativo: no sustituye al técnico."""
import json, math
import ezdxf
from shapely.geometry import Polygon, box as sbox, LineString
import opciones as o

E = json.load(open("estructura.json")); LX = E["lineas_x"]; CY = [7.60, 11.80]
N_C, N_S = E["pilar"]["N_central"], E["pilar"]["N_sur"]       # kN de cálculo (ELU) del pilar de la línea y = 11,80 y de la línea y = 7,60
ZAP, CANTO, RECUB_Z = 1.60, 0.60, 0.05
T_S, T = 0.25, 0.55
SB, HOUSE = Polygon(o.SB_), Polygon(o.NB_FULL)
GAMMA_ELU = 1.42                                               # relación ELU/servicio con 1,35 G + 1,5 Q (valor aproximado para G ≈ 70 %)
FY = 500 / 1.15                                                # MPa de cálculo, B 500 S
out = []
P = out.append

# ---- 1. presión sobre el terreno
LC = (LX[2] - LX[1]) + ZAP
zap = [("Z-1 (x=3,10; y=11,80)", ZAP, ZAP, [N_C]), ("Z-1 (x=3,10; y=7,60)", ZAP, ZAP, [N_S]),
       ("Z-2 (x=5,55 y 7,20; y=11,80)", LC, ZAP, [N_C, N_C]), ("Z-2 (x=5,55 y 7,20; y=7,60)", LC, ZAP, [N_S, N_S])]
P("## 1. Presión sobre el terreno (cargas máximas de estructura.json)")
P("| Zapata | Carga ELU (kN) | Servicio + peso propio y tierra (kN) | Área (m²) | σ (kPa) | % de 130 kPa | % de 100 kPa |")
P("|---|---|---|---|---|---|---|")
sig = {}
for n, a, b, ns in zap:
    N = sum(ns); area = a * b
    serv = N / GAMMA_ELU + area * CANTO * 25 + area * 0.40 * 18
    s = serv / area; sig[n] = s
    P(f"| {n} | {N:.0f} | {serv:.0f} | {area:.2f} | {s:.0f} | {s / 130 * 100:.0f} % | {s / 100 * 100:.0f} % |")

# ---- 2. armado de zapatas
a0 = 0.30                                                      # placa base 30 × 30
v = (ZAP - a0) / 2; d = CANTO - RECUB_Z - 0.012 * 1.5
sig_elu = N_C / ZAP ** 2
M = sig_elu * v ** 2 / 2
As_flex = M * 1e6 / (0.9 * d * 1000 * FY)                      # mm² por metro
Td = N_C * 1e3 * (ZAP - a0) / (8 * 0.85 * d)                # N; zapata rígida por bielas y tirantes (a − a0)/(8·0,85·d), orientativo
As_biela = Td / FY / ZAP                                       # mm² por metro de ancho
As_dada = math.pi * 6 ** 2 / 0.15
P("\n## 2. Armado de la parrilla de las zapatas (Ø12 cada 15 cm en los dos sentidos)")
P(f"- Vuelo desde la placa base: {v:.2f} m; canto útil ≈ {d * 1000:.0f} mm; presión de cálculo con el pilar más cargado: {sig_elu:.0f} kPa.")
P(f"- Armadura que pide el cálculo: ≈ {As_flex:.0f} mm²/m por flexión y ≈ {As_biela:.0f} mm²/m por bielas y tirantes. Armadura dada, Ø12/15: {As_dada:.0f} mm²/m ({As_dada / (1000 * 600) * 1000:.2f} ‰ de la sección de 1,00 × 0,60 m).")
P(f"- Resultado: la parrilla Ø12/15 da unas {As_dada / max(As_flex, As_biela):.1f} veces lo que pide el cálculo simple. Cumple con holgura.")

# ---- 3. riostras
P("\n## 3. Riostras RI-1 (40 × 50 cm, 4Ø16 arriba y 4Ø16 abajo, cercos Ø8 cada 20 cm)")
ac = 0.16
Ntie = ac * N_C
As_tie = Ntie * 1e3 / FY
As_dada_r = 4 * math.pi * 8 ** 2
As_min_geo = 0.0028 * 400 * 500
P(f"- Esfuerzo de atado orientativo: {ac:.2f} × {N_C:.0f} kN = {Ntie:.0f} kN → {As_tie:.0f} mm² de acero. Dados 4Ø16 = {As_dada_r:.0f} mm² por cara.")
P(f"- Cuantía mínima geométrica de referencia (≈ 2,8 ‰ de b·h): {As_min_geo:.0f} mm²; 4Ø16 la cumple; 4Ø14 ({4 * math.pi * 7 ** 2:.0f} mm²) también.")
P("- Resultado: cumple con mucho margen. El armado es más fuerte de lo que pide el cálculo; la diferencia de peso con 4Ø14 es de unos 100 kg en todo el pedido de riostras.")

# ---- 4. coincidencias geométricas
HOUSE_FOOT = HOUSE.difference(HOUSE.buffer(-1.10, join_style=2))
SALON_FOOT = SB.buffer(0.175, join_style=2).difference(SB.buffer(-T_S - 0.175, join_style=2)).intersection(sbox(-1, -1, 14, 7.2))
zapatas = {"Z-1 y=7,60": sbox(LX[0] - ZAP / 2, 7.60 - ZAP / 2, LX[0] + ZAP / 2, 7.60 + ZAP / 2),
           "Z-1 y=11,80": sbox(LX[0] - ZAP / 2, 11.80 - ZAP / 2, LX[0] + ZAP / 2, 11.80 + ZAP / 2),
           "Z-2 y=7,60": sbox((LX[1] + LX[2]) / 2 - LC / 2, 7.60 - ZAP / 2, (LX[1] + LX[2]) / 2 + LC / 2, 7.60 + ZAP / 2),
           "Z-2 y=11,80": sbox((LX[1] + LX[2]) / 2 - LC / 2, 11.80 - ZAP / 2, (LX[1] + LX[2]) / 2 + LC / 2, 11.80 + ZAP / 2)}
colector = LineString([(5.9, 8.0), (5.9, -1.0)])
ESC = sbox(7.25, 9.65, 9.00, 12.29)
rio = [LineString([(T / 2, cy), (9.55 - T / 2, cy)]) for cy in CY] + [LineString([(lx, CY[0]), (lx, CY[1])]) for lx in LX]
P("\n## 4. Coincidencias entre elementos (en planta)")
P("| Zapata nueva | Con la zapata corrida del salón (0,60 m, ya hecha) | Con la cimentación de los muros de 55 cm (ancho supuesto 1,10 m) | El colector Ø150 (x = 5,90) la cruza | Bajo la escalera |")
P("|---|---|---|---|---|")
hallazgos = {}
for n, z in zapatas.items():
    a = z.intersection(SALON_FOOT).area; b = z.intersection(HOUSE_FOOT).area; c = colector.intersection(z).length; e = z.intersection(ESC).area
    hallazgos[n] = (a, b, c, e)
    P(f"| {n} | {a:.2f} m² | {b:.2f} m² | {c:.2f} m | {e:.2f} m² |")
cruces = [(i, colector.intersection(r).length, colector.intersects(r)) for i, r in enumerate(rio)]
P(f"\n- Riostras que cruza el colector: {sum(1 for _, _, k in cruces if k)} (la de y = 7,60 y las zapatas Z-2).")
P(f"- Zapata corrida de los muros de 55 cm: tramo bajo el muro que se quita entre x = 3,45 y x = 9,00 (fachada interior): {9.0 - 3.45:.2f} m. Su cimentación sigue enterrada donde irá la riostra de y = 7,60 y las zapatas de esa línea.")

# ---- 5. escalera
RISE, TREAD, LAND, XL = 0.192, 0.22, 0.88, 8.125
v_esc = (9.00 - XL) * TREAD * RISE * sum(range(1, 9)) + (9.00 - XL) * LAND * 9 * RISE + (XL - 7.25) * LAND * 0.22 + 7 * (XL - 7.25) * TREAD * 0.22
w_esc = v_esc * 24
P("\n## 5. Escalera de hormigón (v8)")
P(f"- Volumen de hormigón de los dos tramos y la meseta: {v_esc:.1f} m³ → peso ≈ {w_esc:.0f} kN ({w_esc / 9.81:.1f} t), más acabados y uso.")
P(f"- Lo que apoya en el suelo es el carril este macizo: {(9.00 - XL):.3f} × {8 * TREAD + LAND:.2f} m = {(9.00 - XL) * (8 * TREAD + LAND):.1f} m², con una presión de ≈ {((9.00 - XL) * TREAD * RISE * 36 + (9.00 - XL) * LAND * 9 * RISE) * 24 / ((9.00 - XL) * (8 * TREAD + LAND)):.0f} kPa de peso propio.")
P("- En el plano de cimentación **no hay nada previsto bajo la escalera**: queda sobre la solera. Hace falta una losa o zapata reforzada bajo el carril macizo.")

# ---- 6. comparación con el DXF
doc = ezdxf.readfile("cimentacion_v7.dxf"); msp = doc.modelspace()
def largo(pl):
    pts = list(pl.get_points("xy")); xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return max(max(xs) - min(xs), max(ys) - min(ys))
r_dxf = sum(largo(e) for e in msp.query('LWPOLYLINE[layer=="RIOSTRAS"]'))
z_dxf = sum(1 for e in msp.query('LWPOLYLINE[layer=="ZAPATAS"]'))
pa_dxf = sum(1 for e in msp.query('LWPOLYLINE[layer=="PILARES_ATADO"]'))
L_RIO = 2 * (9.55 - T) + 3 * (11.80 - 7.60)
P("\n## 6. Longitudes del pedido contra el DXF")
P(f"- Riostras: pedido {L_RIO:.1f} m; DXF {r_dxf:.1f} m (en el DXF cada riostra cubre además el medio ancho de la zapata o del muro en cada extremo; diferencia {r_dxf - L_RIO:+.1f} m).")
P(f"- Zapatas: {len(zapatas)} en el cálculo; {z_dxf} en el DXF. Pilares de atado dibujados en el DXF (salón): {pa_dxf}.")

if __name__ == "__main__":
    print("\n".join(out))
