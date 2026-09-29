"""Envolvente de la vivienda a construir, sobre el croquis a mano (medidas EXTERIORES, en metros).
Solo lo indicado: contorno, salón (sur), cristalera + puerta + murete de pasillo de entrada, muro central continuo.
El resto (habitaciones, huecos del norte/este, escalera) queda por definir."""
import cadquery as cq

# ---- croquis (cm -> m) ----
XE, Y_TOP = 9.55, 16.30                 # ancho norte, largo total
W_FRONT, W_SUR = 6.40, 6.68             # ancho sur en fachada (cristalera) y al fondo (se abre hacia dentro)
Y_JUNC = Y_TOP - 8.98                   # 7.32: borde sur del bloque norte (lado oeste 898 desde arriba)
Y_E1, Y_E2 = 8.30, 8.30 + 3.50          # saliente este: 830 desde el sur, 350 de largo
SAL = 2.50                              # saliente este: 250 de ancho
PTS = [(XE - W_FRONT, 0), (XE, 0), (XE, Y_E1), (XE + SAL, Y_E1), (XE + SAL, Y_E2), (XE, Y_E2),
       (XE, Y_TOP), (0, Y_TOP), (0, Y_JUNC), (XE - W_SUR, Y_JUNC)]
# ---- supuestos (a confirmar) ----
T, T_CEN = 0.40, 0.30
H_CIM, ZAP = 0.60, 1.10
H_PB, T_FORJ, H_PA = 3.01, 0.25, 2.70
Z_PA = H_PB + T_FORJ
Z_TOP = Z_PA + H_PA
Y_CEN = Y_JUNC + 0.10                   # cara sur del muro central (cara norte enrasada con el muro exterior)
ROOF_H, VUELO = 1.60, 0.35
# fachada sur (interior x = 3.55 .. 9.15)
CRISTALERA = (3.55, 7.75)               # x0, x1
PUERTA = (8.05, 8.95)                   # puerta de entrada normal
MURETE_X, T_MURETE, H_MURETE = 7.75, 0.10, 1.00   # murete bajo del pasillo (lado derecho del salón)
PASO_CEN = (8.05, 8.95)                 # paso del pasillo por el muro central


def prisma(z0, h, off=0.0):
    w = cq.Workplane("XY").workplane(offset=z0).polyline(PTS).close()
    if off: w = w.offset2D(off, "intersection")
    return w.extrude(h)


def box(x, y, z, dx, dy, dz):
    return cq.Workplane("XY").box(dx, dy, dz, centered=False).translate((x, y, z))


def muros(z0, h):
    return prisma(z0, h).cut(prisma(z0 - .01, h + .02, -T))


cimentacion = prisma(-H_CIM, H_CIM, (ZAP - T) / 2).cut(prisma(-H_CIM - .01, H_CIM + .02, -(T + (ZAP - T) / 2)))
cimentacion = cimentacion.union(box(T - .35, Y_CEN + T_CEN / 2 - ZAP / 2, -H_CIM, XE - 2 * T + .70, ZAP, H_CIM))

muros_pb = muros(0, H_PB)
muros_pb = muros_pb.cut(box(CRISTALERA[0], -.01, 0.10, CRISTALERA[1] - CRISTALERA[0], T + .02, 2.45))   # cristalera
muros_pb = muros_pb.cut(box(PUERTA[0], -.01, 0, PUERTA[1] - PUERTA[0], T + .02, 2.10))                # puerta
muros_pa = muros(Z_PA, H_PA)

muro_central = box(T, Y_CEN, 0, XE - 2 * T, T_CEN, Z_TOP)                    # continuo de cimentación a cubierta
for z0 in (0, Z_PA):
    muro_central = muro_central.cut(box(PASO_CEN[0], Y_CEN - .01, z0, PASO_CEN[1] - PASO_CEN[0], T_CEN + .02, 2.05))
murete = box(MURETE_X, T, 0, T_MURETE, Y_CEN - T, H_MURETE)

forjado = prisma(H_PB, T_FORJ)
forjado_cub = prisma(Z_TOP, T_FORJ)


def hip(x0, y0, x1, y1):
    w, d = x1 - x0 + 2 * VUELO, y1 - y0 + 2 * VUELO
    rw, rd = (max(w - d, .05), .05) if w >= d else (.05, max(d - w, .05))
    return (cq.Workplane("XY").workplane(offset=Z_TOP + T_FORJ).center((x0 + x1) / 2, (y0 + y1) / 2)
            .rect(w, d).workplane(offset=ROOF_H).rect(rw, rd).loft(combine=True))


cubierta = hip(0, Y_JUNC, XE, Y_TOP).union(hip(XE - W_SUR, 0, XE, Y_JUNC))

partes = [("cimentacion", cimentacion, (.55, .55, .55)), ("muros_PB", muros_pb, (.85, .80, .70)),
          ("muros_PA", muros_pa, (.85, .80, .70)), ("MURO_CENTRAL", muro_central, (.75, .45, .35)),
          ("murete_pasillo", murete, (.90, .88, .80)), ("forjado_PB_PA", forjado, (.70, .70, .72)),
          ("forjado_cubierta", forjado_cub, (.70, .70, .72)), ("cubierta", cubierta, (.62, .28, .20))]
AREA_EXT = prisma(0, 1).val().Volume()          # m² (planta exterior)
AREA_INT = prisma(0, 1, -T).val().Volume()      # m² (interior, sin descontar muro central)

if __name__ == "__main__":
    asm = cq.Assembly(name="vivienda_v2")
    for n, s, col in partes: asm.add(s, name=n, color=cq.Color(*col, 1))
    asm.export("casa_v2.step"); asm.export("casa_v2.glb")
    print("ok", round(AREA_EXT, 2), round(AREA_INT, 2), {n: round(s.val().Volume(), 1) for n, s, _ in partes})
