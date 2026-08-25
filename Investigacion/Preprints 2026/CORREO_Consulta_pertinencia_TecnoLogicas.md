# Correo de consulta de pertinencia — TecnoLógicas (ITM)

**Escrito el 25/08/2026. Envíalo tú desde tu correo institucional.**

- **Para:** tecnologicas@itm.edu.co
- **Asunto:** Consulta de pertinencia temática — auditoría de configuración en Moodle 4.5

Lo pide la propia revista antes de someter: «comuníquese con nuestro equipo editorial a
tecnologicas@itm.edu.co, enviando el título y el resumen para validar la pertinencia temática».
Es gratis, contestan rápido, y decide si estas horas de trabajo van a TecnoLógicas o a ACOFI.

**Por qué importa preguntar:** «docencia» no está entre las nueve áreas que declara la revista,
y hay una fase de evaluación editorial que decide expresamente si el trabajo cabe. El rechazo de
escritorio por alcance es el riesgo número uno de este envío. Veinte minutos ahora ahorran tres
semanas de espera para un «no».

---

## Texto para pegar

Estimado equipo editorial de TecnoLógicas:

Escribo para consultar la pertinencia temática de un manuscrito antes de someterlo, siguiendo la
indicación de su sitio. Soy docente de la Escuela de Ingeniería de la Corporación Unificada
Nacional de Educación Superior (CUN), en Bogotá.

El trabajo es una **auditoría instrumentada de la configuración de un sistema desplegado**. Escribí
un cliente para auditar las fechas de siete instancias de curso en Moodle 4.5 y documento un
acoplamiento no evidente entre dos subsistemas de la plataforma: una actividad sin calificación
—invisible para el instrumento, porque este se guiaba por el catálogo de ítems calificables—
gobernaba, mediante una restricción por finalización, la apertura efectiva de otra actividad de
peso alto. Las afirmaciones sobre el comportamiento de la plataforma están verificadas contra el
**código fuente de la rama MOODLE_405_STABLE**, no inferidas de la interfaz. El artículo reporta
también la corrección aplicada, las salvaguardas que el incidente obligó a introducir en el cliente
y la verificación de que ningún otro campo se modificó.

Mi duda es de encuadre: entiendo que el trabajo entra por **Ciencias de la Computación** y
**Aplicaciones de la computación**, en la línea de la literatura sobre errores de configuración en
sistemas de producción y deuda de configuración, que es el marco que utilizo. El aula es el caso de
validación, no el objeto de estudio: no se evalúa ninguna intervención pedagógica ni se reclama
ningún resultado de aprendizaje, y no se reportan datos de estudiantes. Les agradecería que me
confirmen si lo consideran pertinente.

Aprovecho para una segunda consulta, de forma. He encontrado una discrepancia entre dos documentos
del sitio: la guía para autores pide un resumen de 250 a 300 palabras, y la lista de comprobación
del envío pide de 200 a 250. Algo parecido ocurre con el número de palabras clave. He preparado el
manuscrito con **249 palabras de resumen y 5 palabras clave por idioma**, para cumplir las dos a la
vez, pero les agradecería saber qué cifra rige.

Datos del manuscrito:

- **Título (inglés, el idioma del manuscrito):** An Ungraded Survey Gating a 32.8% Assignment in
  Seven Moodle Courses
- **Título (español):** Una encuesta sin nota bloquea una entrega del 32,8 % en Moodle
- **Tipo:** artículo de investigación. Autor único.
- **Extensión:** unas 6.600 palabras de cuerpo, 25 referencias, 5 tablas, ninguna figura.
- **Idioma:** inglés. Puedo traducirlo al español si lo prefieren.
- **ORCID:** 0009-0003-6598-432X
- **Estado:** inédito. No está depositado en ningún servidor de preprints ni sometido a ninguna
  otra publicación.

**Resumen:**

El aula institucional llega poblada por una plantilla y el docente corrige lo que quedó mal. Este
informe documenta una auditoría instrumentada de siete aulas Moodle 4.5 y lo que la instrumentación
no vio. El catálogo calificable estaba en orden: 53 ítems alineados con el calendario del programa,
cero discrepancias. El defecto vivía fuera de él. Las 28 encuestas institucionales feedback, sin
nota y por eso invisibles para el instrumento, conservaban sus fechas de plantilla: 13 abrían en
2028 o 2030 en un curso de 2026, y 11 de ellas guardaban una apertura idéntica al cierre, una
ventana que nunca abre. El formulario la acepta: solo rechaza un cierre estrictamente anterior a la
apertura. El hallazgo con consecuencias es un acoplamiento: en dos aulas la entrega final, 32,8 % de
la nota y sin prórroga, estaba restringida por la finalización de una de esas encuestas, así que la
fecha de la encuesta era su apertura real: 2 días útiles de 31 en un aula y 10 de 39 en la otra,
mientras el calendario mostraba la ventana completa. La corrección quitó la ventana de las
encuestas, no la restricción institucional; al releer el servidor, las respuestas y los demás campos
seguían intactos. La regla generalizable: el peso de un ítem no predice su riesgo de calendario ni
su poder de bloqueo; toda auditoría de fechas debe enumerar cada tipo de actividad y resolver cada
restricción de acceso antes de declarar correcta un aula. No se reportan datos de estudiantes.

**Palabras clave:** entorno virtual de aprendizaje; Moodle; acceso condicional; finalización de actividad; error de configuración

Quedo atento y agradezco su tiempo.

Julian Andrés Castaño Espinosa
Escuela de Ingeniería — Corporación Unificada Nacional de Educación Superior (CUN)
Bogotá, Colombia
julian_castanoe@cun.edu.co
ORCID: https://orcid.org/0009-0003-6598-432X

---

## Antes de darle a enviar, comprueba dos cosas

**1. ¿Va con el nombre de la CUN o anonimizada?** El manuscrito dice que siete aulas de la CUN
tenían fechas de 2028 y 2030, y **lleva los identificadores reales de curso** (129268, 112321,
116387, 129270, 130378) y de módulo (6522210, 6745731, …). Están a propósito: la declaración de
disponibilidad de datos dice que se incluyen para que los administradores de la institución puedan
reproducir cada lectura. Eso es buena ciencia y es exposición institucional a la vez. Se puede
anonimizar sin tocar ningún dato. Es tu decisión, no la mía.

**2. ¿Lo sabe la decanatura o la DNI?** Conviene avisar antes de publicar, no después de que lo
acepten.

Ninguna de las dos cosas bloquea este correo: la consulta de pertinencia no compromete a nada.
