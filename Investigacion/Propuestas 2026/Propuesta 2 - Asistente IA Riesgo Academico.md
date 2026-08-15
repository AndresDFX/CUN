# Propuesta 2 — Asistente de IA Generativa para Detección Temprana de Riesgo Académico en la CUN

*Anteproyecto de investigación · Fase 1 (ideación) · Formato INV-FO03 · Convocatoria interna CUN 2026 (Fase II)*

> **Notas de verificación institucional (léanse antes de radicar — no están resueltas por este documento):**
>
> 1. **Vinculación del investigador principal.** El numeral 5.1 de los Términos de Referencia 2026 (Fase II) exige, para el investigador principal: (a) vinculación activa a la CUN como docente investigador con **contrato de tiempo completo**; (b) **descarga horaria** aprobada por la DNI; (c) no tener actividades o productos pendientes de convocatorias anteriores, incluido el cumplimiento íntegro del plan de trabajo 2025; y (d) **CvLAC actualizado**. Esta propuesta no puede verificar si Julian Andres Castaño cumple hoy las cuatro condiciones — debe confirmarse con la DNI antes de radicar, no asumirse resuelto.
> 2. **Inconsistencia en los criterios de evaluación (num. 11).** La tabla del documento asigna 2 / 28 / 50 / 20 puntos a Elementos preliminares / Impacto-viabilidad-retorno / Calidad de la propuesta / Resultados y productos (= 100), pero el texto explicativo inmediatamente debajo describe solo tres criterios con pesos 20 / 60 / 20 (fusiona "impacto" dentro de "calidad"). Es una inconsistencia del propio documento institucional; esta propuesta se redactó cuidando el criterio más exigente de los dos bajo cualquier lectura (calidad de la propuesta = grueso de la nota).
> 3. **Cronograma del documento.** El numeral 9 fecha el cierre de entrega el 20 de marzo de 2026 y el acta de inicio el 10 de abril de 2026 — fechas anteriores a la fecha de redacción de este documento (13 de agosto de 2026). Verificar con la DNI si el cronograma vigente es otro antes de radicar.

**Investigador principal:** Julian Andres Castaño — docente Ingeniería de Sistemas / Especialización en Inteligencia Artificial, CUN. Correo: julian_castanoe@cun.edu.co.

**Grupo Temático 1 · Línea de Gestión y Tecnologías — Eje Dinamizador: Inteligencia Artificial y Tecnologías Emergentes**, con vinculación explícita del eje transversal de herramientas de IA en la construcción y proyección de resultados.

---

## 1. Título de la propuesta

**Asistente de IA Generativa para Detección Temprana de Riesgo Académico en la CUN**

## 2. Tipo de Propuesta

☑ **Desarrollo de Software** — el entregable central es un prototipo funcional (asistente conversacional con arquitectura RAG), no un estudio puramente teórico ni una intervención pedagógica.

## 3. Relación con los ejes temáticos dinamizadores

La propuesta se inscribe en el **Grupo Temático 1 (Línea de Gestión y Tecnologías)**, eje **"Inteligencia Artificial y Tecnologías Emergentes"**: su objeto de estudio es, precisamente, el diseño de un modelo de IA generativa aplicado a una función sustantiva institucional (permanencia/deserción estudiantil), no la instrumentación física de espacios ni de sensores — ese componente de infraestructura/IoT se cubre en una propuesta paralela independiente, con la que esta no compite ni se superpone.

Cumple además el eje transversal de la convocatoria (*"vinculación de herramientas IA en la construcción y la proyección de resultados"*) de forma nativa: la IA generativa no es un anexo del proyecto, es el objeto mismo de investigación y desarrollo.

## 4. Resumen

