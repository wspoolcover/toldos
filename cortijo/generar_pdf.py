"""Pasa el proyecto a PDF: dossier completo (pdf/Cortijo_Albox_Dossier.pdf), un PDF por documento (pdf/docs/), y los planos DXF en PDF vectorial (pdf/planos/).
Uso: python generar_pdf.py        (regenera antes las imágenes a más resolución si hace falta; tarda un par de minutos)"""
import glob, io, os, re, subprocess, sys, shutil
from PIL import Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, HRFlowable, Image as RLImage, KeepTogether, NextPageTemplate, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FUENTES = "/usr/share/fonts/truetype/liberation/"
for nombre, f in (("LS", "LiberationSans-Regular"), ("LS-B", "LiberationSans-Bold"), ("LS-I", "LiberationSans-Italic"), ("LS-BI", "LiberationSans-BoldItalic"), ("LM", "LiberationMono-Regular")):
    pdfmetrics.registerFont(TTFont(nombre, FUENTES + f + ".ttf"))
pdfmetrics.registerFontFamily("LS", normal="LS", bold="LS-B", italic="LS-I", boldItalic="LS-BI")

INK, ACC, MUTED, LINE, PAPER = colors.HexColor("#201d19"), colors.HexColor("#8c4a2f"), colors.HexColor("#6a645b"), colors.HexColor("#c9c0b0"), colors.HexColor("#f1ece2")
FECHA = "14 de octubre de 2026"
AVISO = "Borrador preliminar · sin visado · medidas del croquis a mano del propietario"
EST = {
    "body": ParagraphStyle("body", fontName="LS", fontSize=9.4, leading=13.2, textColor=INK, spaceAfter=5),
    "small": ParagraphStyle("small", fontName="LS", fontSize=8, leading=10.4, textColor=MUTED),
    "cap": ParagraphStyle("cap", fontName="LS-I", fontSize=8.2, leading=10.5, textColor=MUTED, alignment=TA_CENTER, spaceAfter=6),
    "H1": ParagraphStyle("H1", fontName="LS-B", fontSize=21, leading=25, textColor=ACC, spaceBefore=0, spaceAfter=10),
    "H2": ParagraphStyle("H2", fontName="LS-B", fontSize=13.5, leading=17, textColor=INK, spaceBefore=11, spaceAfter=5),
    "H3": ParagraphStyle("H3", fontName="LS-B", fontSize=10.6, leading=14, textColor=ACC, spaceBefore=8, spaceAfter=3),
    "li": ParagraphStyle("li", fontName="LS", fontSize=9.4, leading=13, textColor=INK, spaceAfter=2.5),
    "cell": ParagraphStyle("cell", fontName="LS", fontSize=7.8, leading=9.8, textColor=INK),
    "cellh": ParagraphStyle("cellh", fontName="LS-B", fontSize=7.8, leading=9.8, textColor=INK),
}
TMP = "pdf/_tmp"


# ---------------------------------------------------------------- conversión de Markdown
def inline(t):
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<link href="\2" color="#1f5f8f">\1</link>', t)
    t = re.sub(r"`([^`]+)`", r'<font face="LM" size="8.4">\1</font>', t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![*\w])\*([^*\s][^*]*?)\*(?![*\w])", r"<i>\1</i>", t)
    return t


