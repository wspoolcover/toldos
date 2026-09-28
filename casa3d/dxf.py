"""Plantas, secciones y lámina A1 (DXF) cortando los sólidos de casa.py.
Modelo en metros; salida en mm de papel/modelo. Escala de la lámina 1/50."""
import math, ezdxf, cadquery as cq
from ezdxf.enums import TextEntityAlignment as TA
import casa as c

FECHA = "28/09/2026"
ESC = 50
LAYERS = {  # nombre: (color, grosor 1/100 mm, tipo de línea)
    "cimentacion": (8, 25, "Continuous"), "muros_PB": (7, 50, "Continuous"), "muros_PA": (7, 50, "Continuous"),
    "MURO_CENTRAL": (1, 70, "Continuous"), "tabiques": (3, 25, "Continuous"), "forjado_PB_PA": (5, 35, "Continuous"),
    "escalera": (30, 18, "Continuous"), "losa_terraza": (5, 35, "Continuous"), "pilares": (4, 35, "Continuous"),
    "antepecho": (7, 35, "Continuous"), "forjado_cubierta": (5, 35, "Continuous"), "cubierta": (6, 35, "Continuous"),
    "HUECOS": (7, 25, "Continuous"), "CARPINTERIA": (4, 18, "Continuous"), "COTAS": (3, 13, "Continuous"),
    "TEXTO": (2, 13, "Continuous"), "ESCALERA_ALTA": (30, 18, "DASHED"), "CORTES": (1, 35, "DASHDOT"),
    "MARCO": (7, 70, "Continuous"), "TABLA": (7, 25, "Continuous")}

PX = (c.W - c.PORCHE[0]) / 2
Y_N = c.Y_CEN + c.T_CEN
XI0, XI1, YI1 = c.T_EXT, c.W - c.T_EXT, c.D - c.T_EXT
ROOMS = {
    "PB": [("Despacho", XI0, XI0 and c.T_EXT, 3.20, c.Y_CEN), ("Baño", 3.30, c.T_EXT, 5.20, c.Y_CEN),
           ("Dormitorio", 5.30, c.T_EXT, XI1, c.Y_CEN), ("Salón-cocina-escalera", XI0, Y_N, XI1, YI1),
           ("Porche", PX, c.D, PX + c.PORCHE[0], c.D + c.PORCHE[1])],
    "PA": [("Dormitorio 1", XI0, c.T_EXT, 3.20, c.Y_CEN), ("Baño", 3.30, c.T_EXT, 5.20, c.Y_CEN),
           ("Dormitorio 2", 5.30, c.T_EXT, XI1, c.Y_CEN), ("Estar-escalera", XI0, Y_N, 5.10, YI1),
           ("Dormitorio 3", 5.20, Y_N, XI1, YI1), ("Terraza", PX, c.D, PX + c.PORCHE[0], c.D + c.PORCHE[1])]}
STAIR = (0.80, Y_N + 0.5, 1.90, Y_N + 3.0)


def contornos(solid, eje, valor):
    """Polilíneas (m) del corte: eje 'z' planta; 'x'/'y' sección (giro para llevar el plano a z')."""
    s = solid
    if eje == "y": s = s.rotate((0, 0, 0), (1, 0, 0), 90)
    elif eje == "x": s = s.rotate((0, 0, 0), (0, 1, 0), -90)
    try:
        caras = cq.Workplane("XY").add(s).section(valor).vals()
    except Exception:
        return []
    out = []
    for f in caras:
        for e in f.Edges():
            ts = [0, 1] if e.geomType() == "LINE" else [i / 16 for i in range(17)]
            out.append([(e.positionAt(t).x, e.positionAt(t).y) for t in ts])
    return out


