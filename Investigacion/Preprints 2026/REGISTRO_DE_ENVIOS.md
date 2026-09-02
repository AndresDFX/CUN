# Registro de envíos — dónde está cada manuscrito

Este archivo existe porque los números de envío **no vivían en ninguna parte**. Se depositaron tres
preprints y los identificadores quedaron solo en la memoria de una sesión y en un README dentro de
una carpeta temporal. Sin el número no hay forma de consultar el estado, ni de predecir el DOI, ni
de reclamar a la moderación.

**Se anota aquí, en la misma sesión en que se deposita.** Lo mantienen los dos agentes hermanos:
`publicaciones-cun` (que deposita y escribe) y `estado-publicaciones-cun` (que vigila y lee).

Cuenta de SciELO Preprints: **`andresdfx`** · ORCID del autor:
<https://orcid.org/0009-0003-6598-432X>

---

## SciELO Preprints

El DOI **se deriva del número de envío** y por eso se conoce antes de que exista:
`10.1590/SciELOPreprints.<id>`. Mientras `https://doi.org/<ese DOI>` responda `404`, el preprint
sigue en moderación; cuando responda `302`, está aprobado y publicado.

| Manuscrito | id | Idioma | Depositado | DOI previsto | Estado |
|---|---:|---|---|---|---|
| `Preprint_Protocolo_Desercion_ML` | **17601** | es | 2026-08-21 | `10.1590/SciELOPreprints.17601` | en fila |
| `Preprint_AI_Assisted_Course_Authoring` | **17602** | en | 2026-08-21 | `10.1590/SciELOPreprints.17602` | en fila |
| `Preprint_Anchored_Feedback_Google_Docs` | **17606** | en | 2026-08-21 | `10.1590/SciELOPreprints.17606` | en fila |

Última comprobación: **2026-09-01** (sondeo Ruta B, sin credenciales). Los tres siguen en `404`, tanto
en `doi.org` como en la API de Crossref. Control de que el sondeo funciona: `…17562` devuelve `302` a
`…/preprint/view/17562/version/18445`, y `…17736` (el más nuevo de la cola) devuelve `302` a
`…/preprint/view/17736/version/18622`.

**Segunda fuente independiente, nueva el 2026-09-01: el OAI-PMH ya no está tras el escudo.**
`https://preprints.scielo.org/index.php/scielo/oai?verb=Identify` devuelve **200** (1.972 bytes de
XML válido), no el 403 de 1.830 bytes que devolvía el 2026-08-28. El identificador válido es
`oai:ops.preprints.scielo.org:preprint/<id>` (lo declara su propio `sampleIdentifier`). Consultados
hoy por `verb=GetRecord&metadataPrefix=oai_dc`:

| id | Respuesta del OAI |
|---:|---|
| 17601 | `idDoesNotExist` — «No matching identifier in this repository» |
| 17602 | `idDoesNotExist` |
| 17606 | `idDoesNotExist` |
| 17562 (control) | registro completo: título, `10.1590/SciELOPreprints.17562`, autoras, CC BY, datestamp `2026-08-21T17:31:04Z` |

Esto **corrobora** el 404 de Crossref con una fuente distinta, pero **no lo mejora**: el OAI solo
expone lo publicado, así que un rechazo también saldría como `idDoesNotExist`. La distinción entre
«en fila» y «rechazado» sigue necesitando el entero `status` de la Ruta A. Ojo, que este repositorio
declara `deletedRecord: persistent`: un registro retirado *después* de publicarse aparecería con
`status="deleted"` en la cabecera, no como inexistente — no es nuestro caso.

Id más alto publicado en el prefijo `10.1590` a esta fecha: **17736**, depositado el 2026-08-31 (el
2026-08-28 era 17675 y el 2026-08-23, 17584). **La cola ya adelantó a los tres envíos:** hay
**dieciocho** ids más altos publicados —17617, 17619, 17621, 17635, 17639, 17644, 17653, 17657,
17661, 17671, 17675, 17687, 17707, 17721, 17729, 17730, 17735 y 17736— mientras los nuestros siguen
sin DOI. **Entre 17595 y 17610 no se ha publicado ni un solo id.** Eso **no** prueba que estén
atascados, porque la moderación no es FIFO (el 25-ago se publicaron ids en un rango de 2.023 y el
26-ago en uno de 1.249), pero sí es el disparador para entrar por la Ruta A. El umbral de «silencio
prolongado» (`nuestro_id + 200`, estimación propia pendiente de recalibrar) **todavía no se ha
alcanzado**: exigiría ver publicado el 17806 y vamos por el 17736 — quedan **70 ids** de margen, así
que es previsible que se cruce en días, no en semanas.

Día 11 desde el depósito. Un `404` **no distingue «en fila» de «rechazado»**: para eso hace falta el
entero `status` de la Ruta A, y **hoy tampoco se pudo consultar**. La API de OJS sigue tras el escudo
de Bunny (**403** en `/api/v1/submissions/17601`, reverificado el 2026-09-01; lo que cambió es solo
el OAI), y el perfil de navegador `%LOCALAPPDATA%\scielo-cun\` **no existe**: en `%LOCALAPPDATA%`
hay `gdocs-cun\`, `synapse-cun\`, `revistas-cun\` y `cdigital-cun\`. La Ruta A necesita que el
Docente abra Chrome con la sesión de `andresdfx`.

**Ojo con una pista falsa, comprobada el 02/09/2026:** el perfil `revistas-cun` **sí tiene una
cookie `OJSSID` de `.preprints.scielo.org`**, así que parece que la sesión estuviera ahí. No lo
está: abrir `preprints.scielo.org/index.php/scielo/submissions` con ese perfil **redirige a
`login`**. Una cookie de sesión guardada no prueba que la sesión siga viva; lo único que lo
prueba es cargar una página que exija estar dentro.

Por tanto el estado «en fila» de la tabla es **lo último observado, no lo confirmado hoy**: es
compatible con un rechazo silencioso, que por Crossref y por OAI es invisible.

Cuando salga el DOI, se añade a la fila la URL pública
(`https://preprints.scielo.org/index.php/scielo/preprint/view/<id>/version/<pubId>`) y se lleva el
DOI a **CvLAC**, a **ORCID** y a la evidencia del producto de **Synapse**.

## Revistas indexadas

