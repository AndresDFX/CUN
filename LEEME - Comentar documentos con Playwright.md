# Comentar el documento de un estudiante — anclado a la frase, con el navegador

**5 cursos · 6 guías de ACA · 41 criterios · el Syllabus de cada asignatura** · sirve tal cual en
cualquier semestre

> Agente: `comentar-documentos-cun`. Le pasas el enlace y el curso, y él hace todo lo de abajo.
> Este documento es para cuando quieras entender qué está pasando, o hacerlo a mano.

## Qué vas a conseguir

Que el documento que te comparte un estudiante quede comentado **como si lo hubieras comentado tú**:
cada comentario **colgado de la frase exacta** de la que habla, con la cita subrayada en el texto. No
en la barra lateral sin ancla — anclado.

Y el ancla es exacta, ni un carácter de más. La comprobación no es mirar la pantalla: se exporta el
documento a `.docx` y se leen `word/comments.xml` y los `w:commentRangeStart/End`, que dicen qué texto
quedó anclado **de verdad**. Comprobado sobre un anteproyecto real de 44 páginas, 11 comentarios,
11 anclas correctas.

## Hay dos rutas, y esta es la buena

La otra es [Apps Script](LEEME%20-%20Comentar%20documentos%20de%20estudiantes.md), anterior. Sigue
funcionando y no se ha retirado, pero tiene un límite que no se puede saltar: los comentarios que
ancla un programa **por API** los dibuja Google como comentarios *sueltos*, sin frase.

| | **Playwright** (esta) | Apps Script |
|---|---|---|
| Comentario anclado a la frase | **sí** | no: barra lateral, con la cita dentro del texto |
| Instalación | Chrome + un `login`, una vez | pegar el `.gs` una vez y autorizar |
| Token con acceso a **todo** tu Drive en disco | no | no |
| Pegado manual por cada documento | **no** | sí, el `Plan.gs` |
| El Syllabus de la asignatura | **sí, lo lee** | no, solo los criterios |
| Necesita ventana de Chrome | sí | no |

Por qué no se hace por API, en una línea cada una: la API de Docs **no crea sugerencias**; sus anclas
salen sueltas; y comentar un archivo ajeno exigiría el alcance amplio `drive`, porque **no existe un
alcance de solo comentar**. El detalle está en
[VIABILIDAD_COMENTARIOS_GOOGLE_DOCS.md](VIABILIDAD_COMENTARIOS_GOOGLE_DOCS.md).

## Cómo funciona por dentro

Google Docs pinta el texto en un **lienzo**, no en el DOM: no hay nada que seleccionar con el ratón.
La única vía es el teclado, y es exactamente la que usarías tú:

```
Ctrl+F  →  escribir la cita  →  Enter  →  Escape      la selección queda sobre la coincidencia
Ctrl+Alt+M  →  escribir el comentario  →  Ctrl+Enter
```

De ahí salen **tres reglas de la cita** que no son un capricho del programa, son de Ctrl+F:

1. **Cabe dentro de un párrafo.** Ctrl+F no cruza saltos de párrafo.
2. **Es única en el documento.** Ctrl+F va a la primera coincidencia. Si la frase está dos veces, el
   comentario aparecería delante del estudiante señalando la equivocada.
3. **Se escribe literal, letra por letra.** Un espacio doble, una comilla curva distinta, y no hay
   coincidencia. Entre **20 y 180** caracteres.

Las tres las comprueba `simular` antes de que nada llegue a nadie.

---

## Instalación (una vez por máquina)

```bash
pip install playwright python-docx        # Chrome ya instalado: no hace falta `playwright install`
python config/gdocs/sesion_google.py login
```

Se abre **tu Chrome** —no el Chromium que trae Playwright: Google detecta las marcas de automatización
y no deja pasar el SSO— y haces el inicio de sesión con `julian_castanoe@cun.edu.co`. Lo que queda
guardado es el **perfil**, en `%LOCALAPPDATA%\gdocs-cun\perfil`, y con eso basta para todas las
corridas siguientes.

La clave es **opcional**: si pones `%LOCALAPPDATA%\gdocs-cun\credenciales.json` con
`{"usuario": "…", "clave": "…"}`, el `login` autocompleta el formulario y tú solo confirmas el segundo
factor. Va **fuera del repositorio** a propósito: esto está en git y sincronizado a Drive.

Comprobar cuando dudes:

```bash
python config/gdocs/sesion_google.py estado --doc <ID>     # ¿sigo dentro, y veo ESE documento?
```

---

## El ciclo, por cada documento

### 1. Leer

```bash
python config/gdocs/comentar_docs.py leer \
    --doc "https://docs.google.com/document/d/1KaQdgX…/edit" --curso tg2 --aca acafinal
```

Baja el documento **vivo** a `_Revisiones/<título>.docx` (esa carpeta está **ignorada por git**) y lo
vuelca numerado, precedido de dos cosas distintas que las dos hacen falta:

- **el Syllabus de la asignatura** — competencia, elementos, unidades, resultado de aprendizaje: *qué
  enseña el curso*;
