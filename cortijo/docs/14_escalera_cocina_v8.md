# v8 (13-10-2026): escalera movida, cocina abierta a la sala y puertas libres

Petición del propietario: desde la sala de estar tiene que haber acceso libre a la cocina, y la escalera estorbaba en medio.

## 1. Qué estaba mal (error mío en la v7)
En la v7 la escalera ocupaba todo el bloque x 7,25–9,00 × y 8,95–11,75 y su meseta (maciza, a 1,73 m) cerraba el extremo sur. Resultado:
- La **puerta de la cocina** daba a esa meseta: la cocina no tenía acceso desde la sala.
- La **puerta del baño grande** daba a los primeros escalones de subida: tampoco se llegaba.
- El baño de arriba tenía el mismo problema (su puerta daba al hueco).

Para no depender de la vista, he escrito `verificar_circulacion.py`: corta el modelo (`casa_v8.glb`) a varias alturas entre 0,30 y 2,00 m sobre cada suelo, quita paredes, escalera, muebles, pilares y huecos, y comprueba qué estancias quedan unidas por un paso de al menos 0,70 m de ancho. **Con el modelo v7 la comprobación falla** (cocina y baño grande aislados); con v8 pasa en las dos plantas, terraza incluida.

La misma comprobación sacó otros fallos de mobiliario que ya estaban en la v7 y que he corregido:
| Fallo | Arreglo |
|---|---|
| Inodoro de la suite justo detrás de la puerta del vestidor | Inodoro contra el muro norte y lavabo doble contra el muro este |
| Armario del vestidor delante de la puerta a la suite, y banco delante de la del baño | Armarios al oeste y junto a la puerta de la sala; puertas libres |
| Sofá de la sala familiar a 25 cm de las puertas de los dormitorios de arriba | Sofá de 1,20 m contra el muro este |
| Puerta del dormitorio 3 de arriba sobre el pilar de x = 5,55 y detrás de un armario | Puerta en x 5,80–6,60 |
| Puerta del dormitorio 2 de arriba cruzando el tabique hacia el dormitorio 3 | Tabique en x 4,85 y puerta en x 4,05–4,85 |

## 2. Qué cambia
| | Antes (v7) | Ahora (v8) |
|---|---|---|
| Escalera | Pie en y = 8,95, huella 24 cm, meseta maciza al sur | Pie en **y = 9,65**, huella **22 cm**, contrahuella 19,2 cm, tramos de 87,5 cm, meseta de 88 cm; el tramo de vuelta es una losa escalonada (queda un **paso libre bajo la escalera**) |
| Entrada (PB) | 1,9 m² | **3,1 m²**, con la puerta del baño grande y el pie de la escalera |
| Entrada (PA) | 1,9 m² | **3,5 m²**, con la puerta del baño de arriba; el hueco en L (el suelo de arriba tapa los 5 primeros escalones, con 2,08 m libres) |
| Cocina | Al este (x 6,40–9,00), cortada por la escalera | **En el centro (x 3,75–6,15), 9,4 m², abierta a la sala por un paso libre de 1,60 m** entre los pilares x = 3,10 y x = 5,55 (se le puede poner una corredera). Puerta de servicio y ventana al sur |
| Dormitorio 2 (PB) | Centro, 9,9 m² | **Este, 9,7 m²**, en L (rodea el final de la escalera), puerta desde la sala (x 6,35–7,15), armario en el rincón |
| Entrada ↔ sala | Paso de 0,93 m | **Paso libre de 1,58 m** |
| Armario técnico (módulo hidráulico y ACS 200 L) | Bajo el primer tramo, junto a la entrada | Bajo el tramo de vuelta, al fondo del paso bajo la escalera (se entra desde la entrada) |
| Dormitorios de arriba | 13,2 / 16,0 / 16,6 m² | 13,2 / **16,8** / **14,8** m² (el dormitorio 3 en L, por el final del hueco) |
| Paneles solares | 17 (7,6 kWp) | **16 (7,2 kWp)**: uno tapaba el lucernario de la escalera |
| Aerotermia (unidad exterior) | y = 12,40 | y = 12,55, junto al lucernario |

Escalera (CTE DB-SUA 1, uso restringido; confirmar en el texto): 17 contrahuellas × 19,2 cm, huella 22 cm (2c + h = 60,4 cm), ancho 87,5 cm, meseta 88 cm, barandilla de 1,00 m. Altura libre bajo el tramo de vuelta ≥ 2,05 m hasta y = 10,85.

## 3. Puntos que conviene confirmar
- **Estructura**: el hueco de la escalera es ahora en L y llega hasta y = 12,29. Los **brochales** de los forjados y la cubierta alrededor del hueco los define el ingeniero (en la v7 pasaba lo mismo con otro tamaño). Las vigas HEB y los pilares no cambian de sitio.
- **Cocina junto a la suite**: el tabique de la cocina da al cabecero de la cama. Pon allí la nevera y las columnas de despensa, y hazlo de 15 cm con lana mineral (acústico).
- **Nicho de la CGP**: queda entre la ventana de la cocina y la del dormitorio 2 (x ≈ 6,2); confirmar la posición real.
- **Dormitorio 2 en L**: pierde 1 m² por el final de la escalera; es el precio de tener el baño grande y la cocina accesibles.
- El baño grande tiene la puerta de 0,75 m (el máximo que cabe junto al pie de la escalera); para 0,80 m habría que mover 5 cm el pie.