| Manuscrito | Revista | Publindex | Fecha | Estado |
|---|---|---|---|---|
| `Articulo_TecnoLogicas_Completion_Gating` | TecnoLógicas (ITM) | **B** · 8 pts | 2026-08-25 | **consulta de pertinencia enviada** |
| `Preprint_Protocolo_Desercion_ML` (17601) | EDU REVIEW (Edulab, ES) | **ninguna** · 0 pts | **2026-08-27** | **SOMETIDO** · envío **5579** · «Envío completo», en Revisión |
| `Preprint_AI_Assisted_Course_Authoring` (17602) | ITEES (EIDEC) | sin comprobar | 2026-08-27 | **envío 596 A MEDIAS** — falta el tipo de archivo, ver su sección |
| `Preprint_Anchored_Feedback_Google_Docs` (17606) | **ninguna viable hoy** | — | 2026-08-28 | **NO SE ENVIÓ** — dictamen aquí abajo |

### 28/08/2026 — el 17606 NO se envió a ninguna parte, y el motivo es firme

Se buscó destino para `Preprint_Anchored_Feedback_Google_Docs` (**17606**, inglés) y **no hay ninguno
firmable hoy**. Queda anotado para no repetir la búsqueda; el dictamen completo, con la cita literal
de cada web, está en **`DESTINOS_BASE_DE_DATOS_ARTICULOS.md`**.

Con la cláusula «en ningún formato» fuera de juego (CEA, TecnoLógicas y Revista Virtual UCN, más
abajo), las únicas dos candidatas eran EDU REVIEW e ITEES, y **cada una falla por un motivo
distinto**. Ninguno de los dos se arregla con una carta:

| Revista | ¿Se puede firmar su casilla 1? | Por qué no se envió |
|---|---|---|
| **EDU REVIEW** | **sí** — su política admite el preprint | **por extensión**: su umbral más bajo para un texto académico son **3.000** palabras y el 17606 no llega ni contando el archivo entero |
| **ITEES** | **sí** — por la salvedad de su casilla 1 | **no declara si cobra**, **no publica normas de autor ni extensión**, no consta que acepte el cuerpo en inglés, y su envío **596** sigue a medias |

**Lo que el manuscrito es, medido hoy sobre el archivo** —que no ha cambiado desde el 23/08—: **1.486
palabras de cuerpo** (§1–§6), **1.744** con las declaraciones y **2.785** el archivo entero sin
excluir nada, ni abstracts ni referencias. **16** referencias APA 7 sin DOI (el «17» que decía aquí
se contó mal; y desde el 01/09 son **17** de verdad, al añadirse la fuente de Google), cero tablas,
cero figuras,
cero marcadores `[PENDIENTE]`. El **1.479** anotado el 26/08 es el mismo texto contado de otra forma.
Género: resultado negativo con solución alterna sobre una limitación documentada de la API de Google
Docs, más el reporte de un incidente. No mide nada y lo declara: «No student data are reported and no
learning outcome is claimed.»

**EDU REVIEW falla por extensión, no por política.** Sus tres condiciones se verificaron hoy y están
por escrito: «Coste de publicación: gratuito», «Se permite también la difusión pre-print del
artículo» y publicación «de manera inmediata» (recepción continua). Lo que la cierra son sus umbrales
**por tipo de envío**, en `edulab.es/revEDU/typesofsubmissions`: investigación mín. **5.000**,
**reflexión crítica mín. 3.000** ← el más bajo, revisión sistemática mín. **5.000**, monográfico por
propuesta, **reseñas 800–1.500**, vídeos académicos. La regla excluye del cómputo resúmenes, palabras
clave y bibliografía. **No existe convención de conteo que lleve el 17606 a 3.000**: no es un caso
límite negociable con el editor.

> **La trampa que no hay que morder.** La ventana de **«Reseñas» (800–1.500)** encaja al milímetro con
> las 1.486 palabras del 17606. Es una coincidencia sin valor: una reseña es, con las palabras de la
> revista, un texto «a través de los cuales se da a conocer el contenido de un libro de interés
> académico». Esto no es un libro ni una reseña de nada. Meterlo ahí para que cuadre el número es
> **declarar un género falso**: rebote de mesa y una firma que no se sostiene. Queda escrito para que
> nadie redescubra la coincidencia y la tome por una puerta.

**ITEES sí es firmable, pero hoy no se le manda un segundo manuscrito.** Su casilla 1 trae la salvedad
expresa —así se usó en el 596— y declara acceso libre inmediato con CC BY-NC-ND 4.0. Lo que decide es
lo que **no** publica: **no dice en ninguna parte si cobra al autor** (se buscaron «APC», «cargo»,
«cobro», «tarifa», «gratuito», «pago» y «fee» en sus páginas de envíos y de políticas: ni una
mención, y acceso gratuito **para el lector** no es lo mismo), su pestaña **«Author Guidelines» está
vacía** mientras anuncia una «Revisión equipo Editorial» que juzga «criterios de fondo y forma según
las normas de la revista», y **no consta que acepte el cuerpo en inglés**. Las dos primeras preguntas
ya van escritas en la carta del 596 y **siguen sin contestar**. Encima el 596 está a medias en esa
misma revista y esa misma sección («Artículos de Reflexión»): abrir un segundo envío antes de cerrar
el primero, en una cuatrimestral y con un solo autor firmante, es quemar el trato.

**Qué se hace en su lugar, en este orden:**

1. **Terminar a mano el envío 596** (`Envio_ITEES_17602/_COMO_TERMINARLO.md`). No es solo cerrar el
   17602: **la respuesta del editor resuelve las dos incógnitas —cargos e inglés— que hoy bloquean a
   ITEES como destino del 17606**. Es a la vez la acción urgente y el paso que produce la información
   que falta.
2. **Decidir el alcance del 17606**, que es de `escritor-investigacion-cun` y no de aquí: o crece a
   **≥3.000 palabras de cuerpo** —le faltan unas **1.520**— y va a EDU REVIEW como «Artículo de
   reflexión crítica», o espera la respuesta de ITEES y va a «Artículos de Reflexión». El material
   para crecer honestamente ya está dentro del manuscrito: la evidencia documental de §2, el incidente
   de §4, los límites de §5.3 y las dos líneas de trabajo futuro de §6. **Crecer no es añadir ninguna
   cifra: el manuscrito no mide nada y no debe empezar a hacerlo.**
3. **No mandarlo como reseña a EDU REVIEW.**

**Que no haya destino hoy no cuesta nada en el expediente:** `ART_OPEN_D` ya está cubierto en lo
esencial por el sometimiento 5579 del 17601, y lo que falta ahí es el correo de acuse, no otro
sometimiento. Un rebote de mesa sí costaría.

**Disciplina de acceso del dictamen:** 2 accesos a `revistaseidec.com` y 3 a `edulab.es`, y el resto
parseando el HTML ya descargado. Sin credenciales, sin tocar ningún formulario y sin pulsar nada a
nombre del Docente.

### 27/08/2026 — SOMETIDO a EDU REVIEW: envío 5579

Primer sometimiento a revista de esta carpeta. **Constancia:**

