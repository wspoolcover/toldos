# Estructura barata y fuerte (proyecto personal, Albox)

Cifras del modelo. Los precios son de referencia de internet: pide presupuestos.

## Diseño actual
| Elemento | Solución |
|---|---|
| Terraza del salón (≈ 40 m²) | Forjado de vigueta pretensada y bovedilla de poliestireno (25+5)×71, vigueta T-2 |
| Forjado de la casa y cubierta (≈ 148 m²) | Forjado (17+5)×71, vigueta T-1, bovedilla de poliestireno, apoyado en las vigas de acero |
| Vigas largas norte-sur | 3 líneas de HEB 140 en una sola pieza continua, en forjado y en cubierta |
| Pilares | 6 × HEB 120 ocultos en muros y tabiques, con zapatas de 1,3 m |
| Fachada y saliente | Viga de fachada HEB 120 y viga de borde del saliente HEB 140 |
| Huecos | Dintel HEB 160 sobre la cristalera y 14 dinteles IPE 100/120 |
| Atado | Zunchos de hormigón en cada nivel y riostras entre zapatas |

Los datos de las viguetas salen de la [ficha técnica de Prearcon (T-18)](https://prearcon.com/pdf/VIGUETA%20T18.pdf). Cumplen con mucho margen en la casa (M/Mu 0,40) y con poco en el salón (0,96 con T-2; con T-3 hay margen). El fabricante debe confirmar la luz de 5,75 m del salón.

## Ahorro
- **Acero:** 6.668 kg (primer diseño) → **3.630 kg (−46 %)**, sin uniones ni placas.
- **Coste orientativo de acero más forjados** (sin zunchos, riostras ni cimentación): entre unos **19.000 y 36.000 €**, frente a **25.000-52.000 €** del primer diseño con acero y chapa colaborante. Ahorro estimado de **6.000 a 16.000 €**.
- Cálculo: acero 3,6 t × 2,4-5,5 €/kg ([CYPE](https://www.generadordeprecios.info/obra_nueva/Estructuras/Acero/Vigas/Acero_en_vigas.html), [preciom2](https://preciom2.com/guias/acero/)) más 188 m² de forjado a 55-85 €/m² ([preciom2](https://preciom2.com/guias/hormigon-estructuras/forjado-vigueta-bovedilla/)).

## Sismo (lo importante en Albox)
- La aceleración sísmica de Albox no estaba en la tabla que encontré (Almería capital: 0,14 g); usé 0,16 g como suposición. Hay que mirar el Anexo 1 de NCSE-02.
- Comprobación orientativa (cortante en la base de unos 770-965 kN): en la dirección norte-sur los muros trabajan a unos 0,08 MPa y en la este-oeste a unos 0,11 MPa. **Los dos están dentro del rango de una mampostería antigua en buen estado (0,05-0,15 MPa), pero sin mucho margen**: hay poco muro en el este-oeste porque el salón es acristalado y en el norte-sur los muros nuevos del salón son de solo 25 cm.
- No recortaría el refuerzo: cruces de acero en dos paños de la línea de fachada, pantallas de hormigón armado de 15-20 cm o mallazo con mortero. Lo decide un técnico con el cálculo sísmico.

## Muros laterales del salón (ladrillo de 25 cm, cimentación de 60 cm)
- La cimentación existente **cumple**: unos 40 kN/m de carga de servicio (forjado, muro y antepecho) sobre 0,60 m de ancho dan unos **67 kPa**, frente a 150 kPa supuestos. Falta el estudio geotécnico y confirmar que los 60 cm son de ancho.
- Muro de 25 cm entre cimentación y forjado (3,3 m): esbeltez 13, admisible con zuncho arriba. Llevará pilares de atado de hormigón de unos 25×25 cm en las esquinas y cada 3,5-4 m (unos 3 por muro lateral).
- Con muros de 25 cm el salón queda más ancho: unos 5,9 m interiores en la fachada. La cristalera pasa a 4,00 m y el pasillo de entrada a 1,45 m.

## Lo que no conviene tocar para abaratar
Zunchos, riostras, refuerzo este-oeste, pilares, zapatas, dinteles, uniones y las flechas. Sí se puede ajustar la variedad de perfiles, las mermas de corte y atornillar en obra en lugar de soldar.
