# Cortijo – vivienda en Albox (Almería)

Proyecto personal. Polígono 33, parcela 198, San Roque (Albox). Arquitecto de la legalización y reforma: Andrés Oller Rodríguez (exp. 25-029). Todo es **preliminar**: necesita técnico para sismo, geotecnia, estado de los muros, armado, uniones y resistencia al fuego.

## Estado
- Distribución actual: vista en `distribucion.png` y `suite.png` (suite principal compacta con vestidor en L, rincón de lectura y despacho íntimo).
- Modelo 3D **v4**: `casa_v4.step` (FreeCAD/CAD) y `casa_v4.glb` (Blender/visor). Se genera con `python casa_v4.py` (CadQuery).
- Planos DXF v4: plantas, secciones y dos láminas A1 (`*_v4.dxf`).
- Vistas: `cortijo_3d.png`, `cortijo_3d_PB.png` (se generan con `vista3d.py`).
- Estructura: `estructura.py` → `memoria_estructura.md`; sismo en `sismo.py`; ahorro en `abaratar.md`; dossier para albañiles `dossier_obra.pdf` (distribución anterior).
- Documentos: `docs/` (disponibles/faltan, instalaciones, envolvente, inicio de cimentación, ahorro).

## Pendiente
- Decidir cuántos dormitorios van en la planta baja: la zona sur de la planta baja es amplia y podrían caber tres.
- Actualizar visor, dossier PDF y DXF cuando se cierre la distribución.
- Estudio geotécnico y catas de cimentación.

## Versiones antiguas
`casa.py`, `casa_v2.py`, `casa_v3.py`: modelos anteriores, se conservan por si hay que comparar.
