# Cortijo – vivienda en Albox (Almería)

Proyecto personal. Polígono 33, parcela 198, San Roque (Albox). Arquitecto de la legalización y reforma: Andrés Oller Rodríguez (exp. 25-029). Todo es **preliminar**: necesita técnico para sismo, geotecnia, estado de los muros, armado, uniones y resistencia al fuego.

## Estado
- Distribución actual (opción 2): abajo suite compacta + Dormitorio 2 (9,9 m²) + despacho íntimo (3,8 m²) pegado al vestidor, junto a la sala de estar + chimenea dentro del salón (34,2 m²) + cocina de 10 m²; arriba 3 dormitorios. Ver `distribucion.png` y `suite.png`. **Medidas: las del croquis a mano del propietario (la casa se ha agrandado); no las del proyecto original.**
- Modelo 3D **v6** (actual): `casa_v6.step` (FreeCAD/CAD) y `casa_v6.glb` (Blender/visor). Se genera con `python casa_v6.py` (CadQuery). Los v5 y anteriores se conservan.
- Planos DXF v5: plantas, secciones y dos láminas A1 (`*_v6.dxf`).
- Vistas: `cortijo_3d.png`, `cortijo_3d_PB.png` (se generan con `vista3d.py`).
- Estructura: `estructura.py` → `memoria_estructura.md`; sismo en `sismo.py`; ahorro en `abaratar.md`; dossier para albañiles `dossier_obra.pdf` (distribución anterior).
- Documentos: `docs/` (disponibles/faltan, instalaciones, envolvente, inicio de cimentación, ahorro).

## Pendiente
- Actualizar visor, dossier PDF y DXF cuando se cierre la distribución.
- Estudio geotécnico y catas de cimentación.

## Versiones antiguas
`casa.py`, `casa_v2.py`, `casa_v3.py`: modelos anteriores, se conservan por si hay que comparar.
