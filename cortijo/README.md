# Cortijo – vivienda en Albox (Almería)

Proyecto personal. Polígono 33, parcela 198, San Roque (Albox). Arquitecto de la legalización y reforma: Andrés Oller Rodríguez (exp. 25-029). Todo es **preliminar**: necesita técnico para sismo, geotecnia, estado de los muros, armado, uniones y resistencia al fuego.

## Estado
- Orientación (confirmada por el propietario): el norte (salón y entrada) es el acceso por el camino, con entrada de 7 m con puerta corredera y la acometida de agua; el sur (fachada ancha con la CGP y las rejas) es terreno propio hacia la rambla de Albox. Distribución actual (v8): abajo suite compacta + Dormitorio 2 (9,7 m², al este) + despacho íntimo (3,8 m²) pegado al vestidor, junto a la sala de estar + chimenea dentro del salón (34,2 m²) + cocina de 9,4 m² abierta a la sala por un paso libre de 1,60 m; la escalera tiene el pie junto a la entrada y ya no tapa la cocina ni el baño grande (`docs/14_escalera_cocina_v8.md`); arriba 3 dormitorios con armarios empotrados. Ver `distribucion.png` y `suite.png`. **Medidas: las del croquis a mano del propietario (la casa se ha agrandado); no las del proyecto original.**
- Modelo 3D **v8** (actual: escalera y cocina reubicadas, 16 paneles solares, aerotermia): `casa_v8.step` (FreeCAD/CAD) y `casa_v8.glb` (Blender/visor). Se genera con `python casa_v8.py` (CadQuery). Los v7 y anteriores se conservan.
- Comprobación de circulación: `python verificar_circulacion.py [casa_v8.glb]` corta el modelo y dice qué estancias quedan unidas por un paso de 0,70 m (con v7 falla, con v8 pasa).
- Planos DXF v8: plantas, secciones y dos láminas A1 (`*_v8.dxf`; se generan con `python dxf_v8.py`).
- Vistas: `cortijo_3d.png`, `cortijo_3d_PB.png` (se generan con `vista3d.py`).
- Render realista (Blender como módulo `bpy`, Cycles, materiales procedurales, estilo cortijo andaluz/mallorquín: encalado, piedra marés en el salón, madera oscura, barro cocido): `render_blender.py` → `render_*.png`. Se ejecuta con `python render_blender.py 48` (48 = muestras).
- Estructura (líneas de vigas x = 3,10 / 5,55 / 7,20; acero ≈ 3,7 t): `estructura.py` → `memoria_estructura.md`; sismo en `sismo.py`; ahorro en `abaratar.md`; dossier para albañiles `dossier_obra.pdf` (distribución anterior).
- Instalaciones: `instalaciones.py` → `instalaciones.png` (fontanería, electricidad, climatización por planta) y `cubierta_solar.png`.
- Presupuesto y ahorro: `docs/08_presupuesto_y_ahorro.md`.
- Documentos: `docs/` (disponibles/faltan, instalaciones, envolvente, inicio de cimentación, ahorro, escalera y revisión de optimización).

- Visor web interactivo (modelo 3D con capas, renders, plantas, instalaciones): `visor_v7.html` (publicado como artefacto «Cortijo Albox»; sigue con la v7 hasta que se republique).

- Estado real (fotos del 12-10-2026): `docs/11_estado_real_fotos.md`.

- **Propuestas para la planta baja (14-10-2026)**: tres modelos A, B y C con cocina más amplia y salida de aluminio, puerta del vestidor, muros y puertas de seguridad y asientos en las ventanas del sur: `docs/15_propuestas_planta_baja.md`, `modelos_planta_baja.png` (se generan con `python modelos_pb.py`). A la espera de elegir uno para hacer el modelo 3D v9 y los renders.
- **Ideas de obra (referencia de una constructora)**: `docs/16_ideas_de_obra_referencia.md` y `detalles_apoyo_placa.png` y `viga_bloque_u.png` (`python detalles_apoyo.py`): viga sobre pilarete de bloque, zuncho de bloque en U, placas alveolares para el salón, apoyo de la placa superior y vigas de hormigón con bloque en U.
- **Opción C2 (cocina central con el despacho girado)**: `pdf/Opcion_C_cocina_central.pdf` y `modelo_C2_planta_baja.png` (`python pdf_opcion_c.py`).
- **Opción D (suite, cocina en medio y dormitorio pequeño con armario bajo la escalera)**: `pdf/Opcion_D_suite_cocina_dormitorio.pdf` y `modelo_D_planta_baja.png` (`python pdf_opcion_d.py`).
- **Versión económica y rápida (14-10-2026)**: `docs/17_version_economica.md`, `version_economica_costes.png` y `modelo_C2E_planta_baja.png` (`python economica.py`; `python modelos_pb.py`). Ahorro estimado 30–53 mil € sin recortar estructura, cimentación, aislamiento ni seguridad.
- **Fosa séptica y pozo filtrante (28-10-2026)**: `docs/18_fosa_septica_y_pozo_filtrante.md`, `fosa_septica_esquema.png` y `pozo_filtrante_5m.png` (`python fosa_esquema.py`). Cómo funciona, normativa comprobada, pozo de 5 m con anillos (diámetros, pesos, tasa de infiltración que necesita), qué pedir al proveedor y por qué todavía no conviene comprar los anillos.
- **PDF**: `pdf/Cortijo_Albox_Proyecto_completo.pdf` (todo en uno, con la versión económica), `pdf/docs/*.pdf` (un PDF por documento) y `pdf/planos/*.pdf` (planos DXF en vectorial). Se regeneran con `python generar_pdf.py`.
- **Muebles libres** (CC0, Poly Haven) para los renders: `python descargar_muebles.py` los baja a `assets/` (no se suben al repositorio); vista previa en `muebles_disponibles.png`.

## Pendiente
- Elegir el modelo de planta baja y pasarlo al modelo 3D (v9), renders con muebles, DXF, visor y PDF. El `dossier_obra.pdf` antiguo (cimentación y estructura para albañiles) sigue con una distribución anterior.
- Estudio geotécnico y catas de cimentación.

## Versiones antiguas
`casa.py`, `casa_v2.py`, `casa_v3.py`: modelos anteriores, se conservan por si hay que comparar.
