# Revisión completa: qué se ha optimizado y qué queda por decidir (12-10-2026)

He repasado planta baja, planta alta, estructura, instalaciones y costes de la versión v6. Las correcciones claras ya están hechas en el plano, el modelo 3D y los DXF. Las que cambian el diseño las dejo como opciones para que decidas.

## 1. Corregido ya

| Qué | Antes | Ahora | Por qué |
|---|---|---|---|
| Pilar de acero en el hueco de la cocina | El pilar de x = 7,20 caía en medio del paso a la cocina (6,50–8,00) | Paso movido a 7,40–8,90; el pilar queda dentro del tabique | No se puede dejar un pilar en una puerta |
| Pilar en el cristal del despacho | La línea de vigas x = 5,30 ponía un pilar en el cristal fijo del despacho | Línea movida a x = 5,55: el pilar queda en la esquina del despacho y, al fondo, en el tabique entre dormitorio 2 y cocina | Pilares escondidos en tabiques, no en huecos |
| Luces de viguetas de la memoria | Memoria calculada con luces 2,55/2,20/1,90/1,80 m que ya no eran las reales | Luces reales 2,83/2,45/1,65/2,08 m | Honestidad del cálculo: la viga de borde del saliente pasa de HEB 140 a **HEB 160** y la zapata de 1,30 a **1,50 m** (con los 130 kPa de PL-11) |
| Isla de cocina | Isla de 1,8 × 0,8 en una cocina de 2,6 m de ancho: dejaba pasos de 45 cm | Cocina en U (sur, este y un tramo oeste), pasillo central de 1,35 m | Una isla necesita 90 cm por cada lado: no cabe |
| Escalera | 16 contrahuellas de 20,4 cm (> 20 cm del CTE uso restringido) | 17 contrahuellas de 19,2 cm, huella 24 cm | Cumplimiento |
| Chimenea | En el rincón que ahora es el despacho | Esquina oeste del salón, humero por la terraza | Petición tuya |

Acero total: 3.698 kg (antes 3.628: +70 kg por la viga del saliente, que estaba infravalorada). Sigue siendo −45 % frente al primer diseño.

## 2. Comprobado y descartado (no mejora)

- **Dos líneas de vigas en vez de tres** (x = 3,10 y 6,35): ahorraría ≈ 550 kg de acero, 2 pilares y 2 zapatas (≈ 2.000–3.000 €), pero el pilar central caería en medio del paso abierto entre la sala de estar y el salón (5,70–7,05) y las vigas HEB 140 quedarían al 90 % de su capacidad. No lo recomiendo salvo que se acepte un pilar visto en ese paso.
- **Mover la escalera**: ni la recta ni la en L ahorran superficie; la U actual comparte bajantes con los baños y sube a la sala familiar (ver `06_escalera.md`).
- **Pasillo de entrada de 1,45 m**: bajarlo a 1,20 m daría 1,9 m² al salón, pero el murete bajo ya hace que el pasillo se viva como parte del salón. Lo dejo.

## 3. Opciones que cambian el diseño (decides tú)

| Opción | Efecto | Mi recomendación |
|---|---|---|
| **A. Reequilibrar los dormitorios de arriba**: el Dormitorio 2 (17,2 m²) es mucho mayor que el 1 (10,9 m²). Mover el tabique del Dormitorio 1 de x = 3,35 a 3,95 y el del Dormitorio 2 a 4,35 | Dorm. 1 ≈ 13,2 m², Dorm. 2 ≈ 14,8 m², Dorm. 3 igual | Sí: dormitorios más parejos sin coste |
| **B. Segundo baño arriba**: tomar 3 m² del Dormitorio 2 para un baño en suite, pegado al tabique del Dormitorio 3 | Dorm. 2 ≈ 12 m²; una bajante más | Solo si lo necesitáis; cuesta 3.000–5.000 € |
| **C. Armarios empotrados** en Dormitorio 2 (PB) y en los tres de arriba, de 60 cm, en los tabiques | Pierden 1,2–2,4 m² cada uno; ahorro frente a armarios de mueble | Sí, al menos arriba |
| **D. Terraza del salón (42,7 m²)**: cubrir la mitad con pérgola bioclimática o paneles solares elevados | Sombra en verano, +6–10 kWp si son paneles | Pérgola de aluminio: la puedes hacer tú |
| **E. Cristalera norte de 4,00 m**: reducir a 3,00 m y meter 1 m de muro para el sismo | Menos luz, más muro E-O (el sentido más débil) | Pedir cálculo sísmico antes de decidir |

## 4. Lo que no se puede optimizar sin datos

- **Geotécnico**: zapatas, zuncho y cimentación del salón dependen de él. Las zapatas de 1,40 m son para 150 kPa supuestos.
- **Sismo real de Albox** (NCSE-02): el margen E-O es justo; decide si hacen falta cruces o pantallas.
- **Cimentación existente de los muros de 55 cm**: catas.


## Actualización 12-10-2026 (medianeras, PL-11 y paso a la terraza)
- **Paso a la terraza**: el cierre de la planta alta seguía sin salida porque quedaba **una tira de 5 cm de parapeto** a lo largo de todo el frente y la corredera caía sobre el **pilar de x = 5,55**. Ahora el frente del parapeto está abierto, la corredera es de **1,42 m entre los pilares x = 5,55 y 7,20** y el paso queda libre (comprobado con volúmenes en el modelo: sin intersección con muros, parapeto, tabiques ni acero).
- **Casas vecinas pegadas (este y oeste)**: quitadas todas las ventanas de esas paredes; la cocina gana una ventana sobre la encimera; Dormitorio 1 gana una cristalera al final de la sala hacia la terraza (el muro de fachada se abre desde x = 2,95).
- **Instalaciones**: agua y luz por el sur, fosa al norte (como PL-08/09/10); la unidad exterior de la aerotermia ya no está dentro del baño grande (error mío); tras las fotos pasa a la cubierta; módulo hidráulico y acumulador en un armario bajo el segundo tramo de la escalera.
- **PL-11 del arquitecto**: su estructura es bastante más pesada que la mía (HEB-160 y HEB-220 donde yo uso HEB 120–140, IPE-240 sobre la terraza, muro central existente). El diseño del propietario sustituye el muro central por vigas de acero, así que **ambas estructuras no son comparables**: la mía es una propuesta de ahorro que **debe calcular un ingeniero** antes de ejecutarla.
- **Terreno**: se usa 130 kPa (PL-11) en vez de 150 kPa supuestos.
