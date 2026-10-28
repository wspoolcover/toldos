# Fosa séptica y pozo filtrante (28-10-2026)

Pregunta del propietario: cómo se hace exactamente la fosa séptica y el «pozo ciego», si el pozo va a unos 5 m de profundidad con anillos de hormigón, qué diámetro tienen y si ya se pueden comprar. Esquemas: `fosa_septica_esquema.png` y `pozo_filtrante_5m.png` (`python fosa_esquema.py`).

## 1. Cómo funciona, en cinco pasos
1. **Casa**: los baños y la cocina bajan por las bajantes a un colector enterrado con 1–2 % de pendiente.
2. **Arqueta de registro** (y, en la cocina, un separador de grasas): para poder desatascar.
3. **Fosa séptica**: tanque cerrado y estanco de dos cámaras. Los sólidos se hunden y se descomponen en parte; sale agua turbia, todavía sucia. Se vacía cada 1–2 años con un camión de un gestor autorizado.
4. **Arqueta de reparto**.
5. **Pozo filtrante** (o zanjas filtrantes): el agua se filtra al terreno y la tierra termina de depurarla.

**Lo importante**: el «pozo ciego» tal como se hacía en los cortijos (todo directo al terreno, sin fosa delante) no se autoriza hoy en una vivienda nueva. Lo que sí se hace es la misma idea con la **fosa séptica delante**: el pozo pasa a ser un **pozo filtrante**. Es la solución que describo aquí.

| | Qué es | Se admite |
|---|---|---|
| **Pozo ciego o negro** | Pozo sin tratamiento previo | No para una vivienda nueva |
| **Fosa séptica + zanjas filtrantes** | Tubo agujereado en grava, poco profundo | Sí, con autorización de vertido; la más recomendada |
| **Fosa séptica + pozo filtrante** | Anillos de hormigón perforados, hondo | Sí, con autorización; depende del terreno y del nivel freático |
| **Depósito estanco** | Tanque cerrado sin salida; lo vacía un camión | Sí; no es vertido, pero es un coste fijo (ver apartado 5) |
| **Depuradora compacta** | Equipo prefabricado que depura más | Sí; útil si el terreno no infiltra |

## 2. Lo que hay en el proyecto y lo que no sabemos
- El plano **PL-09** del arquitecto solo dice «conexión a fosa séptica», y los planos la sitúan al norte. En las fotos de octubre **no se ve ninguna fosa ni pozo**.
- En las fotos hay un **pasamuros circular** en uno de los muros de hormigón en L junto a la losa. Podría ser la salida del saneamiento; hay que confirmarlo.
- Nuestro esquema (`instalaciones.py`, `cimentacion_plano.py`) lleva un colector Ø150 bajo la solera por el eje del salón hacia el norte. Falta fijar dónde acaba y a qué cota.
- Falta también el **desnivel de la finca** (qué parte queda más baja que la casa) y el **nivel del agua subterránea**.

## 3. Qué dice la normativa (lo que he podido comprobar)
Fuente principal: guía de la Confederación Hidrográfica del Segura (rev. 2017) sobre vertidos de viviendas unifamiliares. **No es la de Albox**: Albox está, según creo, en las Cuencas Mediterráneas Andaluzas, que gestiona la Junta de Andalucía, pero no he podido confirmarlo y no he podido leer el Decreto 109/2015 de vertidos de Andalucía. Sirve como referencia; hay que confirmar con la Delegación de Medio Ambiente de Almería y con el Ayuntamiento.
- Verter al terreno, o a través de un pozo o una zanja filtrante, se considera **vertido indirecto a aguas subterráneas** y necesita **autorización** del organismo de cuenca (arts. 245 y siguientes del Reglamento del Dominio Público Hidráulico). La vivienda unifamiliar cuenta como vertido urbano, y se autoriza **después de un tratamiento depurador adecuado**.
- Un **pozo que llega hasta el nivel freático** se trata como **vertido directo** a aguas subterráneas, y puede exigir más depuración y un estudio hidrogeológico (art. 258).
- Si se vierte a un **recinto estanco** vaciado por un gestor autorizado, no hay vertido y no hace falta autorización de vertido; lo valora la administración local o autonómica.
- **No se autoriza** verter al dominio público cuando se puede conectar a la red municipal; consultan al Ayuntamiento. En un diseminado de Locaiba lo normal es que no haya red; conviene preguntarlo.
- Fosa prefabricada: norma **UNE-EN 12566-1**, con marcado CE. Capacidad mínima **3 m³** hasta 5 habitantes y **+1 m³ por cada 5 habitantes más**; para 10 habitantes, 4 m³. Carga hidráulica de 600 L/día más 120 L/día por cada habitante adicional (1.200 L/día para 10).
- Para dimensionar la parte filtrante recomiendan la norma **NTE-ISD/1974**; no he podido leer sus tablas.
- **Pluviales y vaciado de piscinas no van** por la fosa.
- El titular tiene que ser propietario del terreno que ocupa el sistema.
- Un expediente de la Cuenca Mediterránea Andaluza (en Granada) sancionó con 1.000 € el vertido a una fosa sin impermeabilizar; es un ejemplo de por qué hay que hacerla bien.

