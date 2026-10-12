"""Plantas, secciones y lámina A1 (1/75) de la envolvente v2. Reutiliza utilidades de dxf.py."""
import math
from ezdxf.enums import TextEntityAlignment as TA
import dxf as base
import casa_v2 as h

base.ESC = 75
S75 = 1 / 75
FECHA = "29/09/2026"
Z_PB_CUT, Z_PA_CUT = 0.95, h.Z_PA + 1.20
for n, v in {"murete_pasillo": ("RAYADO_OTROS", None, 0, 7)}.items(): base.RAYADO[n] = v
base.LAYERS["murete_pasillo"] = (7, 35, "Continuous")
LAY = {"DEF": (2, 13, "Continuous")}


def texto(cx, txt, x, y, hh, rot=0, layer="TEXTO"):
    e = cx.msp.add_text(txt, height=hh * cx.K, dxfattribs={"layer": layer, "rotation": rot})
    e.set_placement(cx.t(x, y), align=TA.MIDDLE_CENTER)


def planta(cx, planta, titulo):
    z = Z_PB_CUT if planta == "PB" else Z_PA_CUT
    for n, sol, _ in h.partes: base.pintar(cx, n, sol, "z", z)
    if planta == "PB":
        x0, x1 = h.CRISTALERA
        for x in (x0, x1): cx.line((x, 0), (x, h.T), "HUECOS")
        for f in (.30, .50, .70): cx.line((x0, f * h.T), (x1, f * h.T), "CARPINTERIA")
        p0, p1 = h.PUERTA
        for x in (p0, p1): cx.line((x, 0), (x, h.T), "HUECOS")
        cx.door((p1, h.T), (-1, 0), (0, 1), p1 - p0)
        texto(cx, "CRISTALERA DOBLE", (x0 + x1) / 2, -0.35, 1.8); texto(cx, "PUERTA", (p0 + p1) / 2, -0.35, 1.8)
        for x in (h.PASO_CEN[0], h.PASO_CEN[1]): cx.line((x, h.Y_CEN), (x, h.Y_CEN + h.T_CEN), "HUECOS")
        texto(cx, "SALÓN (supuesto)", 5.30, 3.9, 3.0); texto(cx, "salón: unos 30 m²", 5.30, 3.3, 2.0)
        texto(cx, "PASILLO DE ENTRADA", 8.55, 3.9, 2.2, 90)
        texto(cx, "murete bajo", h.MURETE_X + .05, 6.3, 1.8, 90)
    else:
        texto(cx, "sobre el salón: por definir", 5.30, 3.9, 2.4)
    texto(cx, "ZONA NORTE: POR DEFINIR", 4.80, 11.9, 3.0); texto(cx, "anexo este", h.XE + 1.25, 10.0, 2.0, 90)
    # cotas (croquis, exteriores)
    xf = h.XE - h.W_FRONT
    cx.chain_x([xf, h.CRISTALERA[0], h.CRISTALERA[1], h.PUERTA[0], h.PUERTA[1], h.XE], 0, -0.6)
    cx.dim((xf, 0), (h.XE, 0), ((xf + h.XE) / 2, -1.2), 0)
    ex = h.XE + h.SAL
    cx.chain_y([0, h.Y_E1, h.Y_E2, h.Y_TOP], ex, ex + 0.6)
    cx.dim((ex, 0), (ex, h.Y_TOP), (ex + 1.2, h.Y_TOP / 2), 90)
    cx.dim((h.XE, h.Y_E2), (ex, h.Y_E2), ((h.XE + ex) / 2, h.Y_E2 + 0.6), 0)
    cx.dim((0, h.Y_TOP), (h.XE, h.Y_TOP), (h.XE / 2, h.Y_TOP + 0.6), 0)
    cx.dim((0, h.Y_JUNC), (0, h.Y_TOP), (-0.6, (h.Y_JUNC + h.Y_TOP) / 2), 90)
    cx.dim((h.XE - h.W_SUR, h.Y_JUNC), (h.XE, h.Y_JUNC), (h.XE - h.W_SUR / 2, h.Y_JUNC - 0.6), 0)
    cx.line((-0.35, h.Y_CEN + .15), (ex + 0.35, h.Y_CEN + .15), "CORTES") if False else None
    if planta == "PB":                              # trazas de cortes
        xa, yb = 5.50, 4.00
        cx.line((xa, -0.35), (xa, h.Y_TOP + 0.35), "CORTES"); cx.line((h.XE - h.W_SUR - .3, yb), (h.XE + .35, yb), "CORTES")
        for tx, ty, t in [(xa, -0.6, "A"), (xa, h.Y_TOP + 0.6, "A'"), (h.XE - h.W_SUR - .55, yb, "B"), (h.XE + .6, yb, "B'")]:
            texto(cx, t, tx, ty, 3.0, layer="CORTES")
    cx.line((-1.2, h.Y_TOP + 1.0), (-1.2, h.Y_TOP + 2.0), "COTAS"); texto(cx, "N (supuesto)", -1.2, h.Y_TOP + 2.5, 2.0)
    texto(cx, titulo, h.XE / 2 + 1.2, -2.0, 4.0)


