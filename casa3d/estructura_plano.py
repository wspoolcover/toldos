"""Planos de estructura (forjado y cubierta) y vista 3D solo del acero, a partir de casa_v3.STEEL."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MPoly, Rectangle
import casa_v3 as h
from perfiles import SECC

COLOR = {"IPE 100": "#7fbf7f", "IPE 120": "#2e9d5f", "IPE 240": "#0b6e4f", "HEB 120": "#e0952b", "HEB 140": "#d9601e", "HEB 160": "#b02a1a"}
VIGAS = {"forjado": ["viguetas_salon", "viguetas_casa", "vigas_forjado", "dinteles", "dintel"], "cubierta": ["viguetas_cubierta", "vigas_cubierta"]}


def panel(ax, nivel, titulo):
    ax.add_patch(MPoly(h.PTS if nivel == "forjado" else h.NB_PA, closed=True, fc="#f3f0ea", ec="#222", lw=1.4, zorder=1))
    x0, y0, x1, y1 = h.VOID; ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fc="none", ec="#555", hatch="//", lw=.8, zorder=2))
    ax.text((x0 + x1) / 2, (y0 + y1) / 2, "hueco\nescalera", ha="center", va="center", fontsize=6.5, color="#555")
    for lx, cy, sec in h.STEEL["pilares"]:
        z = h.ZAP / 2; ax.add_patch(Rectangle((lx - z, cy - z), 2 * z, 2 * z, fc="none", ec="#999", ls="--", lw=.7, zorder=2))
    for cat in VIGAS[nivel]:
        for g in h.STEEL[cat]:
            xa, ya, xb, yb, sec = g
            heavy = SECC[sec][1] >= 100 or cat in ("vigas_forjado", "vigas_cubierta")
            lw = 4.2 if cat in ("vigas_forjado", "vigas_cubierta") else (2.6 if cat == "dintel" else (1.4 if cat == "dinteles" else 1.6))
            ax.plot([xa, xb], [ya, yb], color=COLOR.get(sec, "#333"), lw=lw, solid_capstyle="butt", zorder=4 if heavy else 3)
    for lx, cy, sec in h.STEEL["pilares"]:
        a = SECC[sec][0] / 2000; ax.add_patch(Rectangle((lx - 0.12, cy - 0.12), 0.24, 0.24, fc=COLOR[sec], ec="#000", lw=.9, zorder=6))
    ex = h.E; s_h = ex["casa_vigueta"]
    if nivel == "forjado":
        ax.text(6.2, 3.7, f"{ex['salon_vigueta']['perfil']} cada {ex['salon_vigueta']['sep']:.1f} m\n(terraza sobre el salón, luz 5,75 m)", ha="center", fontsize=8, color=COLOR[ex['salon_vigueta']['perfil']], weight="bold")
        ax.text(4.5, 0.9 if False else 8.0, "", fontsize=6)
        ax.text(4.9, 7.72, f"viga de fachada {ex['viga_fachada']['perfil']}", fontsize=6.5, color=COLOR[ex['viga_fachada']['perfil']], ha="center", va="top")
        ax.text(5.5, 1.45, f"dintel {ex['dintel']['perfil']} sobre la cristalera", fontsize=6.5, color=COLOR[ex['dintel']['perfil']], ha="center")
    ax.text(1.9, 13.5, f"{s_h['perfil']} cada {s_h['sep']:.1f} m", fontsize=7.5, rotation=90, color=COLOR[s_h['perfil']], weight="bold", ha="center")
    for lx in h.LINES_X: ax.text(lx, h.Y_TOP + 0.25, ex["viga_ns" if nivel == "forjado" else "viga_cub"]["perfil"], fontsize=7, rotation=90, ha="center", va="bottom", color=COLOR[ex["viga_ns" if nivel == "forjado" else "viga_cub"]["perfil"]])
    ax.text(10.75, 12.5, f"borde saliente\n{ex['viga_saliente']['perfil']}", fontsize=6.5, ha="center", color=COLOR[ex['viga_saliente']['perfil']])
    ax.set_xlim(-0.6, 12.6); ax.set_ylim(-0.8, 18.6); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(titulo, fontsize=10, weight="bold")


if __name__ == "__main__":
    fig = plt.figure(figsize=(13, 9.8)); fig.suptitle("Estructura de acero: vigas y viguetas (S275JR)", fontsize=14, weight="bold", x=0.02, ha="left")
    a1 = fig.add_axes([0.02, 0.17, 0.47, 0.75]); a2 = fig.add_axes([0.51, 0.17, 0.47, 0.75])
    panel(a1, "forjado", "FORJADO SOBRE PLANTA BAJA Y TERRAZA (cota +3,26)"); panel(a2, "cubierta", "CUBIERTA PLANA (cota +5,96)")
    filas = sorted(h.KG.items(), key=lambda kv: -kv[1])
    xx = 0.02
    for k, v in filas:
        t = f"■ {k}: {v:,.0f} kg".replace(",", "."); fig.text(xx, 0.11, t, fontsize=9, va="top", color=COLOR.get(k, "#333"), weight="bold"); xx += 0.017 * len(t) * 0.62
    for i, (k, v) in enumerate(filas): pass
    fig.text(0.02, 0.075, f"Acero total del modelo: {h.KGTOT:,.0f} kg sin uniones ni placas.  Línea gruesa = vigas (una pieza continua de 8 m por línea) · línea fina = viguetas · cuadrados = pilares HEB 120 · trazos = zapatas.".replace(",", "."), fontsize=8.5, va="top")
    fig.text(0.02, 0.045, "Borrador: el cálculo definitivo y las uniones los define un técnico competente.", fontsize=8, va="top", color="#a33")
    fig.savefig("estructura_planos.png", dpi=110)
    print("ok")
