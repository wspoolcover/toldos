# Distribución deseada sobre la obra real (croquis del propietario, 27-11-2026)

Archivos: `distribucion_deseada_27nov.png` (plano), `distribucion_deseada_3d.png` (maqueta seccionada a 1,5 m), `distribucion_deseada.step` y `.glb` (modelo 3D), `distribucion_deseada.dxf` (plano por capas). Todo sale de `python distribucion_deseada.py`, que usa las cifras de `plano_realidad.py` (zunchos y muros por espesor).

**Aviso sobre FreeCAD**: no se puede instalar en este entorno. El modelo está hecho con CadQuery (mismo núcleo OpenCascade que FreeCAD). El `.step` se abre en FreeCAD con Archivo → Abrir; trae siete piezas con color (solera, zunchos, muros de 14 cm, muros de 29 cm, tabiques de 7 cm, escalera, mobiliario). Es un esquema «para hacernos una idea», no al milímetro: los muros y zunchos son los de obra; los tabiques, puertas, ventanas y muebles son de diseño.

## 1. Lo que he recogido de tu mensaje y del croquis
| Pediste | Cómo queda |
|---|---|
| Dormitorio suite arriba a la izquierda, con vestidor S y baño | Suite 17,1 m² al suroeste. Vestidor (5,9 m²) y baño de la suite (6,9 m²) en el oeste de la mitad norte del bloque, uno detrás del otro. **Desde la entrada (el vestíbulo del pasillo) se va al dormitorio** (D1, en el muro central, abre hacia el dormitorio) **y al vestidor** (D2, en el tabique de x = 3,10 m). **Del dormitorio al vestidor hay una puerta corredera** (D7, en el muro central, colgada en el lado del dormitorio). Del vestidor se pasa al baño (D4). Cama de 1,80 × 2,00 m con el cabecero en el muro oeste |
| Baño de dormitorio «decente, no pequeño»; vestidor «apropiado» | 3,00 × 2,31 m (6,9 m²) y 3,00 × 1,96 m (5,9 m²). Ducha de 0,90 × 1,50 m, lavabo de 1,40 m, y armarios en el oeste, en el sur y en un tramo del este del vestidor, con paso de 0,8 m hasta las puertas del dormitorio y del baño |
| Oficina pequeña, del tamaño del baño, «partiendo la distancia» | **Independiente**: puerta propia (D3) desde el vestíbulo, a la izquierda (x = 3,30 a 4,10 m), sin pasar por el vestidor. 2,23 × 3,16 m = 7,0 m², como el baño de la suite (6,9 m²). **Movida 1 m al este** hacia el comedor-distribuidor: el tabique que la separa del vestidor y del baño está a 3,10 m del muro oeste y el de su lado este, a 5,40 m |
| Comedor en el distribuidor | Mesa de 1,60 × 0,90 m con 6 sillas entre la escalera y el baño grande, a 0,9 m del lado este y sin tapar la salida del pasillo bajo la escalera ni la puerta de la cocina (D5) |
| Baño grande: el que hay, el del saliente | 2,18 × 2,71 m = 5,9 m², con ducha, inodoro y lavabo doble. Puerta en su lado oeste |
| Cocina con la salida actual (P1) y ventana; barra o mesita bajo la ventana de la izquierda | Cocina 18,7 m². P1 de doble hoja (1,10 m) en el extremo este del muro sur. V1 (1,30 m) a la izquierda, con una barra de 1,60 m y tres taburetes debajo. Encimera en L (2,05 + 2,85 m) y columna de nevera |
| Entrada por debajo de la escalera, hacia dormitorio, vestidor, oficina y baño | Puerta de entrada al norte del salón, en su lado este. Pasillo de entrada de 1,3 m a lo largo del lado este del salón y paso al comedor-distribuidor. Desde ahí, un pasillo de 1,10 m **bajo el tramo alto de la escalera** llega a una **puerta (D8) que cierra el pasillo** en x = 4,20 m. Detrás queda la entrada privada: puertas al dormitorio, al vestidor y a la oficina. Del vestidor se pasa al baño |
| Chimenea en el salón; sofá en C invertida | Chimenea de esquina (suroeste del salón, junto al bloque) con su conducto en el muro de 29 cm. Sofá en C abierto hacia el oeste, con mueble de TV en el muro oeste |

## 2. Superficies útiles (entre caras de muro)
| Estancia | m² | Estancia | m² |
|---|---|---|---|
| Dormitorio suite | 17,1 | Baño grande | 5,9 |
| Vestidor | 5,9 | Cocina | 18,7 |
| Baño de la suite | 6,9 | Comedor / distribuidor | 11,6 |
| Oficina | 7,0 | Pasillo bajo la escalera | 3,6 |
| Escalera | 4,8 | Salón | 38,7 |
| **Total planta baja** | **120,3** | | |

