# Especificación del material · Póster científico y documentos de memorias

**IV Encuentro Latinoamericano de Semilleros de Investigación · Universidad de Cundinamarca, sede Fusagasugá · miércoles 4 de noviembre de 2026**
**Escrito el sábado 29 de agosto de 2026.** Toda fecha va en absoluto; los días restantes se cuentan desde hoy.

Fuentes primarias, ya guardadas en el expediente:

- `Convocatoria/INVITACIÓN FORMAL IV ENCUENTRO TRANSLOCAL.pdf` (11 páginas, 258.166 bytes, `creationDate D:20260821101039-05'00'`)
- `Convocatoria/Encuentro Latinoamericano translocal.jpg` (pieza gráfica, 1080 × 1080 px, RGB, 679.784 bytes)
- `Convocatoria/_extraccion/` — derivados de trabajo: `p6_poster.png` (diagrama del póster recortado de la p.6), `_pdftext.txt`, `_pdftext_1011.txt`, `_qr.png`
- Censo de los 48 ítems del formulario de semilleristas (2026-08-29), transcrito en `GUIA - Inscripcion paso a paso.md`

**Qué cubre este documento.** Dos entregables distintos, con reglas y plazos distintos:

- **§A · el póster de 90 × 120 cm**, que la p.6 impone («Los proyectos deberán presentarse mediante: Modalidad Póster Científico») y que las pp.8-9 y el ítem 36 del formulario vuelven opcional. Está sin resolver: es la pregunta 7 del correo al organizador (§5 de la guía). **Prepáralo solo cuando contesten, o si decides asumirlo.**
- **§B · los dos documentos de memorias** del ítem 43, que son **obligatorios para poder enviar el formulario** y vencen el **lunes 14 de septiembre de 2026 (faltan 16 días)**. Esto no es opcional y es la fecha operativa real de toda la vía.

> ⚠️ **Advertencia que gobierna las dos partes.** Hoy no está resuelto **de quién es el trabajo** que se presentaría (bloqueo **B14** de la guía: los ítems 3, 32 y 45 fila 1 forman una sola declaración de autoría). Toda la especificación de abajo es geometría y tipografía: define **el recipiente**, no el contenido. Los datos que dependen de personas —semillero, autores, resultados— van marcados **FALTA - lo pones tú**, y no se rellenan con nada parecido.

---

## §A · Póster científico

### A.1 · Lo que exige la fuente, y sus contradicciones

| Requisito | Literal de la fuente | Estado |
|---|---|---|
| Medida | «90 x 120 cm» (vertical, según el diagrama incrustado) | PDF p.6. Es la única medida numérica |
| Material | «PAPEL BOND TAMAÑO PLIEGO» | PDF p.6. ⛔ **Contradice la medida**: no dice cuánto mide un pliego, y ningún pliego comercial colombiano mide 90 × 120 cm |
| Legibilidad | «legibilidad a dos metros» | PDF p.7. Es el único criterio de tipografía que da la convocatoria: **no fija cuerpos ni fuentes** |
| Contenido obligatorio 1 | «Logo de la Universidad e institución participante» | PDF p.7. ⛔ **Bloqueo de producción**: el logo de la UdeC no existe en calidad de impresión (ver A.5) |
| Contenido obligatorio | Título, autores, semillero, introducción, objetivos, metodología, resultados, conclusiones y referencias | PDF p.7 |
| Modalidad | «Los proyectos deberán presentarse mediante: Modalidad Póster Científico» | PDF p.6, contra pp.8-9 e ítem 36 del formulario, que ofrecen tres modalidades |

**Sobre el «pliego».** La convocatoria pide a la vez una medida exacta (90 × 120 cm) y un soporte cuyo tamaño no define. Mandan los 90 × 120 cm, que es el dato numérico; el «papel bond» se interpreta como recomendación de acabado (mate, no brillante). Si el organizador contesta otra cosa, manda su respuesta. Esto va en el correo.

### A.2 · Geometría del archivo

| Magnitud | A 150 dpi (recomendado) | A 300 dpi |
|---|---|---|
| Lienzo 90 × 120 cm | **5.315 × 7.087 px** | 10.630 × 14.173 px |
| Píxeles por centímetro | 59,06 | 118,11 |
| Ancho mínimo de una imagen colocada a 20 cm | **1.181 px** | 2.362 px |
| Alto mínimo de una banda de logos de 6 cm | **354 px** | 709 px |

