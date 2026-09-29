"""Vivienda v3: envolvente sobre croquis (muros existentes 0,55 m), distribución propuesta y estructura de acero.
Coordenadas del croquis en metros: abajo = NORTE (calle, entrada, salón); arriba = SUR (cocina y dormitorio principal)."""
import json, math
import cadquery as cq
from perfiles import SECC

E = json.load(open("estructura.json"))
XE, Y_TOP, W_FRONT, W_SUR = 9.55, 16.30, 6.40, 6.68
Y_JUNC, Y_E1, Y_E2, SAL, SAL_PA = Y_TOP - 8.98, 8.30, 11.80, 2.50, 1.30    # saliente este: 2,50 abajo; en planta alta solo la mitad (1,30)
PTS = [(XE - W_FRONT, 0), (XE, 0), (XE, Y_E1), (XE + SAL, Y_E1), (XE + SAL, Y_E2), (XE, Y_E2), (XE, Y_TOP), (0, Y_TOP), (0, Y_JUNC), (XE - W_SUR, Y_JUNC)]
NB_MAIN = [(0, Y_JUNC), (XE, Y_JUNC), (XE, Y_TOP), (0, Y_TOP)]
NB_PA = [(0, Y_JUNC), (XE, Y_JUNC), (XE, Y_E1), (XE + SAL_PA, Y_E1), (XE + SAL_PA, Y_E2), (XE, Y_E2), (XE, Y_TOP), (0, Y_TOP)]
SB = [(XE - W_FRONT, 0), (XE, 0), (XE, Y_JUNC), (XE - W_SUR, Y_JUNC)]
T, TP, T_BUMP = 0.55, 0.10, 0.30
H_CIM, T_LOSA = 0.60, 0.15
Z_PA, H_PA = 3.26, 2.70
Z_TOP = Z_PA + H_PA
XI1, YI1 = XE - T, Y_TOP - T
Y_FAC0 = Y_JUNC
VOID = (7.25, 8.95, 9.00, 11.75)                     # escalera
LINES_X, COL_Y = E["lineas_x"], [7.60, 11.80]

# ---- huecos: (planta, ori, pos, t, ini, w, tipo, sw, etiqueta, antepecho, alto) ----
OPEN = [
 ("PB", "H", 0.0, T, 3.70, 3.65, "V", 0, "CR", 0.0, 2.55), ("PB", "H", 0.0, T, 7.55, 1.40, "P2", 1, "P0", 0, 2.20),
 ("PB", "H", Y_FAC0, T, 1.20, 1.20, "V", 0, "V", 1.50, 0.60), ("PA", "H", Y_FAC0, T, 1.20, 1.40, "V", 0, "V", 0.90, 1.30),
 ("PB", "H", YI1, T, 1.00, 1.20, "V", 0, "V", 0.90, 1.30), ("PB", "H", YI1, T, 3.00, 1.20, "V", 0, "V", 0.90, 1.30),
 ("PB", "H", YI1, T, 5.55, 1.20, "V", 0, "V", 0.90, 1.30), ("PB", "H", YI1, T, 7.50, 1.00, "P", -1, "P0", 0, 2.10),
 ("PA", "H", YI1, T, 1.00, 1.20, "V", 0, "V", 0.90, 1.30), ("PA", "H", YI1, T, 3.00, 1.20, "V", 0, "V", 0.90, 1.30),
 ("PA", "H", YI1, T, 5.55, 1.20, "V", 0, "V", 0.90, 1.30), ("PA", "H", YI1, T, 7.50, 1.00, "V", 0, "V", 0.90, 1.30),
 ("PB", "V", XI1, T, 13.00, 1.60, "V", 0, "V", 0.90, 1.30), ("PA", "V", XI1, T, 13.60, 1.20, "V", 0, "V", 0.90, 1.30),
 ("PB", "V", XE + SAL - T, T, 9.60, 0.90, "V", 0, "V", 1.50, 0.60),
 # puertas y pasos en tabiques
 ("PB", "V", 3.35, TP, 10.20, 0.90, "P", -1, "P2", 0, 2.05), ("PB", "H", 9.35, TP, 1.50, 0.80, "P", -1, "P3", 0, 2.05),
 ("PB", "H", 11.75, TP, 1.50, 0.80, "P", 1, "P3", 0, 2.05), ("PB", "H", 11.75, TP, 5.30, 1.80, "L", 0, "", 0, 2.40),
 ("PB", "V", 9.00, TP, 9.20, 0.80, "P", 1, "P3", 0, 2.05),
 ("PA", "V", 3.35, TP, 9.50, 0.90, "P", -1, "P2", 0, 2.05), ("PA", "H", 11.75, TP, 3.60, 0.80, "P", 1, "P2", 0, 2.05),
 ("PA", "H", 11.75, TP, 5.50, 0.80, "P", 1, "P2", 0, 2.05), ("PA", "V", 9.00, TP, 9.20, 0.80, "P", 1, "P3", 0, 2.05)]
