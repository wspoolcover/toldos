# Comprobación de la cimentación, tal como está en el proyecto (04-11-2026)

Qué he comprobado: el plano de cimentación (`cimentacion_plano.py`, `cimentacion_v7.dxf`), las cargas de `estructura.json`, la escalera del modelo v8 (`casa_v8.py`) y la circulación del modelo (`verificar_circulacion.py`). El cálculo es sencillo y orientativo (script: `comprobar_cimentacion.py`); **no sustituye al técnico**. Pedido de hierro resultante: `pdf/Pedido_1_hierro_cimentacion.pdf`.

## 1. Resumen
| | Resultado |
|---|---|
| Presión de las zapatas sobre el terreno | **Cumple**: como máximo 89 kPa (69 % de los 130 kPa del plano PL-11; 89 % si el terreno real fuera de 100 kPa) |
| Armado de la parrilla de las zapatas (Ø12 cada 15 cm) | **Cumple** con holgura: unas 6 veces lo que pide el cálculo simple |
| Armado de las riostras (4Ø16 + 4Ø16, cercos Ø8 cada 20 cm) | **Cumple** con mucho margen: el atado pide unos 90 mm² y hay 804 mm² por cara |
| Longitudes del pedido contra el DXF | **Coinciden**: riostras 30,6 m, 4 zapatas |
| Circulación del modelo v8 (sala, cocina, baños, dormitorios, escalera) | **Pasa** con 0,70 m de paso en las dos plantas |
| Zapatas de la línea y = 7,60 contra la cimentación existente | **Hay que resolver** antes de hormigonar |
| Colector Ø150 contra la zapata Z-2 y la riostra de y = 7,60 | **Hay que resolver** antes de hormigonar |
| Cimentación de la escalera | **Falta**: no está en el plano |
| Terreno: 130 kPa, cota de apoyo, nivel del agua | **Sin confirmar** (falta el estudio geotécnico) |

## 2. Lo que cumple
**Presión sobre el terreno** (cargas máximas de `estructura.json`: 245 kN de cálculo en los pilares de la línea y = 11,80 y 99 kN en los de y = 7,60; con peso propio y 0,40 m de tierra encima):

| Zapata | Carga de cálculo (kN) | σ (kPa) | % de 130 kPa | % de 100 kPa |
|---|---|---|---|---|
| Z-1 (x = 3,10; y = 11,80) | 245 | 89 | 69 % | 89 % |
| Z-1 (x = 3,10; y = 7,60) | 99 | 50 | 38 % | 50 % |
| Z-2 combinada (x = 5,55 y 7,20; y = 11,80) | 489 | 88 | 68 % | 88 % |
| Z-2 combinada (x = 5,55 y 7,20; y = 7,60) | 199 | 49 | 38 % | 49 % |

Si el terreno resultara peor de 90 kPa, las zapatas de la línea y = 11,80 tendrían que crecer. Por eso hace falta el estudio.

**Zapatas**: con el pilar más cargado, el vuelo desde la placa base es de 0,65 m y la presión de cálculo, 96 kPa. El cálculo pide unos 100–130 mm²/m y la parrilla Ø12/15 da 754 mm²/m.

**Riostras**: esfuerzo de atado orientativo de 0,16 × 245 = 39 kN, unos 90 mm². La cuantía mínima de referencia de una viga de 40 × 50 cm (unos 2,8 ‰) son 560 mm²; 4Ø16 da 804 mm² y 4Ø14, 616 mm². El armado de 4Ø16 es más fuerte de lo necesario, y con 4Ø14 solo se ahorrarían unos 100 kg. Lo dejo como está.

**Circulación del modelo v8**: sin cambios respecto a la v8; se puede pasar entre todas las estancias con un cuerpo de 0,70 m, y el paso libre bajo el tramo de vuelta de la escalera es de 2,08 m o más hasta y = 10,85.

## 3. Lo que hay que resolver antes de hormigonar
**a) Las zapatas de la línea y = 7,60 coinciden con cimentación existente.**

