"""PDF de la opción C (cocina central) con el despacho girado: pdf/Opcion_C_cocina_central.pdf. Uso: python pdf_opcion_c.py"""
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import generar_pdf as g
from generar_pdf import EST, FECHA, AVISO, figura, tabla, md, construir, Paragraph, Spacer, PageBreak, A4, mm, inline
import modelos_pb as mp

fig, ax = plt.subplots(figsize=(7.2, 9.4)); tot = mp.dibujar(ax, mp.MODELO_C2); fig.tight_layout(); fig.savefig("modelo_C2_planta_baja.png", dpi=int(os.environ.get("DPI", 200))); plt.close(fig)   # más resolución para el PDF
W, H = A4; wp = W - 36 * mm; hp = H - 40 * mm
f1 = lambda x: f"{x:.1f}".replace(".", ",")
def li(t): return Paragraph(inline(t), g.ParagraphStyle("li", parent=EST["li"], leftIndent=13, bulletIndent=2), bulletText="•")

nombres = ("Salón con comedor", "Pasillo de entrada", "Entrada", "Escalera", "Sala de estar", "Despacho", "Cocina", "Despensa", "Lavadero", "Dormitorio principal", "Vestidor", "Baño", "Baño grande")
mitad = (len(nombres) + 1) // 2
filas = ["| Estancia | m² | Estancia | m² |", "|---|---|---|---|"] + [f"| {nombres[i]} | {f1(tot[nombres[i]])} | " + (f"{nombres[i + mitad]} | {f1(tot[nombres[i + mitad]])} |" if i + mitad < len(nombres) else " |  |") for i in range(mitad)]
antes = ["| | v8 | Opción C2 |", "|---|---|---|",
         "| Forma | 2,40 × 1,58 m, horizontal, junto al salón | 1,80 × 2,65 m, vertical, a lo largo de la pared del vestidor |",
         "| Superficie | 3,8 m² | 4,8 m² |", "| Recorrido | Al norte de la sala de estar | De la puerta del vestidor a la chimenea |",
         "| Puerta | Por el lado sur, desde la sala | Por el lado este, desde la sala, junto al extremo sur |",
         "| Cristal fijo | 2,0 m hacia el salón | 1,60 m en el extremo norte, hacia el salón y la chimenea |", "| Sala de estar | 11,1 m² | 10,1 m² |"]
h = [Paragraph("Opción C · cocina central", EST["H1"]),
     Paragraph("Planta baja con el despacho girado, de la puerta del vestidor hasta la chimenea. " + FECHA + ".", EST["body"]),
     figura("modelo_C2_planta_baja.png", "Opción C2: cocina central de 13,4 m² con despensa y lavadero; despacho girado. Muros de seguridad rayados. Norte abajo.", wp, hp - 60, 2400),
     PageBreak(), Paragraph("Qué incluye", EST["H2"]),
     li("**Cocina central de 13,4 m²**, abierta a la sala de estar por dos pasos libres (1,60 y 1,45 m), con mesa de comedor, **salida acristalada de aluminio de 1,60 m** al patio sur y asiento de lectura en la ventana (banco de obra de 45 cm de altura)."),
     li("**Despensa de 2,0 m² y lavadero de 3,7 m²** al este, con puerta desde la cocina. El lavadero puede ser más adelante una habitación pequeña."),
     li("**Despacho girado**, a lo largo de la pared del vestidor: mesa larga contra la pared, estantería y sillón de lectura junto a la puerta, y cristal fijo en el extremo norte hacia el salón y la chimenea."),
     li("**Suite**: puerta de seguridad del vestidor pegada al dormitorio (bisagra a la derecha al entrar, abre hacia el vestidor), puerta de seguridad al dormitorio, muros de seguridad de 15 cm (hormigón armado o bloque de hormigón relleno y armado) y asiento de lectura en la ventana de 1,30 m."),
     li("No hay dormitorio 2 abajo: la casa queda con cuatro dormitorios (suite y tres arriba). Escalera, entrada, baño grande y armario técnico como en la v8."),
     Paragraph("Superficies", EST["H2"]), tabla(filas, wp), Spacer(1, 4),
     Paragraph("El despacho, antes y ahora", EST["H2"]), tabla(antes, wp),
     Paragraph("A confirmar", EST["H2"]),
     li("¿He entendido bien el despacho? Girado 90°, pegado a la pared del vestidor, desde su puerta hasta la chimenea del salón."),
     li("Si quieres **ver el fuego desde el despacho**, la chimenea se gira o se hace de dos caras con cristal. Ahora el cristal da al salón y a un lado de la chimenea."),
     li("Si «luminio» era aluminio (así lo he puesto en la salida de la cocina) o una salida grande y luminosa; el diseño sirve para las dos."),
     li("Si en la planta alta quieres también asientos en las ventanas y paredes de seguridad."),
     Paragraph("Siguiente paso", EST["H2"]),
     Paragraph("Con tu OK hago el modelo 3D v9 con esta distribución y los muebles reales, 6 a 8 renders (cocina, suite con el asiento, vestidor, despacho con vista a la chimenea, salón, patio sur y exterior), los planos DXF y el dossier actualizados.", EST["body"]),
     Paragraph(AVISO + ".", EST["small"])]
os.makedirs("pdf", exist_ok=True)
construir("pdf/Opcion_C_cocina_central.pdf", "Opción C, cocina central", h)
print("ok", round(os.path.getsize("pdf/Opcion_C_cocina_central.pdf") / 1e6, 2), "MB")