TAB = [("PB", 3.35, 7.87, TP, 3.88), ("PB", 0.55, 9.35, 2.80, TP), ("PB", 0.55, 11.75, 8.45, TP), ("PB", 4.95, 11.85, TP, 3.90),
       ("PB", 7.15, 8.95, TP, 2.80), ("PB", 9.00, 8.85, TP, 2.40), ("PB", 3.45, 9.55, 2.10, TP),
       ("PA", 3.35, 7.87, TP, 3.88), ("PA", 0.55, 11.75, 8.45, TP), ("PA", 4.95, 11.85, TP, 3.90), ("PA", 7.15, 8.95, TP, 2.80), ("PA", 9.00, 8.85, TP, 2.40)]
ROOMS = [
 ("PB", "Salón con comedor", [(3.68, 0.55, 7.45, 7.87), (3.45, 7.87, 5.55, 9.55)]), ("PB", "Pasillo entrada", [(7.55, 0.55, 9.00, 7.87)]),
 ("PB", "Entrada", [(7.25, 7.87, 9.00, 8.95)]), ("PB", "Escalera", [(7.25, 8.95, 9.00, 11.75)]), ("PB", "Baño grande", [(9.10, 8.85, 11.50, 11.25)]),
 ("PB", "Sala de estar y paso", [(3.45, 9.65, 7.15, 11.75), (5.65, 7.87, 7.15, 9.65)]), ("PB", "Cocina", [(5.05, 11.85, 9.00, 15.75)]),
 ("PB", "Dormitorio principal", [(0.55, 11.85, 4.95, 15.75)]), ("PB", "Vestidor", [(0.55, 9.45, 3.35, 11.75)]), ("PB", "Baño principal", [(0.55, 7.87, 3.35, 9.35)]),
 ("PA", "Terraza sobre salón", [(3.68, 0.55, 7.45, 7.32)]), ("PA", "Sala familiar", [(3.45, 7.87, 7.15, 11.75)]), ("PA", "Entrada", [(7.25, 7.87, 9.00, 8.95)]),
 ("PA", "Baño", [(9.10, 8.85, 10.55, 11.25)]), ("PA", "Dormitorio 1", [(0.55, 7.87, 3.35, 11.75)]), ("PA", "Dormitorio 2", [(0.55, 11.85, 4.95, 15.75)]),
 ("PA", "Dormitorio 3 / despacho", [(5.05, 11.85, 9.00, 15.75)]), ("PA", "Hueco escalera", [(7.25, 8.95, 9.00, 11.75)])]


def area(rects): return sum((x1 - x0) * (y1 - y0) for x0, y0, x1, y1 in rects)
def box(x, y, z, dx, dy, dz): return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x, y, z))


def prisma(pts, z0, h, off=0.0):
    w = cq.Workplane("XY").workplane(offset=z0).polyline(pts).close()
    if off: w = w.offset2D(off, "intersection")
    return w.extrude(h)


def anillo(pts, z0, h, t): return prisma(pts, z0, h).cut(prisma(pts, z0 - .01, h + .02, -t))


def cortar(solid, planta, z0):
    for pl, ori, pos, t, ini, w, tipo, sw, tag, sill, h in OPEN:
        if pl != planta: continue
        solid = solid.cut(box(ini, pos - .01, z0 + sill, w, t + .02, h) if ori == "H" else box(pos - .01, ini, z0 + sill, t + .02, w, h))
    return solid