class Ctx:
    def __init__(self, doc, msp, ox, oy, s):
        self.doc, self.msp, self.ox, self.oy, self.s = doc, msp, ox, oy, s
        self.K = ESC * s                      # mm de dibujo por mm de papel
        self.m = 1000 * s                     # mm de dibujo por metro

    def t(self, x, y): return (self.ox + x * self.m, self.oy + y * self.m)
    def line(self, a, b, layer): self.msp.add_line(self.t(*a), self.t(*b), dxfattribs={"layer": layer})
    def poly(self, pts, layer, close=False):
        self.msp.add_lwpolyline([self.t(*p) for p in pts], close=close, dxfattribs={"layer": layer})
    def text(self, txt, x, y, h, layer="TEXTO", al=TA.MIDDLE_CENTER):
        e = self.msp.add_text(txt, height=h * self.K, dxfattribs={"layer": layer})
        e.set_placement(self.t(x, y), align=al)
    def dim(self, p1, p2, base, ang):
        d = (abs(p2[0] - p1[0]) if ang == 0 else abs(p2[1] - p1[1]))
        K = self.K
        self.msp.add_linear_dim(base=self.t(*base), p1=self.t(*p1), p2=self.t(*p2), angle=ang, dimstyle="EZDXF",
                                text=f"{d:.2f}", dxfattribs={"layer": "COTAS"},
                                override={"dimtxt": 2.2 * K, "dimasz": 1.8 * K, "dimexe": 1.0 * K, "dimexo": 0.8 * K,
                                          "dimgap": 0.6 * K, "dimtad": 1, "dimclrt": 3}).render()
    def chain_x(self, xs, y0, ybase):
        for a, b in zip(xs, xs[1:]):
            if b - a > 1e-3: self.dim((a, y0), (b, y0), ((a + b) / 2, ybase), 0)
    def chain_y(self, ys, x0, xbase):
        for a, b in zip(ys, ys[1:]):
            if b - a > 1e-3: self.dim((x0, a), (x0, b), (xbase, (a + b) / 2), 90)
    def door(self, hinge, u, v, w):
        """Hoja desde 'hinge' en dirección v (longitud w) y arco hasta la dirección u del hueco."""
        hx, hy = hinge
        self.line((hx, hy), (hx + v[0] * w, hy + v[1] * w), "CARPINTERIA")
        a_u, a_v = math.degrees(math.atan2(u[1], u[0])), math.degrees(math.atan2(v[1], v[0]))
        st, en = (a_u, a_v) if (a_v - a_u) % 360 == 90 else (a_v, a_u)
        self.msp.add_arc(self.t(hx, hy), w * self.m, st, en, dxfattribs={"layer": "CARPINTERIA"})


def hueco_muro(cx, cara, x0, w, tipo, tag):
    """Hueco en muro E-O. cara 'S' (y 0..T_EXT, hoja hacia +y) o 'N' (y D-T..D, hacia -y)."""
    ya, yb = (0, c.T_EXT) if cara == "S" else (c.D - c.T_EXT, c.D)
    inw = 1 if cara == "S" else -1
    yi = yb if cara == "S" else ya               # cara interior
    for x in (x0, x0 + w): cx.line((x, ya), (x, yb), "HUECOS")
    if tipo == "V":                                # ventana: dos líneas de carpintería
        for f in (0.35, 0.65): cx.line((x0, ya + f * (yb - ya)), (x0 + w, ya + f * (yb - ya)), "CARPINTERIA")
    elif tipo == "B1":                             # balconera de 2 hojas
        h = w / 2
        cx.door((x0, yi), (1, 0), (0, inw), h); cx.door((x0 + w, yi), (-1, 0), (0, inw), h)
    else:                                          # P0: 1 hoja
        cx.door((x0, yi), (1, 0), (0, inw), w)
    cx.text(tag, x0 + w / 2, (ya + yb) / 2 - inw * 0.55, 1.8, "TEXTO")


def paso_central(cx, x0, w, k):
    ya, yb = c.Y_CEN, c.Y_CEN + c.T_CEN
    for x in (x0, x0 + w): cx.line((x, ya), (x, yb), "HUECOS")
    cx.door((x0, yb), (1, 0), (0, 1), w) if k % 2 == 0 else cx.door((x0 + w, ya), (-1, 0), (0, -1), w)
    cx.text("P1", x0 + w / 2, ya - 0.3 if k % 2 else yb + 0.3, 1.8)


