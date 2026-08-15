# Propuesta 5 — Docente Avatar: piloto de un asistente virtual generativo para sesiones de cursos virtuales CUN

**Investigador principal:** Julian Andres Castaño — julian_castanoe@cun.edu.co
**Programa / Escuela:** Ingeniería de Sistemas / Especialización en Inteligencia Artificial — Escuela de Ingenierías
**Fase del documento:** Fase 1 · Propuesta de anteproyecto (nivel ideación), formato INV-FO03, convocatoria interna CUN 2026 (Fase II)

> **Nota de elegibilidad a verificar (no asumida como resuelta):** los Términos de Referencia 2026 (Fase II), numeral 5.1, exigen del investigador principal: (a) vinculación activa con contrato de tiempo completo, (b) descarga horaria aprobada por la DNI para investigación, (c) no tener productos pendientes de convocatorias anteriores y haber cumplido el plan de trabajo 2025, y (d) CvLAC actualizado. El usuario debe confirmar estos cuatro puntos antes de radicar; este documento no los da por cumplidos.
>
> **Nota sobre la tabla de puntajes:** el numeral 11 de los Términos de Referencia trae una inconsistencia entre la tabla (2/28/50/20 = 100) y el texto explicativo inmediatamente debajo (Elementos preliminares hasta 20, Calidad de la propuesta hasta 60, Resultados y productos hasta 20). Esta propuesta se redactó para el criterio más exigente de los dos (Calidad de la propuesta = mayor peso posible), pero conviene que el investigador confirme con la DNI cuál tabla rige antes de radicar.

---

## 1. Título (provisional)

**Docente Avatar: piloto de un asistente virtual generativo para complementar sesiones sincrónicas y asincrónicas en cursos virtuales de la CUN**

## 2. Tipo de Propuesta

**Innovación.** No se trata de investigación básica sobre agentes pedagógicos (ese conocimiento ya existe y se cita en la sección de referentes), sino de la aplicación piloto y documentada de tecnología de IA generativa ya disponible (LLM + síntesis de voz + generación de avatar/video) a un problema pedagógico real de la CUN, con medición de percepción de los estudiantes como evidencia de resultado.

## 3. Grupo Temático + Eje Dinamizador

**Grupo Temático 2 — Línea de Innovación Pedagógica · Eje Dinamizador: Docente Avatar y Telepresencia.**

Aunque este eje pertenece formalmente al Grupo Temático 2 y no al de Gestión y Tecnologías (donde se ubica el perfil típico de un Ingeniero de Sistemas), la propuesta encaja de forma natural con ese perfil porque su núcleo es un problema de ingeniería: seleccionar, integrar y evaluar un pipeline de IA generativa (modelo de lenguaje + síntesis de voz neuronal + generación de video/avatar) capaz de operar en tiempo real o cuasi real dentro de un entorno de videoconferencia/LMS. La propuesta declara explícitamente su carácter **interdisciplinar entre ingeniería y pedagogía**: el investigador aporta la arquitectura técnica y la evaluación de viabilidad del sistema; la pregunta de fondo —si un avatar docente mejora, sostiene o daña la experiencia de aprendizaje— es pedagógica. Esta doble naturaleza también favorece el criterio de **Elementos preliminares**: por el diseño del piloto (una sesión replicable como plantilla), el resultado esperado impacta potencialmente a **más de un programa académico** (cualquier asignatura virtual de la CUN, no solo Ingeniería de Sistemas) y a **más de una modalidad de formación** (virtual y a distancia, que son las que dependen de sesiones grabadas o sincrónicas mediadas por videoconferencia).

## 4. Resumen (máximo 200 palabras — conteo real: 178 palabras)

Esta propuesta explora, desde la Ingeniería de Sistemas, la viabilidad técnica y pedagógica de un "docente avatar": un asistente virtual que combina un modelo de lenguaje generativo, síntesis de voz neuronal y generación de video/avatar para complementar —nunca reemplazar— sesiones sincrónicas y asincrónicas en cursos virtuales de la CUN. El proyecto es un piloto exploratorio, no un producto terminado: diseña y documenta una arquitectura técnica realista con herramientas ya disponibles, la implementa en un microescenario de una sesión de una asignatura virtual del investigador, y mide la percepción de los estudiantes frente a claridad, cercanía y utilidad percibida del recurso, comparándola con la sesión dictada por el docente humano. Se articula el eje Docente Avatar y Telepresencia (Grupo Temático 2, Innovación Pedagógica) con el perfil técnico de Ingeniería de Sistemas, subrayando su carácter interdisciplinar entre ingeniería y pedagogía. Los resultados esperados son un informe técnico de arquitectura replicable y una guía de buenas prácticas y límites éticos para el uso de avatares docentes en la CUN, insumos para decidir si conviene escalar la experiencia a otros programas y modalidades.

## 5. Objetivo general y objetivos específicos

**Objetivo general:** Determinar la viabilidad técnica y pedagógica de un docente avatar basado en IA generativa como recurso complementario en sesiones de un curso virtual de la CUN, mediante el diseño de una arquitectura técnica replicable y la evaluación de la percepción estudiantil frente a su uso.

**Objetivos específicos:**
1. Diseñar, en un plazo de 4 semanas, una arquitectura técnica de referencia para un docente avatar (LLM + síntesis de voz + generación de video/avatar) integrable con las herramientas de videoconferencia y LMS ya usadas en los cursos virtuales de la CUN.
2. Implementar, durante 3 semanas, un piloto del docente avatar en al menos una sesión de una asignatura virtual a cargo del investigador, documentando tiempos, costos y limitaciones técnicas reales de las herramientas seleccionadas.
3. Evaluar, mediante una encuesta de percepción aplicada a los estudiantes participantes en las 2 semanas siguientes al piloto, la claridad, cercanía y utilidad percibida del docente avatar frente a la sesión dictada sincrónicamente por el docente humano.