# ---------------- obra ----------------
ZAP = E["zapata"]["lado"]
cimentacion = prisma(PTS, -H_CIM, H_CIM, (1.10 - T) / 2).cut(prisma(PTS, -H_CIM - .01, H_CIM + .02, -(T + (1.10 - T) / 2)))
for lx in LINES_X:
    for cy in COL_Y: cimentacion = cimentacion.union(box(lx - ZAP / 2, cy - ZAP / 2, -H_CIM, ZAP, ZAP, H_CIM))

muros_pb = cortar(anillo(PTS, 0, Z_PA, T).union(box(XE - W_SUR, Y_FAC0, 0, 3.45 - (XE - W_SUR), T, Z_PA)), "PB", 0)
# planta alta: casa sin muro de fachada (cierre acristalado), saliente de baño con muros ligeros y solo la mitad de fondo
pa = anillo(NB_MAIN, Z_PA, H_PA, T).cut(box(3.45, Y_FAC0 - .01, Z_PA - .01, XI1 - 3.45, T + .02, H_PA + .02))
pa = pa.cut(box(XI1 - .01, Y_E1, Z_PA - .01, T + .02, Y_E2 - Y_E1, H_PA + .02))
for (x, y, dx, dy) in [(XI1, Y_E1, XE + SAL_PA - XI1, T_BUMP), (XI1, Y_E2 - T_BUMP, XE + SAL_PA - XI1, T_BUMP), (XE + SAL_PA - T_BUMP, Y_E1, T_BUMP, Y_E2 - Y_E1)]:
    pa = pa.union(box(x, y, Z_PA, dx, dy, H_PA))
muros_pa = cortar(pa, "PA", Z_PA)
parapeto_terraza = anillo(SB, Z_PA, 1.00, 0.30).cut(box(XE - W_SUR - 1, Y_JUNC - .2, Z_PA - .1, W_SUR + 2, .5, 2))
parapeto_cubierta = anillo(NB_PA, Z_TOP, 0.50, 0.30)

def losa(pts, z_top, hueco):
    return prisma(pts, z_top - T_LOSA, T_LOSA).cut(box(hueco[0], hueco[1], z_top - T_LOSA - .01, hueco[2] - hueco[0], hueco[3] - hueco[1], T_LOSA + .02))

forjado = losa(PTS, Z_PA, VOID)
losa_cubierta = losa(NB_PA, Z_TOP, VOID)
lucernario = box(VOID[0] - .05, VOID[1] - .05, Z_TOP, VOID[2] - VOID[0] + .10, VOID[3] - VOID[1] + .10, .05)
cristal_pb = box(3.70, 0.24, 0.0, 3.65, 0.04, 2.55)
cristal_pa = box(3.45, Y_FAC0 + 0.25, Z_PA, XI1 - 3.45, 0.04, H_PA - T_LOSA)   # cierre acristalado de la casa hacia la terraza

def tabiques(pl):
    z0, h = (0, Z_PA - T_LOSA) if pl == "PB" else (Z_PA, H_PA - T_LOSA)
    s = None
    for p, x, y, dx, dy in TAB:
        if p != pl: continue
        b = box(x, y, z0, dx, dy, h); s = b if s is None else s.union(b)
    return cortar(s, pl, z0)
tab_pb, tab_pa = tabiques("PB"), tabiques("PA")
murete = box(7.45, T, 0, TP, Y_JUNC - T, 1.00)

# escalera en U: pie al sur de la entrada (y 8.95); sube por el lado este, gira arriba y vuelve por el oeste hasta la planta alta
RISE, TREAD = Z_PA / 16, 0.24
esc = [box(8.15, 8.95 + i * TREAD, 0, 0.85, TREAD, (i + 1) * RISE) for i in range(8)]
esc.append(box(7.25, 8.95 + 8 * TREAD, 0, 1.75, 0.88, 8 * RISE))
esc += [box(7.25, 8.95 + 8 * TREAD - (j + 1) * TREAD, 0, 0.85, TREAD, (9 + j) * RISE) for j in range(8)]
escalera = esc[0]
for b in esc[1:]: escalera = escalera.union(b)

# ---------------- estructura de acero ----------------
def _perfil(sec, L):
    h, b, tw, tf = [SECC[sec][i] / 1000 for i in range(4)]
    p = [(-h/2, -b/2), (-h/2, b/2), (-h/2 + tf, b/2), (-h/2 + tf, tw/2), (h/2 - tf, tw/2), (h/2 - tf, b/2), (h/2, b/2), (h/2, -b/2),
         (h/2 - tf, -b/2), (h/2 - tf, -tw/2), (-h/2 + tf, -tw/2), (-h/2 + tf, -b/2)]
    return cq.Workplane("XY").polyline(p).close().extrude(L)

