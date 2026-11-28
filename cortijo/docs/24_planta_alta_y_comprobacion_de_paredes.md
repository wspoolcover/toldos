# Planta alta: 3 dormitorios, 2 baños, terraza sobre el salón, y comprobación de las paredes (27-11-2026)

> **Nota (28-11-2026):** el propietario indica que la distribución de arriba es diferente. Este documento es la primera propuesta y queda pendiente de rehacer con su croquis. La tabla de apoyo se ha vuelto a calcular con la planta baja actual (puertas D1, D2, D3, D7 y D8 nuevas).

Archivos: `planta_alta_27nov.png` (plano sobre la planta baja en gris), `dos_plantas_3d.png` (vista previa; el modelo bueno es el STEP), `dos_plantas.step` y `.glb` (planta baja + forjado + planta alta + terraza, en piezas con color), `planta_alta.dxf`. Todo sale de `python planta_alta.py`, que usa la planta baja de `distribucion_deseada.py` (`23_distribucion_deseada_27nov.md`). Esquema, no al milímetro.

## 1. Lo que he entendido
- **Terraza**: «la planta alta sobre el salón es terraza». La he hecho a nivel del suelo de la planta alta (+3,30 m), sobre el forjado del salón, con antepecho de 1,0 m sobre los muros de 29 cm del salón. Lo que escribiste como «balcón sobrepuesto» lo he tomado como esta terraza. Si querías además un balcón volado en alguna fachada, dímelo.
- **Arriba**: 3 dormitorios, 2 baños, salida a la terraza.
- **Solo dos plantas** (confirmado el 28-11-2026): planta baja y planta 1, sin ático ni sótano. Encima de la planta 1, la cubierta (plana, con paneles solares, según la v8) y nada más. El diseño de este documento no cambia.
- **Tabiques sobre tabiques**: todos los tabiques de arriba van encima de un tabique de abajo. Donde no había tabique abajo (el comedor-distribuidor, debajo de la sala de estar) no he puesto ninguno.

## 2. Distribución de la planta alta
| Estancia | m² | Qué hay |
|---|---|---|
| Dormitorio 1 (suroeste, sobre la suite) | 17,1 | Cama de 1,80 m, armario, ventana al sur. Puerta de baño propio (Baño 1) y puerta al pasillo |
| Dormitorio 2 (sureste, sobre la cocina) | 18,7 | Cama de 1,80 m, armario, dos ventanas al sur. Puerta al pasillo. Sin baño propio: usa el Baño 1 desde el pasillo |
| Dormitorio 3 (sobre la oficina) | 7,0 | Cama de 1,35 m, armario, ventana al norte. Baño propio (Baño 2) |
| Baño 1 (sobre el vestidor) | 5,9 | Ducha, lavabo, inodoro. Dos puertas: al Dormitorio 1 y al pasillo. Sin ventana |
| Baño 2 (sobre el baño de la suite) | 6,9 | Ducha, lavabo, inodoro, ventana pequeña alta al norte |
| Pasillo (arriba de la escalera) | 2,5 | Reparte a los dormitorios y al Baño 1 |
| Sala de estar | 13,5 | Sofá, mesa, TV. **Sale a la terraza** por una puerta balconera de 1,60 m |
| Terraza sobre el salón | 38,7 | Mesa con 6 sillas y dos tumbonas dibujadas |
| **Total útil planta alta** | **71,6** | sin terraza ni hueco de la escalera (2,8 m²) |

Útil de las dos plantas: 120,3 + 71,6 = **191,9 m²** (la v8 tenía 177,7 m²).

**Escalera**: la he mantenido como confirmaste (sube hacia el sur). Llega arriba en el extremo sur del hueco (0,96 × 2,9 m) y se sale **por los dos lados** en los últimos peldaños: al oeste al pasillo y al este a la sala de estar. El resto del borde del hueco lleva barandilla de 1,05 m.