150 dpi es el estándar de impresión de gran formato para piezas que se ven a más de un metro, y es el que usa esta especificación: a 300 dpi el archivo se cuadruplica sin ganancia visible a dos metros. **Regla que se aplica sin excepción: ninguna imagen se escala por encima de su resolución nativa.** El alto máximo en centímetros de cualquier logo o captura es `píxeles ÷ 59,06`.

Formato de entrega a la litografía: **PDF/X con las fuentes incrustadas**, más un PNG de respaldo a 150 dpi. Sangrado 3 mm si se imprime a corte; si va montado en foam o se cuelga con ojales, sin sangrado.

### A.3 · La retícula

Vertical, 90 × 120 cm, dos columnas. Cuadra exactamente: **4 + 39 + 4 + 39 + 4 = 90 cm** de ancho y **4 + 22 + 2 + 74 + 2 + 12 + 4 = 120 cm** de alto.

**Banda superior — 22 cm de alto, 82 cm de ancho**

| # | Bloque | Alto | Contenido | Estado |
|---|---|---|---|---|
| 1 | Fila de logos | 5 cm | Logo de la UdeC + logo de la CUN, alineados a los extremos | ⛔ **BLOQUEADO**: falta el logo de la UdeC en calidad de impresión (A.5) |
| 2 | Título | 10,6 cm (2 líneas a 120 pt) | El mismo texto **en mayúscula** que se teclee en el ítem 32 del formulario | **FALTA - lo pones tú.** Depende de B14 |
| 3 | Autores | 2,65 cm (1 línea a 60 pt) | Ponente Principal (estudiante) y Segundo Ponente, en el orden en que se registren en los ítems 3 y 15 | **FALTA - lo pones tú** el nombre del estudiante. El tuyo: JULIAN ANDRÉS CASTAÑO ESPINOSA |
| 4 | **Semillero de investigación** | 2,12 cm (1 línea a 48 pt) | Nombre del semillero que firma la ponencia | ⛔ **FALTA.** Ver la regla de abajo |

> ⛔ **Regla del bloque 4, y no admite atajo.** Aquí va **únicamente el semillero que efectivamente firma la ponencia y que lo ha aceptado por escrito** (acta o correo del líder). Hoy no existe ese documento: SIAES no está constituido —sin acta y sin estudiantes adscritos— y AXON 23, IDECUN, INNOTI y METAPROMPT son ajenos al trabajo. **No se escribe un semillero por parecido, ni el del líder que te acoja «mientras se formaliza».**
>
> **Y si el trabajo sigue siendo examlab, este bloque no lleva semillero: lleva la filiación del autor.** La línea correcta bajo el título sería entonces `Corporación Unificada Nacional de Educación Superior (CUN) — Escuela de Ingenierías`, porque ningún semillero produjo ese trabajo. Ojo: eso choca con el contenido obligatorio de la p.7 («semillero») y con el sentido del Encuentro, y es otra cara del bloqueo B14. Se resuelve antes de maquetar, no durante.

**Columna izquierda — 39 cm de ancho, 74 cm de alto**

| # | Bloque | Encabezado | Gráfico | Texto | Alto |
|---|---|---|---|---|---|
| 5 | Introducción y planteamiento | 3,5 cm | — | 9 líneas · ≈ 80 palabras | 19,4 cm |
| 6 | Objetivos (general + 3 específicos) | 3,5 cm | — | 8 líneas · ≈ 70 palabras | 17,6 cm |
| 7 | Metodología | 3,5 cm | diagrama de 12 cm | 8 líneas · ≈ 70 palabras | 29,6 cm |

Suma: 66,6 cm de bloques + 2 aires de 2 cm = **70,6 cm**, con **3,4 cm de holgura** sobre los 74 disponibles.

**Columna derecha — 39 cm de ancho, 74 cm de alto**

| # | Bloque | Encabezado | Gráfico | Texto | Alto |
|---|---|---|---|---|---|
| 8 | Resultados | 3,5 cm | 28 cm de figuras o capturas | 8 líneas · ≈ 70 palabras | 45,6 cm |
| 9 | Conclusiones | 3,5 cm | — | 11 líneas · ≈ 100 palabras | 22,9 cm |

Suma: 68,5 cm + 1 aire de 2 cm = **70,5 cm**, con **3,5 cm de holgura**.