def viga_x(sec, x0, x1, y, ztop):
    return _perfil(sec, x1 - x0).rotate((0, 0, 0), (0, 1, 0), 90).translate((x0, y, ztop - SECC[sec][0] / 2000))
def viga_y(sec, y0, y1, x, ztop):
    return _perfil(sec, y1 - y0).rotate((0, 0, 0), (0, 1, 0), 90).rotate((0, 0, 0), (0, 0, 1), 90).translate((x, y0, ztop - SECC[sec][0] / 2000))
def pilar(sec, x, y, z0, z1): return _perfil(sec, z1 - z0).translate((x, y, z0))

STEEL = {k: [] for k in ("viguetas_salon", "viguetas_casa", "viguetas_cubierta", "vigas_forjado", "vigas_cubierta", "pilares", "dintel")}
sols = {k: [] for k in STEEL}; KG = {}
def add(cat, sec, L, solid, geom):
    sols[cat].append(solid); STEEL[cat].append(geom); KG[sec] = KG.get(sec, 0) + SECC[sec][7] * L

BAY_X = [T / 2, *LINES_X, XE - T / 2]; Y_END = Y_TOP - T / 2
sv, sc, sq = E["salon_vigueta"], E["casa_vigueta"], E["cubierta_vigueta"]
zt1, zt2 = Z_PA - T_LOSA, Z_TOP - T_LOSA
for y in [1.0 + k * sv["sep"] for k in range(int((Y_JUNC - 1.0) / sv["sep"]) + 1)] + [6.75]:
    if y > Y_JUNC - 0.35 and y != 6.75: continue
    x0, x1 = (XE - W_FRONT) + ((XE - W_SUR) - (XE - W_FRONT)) * y / Y_JUNC + T / 2, XE - T / 2
    add("viguetas_salon", sv["perfil"], x1 - x0, viga_x(sv["perfil"], x0, x1, y, zt1), (x0, y, x1, y, sv["perfil"]))

def viguetas(cat, spec, ztop):
    for k in range(int((YI1 - (Y_JUNC + T) - 0.45) / spec["sep"]) + 1):
        y = Y_JUNC + T + 0.45 + k * spec["sep"]
        if y > YI1 - 0.2: continue
        for a, b in zip(BAY_X, BAY_X[1:]):
            if VOID[1] - 0.05 <= y <= VOID[3] + 0.05 and a >= LINES_X[2] - 1e-6: continue          # hueco de escalera
            add(cat, spec["perfil"], b - a, viga_x(spec["perfil"], a, b, y, ztop), (a, y, b, y, spec["perfil"]))
    for y in (9.35, 10.35):                                                                           # saliente del baño (piso bajo)
        if cat == "viguetas_casa": add(cat, "IPE 100", 2.775, viga_x("IPE 100", XE - T / 2, XE + SAL - T / 2, y, ztop), (XE - T / 2, y, XE + SAL - T / 2, y, "IPE 100"))
viguetas("viguetas_casa", sc, zt1); viguetas("viguetas_cubierta", sq, zt2)
for lx in LINES_X:
    add("vigas_forjado", E["viga_ns"]["perfil"], Y_END - COL_Y[0], viga_y(E["viga_ns"]["perfil"], COL_Y[0], Y_END, lx, zt1), (lx, COL_Y[0], lx, Y_END, E["viga_ns"]["perfil"]))
    add("vigas_cubierta", E["viga_cub"]["perfil"], Y_END - COL_Y[0], viga_y(E["viga_cub"]["perfil"], COL_Y[0], Y_END, lx, zt2), (lx, COL_Y[0], lx, Y_END, E["viga_cub"]["perfil"]))
hb = SECC[E["viga_cub"]["perfil"]][0] / 1000
for lx in LINES_X:
    for cy in COL_Y: add("pilares", E["pilar"]["perfil"], zt2 - hb, pilar(E["pilar"]["perfil"], lx, cy, 0, zt2 - hb), (lx, cy, E["pilar"]["perfil"]))
