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
