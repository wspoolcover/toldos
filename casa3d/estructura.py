"""Predimensionado de la estructura de acero (S275JR). PRELIMINAR: la calcula y firma un técnico competente.
Unidades: kN, m, cm (secciones), MPa. Valores de prontuario (IPE/HEB) redondeados."""
import json, math

FY, GM0, GM1, E = 275.0, 1.05, 1.05, 210e3          # MPa
GG, GQ = 1.35, 1.50                                 # coeficientes parciales (ELU, CTE DB-SE)
from perfiles import IPE, HEB, SECC


# ---- cargas (kN/m²) ----
G_FORJ = 2.6            # chapa colaborante + hormigón 12 cm
G_PAV, G_TAB = 1.2, 1.0 # pavimento interior, tabiquería ligera
G_TERR = 2.2            # solado + aislamiento + impermeabilización + pendientes
G_CUB = G_FORJ + 2.2 + 1.0 + 0.3   # forjado + aislamiento/pendientes/impermeabilización + piedra/grava + paneles solares
G_VIG = 2.02                                         # forjado (17+5)x71 con bovedilla de poliestireno (ficha Prearcon)
G_HOUSE, G_TERRAZA = G_VIG + G_PAV + G_TAB, G_FORJ + G_TERR
G_CUB = G_VIG + 2.2 + 1.0 + 0.3
Q_HOUSE, Q_TERRAZA, Q_CUB = 2.0, 2.0, 1.0   # uso vivienda / terraza privada / cubierta accesible solo privadamente (nieve 0,5 no simultánea)
GAMMA_MURO = 20.0       # kN/m³ mampostería

def w(name): return SECC[name][7] * 9.81 / 1000        # peso propio kN/m

def check_viga(name, L, trib, G, Q, extra_line_G=0.0, extra_line_Q=0.0, lim_tot=300, lim_q=400):
    """Viga biapoyada de luz L (m), ancho tributario trib (m). Devuelve dict con ratios."""
    h, b, tw, tf, A, I, Wpl, kg, iz = SECC[name]
    g = G * trib + w(name) + extra_line_G
    q = Q * trib + extra_line_Q
    qd = GG * g + GQ * q
    M, V = qd * L**2 / 8, qd * L / 2
    Mrd = Wpl * 1e-6 * FY / GM0 * 1e3                    # kNm
    Vrd = (h * tw * 1e-6) * FY / (math.sqrt(3) * GM0) * 1e3
    Icm = I * 1e-8
    d_tot = 5 * (g + q) * L**4 / (384 * E * 1e3 * Icm)   # m
    d_q = 5 * q * L**4 / (384 * E * 1e3 * Icm)
    return dict(name=name, L=L, M=M, Mrd=Mrd, V=V, Vrd=Vrd, rM=M / Mrd, rV=V / Vrd,
                d_tot_mm=d_tot * 1e3, d_q_mm=d_q * 1e3, lim_tot_mm=L / lim_tot * 1e3, lim_q_mm=L / lim_q * 1e3,
                ok=(M <= Mrd and V <= Vrd and d_tot <= L / lim_tot and d_q <= L / lim_q), kg=kg, R=qd * L / 2)

def check_cont(name, L1, L2, trib, G, Q, extra_G=0.0, lim_tot=300, lim_q=400):
    """Viga continua de dos vanos (L1 >= L2) con carga uniforme: momento en el apoyo central (teorema de los tres momentos)."""
    h, b, tw, tf, A, I, Wpl, kg, iz = SECC[name]
    g = G * trib + w(name) + extra_G; q = Q * trib
    qd = GG * g + GQ * q
    MB = qd * (L1**3 + L2**3) / (8 * (L1 + L2))
    VB = qd * L1 / 2 + MB / L1
    RB = qd * (L1 + L2) / 2 + MB * (1 / L1 + 1 / L2)
    Mrd = Wpl * 1e-6 * FY / GM0 * 1e3; Vrd = (h * tw * 1e-6) * FY / (math.sqrt(3) * GM0) * 1e3
    EI = E * 1e3 * I * 1e-8
    d_tot = 0.0054 * (g + q) * L1**4 / EI; d_q = 0.0054 * q * L1**4 / EI      # flecha máxima de dos vanos iguales (aprox.)
    return dict(name=name, M=MB, Mrd=Mrd, rM=MB / Mrd, rV=VB / Vrd, RB=RB, d_tot_mm=d_tot * 1e3, lim_tot_mm=L1 / lim_tot * 1e3,
                ok=(MB <= Mrd and VB <= Vrd and d_tot <= L1 / lim_tot and d_q <= L1 / lim_q), kg=kg)

