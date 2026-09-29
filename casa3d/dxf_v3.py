"""Plantas de distribución y estructura, secciones y láminas A1 (1/75) de la vivienda v3."""
import math
from ezdxf.enums import TextEntityAlignment as TA
import dxf as base
import casa_v3 as h
from perfiles import SECC

base.ESC = 75
S75, FECHA = 1 / 75, "29/09/2026"
for n in ("VIGUETAS", "VIGAS", "PILARES", "ZAPATAS", "LUCERNARIO"):
    base.LAYERS[n] = {"VIGUETAS": (5, 25, "Continuous"), "VIGAS": (1, 60, "Continuous"), "PILARES": (1, 50, "Continuous"),
                      "ZAPATAS": (8, 18, "DASHED"), "LUCERNARIO": (4, 18, "DASHED")}[n]
for n, v in {"parapeto_terraza": ("RAYADO_MURO", "ANSI31", 45, None), "parapeto_cubierta": ("RAYADO_MURO", "ANSI31", 45, None),
             "tabiques_PB": ("RAYADO_OTROS", None, 0, 7), "tabiques_PA": ("RAYADO_OTROS", None, 0, 7), "murete_pasillo": ("RAYADO_OTROS", None, 0, 7)}.items():
    base.RAYADO[n] = v
    base.LAYERS[n] = (7, 35, "Continuous")
for k in h.STEEL:
    base.RAYADO["acero_" + k] = ("RAYADO_FORJADO", None, 0, 5); base.LAYERS["acero_" + k] = (5, 35, "Continuous")
for n in ("escalera", "lucernario"): base.LAYERS.setdefault(n, (30, 18, "Continuous"))
PLAN_SKIP = ("cimentacion", "forjado_PB_PA", "forjado_cubierta", "lucernario", "parapeto_cubierta", "cristal_PB", "cristal_PA", "mobiliario")
Z_CUT = {"PB": 0.95, "PA": h.Z_PA + 1.20}


def tx(cx, txt, x, y, hh, rot=0, layer="TEXTO", al=TA.MIDDLE_CENTER):
    e = cx.msp.add_text(txt, height=hh * cx.K, dxfattribs={"layer": layer, "rotation": rot}); e.set_placement(cx.t(x, y), align=al)


def hueco(cx, o):
    pl, ori, pos, t, ini, w, tipo, sw, tag, sill, hh = o
    if ori == "H":
        ends = [((ini, pos), (ini, pos + t)), ((ini + w, pos), (ini + w, pos + t))]; al, nm = (1, 0), (0, 1)
    else:
        ends = [((pos, ini), (pos + t, ini)), ((pos, ini + w), (pos + t, ini + w))]; al, nm = (0, 1), (1, 0)
    for p, q in ends: cx.line(p, q, "HUECOS")
    def pt(u, v):                                      # u a lo largo del muro desde 'ini', v a través (0..t)
        return (ini + u * al[0] + v * nm[0] + (pos if ori == "V" else 0) * (1 if ori == "V" else 0) * 0, (pos if ori == "H" else ini) + u * al[1] * (1 if ori == "V" else 0) + v * nm[1]) if False else \
               ((ini + u, pos + v) if ori == "H" else (pos + v, ini + u))
    if tipo == "V":
        for f in (0.35, 0.65): cx.line(pt(0, f * t), pt(w, f * t), "CARPINTERIA")
    elif tipo != "L":
        s = sw or 1; face = t if s > 0 else 0
        nv = (nm[0] * s, nm[1] * s)
        if tipo == "P":
            hg = pt(0, face); cx.door(hg, al, nv, w)
        else:
            hw = w / 2
            cx.door(pt(0, face), al, nv, hw); cx.door(pt(w, face), (-al[0], -al[1]), nv, hw)
        cx.text(tag, *[(a + b * w * 0.5 * s) for a, b in zip(pt(w / 2, t / 2), nm)], 1.6)


def salas(cx, planta):
    for pl, nombre, rects in h.ROOMS:
        if pl != planta: continue
        big = max(rects, key=lambda r: (r[2] - r[0]) * (r[3] - r[1]))
        x, y = (big[0] + big[2]) / 2, (big[1] + big[3]) / 2
        small = (big[2] - big[0]) < 2.0 or (big[3] - big[1]) < 2.0
        tx(cx, nombre, x, y + 0.2, 1.5 if small else 2.0)
        tx(cx, f"{h.area(rects):.1f} m²", x, y - 0.25, 1.3 if small else 1.7)