> ⛔ **Los 28 cm de figuras del bloque 8 son un hueco, no un contenido.** Ahí van resultados que hoy no existen: **FALTA - los aporta quien hizo el trabajo.** Y con una prohibición explícita: **ninguna cifra de desempeño que no se haya medido entra en este póster.** Si el trabajo es la Ruta A de la guía (proyecto del estudiante), las figuras las trae él; si no hay resultados, el bloque se rehace como «Resultados esperados» y se dice que son esperados.

**Pie — 12 cm de alto, 82 cm de ancho**

| # | Bloque | Alto | Contenido |
|---|---|---|---|
| 10 | Referencias | 2,5 cm de encabezado + 9,5 cm de texto | A 22 pt, en dos columnas de 39 cm: **9 líneas por columna, 18 en total** ≈ 6 referencias APA. Cabe el DOI de `anchored-feedback` (`10.5281/zenodo.22069535`) si el trabajo lo usa |

Datos de contacto y QR: van dentro de la banda superior, al lado derecho de la fila de logos, a 28 pt. El correo es `julian_castanoe@cun.edu.co` (`config/universidades/cun.json` → `docente.correo_cun`). **Tu celular: FALTA - lo pones tú** si decides ponerlo; no está en el repositorio.

**Presupuesto total de texto: ≈ 400 palabras de cuerpo** más las referencias. Sube a **≈ 480** solo si recortas el diagrama de metodología y las capturas de resultados; ese es el techo. Todo lo que pase de ahí obliga a bajar el cuerpo por debajo de 36 pt, y entonces se cae el criterio de legibilidad. **El resumen del ítem 35 es otro documento y tiene mínimo de 300 palabras: no se copia y pega aquí, ni al contrario.**

Cálculo de la línea: a 40 pt con interlineado 1,25 cada línea ocupa **17,64 mm**; en una columna de 39 cm caben **≈ 55 caracteres** por línea, es decir **≈ 9 palabras**. La estimación de caracteres usa un ancho medio de 0,5 em por carácter: es una regla de composición habitual, **no una medida tomada de la fuente**. Los altos y los ángulos de A.4 sí están medidos.

### A.4 · Tipografía

Fuente: **Calibri** (`config/universidades/cun.json` → `marca.tipografia`, `marca.fuente_titulos`, `marca.fuente_cuerpo`).

**Cómo se calcula, y qué se corrigió.** La convocatoria solo pide «legibilidad a dos metros» (PDF p.7). Para convertir eso en cuerpos se necesitan tres cosas:

1. **La altura de mayúscula real de la fuente.** Medida en el propio archivo de la fuente: `sCapHeight = 1294` sobre `unitsPerEm = 2048`, es decir **0,632**. Verificado con fontTools el 2026-08-29 en `calibri.ttf`, `calibrib.ttf` y `calibril.ttf` (los tres dan el mismo valor). Altura de mayúscula en mm = `pt × 0,352778 × 0,632` = `pt × 0,2229`.
   > **Corrección respecto de la versión anterior de este documento.** Antes se usaba un factor de **0,70** que no tenía fuente y que es falso para Calibri: infla la columna de alturas un **10,8 %**. Con 0,70, un cuerpo de 24 pt figuraba como 5,93 mm y 10,2′; medido de verdad son **5,35 mm y 9,20′**. Por eso todos los mínimos de la tabla anterior quedaban **por debajo** del criterio que el documento decía cumplir, y por eso los cuerpos de abajo suben ~11 %, redondeados hacia arriba a múltiplos de 2 pt.
   > **Si se cambia de fuente, hay que volver a medir el factor.** No es una constante tipográfica: es un dato de cada archivo de fuente.
2. **El ángulo visual a 2 metros.** 1 mm a 2.000 mm de distancia subtiende **1,71887 minutos de arco**. Combinado con lo anterior: **arcmin = pt × 0,3831**.
3. **El umbral de legibilidad.** El umbral de agudeza normal es **5′** (tamaño del optotipo estándar, agudeza 20/20). Ese es el **requisito literal** de la convocatoria: a 2 m, cualquier texto por encima de 5′ «se lee».