def elegir(L, G, Q, tabla, spacings, trib_fn=lambda s: s, **kw):
    """Elige la sección más ligera por m² entre separaciones candidatas (prefiere secciones pequeñas)."""
    mejores = []
    for s in spacings:
        for n in tabla:
            r = check_viga(n, L, trib_fn(s), G, Q, **kw)
            if r["ok"]:
                mejores.append((r["kg"] / s, s, r)); break
    mejores.sort(key=lambda t: (t[0], -t[1]))
    return mejores

def pandeo_pilar(name, N, Lcr):
    h, b, tw, tf, A, I, Wpl, kg, iz = SECC[name]
    lam = (Lcr * 100 / iz) / (math.pi * math.sqrt(E / FY))
    phi = 0.5 * (1 + 0.49 * (lam - 0.2) + lam**2)          # curva c (eje débil HEB)
    chi = min(1.0, 1 / (phi + math.sqrt(phi**2 - lam**2)))
    Nbrd = chi * A * 1e-4 * FY / GM1 * 1e3
    return dict(name=name, N=N, Nbrd=Nbrd, ratio=N / Nbrd, chi=chi)

R = {}; out = []
P = out.append
# ---------- geometría base ----------
L_SAL = 5.75                    # luz de viguetas del salón (E-O), entre ejes de apoyo en muros
LINES_X = [3.10, 5.30, 7.20]    # líneas de vigas N-S (coinciden con tabiques y con el hueco de escalera)
BAYS = [2.55, 2.20, 1.90, 1.80] # luces de viguetas E-O entre muros y líneas de vigas
SPAN_NS = [4.20, 3.95]          # vanos de vigas N-S entre pilares/muro
TRIB = [(BAYS[i] + BAYS[i + 1]) / 2 for i in range(3)]   # anchos tributarios de las tres líneas de vigas

P("# Predimensionado de estructura de acero (PRELIMINAR)\n")
P("Acero S275JR (fy = 275 MPa), γM0 = γM1 = 1,05, ELU 1,35 G + 1,50 Q, flecha total L/300 y de sobrecarga L/400 (CTE DB-SE).\n")
P("| Carga | G (kN/m²) | Q (kN/m²) |\n|---|---|---|")
P(f"| Forjado de la casa (planta alta) | {G_HOUSE:.1f} | {Q_HOUSE:.1f} |")
P(f"| Terraza transitable sobre el salón | {G_TERRAZA:.1f} | {Q_TERRAZA:.1f} |")
P(f"| Cubierta plana no transitable (piedra + paneles solares) | {G_CUB:.1f} | {Q_CUB:.1f} (mantenimiento; nieve 0,5 supuesta) |\n")

# 1) viguetas terraza sobre el salón
sal = elegir(L_SAL, G_TERRAZA, Q_TERRAZA, IPE, [1.0, 1.2])
P("## Terraza sobre el salón: viguetas E-O (luz 5,75 m)\n| Sección | Separación (m) | kg/m² | M/Mrd | Flecha total / límite (mm) |\n|---|---|---|---|---|")
for kgm2, s, r in sal[:4]: P(f"| {r['name']} | {s:.1f} | {kgm2:.1f} | {r['rM']:.2f} | {r['d_tot_mm']:.1f} / {r['lim_tot_mm']:.1f} |")
R["salon_vigueta"] = dict(perfil=sal[0][2]["name"], sep=sal[0][1], luz=L_SAL)