| Dato | Valor |
|---|---|
| Revista | EDU REVIEW. International Education and Learning Review · **ISSN 2695-9917** · Edulab (España) |
| Identificador del envío | **5579** |
| Fecha | **27 de agosto de 2026** |
| Sección | Artículos de investigación |
| Idioma | Español (con título y resumen también en inglés) |
| Estado | **«Envío completo»**, el flujo marca *Revisión* y no aparece como incompleto |
| Archivos | `19021` Manuscrito_ciego.docx · `19022` Portada_con_autoria.docx · `19023` Carta_de_presentacion.docx |
| Evidencia | `Envio_EDU_REVIEW_17601/_evidencia_envio_5579.png` (captura del panel del autor) |
| Panel | <https://edulab.es/revEDU/authorDashboard/submission/5579> |

**Lo declarado al editor, por escrito en «Comentarios al editor»:** que el manuscrito está depositado
como preprint en SciELO Preprints (**17601**, DOI previsto `10.1590/SciELOPreprints.17601`), que no
está publicado ni sometido en otro medio, que **el conjunto de datos es sintético** y que **es un
protocolo y no reporta resultados**. Las dos últimas se comprobaron guardadas en el resumen del
envío, no solo en la carta.

> **2026-08-28 · no verificado hoy.** `edulab.es` está en pie: la ruta del panel del autor de 5579
> devuelve `302` al login, que es lo normal sin sesión. **Eso no dice nada del estado del envío** —OJS
> redirige igual para cualquier id, exista o no—, y el panel es justamente la única superficie válida
> (el formulario del paso 3 se pinta vacío aunque haya guardado). Para saber si sigue en *Revisión*
> hay que entrar con la credencial de `%LOCALAPPDATA%\revistas-cun\credenciales.json`, y este agente
> no la usa. **Sigue pendiente el correo de acuse**, que es la pieza que falta para radicar.

**Riesgo señalado el 28/08 y sin resolver.** EDU REVIEW «utiliza Turnitin … detectando plagio y
autoplagio», y avisa de que «el incumplimiento en la fase inicial de evaluación llevará al **rechazo
automático** del envío». El 17601 **coincidirá con su propio preprint de SciELO**. Es defendible —el
preprint va declarado por escrito al editor y la política de la revista lo admite—, pero conviene
vigilar esa respuesta y **no confundir un rechazo automático de mesa con un juicio de fondo**.

**Sirve para el producto `ART_OPEN_D` de Synapse**, que se cumple con la constancia de sometimiento
y no con la aceptación. Para radicarlo faltan el correo de acuse de la revista (la revista avisa que
lo manda) y el PDF del manuscrito enviado. **Publindex: ninguna, 0 puntos** — EDU REVIEW no está en
Scopus ni WoS.

#### Tres cosas del formulario que no están en sus normas de autor

Costaron varios intentos y conviene no volver a descubrirlas:

1. **Hay un campo «Citas» OBLIGATORIO.** El paso 3 no guarda nada y no dice por qué hasta que se
   inspeccionan los errores: «Citas* Este campo es obligatorio». Hay que **pegar la lista completa de
   referencias** en ese campo. Se pegaron las **52** del manuscrito (9.687 caracteres), extraídas por
   párrafo y no por línea —por línea salen 109 fragmentos, porque las referencias vienen partidas—.
2. **El resumen no puede pasar de 200 palabras.** El del manuscrito tenía **234**. Se recortó a
   **189** (y el inglés a 177) conservando intactas las dos declaraciones no negociables. Las normas
   públicas de la revista no mencionan ese límite; lo dice el propio formulario.
3. **El paso 3 se pinta vacío al recargarlo, aunque haya guardado.** No sirve como comprobación:
   parece que se perdió todo cuando no es cierto. Lo que sí vale es el **panel del autor**
   (`/authorDashboard/submission/5579`), que muestra el título y el resumen reales.

### 26/08/2026 — revisión de la «BASE DE DATOS ARTÍCULOS» y paquete para EDU REVIEW

Se revisaron los 56 enlaces de `BASE DE DATOS ARTÍCULOS.docx`. El análisis completo, revista por
revista y con cita textual de cada sitio, está en **`DESTINOS_BASE_DE_DATOS_ARTICULOS.md`**. Tres
cosas que cambian decisiones:

**La mitad de la lista no son destinos.** 28 de las 56 filas apuntan a ResearchGate, Dialnet,
Redalyc o repositorios institucionales. Ahí no se somete nada. Quedan **19 revistas reales**.

**Dos de esos destinos cobran.** Migration Letters **1.100 USD** por artículo aceptado y Espacios
**150 USD**. Que un enlace figure en la lista de publicaciones de la CUN no dice que su revista sea
gratuita.

**Destino nuevo verificado: EDU REVIEW** (Edulab, España, `2695-9917`). Es el único de la lista que
reúne las tres condiciones a la vez, y las tres están por escrito en su web: **«Coste de
publicación: gratuito»**, **«Se permite también la difusión pre-print del artículo»** y recepción
continua. Ámbito: educación y aprendizaje. Vive: v14(1) del 30/06/2026. Indexada en REDIB, EBSCO,
Dialnet, ERIH Plus, Latindex — **no en Scopus ni WoS, así que Publindex no la homologa y da 0
puntos**. Sirve para el producto de acceso abierto, no para sumar categoría.

Segundo destino, colombiano: **Revista Virtual UCN** (`0124-5821`), sin cargos por escrito y con
recepción permanente declarada para los tres números de 2027.

**Paquete preparado en `Envio_EDU_REVIEW_17601/`**, comprobado programáticamente:

| Archivo | Qué es |
|---|---|
| `Manuscrito_ciego.docx` | 8.077 palabras · **0 fugas de identidad**, 0 marcadores pendientes |
| `Portada_con_autoria.docx` | Autoría, filiación, ORCID y declaraciones de financiación |
| `Carta_de_presentacion.docx` | Declara el preprint 17601, la naturaleza sintética del conjunto y que es un protocolo |
| `_MARCADOR_RETIRADO.txt` | Copia literal de lo que se quitó, para poder reponerlo |

Se eligió este manuscrito porque **es el único de los tres que cumple la extensión**: 6.027 palabras
de cuerpo contra el rango 5.000–9.000 de la revista. Los otros dos se quedan muy cortos —**1.717** el
17602 y **1.479** el 17606— y su problema no es de revista sino de formato.

> **Corregido el 28/08/2026 — ese rango no es «de la revista».** Es el de los **artículos de
> investigación**. EDU REVIEW tiene **seis tipos de envío con umbrales distintos**, y el mínimo más
> bajo para un texto académico es **3.000** palabras («Artículos de reflexión crítica»), no 5.000. Los
> huecos reales son por tanto **unas 1.300** palabras en el 17602 y **unas 1.520** en el 17606 —no
> 3.300 ni 3.500—. Siguen sin alcanzar, pero cambia cuánto hay que escribir. Detalle en el dictamen
> del 28/08, arriba.