| Cuerpo | Altura de mayúscula | Ángulo a 2 m | Alto de línea (int. 1,25) | Px a 150 dpi | ¿Pasa el requisito literal (≥ 5′)? | ¿Entra en la holgura 15-25′? |
|---|---|---|---|---|---|---|
| **120 pt** · Título | 26,75 mm | **45,98′** | 52,92 mm | 313 | Sí | Por encima (así debe ser un título) |
| **60 pt** · Autores | 13,37 mm | **22,99′** | 26,46 mm | 156 | Sí | **Sí** |
| **54 pt** · Encabezados de sección | 12,04 mm | **20,69′** | 23,81 mm | 141 | Sí | **Sí** |
| **48 pt** · Semillero / filiación | 10,70 mm | **18,39′** | 21,17 mm | 125 | Sí | **Sí** |
| **40 pt** · Cuerpo recomendado | 8,92 mm | **15,33′** | 17,64 mm | 104 | Sí | **Sí, justo dentro** |
| **36 pt** · Cuerpo mínimo | 8,02 mm | **13,79′** | 15,88 mm | 94 | Sí | No: por debajo de la holgura |
| **28 pt** · Pies de figura | 6,24 mm | **10,73′** | 12,35 mm | 73 | Sí | No |
| **22 pt** · Referencias | 4,90 mm | **8,43′** | 9,70 mm | 57 | Sí | No |

**Las dos columnas de la derecha dicen cosas distintas, y conviene no confundirlas:**

- **«Pasa el requisito literal»** es lo que exige la convocatoria: ≥ 5′ a 2 m. Todos los cuerpos de la tabla lo pasan, incluido el de 22 pt de las referencias.
- **«Holgura 15-25′»** es un **criterio de diseño adoptado aquí, no un requisito del organizador**. La convocatoria no menciona ningún múltiplo del umbral. Se adopta porque leer al límite de la agudeza es incómodo y porque un póster se lee de pie, con gente delante y luz irregular. **No hay norma citada que respalde el rango 15-25′**: es una decisión de este documento, y se declara como tal para que cualquiera pueda discutirla o cambiarla.

**Cambios concretos frente a la versión anterior** (todos por el factor real 0,632): cuerpo mínimo **32 → 36 pt**; cuerpo recomendado **36 → 40 pt**; pies de figura **24 → 28 pt**; referencias **20 → 22 pt**. Título, autores, encabezados y filiación se mantienen en 120 / 60 / 54 / 48 pt: siguen dentro o por encima de la holgura con el factor corregido.

Reglas de composición: bandera a la izquierda, sin justificar (el justificado a 55 caracteres abre calles blancas); interlineado 1,25; encabezados de sección en azul marino `#0C2340` sobre blanco; **nunca texto de cuerpo en verde ni en azul** (`marca.reglas_de_estilo` de `cun.json`); verde CUN `#007433` solo como acento, 1-2 elementos; verde lima `#91DC00` solo como detalle, nunca como fondo ni como texto.

### A.5 · Logos: inventario medido, y el bloqueo de producción

Contenido obligatorio 1 de la p.7: «Logo de la Universidad e institución participante». Son dos logos: el de la Universidad de Cundinamarca y el de la CUN. **Uno de los dos no existe en calidad utilizable.**

**Lo que hay del lado de la Universidad de Cundinamarca** (todas las imágenes incrustadas en el PDF, medidas con pypdf + PIL el 2026-08-29):

| Imagen | Páginas | Tamaño | Modo | Máximo imprimible a 150 dpi | Qué es |
|---|---|---|---|---|---|
| `Image20.png` | 1 a 3 | **84 × 126 px** | RGBA | **1,42 × 2,13 cm** | Escudo de la UdeC (cabecera) |
| `Image50.png` | 4 a 11 | **84 × 126 px** | RGBA | **1,42 × 2,13 cm** | El mismo escudo, reincrustado |
| `Image31.jpg` | 1 | 453 × 352 px | — | 7,67 × 5,96 cm | Fotografía / banda decorativa |
| `Image32.jpg` | 1 | 812 × 607 px | — | 13,75 × 10,28 cm | Fotografía / banda decorativa |
| `Image61.png` | 6 | 219 × 278 px | — | 3,71 × 4,71 cm | Diagrama del póster (recortado en `Convocatoria/_extraccion/p6_poster.png`) |
| `Image94.png` | 11 | 115 × 50 px | — | 1,95 × 0,85 cm | Marca de pie de la última página |
| `Encuentro Latinoamericano translocal.jpg` | — | 1080 × 1080 px | RGB | 18,29 × 18,29 cm | Pieza gráfica del evento (no es un logo) |