# 1b) alternativa: forjado de vigueta pretensada y bovedilla (ficha Prearcon T-18, forjado (25+5)*71, por metro de ancho)
#     Mu: T-1 28,9 · T-2 40,3 · T-3 50,8 · T-4 60,5 kN·m/m; Vu 29,8-47,9 kN/m; rigidez fisurada EI ≈ 17,8-18,8 MN·m²/m; peso 3,71 (bovedilla de hormigón) o 2,51 kN/m² (poliestireno)
FICHA = {"T-2": (40.27, 34.29, 18.10), "T-3": (50.80, 38.60, 18.44), "T-4": (60.49, 43.04, 18.78)}
AREA_SAL = 40.0                                      # m² aprox. de terraza sobre el salón y el pasillo (entre ejes de muros)
def vigueta(g_forj, tipo):
    G = g_forj + G_TERR; qd = GG * G + GQ * Q_TERRAZA
    M, V = qd * L_SAL**2 / 8, qd * L_SAL / 2
    Mu, Vu, EI = FICHA[tipo]
    dG = 5 * G * 1e-3 * L_SAL**4 / (384 * EI); dQ = 5 * Q_TERRAZA * 1e-3 * L_SAL**4 / (384 * EI)   # m, flecha instantánea (sección fisurada)
    d_lp = (dG * 3 + dQ) * 1e3                                                                     # con fluencia (factor 2 sobre la carga permanente)
    return dict(G=G, qd=qd, M=M, V=V, rM=M / Mu, rV=V / Vu, d_lp=d_lp, lim=L_SAL / 300 * 1e3, R=qd * L_SAL / 2, ok=(M <= Mu and V <= Vu and d_lp <= L_SAL / 300 * 1e3))
P("\n## Terraza sobre el salón: alternativa de forjado de vigueta pretensada y bovedilla (datos de fabricante)\n")
P("Ficha técnica de [Prefabricados Arcón, forjado T-18](https://prearcon.com/pdf/VIGUETA%20T18.pdf): forjado (25+5)×71, peso 3,71 kN/m² con bovedilla de hormigón o 2,51 con bovedilla de poliestireno. El fabricante debe confirmar la luz de 5,75 m con su ficha de autorización de uso.\n")
P("| Forjado (25+5)×71 | Peso propio | G total | M/Mu | V/Vu | Flecha con fluencia / límite (mm) |\n|---|---|---|---|---|---|")
ops = {}
for nom, gf in (("bovedilla de hormigón", 3.71), ("bovedilla de poliestireno", 2.51)):
    for t in ("T-2", "T-3", "T-4"):
        r = vigueta(gf, t)
        if r["ok"]: ops[nom] = (t, gf, r); P(f"| {nom}, vigueta {t} | {gf:.2f} | {r['G']:.2f} | {r['rM']:.2f} | {r['rV']:.2f} | {r['d_lp']:.1f} / {r['lim']:.1f} |"); break
t, gf, rv = ops["bovedilla de poliestireno"]
kg_m2 = SECC[R["salon_vigueta"]["perfil"]][7] / R["salon_vigueta"]["sep"]
c_ac = (kg_m2 * 2.4 + 50, kg_m2 * 5.5 + 80); c_vg = (55, 85)
P(f"\nElegida: **(25+5)×71 con vigueta {t} y bovedilla de poliestireno** (peso {gf:.2f} kN/m², más ligera que la solución de acero con chapa). Reacción en cada muro ≈ {rv['R']:.0f} kN/m (con IPE 240 y chapa serían unos 27 kN/m).")
P(f"\nCoste orientativo por m² ({AREA_SAL:.0f} m²): acero (IPE 240 a 1,2 m: {kg_m2:.1f} kg/m² × 2,4-5,5 €/kg) + chapa colaborante 50-80 €/m² = **{c_ac[0]:.0f}-{c_ac[1]:.0f} €/m²**; vigueta y bovedilla, ya con viguetas: **{c_vg[0]}-{c_vg[1]} €/m²**. Ahorro estimado **{(c_ac[0]-c_vg[1])*AREA_SAL/1000:.1f}-{(c_ac[1]-c_vg[0])*AREA_SAL/1000:.1f} mil €** y unos {R['salon_vigueta']['perfil']}: {kg_m2 * AREA_SAL:,.0f} kg de acero menos.".replace(",", "."))
R["salon_sistema"] = dict(tipo="vigueta", forjado="(25+5)x71", vigueta=t, bovedilla="poliestireno", peso=gf, canto=0.30, reaccion_kN_m=rv["R"], area=AREA_SAL, kg_evitados=kg_m2 * AREA_SAL)