| Zapata nueva | Con la zapata corrida del salón (0,60 m, ya hecha) | Con la cimentación de los muros de 55 cm (ancho supuesto 1,10 m) |
|---|---|---|
| Z-1 (x = 3,10; y = 7,60) | 0,42 m² | 1,73 m² |
| Z-2 (x = 5,55 y 7,20; y = 7,60) | 0,99 m² | 3,51 m² |

En esa línea se quita el muro viejo entre x = 3,45 y x = 9,00 (5,55 m) y lo sustituyen la viga de fachada y los pilares. Pero su cimentación sigue enterrada justo donde van la riostra de y = 7,60 y las zapatas. El ancho de 1,10 m es una suposición del plano. Hace falta una cata para ver qué hay y a qué cota: o se hormigona la zapata nueva contra la existente con pasadores, o se desplaza, o se pica la existente. Lo decide el técnico con la cata.

**b) El colector Ø150 cruza la zapata Z-2 y la riostra de y = 7,60.** El colector baja por x = 5,90 hacia la fosa del norte y atraviesa 1,20 m de la zapata Z-2 y la riostra. Opciones: dejar un pasamuros Ø200 en la riostra y subir el colector por encima de la zapata, o bajar la cota de las zapatas, o mover el colector. Hay que decidirlo antes de colocar el hierro de esa zona.

**c) La escalera no tiene cimentación.** La escalera de hormigón de la v8 pesa unos 75 kN (7,7 t) con sus 3,1 m³. El carril este macizo apoya en el suelo sobre 2,3 m² (0,875 × 2,64 m), con unos 28 kPa de peso propio. La presión es baja, pero va sobre la solera, que no está pensada para eso: hace falta una losa o zapata reforzada bajo el carril macizo. La riostra de y = 11,80 pasa por debajo de la meseta y ayuda, pero no cubre el tramo. No está dimensionada: **queda pendiente de que el técnico la defina** (mallazo, canto y cota).

## 4. Datos que faltan
- **Estudio geotécnico**: el 130 kPa es el del plano PL-11 del arquitecto. Las fotos de octubre muestran una costra de arcilla o limo agrietada, que se hincha y se contrae. Lo ideal es una calicata en el sitio de una zapata y otra en el sitio del pozo filtrante, el mismo día.
- **Zapata corrida del salón**: hay que medir si los 60 cm son de ancho o de profundidad. Si fueran de profundidad, la presión de los muros del salón cambia.
- **Nivel del agua subterránea** y cota de apoyo (por lo menos 1,00 m bajo el terreno natural, en terreno firme).

## 5. Incoherencias en documentos antiguos
- **`dossier_obra.pdf`** (primer borrador) habla de 6 zapatas de 1,50 m y riostras de 40 × 40 con 4Ø12. Vale lo de `docs/10`: **4 zapatas** (2 de 1,60 × 1,60 y 2 combinadas de 3,25 × 1,60) y riostras de 40 × 50 con 4Ø16.
- **Pilares de atado**: el DXF dibuja 10 (los del salón); la imagen del plano, 22 (13 del salón y 9 de la casa); `docs/10` dice «≈ 20». El pedido los deja aparte.
- El plano y el DXF se llaman «v7»; los pilares y las zapatas son los mismos en la v8. Lo que cambió en la v8 es la escalera, y por eso falta el punto c.

## 6. Qué se puede pedir ya
**El hierro del Pedido 1** (zapatas y riostras): 22 barras de Ø12, 28 de Ø16 y 24 de Ø8 para cercos, unos 880 kg. Las cantidades no dependen de los tres puntos de arriba, salvo los cortes de las zapatas de la línea y = 7,60. Si quieres curarte en salud, pide esas barras sin cortar.

**Lo que no se debe hormigonar todavía**: la línea y = 7,60 (zapatas Z-1 y Z-2 de ese lado y su riostra), hasta resolver a) y b).
