# Propuesta 3 · Sistematización y evaluación de un sistema de generación automatizada de material docente con IA generativa alineado al Syllabus institucional CUN (título provisional)

**Convocatoria:** Desarrollo de Grupos Temáticos de Investigación CUN – 2026 (Fase II)
**Fase de trabajo:** Fase 1 — propuesta de ideación (INV-FO03 simplificado, para decisión)
**Investigador principal:** Julian Andres Castaño — Docente, Ingeniería de Sistemas / Especialización en Inteligencia Artificial — CUN
**Correo:** julian_castanoe@cun.edu.co
**Escuela:** Escuela de Ingenierías → norma de citación aplicable: **IEEE**

> **Nota de cumplimiento — verificar antes de radicar.** Los Términos de Referencia 2026 (Fase II), numeral 5.1, exigen para el investigador principal: (a) vinculación activa con **contrato de tiempo completo**, (b) **descarga horaria** aprobada por la DNI para investigación, (c) **no tener productos pendientes** de convocatorias anteriores y haber cumplido el plan de trabajo 2025, y (d) **CvLAC actualizado**. Esta propuesta no asume que Julian Andres Castaño cumple los cuatro requisitos — no hay información en este ejercicio que lo confirme — y deben verificarse con la DNI antes de radicar, especialmente la descarga horaria, que condiciona cuántas horas reales tendrá disponibles para ejecutar el cronograma de 3 meses.
>
> **Nota sobre el puntaje de evaluación.** El documento de Términos de Referencia trae una inconsistencia entre la tabla del numeral 11 (2/28/50/20 = 100) y el texto explicativo inmediatamente debajo (Elementos preliminares 2 / Calidad de la propuesta 60 / Resultados y productos... nótese que el texto describe "Calidad de la propuesta" con 60 puntos y no reporta explícitamente el peso de "Impacto, viabilidad y retorno" por fuera de la tabla). No se resuelve aquí cuál cifra es la vigente; en cualquier lectura, "Calidad de la propuesta" es el bloque de mayor peso, por lo que esta propuesta se escribió priorizando ese criterio (claridad del problema, objetivos medibles, diseño metodológico y rigor de los referentes).

---

## 1. Título (provisional)

**Sistematización y evaluación empírica de un sistema de generación automatizada de material docente con IA generativa, alineado al Syllabus institucional, en cinco cursos de la CUN**

Título corto de trabajo: *GenIA Docente CUN*.

## 2. Tipo de Propuesta

**Innovación** (checkbox único de las 8 opciones oficiales del INV-FO03).

Justificación de la elección: la propuesta no crea un desarrollo de software desde cero (ese componente tecnológico ya existe y está en uso productivo desde 2025), tampoco es investigación básica sin aplicación, ni es un producto exclusivamente pedagógico de aula. Es la evaluación y sistematización de una innovación tecnológica ya implementada en la práctica docente real, con miras a su adopción institucional — el perfil exacto de "Innovación": tomar algo que ya funciona en un contexto acotado y generar la evidencia y el protocolo que permitan escalarlo.

## 3. Grupo Temático + Eje Dinamizador

**Grupo Temático 1 · Línea de Gestión y Tecnologías → Eje Dinamizador: Desarrollo de Tecnologías Educativas.**

Por qué encaja: el eje pide, literalmente, desarrollo de tecnologías aplicadas a la educación; el investigador ya tiene una tecnología educativa propia en operación (generación automatizada de material de curso desde IA generativa) y lo que falta —y es la oportunidad real de esta convocatoria— es la evidencia empírica y la sistematización que permitan defenderla como aporte institucional, no solo como una herramienta personal de productividad docente.

## 4. Resumen (máximo 200 palabras)

Desde 2025, el investigador principal opera en producción un sistema propio en Python que genera automáticamente el material de los cinco cursos que dicta en la CUN —presentaciones, guiones de docente, calendarios, correos y enunciados de evaluación— a partir del Syllabus institucional (SIAC) y del libro de calificaciones de la plataforma institucional, usando IA generativa para redactar cada entregable. Esta propuesta no construye el sistema —ya existe y está en uso—, sino que lo sistematiza y lo evalúa empíricamente: documenta su arquitectura como protocolo replicable; mide la consistencia curricular del material frente al Syllabus mediante una rúbrica de trazabilidad tema a tema; cuantifica el tiempo docente ahorrado frente a la elaboración manual; y explora, mediante encuesta a estudiantes y pares docentes, la percepción de calidad del material producido. El resultado esperado es evidencia empírica —no solo anecdótica— sobre si la generación automatizada de material didáctico alineada a Syllabus mediante IA generativa es confiable y escalable a otros docentes y programas de la CUN, junto con una guía práctica de adopción. El estudio se desarrolla en los cinco cursos reales del investigador durante 2026-1, en un enfoque mixto ejecutable en tres meses con la infraestructura ya construida.

*(Conteo real: 196 palabras.)*

## 5. Objetivo general y objetivos específicos

**Objetivo general:** Evaluar empíricamente la consistencia curricular, el tiempo docente ahorrado y la percepción de calidad de un sistema propio de generación automatizada de material de curso mediante IA generativa alineado al Syllabus institucional, en los cinco cursos dictados por el investigador durante el periodo 2026-1, para determinar su viabilidad de escalamiento a otros docentes y programas de la CUN.

**Objetivos específicos:**

