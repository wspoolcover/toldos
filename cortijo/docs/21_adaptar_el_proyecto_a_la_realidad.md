# Adaptar el proyecto visado a la casa que se construye (04-11-2026)

El proyecto visado (PL-04 a PL-11, 22-09-2025) es el punto de partida. La casa que se construye es la del modelo v8, con las medidas del propietario y ampliada. Este documento lista **qué hay que cambiar en cada lámina** y **con qué datos**. No sustituye al arquitecto: es el material de trabajo para pasárselo.

## 1. Muros caídos (aviso del propietario, 04-11-2026)
Sobre la lámina PL-05 (fase 3, «consolidación estructural y recrecido de muros») el propietario marca:
- **Dos muros que han caído**: el **muro norte de la casa** (el que separa el porche de la casa) y el **muro central** («muro existente» de PL-11), por lo que dibuja la marca.
- En una segunda marca, el **muro este y el muro sur**. **Pendiente de confirmar**: no sé si también han caído o si son los que siguen en pie.

Lo que implica, sea cual sea el caso:
- **Seguridad primero**: nadie debe pasar bajo los muros que quedan ni cerca de ellos hasta que los revise un técnico. Las casas vecinas están pegadas (este y oeste). PL-05 (ADD-13) dice que al interrumpir la jornada no se dejen muros sin arriostrar de más de 7 veces su espesor: con muros de 55 cm, unos 3,85 m. Hay que **apuntalar** los que sigan en pie y **no retirar escombros** antes de fotografiarlo y de que lo vea el arquitecto.
- **Avisar al arquitecto** (director de obra), y al seguro de obra si lo hay. Si hay daños en las casas vecinas o personas afectadas, es un asunto aparte que no sé valorar.
- **El proyecto visado se apoyaba en el muro central** (PL-11: viguetas T-20 a cada lado del «muro existente»), así que ya no se puede construir tal cual.
- **Nuestra estructura no depende de esos dos muros**: la línea norte (y ≈ 7,60) y la central (y = 11,80) llevan pilares HEB 120 y vigas, con zapatas y riostras. Sí depende de los **muros laterales** (este y oeste), que arriostraban los muros caídos, y del **muro sur**: hay que comprobar que no están inclinados ni dañados.
- **Cimentación**: bajo los muros caídos puede seguir su zapata. Hay que verla con una cata antes de hormigonar la línea y = 7,60 (ver `19_comprobacion_cimentacion.md`), y comprobar también la de los muros que sigan en pie.

## 2. Superficies de la casa que se construye (modelo v8)
Superficies útiles por estancia. La planta baja cambia algo según la opción elegida (A, B, C, C2 o D; ver `15_propuestas_planta_baja.md`); aquí va la base v8.

| Planta baja | m² | Planta alta | m² |
|---|---|---|---|
| Salón con comedor | 33,91 | Sala familiar | 12,03 |
| Pasillo de entrada (junto al salón) | 11,05 | Entrada | 3,50 |
| Entrada | 3,12 | Baño | 3,48 |
| Escalera | 4,62 | Dormitorio 1 | 13,19 |
| Baño grande | 5,76 | Dormitorio 2 | 16,77 |
| Sala de estar y paso | 11,07 | Dormitorio 3 / despacho | 14,80 |
| Cocina | 9,36 | | |
| Dormitorio principal | 12,09 | | |
| Dormitorio 2 | 9,73 | | |
| Despacho | 3,79 | | |
| Vestidor | 5,75 | | |
| Baño principal | 3,70 | | |
| **Total útil planta baja** | **113,94** | **Total útil planta alta** | **63,77** |

**Total útil: 177,71 m²**, más la terraza sobre el salón (42,42 m²).

| | Proyecto visado | Casa que se construye |
|---|---|---|
| Útil planta baja | 91,45 m² (con el porche de 23,49) | 113,94 m² |
| Útil planta alta | 63,63 m² | 63,77 m² |
| **Útil total** | **155,08 m²** | **177,71 m²** |
| Terraza | 23,00 m² | 42,42 m² |
| Construida | 200,00 m² (PB 115,35 + PA 84,65) | **≈ 233 m²** por huellas: PB 142,4 (casa 94,5 + salón 47,9) y PA 90,3 |