> ⛔ **BLOQUEO DE PRODUCCIÓN. El escudo de la UdeC del PDF es inservible: 84 px de ancho son 1,4 cm impresos a 150 dpi.** Estirado a los 6 cm que pide una banda de logos en una pieza de 90 × 120 cm, quedaría a **53 dpi**: pixelado y visible desde lejos. **No se imprime el póster sin el logo institucional en condiciones**, y no se sustituye por una versión redibujada, ni recortada de la pieza gráfica, ni «mejorada» con reescalado.
>
> **Petición al organizador, ya incorporada como pregunta 9 del correo de §5 de la guía** (a `apoyosemillerosinvestigacion@ucundinamarca.edu.co`): el logotipo institucional en **vectorial (.ai, .eps o .svg)** o, en su defecto, un **PNG de 1200 px de ancho o más**; y si existe, la plantilla oficial de póster.

**Lo que hay del lado de la CUN** (verificado el 2026-08-29):

| Archivo | Tamaño | Modo | Máximo imprimible a 150 dpi | Uso |
|---|---|---|---|---|
| `config/slides/assets/logo_cun_solo.png` | **150 × 104 px** | RGBA | 2,54 × 1,76 cm | Wordmark «cun» + nombre completo, sin el sello de aniversario. **Es el logo institucional por omisión** (`marca.logo` de `cun.json`) |
| `config/slides/assets/logo_cun.png` | **300 × 104 px** | P (paleta indexada) | 5,08 × 1,76 cm | Versión con el sello «40 años» |
| `config/slides/assets/logo_nueva_america.png` | **1498 × 314 px** | RGB | 25,37 × 5,32 cm | **FESNA. NO se usa en este póster**: no hay convenio y este material es CUN |

Los tres archivos existen y están verificados, pero **son de resolución de pantalla**: el de 104 px de alto da 1,76 cm impresos, y llevado a 6 cm caería a 44 dpi. Consecuencia práctica, para no repetir el error del escudo ajeno:

1. **La fila de logos se dimensiona por lo que aguantan los archivos, no al contrario.** Con `logo_cun.png` tal cual, el alto máximo honesto es **1,7 cm**, no los 5 cm que reserva la retícula.
2. **Pide también el logo CUN en vectorial** a quien administre la marca en la institución. La nota `marca._fuente` de `cun.json` dice que el PNG salió de `https://cun.edu.co/wp-content/uploads/2025/02/logocun40.png`, recortado; esa descarga es lo que hay, y no consta que exista una versión mayor en el repositorio.
3. Regla de estilo que sigue en pie: **el logo no se reconstruye con texto ni con formas**, se usa siempre el PNG real (`marca.reglas_de_estilo`, último punto). Si no hay archivo con resolución, no hay logo: se pide.

Mientras falten los dos vectoriales, **el póster se puede maquetar pero no se puede mandar a imprimir.** Eso es lo que significa «bloqueo de producción».

### A.6 · Lo que NO va en el póster

- **Ninguna cifra de desempeño que no se haya medido.** Los preprints del portafolio son protocolos: no reportan resultados, y el conjunto de datos del 17601 es sintético. Si no hay medición, se escribe «resultados esperados».
- **Ningún semillero que no haya aceptado firmar por escrito** (bloque 4).
- **Nunca «la CUN» ni «institución aliada» al hablar de examlab.** Es propiedad personal tuya, previa y externa a tu vinculación con la CUN; sus 93 estudiantes son del tenant FESNA (`@lanuevaamerica.edu.co`) y **no hay convenio**. La forma admitida es «una institución de educación superior donde ejerzo docencia».
- **Ningún dato de identidad de terceros** —correos, celulares, documentos— sin permiso expreso de esa persona.
- **Ningún logo estirado** por encima de su resolución nativa (A.5).

### A.7 · Comprobación antes de imprimir

1. Lienzo exacto de 5.315 × 7.087 px (o 10.630 × 14.173) y proporción 3:4 vertical.
2. Ninguna imagen colocada por encima de su resolución nativa: comprobar cada una con la fórmula `px ÷ 59,06 = cm máximos`.
3. Los dos logos presentes y en calidad de impresión. Si el de la UdeC sigue siendo el de 84 px: **no se imprime**.
4. Cuerpo de texto ≥ 36 pt en todas partes; referencias ≥ 22 pt; nada por debajo.
5. Los nueve bloques obligatorios de la p.7 presentes: logo, título, autores, semillero, introducción, objetivos, metodología, resultados, conclusiones y referencias.
6. Cero cifras sin medición. Cero pronombres de tercera persona sobre personas cuyos pronombres no estén declarados.
7. PDF/X con fuentes incrustadas + PNG de respaldo, y una prueba impresa en A4 leída a 40 cm (equivalente proporcional de los 2 m sobre el original).
8. Copia del archivo final guardada en `Eventos/IV Encuentro Semilleros UdeC 2026/`.