# 2) forjados de la casa y de la cubierta: vigueta pretensada y bovedilla (17+5)x71, apoyada en las vigas HEB (luz máx. 2,55 m)
FICHA2 = {"T-1": (17.47, 21.60, 6.21), "T-2": (24.99, 24.64, 6.36)}
def vig_casa(G, Q, L=max(BAYS), tipo="T-1"):
    qd = GG * G + GQ * Q; Mu, Vu, EI = FICHA2[tipo]
    M, V = qd * L**2 / 8, qd * L / 2
    d = (5 * G * 1e-3 * L**4 / (384 * EI) * 3 + 5 * Q * 1e-3 * L**4 / (384 * EI)) * 1e3
    return dict(G=G, qd=qd, rM=M / Mu, rV=V / Vu, d=d, lim=L / 300 * 1e3)
rc, rq = vig_casa(G_HOUSE, Q_HOUSE), vig_casa(G_CUB, Q_CUB)
P("\n## Forjados de la casa y de la cubierta: vigueta pretensada y bovedilla (luz máx. 2,55 m)\n")
P("Forjado (17+5)×71 con bovedilla de poliestireno, 2,02 kN/m² ([ficha Prearcon T-18](https://prearcon.com/pdf/VIGUETA%20T18.pdf)); vigueta T-1: Mu = 17,5 kN·m/m, Vu = 21,6 kN/m, EI fisurada = 6,21 MN·m²/m. Las viguetas apoyan en el ala inferior de las vigas HEB y el hormigón las cubre, así que las vigas no se ven por debajo.\n")
P("| Forjado | G total | M/Mu | V/Vu | Flecha con fluencia / límite (mm) |\n|---|---|---|---|---|")
P(f"| Casa (planta alta) | {rc['G']:.2f} | {rc['rM']:.2f} | {rc['rV']:.2f} | {rc['d']:.1f} / {rc['lim']:.1f} |")
P(f"| Cubierta plana (piedra y paneles solares) | {rq['G']:.2f} | {rq['rM']:.2f} | {rq['rV']:.2f} | {rq['d']:.1f} / {rq['lim']:.1f} |")
R["casa_sistema"] = dict(tipo="vigueta", forjado="(17+5)x71", vigueta="T-1", bovedilla="poliestireno", peso=G_VIG, sep=0.71)

# 3) vigas N-S nivel 1: una sola pieza continua sobre el pilar central (dos vanos)
vig = next(r for r in (check_cont(n, SPAN_NS[0], SPAN_NS[1], max(TRIB), G_HOUSE, Q_HOUSE) for n in HEB) if r["ok"])
P(f"\n## Vigas N-S del forjado (líneas x = 3,10; 5,30 y 7,20; una pieza continua de dos vanos {SPAN_NS[0]:.2f} + {SPAN_NS[1]:.2f} m; ancho tributario {max(TRIB):.2f} m)\n")
P(f"Sección: **{vig['name']}**. M/Mrd = {vig['rM']:.2f} en el apoyo central; V/Vrd = {vig['rV']:.2f}; flecha {vig['d_tot_mm']:.1f} mm (límite {vig['lim_tot_mm']:.1f}). Reacción en el pilar central ≈ {vig['RB']:.0f} kN. Al ser continua trabaja mejor que dos vigas sueltas y admite un perfil menor.")
R["viga_ns"] = dict(perfil=vig["name"])
R["lineas_x"] = LINES_X
Rn1 = vig["RB"]