## 4. El pozo filtrante de 5 m con anillos de hormigón
Supuestos: 5 m de profundidad medidos desde el suelo hasta el fondo; **5 anillos de 1,0 m** y una losa de cierre con boca de Ø 60 cm. El primer anillo va **liso** y los otros cuatro **perforados**, con una corona de grava de unos 0,4 m envuelta en geotextil y 0,5 m de grava en el fondo (sin solera).

| Ø interior del anillo | Peso aprox. de un anillo de 1 m | Pared filtrante (4 m) | Tasa mínima del terreno para 1.200 L/día · 1.500 L/día |
|---|---|---|---|
| 1,2 m | ≈ 1,6 t | 15 m² | 80 · 100 L/m²·día |
| **1,5 m** | ≈ 2,3 t | 19 m² | 64 · 80 L/m²·día |
| 1,8 m | ≈ 2,9 t | 23 m² | 53 · 66 L/m²·día |
| 2,0 m | ≈ 3,3 t | 25 m² | 48 · 60 L/m²·día |

- **Caudal**: 8–10 personas × 150 L = 1.200–1.500 L/día. Si la casa se usa solo en parte del año, o los dormitorios finales son 4, baja.
- **Datos de partida de los pesos**: un catálogo de precios da, para un anillo de Ø 1,2 m, 16 cm de pared y 1 m de alto, 1.600 kg. Para los demás diámetros he supuesto paredes de 18–20 cm; el peso exacto lo da el fabricante.
- **Lo que hay que saber del terreno**: los valores habituales de diseño van de unos 18 a 48 L/m²·día (de terreno «lento pero válido» a «muy permeable»). **Un solo pozo de 5 m de Ø 1,5–2,0 m solo cumple si el terreno es muy permeable** (grava o arena). Con limo o arcilla no hay diámetro que lo arregle: harían falta más pozos o zanjas, o una depuradora. Las fotos de octubre muestran una costra de **arcilla o limo agrietada**; eso es la capa de arriba, y a 5 m puede haber otra cosa. Por eso hay que mirarlo.
- **Nivel freático**: en zanjas se exige 1,2 m entre el fondo y el agua en época de lluvias. Para un pozo de 5 m significa que el agua debería estar a más de 6 m; si no, es vertido directo.
- **Cimentación**: la arcilla se hincha al mojarse. El pozo debe quedar **lejos de los muros y las zapatas**: mi criterio es **al menos 5 m** del muro más cercano de la casa, mejor 6–8 m, y cuesta abajo.
- **Obra a 5 m**: la excavación sale de unos 3 m de diámetro y 28–40 m³ de tierra. A esa profundidad nadie baja al hoyo sin entibación o talud tendido, y los anillos de más de 2 t necesitan una grúa de camión. Lo plantea el contratista.

## 5. ¿Se pueden comprar ya los anillos?
**Todavía no; sí se puede pedir presupuesto.** Comprar antes de saber tres cosas es arriesgarse a un diámetro o un número de anillos equivocados:
1. **El terreno a 5 m**: una calicata con retroexcavadora en el sitio previsto (medio día) para ver los estratos y el agua, y un **ensayo de infiltración** a la profundidad del pozo. Decide si el pozo vale y de qué diámetro, o si son mejores las zanjas.
2. **La vía legal**: la consulta a la Delegación de Medio Ambiente y al Ayuntamiento, con la propuesta fosa + pozo. Si piden depuradora o zanjas, el pozo cambia.
3. **El sitio y las cotas**: la posición de la fosa y del pozo y la profundidad del colector, para saber a qué cota entra el agua en el pozo. Lo fija el técnico con el desnivel real.

**Qué pedir al proveedor**: anillos de hormigón armado **perforados (drenantes)** de Ø interior 1,5 m (y presupuesto del 2,0 m), altura 1,0 m, junta machihembrada, **peso por pieza**, una losa de cierre con boca de registro Ø 60 y tapa con cerco, y las condiciones de entrega con **grúa**. Pregunta también por el anillo **liso** de arriba y por los de 0,5 m (pesan la mitad). Para la fosa: depósito prefabricado de **4–5 m³** con marcado CE y UNE-EN 12566-1, y, si el camión va a circular encima, que sea de clase de carga apta para tráfico.

**Orden de compra recomendado**: primero la calicata y el ensayo; luego la fosa (que se necesita casi con seguridad); el pozo, cuando el terreno confirme el diámetro. Los anillos no son lo que más pesa en el presupuesto; la grúa, la excavación y la autorización sí.

