# Predimensionado de estructura de acero (PRELIMINAR)

Acero S275JR (fy = 275 MPa), γM0 = γM1 = 1,05, ELU 1,35 G + 1,50 Q, flecha total L/300 y de sobrecarga L/400 (CTE DB-SE).

| Carga | G (kN/m²) | Q (kN/m²) |
|---|---|---|
| Forjado de la casa (planta alta) | 4.2 | 2.0 |
| Terraza transitable sobre el salón | 4.8 | 2.0 |
| Cubierta plana no transitable (piedra + paneles solares) | 5.5 | 1.0 (mantenimiento; nieve 0,5 supuesta) |

## Terraza sobre el salón: viguetas E-O (luz 5,75 m)
| Sección | Separación (m) | kg/m² | M/Mrd | Flecha total / límite (mm) |
|---|---|---|---|---|
| IPE 240 | 1.2 | 25.6 | 0.51 | 14.7 / 19.2 |
| IPE 220 | 1.0 | 26.2 | 0.54 | 17.3 / 19.2 |

## Terraza sobre el salón: alternativa de forjado de vigueta pretensada y bovedilla (datos de fabricante)

Ficha técnica de [Prefabricados Arcón, forjado T-18](https://prearcon.com/pdf/VIGUETA%20T18.pdf): forjado (25+5)×71, peso 3,71 kN/m² con bovedilla de hormigón o 2,51 con bovedilla de poliestireno. El fabricante debe confirmar la luz de 5,75 m con su ficha de autorización de uso.

| Forjado (25+5)×71 | Peso propio | G total | M/Mu | V/Vu | Flecha con fluencia / límite (mm) |
|---|---|---|---|---|---|
| bovedilla de hormigón, vigueta T-3 | 3.71 | 5.91 | 0.89 | 0.82 | 15.2 / 19.2 |
| bovedilla de poliestireno, vigueta T-2 | 2.51 | 4.71 | 0.96 | 0.78 | 12.7 / 19.2 |

Elegida: **(25+5)×71 con vigueta T-2 y bovedilla de poliestireno** (peso 2.51 kN/m², más ligera que la solución de acero con chapa). Reacción en cada muro ≈ 27 kN/m (con IPE 240 y chapa serían unos 27 kN/m).

Coste orientativo por m² (40 m²): acero (IPE 240 a 1.2 m: 25.6 kg/m² × 2.4-5.5 €/kg) + chapa colaborante 50-80 €/m² = **111-221 €/m²**; vigueta y bovedilla. ya con viguetas: **55-85 €/m²**. Ahorro estimado **1.1-6.6 mil €** y unos IPE 240: 1.023 kg de acero menos.

## Forjados de la casa y de la cubierta: vigueta pretensada y bovedilla (luz máx. 2,55 m)

Forjado (17+5)×71 con bovedilla de poliestireno, 2,02 kN/m² ([ficha Prearcon T-18](https://prearcon.com/pdf/VIGUETA%20T18.pdf)); vigueta T-1: Mu = 17,5 kN·m/m, Vu = 21,6 kN/m, EI fisurada = 6,21 MN·m²/m. Las viguetas apoyan en el ala inferior de las vigas HEB y el hormigón las cubre, así que las vigas no se ven por debajo.

| Forjado | G total | M/Mu | V/Vu | Flecha con fluencia / límite (mm) |
|---|---|---|---|---|
| Casa (planta alta) | 4.22 | 0.40 | 0.51 | 1.3 / 8.5 |
| Cubierta plana (piedra y paneles solares) | 5.52 | 0.42 | 0.53 | 1.6 / 8.5 |

## Vigas N-S del forjado (líneas x = 3,10; 5,30 y 7,20; una pieza continua de dos vanos 4.20 + 3.95 m; ancho tributario 2.38 m)

Sección: **HEB 140**. M/Mrd = 0.68 en el apoyo central; V/Vrd = 0.37; flecha 8.0 mm (límite 14.0). Reacción en el pilar central ≈ 108 kN. Al ser continua trabaja mejor que dos vigas sueltas y admite un perfil menor.

Vigas N-S de cubierta (continuas): **HEB 140** (M/Mrd 0.70, flecha 8.4/14.0 mm).

## Dintel sobre la cristalera (luz 4.40 m; muro de ladrillo de 25 cm y antepecho 7.7 kN/m)

Sección: **HEB 160** (M/Mrd 0.40, flecha 10.4/14.7 mm). Se aloja en el espesor del muro con placas de apoyo de 0,20 m en cada extremo.

## Viga de fachada (sustituye al muro entre salón y casa, en cada planta; luz 2.30 m entre pilares)

Sección: **HEB 120** (M/Mrd 0.25, flecha 2.4/7.7 mm). Cada planta lleva su viga; los pilares HEB 120 en x = 3,10; 5,30 y 7,20 quedan vistos en el borde del salón.

## Viga de borde del saliente del baño (a x = 9,15, en forjado y en cubierta; luz 3.70 m entre muros)

Falta ese muro entre la casa y el saliente, así que una viga recoge el borde de la casa y las viguetas del saliente. Sección: **HEB 140** (forjado M/Mrd 0.54, cubierta 0.56).

## Dinteles de puertas y ventanas en muros de mampostería
| Hueco (m) | Luz de cálculo | Perfil | M/Mrd |
|---|---|---|---|
| ≤ 1.0 | 1.4 | IPE 100 | 0.65 |
| ≤ 1.2 | 1.6 | IPE 100 | 0.85 |
| ≤ 1.4 | 1.8 | IPE 120 | 0.70 |
| ≤ 1.6 | 2.0 | IPE 120 | 0.86 |

## Pilares HEB (6 uds., x = 3,10; 5,30 y 7,20; y = 7,60 y 11,80; ocultos en muros y tabiques; altura ≈ 5,6 m)

Carga axial de cálculo máx. ≈ 221 kN (pilar central) y ≈ 90 kN (pilar sur). Sección: **HEB 120**, N/Nb,Rd = 0.60 (pandeo eje débil, Lcr = 3,3 m).

Zapatas aisladas bajo pilares (σ adm. supuesta 150 kPa, **pendiente de estudio geotécnico**): ≈ 1.3 × 1.3 m, canto 0,60 m.

## Cimentación existente de los muros del salón (ladrillo de 25 cm, zapata de 60 cm)

Carga de servicio por metro de muro ≈ 40 kN/m (forjado 19 + muro y antepecho 19 + zuncho) → presión sobre el terreno ≈ **67 kPa** con 0,60 m de ancho, frente a 150 kPa supuestos: **cumple** con margen si el terreno es normal (falta el estudio geotécnico). Si los 60 cm fueran de profundidad y no de ancho, habría que medir el ancho.
Muro de ladrillo de 25 cm y 3,3 m de altura entre cimentación y forjado: esbeltez 13, admisible con zuncho arriba. Pilares de atado de hormigón (unos 25×25 cm) en las esquinas y cada 3,5-4 m (≈ 3 por muro lateral) para el sismo.

## Apoyo en los muros de mampostería (50-60 cm)

Carga lineal en cabeza de muro de la casa ≈ 23 kN/m + peso propio ≈ 83 kN/m → tensión en base ≈ 0.19 MPa (referencia orientativa 0,3-0,5 MPa: **hay que ensayar la mampostería**).
Las viguetas apoyan en placas de reparto sobre un zuncho perimetral que ata los muros y hace de diafragma. Recomendación para abaratar: zuncho de hormigón armado (hecho a la vez que el forjado) en lugar de perfil UPN de acero.

## Pendiente de confirmar por un técnico
- Sismo (NCSE-02, zona sísmica de Almería) y arriostramiento de los muros de mampostería.
- Estudio geotécnico y zapatas definitivas; estado real de los muros (grietas, humedad, calidad de la piedra).
- Uniones, anclajes, protección contra fuego (R60 en vivienda de 2 plantas según CTE DB-SI) y comprobación de pandeo lateral.
- Cálculo de la chapa colaborante, del anclaje de los paneles solares al viento y de la impermeabilización con los fabricantes.
- Este documento no sustituye al proyecto de estructura visado.

## Sismo: comprobación orientativa (Albox está en zona sísmica)
Peso sísmico del edificio ≈ **3861 kN** (muros 2464, forjados 698, cubierta 551, sobrecarga casi permanente 113, acero 36).
Aceleración básica supuesta ab = 0.16 g (Almería capital: 0,14 g según la [tabla de municipios de NCSE-02](https://normatia.com/es/recursos/emplazamiento/zona-sismica/); Albox no aparece en esa tabla: hay que mirar el Anexo 1 de la norma).
Con un coeficiente sísmico de 0.20-0.25 (suposición conservadora para mampostería) el cortante en la base sería ≈ **772-965 kN**.
- **Dirección N-S:** muros de la casa (0,55 m) y de ladrillo del salón (0,25 m), 11.6 m² de sección → tensión tangencial ≈ 0.08 MPa.
- **Dirección E-O:** solo resisten el muro del fondo y los tramos del oeste (unos 16 m), porque el salón tiene la fachada acristalada y la línea de la viga de fachada no es muro → tensión ≈ 0.11 MPa.
Referencia de resistencia a cortante de mampostería antigua en buen estado: unos 0,05-0,15 MPa (hay que ensayarla).
**Conclusión:** en la dirección E-O el margen es justo. Antes de construir un técnico debe hacer el cálculo sísmico y definir el refuerzo: por ejemplo cruces de acero en dos paños de la línea de fachada, pantallas de hormigón armado de 15-20 cm en los tabiques de la suite o mallazo con mortero en las caras de los muros. Ya está previsto: zunchos de hormigón en cada nivel, riostras de cimentación entre zapatas y forjados que hacen de diafragma.


## Acero del modelo 3D (sin uniones ni placas)
Total ≈ 3630 kg (HEB 140: 1966 kg, HEB 120: 1281 kg, HEB 160: 187 kg, IPE 100: 137 kg, IPE 120: 58 kg). Ver `abaratar.md`.
