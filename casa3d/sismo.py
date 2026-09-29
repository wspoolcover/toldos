"""Comprobación sísmica ORIENTATIVA y resumen de acero; se añade a memoria_estructura.md (ejecutar después de estructura.py)."""
import json
import casa_v3 as h
from shapely.geometry import Polygon

v = lambda n: dict((a, b) for a, b, _ in h.partes)[n].val().Volume()
E = h.E
muros = (v("muros_PB") + v("muros_PA") + v("parapeto_terraza") + v("parapeto_cubierta")) * 20 + (v("tabiques_PB") + v("tabiques_PA")) * 8
a_forj = Polygon(h.PTS).area; a_cub = Polygon(h.NB_PA).area
pesos = dict(muros=muros, forjados=a_forj * 4.9, cubierta=a_cub * 6.1, cuasi_permanente=0.3 * 2.0 * a_forj + 0.3 * 1.0 * a_cub, acero=h.KGTOT * 9.81 / 1000)
W = sum(pesos.values())
AB = 0.16     # ab/g supuesto: Almería capital tiene 0,14 (NCSE-02); Albox está en zona igual o superior. Consultar Anexo 1
c_lo, c_hi = 0.20, 0.25
V_lo, V_hi = c_lo * W, c_hi * W
# longitud de muro de mampostería que resiste en cada dirección (sin huecos grandes)
L_ew = 9.55 + 2.87 + 3.45 + 9.55 * 0 + 3.15 * 0      # muro del fondo (y=16,30), tramo oeste de la línea y=7,32 y tramo hasta x=3,45
L_ns = 16.30 + 12.05 * 0 + 8.30 + 8.98 + (16.30 - 11.80) + 7.32       # muros este y oeste
tau_ew, tau_ns = V_hi / (L_ew * 0.55) / 1000, V_hi / (L_ns * 0.55) / 1000
txt = f"""

## Sismo: comprobación orientativa (Albox está en zona sísmica)
Peso sísmico del edificio ≈ **{W:.0f} kN** (muros {pesos['muros']:.0f}, forjados {pesos['forjados']:.0f}, cubierta {pesos['cubierta']:.0f}, sobrecarga casi permanente {pesos['cuasi_permanente']:.0f}, acero {pesos['acero']:.0f}).
Aceleración básica supuesta ab = {AB:.2f} g (Almería capital: 0,14 g según la [tabla de municipios de NCSE-02](https://normatia.com/es/recursos/emplazamiento/zona-sismica/); Albox no aparece en esa tabla: hay que mirar el Anexo 1 de la norma).
Con un coeficiente sísmico de {c_lo:.2f}-{c_hi:.2f} (suposición conservadora para mampostería) el cortante en la base sería ≈ **{V_lo:.0f}-{V_hi:.0f} kN**.
- **Dirección N-S:** muros existentes de unos {L_ns:.0f} m × 0,55 m → tensión tangencial ≈ {tau_ns:.2f} MPa.
- **Dirección E-O:** solo resisten el muro del fondo y los tramos del oeste (unos {L_ew:.0f} m), porque el salón tiene la fachada acristalada y la línea de la viga de fachada no es muro → tensión ≈ {tau_ew:.2f} MPa.
Referencia de resistencia a cortante de mampostería antigua en buen estado: unos 0,05-0,15 MPa (hay que ensayarla).
**Conclusión:** en la dirección E-O el margen es justo. Antes de construir un técnico debe hacer el cálculo sísmico y definir el refuerzo: por ejemplo cruces de acero en dos paños de la línea de fachada, pantallas de hormigón armado de 15-20 cm en los tabiques de la suite o mallazo con mortero en las caras de los muros. Ya está previsto: zunchos de hormigón en cada nivel, riostras de cimentación entre zapatas y forjados que hacen de diafragma.
"""
kg = ", ".join(f"{k}: {x:.0f} kg" for k, x in sorted(h.KG.items(), key=lambda t: -t[1]))
txt += f"\n\n## Acero del modelo 3D (sin uniones ni placas)\nTotal ≈ {h.KGTOT:.0f} kg ({kg}). Ver `abaratar.md`.\n"
open("memoria_estructura.md", "a").write(txt)
json.dump(dict(W=W, V_lo=V_lo, V_hi=V_hi, tau_ew=tau_ew, tau_ns=tau_ns, kg=h.KGTOT), open("sismo.json", "w"))
print(round(W), round(V_lo), round(V_hi), round(tau_ns, 3), round(tau_ew, 3), round(h.KGTOT))
