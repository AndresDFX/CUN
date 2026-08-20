# Docente — Proyecto I

**ESP329 · grupo 54ES4** · aula CDigital **130378**

> ⛔ **Esta carpeta NO se comparte con los estudiantes.** `Clases/` sí: es la carpeta que ellos ven, y
> su propio `LEEME - Material para estudiantes` les dice «no busques estos archivos fuera de
> `Clases/`». Todo lo que esté aquí queda fuera de ese alcance a propósito.

## Qué hay aquí y por qué

`Guiones/` — los **guiones docentes**, uno por sesión (`Sesion NN - <tema>.md`, 11 en este curso) y
`Capturas/` con los 14 pantallazos que se proyectan o se repasan antes de clase. Son **solo `.md`**:
de un guion no se genera `.docx`.

Estaban en la raíz de la asignatura, al lado de `Clases/`. Se movieron aquí el **19 de agosto de
2026** por la misma razón que los bancos: son material del Docente —traen el minuto a minuto, las
respuestas esperadas de cada taller y las notas de qué hacer si el grupo no responde— y no tienen
por qué estar a un clic de la carpeta que ven los estudiantes. Las imágenes van referenciadas en
relativo (`Capturas/…`), así que el movimiento no rompió ningún enlace.

El guion no se edita a mano cuando hay que regenerarlo entero: lo escribe
`_regen_guiones_proyecto1.py` (o `config/slides/build_sesion_material.py <curso> all --guion-only`).

`Cuestionarios/` — el **banco de preguntas maestro** del Quiz, en dos versiones:

| Archivo | Para qué sirve |
|---|---|
| `Quiz - banco de preguntas (Moodle XML).xml` | El **maestro**. Es lo que se importa a CDigital. |
| `Quiz - banco de preguntas.md` | El gemelo legible: qué evalúa cada pregunta, con la **cita literal** de donde salió la clave. Sirve para revisar el banco sin abrir Moodle y para atender reclamos. |

**Los dos llevan la respuesta correcta.** El `.md` la trae en una columna titulada «Respuesta
correcta» y el `.xml` en los atributos `fraction="100"` de cada opción. Por eso estaban mal ubicados:
vivían en `Clases/Recursos/Cuestionarios/`, dentro de la carpeta que ven los estudiantes. Se
movieron aquí el **18 de agosto de 2026**.

## El otro canal por el que este banco puede salir

Mover el archivo cierra la puerta de Drive, no la del campus. **El Quiz de Proyecto I es el único de
los 19 que muestra la respuesta correcta después de cerrar**, y cierra el **30/08/2026**: ese día 50
estudiantes pueden transcribir las 10 claves, y el banco se reimporta en cada edición del curso. Los
18 de Pregrado no corren ese riesgo porque tienen esa casilla apagada.

La decisión sigue abierta y el camino intermedio propuesto es dejar encendidas *si acertó* y *la
retroalimentación* y apagar solo *la respuesta correcta*: el estudiante ve en qué falló y por qué, sin
que el enunciado correcto quede transcrito. El cambio es una corrida de
`python config/moodle/revision_quiz.py`. Contexto completo en `ALISTAMIENTO CDigital 2026-08-15.md`
§5.2, punto 3.

## Lo que NO se movió, y por qué

La **guía del estudiante** sigue en `Clases/Recursos/ACAs/` y ahí se queda: es para el estudiante,
dice **qué entra** en el cuestionario y no revela ninguna clave. La tabla del libro de calificaciones
del `LEEME` de los estudiantes la apunta por nombre, así que moverla rompería ese enlace. **El alcance
del banco se define entre el Manual del Docente y esa guía** — de ahí que el banco cite las dos.

## Cómo se usa el banco

El maestro es el `.xml` **de este repositorio, no el aula**. Si hay que corregir una pregunta se
corrige aquí, se borra la categoría del aula y se reimporta; así el próximo periodo arranca con la
corrección puesta.

```bash
# validar sin tocar el aula (siempre primero)
python config/moodle/cdigital.py importar \
  "Especializacion/Proyecto I/Docente/Cuestionarios/Quiz - banco de preguntas (Moodle XML).xml" \
  --curso 130378 --simular
```

El procedimiento completo está en `config/moodle/LEEME.md` § «Alistamiento del aula» y en
`ALISTAMIENTO_DE_AULAS_CDIGITAL.md` (raíz del repositorio). El inventario de la última corrida, con
los cmid, en `ALISTAMIENTO CDigital 2026-08-15.md`.

## Verificado en el campus

El **18 de agosto de 2026** se revisaron las **28 carpetas de material** de las 7 aulas (167 archivos)
buscando bancos subidos por error: **cero**. La fuga estaba solo en Drive, y era esta.