def seccion(cx, eje, valor, titulo):
    tf = (lambda p: (p[1], -p[0])) if eje == "x" else (lambda p: (p[0], -p[1]))
    for n, sol, _ in h.partes: base.pintar(cx, n, sol, eje, valor, tf)
    xs = [tf(p)[0] for b in base.contornos(h.cimentacion.val(), eje, valor) for bb in b for p in bb]
    a, b = min(xs), max(xs)
    zc = h.Z_TOP + h.T_FORJ
    zs = [-h.H_CIM, 0, h.H_PB, h.Z_PA, h.Z_TOP, zc, zc + h.ROOF_H]
    cx.chain_y(zs, a, a - 0.6)
    cx.dim((a, -h.H_CIM), (a, zc + h.ROOF_H), (a - 1.2, (zc + h.ROOF_H - h.H_CIM) / 2), 90)
    cx.dim((a, -h.H_CIM), (b, -h.H_CIM), ((a + b) / 2, -h.H_CIM - 0.7), 0)
    for zz, t in [(0, "±0.00 SUELO PB"), (h.Z_PA, f"+{h.Z_PA:.2f} SUELO PA"), (h.Z_TOP, f"+{h.Z_TOP:.2f} FORJ. CUBIERTA")]:
        cx.line((b + 0.3, zz), (b + 1.0, zz), "COTAS"); cx.text(t, b + 1.05, zz, 1.8, al=TA.MIDDLE_LEFT)
    cx.text(titulo, (a + b) / 2, -h.H_CIM - 1.9, 4.0)


def dibujos(cx, k):
    if k == "PB": planta(cx, "PB", "PLANTA BAJA  esc. 1/75")
    elif k == "PA": planta(cx, "PA", "PLANTA ALTA  esc. 1/75")
    elif k == "A": seccion(cx, "x", 5.50, "SECCIÓN A-A' (por salón y muro central)  esc. 1/75")
    else: seccion(cx, "y", 4.00, "SECCIÓN B-B' (por salón y murete)  esc. 1/75")


def cuadro(msp, x0, y0):
    sal = (7.75 - (3.55 + 3.27) / 2) * (h.Y_CEN - h.T)
    cor = (9.15 - 7.85) * (h.Y_CEN - h.T)
    filas = [("CONCEPTO", "PLANTA", "m²"), ("Superficie construida (exterior)", "cada una", f"{h.AREA_EXT:.2f}"),
             ("Superficie interior (sin muro central)", "cada una", f"{h.AREA_INT:.2f}"),
             ("Salón (aprox.)", "PB", f"{sal:.2f}"), ("Pasillo de entrada (aprox.)", "PB", f"{cor:.2f}"),
             ("Zona norte y anexo este", "PB/PA", "por definir")]
    w, hh = (105, 40, 35), 7
    msp.add_text("CUADRO DE SUPERFICIES (croquis, exteriores)", height=3.5, dxfattribs={"layer": "TEXTO", "insert": (x0, y0 + 4)})
    y = y0
    for f in filas:
        x = x0
        for wi, val in zip(w, f):
            msp.add_text(val, height=2.5, dxfattribs={"layer": "TEXTO", "insert": (x + 2, y - hh + 2)}); x += wi
        msp.add_lwpolyline([(x0, y), (x0 + sum(w), y), (x0 + sum(w), y - hh), (x0, y - hh)], close=True, dxfattribs={"layer": "TABLA"})
        y -= hh
    return y