**Dos marcadores bloqueaban el envío**, uno rotulado «ANTES DEL SOMETIMIENTO»:

1. El **ABSTRACT inglés decía lo contrario que el RESUMEN español**: conservaba
   `[PENDING: summary of the main results…]` cuando el español ya se había corregido a «por tratarse
   de un protocolo, no se reportan resultados». **Corregido en el original.**
2. El **marcador de SPADIES**. Se intentó la fuente oficial y **ni `spadies3.mineducacion.gov.co` ni
   el micrositio del MEN respondieron**. No se inventó ninguna tasa. En la copia de envío se retiró
   el hueco; el original queda intacto y lo retirado está guardado literal.

**Lo que falta es el clic.** Crear la cuenta en el OJS de la revista pide verificación por correo y
reCAPTCHA, y someter a nombre del Docente es irreversible: **no se envía sin su visto bueno en ese
momento**. Igual que con TecnoLógicas.

**Sin resolver, y son preguntas de una línea:** si Sinergias Educativas admite preprints
(`revistasinergia@soyuo.mx` — dice **«no acepta material previamente publicado»**, el mismo riesgo
del candado), si ITEES cobra (`revistaitees@eidec.com.co`), y qué dicen las dos revistas de la casa
—**Ignis y Opinión Pública—, que no se pudieron revisar porque `revistas.cun.edu.co` está detrás de
BunkerWeb** y hay que abrirlas a mano en el navegador.

### 25/08/2026 — consulta de pertinencia a TecnoLógicas

Enviada desde `julian_castanoe@cun.edu.co` a **tecnologicas@itm.edu.co**, asunto «Consulta de
pertinencia tematica - auditoria de configuracion en Moodle 4.5». Comprobado en Enviados: **una
sola copia**, sin borradores colgando. El texto está en `CORREO_Consulta_pertinencia_TecnoLogicas.md`.

Se preguntan dos cosas:

1. **Pertinencia temática.** Es el riesgo número uno del envío: «docencia» no está entre las nueve
   áreas que declara la revista, y hay una fase de evaluación editorial que decide expresamente si
   el trabajo cabe. Se argumenta que entra por Ciencias de la Computación —auditoría instrumentada
   de la configuración de un sistema desplegado, verificada contra el código fuente de la rama
   `MOODLE_405_STABLE`— y que el aula es el caso de validación, no el objeto.
2. **Qué cifra rige para el resumen.** La guía de autor pide 250-300 palabras y la lista de
   comprobación pide 200-250. El manuscrito se preparó con 249 y 5 palabras clave por idioma, que
   cumple las dos a la vez.

**Mientras no contesten, no se toca nada más.** Maquetar en la plantilla del ITM antes de esa
respuesta es tirar tres horas. Si dicen que no cabe, el destino es ACOFI (C, 3 puntos), que es el
mejor encaje temático de la lista pero **solo admite un artículo por autor y año**.

**Pendiente cuando contesten que sí:** maquetación en la plantilla Word del ITM (Montserrat, 10 pt,
tablas como tablas y no como imagen), carta de presentación, tres evaluadores propuestos —los pone
el Docente, no se inventan— y la cuenta en su OJS, que tiene reCAPTCHA y se crea a mano.

**Dos decisiones del Docente, abiertas:** si el artículo va con el nombre de la CUN y con los
identificadores reales de las siete aulas (`129268`, `112321`, `6522210`…), o anonimizado; y si la
decanatura o la DNI lo saben antes de la publicación.

## ⚠️ La cláusula «en ningún formato» descarta tres de las cinco revistas

Descubierto el 27/08/2026 al intentar someter el **17602**. Es el hallazgo que más condiciona el
plan, porque **no es un problema de encaje temático sino de integridad**: hay revistas cuya
declaración de originalidad **no se puede firmar** con un preprint depositado, y las tres primeras
preguntas de sus listas de comprobación lo dicen con estas palabras:

| Revista | Casilla 1 de su lista de comprobación | ¿Se puede firmar con preprint? |
|---|---|---|
| **Revista CEA (ITM)** | «original and unpublished … **has not been published in any format**» | **NO** |
| **TecnoLógicas (ITM)** | la misma cláusula (de ahí el candado del 25/08) | **NO** |
| **Revista Virtual UCN** | «no ha sido publicado ni aceptado ni presentado para publicación en otra revista **o sitio web en internet**» | **NO** — es aún más estricta |
| **ITEES (EIDEC)** | «El envío no ha sido publicado previamente ni se ha sometido a consideración por ninguna otra revista **(o se ha proporcionado una explicación al respecto en los Comentarios al editor/a)**» | **SÍ**, declarándolo |
| **EDU REVIEW** | «Solo publicamos artículos originales e inéditos … garantizan la originalidad y la inexistencia de plagio, **incluido el auto-plagio**» — y su política editorial añade: «**Se permite también la difusión pre-print del artículo**» | **SÍ**, por esa política |

Las casillas de **ITEES** y **EDU REVIEW** se releyeron literales el **28/08/2026** en
`revistaseidec.com/index.php/ITEES/about/submissions` y `edulab.es/revEDU/about/submissions`, y siguen
igual. Ojo con la de EDU REVIEW: **su casilla 1 no menciona los preprints** y habla de auto-plagio; lo
que la hace firmable es su política editorial, que los admite por escrito.

**Consecuencia práctica.** De las cinco cuentas creadas, **solo EDU REVIEW e ITEES sirven para los
tres manuscritos depositados** (17601, 17602, 17606). Las tres restantes quedan reservadas de hecho
para material **no difundido**, que hoy es únicamente `Preprint_Completion_Gating_Moodle` —el del
candado—. Y el candado, visto esto, protege más de lo que se creía: no solo TecnoLógicas, también
CEA y UCN.

**No se marcó la casilla de CEA.** Se abandonó ese envío antes de empezar y se borró su carpeta de
paquete. Firmar «has not been published in any format» con el 17602 depositado en SciELO habría sido
declarar algo falso.

## Envío en curso · ITEES 596 (manuscrito 17602)

**A medias, y le faltan dos clics.** Instrucciones completas en
`Envio_ITEES_17602/_COMO_TERMINARLO.md`.