def puerta_tabique(cx, pos, ini, w, k):
    xa, xb = pos, pos + c.T_TAB
    for y in (ini, ini + w): cx.line((xa, y), (xb, y), "HUECOS")
    cx.door((xb, ini), (0, 1), (1, 0), w) if k % 2 == 0 else cx.door((xa, ini + w), (0, -1), (-1, 0), w)
    cx.text("P2", pos + c.T_TAB / 2 + (0.35 if k % 2 == 0 else -0.35), ini + w / 2, 1.8)


def dibujar_planta(cx, planta, titulo):
    z = 1.20 if planta == "PB" else c.Z_PA + 1.20
    for n, sol, _ in c.partes:
        for pl in contornos(sol.val(), "z", z):
            cx.poly(pl, n)
    # carpintería
    for x0, w, h, sill in c.SUR:
        tipo = "V" if (planta == "PB" or x0 == 4.03) else "B1"
        hueco_muro(cx, "S", x0, w, tipo, "V1" if tipo == "V" else "B1")
    for pl, x0, w, h, sill, tipo in c.NORTE:
        if pl == planta: hueco_muro(cx, "N", x0, w, tipo, tipo if tipo != "V" else "V2")
    for k, (x0, w) in enumerate(c.PASOS_CEN): paso_central(cx, x0, w, k)
    for k, (pl, ori, pos, ini, w) in enumerate([p for p in c.PUERTAS_TAB if p[0] == planta]):
        puerta_tabique(cx, pos, ini, w, k)
    # escalera
    x0, y0, x1, y1 = STAIR
    if planta == "PB":
        for i in range(17): cx.line((x0, y0 + i * (y1 - y0) / 16), (x1, y0 + i * (y1 - y0) / 16), "escalera")
    else:
        cx.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], "ESCALERA_ALTA", True)
    cx.text("ESC.", (x0 + x1) / 2, (y0 + y1) / 2, 2.0)
    # estancias
    for nombre, ax, ay, bx, by in ROOMS[planta]:
        cx.text(nombre, (ax + bx) / 2 + (0.6 if "escalera" in nombre else 0), (ay + by) / 2 + 0.35, 2.4)
        cx.text(f"{bx-ax:.2f} x {by-ay:.2f} m  |  {(bx-ax)*(by-ay):.2f} m²",
                (ax + bx) / 2 + (0.6 if "escalera" in nombre else 0), (ay + by) / 2 - 0.15, 1.8)
    # cotas: sur (huecos y total), este (muros y total), norte (porche)
    xs = sorted({0, c.W} | {x for x0, w, *_ in c.SUR for x in (x0, x0 + w)})
    cx.chain_x(xs, 0, -0.6); cx.dim((0, 0), (c.W, 0), (c.W / 2, -1.2), 0)
    cx.chain_y([0, c.T_EXT, c.Y_CEN, Y_N, YI1, c.D, c.D + c.PORCHE[1]], c.W, c.W + 0.6)
    cx.dim((c.W, 0), (c.W, c.D), (c.W + 1.2, c.D / 2), 90)
    cx.dim((PX, c.D + c.PORCHE[1]), (PX + c.PORCHE[0], c.D + c.PORCHE[1]), (PX + c.PORCHE[0] / 2, c.D + c.PORCHE[1] + 0.6), 0)
    # norte
    cx.line((9.4, c.D + 1.3), (9.4, c.D + 2.3), "COTAS"); cx.text("N", 9.4, c.D + 2.6, 3.0)
    cx.line((9.4, c.D + 2.3), (9.25, c.D + 1.9), "COTAS"); cx.line((9.4, c.D + 2.3), (9.55, c.D + 1.9), "COTAS")
    if planta == "PB":                              # trazas de secciones A-A' y B-B'
        xa, yb = 4.45, c.Y_CEN + c.T_CEN / 2
        cx.line((xa, -0.35), (xa, c.D + c.PORCHE[1] + 0.35), "CORTES")
        cx.line((-0.35, yb), (c.W + 0.35, yb), "CORTES")
        for tx, ty, txt in [(xa, -0.6, "A"), (xa, c.D + c.PORCHE[1] + 0.6, "A'"), (-0.6, yb, "B"), (c.W + 0.6, yb, "B'")]:
            cx.text(txt, tx, ty, 3.0, "CORTES")
        for yy in (-0.35, c.D + c.PORCHE[1] + 0.35):    # flechas hacia -x (se mira hacia el oeste)
            cx.line((xa, yy), (xa - 0.4, yy), "CORTES")
        for xx in (-0.35, c.W + 0.35):                   # flechas hacia +y (se mira hacia el norte)
            cx.line((xx, yb), (xx, yb + 0.4), "CORTES")
    cx.text(titulo, c.W / 2, -2.0, 4.0)