- **los criterios de la guía del ACA** — la misma guía que recibió el estudiante: *qué se le pidió en
  esta entrega*.

Con solo lo segundo, el comentario sale hecho un inventario del checklist.

Claves de `--curso`: `proyecto1`, `creatividad`, `investigacion`, `tg2`, `tg3`. Claves de `--aca`:
`aca1` (solo Proyecto I) y `acafinal` (los cinco).

> **TG2 no tiene Syllabus.** La CUN nunca lo entregó, y el volcado lo dice: «No te inventes
> competencias ni unidades: comenta con la guía del ACA». No es un fallo del programa.

### 2. Redactar el plan

Un `.json` al lado del `.docx`, en `_Revisiones/`:

```json
{
  "docId": "1KaQdgX…",
  "titulo": "NOMBRE - Plantilla Anteproyectos Pregrado",
  "curso": "tg2",
  "aca": "acafinal",
  "comentarios": [
    {
      "criterio": "Documento integrado (no fragmentos pegados)",
      "cita": "en total participaron 32 estudiantes",
      "texto": "Aquí dices 32 y en Población y muestra dices 34. Los porcentajes de las figuras solo cuadran con 34: el 41,2% son 14 de 34. Deja el número con el que efectivamente calculaste y revisa que quede igual en las cuatro partes donde aparece."
    }
  ]
}
```

La `cita` se copia **del volcado**, nunca de memoria. El `criterio` es trazabilidad —de dónde salió
cada comentario— y **no se publica**: nadie le escribe «Criterio "Documento integrado" — párrafo 12» a
un estudiante.

#### El lenguaje: es la mitad del trabajo

Lo lee una persona. Se habla del **contenido y de la estructura del documento**. El programa rechaza
ocho aperturas de oficio y tiene razón en las ocho:

| No | Sí |
|---|---|
| «Criterio "X": …» | qué le falta a esta parte |
| «No cumple con…» | qué habría que cambiar |
| «Según el criterio / la rúbrica / la guía…» | habla del documento |
| «De acuerdo con la rúbrica…» | igual |
| «Se evidencia…» | «aquí falta…», «esta parte dice…» |
| «El estudiante no…» | háblale a esa persona, no de esa persona |
| «Párrafo 12: …» | el ancla ya señala la frase |
| «insuficiente / satisfactorio / sobresaliente» | son bandas de nota, no observaciones |

Lo que sí funciona: **señalar la contradicción con su propio documento** («aquí dices 32 y allá 34, y
los porcentajes solo cuadran con 34» es irrefutable), **nombrar el problema técnico** para que tenga
algo que buscar («se llama restricción de rango»), **dar salidas en plural** y dejarle la decisión, y
**hablar de estructura** cuando el problema es estructural («estas cuatro secciones dicen lo mismo;
reúnelas en dos y el documento pierde tres páginas de repetición»).

Calibración: entre 8 y 12 comentarios en un documento largo. Uno por criterio no es la meta.

### 3. Simular — siempre, y no escribe nada

```bash
python config/gdocs/comentar_docs.py simular --doc <ID> --plan "_Revisiones/….plan.json"
```

Vuelve a bajar el documento **vivo** (el estudiante sigue editando mientras tú revisas) e imprime,
comentario por comentario, la sección y el párrafo donde cae, el ancla y el texto **exacto** que
vería. Y no publica nada si algo no cuadra:

- una cita que ya no está, que se repite, que cruza un párrafo, que es demasiado corta;
- un criterio que no está en la guía —te enseña la guía entera—;
- un comentario vacío o escrito en lenguaje de oficio.

### 4. Ensayar — publica de verdad, pero en una copia tuya

```bash
python config/gdocs/comentar_docs.py ensayar --doc <ID> --plan "_Revisiones/….plan.json"
```

Copia el documento a tu Drive y publica **ahí** los comentarios, con la misma secuencia de teclas que
usaría la publicación real. Te da el enlace de la copia: ábrela y **léela con tus ojos**.

`simular` comprueba el plan, no el resultado: no puede mentir, pero tampoco puede probar nada. El
ensayo sí lo prueba. Cuando acabes, la copia es tuya y va a la papelera.

**Pero no es una parada obligatoria.** El 01/09/2026 el Docente lo dijo así: «la revisión se pone
aquí ‹enlace› directamente». Pedir la revisión sobre un enlace concreto **es** la autorización para
publicar; pararse a pedir permiso otra vez le devuelve el trabajo que quería delegar. Úsalo cuando
algo del plan te dé mala espina —una cita rara, un documento con tabla de contenido, tipografía
mezclada—, no por rutina. Lo que sí es obligatorio siempre es `simular`.

### 5. Publicar

```bash
python config/gdocs/comentar_docs.py comentar --doc <ID> --plan "…" --confirmar
```

Sin `--confirmar` te dice qué publicaría y para. Con `--confirmar` publica, **comprueba sobre el
documento exportado** que cada comentario quedó anclado donde debía, y escribe el **recibo** en
`_Revisiones/<id>.publicados.json`.