| Dato | Valor |
|---|---|
| Revista | ITEES · EIDEC (Colombia) |
| Envío | **596** · sección **Artículos de Reflexión** (id 18) |
| Paso 1 | **completo** — con el **preprint 17602 declarado por escrito** al editor, acogiéndose a la salvedad de su lista de comprobación |
| Paso 2 | **tres archivos subidos** (`1486` manuscrito ciego · `1487` portada · `1488` carta) |
| Bloqueo | **falta asignar el tipo a cada archivo**: «Texto del artículo» al manuscrito, «Otro» a los otros dos |

**Por qué se quedó ahí.** El botón de tipo es un componente Vue que **no reacciona a clics
automatizados**, y la vía de la API —`PUT …/files/<id>` con `{"genreId": 37}` («Texto del artículo»)
o `48` («Otro»)— **devuelve HTTP 403**: el servidor no admite esa escritura. Tras unos quince
accesos automatizados, el sitio **dejó de aceptar conexiones** de esta máquina —el dominio resolvía
pero las conexiones expiraban—. Se dejó de insistir a propósito. **Fue temporal: el 28/08 ya volvía a
responder** (nota de abajo).

En la carta se le preguntan además dos cosas al editor: **si la revista cobra** —no lo publica en
ninguna parte— y **si acepta el cuerpo en inglés**, con el compromiso de traducirlo si no.

> **2026-08-28 · la limitación por tasa se levantó.** `revistaseidec.com` vuelve a responder:
> `HTTP 200` en la portada de ITEES y `302` al login en la ruta del asistente del envío 596, que es
> la respuesta normal sin sesión. **Se hicieron tres accesos y se paró**, para no volver a agotar el
> cupo. Esto solo dice que **el sitio es alcanzable**: el estado interno del envío 596 —si sigue
> faltando el tipo de archivo— **no se comprobó**, porque el asistente exige sesión y este agente no
> entra con la credencial. La ventana para terminarlo a mano está abierta.

**Lo que ITEES no publica, comprobado el 28/08.** Las dos preguntas de la carta **no se pueden resolver
en su web, y no por descuido de la búsqueda**: no hay una sola mención de «APC», «cargo», «cobro»,
«tarifa», «gratuito», «pago» ni «fee» en sus páginas de envíos y de políticas —lo que declara es acceso
libre **para el lector**, con CC BY-NC-ND 4.0, que no es lo mismo que sin cargos para el autor—, y su
pestaña **«Author Guidelines» está vacía**, con un enlace de plantilla a
`ojs3modern8.openjournalsystems.com` todavía puesto: **no publica extensión ni normas de autor**. Por
eso ITEES tampoco se pudo usar hoy como destino del **17606** (dictamen del 28/08, arriba), y por eso
**la respuesta del editor al 596 vale doble**: cierra este envío y desbloquea el otro.

## Cuentas en los OJS de las revistas

Las crea `config/revistas/registrar_revistas.py`. **Las claves NO están en este repositorio**: van
en `%LOCALAPPDATA%\revistas-cun\credenciales.json`, una distinta por revista, generadas con
`secrets`. Usuario en todas: **`jcastanoe`** · correo `julian_castanoe@cun.edu.co`.

| Revista | Captcha | Cuenta | Comprobada |
|---|---|---|---|
| Revista Virtual UCN | ninguno | **creada** 2026-08-26 | **sí** — entra con la credencial |
| ITEES (EIDEC) | ninguno | **creada** 2026-08-26 | **sí** — entra con la credencial |
| TecnoLógicas (ITM) | reCAPTCHA v2 | **creada y ACTIVA** 2026-08-26 | **sí** — entra con la credencial |
| Revista CEA (ITM) | reCAPTCHA v2 | **la misma del ITM, activa** | **sí** — reconoce la sesión |
| **EDU REVIEW** | reCAPTCHA v2 | **creada y ACTIVA** 2026-08-26 | **sí** — entra con la credencial, sin validación por correo |

### ⚠️ El OJS del ITM manda su correo a SPAM

La cuenta del ITM nació **deshabilitada** («Your account has been disabled… **We've sent a
confirmation email to you**») y el correo de validación **no estaba en Recibidos: estaba en Spam**,
como «TecnoLógicas via Op. Spam — [tl] Validate Your Account». Ahí se quedó parada.

Se activó abriendo ese mensaje y siguiendo su enlace, que además viene **envuelto en un rastreador**
(`track.pstmrk.it/...`) y cuya ruta real no es `validate` sino
`…/tecnologicas/user/activateUser/jcastanoe/<token>`. Comprobado después: **entra en TecnoLógicas y
CEA reconoce la sesión**, lo que confirma que una sola cuenta cubre las dos revistas del sitio.

**Y esto importa más allá del registro:** hay una **consulta de pertinencia esperando respuesta de
`tecnologicas@itm.edu.co`** desde el 25/08. Si el correo de esa instalación cae en Spam, **la
respuesta editorial también puede caer ahí**. Mirar Spam antes de concluir que no han contestado.

UCN e ITEES no pidieron validación: entraron directo.

**Lo que confirma que una cuenta existe** no es que la página redirija —OJS redirige igual cuando
falla— sino una de estas dos: que **entre con la credencial**, o que al reintentar el registro el
OJS lo rechace con «El nombre de usuario seleccionado ya está siendo utilizado». Las dos pruebas se
corrieron.

**Diagnóstico de EDU REVIEW, para no repetirlo.** Tras dos esperas agotadas se comprobó si el
problema era del formulario: el reCAPTCHA **renderiza bien** (sitekey `6Lc2teAU…`, widget de
800×78, dos iframes) y al enviar a propósito sin resolverlo **el único error que devuelve es
«Obligatorio»** —no dice que el usuario o el correo estén cogidos—. Conclusión: la cuenta **no
existe todavía**, el formulario está correcto y lo único que falta es el clic humano. Por eso el
guion ahora **pinta un cartel dentro de la propia página** con la instrucción y el nombre de la
revista: en las dos primeras corridas nada en pantalla decía qué se esperaba.

### Se agotaron las plataformas gratuitas registrables sin captcha

Se sondearon **todas** las revistas gratuitas de la lista, no solo las cinco primeras. El reparto
final es este, y explica por qué no se puede llegar más lejos sin la mano del Docente:

| Situación | Revistas |
|---|---|
| **Cuenta creada y activa** (5) | **EDU REVIEW** · Revista Virtual UCN · ITEES · TecnoLógicas · Revista CEA |
| **Formulario listo, pide reCAPTCHA v2** (3) | Revista NODO (UAN) · **Ignis (CUN)** · **Opinión Pública (CUN)** |
| **No tienen formulario de registro** (2) | HUMAN REVIEW (Eagora) · Sinergias Educativas |

**El destino 1 ya tiene cuenta.** EDU REVIEW se registró al primer envío en cuanto se marcó el
captcha, y el login confirma que la cuenta está **activa sin necesidad de validar el correo**. Con
esto, someter el **17601** solo depende de subir los tres archivos de `Envio_EDU_REVIEW_17601/` —y
de que el Docente lo autorice, porque someter sigue siendo irreversible.