vfp = E["viga_fachada"]["perfil"]; nodos = [XE - W_SUR - 0.27, *LINES_X, XI1 + T / 2]
for cat, zt in (("vigas_forjado", zt1), ("vigas_cubierta", zt2)):
    for a, b in zip(nodos, nodos[1:]): add(cat, vfp, b - a, viga_x(vfp, a, b, 7.60, zt), (a, 7.60, b, 7.60, vfp))
d = E["dintel"]["perfil"]
add("dintel", d, 4.05, viga_x(d, 3.50, 7.55, T / 2, 2.55 + SECC[d][0] / 1000), (3.50, T / 2, 7.55, T / 2, d))

def comp(lst): return cq.Workplane("XY").newObject([cq.Compound.makeCompound([s.val() for s in lst])])
acero = {k: comp(v) for k, v in sols.items() if v}

# ---------------- mobiliario y chimenea (solo para ver el conjunto) ----------------
MOB = [box(6.45, 1.05, 0, .75, 3.30, .85), box(5.05, 3.65, 0, 1.40, .70, .45), box(5.05, 1.05, 0, 1.40, .70, .45), box(5.35, 2.05, 0, .80, 1.35, .40),   # sofá en U y mesa baja
       box(3.60, 1.60, .70, .16, 1.90, 1.00),                                                                                                          # pantalla
       box(4.55, 5.25, 0, 1.00, 2.05, .75), *[box(x, y, 0, .22, .40, .45) for y in (5.4, 6.1, 6.8) for x in (4.27, 5.61)],                              # comedor
       box(0.55, 13.15, 0, 2.00, 1.60, .50), box(0.55, 9.55, 0, .60, 2.05, 2.20), box(1.15, 11.20, 0, 2.15, .50, 2.20), box(0.65, 7.97, 0, 1.75, .70, .55),  # suite
       box(6.0, 13.2, 0, 2.2, .8, .90), box(5.15, 15.2, 0, 3.7, .5, .90),                                                                              # cocina
       box(0.7, 9.3, Z_PA, 2.0, 1.6, .50), box(0.7, 13.2, Z_PA, 2.0, 1.6, .50), box(6.0, 13.2, Z_PA, 2.0, 1.6, .50),                                    # camas de arriba
       box(4.0, 9.0, Z_PA, 2.4, 0.9, .45)]                                                                                                              # sofá de la sala familiar
mobiliario = comp(MOB)
chimenea = comp([box(3.50, 8.75, 0, 1.15, .80, 1.25), box(3.70, 8.95, 1.25, .50, .50, Z_TOP + 1.0 - 1.25)])   # hogar y humero, sube por la esquina hasta pasar la cubierta

partes = [("cimentacion", cimentacion, (.55, .55, .55)), ("muros_PB", muros_pb, (.85, .80, .70)), ("muros_PA", muros_pa, (.85, .80, .70)),
          ("parapeto_terraza", parapeto_terraza, (.85, .80, .70)), ("parapeto_cubierta", parapeto_cubierta, (.85, .80, .70)),
          ("forjado_PB_PA", forjado, (.70, .70, .72)), ("forjado_cubierta", losa_cubierta, (.70, .70, .72)),
          ("tabiques_PB", tab_pb, (.95, .95, .92)), ("tabiques_PA", tab_pa, (.95, .95, .92)), ("murete_pasillo", murete, (.90, .88, .80)),
          ("escalera", escalera, (.60, .45, .30)), ("lucernario", lucernario, (.55, .75, .90)),
          ("cristal_PB", cristal_pb, (.55, .75, .90)), ("cristal_PA", cristal_pa, (.55, .75, .90)),
          ("mobiliario", mobiliario, (.78, .68, .55)), ("chimenea", chimenea, (.60, .30, .25))]
partes += [("acero_" + k, v, (.20, .32, .55)) for k, v in acero.items()]
KGTOT = sum(KG.values())

if __name__ == "__main__":
    asm = cq.Assembly(name="vivienda_v3")
    for nn, s, col in partes: asm.add(s, name=nn, color=cq.Color(*col, 0.45 if nn.startswith("cristal") else 1))
    asm.export("casa_v3.step"); asm.export("casa_v3.glb")
    print("ok; acero total kg:", round(KGTOT), {k: round(v) for k, v in KG.items()}); print({k: len(v) for k, v in STEEL.items()})
