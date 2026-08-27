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

Última comprobación: **2026-08-23**. Los tres en `404` (Crossref y `doi.org`). Id más alto publicado
en el prefijo `10.1590` a esa fecha: **17584**, depositado el 2026-08-21. Los tres están justo por
encima de la frontera de la cola, que es lo esperable dos días después de enviarlos.

Cuando salga el DOI, se añade a la fila la URL pública
(`https://preprints.scielo.org/index.php/scielo/preprint/view/<id>/version/<pubId>`) y se lleva el
DOI a **CvLAC**, a **ORCID** y a la evidencia del producto de **Synapse**.

## Revistas indexadas

| Manuscrito | Revista | Publindex | Fecha | Estado |
|---|---|---|---|---|
| `Articulo_TecnoLogicas_Completion_Gating` | TecnoLógicas (ITM) | **B** · 8 pts | 2026-08-25 | **consulta de pertinencia enviada** |
| `Preprint_Protocolo_Desercion_ML` (17601) | EDU REVIEW (Edulab, ES) | **ninguna** · 0 pts | 2026-08-26 | **paquete listo, sin enviar** — falta cuenta OJS y el clic del Docente |

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

**Qué significa para TecnoLógicas.** Hoy **no hay evidencia de difusión pública**, así que la
declaración de «no publicado en ningún formato» sigue sostenible. Pero conviene que el Docente
resuelva dos cosas antes de someter, porque son las únicas que quedan sin mirar: **con quién están
compartidos esos cuatro archivos en Drive** (la interfaz los marca «Compartido», aunque no sean
públicos) y **qué hay en su lista de envíos de SciELO**, que necesita su clave.

## Software acompañante

| Paquete | Preprint al que acompaña | Depósito |
|---|---|---|
| `anchored-feedback` v1.0.0 | 17606 | sin depositar |

## Producto de Synapse al que responden

`productTypeId: ART_OPEN_D` — «Artículos de investigación con Calidad D (acceso abierto)»,
`prod_1785940748621`, vence **2026-11-20**. El emparejamiento se hace por `productTypeId`, nunca por
el nombre: hay nombres repetidos entre los productos del Docente.

## Manuscritos que NO están depositados

| Manuscrito | Por qué |
|---|---|
| `Articulo_Calidad_D_Desercion_ML.md` | 39 marcadores `[PENDIENTE: …]`, una nota interna «eliminar antes del sometimiento» y cifras nunca medidas. Su versión depositable es el protocolo (17601). Destino previsto: revista, ver `Articulo_Calidad_D_NOTAS_DE_ENVIO.md` |
| `Preprint_Completion_Gating_Moodle.md` | **RESERVADO. NO DEPOSITAR EN NINGÚN SERVIDOR DE PREPRINTS.** Ver el candado de aquí abajo. |

### Candado: `Preprint_Completion_Gating_Moodle` va a revista, no a preprint

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
