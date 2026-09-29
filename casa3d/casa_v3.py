"""Vivienda v3: envolvente sobre croquis (muros existentes 0,55 m), distribución propuesta y estructura de acero.
Sistema de coordenadas del croquis (x este, y hacia arriba del croquis). Según el propietario, la parte alta del croquis
mira al SUR (cocina) y la derecha al ESTE (otro terreno). Metros."""
import json, math
import cadquery as cq
from perfiles import SECC

E = json.load(open("estructura.json"))
# ---- croquis ----
XE, Y_TOP, W_FRONT, W_SUR = 9.55, 16.30, 6.40, 6.68
Y_JUNC, Y_E1, Y_E2, SAL = Y_TOP - 8.98, 8.30, 11.80, 2.50
PTS = [(XE - W_FRONT, 0), (XE, 0), (XE, Y_E1), (XE + SAL, Y_E1), (XE + SAL, Y_E2), (XE, Y_E2), (XE, Y_TOP), (0, Y_TOP), (0, Y_JUNC), (XE - W_SUR, Y_JUNC)]
NB = [(0, Y_JUNC), (XE, Y_JUNC), (XE, Y_E1), (XE + SAL, Y_E1), (XE + SAL, Y_E2), (XE, Y_E2), (XE, Y_TOP), (0, Y_TOP)]   # casa
SB = [(XE - W_FRONT, 0), (XE, 0), (XE, Y_JUNC), (XE - W_SUR, Y_JUNC)]                                                     # salón
T, TP = 0.55, 0.10                       # muro existente, tabique
H_CIM, T_LOSA = 0.60, 0.15
Z_PA, H_PA = 3.26, 2.70
Z_TOP = Z_PA + H_PA
XI0, XI1, YI1 = T, XE - T, Y_TOP - T     # interior de la casa: x .55-9.00, y hasta 15.75
Y_FAC0, Y_FAC1 = Y_JUNC, Y_JUNC + T      # muro de fachada existente entre salón y casa (y 7.32-7.87)
VOID = (5.35, 8.95, 7.15, 11.75)         # hueco de escalera
LINES_X, COL_Y = E["lineas_x"], [7.60, 11.80]

# ---- huecos: (planta, ori, pos, t, ini, w, tipo, sw, etiqueta, antepecho, alto) ----
# ori 'H': muro a lo largo de x, ocupa y in [pos, pos+t]; 'V': a lo largo de y, ocupa x in [pos, pos+t]. sw: giro de hoja (+ / -).
OPEN = [
 ("PB", "H", 0.0, T, 3.85, 3.35, "V", 0, "CR", 0.10, 2.45), ("PB", "H", 0.0, T, 7.55, 1.40, "P2", 1, "P0", 0, 2.20),
 ("PB", "H", Y_FAC0, T, 7.90, 1.00, "L", 0, "", 0, 2.40), ("PB", "H", Y_FAC0, T, 1.20, 1.40, "V", 0, "V", 0.90, 1.30),
 ("PA", "H", Y_FAC0, T, 7.55, 1.40, "P2", 1, "T", 0, 2.20), ("PA", "H", Y_FAC0, T, 3.80, 1.20, "B", 1, "B1", 0, 2.20),
 ("PA", "H", Y_FAC0, T, 1.20, 1.40, "V", 0, "V", 0.90, 1.30),
 ("PB", "H", YI1, T, 6.00, 1.60, "V", 0, "V", 0.90, 1.30), ("PB", "H", YI1, T, 3.60, 1.00, "V", 0, "V", 0.90, 1.30),
 ("PB", "H", YI1, T, 1.00, 0.80, "V", 0, "V", 1.50, 0.60), ("PA", "H", YI1, T, 1.50, 1.40, "V", 0, "V", 0.90, 1.30),
 ("PA", "H", YI1, T, 6.00, 1.60, "V", 0, "V", 0.90, 1.30),
 ("PB", "V", XI1, T, 13.00, 1.60, "V", 0, "V", 0.90, 1.30), ("PA", "V", XI1, T, 13.60, 1.20, "V", 0, "V", 0.90, 1.30),
 ("PB", "V", XE + SAL - T, T, 9.60, 0.90, "V", 0, "V", 1.50, 0.60), ("PA", "V", XE + SAL - T, T, 9.60, 0.90, "V", 0, "V", 1.50, 0.60),
 # puertas y pasos en tabiques
 ("PB", "V", 5.25, TP, 8.05, 0.90, "P", -1, "P2", 0, 2.05), ("PB", "H", 11.75, TP, 1.00, 0.80, "P", 1, "P3", 0, 2.05),
 ("PB", "H", 13.15, TP, 1.00, 0.80, "P", 1, "P3", 0, 2.05), ("PB", "V", 4.95, TP, 12.50, 0.90, "P", -1, "P2", 0, 2.05),
 ("PB", "H", 11.75, TP, 7.30, 1.60, "L", 0, "", 0, 2.40), ("PB", "V", 9.00, TP, 9.40, 0.80, "P", 1, "P3", 0, 2.05),
 ("PA", "H", 11.75, TP, 3.90, 0.80, "P", -1, "P2", 0, 2.05), ("PA", "H", 12.85, TP, 3.90, 0.80, "P", 1, "P2", 0, 2.05),
 ("PA", "H", 12.85, TP, 6.00, 0.80, "P", 1, "P2", 0, 2.05), ("PA", "H", 11.75, TP, 5.35, 1.80, "L", 0, "", 0, 2.40),
 ("PA", "H", 11.75, TP, 7.30, 1.60, "L", 0, "", 0, 2.40), ("PA", "V", 9.00, TP, 9.40, 0.80, "P", 1, "P3", 0, 2.05)]
