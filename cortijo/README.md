# Cortijo – vivienda en Albox (Almería)

Proyecto personal. Polígono 33, parcela 198, San Roque (Albox). Arquitecto de la legalización y reforma: Andrés Oller Rodríguez (exp. 25-029). Todo es **preliminar**: necesita técnico para sismo, geotecnia, estado de los muros, armado, uniones y resistencia al fuego.

## Estado
- Distribución actual (opción 2): abajo suite compacta + Dormitorio 2 (9,9 m²) + despacho íntimo (3,8 m²) pegado al vestidor, junto a la sala de estar + chimenea dentro del salón (34,2 m²) + cocina de 10 m² en U; arriba 3 dormitorios parejos con armarios empotrados. Ver `distribucion.png` y `suite.png`. **Medidas: las del croquis a mano del propietario (la casa se ha agrandado); no las del proyecto original.**
- Modelo 3D **v7** (actual, con paneles solares y aerotermia): `casa_v7.step` (FreeCAD/CAD) y `casa_v7.glb` (Blender/visor). Se genera con `python casa_v7.py` (CadQuery). Los v6 y anteriores se conservan.
- Planos DXF v5: plantas, secciones y dos láminas A1 (`*_v7.dxf`).
- Vistas: `cortijo_3d.png`, `cortijo_3d_PB.png` (se generan con `vista3d.py`).
- Estructura (líneas de vigas x = 3,10 / 5,55 / 7,20; acero ≈ 3,7 t): `estructura.py` → `memoria_estructura.md`; sismo en `sismo.py`; ahorro en `abaratar.md`; dossier para albañiles `dossier_obra.pdf` (distribución anterior).
- Instalaciones: `instalaciones.py` → `instalaciones.png` (fontanería, electricidad, climatización por planta) y `cubierta_solar.png`.
- Presupuesto y ahorro: `docs/08_presupuesto_y_ahorro.md`.
- Documentos: `docs/` (disponibles/faltan, instalaciones, envolvente, inicio de cimentación, ahorro, escalera y revisión de optimización).

## Pendiente
- Actualizar visor, dossier PDF y DXF cuando se cierre la distribución.
- Estudio geotécnico y catas de cimentación.

## Versiones antiguas
`casa.py`, `casa_v2.py`, `casa_v3.py`: modelos anteriores, se conservan por si hay que comparar.
