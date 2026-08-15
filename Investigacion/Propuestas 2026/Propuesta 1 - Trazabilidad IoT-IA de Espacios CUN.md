# Propuesta de Anteproyecto — Fase 1 (ideación)

## Sistema IoT-IA de Monitoreo y Trazabilidad de Espacios Académicos en la CUN

Convocatoria interna CUN 2026 (Fase II) · Formato INV-FO03 (Anexo 2) · Documento de **Fase 1** —
resumen ejecutivo para decisión, no el formulario completo.

**Investigador principal:** Julian Andrés Castaño Erazo — docente Ingeniería de Sistemas /
Especialización en Inteligencia Artificial, CUN.
**Correo:** julian_castanoe@cun.edu.co
**Rol desde el que se formula:** Ingeniero de Sistemas y docente universitario CUN.

> **Nota administrativa (no es un campo del INV-FO03, léase antes de radicar):** los Términos de
> Referencia exigen para el investigador principal (num. 5.1): vinculación activa con **contrato de
> tiempo completo**, **descarga horaria** aprobada por la DNI para investigación, **no tener
> pendientes** de convocatorias anteriores (incluido el cumplimiento íntegro del plan de trabajo
> 2025) y **CvLAC actualizado**. Este documento no verifica esas cuatro condiciones — quien radique
> debe confirmarlas antes de enviar la propuesta; si alguna no está resuelta, es motivo de rechazo
> administrativo independiente de la calidad del contenido.
>
> **Nota sobre los criterios de evaluación:** el propio documento de Términos de Referencia es
> inconsistente entre la tabla del numeral 11 (Elementos preliminares 2 / Impacto-viabilidad-retorno
> 28 / Calidad de la propuesta 50 / Resultados y productos 20 = 100) y el texto explicativo
> inmediatamente debajo (Elementos preliminares 20 / Calidad de la propuesta 60 / Resultados y
> productos 20 = 100, sin desglosar "impacto, viabilidad y retorno" como criterio aparte). No se
> resuelve aquí cuál es la correcta; este documento está escrito para el criterio más exigente de
> ambas lecturas: la **Calidad de la propuesta** (originalidad, claridad del problema, objetivos
> medibles, diseño metodológico, rigor teórico y referencias) es, bajo cualquier lectura, el bloque
> de mayor peso.

---

## 1. Tipo de Propuesta

☑ **Desarrollo de Software** — el entregable central es un sistema (firmware de nodos sensores +
backend + tablero de trazabilidad) con un componente de inteligencia artificial embebido; no se
marca "Innovación" porque el alcance de 3 meses no llega a una innovación validada en el mercado,
y no se marca "Investigación" porque no hay pregunta de investigación científica propiamente dicha,
sino un producto tecnológico aplicado a un problema institucional real.

## 2. Grupo Temático y Eje Dinamizador

- **Grupo Temático 1 — Línea de Gestión y Tecnologías.**
- **Eje Dinamizador:** *Tecnologías de la Información y la Comunicación e Internet de las Cosas
  (IoT).*
- **Por qué encaja:** la propuesta es, literalmente, una aplicación de IoT (sensórica distribuida,
  captura y transmisión de datos) e ICT (backend, tablero web) a un problema de gestión
  institucional (uso de espacios y equipos), y no un desarrollo de IA "de laboratorio" — encaja
  mejor aquí que en el eje "Inteligencia Artificial y Tecnologías Emergentes" porque la IA es un
  componente instrumental (detección de anomalías sobre datos de sensores), no el objeto de estudio.
  El **eje transversal de IA** se cubre con el modelo de detección de anomalías de uso y con el uso
  de un asistente de IA generativa para la construcción del software y la documentación (ver
  sección 5).

## 3. Resumen (máximo 200 palabras — conteo real: **197 palabras**)

Las sedes de la CUN operan bajo un modelo multi-sede y multi-modal (presencial, distancia y
virtual) que dificulta conocer, en tiempo real, cómo se usan realmente las aulas, laboratorios y
equipos tecnológicos disponibles para docencia y préstamo. Esta propuesta plantea diseñar e
implementar un piloto de sistema de Internet de las Cosas (IoT) e Inteligencia Artificial para el
monitoreo y trazabilidad del uso de espacios y equipos académicos en dos sedes de la Corporación.
Nodos sensores de bajo costo, con microcontrolador y sensores de presencia y variables ambientales,
capturarán datos de ocupación y condiciones de las aulas y laboratorios seleccionados. Un modelo de
aprendizaje automático analizará los patrones de uso y detectará anomalías como subutilización,
congestión o fallas de equipos, y un tablero de control entregará esa trazabilidad a los
coordinadores académicos para apoyar decisiones de asignación de espacios. El piloto se ejecutará
en aproximadamente tres meses con presupuesto ajustado a la convocatoria, priorizando componentes
de bajo costo y software abierto. Se espera un prototipo funcional verificable con datos reales, la
vinculación de estudiantes semillero en IoT e Inteligencia Artificial, y evidencia cuantitativa del
potencial de escalar la solución a más sedes y modalidades de la institución.

## 4. Objetivo general

Diseñar e implementar un piloto de sistema IoT-IA para el monitoreo y trazabilidad del uso de
aulas, laboratorios y equipos tecnológicos en dos sedes de la CUN, que permita optimizar su gestión
y asignación con información real y no con estimaciones manuales.

## 5. Objetivos específicos

1. **Diseñar** la arquitectura de sensórica IoT (nodos de presencia y variables ambientales) y el
   pipeline de captura, transmisión y almacenamiento de datos para el monitoreo de aulas y
   laboratorios en las dos sedes piloto, durante el primer mes de ejecución.