# tabiques (planta, x, y, dx, dy)
TAB = [("PB", 5.25, 7.87, TP, 3.88), ("PB", 0.55, 11.75, 8.45, TP), ("PB", 0.55, 13.15, 2.50, TP), ("PB", 3.05, 11.85, TP, 3.90),
       ("PB", 4.95, 11.85, TP, 3.90), ("PB", 9.00, 8.85, TP, 2.40),
       ("PA", 0.55, 11.75, 8.45, TP), ("PA", 0.55, 12.85, 8.45, TP), ("PA", 4.90, 12.95, TP, 2.80), ("PA", 5.25, 7.87, TP, 3.88),
       ("PA", 9.00, 8.85, TP, 2.40)]
# estancias para rotular: (planta, nombre, [rects x0,y0,x1,y1])
ROOMS = [
 ("PB", "Salón", [(3.50, 0.55, 7.45, 7.32)]), ("PB", "Pasillo entrada", [(7.55, 0.55, 9.00, 7.32)]),
 ("PB", "Recibidor y escalera", [(5.35, 7.87, 9.00, 11.75)]), ("PB", "Baño grande", [(9.10, 8.85, 11.50, 11.25)]),
 ("PB", "Cocina", [(5.05, 11.85, 9.00, 15.75)]), ("PB", "Dormitorio principal", [(0.55, 7.87, 5.25, 11.75)]),
 ("PB", "Vestidor", [(0.55, 11.85, 3.05, 13.15)]), ("PB", "Baño principal", [(0.55, 13.25, 3.05, 15.75)]),
 ("PB", "Oficina", [(3.15, 11.85, 4.95, 15.75)]),
 ("PA", "Terraza sobre salón", [(3.50, 0.55, 9.00, 7.32)]), ("PA", "Dormitorio 1", [(0.55, 7.87, 5.25, 11.75)]),
 ("PA", "Distribuidor", [(7.25, 7.87, 9.00, 11.75), (0.55, 11.85, 9.00, 12.85)]), ("PA", "Baño", [(9.10, 8.85, 11.50, 11.25)]),
 ("PA", "Dormitorio 2", [(0.55, 12.95, 4.90, 15.75)]), ("PA", "Dormitorio 3", [(5.00, 12.95, 9.00, 15.75)]),
 ("PA", "Hueco escalera", [(5.35, 8.95, 7.15, 11.75)])]


def area(rects): return sum((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in rects)


def prisma(pts, z0, h, off=0.0):
    w = cq.Workplane("XY").workplane(offset=z0).polyline(pts).close()
    if off: w = w.offset2D(off, "intersection")
    return w.extrude(h)


def box(x, y, z, dx, dy, dz): return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x, y, z))


def anillo(pts, z0, h, t): return prisma(pts, z0, h).cut(prisma(pts, z0 - .01, h + .02, -t))


def cortar(solid, planta, z0):
    for pl, ori, pos, t, ini, w, tipo, sw, tag, sill, h in OPEN:
        if pl != planta: continue
        b = box(ini, pos - .01, z0 + sill, w, t + .02, h) if ori == "H" else box(pos - .01, ini, z0 + sill, t + .02, w, h)
        solid = solid.cut(b)
    return solid


# ---------------- obra ----------------
cimentacion = prisma(PTS, -H_CIM, H_CIM, (1.10 - T) / 2).cut(prisma(PTS, -H_CIM - .01, H_CIM + .02, -(T + (1.10 - T) / 2)))
ZAP = E["zapata"]["lado"]
for lx in LINES_X:
    for cy in COL_Y: cimentacion = cimentacion.union(box(lx - ZAP / 2, cy - ZAP / 2, -H_CIM, ZAP, ZAP, H_CIM))