def cotas_perimetro(cx):
    xf = h.XE - h.W_FRONT; ex = h.XE + h.SAL
    cx.dim((xf, 0), (h.XE, 0), ((xf + h.XE) / 2, -0.7), 0)
    cx.chain_y([0, h.Y_E1, h.Y_E2, h.Y_TOP], ex, ex + 0.6); cx.dim((ex, 0), (ex, h.Y_TOP), (ex + 1.2, h.Y_TOP / 2), 90)
    cx.dim((0, h.Y_TOP), (h.XE, h.Y_TOP), (h.XE / 2, h.Y_TOP + 0.6), 0)
    cx.dim((0, h.Y_JUNC), (0, h.Y_TOP), (-0.6, (h.Y_JUNC + h.Y_TOP) / 2), 90)


def flecha_norte(cx):
    cx.line((-1.3, h.Y_TOP - 1.5), (-1.3, h.Y_TOP - 3.0), "COTAS"); cx.line((-1.3, h.Y_TOP - 3.0), (-1.45, h.Y_TOP - 2.6), "COTAS")
    cx.line((-1.3, h.Y_TOP - 3.0), (-1.15, h.Y_TOP - 2.6), "COTAS"); tx(cx, "N (supuesto)", -1.3, h.Y_TOP - 3.5, 1.8)


def planta_dist(cx, planta, titulo):
    for n, sol, _ in h.partes:
        if n.startswith("acero_") and n != "acero_pilares": continue
        if n in PLAN_SKIP: continue
        if planta == "PA" and n in ("muros_PB", "tabiques_PB", "murete_pasillo", "escalera"): continue
        if planta == "PB" and n in ("muros_PA", "tabiques_PA"): continue
        base.pintar(cx, n, sol, "z", Z_CUT[planta])
    for o in h.OPEN:
        if o[0] == planta: hueco(cx, o)
    x0, y0, x1, y1 = h.VOID
    if planta == "PB":
        for i in range(9): cx.line((8.15, 8.95 + i * h.TREAD), (9.00, 8.95 + i * h.TREAD), "escalera")
        for j in range(9): cx.line((7.25, 10.83 - j * h.TREAD), (8.10, 10.83 - j * h.TREAD), "escalera")
        tx(cx, "SUBE", 8.58, 9.9, 1.2, 90)
    else:
        cx.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "ESCALERA_ALTA", True)
    cx.poly([(h.XE - h.W_SUR - 0.27, 7.60), (h.XI1 + h.T / 2, 7.60)], "VIGAS"); tx(cx, "viga de acero (antes muro)", 6.0, 7.30, 1.4)
    salas(cx, planta); cotas_perimetro(cx); flecha_norte(cx)
    if planta == "PB":
        cx.line((6.25, -0.35), (6.25, h.Y_TOP + 0.35), "CORTES"); cx.line((-0.35, 10.05), (h.XE + h.SAL + 0.35, 10.05), "CORTES")
        for tx_, ty, t in [(6.25, -0.6, "A"), (6.25, h.Y_TOP + 0.6, "A'"), (-0.6, 10.05, "B"), (h.XE + h.SAL + 0.6, 10.05, "B'")]: tx(cx, t, tx_, ty, 3.0, layer="CORTES")
    tx(cx, titulo, h.XE / 2 + 1.2, -1.8, 4.0)


