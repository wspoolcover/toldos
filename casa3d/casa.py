"""Modelo 3D paramétrico de la vivienda (planos PBE reforma, hojas 06/07).
CadQuery = ingeniería (STEP). GLB = visualización web. Cotas en metros.
El muro central (eje E-O) baja hasta cimentación: zapata corrida + muro continuo PB->PA->cubierta."""
import cadquery as cq

# ---- parámetros ----
W, D = 9.88, 7.20          # ancho (x) y fondo (y) del cuerpo principal
T_EXT, T_CEN, T_TAB = 0.40, 0.30, 0.10
H_PB, H_PA, T_FORJ = 3.01, 2.70, 0.25
H_CIM, ZAPATA_W = 0.60, 1.10
Y_CEN = T_EXT + 3.10       # cara sur del muro central
PORCHE = (6.81, 2.90)      # ancho, fondo (norte)
ROOF_H, VUELO = 1.60, 0.35
# huecos fachada sur (x0, ancho, alto, antepecho) según hoja 07
SUR = [(0.60, 1.20, 1.30, 0.90), (4.03, 0.80, 1.30, 0.90), (7.06, 1.20, 1.30, 0.90)]
Z_PB, Z_PA = 0.0, H_PB + T_FORJ
Z_TOP = Z_PA + H_PA

def box(x, y, z, dx, dy, dz):
    return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x, y, z))

def cut_hueco(wall, x0, w, h, sill, z0, y, t):
    return wall.cut(box(x0, y - 0.01, z0 + sill, w, t + 0.02, h))

# ---- cimentación: zapata perimetral + zapata corrida bajo muro central ----
cim = box(-(ZAPATA_W - T_EXT) / 2, -(ZAPATA_W - T_EXT) / 2, -H_CIM, W + ZAPATA_W - T_EXT, ZAPATA_W, H_CIM)
for (x, y, dx, dy) in [(-(ZAPATA_W-T_EXT)/2, D-T_EXT-(ZAPATA_W-T_EXT)/2, W+ZAPATA_W-T_EXT, ZAPATA_W),
                       (-(ZAPATA_W-T_EXT)/2, 0-(ZAPATA_W-T_EXT)/2, ZAPATA_W, D+ZAPATA_W-T_EXT),
                       (W-T_EXT-(ZAPATA_W-T_EXT)/2, 0-(ZAPATA_W-T_EXT)/2, ZAPATA_W, D+ZAPATA_W-T_EXT)]:
    cim = cim.union(box(x, y, -H_CIM, dx, dy, H_CIM))
zap_cen = box(-(ZAPATA_W-T_EXT)/2, Y_CEN - (ZAPATA_W - T_CEN)/2, -H_CIM, W + ZAPATA_W - T_EXT, ZAPATA_W, H_CIM)
cimentacion = cim.union(zap_cen)

# ---- muros exteriores (mampostería) por planta, con huecos al sur ----
def envolvente(z0, h):
    m = box(0, 0, z0, W, D, h).cut(box(T_EXT, T_EXT, z0 - .01, W - 2*T_EXT, D - 2*T_EXT, h + .02))
    return m
muros_pb = envolvente(Z_PB, H_PB)
muros_pa = envolvente(Z_PA, H_PA)
for x0, w, h, sill in SUR:
    muros_pb = cut_hueco(muros_pb, x0, w, h, sill, Z_PB, 0, T_EXT)                 # ventanas PB
    balcon = x0 != 4.03                                                            # balconeras B1 en PA
    muros_pa = cut_hueco(muros_pa, x0, w, 2.10 if balcon else h, 0.0 if balcon else sill, Z_PA, 0, T_EXT)
# puerta principal norte (P0) hacia porche y hueco de ventana oeste
muros_pb = muros_pb.cut(box(5.10, D - T_EXT - .01, 0, 1.00, T_EXT + .02, 2.10))
muros_pb = muros_pb.cut(box(1.50, D - T_EXT - .01, 0.9, 1.20, T_EXT + .02, 1.30))
muros_pa = muros_pa.cut(box(3.20, D - T_EXT - .01, Z_PA, 1.20, T_EXT + .02, 2.10))
muros_pa = muros_pa.cut(box(6.00, D - T_EXT - .01, Z_PA, 1.20, T_EXT + .02, 2.10))