**Lo que costó y por qué merece anotarse:** cinco intentos. Los cuatro primeros se agotaron porque
el guion pedía «resuelve el captcha **y pulsa Registrarse**», y el token de reCAPTCHA v2 caduca en
unos dos minutos: el único intento que llegó a enviarse murió con «No superó la comprobación de
validación utilizada para evitar envíos de spam». El quinto funcionó a la primera con el cambio de
diseño —el guion **detecta el token y envía él mismo**— y con la ventana dedicada a una sola revista
en vez de recorrer cuatro, que gastaba la atención del Docente en la de peor encaje.

Las dos últimas no es que no se puedan automatizar: su `/user/register` **no trae ningún campo ni
botón** —comprobado, en HUMAN REVIEW incluso tras aceptar el aviso de cookies que tapaba la
página—, así que esa vía está cerrada también a mano. Quedan anotadas en el guion
(`SIN_FORMULARIO_DE_REGISTRO`) para que nadie lo reintente.

**Para terminar las cuatro que faltan**, todas de un solo clic cada una:

```bash
python -u config/revistas/registrar_revistas.py --espera 3600
```

Abre Chrome, salta las cuatro cuentas ya creadas, y en cada pendiente rellena el formulario y pinta
un cartel azul. **Solo hay que marcar «No soy un robot»**; el guion envía en el instante. Con
`--solo edu` va únicamente al destino 1, que es el que importa para el manuscrito 17601.

> **Marca solo el reCAPTCHA. No pulses «Registrarse»: lo envía el guion.**
>
> El token del reCAPTCHA v2 **caduca en unos 2 minutos**, y ahí se perdió el tercer intento: el
> formulario llegó a enviarse y EDU REVIEW contestó «**No superó la comprobación de validación
> utilizada para evitar envíos de spam**» —el captcha estaba marcado, pero el token ya había
> expirado—. No era un fallo del formulario: el widget renderiza bien y el usuario no está cogido.
>
> Arreglado en el guion: `captcha_resuelto()` lee el token de
> `textarea[name=g-recaptcha-response]` sondeando cada 1,5 s y **envía el formulario en el instante
> en que aparece**, sin depender de que nadie pulse a tiempo. Si OJS lo rechaza, rellena otra vez y
> permite re-marcar, hasta 4 intentos. El cartel de la página lo dice: marcar sí, pulsar no.

**El sondeo de las cinco** (`config/revistas/_sondear_registro.py`, solo lectura) encontró que los
cinco son OJS 3 con los mismos nombres de campo, y que **el captcha no está donde se suponía**: dos
de las cinco no tienen ninguno y se registran sin intervención. Las otras tres llevan reCAPTCHA v2,
que el guion **no intenta resolver ni rodear**: rellena todo lo demás y sondea la página hasta que
el Docente lo resuelve en la ventana.

**Cómo se comprobó que la cuenta existe.** Que la página de registro redirija no prueba nada: OJS
redirige igual cuando falla. La única prueba que no miente es **entrar con la credencial guardada**,
y es la que se corrió. Las dos primeras entraron y dejaron sesión abierta.

**Dos cosas quedan abiertas en cada cuenta creada:** meter el **ORCID** en el perfil
(`0009-0003-6598-432X`) —OJS no lo pide al registrarse— y atender el correo de validación si la
revista lo manda. Y una decisión del Docente: en el registro se dejó **sin marcar** la casilla de
ofrecerse como evaluador, porque compromete a revisar para esa revista.

## ⚠️ Solicitud depredadora recibida — 26/08/2026

Llegó a `julian_castanoe@cun.edu.co` un correo de **`vjmcr@openaccesreserchgroup.com`** firmado
«Eunice», con asunto «Opportunity to contribute an article : Journal of Research and Education»,
invitando a someter antes del **11 de septiembre de 2026**. **No se responde y no se somete nada.**

Lo que lo delata, comprobado y no supuesto:

| Señal | Comprobación |
|---|---|
| El dominio **no existe** | `openaccesreserchgroup.com` **no resuelve por DNS** |
| **No puede recibir respuesta** | **no tiene registro MX**: contestar no llega a ninguna parte |
| No es una imitación de algo real | la versión bien escrita, `openaccessresearchgroup.com`, **tampoco resuelve** |
| El nombre está mal escrito **dos veces** | «open**acces**» y «**reserch**» |
| Adulación con texto de plantilla | «Your work has made a significant impact in the field of **Journal of Research and Education**» — usa el nombre de la revista como si fuera un campo del saber |
| Urgencia con fecha | plazo a dos semanas, el patrón habitual |
| Sin ISSN, sin editor, sin comité, sin decir si cobra | nada verificable |

Para contrastar: el otro correo del mismo día, el de validación del OJS del ITM, viene de
`notificaciones@biteca.online`, y **`biteca.online` sí resuelve** (67.205.25.183). Es legítimo: es
el servicio que hospeda el OJS del ITM.

### Lo que sí inquieta de ese correo

Cita el título **exacto y completo** de `Preprint_Completion_Gating_Moodle.md` —«An Ungraded Survey
Can Gate a 32.8% Assignment: Template Dates, Completion Restrictions, and Audit Blind Spots in
Seven Moodle Course Instances»—, que es **el manuscrito bajo candado, el que no se ha depositado en
ningún sitio**. No es la versión corta que se mandó a TecnoLógicas. Un título de veinte palabras no
se adivina.

Se buscó de dónde pudo salir, y **las cuatro vías dieron negativo**:

| Vía | Resultado |
|---|---|
| SciELO Preprints (título, autor, «Completion Gating») | sin rastro |
| ORCID `0009-0003-6598-432X` | **0 obras públicas** |
| El correo a `tecnologicas@itm.edu.co` | llevaba **solo el título corto** |
| Google Drive | los 4 archivos dan **HTTP 401 sin sesión**: privados |

La búsqueda en web abierta quedó **inconcluyente** (el selector del buscador no devolvió nada
utilizable), así que no se puede afirmar que no esté indexado en ninguna parte.

**⛔ CORREGIDO EL 2026-08-28. El manuscrito está público y la declaración ya no se puede firmar.**
Lo que decía este párrafo —«hoy no hay evidencia de difusión pública, así que la declaración de *no
publicado en ningún formato* sigue sostenible»— es **falso**. Comprobado en Crossref el 28/08:

| Dato | Valor |
|---|---|
| DOI | **`10.32388/z2uxxt`** |
| Tipo · editor | `posted-content` · **Qeios Ltd** |
| `posted` · `created` | 2026-08-25 · 2026-08-25T13:36:58Z |
| Licencia | **CC BY 4.0** (irrevocable) |
| Autor | Julian Andrés Castaño Espinosa (en Crossref el ORCID va **nulo** y la filiación **vacía**) |
| Título | coincide palabra por palabra con `Preprint_Completion_Gating_Moodle.md` |

Consecuencias, en orden de gravedad:

1. **La casilla 1 de TecnoLógicas, CEA y UCN ya no se puede firmar para este manuscrito**, y con eso
   se queda sin material el único destino Publindex **B** de la lista (8 puntos).
2. **Existía una vía de difusión pública anterior** al correo depredador del 26/08 que citaba el
   título exacto. Eso no prueba de dónde salió ese correo —el origen sigue sin establecerse—, pero
   tumba la premisa con la que se cerró la búsqueda.
3. **Lo institucional, que es lo grande:** el texto audita la mala configuración de siete aulas de
   la CUN y está en abierto sin que nadie de la institución lo sepa. Retirarlo no lo arregla: CC BY
   es irrevocable y Crossref ya tiene el registro. **Hay que averiguar quién depositó, cuándo y con
   qué versión**, entrando a `qeios.com` con la cuenta asociada al correo institucional; si no hay
   cuenta, es uso no autorizado de esa identidad. En este mismo directorio existe un
   `Preprint_Completion_Gating_Moodle.pdf`, así que el paquete para depositarlo estaba listo.
4. **No añadir obras al perfil de Google Académico** que hay que crear antes del 31/08: Qeios
   declara indexación en Scholar, y este texto sería la única obra visible bajo filiación CUN. El
   producto se cierra con un perfil verificado y vacío, que es lo único que pide su observación.

De lo que quedaba sin mirar sigue pendiente una sola cosa, y la puede hacer solo el Docente: **qué
hay en su lista de envíos de SciELO**, que necesita su clave. Los cuatro archivos de Drive dan HTTP
401 sin sesión.

## Software acompañante

| Paquete | Preprint al que acompaña | Depósito |
|---|---|---|
| `anchored-feedback` v1.0.0 | 17606 | **Zenodo, 2026-08-23.** DOI de versión `10.5281/zenodo.22069535`, DOI de concepto `10.5281/zenodo.22069534` · tipo Software · CC BY 4.0 + MIT · autor «Castaño Espinosa, Julian Andrés» |

> Corregido el 2026-08-28: esta fila decía **«sin depositar»** y es falso. Verificado en la API de
> DataCite (`api.datacite.org/dois/10.5281/zenodo.22069535`): `registered 2026-08-23T14:43:08Z`,
> `version 1.0.0`, `IsVersionOf 10.5281/zenodo.22069534`. Son **dos DOI del mismo objeto** (concepto
> y versión), no dos depósitos distintos — de ahí el `works_count` inflado en OpenAlex. En la ficha
> de DataCite la **filiación del autor va vacía y sin ORCID**.

## Producto de Synapse al que responden

`productTypeId: ART_OPEN_D` — «Artículos de investigación con Calidad D (acceso abierto)»,
`prod_1785940748621`, vence **2026-11-20**. El emparejamiento se hace por `productTypeId`, nunca por
el nombre: hay nombres repetidos entre los productos del Docente.

**Consultado el 2026-09-01:** sigue en `Pendiente`, **sin evidencia radicada**, a **80 días** de su
fecha. El sometimiento a EDU REVIEW (5579) ya lo cubre en lo esencial; falta el correo de acuse.

**Medida el 2026-09-01 sobre `productos_propios.json`:** el campo que lleva la evidencia es
`documentUrl`, y **de los 11 productos solo uno lo tiene** — el de ORCID (`prod_1785939730775`, ya
`Aprobado`). Los otros **diez lo traen ausente**: cero evidencia radicada en todo lo abierto.

### El plazo de Synapse que VENCIÓ ayer, y toca a este expediente

No está en `ART_OPEN_D` y por eso se pasa por alto. Se llama «Labores administrativas» —de ahí la
regla de emparejar por id y no por nombre— y venció el **2026-08-31**:

| id | Qué pide | Estado el 2026-09-01 |
|---|---|---|
| `prod_1785939714815` | «Actualización **GOOGLE ACADEMIC**» · pantallazo del perfil actualizado | **Pendiente · VENCIDO hace 1 día** |
| `prod_1785939730775` | «Actualización **ORCID**» · pantallazo del perfil actualizado | **Aprobado** (con `documentUrl` en Drive) |

> **El de Google Académico se pasó de fecha.** El 2026-08-28 se anotó aquí como «a 3 días»; hoy,
> 2026-09-01, está **vencido**. No lo cierra este agente —es solo lectura— pero es lo primero que
> hay que decirle al Docente: la observación pide un pantallazo del perfil, y **el perfil se cierra
> con estar verificado y vacío**, sin añadir obras. Sigue siendo la acción más barata del expediente,
> solo que ahora fuera de plazo.

**Y hay una contradicción que conviene ver:** el de ORCID está **Aprobado** mientras
`0009-0003-6598-432X` sigue con **cero obras** (`group: []`, reverificado el 2026-08-28). La
plataforma lo dio por bueno con el perfil vacío. No hay que hacer nada, pero tampoco conviene leer ese
«Aprobado» como que ORCID esté al día: no lo está, y en cuanto salga un DOI habrá que cargarlo.

El de CvLAC (`prod_1785939694462`, pantallazo con productos 2026) vence el **2026-11-20**.

## Manuscritos que NO están depositados

| Manuscrito | Por qué |
|---|---|
| `Articulo_Calidad_D_Desercion_ML.md` | **90** marcadores `[PENDIENTE: …]` (contados el 2026-08-28; este registro decía **39**, y eran 91 antes de retirar el de la financiación inexistente). Casi todos están donde irían los resultados, y **la investigación no existe**: cero notebooks, cero datasets de deserción, cero modelos entrenados y cero scripts en todo el repositorio. Lleva además una nota interna «eliminar antes del sometimiento» y cifras nunca medidas. Su versión depositable es el protocolo (17601). Destino previsto: revista, ver `Articulo_Calidad_D_NOTAS_DE_ENVIO.md` |
| ~~`Preprint_Completion_Gating_Moodle.md`~~ | ⛔ **ESTA FILA ES FALSA DESDE EL 2026-08-25.** Decía «RESERVADO. NO DEPOSITAR EN NINGÚN SERVIDOR DE PREPRINTS». **Sí está depositado**: Qeios, DOI `10.32388/z2uxxt`, CC BY 4.0 (ver el bloque de Crossref más arriba). Este manuscrito ya no pertenece a esta tabla. |

### ⛔ Candado ROTO: `Preprint_Completion_Gating_Moodle` ya está depositado