def planta_estructura(cx, nivel, titulo):
    z = 1.0
    base.pintar(cx, "muros_PB", h.muros_pb, "z", z)
    if nivel == "L1":
        cats = ["viguetas_salon", "viguetas_casa", "vigas_forjado", "dinteles", "dintel"]; e = "IPE"
    else:
        cats = ["viguetas_cubierta", "vigas_cubierta"]; e = "IPE"
    for c in cats:
        for g in h.STEEL[c]:
            x0, y0, x1, y1, sec = g if len(g) == 5 else (g[0], g[1], g[0], g[1], g[2])
            heavy = c in ("vigas_forjado", "vigas_cubierta", "dintel")
            wd = SECC[sec][1] / 1000
            cx.poly([(x0, y0), (x1, y1)], "VIGAS" if heavy else "VIGUETAS")
    for (lx, cy, sec) in h.STEEL["pilares"]:
        a = SECC[sec][0] / 2000
        cx.poly([(lx - a, cy - a), (lx + a, cy - a), (lx + a, cy + a), (lx - a, cy + a)], "PILARES", True)
        z_ = h.ZAP / 2; cx.poly([(lx - z_, cy - z_), (lx + z_, cy - z_), (lx + z_, cy + z_), (lx - z_, cy + z_)], "ZAPATAS", True)
    x0, y0, x1, y1 = h.VOID
    cx.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "LUCERNARIO" if nivel != "L1" else "ESCALERA_ALTA", True)
    tx(cx, "hueco de escalera" + (" + lucernario" if nivel != "L1" else ""), (x0 + x1) / 2, (y0 + y1) / 2, 1.5)
    if nivel == "L1":
        sv, sc = h.E["salon_vigueta"], h.E["casa_vigueta"]
        tx(cx, f"{sv['perfil']} @ {sv['sep']:.2f}  (luz 5,75)", 6.0, 3.5, 2.2); tx(cx, "TERRAZA SOBRE EL SALÓN", 6.0, 4.1, 2.6)
        tx(cx, f"{sc['perfil']} @ {sc['sep']:.2f}", 1.9, 9.4, 1.8, 90); tx(cx, f"dintel {h.E['dintel']['perfil']}", 5.5, 0.95, 1.8)
    else:
        sq = h.E["cubierta_vigueta"]; tx(cx, f"{sq['perfil']} @ {sq['sep']:.2f}", 1.9, 9.4, 1.8, 90)
        tx(cx, "CUBIERTA PLANA: piedra + paneles solares", 4.8, 8.4, 1.8)
    for lx in h.LINES_X:
        tx(cx, f"{h.E['viga_ns']['perfil']}", lx, h.Y_TOP + 0.35, 1.5, 90)
    xs = [h.T / 2] + h.LINES_X + [h.XE - h.T / 2]
    cx.chain_x(xs, h.Y_TOP, h.Y_TOP + 1.3)
    cx.chain_y([h.COL_Y[0], h.COL_Y[1], h.Y_TOP - h.T / 2], -0.0, -0.9)
    cotas_perimetro(cx); flecha_norte(cx); tx(cx, titulo, h.XE / 2 + 1.2, -1.8, 4.0)


def seccion(cx, eje, valor, titulo):
    tf = (lambda p: (p[1], -p[0])) if eje == "x" else (lambda p: (p[0], -p[1]))
    for n, sol, _ in h.partes:
        if n in ("mobiliario", "cristal_PB", "cristal_PA"): continue
        base.pintar(cx, n, sol, eje, valor, tf)
    xs = [tf(p)[0] for b in base.contornos(h.cimentacion.val(), eje, valor) for bb in b for p in bb]
    a, b = min(xs), max(xs)
    zs = [-h.H_CIM, 0, h.Z_PA, h.Z_TOP, h.Z_TOP + 0.5]
    cx.chain_y(zs, a, a - 0.6); cx.dim((a, -h.H_CIM), (a, h.Z_TOP + 0.5), (a - 1.2, (h.Z_TOP + 0.5 - h.H_CIM) / 2), 90)
    cx.dim((a, -h.H_CIM), (b, -h.H_CIM), ((a + b) / 2, -h.H_CIM - 0.7), 0)
    for zz, t in [(0, "±0.00 SUELO PB"), (h.Z_PA, f"+{h.Z_PA:.2f} SUELO PA / TERRAZA"), (h.Z_TOP, f"+{h.Z_TOP:.2f} CUBIERTA")]:
        cx.line((b + 0.3, zz), (b + 1.0, zz), "COTAS"); cx.text(t, b + 1.05, zz, 1.7, al=TA.MIDDLE_LEFT)
    cx.text(titulo, (a + b) / 2, -h.H_CIM - 1.9, 4.0)


def cuadro_salas(msp, x0, y0):
    filas = [("ESTANCIA", "PLANTA", "m²")]; tot = {"PB": 0, "PA": 0}
    for pl, nombre, rects in h.ROOMS:
        if nombre in ("Hueco escalera",): continue
        a = h.area(rects)
        if nombre not in ("Salón", "Pasillo entrada", "Terraza sobre salón"): tot[pl] += a
        filas.append((nombre, pl, f"{a:.1f}"))
    filas += [("Total casa planta baja", "PB", f"{tot['PB']:.1f}"), ("Total casa planta alta", "PA", f"{tot['PA']:.1f}")]
    return tabla(msp, x0, y0, "CUADRO DE SUPERFICIES (interiores, aprox.)", filas, (78, 24, 26), 5.4)