def dibujar_seccion(cx, eje, valor, titulo):
    if eje == "x": tf = lambda p: (p[1], -p[0])
    else: tf = lambda p: (p[0], -p[1])
    for n, sol, _ in c.partes:
        for pl in contornos(sol.val(), eje, valor):
            cx.poly([tf(p) for p in pl], n)
    zc = c.Z_TOP + c.T_FORJ
    zs = [-c.H_CIM, 0, c.H_PB, c.Z_PA, c.Z_TOP, zc, zc + c.ROOF_H]
    if eje == "x":
        ext = c.D + c.PORCHE[1]
        hx = [0, c.T_EXT, c.Y_CEN, Y_N, YI1, c.D, ext]
    else:
        ext = c.W
        hx = sorted({0, c.T_EXT, c.W - c.T_EXT, c.W} | {v for x0, w in c.PASOS_CEN for v in (x0, x0 + w)})
    cx.chain_y(zs, 0, -0.6)
    cx.dim((0, -c.H_CIM), (0, zc + c.ROOF_H), (-1.2, (zc + c.ROOF_H - c.H_CIM) / 2), 90)
    cx.chain_x(hx, -c.H_CIM, -c.H_CIM - 0.6)
    cx.dim((0, -c.H_CIM), (ext, -c.H_CIM), (ext / 2, -c.H_CIM - 1.2), 0)
    for zz, txt in [(0, "±0.00 SUELO PB"), (c.Z_PA, f"+{c.Z_PA:.2f} SUELO PA"), (c.Z_TOP, f"+{c.Z_TOP:.2f} FORJ. CUBIERTA"),
                    (zc + c.ROOF_H, f"+{zc + c.ROOF_H:.2f} CUMBRERA")]:
        cx.line((ext + 0.3, zz), (ext + 1.0, zz), "COTAS"); cx.text(txt, ext + 1.05, zz, 1.8, al=TA.MIDDLE_LEFT)
    cx.text(titulo, ext / 2, -c.H_CIM - 2.0, 4.0)


def nuevo_doc():
    doc = ezdxf.new("R2010", setup=True); doc.units = ezdxf.units.MM
    for n, (col, lw, lt) in LAYERS.items():
        if n not in doc.layers: doc.layers.add(n)
        L = doc.layers.get(n); L.color = col; L.dxf.lineweight = lw; L.dxf.linetype = lt
    return doc


def dibujos(cx, cual):
    if cual == "PB": dibujar_planta(cx, "PB", "PLANTA BAJA  esc. 1/50")
    elif cual == "PA": dibujar_planta(cx, "PA", "PLANTA ALTA  esc. 1/50")
    elif cual == "A": dibujar_seccion(cx, "x", 4.45, "SECCIÓN A-A'  esc. 1/50")
    elif cual == "B": dibujar_seccion(cx, "y", c.Y_CEN + c.T_CEN / 2, "SECCIÓN B-B' por muro central  esc. 1/50")


def cuadro(msp, x0, y0):
    """Cuadro de superficies (mm de papel)."""
    filas = [("ESTANCIA", "PLANTA", "SUP. (m²)")]
    tot = {"PB": 0, "PA": 0}
    for pl in ("PB", "PA"):
        for nombre, ax, ay, bx, by in ROOMS[pl]:
            a = (bx - ax) * (by - ay)
            if nombre not in ("Porche", "Terraza"): tot[pl] += a
            filas.append((nombre, pl, f"{a:.2f}"))
    filas += [("TOTAL P. BAJA (sin porche)", "PB", f"{tot['PB']:.2f}"), ("TOTAL P. ALTA (sin terraza)", "PA", f"{tot['PA']:.2f}"),
              ("TOTAL", "", f"{tot['PB'] + tot['PA']:.2f}")]
    w, h = (105, 55, 30), 7
    msp.add_text("CUADRO DE SUPERFICIES (interiores, estimadas)", height=3.5, dxfattribs={"layer": "TEXTO", "insert": (x0, y0 + 4)})
    y = y0
    for i, f in enumerate(filas):
        x = x0
        for wi, val in zip(w, f):
            msp.add_text(val, height=2.5, dxfattribs={"layer": "TEXTO", "insert": (x + 2, y - h + 2)})
            x += wi
        msp.add_lwpolyline([(x0, y), (x0 + sum(w), y), (x0 + sum(w), y - h), (x0, y - h)], close=True, dxfattribs={"layer": "TABLA"})
        y -= h
    return y