**Depósito estanco**: con 1.200 L/día, un depósito de 10 m³ se llena en ocho días, unos 45 vaciados al año. No sale a cuenta como solución permanente de una casa habitada; solo como solución temporal o de uso ocasional.

## 6. Dónde ponerlo en la finca
- **Cuesta abajo de la casa**, para que el agua vaya por gravedad. Si no hay desnivel, hay que bombear, y no conviene.
- **A 5 m o más** de los muros y las zapatas de la casa y de los vecinos (medianeras). Los muros del salón ya hechos están en el norte.
- **A 3 m o más de los olivos** y de los árboles grandes (las raíces rompen el drenaje) y a **1,5 m o más de los lindes**.
- **A 15 m o más de cualquier pozo de agua**, propio o del vecino (mejor 30 m). Hay que preguntar a los vecinos si tienen alguno.
- **Lejos de la rambla y de la acequia**: nada de verter en ellas. La acequia es un cauce privado y haría falta permiso del titular.
- **Con acceso para el camión cisterna** hasta la tapa de la fosa (el acceso de 7 m ayuda). Evita ponerla bajo el patio de grava donde aparcan los coches, salvo que sea apta para tráfico.
- **Sin pasar por encima de las instalaciones**: cables, tubo rojo de la CGP, agua.

## 7. Orden de trabajo propuesto
1. **Calicata y ensayo de infiltración** en 1–2 puntos (esta semana si se puede).
2. **Consulta** al Ayuntamiento (red de alcantarillado, licencia, requisitos) y a la Delegación de Medio Ambiente (autorización de vertido y qué documentación piden).
3. **Técnico**: proyecto o memoria de depuración y vertido con plano de situación, si lo exige la autorización.
4. **Compra**: fosa, anillos, grava, geotextil, arquetas; contratar la grúa.
5. **Obra**: la fosa y el colector van **antes de hormigonar la solera** (pasos y pendientes); el pozo puede ir después.
6. **Final**: certificado de la fosa y contrato de vaciado con gestor autorizado; es lo que piden para la ocupación en muchos ayuntamientos.

## 8. Costes orientativos (estimación mía; sin presupuesto; hay que pedirlos)
| Partida | Orden de magnitud |
|---|---|
| Calicata con retroexcavadora y ensayo | 300–600 € |
| Fosa séptica prefabricada de 4–5 m³, colocada | 1.500–3.000 € |
| Pozo filtrante de 5 m (anillos, grava, geotextil, losa, grúa y excavación) | 3.000–6.000 € |
| Alternativa: zanjas filtrantes (80 m) | 2.500–5.000 € |
| Alternativa: depuradora compacta (10 habitantes) | 4.000–8.000 € |
| Memoria técnica y tramitación de la autorización | 800–2.500 € |

## 9. Qué necesito de las fotos y del terreno
1. **Vistas generales** de la finca desde varios puntos, que se vea el **desnivel**, los linderos, la rambla y el camino.
2. **Tapas, losas de hormigón, tubos que sobresalen**, manchas húmedas o verdes, olores: señales de una fosa o un pozo ya hecho. Incluido el **pozo antiguo del cortijo**, que suele estar cerca del corral o de la letrina.
3. **El pasamuros circular** del muro de hormigón en L: foto de cerca, y a dónde apunta.
4. **Cualquier pozo de agua** o aljibe, propio o de los vecinos, a menos de 30 m; el contador de agua, la acequia, el poste de luz.
5. **El terreno en el sitio previsto del pozo**: una calicata de 0,5–1 m con una cinta métrica al lado, para ver las capas.
6. **Medidas con cinta**: de la fachada norte al lindero norte; de la casa al lugar del pozo; de la casa al pozo más cercano.
7. Cuántas personas vivirán, con qué frecuencia y si habrá piscina.

## 10. Fuentes
- [Confederación Hidrográfica del Segura: requisitos de vertido de viviendas unifamiliares (2017)](https://www.chsegura.es/export/descargas/servicios/oficinavirtual/docsdescarga/Requisitos-vertidos-viviendas-unifamiliares-y-nucleos-urbanos-hasta-250-habitantes-equivalentes.pdf)
- [iAgua: zanjas filtrantes, diseño, ubicación y construcción](https://www.iagua.es/blogs/juan-jose-salas/zanjas-filtrantes-fundamentos-diseno-seleccion-ubicacion-y-construccion)
- [Generador de precios: anillo prefabricado de hormigón armado de 120 cm](https://generadordeprecios.info/espacios_urbanos/Instalaciones/Urbanas/Redes_de_saneamiento/IUS055_Pozo_de_registro_prefabricado_de_ho.html)
- [Decreto 109/2015 de vertidos de Andalucía (no he podido leer el texto)](https://www.iberley.es/legislacion/decreto-109-2015-17-marzo-aprueba-reglamento-vertidos-dominio-publico-hidraulico-dominio-publico-maritimo-terrestre-andalucia-20785901)