La v8 daba 113,9 m² útiles en planta baja. Aquí sube porque el bloque real (9,20 × 8,80 m) y el salón (6,0 × 6,4 m interior) son más grandes que los del modelo. La planta alta no está diseñada.

## 3. Ladrillo y muros que salen de este diseño
| Elemento | Longitud | Superficie |
|---|---|---|
| Tabiques de 7 cm (7 tramos, altura 3,0 m) | 20,5 m | 61,5 m² brutos, **52,9 m² netos** de las 5 puertas interiores (D2, D3, D4, D6, D8) |
| Muro de 29 cm que **no está en tu croquis** (línea norte del bloque de x = 2,97 a 7,30 m) | 4,3 m | 13,0 m² |
| Muro de 29 cm del lado norte del salón (sin marcar en el croquis; lo he supuesto de 29 cm) | 6,3 m | 18,9 m² |

Los tabiques salen de la cara del muro al otro, así que están descontados los espesores. Los huecos en muros de obra: V1, V2 y P1 en el muro sur de 14 cm; D1, D5 y D7 en el muro central de 29 cm (necesitan dintel); la puerta de entrada en el muro norte del salón.

## 4. Cosas que hay que revisar (las he visto al dibujarlo)
1. **Altura bajo la escalera.** Con 18 contrahuellas de 18,1 cm, huella de 25,5 cm y losa de 22 cm, el hueco libre en el borde del pasillo (y = 5,45 m) es de unos **2,17 m**. Justo; hay que comprobar con el arquitecto la altura mínima de paso que se exige (no la he verificado). Se gana estrechando el pasillo bajo la escalera o con una losa más fina.
2. **Baños, vestidor y oficina sin ventana exterior.** El muro oeste y el este son medianeras y el norte da al salón. En el plano no hay ventilación natural en esas cuatro estancias: harán falta extractores y decidir la luz (una ventana alta hacia el salón en la oficina, vidrio en una puerta…).
3. **Tabiques de 7 cm en los baños.** No admiten rozas para las tuberías. Lo normal es poner las instalaciones por el tabique de 14 cm o por trasdós. Con 3,0 m de altura el arriostramiento en cabeza lo define el técnico.
4. **Tabique sobre el zuncho central** (decisión del propietario, 27-11-2026). Está en x = 4,40 m, que es la posición aproximada del zuncho en el croquis de medidas (sale entre 4,4 y 4,6 m). Con una medición real hay que mover ese tabique la diferencia. Con esto la suite queda en 17,1 m² y la cocina en 18,7 m². En la mitad norte el tabique de la oficina y la escalera están 1 m más al este (x = 5,40 m), **fuera del zuncho**: un tabique de 7 cm no lo necesita, pero el zuncho central pasa por debajo de la oficina y del pasillo.
5. **Escalera** (el propietario confirma el 27-11-2026 que sube hacia el sur; dibujada con 3 peldaños de arranque hacia el este, descansillo cuadrado y tramo recto de 13 peldaños hacia el sur): el tramo alto llega encima del pasillo y entra en la planta alta por el sur. Esa planta no está pensada.
6. **Chimenea**: el conducto sube por la esquina del salón a través de la terraza de encima. Hay que verlo con el diseño de la cubierta y de los paneles solares.
7. **Comedor-distribuidor de 11,6 m²** con la mesa y la circulación: la salida del pasillo bajo la escalera, la puerta de la cocina (D5), la puerta del baño grande (D6), el arranque de la escalera y el paso desde el pasillo de entrada. El paso libre junto a la mesa es de unos 0,9 m. Es ajustado para 6 sillas; con 4 sillas se despeja.

## 5. Lo que necesito de ti
1. ¿Qué quieres en la planta alta? La escalera sube hacia el sur (confirmado) y llega encima del pasillo.
2. ¿Ventanas o puertas acristaladas en el salón? Ahora solo hay la puerta de entrada.
3. ¿La línea norte del bloque y el lado norte del salón van de 29 cm?
4. ¿Qué es la línea diagonal dentro de la suite en tu croquis? No la he dibujado.
5. En tu plano marcaste con una raya roja el tabique entre el vestidor y el baño, a la altura de su puerta (D4). Lo he dejado como estaba. ¿Querías moverla, cerrarla o cambiarla?
6. La entrada tiene 1,07 × 1,10 m, con puertas al dormitorio, al vestidor y a la oficina y la puerta de cierre. Es justa. Si quieres más, se gana quitando la puerta del vestidor (D2) o ensanchando hacia el este.