def lamina(nombre):
    doc = base.nuevo_doc(); msp = doc.modelspace()
    msp.add_lwpolyline([(0, 0), (841, 0), (841, 594), (0, 594)], close=True, dxfattribs={"layer": "MARCO"})
    msp.add_lwpolyline([(8, 8), (833, 8), (833, 586), (8, 586)], close=True, dxfattribs={"layer": "MARCO"})
    cells = {"PB": (18, 298), "PA": (288, 298), "A": (558, 298), "B": (18, 12)}
    for k, (cx0, cy0) in cells.items():
        ox = cx0 + 40 if k in ("PB", "PA") else cx0 + 50
        oy = cy0 + (48 if k in ("PB", "PA") else (h.H_CIM + 2.4) * 13.33)
        if k == "B": ox = cx0 + 60 - (h.XE - h.W_SUR) * 13.33
        if k in ("PB", "PA"): ox = cx0 + 50 - 0 * 13.33
        dibujos(base.Ctx(doc, msp, ox, oy, S75), k)
    fin = cuadro(msp, 300, 280)
    for i, t in enumerate(["NOTAS: cotas en metros, exteriores según croquis a mano. Muros exteriores 0.40 m (supuesto).",
                           "Muro central (0.30 m) continuo de cimentación a cubierta, en la línea sur del bloque norte (supuesto).",
                           "Fondo del salón: 6.40 m en fachada y 6.68 m al fondo. Sin definir: habitaciones, escalera, huecos N/E, anexo este.",
                           "Discrepancias del croquis: ancho 9.55 (arriba) / 9.64 (abajo); lado oeste del bloque sur sin acotar (7.32 supuesto)."]):
        msp.add_text(t, height=2.2, dxfattribs={"layer": "TEXTO", "insert": (300, fin - 8 - i * 5)})
    x0, y0, x1, y1 = 640, 14, 825, 100
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "MARCO"})
    for yy in (32, 50, 68, 84): msp.add_line((x0, yy), (x1, yy), dxfattribs={"layer": "TABLA"})
    msp.add_line((x0 + 120, y0), (x0 + 120, 50), dxfattribs={"layer": "TABLA"})
    T = lambda t, x, y, s=2.6: msp.add_text(t, height=s, dxfattribs={"layer": "TEXTO", "insert": (x, y)})
    T("BORRADOR - SIN VISADO. Croquis de obra sobre base del proyecto exp. 25-01150-BE (COAA).", x0 + 3, y1 - 6, 2.0)
    T("VIVIENDA UNIFAMILIAR - Pol. 33, parc. 198, San Roque, Albox (Almería)", x0 + 3, 87, 2.4)
    T("ENVOLVENTE SOBRE CROQUIS - PLANTAS Y SECCIONES", x0 + 3, 71, 3.0)
    T("Plano: PLANTAS, SECCIONES Y COTAS", x0 + 3, 54, 2.6); T("Hoja: 01 / 01", x0 + 123, 54, 2.6)
    T("Escala: 1/75 (A1)", x0 + 3, 36, 2.6); T(f"Fecha: {FECHA}", x0 + 123, 36, 2.6)
    T("Unidades: mm (papel)", x0 + 3, 18, 2.2); T("Rev.: R01", x0 + 123, 18, 2.6)
    doc.saveas(nombre); print(nombre)


if __name__ == "__main__":
    for nom, k in [("planta_baja_v2", "PB"), ("planta_alta_v2", "PA"), ("seccion_transversal_v2", "A"), ("seccion_longitudinal_v2", "B")]:
        d = base.nuevo_doc(); dibujos(base.Ctx(d, d.modelspace(), 0, 0, 1), k); d.saveas(nom + ".dxf"); print(nom)
    lamina("lamina_A1_v2.dxf")