def tabla(filas, ancho):
    filas = [[c.strip() for c in f.strip().strip("|").split("|")] for f in filas if not re.match(r"^\s*\|?[\s:\-|]+\|?\s*$", f)]
    n = max(len(f) for f in filas); filas = [f + [""] * (n - len(f)) for f in filas]
    datos = [[Paragraph(inline(c), EST["cellh" if i == 0 else "cell"]) for c in f] for i, f in enumerate(filas)]
    pesos = [min(max(max(len(f[j]) for f in filas), 13), 70) for j in range(n)]
    tot = sum(pesos); cw = [ancho * p / tot for p in pesos]
    t = Table(datos, colWidths=cw, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), PAPER), ("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5), ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    return t


def md(ruta, ancho, desplazar=1, titulo=True):
    """Markdown -> flowables. 'desplazar' sube el nivel de los títulos (1: «#» pasa a H2 dentro de un capítulo; 0: «#» es H1)."""
    out, par, tab = [], [], []
    def vaciar():
        nonlocal par, tab
        if par: out.append(Paragraph(inline(" ".join(par)), EST["body"])); par = []
        if tab: out.append(Spacer(1, 2)); out.append(tabla(tab, ancho)); out.append(Spacer(1, 6)); tab = []
    primera = True
    for linea in open(ruta, encoding="utf-8").read().splitlines():
        if linea.strip().startswith("|"): tab.append(linea); continue
        if tab: vaciar()
        m = re.match(r"^(#{1,4})\s+(.*)", linea)
        if m:
            vaciar(); n = min(3, len(m.group(1)) + desplazar - (0 if desplazar else 0))
            if primera and not titulo: primera = False; continue
            primera = False
            out.append(Paragraph(inline(m.group(2)), EST["H%d" % max(1, n)])); continue
        if re.match(r"^\s*-{3,}\s*$", linea): vaciar(); out.append(HRFlowable(width="100%", thickness=0.5, color=LINE, spaceBefore=4, spaceAfter=6)); continue
        b = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)", linea)
        if b:
            vaciar(); nivel = len(b.group(1)) // 2; marca = "•" if b.group(2) in "-*" else b.group(2)
            out.append(Paragraph(inline(b.group(3)), ParagraphStyle("li%d" % nivel, parent=EST["li"], leftIndent=13 + 12 * nivel, bulletIndent=2 + 12 * nivel), bulletText=marca)); continue
        if not linea.strip(): vaciar(); continue
        par.append(linea.strip())
    vaciar()
    return out


# ---------------------------------------------------------------- imágenes
def recortar(im, pad=14):
    """Quita el margen blanco sobrante de planos y vistas (los renders no tienen)."""
    from PIL import ImageChops
    caja = ImageChops.difference(im, Image.new("RGB", im.size, (255, 255, 255))).convert("L").point(lambda p: 255 if p > 12 else 0).getbbox()
    if not caja: return im
    l, t, r, b = caja; return im.crop((max(0, l - pad), max(0, t - pad), min(im.width, r + pad), min(im.height, b + pad)))


def jpg(origen, ancho_max=2200, q=88):
    os.makedirs(TMP, exist_ok=True)
    destino = f"{TMP}/{os.path.splitext(os.path.basename(origen))[0]}.jpg"
    im = recortar(Image.open(origen).convert("RGB"))
    if im.width > ancho_max: im = im.resize((ancho_max, int(im.height * ancho_max / im.width)), Image.LANCZOS)
    im.save(destino, "JPEG", quality=q, optimize=True); return destino, im.size


def figura(origen, pie, maxw, maxh, ancho_max=2200):
    ruta, (w, h) = jpg(origen, ancho_max); k = min(maxw / w, maxh / h)
    return KeepTogether([RLImage(ruta, width=w * k, height=h * k), Spacer(1, 2), Paragraph(inline(pie), EST["cap"])])


