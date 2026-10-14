"""Versión económica y rápida de la opción C2: tabla de partidas (completa frente a económica), totales, gráfico y docs/17_version_economica.md.
Todas las cifras son estimaciones mías en miles de euros, IVA no incluido, a partir de docs/08 y de los precios que se citan en docs/02 y docs/15; no son un presupuesto.
Uso: python economica.py  ->  docs/17_version_economica.md, version_economica_costes.png"""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# (grupo, (mín, máx) completa, (mín, máx) económica, qué cambia en la económica)
P = [
    ("Demolición y apeos", (6, 10), (6, 10), "Igual: elemento a elemento, con apeos."),
    ("Cimentación y drenaje", (7, 11), (7, 11), "Igual. No se recorta: zapatas, riostras, zunchos, drenaje y geotextil."),
    ("Estructura de acero", (11, 20), (9, 15), "Perfiles en bruto de tu proveedor, cortados a la lista del Excel, y atornillados en obra. Dinteles de los muros nuevos con bloque en U en lugar de perfil."),
    ("Forjados y zunchos", (11, 17), (10, 15), "Vigueta y bovedilla en todo (sin placas alveolares ni grúa). Zunchos con bloque en U, sin madera de encofrado."),
    ("Muros nuevos del salón y pilares de atado", (3, 5), (3, 5), "Igual (material; mano de obra tuya)."),
    ("Cubierta plana", (9, 14), (7, 11), "Impermeabilización y aislamiento iguales; grava de lastre en vez de sedum."),
    ("Aislamiento transpirable de fachadas", (11, 17), (9, 14), "Lana mineral de 6 cm en vez de 8 sobre mortero de cal, solo en fachadas libres. Nunca poliestireno pegado sobre el tapial."),
    ("Carpintería: ventanas y salida de la cocina", (8, 14), (5.9, 9.8), "PVC de medidas estándar a precio de coste; salida de la cocina en PVC de 2 hojas de 1,40 m en vez de corredera de aluminio de 1,60 m."),
    ("Seguridad: muros, puertas, rejas y asientos", (8.2, 16.1), (5.6, 10.8), "Misma seguridad en la suite: bloque relleno de 20 cm, 2 puertas RC3 de serie y rejas de hierro sencillas de tu proveedor; vidrio laminado solo en la suite; asientos de obra sin cajones."),
    ("Tabiquería e interiores", (5, 8), (4.5, 7), "Placa de yeso con lana en los tabiques que no son de seguridad; puertas lisas de serie."),
    ("Climatización, agua caliente y solera", (20.5, 31.5), (14.8, 21.8), "Multisplit en las dos plantas, chimenea y aerotermia solo para el agua caliente, en vez de aerotermia con suelo radiante. Solera sin tubo."),
    ("Fotovoltaica", (7, 10), (4, 6), "8 a 10 paneles ahora, con la canalización dejada para ampliar."),
    ("Electricidad y red", (7, 11), (6, 9), "Mecanismos de gama media-baja y precableado de alarma."),
    ("Fontanería y saneamiento", (5, 8), (5, 7.5), "Igual en lo esencial (la cocina central lleva su bajante)."),
    ("Cocina", (3.5, 6), (2.5, 4.5), "Mueble básico y encimera laminada o de compacto."),
    ("Baños, vestidor y armarios", (9, 14), (6.5, 10), "Gama básica, ducha de obra, armarios empotrados en placa."),
    ("Solados, pintura, falsos techos y escalera", (14, 22), (10, 16), "Porcelánico efecto barro estándar; pintura y encalado tuyos; escalera de acero con peldaños de madera."),
    ("Honorarios", (9, 15), (8, 13), "Reutilizando el proyecto de legalización; el geotécnico y el ingeniero no se recortan."),
]
TC = (sum(p[1][0] for p in P), sum(p[1][1] for p in P)); TE = (sum(p[2][0] for p in P), sum(p[2][1] for p in P))
f = lambda x: (f"{x:.1f}".rstrip("0").rstrip(".") if x != int(x) else str(int(x))).replace(".", ",")
rg = lambda t: f"{f(t[0])}–{f(t[1])}"
rt = lambda t: f"{round(t[0])}–{round(t[1])}"                         # totales redondeados