# 4) vigas N-S de cubierta (la cubierta lleva el mismo forjado de vigueta y bovedilla)
vr = next(r for r in (check_cont(n, SPAN_NS[0], SPAN_NS[1], max(TRIB), G_CUB, Q_CUB) for n in HEB) if r["ok"])
P(f"\nVigas N-S de cubierta (continuas): **{vr['name']}** (M/Mrd {vr['rM']:.2f}, flecha {vr['d_tot_mm']:.1f}/{vr['lim_tot_mm']:.1f} mm).")
R["viga_cub"] = dict(perfil=vr["name"])
Rc = vr["RB"]

# 5) dintel de la cristalera (luz libre 3,60 + 2 x 0,20 de apoyo)
Ld = 4.1
g_muro = 0.55 * 0.71 * GAMMA_MURO + 0.30 * 1.0 * GAMMA_MURO      # muro sobre hueco hasta la terraza + antepecho
eq_G = 0.45 * G_TERRAZA; eq_Q = 0.45 * Q_TERRAZA
lint = None
for n in HEB:
    r = check_viga(n, Ld, 0.0, 0.0, 0.0, extra_line_G=g_muro + eq_G, extra_line_Q=eq_Q)
    if r["ok"]: lint = r; break
P(f"\n## Dintel sobre la cristalera (luz {Ld:.2f} m; muro y antepecho {g_muro:.1f} kN/m)\n")
P(f"Sección: **{lint['name']}** (M/Mrd {lint['rM']:.2f}, flecha {lint['d_tot_mm']:.1f}/{lint['lim_tot_mm']:.1f} mm). Se aloja en el espesor del muro con placas de apoyo de 0,20 m en cada extremo.")
R["dintel"] = dict(perfil=lint["name"], luz=Ld)

# 5b) viga que sustituye al muro de fachada existente (y = 7,60; luces de 2,2 m entre pilares; recibe franja de forjado y antepecho de terraza)
vf = None
for n in list(HEB)[1:]:                                  # mínimo constructivo HEB 120
    r = check_viga(n, max(BAYS[1], 2.30), 0.9, G_HOUSE, Q_HOUSE, extra_line_G=0.30 * 1.0 * GAMMA_MURO)
    if r["ok"]: vf = r; break
P(f"\n## Viga de fachada (sustituye al muro entre salón y casa, en cada planta; luz {max(BAYS[1], 2.30):.2f} m entre pilares)\n")
P(f"Sección: **{vf['name']}** (M/Mrd {vf['rM']:.2f}, flecha {vf['d_tot_mm']:.1f}/{vf['lim_tot_mm']:.1f} mm). Cada planta lleva su viga; los pilares HEB 120 en x = 3,10; 5,30 y 7,20 quedan vistos en el borde del salón.")
R["viga_fachada"] = dict(perfil=vf["name"])

# 5c) viga de borde del saliente del baño (x = 9,15; sustituye al muro de 0,55 entre casa y saliente; luz 3,70 m entre apoyos en muro)
trib_s = BAYS[3] / 2 + 2.775 / 2
sal_f = next(r for r in (check_viga(n, 3.70, trib_s, G_HOUSE, Q_HOUSE) for n in list(HEB)[1:]) if r["ok"])
sal_c = next(r for r in (check_viga(n, 3.70, trib_s, G_CUB, Q_CUB) for n in list(HEB)[1:]) if r["ok"])
sal_p = max([sal_f["name"], sal_c["name"]], key=lambda n: SECC[n][7])
P(f"\n## Viga de borde del saliente del baño (a x = 9,15, en forjado y en cubierta; luz {3.70:.2f} m entre muros)\n")
P(f"Falta ese muro entre la casa y el saliente, así que una viga recoge el borde de la casa y las viguetas del saliente. Sección: **{sal_p}** (forjado M/Mrd {sal_f['rM']:.2f}, cubierta {sal_c['rM']:.2f}).")
R["viga_saliente"] = dict(perfil=sal_p, luz=3.70)

