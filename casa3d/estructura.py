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
G_HOUSE, G_TERRAZA = G_FORJ + G_PAV + G_TAB, G_FORJ + G_TERR
G_CUB = G_FORJ + 2.2 + 1.0 + 0.3
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
sal = elegir(L_SAL, G_TERRAZA, Q_TERRAZA, IPE, [0.9, 1.0])
P("## Terraza sobre el salón: viguetas E-O (luz 5,75 m)\n| Sección | Separación (m) | kg/m² | M/Mrd | Flecha total / límite (mm) |\n|---|---|---|---|---|")
for kgm2, s, r in sal[:4]: P(f"| {r['name']} | {s:.1f} | {kgm2:.1f} | {r['rM']:.2f} | {r['d_tot_mm']:.1f} / {r['lim_tot_mm']:.1f} |")
R["salon_vigueta"] = dict(perfil=sal[0][2]["name"], sep=sal[0][1], luz=L_SAL)

# 2) viguetas casa (luz máxima de bahía = 3,0)
casa = elegir(max(BAYS), G_HOUSE, Q_HOUSE, IPE, [0.9, 1.0])
P("\n## Planta alta de la casa: viguetas E-O (luz máx. 2,55 m)\n| Sección | Separación (m) | kg/m² | M/Mrd | Flecha total / límite (mm) |\n|---|---|---|---|---|")
for kgm2, s, r in casa[:4]: P(f"| {r['name']} | {s:.1f} | {kgm2:.1f} | {r['rM']:.2f} | {r['d_tot_mm']:.1f} / {r['lim_tot_mm']:.1f} |")
R["casa_vigueta"] = dict(perfil=casa[0][2]["name"], sep=casa[0][1], luz=max(BAYS))

# 3) vigas N-S nivel 1 (dos vanos, se comprueba el mayor como biapoyado)
vig = None
for n in HEB:
    rs = [check_viga(n, L, t, G_HOUSE, Q_HOUSE) for L, t in [(SPAN_NS[0], max(TRIB))]]
    if all(r["ok"] for r in rs): vig = rs[0]; break
P(f"\n## Vigas N-S del forjado (líneas x = 3,10; 5,30 y 7,20; vano {SPAN_NS[0]:.2f} m, ancho tributario {max(TRIB):.2f} m)\n")
P(f"Sección: **{vig['name']}**. M/Mrd = {vig['rM']:.2f}; V/Vrd = {vig['rV']:.2f}; flecha {vig['d_tot_mm']:.1f} mm (límite {vig['lim_tot_mm']:.1f}). Reacción máx. por apoyo ≈ {vig['R']:.0f} kN.")
R["viga_ns"] = dict(perfil=vig["name"])
R["lineas_x"] = LINES_X
Rn1 = vig["R"] + check_viga(vig["name"], SPAN_NS[1], max(TRIB), G_HOUSE, Q_HOUSE)["R"]   # reacción en pilar central (suma de ambos vanos)

# 4) cubierta plana no transitable (piedra + paneles solares): misma rejilla que el forjado
cub = elegir(max(BAYS), G_CUB, Q_CUB, IPE, [0.9, 1.0])
P("\n## Cubierta plana (piedra y paneles solares): viguetas E-O (luz 2,55 m)\n| Sección | Separación (m) | kg/m² | M/Mrd | Flecha total / límite (mm) |\n|---|---|---|---|---|")
for kgm2, s_, r in cub[:4]: P(f"| {r['name']} | {s_:.1f} | {kgm2:.1f} | {r['rM']:.2f} | {r['d_tot_mm']:.1f} / {r['lim_tot_mm']:.1f} |")
R["cubierta_vigueta"] = dict(perfil=cub[0][2]["name"], sep=cub[0][1], luz=max(BAYS))
vr = None
for n in HEB:
    r = check_viga(n, SPAN_NS[0], max(TRIB), G_CUB, Q_CUB)
    if r["ok"]: vr = r; break
P(f"\nVigas N-S de cubierta: **{vr['name']}** (M/Mrd {vr['rM']:.2f}, flecha {vr['d_tot_mm']:.1f}/{vr['lim_tot_mm']:.1f} mm).")
R["viga_cub"] = dict(perfil=vr["name"])
Rc = vr["R"] * (SPAN_NS[0] + SPAN_NS[1]) / SPAN_NS[0]

# 5) dintel de la cristalera (luz libre 3,60 + 2 x 0,20 de apoyo)
Ld = 4.0
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

# 6) pilares
N_c2 = 1.05 * (Rn1 + Rc) + 1.35 * 33.7 * 9.81 / 1000 * 5.6          # pilar central (mayor carga) + peso propio
N_c1 = 1.05 * (Rn1 / 2 + Rc / 2) + 1.35 * 33.7 * 9.81 / 1000 * 5.6
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
P("Las viguetas apoyan en placas de reparto sobre un zuncho perimetral (perfil UPN 160 o zuncho de hormigón) que ata los muros y hace de diafragma.")
R["muro"] = dict(sigma_MPa=sigma)
P("\n## Pendiente de confirmar por un técnico\n- Sismo (NCSE-02, zona sísmica de Almería) y arriostramiento de los muros de mampostería.\n- Estudio geotécnico y zapatas definitivas; estado real de los muros (grietas, humedad, calidad de la piedra).\n- Uniones, anclajes, protección contra fuego (R60 en vivienda de 2 plantas según CTE DB-SI) y comprobación de pandeo lateral.\n- Cálculo de la chapa colaborante, del anclaje de los paneles solares al viento y de la impermeabilización con los fabricantes.\n- Este documento no sustituye al proyecto de estructura visado.")
open("memoria_estructura.md", "w").write("\n".join(out)); json.dump(R, open("estructura.json", "w"), indent=1)
print("\n".join(out)); print(json.dumps(R, indent=1))