# ---------------------------------------------------------------- documento
class Dossier(BaseDocTemplate):
    def __init__(self, ruta, titulo, con_portada=True, **kw):
        super().__init__(ruta, pagesize=A4, title=titulo, author="Diseño del cortijo de Albox", subject="Dossier del proyecto (borrador preliminar)", **kw)
        mg = 18 * mm; w, h = A4
        vert = Frame(mg, 16 * mm, w - 2 * mg, h - 34 * mm, id="v", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        wl, hl = landscape(A4)
        horiz = Frame(mg, 14 * mm, wl - 2 * mg, hl - 30 * mm, id="h", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        plantillas = [PageTemplate("port", frames=[vert], pagesize=A4, onPage=self.cabecera), PageTemplate("land", frames=[horiz], pagesize=landscape(A4), onPage=self.cabecera)]
        if con_portada: plantillas.insert(0, PageTemplate("portada", frames=[Frame(0, 0, w, h, id="c", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)], pagesize=A4, onPage=self.portada))
        self.addPageTemplates(plantillas)
        self.titulo_corto = "Cortijo Albox · " + titulo

    def cabecera(self, c, d):
        w, h = c._pagesize; c.saveState(); c.setFont("LS", 7.6); c.setFillColor(MUTED)
        c.drawString(18 * mm, h - 11 * mm, self.titulo_corto); c.drawRightString(w - 18 * mm, h - 11 * mm, AVISO)
        c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(18 * mm, h - 13 * mm, w - 18 * mm, h - 13 * mm)
        c.drawCentredString(w / 2, 8 * mm, f"{d.page}"); c.restoreState()

    def portada(self, c, d):
        w, h = A4; c.saveState(); c.setFillColor(PAPER); c.rect(0, 0, w, h, fill=1, stroke=0)
        c.setFillColor(ACC); c.rect(0, h - 14 * mm, w, 14 * mm, fill=1, stroke=0)
        if getattr(self, "hero", None):
            im = Image.open(self.hero); k = (w - 36 * mm) / im.width; c.drawImage(self.hero, 18 * mm, h - 38 * mm - im.height * k, width=im.width * k, height=im.height * k)
            y = h - 38 * mm - im.height * k - 14 * mm
        else: y = h - 60 * mm
        c.setFillColor(INK); c.setFont("LS-B", 34); c.drawString(18 * mm, y - 6 * mm, self.cover_titulo)
        c.setFont("LS", 13.5); c.setFillColor(ACC)
        for i, linea in enumerate(self.cover_sub): c.drawString(18 * mm, y - 18 * mm - i * 6.2 * mm, linea)
        c.setFillColor(MUTED); c.setFont("LS", 9.4)
        for i, linea in enumerate(self.cover_notas): c.drawString(18 * mm, 40 * mm - i * 5.2 * mm, linea)
        c.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ("H1", "H2"):
            self.notify("TOCEntry", (0 if f.style.name == "H1" else 1, f.getPlainText(), self.page))


def construir(ruta, titulo, historia, portada=None):
    d = Dossier(ruta, titulo, con_portada=bool(portada))
    if portada: d.hero, d.cover_titulo, d.cover_sub, d.cover_notas = portada
    d.multiBuild(historia)


def indice():
    t = TableOfContents(); t.levelStyles = [ParagraphStyle("t1", fontName="LS-B", fontSize=10.5, leading=17, leftIndent=0, textColor=INK, spaceBefore=3),
                                            ParagraphStyle("t2", fontName="LS", fontSize=9, leading=12.5, leftIndent=14, textColor=MUTED)]
    return t


# ---------------------------------------------------------------- datos de los proveedores (del modelo)
def tablas_proveedores(ancho):
    import mediciones as m
    f = lambda x: f"{x:.2f}".replace(".", ",") if isinstance(x, float) else str(x)
    ven = ["| Elemento | Planta | Ancho (m) | Alto (m) | Antepecho (m) | Uds | Descripción |", "|---|---|---|---|---|---|---|"] + [f"| {n} | {p} | {f(w)} | {f(h)} | {f(s)} | {u} | {d} |" for (n, p, w, h, s, u, d) in m.ven]
    sup = sum(w * h * u for (_, _, w, h, _, u, _) in m.ven)
    pue = ["| Elemento | Planta | Ancho (m) | Alto (m) | Uds | Descripción |", "|---|---|---|---|---|---|"] + [f"| {n} | {p} | {f(w)} | {f(h)} | {u} | {d} |" for (n, p, w, h, u, d) in m.pue]
    hie = ["| Pieza | Perfil | Longitud (m) | Uds | kg/m | Peso (kg) |", "|---|---|---|---|---|---|"] + [f"| {c} | {s} | {f(L)} | {n} | {f(k)} | {kg:.0f} |" for (c, s, L, n, k, kg) in m.rows_h] \
          + [f"| {e[0]} |  |  | {e[3]} |  | {e[5]:.0f} |" for e in m.extras] + [f"| **Total hierro** |  |  |  |  | **{m.kg_tot:,.0f}** |".replace(",", ".")]
    return [Paragraph("Ventanas, cristaleras y fijos", EST["H2"]), tabla(ven, ancho), Paragraph(f"Superficie de carpintería de huecos: <b>{sup:.1f} m²</b>. Medidas de obra del modelo v8.".replace(".", ","), EST["small"]),
            Paragraph("Puertas", EST["H2"]), tabla(pue, ancho), Paragraph("Hierro (acero S275JR)", EST["H2"]), tabla(hie, ancho),
            Paragraph("Las filas sin perfil son estimaciones (escalera, barandillas, soportes solares, placas, tornillería): confirmar con el taller. Los perfiles son una propuesta que debe calcular un ingeniero. Las columnas de precio están en <font face=\"LM\">pedido_proveedores.xlsx</font>.", EST["small"])]


def planos_vectoriales():
    import ezdxf, matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from ezdxf import bbox
    from ezdxf.addons.drawing import Frontend, RenderContext
    from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration
    from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
    os.makedirs("pdf/planos", exist_ok=True)
    hojas = [("lamina_A1_v8_distribucion", "A1: distribución (plantas y secciones)"), ("lamina_A1_v8_estructura", "A1: estructura de acero"), ("planta_baja_v8", "planta baja"), ("planta_alta_v8", "planta alta"),
             ("seccion_A_v8", "sección A-A'"), ("seccion_B_v8", "sección B-B'"), ("estructura_forjado_v8", "estructura del forjado"), ("estructura_cubierta_v8", "estructura de cubierta"), ("cimentacion_v7", "cimentación y zunchos")]
    hecho = []
    for nombre, desc in hojas:
        if not os.path.exists(nombre + ".dxf"): continue
        doc = ezdxf.readfile(nombre + ".dxf"); msp = doc.modelspace(); ext = bbox.extents(msp)
        x0, y0, x1, y1 = ext.extmin.x, ext.extmin.y, ext.extmax.x, ext.extmax.y
        if nombre.startswith("lamina"): x0, y0, x1, y1 = 0, 0, 841, 594; fs = (33.11, 23.39)
        else:
            pad = 0.05 * max(x1 - x0, y1 - y0); x0, y0, x1, y1 = x0 - pad, y0 - pad, x1 + pad, y1 + pad; k = 16.5 / max(x1 - x0, y1 - y0); fs = ((x1 - x0) * k, (y1 - y0) * k)
        fig = plt.figure(figsize=fs); ax = fig.add_axes([0, 0, 1, 1])
        Frontend(RenderContext(doc), MatplotlibBackend(ax), config=Configuration(background_policy=BackgroundPolicy.WHITE, color_policy=ColorPolicy.BLACK)).draw_layout(msp)
        ax.set_xlim(x0, x1); ax.set_ylim(y0, y1); ax.set_aspect("equal"); ax.axis("off")
        fig.savefig(f"pdf/planos/{nombre}.pdf", facecolor="white"); plt.close(fig); hecho.append((nombre, desc))
    return hecho


def regenerar_imagenes():
    env = dict(os.environ, DPI="190")
    for s in ("opciones.py", "modelos_pb.py", "instalaciones.py"): subprocess.run([sys.executable, s], env=env, check=True, capture_output=True)


# ---------------------------------------------------------------- ensamblado
def main():
    shutil.rmtree(TMP, ignore_errors=True); os.makedirs("pdf/docs", exist_ok=True)
    regenerar_imagenes()
    W, H = A4; wp = W - 36 * mm; hp = H - 40 * mm; wl, hl = landscape(A4); wl -= 36 * mm; hl -= 36 * mm
    docs = sorted(glob.glob("docs/*.md"))
    por_nombre = lambda n: next(d for d in docs if os.path.basename(d).startswith(n))
    h = []
    h += [NextPageTemplate("port"), PageBreak(), Paragraph("Índice", EST["H1"]), indice(), PageBreak()]
    # 1 resumen
    h += [Paragraph("1. Resumen del proyecto", EST["H1"])]
    h += md("docs/00_resumen.md", wp, desplazar=1, titulo=False) if os.path.exists("docs/00_resumen.md") else []
    h += [NextPageTemplate("land"), PageBreak(), Paragraph("Vistas del modelo 3D", EST["H2"]), figura("cortijo_3d.png", "Modelo v8, vista exterior (CadQuery).", wl, hl - 75),
          NextPageTemplate("port"), PageBreak()]
    # 2 propuestas
    h += [Paragraph("2. Propuestas para la planta baja", EST["H1"])] + md("docs/15_propuestas_planta_baja.md", wp, desplazar=1, titulo=False)
    h += [NextPageTemplate("land"), PageBreak(), Paragraph("Comparación de los tres modelos (mitad sur de la planta baja)", EST["H2"]), figura("modelos_planta_baja.png", "A: dormitorio 2 pequeño y cocina-comedor al este · B: cocina-comedor grande · C: cocina central con despensa y lavadero. Muros de seguridad rayados.", wl, hl - 75, 2600)]
    for k, t in (("A", "Modelo A"), ("B", "Modelo B"), ("C", "Modelo C")):
        h += [NextPageTemplate("port"), PageBreak(), figura(f"modelo_{k}_planta_baja.png", f"{t}: planta baja completa (muros de seguridad rayados).", wp, hp - 12, 2000)]
    h += [NextPageTemplate("land"), PageBreak(), Paragraph("Muebles libres disponibles (Poly Haven, licencia CC0)", EST["H2"]), figura("muebles_disponibles.png", "Piezas ya descargadas para los renders. Los armarios de cocina y las camas se modelan aparte.", wl, hl - 75, 1750)]
    # 3 distribución actual
    h += [NextPageTemplate("land"), PageBreak(), Paragraph("3. Distribución actual (v8)", EST["H1"]),
          figura("distribucion.png", "Plantas baja y alta, norte abajo (acceso por el camino) y sur arriba (patio hacia la rambla de Albox).", wl, hl - 55, 2800)]
    h += [NextPageTemplate("port"), PageBreak(), Paragraph("Suite principal", EST["H2"]), figura("suite.png", "Suite: dormitorio, vestidor y baño; despacho junto a la sala de estar.", wp, hp - 60, 1500), Spacer(1, 6)]
    h += md(por_nombre("14"), wp, desplazar=1) + md(por_nombre("06"), wp, desplazar=1)
    # 4 renders
    h += [PageBreak(), Paragraph("4. Renders", EST["H1"])]
    rr = [("render_exterior_norte.png", "Fachada norte: salón de piedra marés con cristalera, puerta de entrada y terraza."), ("render_exterior_sur.png", "Fachada sur, hacia la rambla: casa encalada, ventanas con contraventanas de madera, paneles solares."),
          ("render_salon_interior.png", "Salón: muro de piedra, chimenea, comedor y, al fondo, la sala de estar."), ("render_planta_baja_abierta.png", "Planta baja abierta, vista desde arriba."),
          ("render_sala_a_cocina.png", "De la sala de estar a la cocina: paso libre."), ("render_entrada_escalera.png", "Entrada con el pie de la escalera, el baño grande y el paso bajo la escalera.")]
    for i in range(0, len(rr), 2):
        if i: h.append(PageBreak())
        for a, b in rr[i:i + 2]: h += [figura(a, b, wp, hp / 2 - 22, 1700), Spacer(1, 6)]
    h += [Paragraph("Los muebles y materiales de estos renders son los de la v8 (representativos). Los renders con los muebles nuevos se harán con el modelo elegido.", EST["small"])]
    # 5 instalaciones
    h += [NextPageTemplate("port"), PageBreak(), Paragraph("5. Instalaciones", EST["H1"])] + md(por_nombre("02"), wp, desplazar=1, titulo=False)
    h += [NextPageTemplate("land"), PageBreak(), figura("instalaciones.png", "Fontanería, electricidad y climatización de las dos plantas (esquema de intenciones, no proyecto de ejecución).", wl, hl - 12, 2800),
          PageBreak(), figura("cubierta_solar.png", "Cubierta: 16 paneles solares, lucernario de la escalera, aerotermia y sumideros.", wl, hl - 12, 1800)]
    # 6 estructura y cimentación
    h += [NextPageTemplate("port"), PageBreak(), Paragraph("6. Estructura y cimentación", EST["H1"])] + md("memoria_estructura.md", wp, desplazar=1, titulo=False)
    h += [NextPageTemplate("land"), PageBreak(), figura("estructura_planos.png", "Estructura: vigas de acero, pilares y forjados (predimensionado).", wl, hl - 12, 2400), PageBreak(),
          figura("cimentacion_planos.png", "Cimentación y zunchos (propuesta).", wl, hl - 12, 2400), NextPageTemplate("port"), PageBreak()]
    h += md(por_nombre("10"), wp, desplazar=1) + md(por_nombre("04"), wp, desplazar=1)
    # 7 envolvente y decisiones
    h += [PageBreak(), Paragraph("7. Envolvente, ahorro y revisión del diseño", EST["H1"])] + md(por_nombre("03"), wp, desplazar=1) + md(por_nombre("05"), wp, desplazar=1) + md(por_nombre("07"), wp, desplazar=1) + md(por_nombre("16"), wp, desplazar=1) + [Spacer(1, 6), figura("detalles_apoyo_placa.png", "Apoyo de la placa superior: sobre el zuncho del muro, sobre una viga de acero y viga sobre pilarete de bloque (esquemas sin escala).", wp, hp / 2.4, 2000), figura("viga_bloque_u.png", "Viga o dintel de hormigón hecho con bloque en U (esquemas sin escala).", wp, hp / 2.4, 2000)]
    # 8 presupuesto y proveedores
    h += [PageBreak(), Paragraph("8. Presupuesto y proveedores", EST["H1"])] + md(por_nombre("08"), wp, desplazar=1) + md(por_nombre("09"), wp, desplazar=1) + tablas_proveedores(wp)
    # 9 terreno
    h += [PageBreak(), Paragraph("9. Estado real, terreno y ubicación", EST["H1"])] + md(por_nombre("11"), wp, desplazar=1) + md(por_nombre("12"), wp, desplazar=1) + md(por_nombre("13"), wp, desplazar=1) + md(por_nombre("01"), wp, desplazar=1)
    # 10 pendientes
    h += [PageBreak(), Paragraph("10. Pendientes y decisiones", EST["H1"])] + md("docs/99_pendientes.md", wp, desplazar=1, titulo=False)
    # anexo planos
    planos = planos_vectoriales()
    h += [PageBreak(), Paragraph("Anexo. Planos DXF en PDF vectorial", EST["H1"]), Paragraph("Cada plano DXF del proyecto está en PDF vectorial en la carpeta <font face=\"LM\">pdf/planos/</font> (ampliable sin perder calidad). Los DXF originales (AutoCAD o FreeCAD) están en la carpeta del proyecto:", EST["body"])]
    h += [Paragraph(f"<font face=\"LM\" size=\"8.4\">{n}.pdf</font> — {d}", EST["li"]) for n, d in planos]
    construir("pdf/Cortijo_Albox_Dossier.pdf", "Dossier del proyecto", h,
              portada=(jpg("render_exterior_norte.png", 1600)[0], "Cortijo de Albox", ["Dossier del proyecto de reforma y ampliación", "Diseño v8 y propuestas para la planta baja", FECHA],
                       ["Polígono 33, parcela 198 · San Roque, Albox (Almería)", "Borrador preliminar: no sustituye un proyecto visado. La estructura, la cimentación, el sismo, la seguridad", "y las uniones los define un técnico competente. Medidas del croquis a mano del propietario."]))
    # un PDF por documento
    for d in docs + ["memoria_estructura.md"]:
        nombre = os.path.splitext(os.path.basename(d))[0]
        construir(f"pdf/docs/{nombre}.pdf", nombre.replace("_", " "), md(d, wp, desplazar=0))
    shutil.rmtree(TMP, ignore_errors=True)
    print("ok", round(os.path.getsize("pdf/Cortijo_Albox_Dossier.pdf") / 1e6, 1), "MB")


if __name__ == "__main__":
    main()