La deserción y el rezago académico son problemáticas persistentes en la educación superior colombiana, y la CUN no es la excepción: las alertas de permanencia suelen apoyarse en revisiones manuales de notas y asistencia, con baja cobertura y retroalimentación tardía para el estudiante. Esta propuesta plantea diseñar y prototipar un asistente conversacional de inteligencia artificial generativa, con arquitectura de generación aumentada por recuperación (RAG), que opere sobre datos institucionales verificables de un programa piloto (calificaciones parciales, asistencia, interacción en el LMS y Syllabus vigente) para identificar tempranamente patrones asociados a riesgo académico y generar recomendaciones explicables para el estudiante y el docente-tutor. A diferencia de plataformas comerciales de analítica educativa genéricas, el aporte diferencial es el anclaje explícito del modelo al contexto normativo y curricular propio de la CUN, lo que permite explicaciones más pertinentes que un tablero estadístico aislado y reduce el riesgo de alucinación del modelo generativo. El alcance del prototipo se limita a un piloto acotado —un programa académico, un periodo— con datos históricos ya existentes, evaluado mediante métricas de precisión de la alerta y una prueba de usabilidad con estudiantes y docentes voluntarios.

*(Conteo real: 187 palabras — cumple el máximo de 200.)*

## 5. Impacto, viabilidad y retorno de la propuesta (versión breve)

El impacto esperado es doble: (a) para el programa piloto, más oportunidad de intervención de bienestar/permanencia al anticipar el riesgo académico semanas antes que el corte de notas; (b) para la DNI, un insumo técnico reutilizable (arquitectura RAG documentada) para otros programas o para la próxima ventana Minciencias. La viabilidad económica es alta: el prototipo se construye sobre un modelo de lenguaje de bajo costo o de código abierto (por ejemplo, la API de GPT-4o mini o un modelo open-weight tipo Llama 3), orquestado con LangChain o LlamaIndex y una base vectorial ligera (FAISS o Chroma) para la recuperación de contexto institucional — herramientas sin licenciamiento adicional que caben en el techo de $5.000.000 de la convocatoria. El retorno institucional se mide en horas de revisión manual evitadas por el equipo de permanencia y en la trazabilidad de cada alerta a una fuente verificable, no a una "caja negra". La herramienta de IA prevista y su uso concreto: un LLM orquestado en arquitectura RAG sobre los datos y documentos propios del programa piloto, exclusivamente para generar explicaciones y recomendaciones ancladas a esas fuentes (nunca para decidir automáticamente sobre la permanencia de un estudiante, que sigue siendo decisión humana).

## 6. Objetivo general

Diseñar y prototipar un asistente conversacional de IA generativa, basado en una arquitectura de generación aumentada por recuperación (RAG) sobre datos institucionales verificables, que apoye la detección temprana de riesgo académico y la retroalimentación personalizada a estudiantes de un programa piloto de la CUN durante un periodo académico.

## 7. Objetivos específicos

1. **Caracterizar**, durante el primer mes del proyecto, las variables e indicadores de riesgo académico disponibles en las fuentes institucionales del programa piloto (calificaciones, asistencia, interacción en el LMS) y validarlas con el área de permanencia/bienestar de la CUN.
2. **Desarrollar**, durante el segundo mes, un prototipo funcional del asistente conversacional con arquitectura RAG que integre dichas fuentes y genere alertas y recomendaciones explicables y trazables a la fuente institucional.
3. **Evaluar**, durante el tercer mes, el desempeño del prototipo mediante métricas de precisión de la alerta (frente al histórico de casos de riesgo ya conocidos) y una prueba de usabilidad con al menos 10 estudiantes y 3 docentes-tutores del programa piloto.

## 8. Productos esperados (tipologías Minciencias)

| Tipología Minciencias | Producto | Objetivo específico asociado |
|---|---|---|
| Desarrollo tecnológico e innovación | Prototipo de software funcional (asistente RAG) + informe técnico de arquitectura | OE 2 |
| Formación de RRHH en CTeI | Vinculación de 1 estudiante-monitor o de semillero de Ingeniería de Sistemas al desarrollo y validación del prototipo | OE 2 y OE 3 |
| Generación de nuevo conocimiento | Ponencia o artículo corto que reporte el diseño metodológico y los resultados de la prueba piloto, para someter a un evento o revista institucional | OE 1 y OE 3 |

