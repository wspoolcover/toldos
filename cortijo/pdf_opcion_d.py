"""PDF de la opción D (suite a la izquierda, cocina en medio y dormitorio pequeño a la derecha con el armario bajo la escalera): pdf/Opcion_D_suite_cocina_dormitorio.pdf. Uso: python pdf_opcion_d.py"""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import generar_pdf as g
from generar_pdf import EST, FECHA, AVISO, figura, tabla, construir, Paragraph, Spacer, PageBreak, A4, mm, inline
import modelos_pb as mp

fig, ax = plt.subplots(figsize=(7.2, 9.4)); tot = mp.dibujar(ax, mp.MODELO_D); fig.tight_layout(); fig.savefig("modelo_D_planta_baja.png", dpi=int(os.environ.get("DPI", 200))); plt.close(fig)
W, H = A4; wp = W - 36 * mm; hp = H - 40 * mm
f1 = lambda x: f"{x:.1f}".replace(".", ",")
def li(t): return Paragraph(inline(t), g.ParagraphStyle("li", parent=EST["li"], leftIndent=13, bulletIndent=2), bulletText="•")

nombres = ("Salón con comedor", "Pasillo de entrada", "Entrada", "Escalera", "Sala de estar", "Despacho", "Cocina", "Dormitorio 2", "Dormitorio principal", "Vestidor", "Baño", "Baño grande")
mitad = (len(nombres) + 1) // 2
filas = ["| Estancia | m² | Estancia | m² |", "|---|---|---|---|"] + [f"| {nombres[i]} | {f1(tot[nombres[i]])} | " + (f"{nombres[i + mitad]} | {f1(tot[nombres[i + mitad]])} |" if i + mitad < len(nombres) else " |  |") for i in range(mitad)]
armario = ["| Parte del armario | Medidas | Altura libre |", "|---|---|---|",
           "| Bajo la meseta de la escalera | 0,88 × 1,75 m, al fondo del hueco | 1,51 m (la meseta está a 1,73 m y su losa es de 22 cm) |",
           "| Bajo el tramo de vuelta | 0,88 m de ancho, hasta 1,44 m de fondo | De 1,5 m junto a la meseta a 2,1 m en el extremo norte |",
           "| Total | ≈ 2,0 m², en L | Prendas largas solo en la parte norte; en el resto, estantes, cajones y ropa doblada |",
           "| Acceso | Desde el dormitorio 2, por el tabique sur de la escalera, 1,50 m de hueco | Puertas correderas, sin espacio de giro |"]
vs = ["| | Opción C2 | Opción D |", "|---|---|---|",
      "| Dormitorios en la casa | 4 (suite y tres arriba) | 5 (suite, dormitorio 2 y tres arriba) |", "| Cocina | 13,4 m² con despensa y lavadero | 9,4 m², en medio, sin lavadero |",
      "| Armario | — | Incorporado bajo la escalera, abierto desde el dormitorio 2 |", "| Armario técnico | Bajo la escalera, junto a la meseta | En el rincón bajo el tramo de vuelta, junto a la entrada (altura libre de 2,05 m o más) |",
      "| Muros y puertas de seguridad | Suite | Suite y dormitorio 2 (una puerta RC3 más) |", "| Coste | — | Parecido al C2: de 1.000 € menos a 3.000 € más (estimación mía) |"]
h = [Paragraph("Opción D · suite, cocina y dormitorio", EST["H1"]),
     Paragraph("La suite grande a la izquierda, la cocina en medio y a la derecha un dormitorio más pequeño con un armario incorporado bajo la escalera. " + FECHA + ".", EST["body"]),
     figura("modelo_D_planta_baja.png", "Opción D: planta baja. Muros de seguridad rayados. Norte abajo.", wp, hp - 95, 2400),
     PageBreak(), Paragraph("Qué incluye", EST["H2"]),
     li("**Suite grande** de 11,9 m² a la izquierda: vestidor con la puerta de seguridad pegada al dormitorio (bisagra a la derecha al entrar), baño, muros de seguridad de 15 cm y asiento de lectura en la ventana de 1,30 m."),
     li("**Cocina en medio** de 9,4 m², abierta a la sala de estar por un paso libre de 1,60 m. Cocina en paralelo con pasillo de 1,10 m y **salida acristalada de aluminio de 1,40 m** al patio sur."),
     li("**Dormitorio 2 pequeño**, 9,5 m², a la derecha: puerta de seguridad de 0,85 m desde la sala, cama de 1,50 m con el cabecero contra la medianera y asiento de lectura en la ventana (1,10 m)."),
     li("**Armario incorporado bajo la escalera**, de unos 2,0 m², que se abre desde el dormitorio 2. Para hacerlo, la meseta de la escalera pasa a ser losa (en el modelo era maciza) y el armario técnico se traslada al rincón bajo el tramo de vuelta."),
     li("**Despacho girado** (4,8 m²), de la puerta del vestidor a la chimenea, como en el C2. Escalera, entrada y baño grande como en la v8."),
     Paragraph("El armario bajo la escalera", EST["H2"]), tabla(armario, wp),
     Paragraph("Superficies", EST["H2"]), tabla(filas, wp),
     Paragraph("Frente a la opción C2", EST["H2"]), tabla(vs, wp),
     Paragraph("A confirmar", EST["H2"]),
     li("Si el armario de 1,5 m de altura te sirve: ropa doblada, cajones y prendas cortas; las largas solo en la parte norte, que llega a 2,1 m."),
     li("Si la cocina de 9,4 m² es suficiente. No hay sitio para agrandarla sin quitárselo a la suite o al dormitorio 2; el comedor sería el del salón o una barra en el paso. La lavadora iría en el baño grande o en el armario técnico."),
     li("La losa de la meseta y las aberturas del tabique de la escalera los calcula el ingeniero."),
     Paragraph("Con tu OK hago el modelo 3D v9 con esta distribución, los muebles reales y los renders.", EST["small"])]
construir("pdf/Opcion_D_suite_cocina_dormitorio.pdf", "Opción D, suite, cocina y dormitorio", h)
print("ok", round(os.path.getsize("pdf/Opcion_D_suite_cocina_dormitorio.pdf") / 1e6, 2), "MB")