2. **Desarrollar** el modelo de detección de anomalías de uso (subutilización, congestión, fallas
   de equipos) y el tablero de trazabilidad para la gestión de espacios, integrando un asistente de
   IA generativa en el ciclo de construcción del software, durante el segundo mes de ejecución.
3. **Validar** el piloto con coordinadores académicos y docentes de las sedes seleccionadas y medir
   su efecto sobre la toma de decisiones de asignación de espacios, durante el tercer mes de
   ejecución.

*(El cumplimiento conjunto de los tres objetivos específicos constituye el objetivo general.)*

## 6. Impacto, viabilidad y retorno (versión breve)

**Impacto:** información objetiva y en tiempo real sobre uso real de aulas/laboratorios y equipos,
hoy gestionado con criterios manuales o históricos; medible mediante el porcentaje de espacios/
equipos monitoreados y el número de decisiones de reasignación tomadas con base en el tablero
durante el trimestre de ejecución. **Viabilidad:** componentes de bajo costo (microcontroladores
tipo ESP32, sensores PIR/ambientales de mercado libre, del orden de $80.000–150.000 COP por nodo) y
software de código abierto, lo que hace operable un piloto de 6 a 10 nodos en dos sedes dentro del
techo de $5.000.000 de la convocatoria. **Retorno institucional:** insumo de datos reales para
futuras decisiones de infraestructura y mantenimiento, y antecedente técnico aprovechable en la
próxima convocatoria Minciencias. **Herramienta de IA prevista:** un modelo de detección de
anomalías sobre series de tiempo de ocupación (Isolation Forest / Scikit-learn, entrenado con los
datos capturados por los sensores) para señalar patrones atípicos de uso, y un asistente de IA
generativa (Claude o ChatGPT) como apoyo de programación del firmware/backend y de redacción de la
documentación técnica del piloto — declarado explícitamente, no como uso genérico.

## 7. Productos esperados (por tipología Minciencias — solo las que el alcance real sostiene)

| Tipología Minciencias | Producto asociado | Objetivo específico que lo sostiene |
|---|---|---|
| Desarrollo tecnológico e innovación | Prototipo funcional del sistema IoT-IA (nodos sensores + backend + tablero de trazabilidad) desplegado en 2 sedes piloto | OE1 y OE2 |
| Formación de RRHH en CTeI | Vinculación documentada de 1–2 estudiantes de semillero (Ingeniería de Sistemas / Especialización en IA) como auxiliares de investigación en el desarrollo del piloto | OE2 |
| Generación de nuevo conocimiento | Documento técnico / ponencia interna con los resultados preliminares del piloto (patrones de uso detectados, lecciones del despliegue multi-sede) | OE3 |

*No se fuerzan las 4 tipologías: en 3 meses y con este presupuesto no hay alcance real para un
producto de apropiación social del conocimiento (divulgación externa) que no sea repetir el mismo
documento técnico bajo otro nombre.*

## 8. Referentes (ancla teórica — 5 fuentes reales y verificables)

1. **Al-Fuqaha, A., Guizani, M., Mohammadi, M., Aledhari, M., & Ayyash, M. (2015).** "Internet of
   Things: A survey on enabling technologies, protocols, and applications." *IEEE Communications
   Surveys & Tutorials*, 17(4), 2347–2376. — Marco de referencia estándar sobre arquitecturas y
   protocolos IoT; sostiene el diseño de la capa de sensórica y transmisión de datos.
2. **Zanella, A., Bui, N., Castellani, A., Vangelista, L., & Zorzi, M. (2014).** "Internet of
   Things for smart cities." *IEEE Internet of Things Journal*, 1(1), 22–32. — Referente para
   trasladar el paradigma de "ciudad inteligente" a la escala de un "campus inteligente" multi-sede.
3. **Minoli, D., Sohraby, K., & Occhiogrosso, B. (2017).** "IoT considerations, requirements, and
   architectures for smart buildings—Energy optimization and next-generation building management
   systems." *IEEE Internet of Things Journal*, 4(1), 269–283. — Base directa para el monitoreo
   ambiental y de ocupación de aulas/laboratorios que propone esta idea.
4. **Balaji, B., Xu, J., Nwokafor, A., Gupta, R., & Agarwal, Y. (2013).** "Sentinel: Occupancy based
   HVAC actuation using existing WiFi infrastructure within commercial buildings." *Proceedings of
   the 11th ACM Conference on Embedded Networked Sensor Systems (SenSys)*, 1–14. — Antecedente
   concreto de detección de ocupación de espacios con sensórica de bajo costo, aplicable al piloto.
5. **Bibri, S. E. (2018).** *Smart Sustainable Cities of the Future: The Untapped Potential of Big
   Data Analytics and Context-Aware Computing for Advancing Sustainability.* Springer. — Sostiene la
   discusión sobre analítica de datos e IA aplicada a infraestructura física institucional.

## 9. Viabilidad de alcance/tiempo

Es realista para los ~3 meses y el techo de $5.000.000 de esta convocatoria **si el piloto se
limita a 6–10 nodos sensores en 2 sedes** (no la instrumentación de todas las aulas de la
institución) y a un modelo de detección de anomalías simple sobre esos datos — no un sistema
predictivo de asignación automática de espacios, que sí exigiría un año y un presupuesto varias
veces mayor; si el usuario quiere ese alcance mayor, la versión aquí descrita es la que hay que
ejecutar primero como piloto para generar los datos que ese proyecto más ambicioso necesitaría.