La superficie construida es mía, por las huellas exteriores; el arquitecto la calcula con su criterio (terrazas, porches, muros).

## 3. Qué hay que cambiar en cada lámina
| Lámina | Qué hay que cambiar | Datos nuestros que sirven |
|---|---|---|
| **PL-04** estado actual | Lo que había antes de caer los muros. Añadir el estado actual de obra y los muros caídos | Fotos y medidas de obra (pendientes) |
| **PL-05** fases | Nueva secuencia: muros caídos, apeos, cimentación nueva (zanja perimetral, riostras, zapatas), estructura de acero, forjados, salón. La fase 3 («consolidación y recrecido») cambia | `docs/16_ideas_de_obra_referencia.md` y el orden de obra del primer borrador (`dossier_obra.pdf`, hoja 6) |
| **PL-06** distribución y superficies | Plantas, alzados y sección nuevos: salón cerrado, distribución de la v8 (o la opción elegida), cubierta plana con paneles | `lamina_A1_v8_distribucion.dxf`, `planta_baja_v8.dxf`, `planta_alta_v8.dxf`, `seccion_A_v8.dxf`, `seccion_B_v8.dxf`, cuadro del apartado 2 |
| **PL-07** cotas y carpintería | Cotas nuevas, memoria de carpintería (puertas de seguridad, cristalera de aluminio al patio, ventanas con asiento), detalle de fachada | `pedido_proveedores.xlsx` (huecos), planos `lamina_A1_v8_*`, `docs/03_envolvente.md` |
| **PL-08** fontanería y ventilación | Red nueva (baños agrupados, aerotermia, depósito, paneles solares) | `docs/02_instalaciones.md`, `instalaciones.png` |
| **PL-09** saneamiento | Colector Ø150, arquetas, fosa séptica y pozo filtrante con posición y capacidad | `docs/18_fosa_septica_y_pozo_filtrante.md`, `fosa_septica_esquema.png`, `pozo_filtrante_5m.png` |
| **PL-10** electricidad | Circuitos nuevos, aerotermia, paneles solares (7,2 kWp), electrificación elevada de 9,2 kW | `docs/02_instalaciones.md`, `cubierta_solar.png` |
| **PL-11** cimentación y estructura | Cimentación nueva (zapatas, riostras, zanja perimetral), pilares y vigas de acero en lugar del muro central, forjados, zunchos, escalera de hormigón y losa sobre el salón | `cimentacion_planos.png`, `cimentacion_anillos.png`, `lamina_A1_v8_estructura.dxf`, `estructura_planos.png`, `memoria_estructura.md`, `19_comprobacion_cimentacion.md` |

## 4. Lo que condiciona el proyecto adaptado
1. **Estado de los muros** que quedan, y qué ha caído exactamente (fotos y medidas).
2. **Elección de la distribución de la planta baja** (A, B, C, C2, D o la económica).
3. **Estudio geotécnico**: el 130 kPa de PL-11 es supuesto. Recomiendo una calicata en una zapata y otra en el pozo filtrante, el mismo día.
4. **Cálculo de la estructura** de acero y de la losa sobre el salón (5,75 m), con ficha del fabricante, por un técnico competente.
5. **Fosa y pozo filtrante**: posición, capacidad y autorización de vertido.
6. **Comunicación con el arquitecto** sobre qué documentación necesita (modificado o proyecto nuevo).

## 5. Orden que propongo
1. **Asegurar y documentar** los muros: apeos, fotos y medidas, sin retirar escombros todavía.
2. **Avisar al arquitecto** y ver con él cómo se adapta el proyecto.
3. **Catas y estudio geotécnico**, y ver las cimentaciones bajo los muros caídos.
4. **Cálculo de la estructura** con la realidad de obra.
5. **Proyecto adaptado** con las láminas de la tabla anterior.
6. **Pedidos de hierro** (el Pedido 1 sigue valiendo para la parte de cimentación que no depende de las catas) y de las vigas de acero.