Al estudiante le llega **al instante**, por correo. Deshacerlo borra el comentario, no que lo leyó.

### 6. Deshacer

```bash
python config/gdocs/comentar_docs.py deshacer --doc <ID> --confirmar
```

Borra los comentarios de la última publicación, uno por uno, **buscando cada uno por su cita** —el
mismo Ctrl+F— y al final comprueba contra la exportación cuáles siguen ahí. Tarda unos diez segundos
por comentario porque recarga el documento entre borrado y borrado: al borrar un hilo, el panel
reposiciona los demás.

Funciona **por el recibo**. El comentario no lleva ninguna marca de que lo escribió un programa —el
estudiante lee prosa, no etiquetas—, así que sin recibo no hay forma de distinguir los tuyos de los de
otra persona, y el programa te lo dice en vez de borrar a ciegas.

---

## Lo que este proceso no hace

- **No modifica el documento.** Solo crea y borra comentarios. En el código no existe ninguna llamada
  que escriba en el cuerpo del texto del estudiante.
- **No pone notas.** La nota la pone el Docente, en CDigital, a mano.
- **No comenta un criterio que no esté en la guía.** Lo valida contra los 41 criterios reales.
- **No publica sin `--confirmar`.**

## Cuando algo falla

| Síntoma | Qué es |
|---|---|
| `La descarga devolvió HTTP 302/401` | la sesión caducó → `sesion_google.py login` |
| `La descarga devolvió HTTP 403/404` | ese documento no está compartido con esta cuenta, o el id está mal |
| «Lo compartieron en modo Lector» | pídele acceso de **Comentador**; con ese basta |
| «la cita aparece 2 veces (una en la tabla de contenido)» | es real: elige otra frase, del cuerpo |
| «la cita cruza un salto de párrafo» | recórtala a lo que quepa en uno |
| «la cita NO está letra por letra» | cópiala del volcado de `leer`, no del PDF ni de memoria |
| «El plan es de otro documento» | el `docId` del plan no es el `--doc` que pediste |
| `deshacer`: «no hay recibo» | esa publicación no la hizo este programa → bórralos a mano |
| Chrome se abre y se queda en la pantalla de Google | pasó con el Chromium de Playwright; usa `channel="chrome"`, que es lo que ya hace |
| «#N quedó anclado a otra cosa» y al mirarlo está bien | **era un falso fallo, corregido el 02/09/2026.** `comentarios_publicados()` leía el `.docx` sin desescapar entidades XML: una cita con `<`, `>` o `&` volvía como `&gt;` y la comparación no casaba. Si vuelve a aparecer, mira si la cita lleva alguno de esos tres caracteres antes de tocar el documento |
| «N comentarios publicados» y el número es mayor que tu plan | no publicó de más: cuenta **todos** los comentarios anclados del documento, incluidos los que ya traía. El recibo `_Revisiones/<id>.publicados.json` es el que dice cuáles son tuyos |

## Mantenimiento

```bash
python config/gdocs/_prueba_comentar_docs.py     # 42 comprobaciones, sin red y sin cuenta
```

Construye documentos `.docx` de mentira —incluido uno con la **tabla de contenido envuelta en `w:sdt`**,
como la exporta Google— y comprueba lo que de verdad se puede romper: que `doc_id` acepte enlace e id y
rechace basura; que los ocho vicios de lenguaje se rechacen y la prosa natural pase; que la cita
duplicada por el índice, la que cruza párrafo, la corta, la no literal y el criterio inventado se
frenen; que una cita **dentro de una tabla** (el cronograma, el presupuesto) sí se pueda comentar; y
que `syllabus_curso` siga leyendo los dos formatos, no pierda las unidades que van de dos en dos y diga
«no hay Syllabus» en TG2 sin romperse.

Si cambian los criterios de un ACA, no hay nada que regenerar: se leen del `.docx` de la guía en cada
corrida. Si cambia un Syllabus, tampoco: se lee del `.docx` oficial del curso.

## Dónde está cada cosa

| Archivo | Qué es |
|---|---|
| `config/gdocs/comentar_docs.py` | el motor y las 5 órdenes |
| `config/gdocs/sesion_google.py` | la sesión de Chrome: `login`, `estado` |
| `config/gdocs/criterios_aca.py` | los 41 criterios, leídos de las 6 guías |
| `config/gdocs/syllabus_curso.py` | el Syllabus de la asignatura, en piezas usables |
| `config/gdocs/plan_comentarios.py` | leer el `.docx` y normalizar tipografía (compartido con Apps Script) |
| `config/gdocs/_prueba_comentar_docs.py` | el arnés |
| `%LOCALAPPDATA%\gdocs-cun\perfil` | la sesión de Chrome. **Fuera del repositorio** |
| `%LOCALAPPDATA%\gdocs-cun\credenciales.json` | usuario y clave, opcional. **Fuera del repositorio** |
| `_Revisiones/` | los `.docx`, los planes y los recibos. **Ignorada por git** |
