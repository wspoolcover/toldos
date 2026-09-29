# Predimensionado de estructura de acero (PRELIMINAR)

Acero S275JR (fy = 275 MPa), γM0 = γM1 = 1,05, ELU 1,35 G + 1,50 Q, flecha total L/300 y de sobrecarga L/400 (CTE DB-SE).

| Carga | G (kN/m²) | Q (kN/m²) |
|---|---|---|
| Forjado de la casa (planta alta) | 4.8 | 2.0 |
| Terraza transitable sobre el salón | 4.8 | 2.0 |
| Cubierta plana no transitable (piedra + paneles solares) | 6.1 | 1.0 (mantenimiento; nieve 0,5 supuesta) |

## Terraza sobre el salón: viguetas E-O (luz 5,75 m)
| Sección | Separación (m) | kg/m² | M/Mrd | Flecha total / límite (mm) |
|---|---|---|---|---|
| IPE 240 | 1.2 | 25.6 | 0.51 | 14.7 / 19.2 |
| IPE 220 | 1.0 | 26.2 | 0.54 | 17.3 / 19.2 |

## Planta alta de la casa: viguetas E-O (luz máx. 2,55 m)
| Sección | Separación (m) | kg/m² | M/Mrd | Flecha total / límite (mm) |
|---|---|---|---|---|
| IPE 120 | 1.2 | 8.7 | 0.59 | 6.8 / 8.5 |
| IPE 120 | 1.0 | 10.4 | 0.49 | 5.7 / 8.5 |

## Vigas N-S del forjado (líneas x = 3,10; 5,30 y 7,20; una pieza continua de dos vanos 4.20 + 3.95 m; ancho tributario 2.38 m)

Sección: **HEB 140**. M/Mrd = 0.74 en el apoyo central; V/Vrd = 0.40; flecha 8.7 mm (límite 14.0). Reacción en el pilar central ≈ 117 kN. Al ser continua trabaja mejor que dos vigas sueltas y admite un perfil menor.

## Cubierta plana (piedra y paneles solares): viguetas E-O (luz 2,55 m)
| Sección | Separación (m) | kg/m² | M/Mrd | Flecha total / límite (mm) |
|---|---|---|---|---|
| IPE 120 | 1.2 | 8.7 | 0.60 | 7.1 / 8.5 |
| IPE 120 | 1.0 | 10.4 | 0.50 | 5.9 / 8.5 |

Vigas N-S de cubierta (continuas): **HEB 140** (M/Mrd 0.76, flecha 9.1/14.0 mm).

## Dintel sobre la cristalera (luz 4.10 m; muro y antepecho 13.8 kN/m)

Sección: **HEB 160** (M/Mrd 0.53, flecha 12.2/13.7 mm). Se aloja en el espesor del muro con placas de apoyo de 0,20 m en cada extremo.

## Viga de fachada (sustituye al muro entre salón y casa, en cada planta; luz 2.30 m entre pilares)

Sección: **HEB 120** (M/Mrd 0.26, flecha 2.5/7.7 mm). Cada planta lleva su viga; los pilares HEB 120 en x = 3,10; 5,30 y 7,20 quedan vistos en el borde del salón.

## Viga de borde del saliente del baño (a x = 9,15, en forjado y en cubierta; luz 3.70 m entre muros)

Falta ese muro entre la casa y el saliente, así que una viga recoge el borde de la casa y las viguetas del saliente. Sección: **HEB 160** (forjado M/Mrd 0.59, cubierta 0.42).

## Dinteles de puertas y ventanas en muros de mampostería
| Hueco (m) | Luz de cálculo | Perfil | M/Mrd |
|---|---|---|---|
| ≤ 1.0 | 1.4 | IPE 100 | 0.65 |
| ≤ 1.2 | 1.6 | IPE 100 | 0.85 |
| ≤ 1.4 | 1.8 | IPE 120 | 0.70 |
| ≤ 1.6 | 2.0 | IPE 120 | 0.86 |

## Pilares HEB (6 uds., x = 3,10; 5,30 y 7,20; y = 7,60 y 11,80; ocultos en muros y tabiques; altura ≈ 5,6 m)

Carga axial de cálculo máx. ≈ 240 kN (pilar central) y ≈ 97 kN (pilar sur). Sección: **HEB 120**, N/Nb,Rd = 0.65 (pandeo eje débil, Lcr = 3,3 m).

Zapatas aisladas bajo pilares (σ adm. supuesta 150 kPa, **pendiente de estudio geotécnico**): ≈ 1.4 × 1.4 m, canto 0,60 m.

## Apoyo en los muros de mampostería (50-60 cm)

Carga lineal en cabeza de muro de la casa ≈ 24 kN/m + peso propio ≈ 83 kN/m → tensión en base ≈ 0.20 MPa (referencia orientativa 0,3-0,5 MPa: **hay que ensayar la mampostería**).
Las viguetas apoyan en placas de reparto sobre un zuncho perimetral que ata los muros y hace de diafragma. Recomendación para abaratar: zuncho de hormigón armado (hecho a la vez que el forjado) en lugar de perfil UPN de acero.

## Pendiente de confirmar por un técnico
- Sismo (NCSE-02, zona sísmica de Almería) y arriostramiento de los muros de mampostería.
- Estudio geotécnico y zapatas definitivas; estado real de los muros (grietas, humedad, calidad de la piedra).
- Uniones, anclajes, protección contra fuego (R60 en vivienda de 2 plantas según CTE DB-SI) y comprobación de pandeo lateral.
- Cálculo de la chapa colaborante, del anclaje de los paneles solares al viento y de la impermeabilización con los fabricantes.
- Este documento no sustituye al proyecto de estructura visado.
## Acero del modelo 3D (sin uniones ni placas)
Total ≈ 6.080 kg: HEB 140 1.704 kg · IPE 120 1.367 kg · HEB 120 1.265 kg · IPE 240 1.105 kg · HEB 160 505 kg · IPE 100 137 kg. Ver `abaratar.md`.