# ---- MURO CENTRAL: continuo desde cimentación hasta cubierta (planta baja + alta) ----
muro_central = box(T_EXT, Y_CEN, 0, W - 2*T_EXT, T_CEN, Z_TOP)
# pasos de puerta (P1 / hueco de salón) sin interrumpir el resto del muro
for x0 in (2.60, 5.60):
    muro_central = muro_central.cut(box(x0, Y_CEN - .01, 0, 0.90, T_CEN + .02, 2.05))
    muro_central = muro_central.cut(box(x0, Y_CEN - .01, Z_PA, 0.90, T_CEN + .02, 2.05))

# ---- tabiquería ligera ----
Y_N = Y_CEN + T_CEN
tabiques = box(3.20, T_EXT, 0, T_TAB, Y_CEN - T_EXT, H_PB)                      # PB: despacho|baño
tabiques = tabiques.union(box(5.20, T_EXT, 0, T_TAB, Y_CEN - T_EXT, H_PB))     # PB: baño|dormitorio
tabiques = tabiques.union(box(3.20, T_EXT, Z_PA, T_TAB, Y_CEN - T_EXT, H_PA))
tabiques = tabiques.union(box(5.20, T_EXT, Z_PA, T_TAB, Y_CEN - T_EXT, H_PA))
tabiques = tabiques.union(box(5.10, Y_N, Z_PA, T_TAB, D - T_EXT - Y_N, H_PA))  # PA: estar|dormitorio
tabiques = tabiques.union(box(T_EXT, Y_N + 1.90, 0, 2.20, T_TAB, H_PB))        # PB: aseo/escalera

# ---- forjado (con hueco de escalera) y escalera ----
forjado = box(0, 0, H_PB, W, D, T_FORJ).cut(box(0.80, Y_N + .5, H_PB - .01, 1.10, 2.50, T_FORJ + .02))
n = 16; rise = (H_PB + T_FORJ) / n
esc = None
for i in range(n):
    p = box(0.80, Y_N + .5 + i * (2.50 / n), 0, 1.10, 2.50 / n, rise * (i + 1))
    esc = p if esc is None else esc.union(p)
escalera = esc

# ---- porche y terraza (norte) ----
px = (W - PORCHE[0]) / 2
losa_terraza = box(px, D, Z_PA - T_FORJ, PORCHE[0], PORCHE[1], T_FORJ)
pilares = None
for (x, y) in [(px + .15, D + PORCHE[1] - .15), (px + PORCHE[0] - .15, D + PORCHE[1] - .15),
               (px + .15, D + .15), (px + PORCHE[0] - .15, D + .15)]:
    p = box(x - .15, y - .15, 0, .30, .30, Z_PA - T_FORJ)
    pilares = p if pilares is None else pilares.union(p)
antepecho = box(px, D + PORCHE[1] - .10, Z_PA, PORCHE[0], .10, 1.0)

# ---- forjado de cubierta y cubierta a 4 aguas ----
forjado_cub = box(0, 0, Z_TOP, W, D, T_FORJ)
we, de = W + 2*VUELO, D + 2*VUELO
cubierta = (cq.Workplane("XY").workplane(offset=Z_TOP + T_FORJ).center(W/2, D/2)
            .rect(we, de).workplane(offset=ROOF_H).rect(max(we - de, .05), .05).loft(combine=True))

# ---- ensamblaje con colores ----
asm = cq.Assembly(name="vivienda")
partes = [("cimentacion", cimentacion, (.55, .55, .55)), ("muros_PB", muros_pb, (.85, .80, .70)),
          ("muros_PA", muros_pa, (.85, .80, .70)), ("MURO_CENTRAL", muro_central, (.75, .45, .35)),
          ("tabiques", tabiques, (.95, .95, .92)), ("forjado_PB_PA", forjado, (.70, .70, .72)),
          ("escalera", escalera, (.60, .45, .30)), ("losa_terraza", losa_terraza, (.70, .70, .72)),
          ("pilares", pilares, (.65, .65, .65)), ("antepecho", antepecho, (.85, .80, .70)),
          ("forjado_cubierta", forjado_cub, (.70, .70, .72)), ("cubierta", cubierta, (.62, .28, .20))]
for nombre, sol, c in partes:
    asm.add(sol, name=nombre, color=cq.Color(*c, 1))
asm.export("casa.step")
asm.export("casa.glb")
print("OK", {n: round(s.val().Volume(), 2) for n, s, _ in partes})