1. Documentar y sistematizar, en un protocolo técnico replicable, la arquitectura y el flujo de datos del sistema (Syllabus SIAC + libro de calificaciones institucional como entradas; presentaciones, guiones de docente, calendarios, correos y enunciados de evaluación como salidas), durante el primer mes de ejecución.
2. Medir, mediante una rúbrica de trazabilidad tema a tema, la consistencia curricular del material generado automáticamente frente a las unidades de conocimiento del Syllabus oficial de cada uno de los cinco cursos, y cuantificar el tiempo docente ahorrado frente a la elaboración manual equivalente, durante el segundo mes.
3. Evaluar la percepción de calidad del material generado mediante encuesta a estudiantes y revisión por pares docentes, y formular los requisitos mínimos (técnicos y de acompañamiento) para su generalización a otros docentes y programas de la CUN, durante el tercer mes.

## 6. Impacto, viabilidad y retorno (versión breve)

El impacto esperado es institucional y medible: si la consistencia curricular y el ahorro de tiempo se confirman con evidencia (no solo con la experiencia personal del investigador), la DNI y las direcciones de programa tendrían un caso documentado para explorar la adopción de flujos de generación de material con IA en otros docentes, con el consiguiente ahorro de horas de preparación de clase a escala. La viabilidad operativa es alta porque el componente de mayor riesgo —construir el sistema— ya está resuelto y en uso; lo que resta es instrumentar la medición (rúbrica, encuesta, registro de tiempos), que no requiere desarrollo adicional de software. La herramienta de IA usada y su rol son concretos: el sistema invoca un modelo de lenguaje generativo (familia Claude de Anthropic, vía API en Python) para redactar y estructurar cada entregable de curso a partir del Syllabus y las calificaciones, y en esta fase de investigación se usará adicionalmente para apoyar el análisis cualitativo de las respuestas abiertas de la encuesta de percepción.

## 7. Productos esperados (tipologías Minciencias)

- **Desarrollo tecnológico e innovación** (objetivo específico 1): protocolo técnico documentado del sistema (arquitectura, flujo de datos, manual de uso) como producto de innovación sistematizado — hoy existe como código de uso personal, no como producto institucional documentado.
- **Generación de nuevo conocimiento** (objetivo específico 2): artículo corto / documento de trabajo con los resultados de consistencia curricular y tiempo docente ahorrado, apto para un evento o revista institucional.
- **Apropiación social del conocimiento** (objetivo específico 3): guía práctica breve de adopción para otros docentes CUN interesados en replicar el flujo, socializada en un espacio interno (p. ej. semillero o encuentro de docentes investigadores).

No se fuerza un cuarto producto de "Formación de RRHH en CTeI": el alcance de 3 meses no incluye vinculación de estudiantes-investigadores; si se quisiera sumarlo, habría que vincular un semillero desde el diseño, lo que alargaría el cronograma.

## 8. Referentes reales (ancla, no lista completa)

1. O. Zawacki-Richter, V. I. Marín, M. Bond, y F. Gouverneur, "Systematic review of research on artificial intelligence applications in higher education – where are the educators?," *International Journal of Educational Technology in Higher Education*, vol. 16, no. 39, 2019. Aporta el estado del arte de IA en educación superior y el vacío de estudios liderados por los propios docentes (no solo por desarrolladores externos), que es justamente el lugar de esta propuesta.
2. E. Kasneci et al., "ChatGPT for good? On opportunities and challenges of large language models for education," *Learning and Individual Differences*, vol. 103, 2023. Da el marco de oportunidades/riesgos de usar LLM en tareas educativas, útil para justificar por qué medir consistencia curricular no es opcional.
3. M. Bearman y R. Ajjawi, "Learning to work with the black box: Pedagogy for a world with generative AI," *British Journal of Educational Technology*, vol. 54, no. 5, 2023. Aporta el concepto de "pedagogía para trabajar con la caja negra" del contenido generado por IA, pertinente para la rúbrica de trazabilidad frente al Syllabus.
4. J. Biggs, "Enhancing teaching through constructive alignment," *Higher Education*, vol. 32, no. 3, 1996. Fuente clásica del concepto de alineación curricular (constructive alignment), base conceptual directa para medir "consistencia curricular" del material generado frente al Syllabus.
5. UNESCO, *Guidance for generative AI in education and research*, París: UNESCO, 2023. Referente institucional/normativo reciente sobre uso responsable de IA generativa en educación, útil para los aspectos éticos de la propuesta.

## 9. Viabilidad de alcance y tiempo

Realista dentro de la convocatoria: la parte más costosa (construir el sistema) ya está hecha y en producción desde 2025, así que los 3 meses y los $5.000.000 disponibles se destinan solo a instrumentar la medición —diseño de la rúbrica de trazabilidad, aplicación de encuestas a estudiantes y pares en los 5 cursos del investigador, análisis de datos y redacción del protocolo y del artículo—, no a desarrollo. El riesgo de alcance está en el objetivo 3 (percepción de calidad vía encuesta a estudiantes reales): debe diseñarse y aprobarse con margen suficiente dentro del mes 3 para no depender de un calendario académico que el investigador no controla del todo. Si el tiempo aprobado en la descarga horaria resulta menor al esperado, la primera reducción de alcance recomendada es limitar la medición de consistencia curricular a 2-3 de los 5 cursos en lugar de los 5, manteniendo objetivos y productos intactos.