---

## §B · Los documentos de memorias (ítem 43)

### B.1 · Qué se exige, y cuándo

Literal del ítem 43 del formulario: *«Para su inclusión, será obligatorio cargar debidamente diligenciados los siguientes documentos: 1. Formato Institucional de Memorias de Evento y 2. Autorización de Uso de Derechos de Propiedad Intelectual… a más tardar el 14 de septiembre de 2026.»*

- **Plazo: lunes 14 de septiembre de 2026 — faltan 16 días.** Es la fecha más corta y más verificable de toda la vía, y aparece en dos fuentes independientes: el ítem 43 del formulario y la p.11 del PDF.
- **El campo es obligatorio para enviar el formulario**, aunque su propio texto y la regla 5 del ítem 2 presenten las memorias como opcionales y sujetas a autorización del autor. Sin este archivo, no hay envío.
- **El widget acepta un solo archivo** («Sube 1 archivo compatible: document. Tamaño máximo: 1 GB») y el ítem pide dos documentos. Es la pregunta 2 del correo al organizador.
- Los dos formatos viven en el **OneDrive personal** de `apoyosemillerosinvestigacion@ucundinamarca.edu.co`, con enlaces con token `?e=`: **descárgalos hoy** y guárdalos en la carpeta del expediente.

### B.2 · Los dos documentos

| Documento | Qué es | Quién lo firma | Estado |
|---|---|---|---|
| `FORMATO INSTITUCIONAL DE MEMORIAS DE EVENTOS DE CTeI.docx` | La versión del trabajo que se publica en las memorias con ISBN | Los autores reales | ❌ Descargar y diligenciar. Depende de B14 |
| `AUTORIZACION DE USO DE DERECHOS DE PROPIEDAD INTELECTUAL.docx` | Cesión / licencia de uso para publicar | **Los titulares de la obra** | ❌ Descargar, **leer el alcance**, firmar |

### B.3 · Cómo se arma el archivo único

1. Diligencia los dos `.docx` por separado y guárdalos con su nombre original + `- Castaño Espinosa` al final, en la carpeta del expediente.
2. Expórtalos a PDF y combínalos en **un solo PDF**, en el orden del ítem (memorias primero, autorización después), con una portada de una línea que diga qué contiene y de quién es la ponencia.
3. Nombra el archivo final de forma que se entienda solo: `MEMORIAS + AUTORIZACION - <apellidos>_<nombre> - IV Encuentro Semilleros UdeC 2026.pdf`. El formulario no exige convención de nombre; esta réplica la de la XIII Semana.
4. **Antes de adjuntar nada, descarta que tu dominio bloquee las subidas — y hazlo SIN tocar el formulario de la Universidad de Cundinamarca.** En Google Forms el archivo se copia al Drive del propietario del formulario **en el momento de adjuntarlo**, no al pulsar Enviar: subir un «PDF de prueba» dejaría un artefacto en el Drive del organizador y sería, materialmente, una subida a una plataforma de la UdeC antes de que hayas decidido participar. Las dos formas correctas de probar: **(a)** crea **tu propio** formulario de Google desde `julian_castanoe@cun.edu.co` con una pregunta de subida de archivo y adjunta ahí un PDF mínimo; **(b)** pregunta a TI de la CUN si el dominio permite adjuntar archivos a formularios de otro dominio. Si aun así decides probar en el formulario real, que quede escrito: **es tu decisión**, el archivo queda en el Drive del organizador y hay que pedirle por correo que lo borre.
5. Guarda copia de todo lo subido en `Eventos/IV Encuentro Semilleros UdeC 2026/` antes de enviar, más una captura del campo diligenciado.

### B.4 · Antes de firmar la autorización de derechos

Léela completa. Tres cosas que ya se sabe que hay que mirar:

- **Si el objeto es examlab**, es propiedad personal tuya, previa y externa a tu vinculación con la CUN, y está marcado «Privado. Todos los derechos reservados». No se firma ninguna cesión sin saber qué cede.
- **Alcance temporal y de formato.** Hay precedente documentado de que una cláusula de tipo «en ningún formato» cierra puertas después: descartó tres revistas del portafolio (`Investigacion/Preprints 2026/REGISTRO_DE_ENVIOS.md`).
- **Secuencia invertida.** La autorización se firma antes del 14 de septiembre; la inscripción cierra el 18 de septiembre y los resultados finales salen el **6 de octubre de 2026**. Firmas la cesión **22 días antes de saber si te aprobaron**, y la p.10 del PDF dice que «los trabajos aprobados podrán ser publicados». Esa contradicción es la segunda parte de la pregunta 2 del correo.

### B.5 · Qué pasa después, con las fechas tal como están escritas

| Hito | Fecha en la fuente | Distancia desde hoy | Fuente |
|---|---|---|---|
| Carga de los dos documentos | **lunes 14 de septiembre de 2026** | 16 días | PDF p.11 e ítem 43 |
| Cierre de inscripciones | viernes 18 de septiembre de 2026 | 20 días | PDF p.11, fila 2 |
| Resultados finales | martes 6 de octubre de 2026 | 38 días | PDF p.11, fila 5 |
| **Publicación de memorias con ISBN** | **«Marzo 2027» — sin día en la fuente** | **≈ 184 días**, si se toma el 1 de marzo | PDF p.11, fila 8, literal: «Publicación de memorias — Marzo 2027» |
| **Entrega de certificaciones** | **«Noviembre 2027» — sin día en la fuente** | **≈ 429 días**, si se toma el 1 de noviembre | PDF p.11, fila 7, literal: «Entrega de certificaciones — Noviembre 2027» |

**Cómo leer las dos últimas filas.** El cronograma de la p.11 da esas dos filas con mes y año y nada más: **no traen día**. Los ≈184 y ≈429 días son aritmética correcta sobre un supuesto que el documento no declara —el día 1 de cada mes—, y por eso van marcados como aproximados y con el supuesto a la vista. Lo que no cambia por eso es el defecto de fondo:

> ⛔ **El certificado llega después de que venzan los productos que ese papel alimentaría.** SEM (`prod_1785940517692`, 200 puntos, «Certificaciones de participación en los eventos (1).») y EC_A (`prod_1785940666716`, 100 puntos, «Certificación de participación 1er evento como ponente.») vencen el **viernes 27 de noviembre de 2026**. Con «Noviembre 2027», el certificado llega **un año tarde**; con «Marzo 2027», las memorias con ISBN llegan **tres meses después** de esos vencimientos. Ni cambiando el día del mes se arregla: el desfase es de meses, no de días.
>
> Mitigación, y hay que pedirla el mismo día: **constancia de participación firmada el 4 de noviembre de 2026, en el evento.** Es la pregunta 5 del correo al organizador.

### B.6 · Lo que hay que preguntar

Las diez preguntas al organizador y las dos a la DNI están redactadas y listas para copiar en `GUIA - Inscripcion paso a paso.md`, §5. Las que afectan directamente a este documento:

- **Pregunta 2** — dos documentos en una casilla de un archivo, y la secuencia firma-antes-de-aprobación.
- **Pregunta 7** — si la Muestra de Innovación exime del póster o si el póster es obligatorio además (p.6 contra pp.8-9 e ítem 36). **De esta respuesta depende que §A haya que producirlo.**
- **Pregunta 8** — tiempos reales (15+5 en el texto de la p.8 contra 10 minutos en su propia tabla) y logística del montaje: hora de inicio y agenda del 4 de noviembre, mesa, energía, internet, pantalla con HDMI.
- **Pregunta 9** — **logo institucional en vectorial o PNG ≥ 1200 px, y plantilla oficial de póster.** Sin esto, §A no se imprime.
- **Pregunta 5** — la fecha real de las certificaciones y la constancia firmada el día del evento.

Y cuando esperes respuesta, **mira Spam antes de concluir que no han contestado**: hay precedente documentado de correo institucional que cae ahí (`REGISTRO_DE_ENVIOS.md`, §«El OJS del ITM manda su correo a SPAM»).

---

## §C · Cómo se midió cada número de este documento

