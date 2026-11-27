# Zunchos que hay en el suelo (croquis y fotos del propietario, 27-11-2026)

Plano: `cimentacion_zunchos_en_obra.png` (`python zunchos_en_obra.py`). Montado con las cifras del croquis; **no está a escala exacta**, y la posición del zuncho central N-S y las medidas del saliente son aproximadas.

## 1. Lo que dice el croquis (largo total de cada zuncho, en m)
| Zuncho | Largo | Dato |
|---|---|---|
| Lado sur (E-O) | 9,20 | croquis |
| Zuncho central E-O (llega hasta el saliente) | 11,55 | croquis |
| Lado norte del bloque (E-O) | 9,27 | croquis |
| Lado oeste (N-S) | 8,80 | croquis |
| Zuncho central N-S (4,20 + 4,60) | 8,80 | croquis |
| Lado este (N-S) | 8,90 | croquis |
| Salón, lado oeste | 6,70 | croquis |
| Salón, lado este | 6,70 | croquis |
| Salón, lado norte | 6,30 (5,70 entre zunchos) | croquis |
| Saliente, lado este (N-S) | ≈ 3,00 | estimada del primer croquis |
| Saliente, lado norte (E-O) | ≈ 2,28 | estimada (11,55 − 9,27) |
| **Total** | **≈ 81,5 m** | 76,2 m de croquis + 5,3 m estimados |

Marcas «X» del croquis: 13, en las esquinas, los cruces y la mitad de los lados del salón. Las leo como **pilares** («pies»); pendiente de confirmar.

## 2. Qué se ve en las fotos
- **Cajas de armadura en zanjas estrechas**: cuatro barras corrugadas longitudinales (dos arriba y dos abajo, a mi ver) con cercos más finos cada 25–30 cm. Sección aproximada de 25 × 30 cm. **No sé los diámetros**; las barras parecen Ø12 o Ø14 y los cercos Ø6 u Ø8.
- **Pilares en los cruces**: cuatro barras verticales gruesas, de 1,5–2 m, en los cruces, con pequeñas patillas en L entre las cajas.
- **Restos de armaduras viejas oxidadas** al pie de los muros de los vecinos: cercos de un pilar anterior.
- **Muro de tapial de la izquierda**: la base está recrecida con mortero proyectado y malla, con barras verticales que salen de ella.
- **Armaduras apoyadas en el terreno**: en varias fotos las cajas descansan sobre el suelo o sobre piedras, sin calzos visibles.
- **Esquina del fondo**: una zanja cierra un recinto pequeño con su caja alrededor.

## 3. El hierro que representan (según el armado)
| Armado | kg/m | Hierro total para 81,5 m | Barras de 12 m | Cercos |
|---|---|---|---|---|
| **Lo que parece verse**: 2Ø12 + 2Ø12, cercos Ø6 cada 25 cm, ≈ 25 × 30 | 4,4 | ≈ 363 kg | 30 de Ø12 | 354 de 1,01 m |
| 2Ø16 + 2Ø16, cercos Ø8 cada 20 cm, ≈ 25 × 30 | 8,3 | ≈ 677 kg | 30 de Ø16 | 440 de 1,01 m |
| Z-1 del proyecto: 4Ø12 + 4Ø12, cercos Ø8 cada 20 cm, 40 × 30 | 9,7 | ≈ 790 kg | 60 de Ø12 | 440 de 1,31 m |
| De `docs/10`: 4Ø16 + 4Ø16, cercos Ø8 cada 15 cm, 40 × 40 | 16,0 | ≈ 1.300 kg | 60 de Ø16 | 583 de 1,27 m |

Incluye +10 % en barras por solapes y esquinas, y +5 % en cercos.

## 4. Frente a lo que habíamos calculado
- **Longitud**: el Pedido 1 (`pedido_1_hierro_cimentacion.xlsx`) cuenta 64,5 m de zunchos (30,6 m de riostras + 33,9 m de zanja perimetral), solo para el bloque principal. Lo que hay en el suelo son **81,5 m**: unos **17 m más**, sobre todo el rectángulo del salón (19,7 m), que el pedido no incluía.
- **Distribución**: la nuestra tenía tres riostras N-S (x = 3,10; 5,55; 7,20) y dos E-O; la real tiene **un zuncho N-S central**, los dos laterales, **tres E-O** (sur, central y norte), el salón y el saliente. Los pilares de acero HEB 120 de nuestro modelo no coinciden con las marcas X del croquis.
- **Armado**: lo que parece verse (4 barras) es **mucho más ligero** que el de `docs/10` (8Ø16) y que el Z-1 del proyecto (8Ø12). Antes de hormigonar, el técnico debe decir si es suficiente.
- **Dimensiones**: el bloque del croquis (9,20–9,27 × 8,80–8,90 m) es unos 0,2–0,4 m mayor que los ejes de nuestro modelo (unos 9,0 × 8,4 m con muros de 55 cm). Es poco, pero hay que ajustar el modelo cuando pases los espesores de los muros.