def tabla(msp, x0, y0, titulo, filas, w, hh):
    msp.add_text(titulo, height=3.2, dxfattribs={"layer": "TEXTO", "insert": (x0, y0 + 4)})
    y = y0
    for f in filas:
        x = x0
        for wi, val in zip(w, f):
            msp.add_text(val, height=2.2, dxfattribs={"layer": "TEXTO", "insert": (x + 1.5, y - hh + 1.5)}); x += wi
        msp.add_lwpolyline([(x0, y), (x0 + sum(w), y), (x0 + sum(w), y - hh), (x0, y - hh)], close=True, dxfattribs={"layer": "TABLA"}); y -= hh
    return y


def marco(msp, titulo, sub, hoja):
    msp.add_lwpolyline([(0, 0), (841, 0), (841, 594), (0, 594)], close=True, dxfattribs={"layer": "MARCO"})
    msp.add_lwpolyline([(8, 8), (833, 8), (833, 586), (8, 586)], close=True, dxfattribs={"layer": "MARCO"})
    x0, y0, x1, y1 = 640, 14, 825, 100
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "MARCO"})
    for yy in (32, 50, 68, 84): msp.add_line((x0, yy), (x1, yy), dxfattribs={"layer": "TABLA"})
    msp.add_line((x0 + 120, y0), (x0 + 120, 50), dxfattribs={"layer": "TABLA"})
    T = lambda t, x, y, s=2.6: msp.add_text(t, height=s, dxfattribs={"layer": "TEXTO", "insert": (x, y)})
    T("BORRADOR - SIN VISADO. Propuesta de diseño y predimensionado; no sustituye proyecto visado.", x0 + 3, y1 - 6, 1.9)
    T("VIVIENDA UNIFAMILIAR - Pol. 33, parc. 198, San Roque, Albox (Almería)", x0 + 3, 87, 2.4)
    T(titulo, x0 + 3, 71, 3.0); T(sub, x0 + 3, 54, 2.6); T(f"Hoja: {hoja}", x0 + 123, 54, 2.6)
    T("Escala: 1/75 (A1)", x0 + 3, 36, 2.6); T(f"Fecha: {FECHA}", x0 + 123, 36, 2.6)
    T("Unidades: mm (papel); cotas en m", x0 + 3, 18, 2.2); T("Rev.: R02", x0 + 123, 18, 2.6)


def notas(msp, x, y, lineas):
    for i, t in enumerate(lineas): msp.add_text(t, height=2.1, dxfattribs={"layer": "TEXTO", "insert": (x, y - i * 4.8)})


def lamina_dist(nombre):
    doc = base.nuevo_doc(); msp = doc.modelspace(); marco(msp, "DISTRIBUCIÓN PROPUESTA - PLANTAS Y SECCIONES", "Plano: DISTRIBUCIÓN, SECCIONES", "01 / 02")
    cells = {"PB": (18, 298), "PA": (288, 298), "A": (558, 298), "B": (18, 12)}
    for k, (cx0, cy0) in cells.items():
        ox = cx0 + (48 if k in ("PB", "PA") else 20); oy = cy0 + (44 if k in ("PB", "PA") else (h.H_CIM + 2.4) * 13.33)
        cx = base.Ctx(doc, msp, ox, oy, S75)
        if k == "PB": planta_dist(cx, "PB", "PLANTA BAJA  esc. 1/75")
        elif k == "PA": planta_dist(cx, "PA", "PLANTA ALTA  esc. 1/75")
        elif k == "A": seccion(cx, "x", 6.25, "SECCIÓN A-A' (salón, escalera, cocina)  1/75")
        else: seccion(cx, "y", 10.05, "SECCIÓN B-B' (dormitorio, escalera, baño)  1/75")
    fin = cuadro_salas(msp, 300, 282)
    notas(msp, 300, fin - 8, ["NOTAS: muros existentes de 0,55 m; medidas exteriores del croquis. Tabiques de 0,10 m.",
        "Falta confirmar a qué lado del croquis queda el este (otro terreno con la salida del sol).",
        "Norte abajo (calle y salón), sur arriba. Escalera en U con hueco y lucernario en cubierta.",
        "Se demuele el muro de fachada entre salón y casa y la pared central: los sustituyen vigas de acero (línea gruesa)."])
    doc.saveas(nombre); print(nombre)