No se fuerzan las cuatro tipologías: la apropiación social del conocimiento queda fuera del alcance realista de 3 meses con un solo piloto.

## 9. Referentes reales (ancla del marco teórico, no lista completa)

Norma **IEEE** (propuesta de la Escuela de Ingenierías).

[1] V. Tinto, *Leaving College: Rethinking the Causes and Cures of Student Attrition*, 2nd ed. Chicago, IL, USA: Univ. of Chicago Press, 1993. — fundamenta teóricamente qué es y cómo se explica la deserción estudiantil, base conceptual del "riesgo académico" que el asistente busca detectar.

[2] G. Siemens, "Learning analytics: The emergence of a discipline," *American Behavioral Scientist*, vol. 57, no. 10, pp. 1380–1400, 2013. — sustenta el uso de analítica de aprendizaje institucional como antecedente directo del enfoque de datos verificables que propone esta propuesta.

[3] O. Zawacki-Richter, V. I. Marín, M. Bond, and F. Gouverneur, "Systematic review of research on artificial intelligence applications in higher education – where are the educators?," *Int. J. Educ. Technol. High. Educ.*, vol. 16, no. 1, art. 39, 2019. — mapea el estado del arte de IA en educación superior y respalda el aporte diferencial frente a herramientas genéricas.

[4] P. Lewis et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks," in *Proc. NeurIPS*, 2020. — referencia técnica de origen de la arquitectura RAG que se prototipa, clave para justificar por qué se ancla el modelo a fuentes verificables en lugar de generación libre.

[5] L. Aulck, N. Velagapudi, J. Blumenstock, and J. West, "Predicting student dropout in higher education," arXiv:1606.06364, 2016. — antecedente técnico de modelos predictivos de deserción con datos administrativos, comparable a las variables que se plantea caracterizar en el OE1.

[6] R. F. Kizilcec and S. Halawa, "Attrition and achievement gaps in online learning," in *Proc. 2nd ACM Conf. on Learning @ Scale (L@S)*, 2015, pp. 57–66. — evidencia empírica de brechas de logro y abandono en entornos con componente virtual, pertinente a la modalidad mixta de la CUN.

## 10. Viabilidad de alcance, tiempo y presupuesto

Con alcance acotado a **un solo programa piloto**, **datos históricos ya existentes** (sin necesidad de instrumentar nueva captura de datos) y herramientas de IA de bajo costo o de código abierto, la propuesta es ejecutable dentro de los ~3 meses y el techo de $5.000.000 de la convocatoria. Una versión multi-programa, multi-sede o con integración en tiempo real a los sistemas académicos de la CUN excede este instrumento y debe quedar planteada como fase 2 de escalamiento — no como el alcance de esta convocatoria — si la propuesta es aprobada y da resultados positivos en el piloto.

---

## Comparativa (para decidir entre propuestas paralelas)

| Título | Eje | Tipo de producto | Fuerza en "calidad de la propuesta" | Realismo en el plazo (~3 meses / $5.000.000) |
|---|---|---|---|---|
| Asistente de IA Generativa para Detección Temprana de Riesgo Académico en la CUN | Inteligencia Artificial y Tecnologías Emergentes (Grupo Temático 1) | Desarrollo de Software (prototipo RAG) | Alta: problema institucional real y verificable, referentes técnicos y teóricos sólidos, arquitectura técnica concreta (RAG) que evita la vaguedad de "se usará IA" | Alto: piloto acotado a un programa, datos ya existentes, stack de bajo costo — cabe en el presupuesto y el plazo si se limita a un solo programa/periodo |