# 5d) dinteles de huecos en muros de 0,55 m (hoja simple; muro 1 m sobre el hueco + reacción de viguetas)
din = {}
P("\n## Dinteles de puertas y ventanas en muros de mampostería\n| Hueco (m) | Luz de cálculo | Perfil | M/Mrd |\n|---|---|---|---|")
for wv in (1.0, 1.2, 1.4, 1.6):
    L = wv + 0.40
    r = next(r for r in (check_viga(n, L, 0.0, 0.0, 0.0, extra_line_G=0.55 * 1.0 * GAMMA_MURO + 4.8 * 1.3, extra_line_Q=2.0 * 1.3) for n in IPE) if r["ok"])
    din[str(wv)] = r["name"]; P(f"| ≤ {wv:.1f} | {L:.1f} | {r['name']} | {r['rM']:.2f} |")
R["dinteles"] = din

# 6) pilares
N_c2 = (Rn1 + Rc) + 1.35 * 33.7 * 9.81 / 1000 * 5.6          # pilar central (mayor carga: reacción de vigas continuas) + peso propio
N_c1 = 0.4 * (Rn1 + Rc) + 1.35 * 33.7 * 9.81 / 1000 * 5.6
pil = None
for n in list(HEB)[1:]:                                              # mínimo constructivo HEB 120
    r = pandeo_pilar(n, N_c2, 3.3)
    if r["ratio"] <= 0.85: pil = r; break
P(f"\n## Pilares HEB (6 uds., x = 3,10; 5,30 y 7,20; y = 7,60 y 11,80; ocultos en muros y tabiques; altura ≈ 5,6 m)\n")
P(f"Carga axial de cálculo máx. ≈ {N_c2:.0f} kN (pilar central) y ≈ {N_c1:.0f} kN (pilar sur). Sección: **{pil['name']}**, N/Nb,Rd = {pil['ratio']:.2f} (pandeo eje débil, Lcr = 3,3 m).")
R["pilar"] = dict(perfil=pil["name"], N_central=N_c2, N_sur=N_c1)
SIG = 150.0                                                          # kPa admisible supuesta (falta estudio geotécnico)
zap = math.ceil(math.sqrt(N_c2 / 1.35 * 1.05 / SIG) * 10) / 10 + 0.2
P(f"\nZapatas aisladas bajo pilares (σ adm. supuesta 150 kPa, **pendiente de estudio geotécnico**): ≈ {zap:.1f} × {zap:.1f} m, canto 0,60 m.")
R["zapata"] = dict(lado=zap, canto=0.60, sigma=SIG)

# 7) apoyos en muros existentes
qw_house = (GG * G_HOUSE + GQ * Q_HOUSE) * BAYS[0] / 2 + (GG * G_CUB + GQ * Q_CUB) * BAYS[0] / 2
peso_muro = 0.55 * 5.6 * GAMMA_MURO * GG
sigma = (qw_house + peso_muro) / 0.55 / 1000
P(f"\n## Apoyo en los muros de mampostería (50-60 cm)\n")
P(f"Carga lineal en cabeza de muro de la casa ≈ {qw_house:.0f} kN/m + peso propio ≈ {peso_muro:.0f} kN/m → tensión en base ≈ {sigma:.2f} MPa (referencia orientativa 0,3-0,5 MPa: **hay que ensayar la mampostería**).")
P("Las viguetas apoyan en placas de reparto sobre un zuncho perimetral que ata los muros y hace de diafragma. Recomendación para abaratar: zuncho de hormigón armado (hecho a la vez que el forjado) en lugar de perfil UPN de acero.")
R["muro"] = dict(sigma_MPa=sigma)
P("\n## Pendiente de confirmar por un técnico\n- Sismo (NCSE-02, zona sísmica de Almería) y arriostramiento de los muros de mampostería.\n- Estudio geotécnico y zapatas definitivas; estado real de los muros (grietas, humedad, calidad de la piedra).\n- Uniones, anclajes, protección contra fuego (R60 en vivienda de 2 plantas según CTE DB-SI) y comprobación de pandeo lateral.\n- Cálculo de la chapa colaborante, del anclaje de los paneles solares al viento y de la impermeabilización con los fabricantes.\n- Este documento no sustituye al proyecto de estructura visado.")
open("memoria_estructura.md", "w").write("\n".join(out)); json.dump(R, open("estructura.json", "w"), indent=1)
print("\n".join(out)); print(json.dumps(R, indent=1))