def lamina_estr(nombre):
    doc = base.nuevo_doc(); msp = doc.modelspace(); marco(msp, "ESTRUCTURA DE ACERO - PREDIMENSIONADO", "Plano: ESTRUCTURA (planta forjado, cubierta)", "02 / 02")
    cells = {"L1": (18, 298), "R": (288, 298), "A": (558, 298)}
    for k, (cx0, cy0) in cells.items():
        ox = cx0 + (48 if k != "A" else 20); oy = cy0 + (44 if k != "A" else (h.H_CIM + 2.4) * 13.33)
        cx = base.Ctx(doc, msp, ox, oy, S75)
        if k == "L1": planta_estructura(cx, "L1", "ESTRUCTURA FORJADO PB-PA Y TERRAZA  1/75")
        elif k == "R": planta_estructura(cx, "R", "ESTRUCTURA DE CUBIERTA  1/75")
        else: seccion(cx, "x", 6.25, "SECCIÓN A-A' (con estructura)  1/75")
    E = h.E
    filas = [("ELEMENTO", "PERFIL", "UDS/SEP"),
             ("Viguetas terraza salón (E-O, luz 5,75)", E["salon_vigueta"]["perfil"], f"@{E['salon_vigueta']['sep']:.1f} m"),
             ("Viguetas forjado casa (E-O, luz 2,55)", E["casa_vigueta"]["perfil"], f"@{E['casa_vigueta']['sep']:.1f} m"),
             ("Viguetas cubierta (E-O, luz 2,55)", E["cubierta_vigueta"]["perfil"], f"@{E['cubierta_vigueta']['sep']:.1f} m"),
             ("Vigas N-S forjado (continuas)", E["viga_ns"]["perfil"], "3 uds"), ("Vigas N-S cubierta (continuas)", E["viga_cub"]["perfil"], "3 uds"),
             ("Viga de borde del saliente (2 niveles)", E["viga_saliente"]["perfil"], "2 uds"), ("Viga de fachada (2 niveles)", E["viga_fachada"]["perfil"], "2 lineas"),
             ("Pilares (ocultos en muros/tabiques)", E["pilar"]["perfil"], "6 uds"), ("Dintel de la cristalera", E["dintel"]["perfil"], "1 ud"),
             ("Dinteles de puertas y ventanas", "IPE 100-120", "14 uds"),
             ("Zapatas aisladas bajo pilares", f"{E['zapata']['lado']:.1f}x{E['zapata']['lado']:.1f}x0,6", "6 uds")]
    fin = tabla(msp, 300, 282, "CUADRO DE PERFILES (acero S275JR)", filas, (88, 26, 26), 5.4)
    kg = ", ".join(f"{k}: {v:,.0f} kg".replace(",", ".") for k, v in sorted(h.KG.items()))
    notas(msp, 300, fin - 8, [f"Acero total del modelo: {h.KGTOT:,.0f} kg (sin uniones ni placas).".replace(",", "."), kg,
        "Cargas: forjado 4,8 + 2,0 kN/m2; cubierta 6,1 + 1,0 kN/m2 (piedra y paneles solares). Ver memoria_estructura.md.",
        "PRELIMINAR: sismo NCSE-02, terreno, muros existentes, incendio R60 y uniones los define un técnico competente."])
    doc.saveas(nombre); print(nombre)


if __name__ == "__main__":
    for nom, fn in [("planta_baja_v3", lambda cx: planta_dist(cx, "PB", "PLANTA BAJA  esc. 1/75")), ("planta_alta_v3", lambda cx: planta_dist(cx, "PA", "PLANTA ALTA  esc. 1/75")),
                    ("estructura_forjado_v3", lambda cx: planta_estructura(cx, "L1", "ESTRUCTURA FORJADO  1/75")), ("estructura_cubierta_v3", lambda cx: planta_estructura(cx, "R", "ESTRUCTURA CUBIERTA  1/75")),
                    ("seccion_A_v3", lambda cx: seccion(cx, "x", 6.25, "SECCIÓN A-A'  1/75")), ("seccion_B_v3", lambda cx: seccion(cx, "y", 10.05, "SECCIÓN B-B'  1/75"))]:
        d = base.nuevo_doc(); fn(base.Ctx(d, d.modelspace(), 0, 0, 1)); d.saveas(nom + ".dxf"); print(nom)
    lamina_dist("lamina_A1_v3_distribucion.dxf"); lamina_estr("lamina_A1_v3_estructura.dxf")