muros_pb = anillo(PTS, 0, Z_PA, T).union(box(XE - W_SUR, Y_FAC0, 0, XI1 - (XE - W_SUR), T, Z_PA))
muros_pb = cortar(muros_pb, "PB", 0)
muros_pa = cortar(anillo(NB, Z_PA, H_PA, T), "PA", Z_PA)
parapeto_terraza = anillo(SB, Z_PA, 1.00, 0.30).cut(box(XE - W_SUR - 1, Y_JUNC - .2, Z_PA - .1, W_SUR + 2, .5, 2))
parapeto_cubierta = anillo(NB, Z_TOP, 0.50, 0.30)

def losa(pts, z_top, hueco=None):
    s = prisma(pts, z_top - T_LOSA, T_LOSA)
    if hueco: s = s.cut(box(hueco[0], hueco[1], z_top - T_LOSA - .01, hueco[2] - hueco[0], hueco[3] - hueco[1], T_LOSA + .02))
    return s

forjado = losa(PTS, Z_PA, VOID)
losa_cubierta = losa(NB, Z_TOP, VOID)
lucernario = box(VOID[0] - .10, VOID[1] - .10, Z_TOP, VOID[2] - VOID[0] + .20, VOID[3] - VOID[1] + .20, .30)

tab_pb = tab_pa = None
for pl, x, y, dx, dy in TAB:
    z0, h = (0, Z_PA - T_LOSA) if pl == "PB" else (Z_PA, H_PA - T_LOSA)
    b = box(x, y, z0, dx, dy, h)
    if pl == "PB": tab_pb = b if tab_pb is None else tab_pb.union(b)
    else: tab_pa = b if tab_pa is None else tab_pa.union(b)
tab_pb, tab_pa = cortar(tab_pb, "PB", 0), cortar(tab_pa, "PA", Z_PA)
murete = box(7.45, T, 0, TP, Y_JUNC - T, 1.00)

# escalera en U: PB -> PA (arranca al norte, y 11.75, sube hacia el sur y vuelve)
RISE, TREAD = Z_PA / 16, 0.24
esc = []
for i in range(8): esc.append(box(6.30, 11.75 - (i + 1) * TREAD, 0, 0.85, TREAD, (i + 1) * RISE))
esc.append(box(5.35, 8.95, 0, 1.80, 0.88, 8 * RISE))
for j in range(8): esc.append(box(5.35, 9.83 + j * TREAD, 0, 0.85, TREAD, (9 + j) * RISE))
escalera = esc[0]
for b in esc[1:]: escalera = escalera.union(b)

# ---------------- estructura de acero ----------------
def _perfil(sec, L):
    h, b, tw, tf = [SECC[sec][i] / 1000 for i in range(4)]
    p = [(-h/2, -b/2), (-h/2, b/2), (-h/2 + tf, b/2), (-h/2 + tf, tw/2), (h/2 - tf, tw/2), (h/2 - tf, b/2), (h/2, b/2), (h/2, -b/2),
         (h/2 - tf, -b/2), (h/2 - tf, -tw/2), (-h/2 + tf, -tw/2), (-h/2 + tf, -b/2)]
    return cq.Workplane("XY").polyline(p).close().extrude(L)

def viga_x(sec, x0, x1, y, ztop):
    h = SECC[sec][0] / 1000
    return _perfil(sec, x1 - x0).rotate((0, 0, 0), (0, 1, 0), 90).translate((x0, y, ztop - h / 2))

def viga_y(sec, y0, y1, x, ztop):
    h = SECC[sec][0] / 1000
    return _perfil(sec, y1 - y0).rotate((0, 0, 0), (0, 1, 0), 90).rotate((0, 0, 0), (0, 0, 1), 90).translate((x, y0, ztop - h / 2))

def pilar(sec, x, y, z0, z1): return _perfil(sec, z1 - z0).translate((x, y, z0))

STEEL = {"viguetas_salon": [], "viguetas_casa": [], "viguetas_cubierta": [], "vigas_forjado": [], "vigas_cubierta": [], "pilares": [], "dintel": []}
KG = {}
def anota(cat, sec, L, geom):
    STEEL[cat].append(geom); KG[sec] = KG.get(sec, 0) + SECC[sec][7] * L
BAY_X = [T / 2, *LINES_X, XE - T / 2]                   # apoyos en muros (eje) y líneas de vigas
Y_END = Y_TOP - T / 2
sv, sc, sq = E["salon_vigueta"], E["casa_vigueta"], E["cubierta_vigueta"]
sols = {k: [] for k in STEEL}
def add(cat, sec, L, solid, geom):
    sols[cat].append(solid); STEEL[cat].append(geom); KG[sec] = KG.get(sec, 0) + SECC[sec][7] * L
for k in list(STEEL): STEEL[k] = []

