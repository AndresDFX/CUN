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