## 5. Cosas a revisar antes de hormigonar
1. **Calzos**: las cajas tienen que quedar elevadas del terreno. PL-11 pide 80 mm contra el terreno y 40 mm sobre hormigón de limpieza. Con 25 cm de ancho, 80 mm por cada lado dejan 9 cm de núcleo: o se encofra o se pone hormigón de limpieza y calzos.
2. **Solapes y anclajes**: PL-11 da, para B-500S, Ø12: 43 cm arriba y 30 cm abajo; Ø16: 57 y 40 cm. Empalmar alternando y en tramo recto. En los cruces, las barras de una caja deben entrar en la otra con patilla.
3. **Pilares**: las barras verticales de los cruces tienen que arrancar dentro de la caja, con cercos, y llegar a su altura de anclaje.
4. **Armaduras oxidadas viejas**: si se reutilizan, que las apruebe el técnico.
5. **Recrecido del tapial con mortero y malla**: no sé si lo ha definido el técnico; conviene enseñárselo.
6. **Hormigón**: HA-25/F/32/XC2 en cimentación, HM-20/F/32/I en limpieza (PL-11).
7. **Bataches**: hormigonar por tramos alternos junto a los muros que siguen en pie (`cimentacion_bataches.png`).

## 6. Lo que necesito de ti
1. **Diámetros** de las barras y de los cercos, y la **sección** de las cajas.
2. **Qué son las X**: ¿pilares? ¿De qué (hormigón o acero)?
3. **Espesores de los muros** (los que dijiste que me pasarías).
4. **Hierro ya comprado** (barras y cercos), para calcular lo que falta.

## 7. Espesores de los muros (croquis con leyenda, 27-11-2026)
Leyenda del propietario: rayado = **ladrillo de 14 cm**; trazo macizo = **ladrillo de 29 cm**. Mi lectura del croquis:

| Espesor | Muros | Largo aproximado |
|---|---|---|
| **14 cm** | Lado sur; lado oeste; lado este, tramo de 4,10 m al sur del saliente; lado este del saliente | ≈ 25,1 m |
| **29 cm** | Muro central E-O (11,55 m, incluye el lado sur del saliente); muro norte al oeste del salón (≈ 2,97 m); lados oeste y este del salón (6,70 m cada uno); lado este entre el saliente y el salón (≈ 1,80 m); lado norte del saliente (≈ 2,28 m) | ≈ 32,0 m |
| Sin marcar | Lado norte del salón; boca del saliente y el tramo norte entre el salón y el este | |

**El croquis cuadra con estos espesores**: interior 8,90 + 2 × 0,14 = 9,18 m (zuncho sur: 9,20); lado oeste 8,40 + 0,14 + 0,29 = 8,83 m (zuncho oeste: 8,80); salón 5,70 + 2 × 0,29 = 6,28 m (zuncho norte: 6,30). Es decir, **las longitudes de los zunchos son las medidas exteriores de los muros**.

**Lo que cambia**:
- El modelo usaba **55 cm** en la casa y 25 cm en el salón. Las medidas reales son un bloque exterior de unos **9,20 × 8,80 m** y un interior de 8,90 × 8,40 m (≈ 74,8 m²), más el salón (≈ 40 m² de interior) y el saliente (≈ 1,9 × 3,0 m). Hay que rehacer el modelo con ellas.
- Con muros de 14 y 29 cm, **los zunchos y los pilares (las X) son la estructura** y los muros son cerramiento; los de 14 cm no pueden cargar forjados por sí solos.
- **Corrijo un dato mío**: la esbeltez de 10–11 que te di para los muros en pie era con 55 cm. Con 29 cm es de unas 21 (6 m de altura) y con 14 cm, de unas 43. Si los muros que siguen en pie tienen esos espesores, están todavía más sueltos de lo que te dije.

**Pendiente de confirmar**: si el rayado y el macizo son el espesor de los muros que **siguen en pie** (o fueron), o el de los muros **por construir**; el espesor real del muro sur y de los laterales que se ven en las fotos; y si el lado norte del salón llevará 29 cm.

## 8. Distribución interior (croquis con leyenda y habitaciones, 27-11-2026)
Plano: `plano_realidad_27nov.png` (`python plano_realidad.py`). Esquema con las cifras del croquis; las posiciones de los tabiques son aproximadas y faltan los huecos.

Leyenda completa del propietario: rayado = ladrillo de 14 cm; macizo = ladrillo de 29 cm; rectángulo vacío = **ladrillo de 7 cm** (tabiques).

Lo que leo:
- **Mitad sur del bloque** (entre el muro sur y el muro central): dos estancias separadas por un **tabique de 7 cm** en el zuncho central N-S (4,20 m): **«b1»** al oeste y **«Cocina»** al este. Una flecha del croquis apunta a la unión del tabique con el muro central; no sé si marca una puerta.
- **Mitad norte del bloque** (entre el muro central y la línea norte): al oeste, un **rectángulo largo de tabiques de 7 cm** de 4,00 m de largo, pegado al muro oeste (la cota «400»); en el centro, un **recinto de tabiques de 7 cm** sin etiqueta, junto al zuncho central N-S (el de 4,60 m). El resto está abierto hacia el salón y el saliente.
- **Salón**: muros de 29 cm al oeste y al este; el lado norte sin marcar, con unos trazos finos y un cuadrado macizo que no sé interpretar (¿pilar, hueco o puerta?).
- **Muro sur**: el rayado lleva marcas verticales a lo largo, que leo como huecos de ventanas y puertas.

**Frente a nuestro diseño (v8)**: la distribución es distinta. En la v8, la cocina está en el centro con la escalera al este, el dormitorio principal con vestidor y baño al oeste y el baño grande en el saliente. Aquí hay «b1» y «Cocina» en el frente sur y recintos de tabique en la parte central.

**Pendiente de confirmar**: qué es «b1» (¿baño 1?, ¿b = baño?), qué son el rectángulo de 4,00 m y el recinto central, si la flecha es una puerta, qué marcas hay en el lado norte del salón, y dónde van las escaleras. La planta alta no está en ningún croquis.