## 3. Comprobación de las paredes de arriba
Qué hay debajo de cada pared (muestreo cada 5 cm sobre su eje, comparado con los muros y tabiques de la planta baja). «Hueco» es una puerta o ventana de abajo: ahí hace falta dintel. Altura libre de arriba: 2,70 m (PL-11).

| Pared de la planta alta | Largo (m) | Espesor | Esbeltez h/e | Debajo: muro | tabique | hueco | vacío | Resultado |
|---|---|---|---|---|---|---|---|---|
| Sur | 9.20 | 14 cm | 19 | 60 % | 0 % | 40 % | 0 % | ✓ con dintel en el hueco de abajo |
| Oeste | 8.80 | 14 cm | 19 | 100 % | 0 % | 0 % | 0 % | ✓ sobre muro |
| Este, tramo sur | 4.20 | 14 cm | 19 | 100 % | 0 % | 0 % | 0 % | ✓ sobre muro |
| Este, tramo del saliente | 3.00 | 14 cm | 19 | 10 % | 63 % | 27 % | 0 % | ⚠ sobre tabique de 7 cm: jácena o muro debajo |
| Este, tramo norte | 1.70 | 29 cm | 9 | 100 % | 0 % | 0 % | 0 % | ✓ sobre muro |
| Norte, hasta x = 7,30 | 7.30 | 29 cm | 9 | 100 % | 0 % | 0 % | 0 % | ✓ sobre muro |
| Norte, balconera | 1.97 | 14 cm | 19 | 8 % | 0 % | 0 % | 92 % | ✗ sin apoyo: jácena (viga) debajo |
| Central E-O | 9.27 | 14 cm | 19 | 72 % | 0 % | 28 % | 0 % | ✓ con dintel en el hueco de abajo |
| T1 x = 4,40 (dormitorio 1 | dormitorio 2) | 3.98 | 7 cm | 39 | 0 % | 100 % | 0 % | 0 % | ✓ tabique sobre tabique; vigueta doble (las viguetas van N-S) |
| T2 x = 3,10 (baños | dormitorio 3 y pasillo) | 4.33 | 7 cm | 39 | 0 % | 81 % | 19 % | 0 % | ✓ tabique sobre tabique; vigueta doble (las viguetas van N-S) |
| T3 y = 5,485 (pasillo | dormitorio 3) | 2.23 | 7 cm | 39 | 0 % | 64 % | 36 % | 0 % | ✓ tabique sobre tabique |
| T4 y = 6,335 (baño 1 | baño 2) | 3.00 | 7 cm | 39 | 0 % | 73 % | 27 % | 0 % | ✓ tabique sobre tabique |
| T5 x = 5,40 (dormitorio 3, este) | 3.16 | 7 cm | 39 | 0 % | 100 % | 0 % | 0 % | ✓ tabique sobre tabique; vigueta doble (las viguetas van N-S) |

**Dato de partida**: en la lámina PL-11 las viguetas T-20 van **perpendiculares al muro central**, es decir, en dirección norte-sur en nuestro plano. Lo he supuesto para toda la planta.

