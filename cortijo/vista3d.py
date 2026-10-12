"""Vista isométrica del modelo v4 desde el GLB (con y sin la planta alta)."""
import sys, numpy as np, trimesh, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
sc = trimesh.load("casa_v4.glb")
def render(skip, out, elev=38, azim=-62, title=""):
    fig = plt.figure(figsize=(11, 8)); ax = fig.add_subplot(111, projection="3d"); allv = []
    for name, g in sc.geometry.items():
        if any(name.startswith(s) or s in name for s in skip): continue
        m = g.copy(); f = m.faces; v = m.vertices; allv.append(v)
        n = m.face_normals; light = np.clip(0.55 + 0.45 * (n @ np.array([-.4, -.6, .7])), .25, 1)
        mc = np.array(m.visual.material.main_color[:3] if hasattr(m.visual, "material") else [200, 190, 170]) / 255
        col = np.tile(mc, (len(f), 1))
        fc = np.c_[col * light[:, None], np.full(len(f), .35 if "cristal" in name else 1)]
        ax.add_collection3d(Poly3DCollection(v[f], facecolors=fc, edgecolors="none"))
    a = np.vstack(allv); mn, mx = a.min(0), a.max(0); c = (mn + mx) / 2; r = (mx - mn).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(0, 2 * r); ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev, azim); ax.axis("off"); ax.set_title(title); fig.savefig(out, dpi=110, bbox_inches="tight"); plt.close(fig)
render([], "cortijo_3d.png", title="Cortijo — vista exterior (v4)")
render(["muros_PA", "forjado_PB_PA", "forjado_salon", "parapeto_terraza", "forjado_cubierta", "parapeto", "lucernario", "tabiques_PA", "cristal_PA", "acero_vigas_cubierta"], "cortijo_3d_PB.png", elev=62, azim=-70, title="Planta baja sin planta alta (v4)")
