# Docente — Investigación en Ciencia y Tecnología

**EI005 · grupo 53339** · aula CDigital **111070**

> ⛔ **Esta carpeta NO se comparte con los estudiantes.** `Clases/` sí: es la carpeta que ellos ven, y
> su propio `LEEME - Material para estudiantes` les dice «no busques estos archivos fuera de
> `Clases/`». Todo lo que esté aquí queda fuera de ese alcance a propósito.

## Qué hay aquí y por qué

`Guiones/` — los **guiones docentes**, uno por sesión (`Sesion NN - <tema>.md`, 6 en este curso) y
`Capturas/` con los 32 pantallazos que se proyectan o se repasan antes de clase. Son **solo `.md`**:
de un guion no se genera `.docx`.

Estaban en la raíz de la asignatura, al lado de `Clases/`. Se movieron aquí el **19 de agosto de
2026** por la misma razón que los bancos: son material del Docente —traen el minuto a minuto, las
respuestas esperadas de cada taller y las notas de qué hacer si el grupo no responde— y no tienen
por qué estar a un clic de la carpeta que ven los estudiantes. Las imágenes van referenciadas en
relativo (`Capturas/…`), así que el movimiento no rompió ningún enlace.

`Cuestionarios/` — los **bancos de preguntas maestros** de los quices y parciales, en dos versiones
por ítem:

| Archivo | Para qué sirve |
|---|---|
| `<ÍTEM> - banco de preguntas (Moodle XML).xml` | El **maestro**. Es lo que se importa a CDigital. |
| `<ÍTEM> - banco de preguntas.md` | El gemelo legible: qué evalúa cada pregunta, con la **cita literal** de donde salió la clave. Sirve para revisar el banco sin abrir Moodle y para atender reclamos. |

**Los dos llevan la respuesta correcta.** El `.md` la trae en una columna titulada «Respuesta
correcta» y el `.xml` en los atributos `fraction="100"` de cada opción. Por eso estaban mal ubicados:
vivían en `Clases/Recursos/Cuestionarios/`, dentro de la carpeta que ven los estudiantes. Se
movieron aquí el **18 de agosto de 2026**.

## Lo que NO se movió, y por qué

Las **guías del estudiante** siguen en `Clases/Recursos/ACAs/<ÍTEM> (N%) - guia del cuestionario.docx`
y ahí se quedan: son para el estudiante, dicen **qué entra** en el cuestionario y no revelan ninguna
clave. La tabla del libro de calificaciones del `LEEME` de los estudiantes las apunta por nombre, así
que moverlas rompería ese enlace. **El alcance de cada banco se define entre el Manual del Docente y
esa guía** — de ahí que el banco cite las dos.

La carpeta de clase `Clases/Sesion 03 - Prueba parcial · 1.er avance del artículo` tampoco se movió:
es una **sesión de clase** —el día en que se resuelve el parcial—, no el banco.

## Cómo se usa el banco

El maestro es el `.xml` **de este repositorio, no el aula**. Si hay que corregir una pregunta se
corrige aquí, se borra la categoría del aula y se reimporta; así el próximo periodo arranca con la
corrección puesta.

```bash
# validar sin tocar el aula (siempre primero)
python config/moodle/cdigital.py importar \
  "Pregrado/Investigacion en ciencia y tecnologia/Docente/Cuestionarios/Parcial 1 - banco de preguntas (Moodle XML).xml" \
  --curso 111070 --simular
```

El procedimiento completo está en `config/moodle/LEEME.md` § «Alistamiento del aula» y en
`ALISTAMIENTO_DE_AULAS_CDIGITAL.md` (raíz del repositorio). El inventario de la última corrida, con
los cmid, en `ALISTAMIENTO CDigital 2026-08-15.md`.

## Verificado en el campus

El **18 de agosto de 2026** se revisaron las **28 carpetas de material** de las 7 aulas (167 archivos)
buscando bancos subidos por error: **cero**. La fuga estaba solo en Drive, y era esta.