## 6. Impacto, viabilidad y retorno (versión breve)

El impacto esperado es doble: para la CUN, un antecedente institucional documentado sobre el uso responsable de avatares docentes en educación virtual, replicable en otros programas y modalidades; para el investigador, evidencia empírica que informe si vale la pena escalar el recurso en sus propias asignaturas. La viabilidad es alta porque no requiere desarrollo de software propio desde cero: se apoya en herramientas de IA generativa ya existentes —un generador de avatar/video (p. ej. HeyGen o D-ID) y un motor de síntesis de voz neuronal (p. ej. ElevenLabs o los servicios de voz de Azure/Google)— orquestados mediante un LLM (ChatGPT o Claude) que redacta y ajusta el guion pedagógico de cada sesión y responde preguntas frecuentes de los estudiantes en el tono del docente. El retorno institucional se mide en horas docentes potencialmente liberadas para tutoría personalizada y en un informe técnico reutilizable por otros docentes investigadores. El presupuesto se limita a suscripciones mensuales de estas herramientas (dentro del techo de $5.000.000) y no requiere hardware adicional.

## 7. Productos esperados (por tipología Minciencias)

- **Desarrollo tecnológico e innovación:** informe técnico de arquitectura del docente avatar + prototipo funcional de la sesión piloto (guion, audio y video generados).
- **Apropiación social del conocimiento:** guía breve de buenas prácticas y límites éticos para el uso de avatares docentes en la CUN, dirigida a otros docentes investigadores interesados en replicar el piloto.

No se fuerzan las cuatro tipologías: en 3 meses y con un solo piloto no hay alcance real para generar nuevo conocimiento teórico ni para un producto de formación de recurso humano en CTeI con estudiantes vinculados como coinvestigadores.

## 8. Referentes reales (ancla teórica, no la lista completa de marco teórico)

[1] N. L. Schroeder, O. O. Adesope, and R. B. Gilbert, "How effective are pedagogical agents for learning? A meta-analysis of learning outcomes," *J. Educ. Comput. Res.*, vol. 49, no. 1, pp. 1–39, 2013. — Evidencia empírica de que los agentes pedagógicos (avatares) mejoran el aprendizaje solo bajo ciertas condiciones de diseño; fija el nivel de expectativa realista para el piloto.

[2] A. L. Baylor and Y. Kim, "Simulating instructional roles through pedagogical agents," *Int. J. Artif. Intell. Educ.*, vol. 15, no. 2, pp. 95–115, 2005. — Marco de diseño de roles del agente pedagógico (experto, motivador, mentor), aplicable al guion del docente avatar.

[3] E. Kasneci *et al.*, "ChatGPT for good? On opportunities and challenges of large language models for education," *Learn. Individ. Differ.*, vol. 103, art. 102274, 2023. — Estado del arte y riesgos del uso de LLM en educación, insumo directo para los aspectos éticos de la propuesta.

[4] F. Tanaka, T. Takahashi, S. Matsuzoe, N. Tazawa, and M. Morita, "Telepresence robot helps children in communicating with teachers who speak a different language," in *Proc. 9th ACM/IEEE Int. Conf. Human-Robot Interaction (HRI)*, 2014, pp. 399–406. — Evidencia de campo sobre telepresencia docente y sus límites de aceptación por parte de los estudiantes.

[5] M. Westerlund, "The emergence of deepfake technology: A review," *Technol. Innov. Manage. Rev.*, vol. 9, no. 11, pp. 40–53, 2019. — Marco de riesgos éticos y de autenticidad de la síntesis de voz/video que la propuesta debe abordar explícitamente.

[6] D. Baidoo-Anu and L. Owusu Ansah, "Education in the era of generative artificial intelligence (AI): Understanding the potential benefits of ChatGPT in promoting teaching and learning," *J. AI*, vol. 7, no. 1, pp. 52–62, 2023. — Marco general de oportunidades pedagógicas de la IA generativa en el que se inscribe el docente avatar.

*(Norma de citación: IEEE, por tratarse de una propuesta de la Escuela de Ingenierías.)*

## 9. Viabilidad de alcance y tiempo

Es realista en el plazo de ~3 meses y el techo de $5.000.000: no exige desarrollo de software desde cero, sino la integración de herramientas de IA generativa ya disponibles en un piloto acotado a una sola sesión de una asignatura y una muestra pequeña de estudiantes. Escalar el docente avatar a varios programas, o construir un avatar 3D interactivo en tiempo real con latencia conversacional, sí sería un proyecto de uno o dos años y debe quedar explícitamente fuera del alcance de esta convocatoria.

---

## Comparación frente a las otras 4 propuestas paralelas de la convocatoria

Esta es la única de las cinco propuestas centrada en **avatares/telepresencia docente**; las otras cubren IoT, IA generativa institucional transversal, tecnologías educativas de generación de material y ciberseguridad/manejo de datos — ejes distintos, sin solapamiento de alcance con esta.

| Título | Eje | Tipo de producto | Fuerza en "calidad de la propuesta" | Realismo en el plazo |
|---|---|---|---|---|
| Docente Avatar: piloto de un asistente virtual generativo | Docente Avatar y Telepresencia (GT2) | Informe técnico de arquitectura + guía de buenas prácticas | Alta — problema claro, objetivos medibles, referentes reales sobre agentes pedagógicos y telepresencia | Alto — piloto acotado a una sesión, sin desarrollo de software desde cero |