### Qué sale
1. **Los 5 tabiques de arriba están sobre tabiques de abajo** (100 % del recorrido, contando los huecos con su dintel). Se cumple lo que pediste.
2. **Tabiques norte-sur (x = 3,10; 4,40; 5,40)**: van en el sentido de las viguetas, así que llevan **vigueta doble** debajo. Como encima de ellos hay tabique abajo, la vigueta doble cae justo sobre ese tabique, y el de x = 4,40 además tiene debajo el zuncho central. Los tabiques este-oeste (y = 5,485 y 6,335) cruzan las viguetas y no necesitan nada especial. Lo confirma el técnico con el cálculo.
3. **✗ Pared norte, tramo de la balconera (x = 7,30 a 9,27 m)**: abajo no hay nada, es el paso abierto del comedor al salón. Hace falta una jácena (viga) de unos 2,0 m a nivel del forjado, que también carga el borde del forjado. Lo necesita la planta baja aunque no hubiera planta alta.
4. **⚠ Pared este, tramo del saliente (y = 4,2 a 7,2 m)**: abajo solo hay el tabique de 7 cm del baño grande (63 %) y los extremos de muro. Un tabique de 7 cm no soporta una pared. Opciones: jácena de unos 3,0 m entre el muro central y el muro norte del saliente, o que esa pared sea la del vecino. **No sé quién es el dueño de esa pared**; hay que mirarlo.
5. **✓ Fachadas sur y oeste, este (tramo sur), norte (hasta x = 7,30) y este (tramo norte)**: están sobre muro. El muro sur y el central tienen puertas y ventanas debajo (40 % y 18 %): los dinteles de abajo los resuelven. El muro central de arriba (14 cm) apoya sobre el de abajo (29 cm).
6. **Esbeltez** (altura libre dividida entre espesor, arriba a 2,70 m): 14 cm → 19; 29 cm → 9; 7 cm → 39 (abajo, a 3,0 m, el de 7 cm sale a 43). El propio proyecto (PL-05, ADD-13) limita las paredes exentas a 7 veces el espesor: 0,98 m para 14 cm. Es decir, los muros de 14 cm de la fachada solo valen si están atados arriba y abajo (zuncho, forjado y pilares). Lo mismo vale para los de abajo que siguen en pie hoy, sin forjado ni tejado, y ya te dije que están sueltos.
7. **Tabiques de abajo bajo el forjado**: los de 7 cm de abajo no deben cargar el forjado. Se deja una junta flexible en su coronación contra el forjado; la carga de los tabiques de arriba va por la losa a las viguetas dobles.

## 4. Baños y fontanería
- **Baño 1 y Baño 2 van pegados por el tabique de y = 6,335**, el mismo tabique que separa abajo el vestidor del baño de la suite. Una sola bajante (Ø110) en esa línea, hacia x ≈ 2,5–3,0 m, sirve a los dos baños de arriba y baja a la planta baja por ese tabique, entre el vestidor y el baño de la suite. Hay que engrosar el tabique o trasdosar un tramo para alojarla. El baño de la suite de abajo cae justo debajo del Baño 2.
- **El Baño 1 está encima de un vestidor** (no hay sanitarios abajo): la bajante es lo único que pasa. Está pensado así para no poner un baño sobre la cocina ni sobre el comedor.
- **Ventilación**: el Baño 1 no tiene ventana; el Baño 2 tiene una pequeña y alta al norte. Hacen falta extractores.

## 5. Otras cosas de la terraza
- El forjado de la terraza salva unos 6,0 m entre los muros de 29 cm del salón (este y oeste). Es la parte delicada que ya había señalado (`20_proyecto_original_y_diseno_actual.md`): nadie la ha calculado.
- Hay que prever pendiente, impermeabilización, desagüe y el antepecho de 1,0 m sobre los muros del salón.
- **La chimenea** sube por la esquina suroeste del salón, atraviesa la terraza (hueco de 0,45 × 0,45 m) y sale por encima del antepecho; he dibujado el conducto hasta +3,0 m sobre la terraza.
- La cubierta de la planta alta no está dibujada (plana con paneles solares, según la v8).

## 6. Lo que necesito de ti
1. ¿Te vale el Dormitorio 3 de 7,0 m², o prefieres que la sala de estar sea un dormitorio y este una sala? (Los tabiques de arriba tendrían que cambiar de sitio y dejarían de estar sobre tabiques de abajo.)
2. ¿Quieres baño propio también en el Dormitorio 2? Con 2 baños, el Baño 1 hace de baño compartido.
3. ¿De quién es la pared este de arriba, entre y = 4,2 y 7,2 m?
4. ¿Qué uso quieres en la terraza (comedor, tumbonas, pérgola…)?