> **El candado se rompió el mismo día en que se puso.** Se escribió el **25/08/2026**, y el depósito
> en Qeios está sellado el **25/08/2026 a las 13:36:58Z**. O se redactó después del depósito sin
> saberlo, o el depósito se hizo con el candado ya escrito. **Averiguar cuál de las dos, entrando a
> `qeios.com`, es lo primero que hay que hacer**, porque solo una de las dos es un descuido.
>
> Todo lo que sigue queda **como registro de la decisión que se tomó, no como instrucción vigente**.
> Lo único que sobrevive de este bloque es su plan B: si hace falta un destino, **ACOFI** sigue en
> pie, y su regla de un artículo por autor y año también.

**No lo deposites en SciELO, ni en Qeios, ni en Zenodo, ni en ningún sitio.** Puesto el 25/08/2026.

Está reservado para **TecnoLógicas (ITM)**, la única revista **Publindex B** —8 puntos— de la lista
de destinos que se verificó ese día (las otras nueve: dos son C y **siete no están en Publindex**,
así que dan cero). Es diamante, sin cargos, y su convocatoria es permanente.

Y es el **único manuscrito de esta carpeta que puede ir**: los otros tres limpios ya están
depositados en SciELO, y el cuarto no es enviable. TecnoLógicas obliga a firmar que el trabajo no
ha sido publicado «en ningún formato» ni sometido a ningún otro medio. Un depósito, aunque sea un
preprint con DOI, **invalida esa declaración** y el filtro antiplagio de la revista lo encontraría
en la evaluación preliminar, que son 48-72 horas.

La revista **no publica política de preprints** —ni a favor ni en contra, se buscó en las 13
páginas del sitio—, así que no hay excepción en la que ampararse. Hasta que respondan a la consulta
de pertinencia enviada a `tecnologicas@itm.edu.co`, la regla es: **no se deposita**.

Si TecnoLógicas lo rechaza por alcance, el plan B es **ACOFI** (Revista Digital de Educación en
Ingeniería, Publindex C, 3 puntos, diamante), que es el mejor encaje temático de toda la lista.
Ojo con ACOFI: **solo admite un artículo por autor y año**, así que gastarla cierra la puerta
hasta 2027. Por eso no es la primera opción.

La versión adaptada a la revista se escribe aparte, en `Articulo_TecnoLogicas_Completion_Gating.md`,
para que este original quede intacto.


---

## 01/09/2026 — Revista PACA y LAJAR: un destino nuevo y uno descartado

Las dos las propuso el Docente. **No son comparables.**

### LAJAR (Latin American Journal of Aquatic Research) — DESCARTADA, y para siempre

No hay que volver a mirarla para ningún manuscrito de este portafolio. Dos motivos, cada uno
suficiente, y los dos literales de su propio sitio:

1. **Alcance.** Publica «original and unpublished research articles, reviews and short
   communications on aquatic science… conducted in aquaculture and marine waters of Latin America».
   Sus categorías propias son Fisheries Q4, Marine & Freshwater Biology Q4, Oceanography Q3, Aquatic
   Science Q3. Sus secciones son exactamente cuatro —Review Articles, Research Articles, Short
   Communications, In Memoriam— y su lista de temas es **cerrada**: siete, sin ninguna coletilla de
   «áreas afines». No hay sección de metodología, ni de notas técnicas, ni de educación.
2. **Cobra.** «Papers accepted are subjected to a publication charge of US$500,00», con casilla de
   aceptación: «I accept to pay US$500.00 once upon I receive the galley proofs».

Se puso un agente a **refutar** ese descarte buscando activamente una puerta. No la encontró.

### Revista PACA (Universidad Surcolombiana, ISSN 2027-257x) — SÍ es un destino real

| Aspecto | Detalle |
|---|---|
| Alcance | educación, pedagogía, currículo, evaluación, políticas públicas en educación, **educación superior**, investigación educativa **y áreas afines** |
| Idioma | español **o inglés** |
| Coste | **cero**, en todos los conceptos |
| Extensión | **8 a 15 páginas**, Arial 12, interlineado 1.5 — la regla es en PÁGINAS, no en palabras |
| Tipologías | investigación · revisión · reflexión |
| Exige | ORCID, afiliación, declaración de financiación, Declaración de Originalidad y **declaración de uso de IA nombrando la herramienta** |
| Contacto | revistapaca@usco.edu.co |

**Que mida en páginas abre una puerta que estaba cerrada.** El 17606 quedó fuera de EDU REVIEW por
su umbral de 3.000 palabras; maquetado en el formato de PACA da **11 páginas** (medidas generando el
.docx y convirtiéndolo a PDF con LibreOffice, no estimadas). Cabe.

### Pero hoy no se puede enviar nada, y el motivo es el mismo para los seis

La casilla 1 de PACA dice «original e inédito y no ha sido publicado ni se encuentra en proceso de
evaluación en otra revista **o medio de difusión científica**». Cada manuscrito choca con ella:

| Manuscrito | Por qué no se puede firmar hoy |
|---|---|
| 17601 Protocolo_Desercion_ML | sometido a EDU REVIEW (5579), en revisión |
| 17602 AI_Assisted_Course_Authoring | envío 596 a medias en ITEES + preprint en moderación |
| 17606 Anchored_Feedback | preprint en moderación en SciELO Preprints |
| Completion_Gating (las dos versiones) | **publicado** en Qeios, DOI 10.32388/z2uxxt, CC BY |
| Articulo_Calidad_D_Desercion_ML | además, 8.657 palabras: 26-29 páginas, el doble del máximo |

**Consulta enviada el 01/09/2026 a `revistapaca@usco.edu.co`** preguntando las dos cosas que no se
pueden resolver leyendo sus normas: si un depósito en SciELO Preprints **aún sin publicar** es
compatible con esa casilla, y bajo qué tipología encajaría el 17606. Texto en
`CORREO_Consulta_PACA.md`.

### Un defecto del 17606 que salió al revisarlo, y que ya está corregido

§2.1 entrecomillaba dos frases de la documentación de Google **sin referencia recuperable**, y la
bibliografía no tenía ni una sola fuente técnica. Peor: **el texto entrecomillado no era el de la
fuente.** Decía «across revisions» donde Google dice «between revisions», y ponía entre comillas
«treat developer-defined anchored comments as unanchored comments in their display», que Google no
escribe en ninguna parte. Corregido el 01/09 contra la página original: las dos citas ahora son
literales, llevan `(Google, 2026)` y la referencia está en la bibliografía, en su sitio alfabético.
La Política Antiplagio de PACA llama plagio a «la reproducción total o parcial de ideas, textos… de
terceros sin el debido reconocimiento de la fuente original».