def grafico(ruta="version_economica_costes.png"):
    AZ, NA, INK, MUT = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e"
    n = len(P); fig, ax = plt.subplots(figsize=(9.2, 8.6)); h = 0.34
    for i, (g, c, e, _) in enumerate(P):
        y = n - 1 - i
        ax.barh(y + h / 2 + .02, sum(c) / 2, height=h, color=AZ, zorder=3); ax.barh(y - h / 2 - .02, sum(e) / 2, height=h, color=NA, zorder=3)
        ax.text(sum(c) / 2 + .5, y + h / 2 + .02, rg(c), va="center", fontsize=7.2, color=MUT); ax.text(sum(e) / 2 + .5, y - h / 2 - .02, rg(e), va="center", fontsize=7.2, color=MUT)
    ax.set_yticks(range(n)); ax.set_yticklabels([p[0] for p in P][::-1], fontsize=8, color=INK)
    ax.set_xlim(0, 30); ax.set_xlabel("miles de euros (la barra marca el punto medio del rango; el rango va escrito)", fontsize=8, color=MUT)
    ax.tick_params(axis="x", labelsize=8, colors=MUT); ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#e4e2dc", lw=.6, zorder=0); [ax.spines[s].set_visible(False) for s in ("top", "right", "left")]; ax.spines["bottom"].set_color("#c9c6bd")
    ax.set_title("Coste orientativo por grupo de partidas (IVA no incluido)", fontsize=11, weight="bold", loc="left", color=INK, pad=26)
    ax.add_patch(plt.Rectangle((0, n + .15), .9, .35, color=AZ, clip_on=False)); ax.text(1.3, n + .32, f"Versión completa (C2): {rt(TC)} mil €", fontsize=8.5, va="center", color=INK, clip_on=False)
    ax.add_patch(plt.Rectangle((15, n + .15), .9, .35, color=NA, clip_on=False)); ax.text(16.3, n + .32, f"Versión económica: {rt(TE)} mil €", fontsize=8.5, va="center", color=INK, clip_on=False)
    fig.tight_layout(); fig.savefig(ruta, dpi=int(os.environ.get("DPI", 150))); plt.close(fig)


def tabla():
    t = ["| Partida | Qué cambia en la económica | Completa (mil €) | Económica (mil €) |", "|---|---|---|---|"]
    t += [f"| {g} | {nota} | {rg(c)} | {rg(e)} |" for g, c, e, nota in P]
    t.append(f"| **Total** | | **{rt(TC)}** | **{rt(TE)}** |")
    return "\n".join(t)