def lamina(nombre):
    doc = nuevo_doc(); msp = doc.modelspace()
    msp.add_lwpolyline([(0, 0), (841, 0), (841, 594), (0, 594)], close=True, dxfattribs={"layer": "MARCO"})
    msp.add_lwpolyline([(8, 8), (833, 8), (833, 586), (8, 586)], close=True, dxfattribs={"layer": "MARCO"})
    cw, chh = 270, 285
    cells = {"PB": (18, 298), "PA": (288, 298), "A": (558, 298), "B": (18, 12)}
    for k, (cx0, cy0) in cells.items():
        if k in ("PB", "PA"): ox, oy = cx0 + 34, cy0 + 44
        else: ox, oy = cx0 + 34, cy0 + (c.H_CIM + 2.2) * 20
        dibujos(Ctx(doc, msp, ox, oy, 1 / ESC), k)
    fin = cuadro(msp, 300, 280)
    msp.add_text("NOTAS: cotas en metros. Alturas libres PB 3.01 m / PA 2.70 m. El muro central (eje E-O, 0.30 m) es continuo desde la "
                 "cimentación hasta la cubierta.", height=2.2, dxfattribs={"layer": "TEXTO", "insert": (300, fin - 8)})
    msp.add_text("Fondo del cuerpo (7.20 m), espesores y cimentación estimados. Carpintería: V ventana, B balconera, P0 entrada, P1/P2 interiores.",
                 height=2.2, dxfattribs={"layer": "TEXTO", "insert": (300, fin - 13)})
    x0, y0, x1, y1 = 640, 14, 825, 100                # cajetín
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True, dxfattribs={"layer": "MARCO"})
    for yy in (32, 50, 68, 84): msp.add_line((x0, yy), (x1, yy), dxfattribs={"layer": "TABLA"})
    msp.add_line((x0 + 120, y0), (x0 + 120, 50), dxfattribs={"layer": "TABLA"})
    T = lambda t, x, y, h=2.6: msp.add_text(t, height=h, dxfattribs={"layer": "TEXTO", "insert": (x, y)})
    T("BORRADOR - SIN VISADO. Basado en proyecto visado exp. 25-01150-BE (COAA, 22/09/25).", x0 + 3, y1 - 6, 2.0)
    T("REFORMA DE VIVIENDA UNIFAMILIAR - Pol. 33, parc. 198, San Roque, Albox (Almería)", x0 + 3, 87, 2.4)
    T("PLANTAS Y SECCIONES - MODELO PARAMÉTRICO (STEP/GLB)", x0 + 3, 71, 3.0)
    T("Plano: PLANTAS, SECCIONES Y COTAS", x0 + 3, 54, 2.6); T("Hoja: 01 / 01", x0 + 123, 54, 2.6)
    T(f"Escala: 1/50 (A1)", x0 + 3, 36, 2.6); T(f"Fecha: {FECHA}", x0 + 123, 36, 2.6)
    T("Unidades: mm (dibujo en papel)", x0 + 3, 18, 2.2); T("Rev.: R00", x0 + 123, 18, 2.6)
    doc.saveas(nombre); print(nombre)


if __name__ == "__main__":
    for nombre, cual in [("planta_baja", "PB"), ("planta_alta", "PA"), ("seccion_transversal", "A"),
                         ("seccion_longitudinal_muro_central", "B")]:
        doc = nuevo_doc(); dibujos(Ctx(doc, doc.modelspace(), 0, 0, 1), cual)
        doc.saveas(nombre + ".dxf"); print(nombre)
    lamina("lamina_A1.dxf")