| Dato | Cómo se obtuvo |
|---|---|
| 90 × 120 cm, papel bond tamaño pliego, legibilidad a 2 m, los contenidos obligatorios | `Convocatoria/INVITACIÓN FORMAL IV ENCUENTRO TRANSLOCAL.pdf`, pp.6 y 7 (texto extraído + diagrama incrustado `Image61.png`, recortado en `Convocatoria/_extraccion/p6_poster.png`) |
| Cronograma: 18/08, 14/09, 18/09, 24/09, 28-30/09, 06/10, 04/11 de 2026; «Marzo 2027»; «Noviembre 2027» | mismo PDF, p.11, extracción de celdas de la tabla CRONOGRAMA. Las dos últimas filas **no traen día** |
| Fecha de creación del PDF `D:20260821101039-05'00'` contra la carta fechada 11/08/2026 | metadatos del PDF, releídos el 2026-08-29 sobre el archivo ya movido a `Convocatoria/` |
| 5.315 × 7.087 px a 150 dpi; 59,06 px/cm; 354 px para 6 cm; 1.181 px para 20 cm | aritmética: `cm × dpi ÷ 2,54` |
| **Factor de altura de mayúscula de Calibri = 1294 / 2048 = 0,632** | fontTools sobre `calibri.ttf`, `calibrib.ttf` y `calibril.ttf`: `OS/2.sCapHeight` sobre `head.unitsPerEm`. Los tres archivos coinciden. Medición del 2026-08-29 |
| 1 mm a 2.000 mm = 1,71887′; arcmin = pt × 0,3831; altura de mayúscula mm = pt × 0,2229 | trigonometría del ángulo visual, con el factor 0,632 medido arriba |
| Umbral de 5′ | tamaño del optotipo estándar para agudeza 20/20. **Criterio externo citado**, no del organizador |
| Banda de holgura 15-25′ | **criterio de diseño adoptado en este documento, no requisito del organizador y sin norma citada** |
| Alturas de línea (interlineado 1,25) y píxeles a 150 dpi de cada cuerpo | `pt × 0,352778 × 1,25`, y ese resultado × 5,9055 px/mm |
| ≈ 55 caracteres por línea a 40 pt en 39 cm | estimación con ancho medio de 0,5 em por carácter. **No medido en la fuente**: es la única cifra estimada de A.4 |
| Tamaño y modo de las seis imágenes del PDF y de la pieza gráfica | pypdf `page.images` + PIL (`.image.size`, `.mode`), 2026-08-29 |
| Tamaño y modo de los tres logos de la CUN | PIL sobre `config/slides/assets/logo_cun_solo.png`, `logo_cun.png` y `logo_nueva_america.png`, 2026-08-29 |
| Fuente, paleta y reglas de estilo de la marca CUN | `config/universidades/cun.json` → `marca.{tipografia, fuente_titulos, fuente_cuerpo, colores, reglas_de_estilo, logo, _fuente}` |
| Correo institucional del Docente | `config/universidades/cun.json` → `docente.correo_cun` |
| Nombre completo de la institución | `config/universidades/cun.json` → `institucion.nombre_completo` (+ `acronimo`) |
| Los 48 ítems del formulario, sus textos y su obligatoriedad; las cinco casillas de archivo | censo del 2026-08-29 (`FB_PUBLIC_LOAD_DATA_` + DOM), transcrito en `GUIA - Inscripcion paso a paso.md` §2 |
| En Google Forms el archivo se copia al Drive del propietario al adjuntarlo | comportamiento del widget de subida de Google Forms. **Sin fuente en el repositorio**: es la razón por la que el punto 4 de B.3 no prueba nada contra el formulario de la UdeC |
| SEM y EC_A: identificadores, puntos, observaciones y vencimiento del 27/11/2026 | `Investigacion/dashboard/datos/productos_propios.json` |
| examlab: propiedad personal, previa y externa a la CUN; 93 estudiantes del tenant FESNA; sin convenio | `Eventos/XIII Semana de la Investigacion 2026/HOJA_DE_RESPUESTAS_Formulario.md` §«Tres cosas que hay que decidir» |
| SIAES no constituido: sin acta, sin estudiantes adscritos | `Investigacion/dashboard/datos/entregables/SEMILLERO_TODO_LISTO_RESUMEN.md` |
| `anchored-feedback` v1.0.0, DOI `10.5281/zenodo.22069535`, CC BY 4.0 + MIT | `Investigacion/Preprints 2026/REGISTRO_DE_ENVIOS.md` §«Software acompañante» |
| La cláusula «en ningún formato» descartó tres revistas; el OJS del ITM manda su correo a Spam | `REGISTRO_DE_ENVIOS.md`, secciones homónimas |