zt1, zt2 = Z_PA - T_LOSA, Z_TOP - T_LOSA
# viguetas del salón (terraza): E-O de muro a muro
n = int((Y_JUNC - 1.0) / sv["sep"]) + 1
for y in [1.0 + k * sv["sep"] for k in range(n)] + [6.75]:
    if y > Y_JUNC - 0.35 and y != 6.75: continue
    xl = (XE - W_FRONT) + (W_SUR - W_FRONT) * y / Y_JUNC * 0 + ((XE - W_SUR) - (XE - W_FRONT)) * y / Y_JUNC + T / 2
    x0, x1 = xl, XE - T / 2
    add("viguetas_salon", sv["perfil"], x1 - x0, viga_x(sv["perfil"], x0, x1, y, zt1), (x0, y, x1, y, sv["perfil"]))
# viguetas de la casa y de la cubierta: E-O entre muro y líneas de vigas; se omite el hueco de escalera
def viguetas(cat, spec, ztop):
    ys = [Y_FAC1 + 0.45 + k * spec["sep"] for k in range(int((YI1 - Y_FAC1 - 0.45) / spec["sep"]) + 1)]
    for y in ys:
        for a, b in zip(BAY_X, BAY_X[1:]):
            if VOID[1] - 0.05 <= y <= VOID[3] + 0.05 and a >= LINES_X[1] - 1e-6 and b <= LINES_X[2] + 1e-6: continue
            if y > YI1 - 0.2: continue
            add(cat, spec["perfil"], b - a, viga_x(spec["perfil"], a, b, y, ztop), (a, y, b, y, spec["perfil"]))
    # anexo este (baño grande): viguetas E-O
    for y in (9.35, 10.35):
        add(cat, "IPE 100", 2.775, viga_x("IPE 100", XE - T / 2, XE + SAL - T / 2, y, ztop), (XE - T / 2, y, XE + SAL - T / 2, y, "IPE 100"))
viguetas("viguetas_casa", sc, zt1); viguetas("viguetas_cubierta", sq, zt2)
# vigas N-S (forjado y cubierta) sobre las 3 líneas
for lx in LINES_X:
    add("vigas_forjado", E["viga_ns"]["perfil"], Y_END - COL_Y[0], viga_y(E["viga_ns"]["perfil"], COL_Y[0], Y_END, lx, zt1), (lx, COL_Y[0], lx, Y_END, E["viga_ns"]["perfil"]))
    add("vigas_cubierta", E["viga_cub"]["perfil"], Y_END - COL_Y[0], viga_y(E["viga_cub"]["perfil"], COL_Y[0], Y_END, lx, zt2), (lx, COL_Y[0], lx, Y_END, E["viga_cub"]["perfil"]))
hb = SECC[E["viga_cub"]["perfil"]][0] / 1000
for lx in LINES_X:
    for cy in COL_Y:
        add("pilares", E["pilar"]["perfil"], zt2 - hb, pilar(E["pilar"]["perfil"], lx, cy, 0, zt2 - hb), (lx, cy, E["pilar"]["perfil"]))
d = E["dintel"]["perfil"]
add("dintel", d, 4.0, viga_x(d, 3.85 - 0.20, 7.20 + 0.20, T / 2, 2.55 + SECC[d][0] / 1000), (3.65, T / 2, 7.40, T / 2, d))

def comp(lst):
    solids = [s.val() for s in lst]
    return cq.Workplane("XY").newObject([cq.Compound.makeCompound(solids)])

acero = {k: comp(v) for k, v in sols.items() if v}
partes = [("cimentacion", cimentacion, (.55, .55, .55)), ("muros_PB", muros_pb, (.85, .80, .70)), ("muros_PA", muros_pa, (.85, .80, .70)),
          ("parapeto_terraza", parapeto_terraza, (.85, .80, .70)), ("parapeto_cubierta", parapeto_cubierta, (.85, .80, .70)),
          ("forjado_PB_PA", forjado, (.70, .70, .72)), ("forjado_cubierta", losa_cubierta, (.70, .70, .72)),
          ("tabiques_PB", tab_pb, (.95, .95, .92)), ("tabiques_PA", tab_pa, (.95, .95, .92)), ("murete_pasillo", murete, (.90, .88, .80)),
          ("escalera", escalera, (.60, .45, .30)), ("lucernario", lucernario, (.55, .75, .90))]
partes += [("acero_" + k, v, (.20, .32, .55)) for k, v in acero.items()]

KGTOT = sum(KG.values())
if __name__ == "__main__":
    asm = cq.Assembly(name="vivienda_v3")
    for nn, s, col in partes: asm.add(s, name=nn, color=cq.Color(*col, 1))
    asm.export("casa_v3.step"); asm.export("casa_v3.glb")
    print("ok; acero total kg:", round(KGTOT), {k: round(v) for k, v in KG.items()}); print({k: len(v) for k, v in STEEL.items()})