def doc():
    a, b = TC[0] - TE[0], TC[1] - TE[1]
    return f"""# Versión económica y rápida (14-10-2026)

Es la misma casa de la opción C2 (cocina central y despacho girado), con las decisiones que bajan el coste y el plazo **sin tocar la cimentación, la estructura, el aislamiento, la impermeabilización ni la seguridad de la suite**. Todas las cifras son estimaciones mías en miles de euros, sin IVA, y salen de `08_presupuesto_y_ahorro.md` y de los precios citados en `02_instalaciones.md` y `15_propuestas_planta_baja.md`. **No es un presupuesto**: sirve para ordenar decisiones y pedir ofertas comparables.

## 1. Reglas
- **No se recorta**: cimentación y drenaje, estructura y apeos, impermeabilización de la cubierta, aislamiento transpirable de las fachadas, instalación eléctrica y de agua, ventilación de baños y cocina, y la seguridad de la suite.
- **Se simplifica**: acabados, climatización, tamaño y número de elementos especiales, y se hace por fases.
- **Se usan sistemas rápidos**: bloque de hormigón en U para zunchos y dinteles (sin madera de encofrado), tabique de placa de yeso donde no hace falta seguridad, ventanas y puertas de medidas estándar pedidas al principio, multisplit en lugar de suelo radiante (no hay que esperar al curado del mortero).

## 2. Qué cambia y cuánto cuesta
{tabla()}

**Ahorro estimado: {rt((a, b))} mil € (≈ {round(100 * (a + b) / (TC[0] + TC[1]))} %)**. La versión completa ya incluye lo que has pedido hoy (muros y puertas de seguridad, salida de aluminio y asientos en las ventanas), por eso supera el rango de `08_presupuesto_y_ahorro.md` (140–225 mil €). Con mano de obra propia en muros, pintura y montaje de ventanas se puede bajar entre 15 y 30 mil € más en cualquiera de las dos. El rango es amplio porque faltan el geotécnico, las catas del tapial y las ofertas. Gráfico: `version_economica_costes.png`.

## 3. Paquete de seguridad económico
Se mantiene lo que más protege y se evita lo que solo cambia el acabado.
1. **Paredes de la suite**: bloque de hormigón de 20 cm relleno de hormigón y armado, en el vestidor (hacia la sala), en el lado norte y en el lado este del dormitorio. Unos 32 m² de muro. El ladrillo hueco no vale: se taladra.
2. **Dos puertas de seguridad RC3** (vestidor y dormitorio), de acero y de serie, con el marco anclado al muro y cilindro con protección antitaladro. Lo que importa es el anclaje: una puerta bien certificada y mal anclada rinde mucho menos ([Selectra](https://selectra.es/alarmas/medidas-seguridad/puerta-blindada-o-acorazada)).
3. **Rejas de hierro sencillas** en las ventanas de la planta baja, de tu proveedor de hierro: son típicas del cortijo, baratas y seguras. Contraventanas de madera o PVC por fuera.
4. **Vidrio laminado** (33.1) en las ventanas de la suite y 44.2 en la cristalera del salón, con cierre multipunto.
5. **Acceso**: puerta corredera de 7 m motorizada con cancela peatonal, luz exterior y videoportero.
6. **Precableado de alarma y cámaras** (tubos vacíos), por poco dinero ahora y mucho más caro después.
7. **Planta alta**: puertas macizas con cerradura de seguridad y paredes normales (no RC3). Si quieres más, se amplía después.

## 4. El plano
`modelo_C2E_planta_baja.png`: igual que el C2 con una sola despensa-lavadero de 5,9 m² y una puerta, salida de la cocina en PVC de 1,40 m y rejas en las ventanas de la planta baja. La planta alta es la de la v8 sin cambios.

## 5. Plazos y fases
Las duraciones son orientativas y las tiene que confirmar el constructor.
- **Fase 1, casa habitable (planta baja y estructura completa)**: demolición y apeos, cimentación, estructura de acero, forjados y cubierta, cerramientos y muros de seguridad, carpintería, instalaciones y acabados de la planta baja. Unos 6 a 8 meses.
- **Fase 2, planta alta**: tabiques, instalaciones, acabados y splits. Unos 2 a 3 meses, con la casa ya habitada abajo.
- **Fase 3, extras**: pérgola del patio sur, ampliar los paneles solares, aerotermia y suelo radiante si se quiere, y batería. Cuando convenga.
- **Lo que acorta el plazo**: pedir al principio ventanas y puertas de medidas estándar (tardan semanas), usar bloque en U sin encofrado, tabique seco y splits, que se montan al final sin esperar al mortero.

## 6. Lo que queda preparado para ampliar
- **Suelo radiante**: dejar 7 cm de altura libre en la planta baja para poder añadirlo más adelante (con los niveles de puertas y escalera ya resueltos).
- **Fotovoltaica**: canalización y espacio en la cubierta para los 16 paneles del diseño completo.
- **Pérgola y patio sur**: preparar el solado y la toma eléctrica.
- **Batería**: espacio y protecciones en el cuadro.

## 7. Compra por tu canal
Ventanas y puertas de PVC (≈ 37 m² y 13 puertas), el hierro en bruto (≈ 4,5 t) y las rejas, a precio de coste. El Excel `pedido_proveedores.xlsx` tiene las mediciones listas y la columna amarilla para tus precios. Pide al taller la lista de corte y el galvanizado de la escalera y las barandillas.

## 8. Qué podría subir el coste
Geotécnico y cimentación existente (el terreno parece arcilla agrietada), el estado de los muros de tapial al abrir huecos, los apeos, los vecinos pegados a ambos lados y la grúa si se acabara usando placa alveolar. Por eso no se recorta nada de lo estructural.
"""


if __name__ == "__main__":
    grafico(); open("docs/17_version_economica.md", "w", encoding="utf-8").write(doc())
    print("completa", rt(TC), "económica", rt(TE), "ahorro", rt((TC[0] - TE[0], TC[1] - TE[1])))
