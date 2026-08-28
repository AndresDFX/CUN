# Aprendizaje automático supervisado para la predicción temprana de deserción académica en educación superior colombiana: protocolo reproducible y evaluación comparativa sobre un conjunto de datos sintético

**Supervised machine learning for the early prediction of student dropout in Colombian higher education: a reproducible protocol and comparative evaluation on a synthetic dataset**

---

**Autor de correspondencia**

Julian Andrés Castaño Espinosa
Escuela de Ingenierías, Corporación Unificada Nacional de Educación Superior — CUN
Bogotá, Colombia
julian_castanoe@cun.edu.co
ORCID: [POR COMPLETAR: registrar en orcid.org y pegar el identificador]

**Coautores**

[POR COMPLETAR: nombres, filiación, correo institucional y ORCID de los integrantes del Equipo 1
del semillero SIAES que participen efectivamente en la ejecución de los experimentos. Se
incorporan como coautores únicamente quienes cumplan los criterios de autoría del ICMJE y hayan
dado autorización expresa y por escrito. Este manuscrito no registra ningún dato de identificación
personal de estudiantes.]

**Filiación institucional del trabajo:** Semillero de Investigación en Inteligencia Artificial
Aplicada a la Educación Superior (SIAES), Escuela de Ingenierías, CUN.

---

## RESUMEN

La deserción académica en la educación superior colombiana sigue siendo un problema de gestión
institucional frente al cual las respuestas predominantes son reactivas: se interviene cuando el
estudiante ya abandonó. La analítica predictiva ofrece una alternativa anticipatoria, pero su
adopción está limitada por la ausencia de protocolos reproducibles y por las barreras legales de
acceso a datos académicos personales. Este trabajo tiene un objetivo deliberadamente acotado:
construir y documentar un protocolo experimental reproducible para comparar cuatro clasificadores
supervisados —regresión logística, bosque aleatorio, potenciación de gradiente extremo y
perceptrón multicapa— en la predicción de riesgo de deserción con información disponible durante
las primeras semanas del periodo académico. **La evaluación se realiza sobre un conjunto de datos
sintético**, generado paramétricamente y calibrado con estadísticos agregados de fuentes públicas;
**no se emplean registros de estudiantes reales y, en consecuencia, ninguna cifra de desempeño
reportada puede interpretarse como evidencia sobre una cohorte real**. El protocolo incorpora
validación cruzada estratificada repetida, intervalos de confianza por remuestreo, atribución de
variables con valores de Shapley, auditoría de equidad por subgrupos y validación externa sobre un
conjunto de datos real de acceso público. [PENDIENTE: síntesis de los resultados principales
—AUC-PR, exactitud y F1 del mejor modelo con su intervalo de confianza— completar tras la
ejecución de los experimentos.] La contribución es metodológica e instrumental: un protocolo
auditable y una línea base honesta sobre la cual validar después con datos institucionales reales.

**Palabras clave:** analítica del aprendizaje, aprendizaje automático supervisado, datos
sintéticos, deserción estudiantil, equidad algorítmica, reproducibilidad.

---

## ABSTRACT

Student dropout in Colombian higher education remains an institutional management problem
addressed mostly through reactive measures: intervention occurs after the student has already
left. Predictive analytics offers an anticipatory alternative, yet its adoption is constrained by
the absence of reproducible protocols and by the legal barriers to accessing personal academic
records. This study pursues a deliberately narrow objective: to build and document a reproducible
experimental protocol for comparing four supervised classifiers —logistic regression, random
forest, extreme gradient boosting and a multilayer perceptron— on the task of predicting dropout
risk from information available during the first weeks of the academic term. **The evaluation is
conducted on a synthetic dataset**, generated parametrically and calibrated against aggregate
statistics from public sources; **no real student records are used and, consequently, no reported
performance figure may be interpreted as evidence about a real cohort**. The protocol includes
repeated stratified cross-validation, bootstrap confidence intervals, Shapley-value feature
attribution, subgroup fairness auditing, and external validation on a publicly available
real-world dataset. [PENDING: summary of the main results —AUC-PR, accuracy and F1 of the best
model with confidence intervals— to be completed once the experiments have been run.] The
contribution is methodological and instrumental: an auditable protocol and an honest baseline
against which to validate later with real institutional data.

**Keywords:** learning analytics, supervised machine learning, synthetic data, student dropout,
algorithmic fairness, reproducibility.

---

## 1. INTRODUCCIÓN

La permanencia estudiantil es uno de los indicadores que con mayor fuerza condiciona la
sostenibilidad académica y financiera de las instituciones de educación superior. En Colombia el
seguimiento de este fenómeno está institucionalizado desde hace más de una década a través del
Sistema para la Prevención de la Deserción de la Educación Superior (SPADIES) del Ministerio de
Educación Nacional (MEN, s.f.), y la metodología de seguimiento, diagnóstico y prevención
publicada por el propio Ministerio (MEN, 2009) sigue siendo el marco de referencia para el
análisis del abandono en el país. [DATO POR VERIFICAR EN SPADIES ANTES DEL SOMETIMIENTO: tasa de
deserción por cohorte y tasa de deserción anual más recientes publicadas, con año de corte y nivel
de formación. No se incorpora aquí ninguna cifra que no haya sido consultada directamente en la
fuente oficial.]

El problema no es la ausencia de medición, sino el momento de la intervención. Los sistemas de
información institucionales registran el abandono cuando ya ocurrió; los programas de apoyo
—tutorías, acompañamiento psicosocial, alivios financieros— se activan sobre estudiantes que ya
interrumpieron su matrícula o que acumularon un historial de pérdida de asignaturas. La analítica
del aprendizaje, constituida como disciplina a partir del trabajo fundacional de Siemens (2013),
propone invertir esa secuencia: usar las trazas que el estudiante genera durante el periodo en
curso para estimar un riesgo y actuar antes de que el desenlace se produzca. La experiencia de
*Course Signals* en Purdue University (Arnold y Pistilli, 2012) mostró que un sistema de alerta
temprana integrado en la operación docente podía asociarse con mejoras de retención, y desde
entonces la predicción de deserción se consolidó como una de las tareas canónicas de la minería de
datos educativos (Romero y Ventura, 2020; Prenkaj et al., 2020).

Ese consenso internacional, sin embargo, no se traslada automáticamente al contexto colombiano de
las instituciones privadas de acceso masivo. Existen al menos tres obstáculos concretos. El
primero es de disponibilidad: acceder a registros académicos personales para entrenar un modelo
exige autorización del titular, finalidad declarada y medidas de tratamiento conformes con la Ley
Estatutaria 1581 de 2012 (Congreso de la República de Colombia, 2012), un trámite que puede
consumir por completo el tiempo disponible de un proyecto de investigación de corta duración. El
segundo es de transferibilidad: buena parte de los modelos publicados se entrenó sobre poblaciones
que no se parecen a la colombiana, y la validez poblacional de un modelo educativo no se hereda
por analogía (Ocumpaugh et al., 2014). El tercero es de reproducibilidad: en la literatura
aplicada abundan los reportes de exactitud sin especificación suficiente del procedimiento de
validación, sin intervalos de confianza y sin auditoría por subgrupos, lo que impide contrastar
resultados entre estudios y, sobre todo, impide auditar el modelo antes de exponerlo a decisiones
que afectan a personas.

Este artículo aborda el tercer obstáculo, que es el único de los tres que puede resolverse sin
acceso previo a datos institucionales, y lo hace reconociendo sus propios límites. La pregunta de
investigación que orienta el trabajo es la siguiente:

> **¿Qué desempeño comparativo, qué estructura de atribución de variables y qué comportamiento por
> subgrupos exhiben cuatro clasificadores supervisados en la predicción temprana de deserción
> académica, cuando se evalúan bajo un protocolo reproducible sobre un conjunto de datos sintético
> calibrado para el contexto de la educación superior colombiana?**

La formulación es intencionalmente modesta y la modestia es parte del argumento. Un conjunto de
datos sintético no autoriza a afirmar nada sobre estudiantes reales: reproduce las relaciones que
su generador codifica y nada más (Dankar e Ibrahim, 2021). Lo que sí permite es construir, depurar
y auditar el instrumento —el protocolo, el código, las métricas, la auditoría de equidad— en
condiciones controladas, de modo que cuando la institución autorice el uso de datos reales el
experimento pueda ejecutarse sin rediseño. Esa distinción entre *validar el instrumento* y
*validar la hipótesis sustantiva* organiza todo el manuscrito.

**Objetivo general.** Construir y evaluar un protocolo experimental reproducible para la
comparación de clasificadores supervisados en la predicción temprana de deserción académica en
educación superior colombiana, empleando un conjunto de datos sintético declarado como tal.

**Objetivos específicos.**

1. Generar y documentar un conjunto de datos sintético de 5.000 registros y 28 variables
   —académicas, demográficas, socioeconómicas y de actividad en el aula virtual— calibrado con
   estadísticos agregados de fuentes públicas, acompañado de su ficha de datos.
2. Comparar el desempeño predictivo de cuatro clasificadores supervisados bajo validación cruzada
   estratificada repetida, reportando métricas sensibles al desbalance de clases con intervalos de
   confianza por remuestreo.
3. Auditar el modelo de mejor desempeño en dos dimensiones —atribución de variables mediante
   valores de Shapley y paridad de tasas de error por subgrupos— y contrastar su comportamiento en
   una validación externa sobre un conjunto de datos real de acceso público.

El resto del artículo se organiza así: la sección 2 revisa los trabajos relacionados en cuatro
frentes; la sección 3 detalla la metodología, incluida la declaración explícita sobre la
naturaleza sintética de los datos; la sección 4 presenta los resultados; la sección 5 los discute
en diálogo con la literatura y expone las limitaciones; la sección 6 concluye.

---

## 2. TRABAJOS RELACIONADOS

### 2.1 Modelos teóricos de la deserción

Antes de ser un problema de clasificación, la deserción fue un problema de teoría social. Spady
(1970) propuso la primera síntesis interdisciplinaria del abandono universitario, y Tinto (1993)
formuló el modelo de integración que aún estructura buena parte de la investigación del campo: la
permanencia depende del grado de integración académica y social del estudiante en la institución,
y el abandono es el desenlace de un proceso longitudinal de desajuste, no un evento puntual. Bean
y Metzner (1985) extendieron el modelo a los estudiantes no tradicionales —trabajadores, mayores,
con dependientes económicos—, cuya integración social en el campus es estructuralmente baja y para
quienes pesan más los factores externos que los institucionales.

La distinción no es un ornamento teórico en un artículo técnico: determina qué variables tienen
sentido en el modelo. Una institución de acceso masivo con población mayoritariamente trabajadora
se parece más al escenario de Bean y Metzner que al de Tinto y, en consecuencia, las variables de
integración social del campus tendrán poco poder explicativo frente a las de carga laboral,
dependencia económica y regularidad de la asistencia. En Colombia, la metodología del Ministerio
de Educación Nacional (MEN, 2009) organiza los determinantes en cuatro categorías —individuales,
académicos, socioeconómicos e institucionales— que aquí se emplean como esquema de construcción de
variables.

### 2.2 Minería de datos educativos y predicción de deserción

La aplicación de aprendizaje automático a la predicción de deserción tiene ya un cuerpo
consolidado de resultados. Dekker et al. (2009) mostraron, en un estudio temprano y todavía
citado, que árboles de decisión simples entrenados con datos de matrícula y desempeño del primer
semestre alcanzaban desempeños comparables a los de modelos más complejos, con la ventaja de ser
interpretables por el personal académico. Delen (2010) comparó sistemáticamente varias familias de
algoritmos para gestión de retención y documentó la relevancia del tratamiento del desbalance de
clases, un problema que atraviesa toda la literatura posterior. Márquez-Vera et al. (2013)
abordaron explícitamente la combinación de alta dimensionalidad y desbalance mediante programación
genética y técnicas de balanceo.

Los trabajos más recientes desplazaron el foco hacia dos preguntas: cuánta anticipación es posible
y con qué datos. Aulck et al. (2016) reportaron que la información disponible en el momento de la
matrícula ya contiene señal predictiva apreciable en cohortes universitarias grandes. Berens et
al. (2019) construyeron un sistema de alerta temprana sobre datos administrativos de universidades
alemanas y mostraron que el desempeño mejora sustancialmente al incorporar los resultados del
primer semestre. Chung y Lee (2019) aplicaron bosques aleatorios a la detección temprana en
educación media, y Kabathova y Drlik (2021) compararon varias técnicas en un curso universitario
concreto, subrayando que el desempeño depende fuertemente del curso y del momento de corte, lo que
relativiza cualquier comparación de exactitudes entre estudios con diseños distintos.

En la educación en línea, Kizilcec y Halawa (2015) documentaron brechas sistemáticas de abandono y
logro asociadas a características demográficas, y la revisión de Prenkaj et al. (2020) sistematizó
los enfoques de predicción de deserción en cursos en línea, señalando la heterogeneidad de
definiciones de la variable objetivo como el principal obstáculo para la acumulación de
conocimiento en el campo. La revisión actualizada de Romero y Ventura (2020) confirma esa
observación desde el campo más amplio de la minería de datos educativos, y la revisión sistemática
de Zawacki-Richter et al. (2019) añade una crítica de fondo: en la mayoría de las aplicaciones de
inteligencia artificial en educación superior, los educadores están ausentes del diseño.

De este cuerpo se desprende el vacío que motiva el presente trabajo. Los estudios en contexto
colombiano con datos tempranos y protocolo de validación completamente especificado son escasos, y
prácticamente ninguno publica el código y el generador de datos que permitirían replicar el
experimento en otra institución. [REFERENCIA POR VERIFICAR: estudios colombianos recientes de
predicción de deserción con aprendizaje automático publicados en revistas indexadas nacionales;
realizar búsqueda en SciELO Colombia, Redalyc y Publindex antes del sometimiento e incorporar dos
o tres referencias locales, o bien retirar la afirmación de escasez si la búsqueda la desmiente.]

### 2.3 Datos sintéticos como sustituto metodológico

Generar datos sintéticos para desarrollar y auditar modelos cuando los datos reales no están
disponibles —o no pueden compartirse— es una práctica establecida, con literatura propia y con
límites bien documentados. Patki et al. (2016) formalizaron el enfoque generativo basado en la
estructura relacional de la base de datos; Xu et al. (2019) propusieron el uso de redes
generativas antagónicas condicionales para datos tabulares, hoy referencia habitual en el área; y
Jordon et al. (2019) mostraron cómo incorporar garantías formales de privacidad diferencial al
proceso de generación.

La pregunta crítica es si un modelo entrenado o evaluado sobre datos sintéticos conserva validez.
Rankin et al. (2020) evaluaron esa transferencia en el dominio de la salud y encontraron que el
desempeño obtenido sobre datos sintéticos puede diferir de forma no trivial del obtenido sobre los
datos reales correspondientes, con degradación dependiente del algoritmo y del método de
generación. Dankar e Ibrahim (2021) sistematizaron las condiciones bajo las cuales la generación
sintética resulta útil y las precauciones que debe declarar quien la emplea. La conclusión
convergente de ambos trabajos es la que este artículo adopta como principio: los datos sintéticos
sirven para desarrollar, depurar y auditar el instrumento, y no sirven para sostener afirmaciones
sustantivas sobre la población que pretenden imitar.

### 2.4 Equidad, explicabilidad y ética de la predicción educativa

Un sistema que clasifica estudiantes como "en riesgo" produce consecuencias materiales, y la
literatura sobre sus riesgos es tan relevante como la de su desempeño. Mehrabi et al. (2021)
ofrecen la sistematización de referencia sobre sesgo y equidad en aprendizaje automático, y Hardt
et al. (2016) formalizaron el criterio de igualdad de oportunidad que aquí se emplea como métrica
de auditoría. En el dominio educativo, Baker y Hawn (2022) documentaron cómo el sesgo algorítmico
se manifiesta específicamente en sistemas educativos, y Gardner et al. (2019) propusieron el
análisis por segmentos (*slicing analysis*) como procedimiento estándar para detectar disparidades
de desempeño que las métricas agregadas ocultan. Holstein y Doroudi (2021) plantean la pregunta de
fondo —si la inteligencia artificial educativa amplifica o alivia las inequidades existentes— y
muestran que la respuesta depende del diseño, no de la tecnología.

Sobre explicabilidad, Lundberg y Lee (2017) unificaron las aproximaciones de atribución de
importancia mediante valores de Shapley, y Ribeiro et al. (2016) propusieron explicaciones locales
agnósticas al modelo. Rudin (2019) formula una objeción que este trabajo toma en serio: en
decisiones de alto impacto, explicar a posteriori un modelo opaco es inferior a usar desde el
principio un modelo interpretable; por eso el protocolo incluye la regresión logística no como
línea base débil sino como candidato legítimo, y compara su desempeño con el de los modelos de
conjunto antes de recomendar cualquiera de ellos.

En el plano normativo, Slade y Prinsloo (2013) identificaron los dilemas centrales de la analítica
del aprendizaje y Prinsloo y Slade (2017) formularon la "obligación de actuar": si una institución
detecta riesgo y no interviene, la detección misma se convierte en un problema ético. El marco de
la UNESCO (2023) para inteligencia artificial generativa en educación e investigación, la política
nacional colombiana de transformación digital e inteligencia artificial (Departamento Nacional de
Planeación [DNP], 2019) y la Ley Estatutaria 1581 de 2012 (Congreso de la República de Colombia, 2012) completan el marco
aplicable. Para la documentación del conjunto de datos y del modelo se adoptan las prácticas de
Gebru et al. (2021) y Mitchell et al. (2019).

---

## 3. METODOLOGÍA

### 3.1 Tipo de estudio y plan de análisis

Se trata de un estudio cuantitativo, de diseño experimental computacional y alcance comparativo,
cuyo objeto de evaluación son cuatro algoritmos de clasificación supervisada aplicados a una misma
tarea sobre un mismo conjunto de datos. No hay intervención sobre personas, no hay recolección de
información primaria y no hay participantes humanos.

El plan de análisis —selección de modelos, particiones, métricas primarias y secundarias, criterio
de comparación estadística y criterios de auditoría de equidad— quedó fijado y documentado en el
repositorio del proyecto **antes** de ejecutar cualquier experimento, con el fin de evitar la
selección posterior de la métrica o del modelo que mejor luce. Ninguna métrica reportada en la
sección 4 se añadió al plan después de conocer los resultados. [PENDIENTE: consignar el
identificador de confirmación (*commit hash*) y la fecha del documento del plan de análisis en el
repositorio, como evidencia verificable de esta afirmación. Si esa evidencia no existe, esta
afirmación debe retirarse del manuscrito.]

### 3.2 Naturaleza del conjunto de datos: declaración explícita

**El conjunto de datos utilizado en este estudio es sintético.** Fue generado por procedimiento
paramétrico y no contiene, ni deriva de, registros de estudiantes reales de ninguna institución.
No se accedió a bases de datos académicas institucionales, no se trataron datos personales y, por
lo tanto, no fue necesario ni procedente recabar consentimiento informado de estudiantes. Toda
cifra de desempeño reportada en este artículo describe el comportamiento de los algoritmos sobre
un conjunto de datos artificial y **no constituye evidencia sobre el comportamiento de una cohorte
real de estudiantes de la Corporación Unificada Nacional de Educación Superior ni de ninguna otra
institución**.

Esta decisión no es una conveniencia sino una restricción declarada del diseño. El uso de
registros académicos reales requiere autorización del titular, finalidad expresa y medidas de
tratamiento conformes a la Ley Estatutaria 1581 de 2012 (Congreso de la República de Colombia,
2012), además del aval del Comité de Ética de la Investigación Institucional; ese trámite excede
el horizonte temporal del presente estudio y constituye la primera etapa del trabajo futuro
(sección 6).

### 3.3 Procedimiento de generación y calibración

El generador produce **5.000 registros** con **28 variables** predictoras y una variable objetivo
binaria (abandono del periodo académico). El procedimiento consta de cinco pasos:

1. **Definición del esquema de variables** a partir de las cuatro categorías de determinantes de
   la metodología del MEN (2009) —individuales, académicos, socioeconómicos e institucionales—,
   más un bloque de actividad en el aula virtual derivado de la literatura de analítica del
   aprendizaje (Siemens, 2013; Romero y Ventura, 2020).
2. **Calibración de distribuciones marginales** de las variables demográficas y socioeconómicas
   con estadísticos agregados de fuentes públicas. [PENDIENTE: registrar la fuente exacta, el año
   de corte y la tabla utilizada para cada variable calibrada, en la ficha de datos. No se
   declararán distribuciones cuya fuente no haya sido consultada directamente.]
3. **Imposición de una estructura de dependencia** entre predictoras y variable objetivo mediante
   un modelo generativo explícito, cuyos coeficientes se fijan a priori y se publican junto con el
   código. Esta es la decisión metodológicamente más delicada del estudio: el generador determina
   qué relaciones puede descubrir el clasificador, y por eso los coeficientes se hacen públicos en
   lugar de dejarse implícitos.
4. **Introducción controlada de ruido, valores faltantes y desbalance de clases**, con una
   prevalencia de la clase minoritaria fijada a priori dentro del rango documentado en la
   literatura de deserción por periodo. [PENDIENTE: fijar y declarar el valor exacto de
   prevalencia empleado y su justificación documental.]
5. **Documentación** del conjunto siguiendo el esquema de fichas de datos de Gebru et al. (2021):
   motivación, composición, proceso de generación, usos recomendados y —de forma explícita— usos
   desaconsejados.

El generador y el conjunto resultante se publican con licencia abierta e identificador persistente
para permitir replicación (sección 3.11).

### 3.4 Variables y punto de corte temporal

Las 28 variables se agrupan en cinco bloques: (i) demográficas; (ii) socioeconómicas; (iii)
antecedentes académicos previos al ingreso; (iv) desempeño académico del periodo en curso hasta la
semana de corte; y (v) actividad en el aula virtual hasta la semana de corte. El punto de corte se
fija en la **semana 4** del periodo académico, de modo que el modelo solo dispone de información
que en un despliegue real estaría efectivamente disponible en ese momento. La restricción es
deliberada: los estudios que alcanzan desempeños altos usando calificaciones finales o información
posterior al desenlace resuelven un problema distinto —y trivial— del que interesa a una alerta
temprana (Berens et al., 2019; Kabathova y Drlik, 2021).

La variable objetivo se define como el no registro de matrícula en el periodo inmediatamente
siguiente, condicionado a no haber culminado el plan de estudios. La heterogeneidad de
definiciones de esta variable es, según Prenkaj et al. (2020), la principal fuente de
incomparabilidad entre estudios, razón por la cual se explicita aquí.

### 3.5 Preprocesamiento

Todo el preprocesamiento se encapsula dentro de las particiones de validación cruzada para evitar
fuga de información: la imputación, la estandarización, la codificación de variables categóricas y
el balanceo se ajustan únicamente con los datos de entrenamiento de cada pliegue y se aplican al
pliegue de prueba. Para el desbalance de clases se emplea sobremuestreo sintético de la clase
minoritaria (Chawla et al., 2002), aplicado exclusivamente sobre el conjunto de entrenamiento; se
reporta también el desempeño sin balanceo, dado que la métrica primaria elegida es robusta al
desbalance.

### 3.6 Modelos comparados

Se comparan cuatro clasificadores, seleccionados para cubrir el espectro entre interpretabilidad y
capacidad:

| Modelo | Familia | Razón de inclusión |
|---|---|---|
| Regresión logística regularizada | Lineal, interpretable | Línea base interpretable y candidato legítimo, según el argumento de Rudin (2019) |
| Bosque aleatorio | Conjunto de árboles, *bagging* | Referencia dominante en la literatura de deserción (Breiman, 2001; Chung y Lee, 2019) |
| Potenciación de gradiente extremo | Conjunto de árboles, *boosting* | Estado del arte en datos tabulares (Chen y Guestrin, 2016) |
| Perceptrón multicapa | Red neuronal densa | Contraste con modelos no basados en árboles |

Los hiperparámetros se ajustan por búsqueda aleatoria (Bergstra y Bengio, 2012) dentro de una
validación cruzada anidada, de modo que la selección de hiperparámetros nunca observa los datos
con los que se estima el desempeño final. Los espacios de búsqueda se declaran íntegramente en el
repositorio.

### 3.7 Protocolo de validación y métricas

El desempeño se estima mediante **validación cruzada estratificada de 10 pliegues repetida 5
veces**, con semilla fijada y publicada. Se prefiere la repetición al pliegue único porque, en
muestras de este tamaño, la varianza entre particiones es del mismo orden que las diferencias
entre modelos que suelen reportarse como sustantivas (Varoquaux, 2018; Vabalas et al., 2019).

Las métricas se reportan con **intervalos de confianza del 95 % estimados por remuestreo
*bootstrap*** (Efron y Tibshirani, 1993). Reportar una exactitud puntual sin intervalo es, en este
contexto, una afirmación no verificable, y el protocolo lo prohíbe explícitamente.

- **Métrica primaria:** área bajo la curva de precisión-exhaustividad (AUC-PR). Se elige sobre el
  área bajo la curva ROC porque, con clases desbalanceadas, la curva ROC ofrece una imagen
  optimista del desempeño (Davis y Goadrich, 2006; Saito y Rehmsmeier, 2015).
- **Métricas secundarias:** exactitud, precisión, exhaustividad, F1 y AUC-ROC, reportadas para
  permitir la comparación con la literatura existente, que mayoritariamente las usa.
- **Comparación entre modelos:** prueba de Friedman sobre los resultados por pliegue con prueba
  post hoc de Nemenyi, según el procedimiento de Demšar (2006), en lugar de comparaciones por
  pares sin corrección.
- **Umbral de decisión:** no se fija en 0,5 por defecto. Se selecciona sobre el conjunto de
  entrenamiento maximizando la exhaustividad sujeta a una precisión mínima admisible, bajo el
  supuesto operativo de que en una alerta temprana el costo del falso negativo —no detectar a
  quien abandona— es mayor que el del falso positivo —ofrecer acompañamiento a quien no lo
  necesitaba—. [PENDIENTE: declarar el valor de precisión mínima adoptado y su justificación
  operativa.]

### 3.8 Explicabilidad y auditoría de equidad

Al modelo de mejor desempeño se le aplican dos análisis obligatorios.

**Atribución de variables.** Se calculan valores de Shapley (Lundberg y Lee, 2017) globales y
locales. La atribución global se contrasta con la estructura de dependencia impuesta por el
generador: si el modelo no recupera las relaciones que el generador codificó, el problema es del
modelo o del protocolo, no de los datos. Esta verificación de consistencia es una de las pocas
ventajas metodológicas reales de trabajar con datos sintéticos, y se explota deliberadamente.

**Auditoría de equidad.** Se realiza análisis por segmentos (Gardner et al., 2019) sobre los
atributos potencialmente sensibles del conjunto (estrato socioeconómico, sexo registrado,
condición de trabajador, modalidad). Para cada subgrupo se reportan las tasas de falsos positivos
y falsos negativos y se evalúa el criterio de igualdad de oportunidad (Hardt et al., 2016). Se
documenta cualquier disparidad, con la advertencia de que sobre datos sintéticos la disparidad
detectada refleja el generador y no una inequidad social observada.

### 3.9 Validación externa sobre datos reales de acceso público

Para acotar el principal riesgo del diseño —que el protocolo funcione solo sobre el mundo que su
propio generador construyó—, el mismo protocolo, sin modificación alguna, se ejecuta sobre un
conjunto de datos **real y de acceso público**: el conjunto de predicción de abandono y éxito
académico publicado por Realinho et al. (2022), construido a partir de registros de una
institución de educación superior portuguesa y descrito metodológicamente en Martins et al.
(2021). Este conjunto no es colombiano y no resuelve el problema de validez poblacional
(Ocumpaugh et al., 2014), pero sí permite comprobar que el protocolo produce resultados razonables
sobre datos que no fueron generados por sus autores, que es exactamente lo que la crítica de
Rankin et al. (2020) exige verificar.

### 3.10 Herramientas y entorno

Los experimentos se implementan en Python con scikit-learn (Pedregosa et al., 2011) para el
preprocesamiento, la regresión logística, el bosque aleatorio y el perceptrón multicapa; la
biblioteca XGBoost para la potenciación de gradiente (Chen y Guestrin, 2016); y la implementación
de referencia de valores de Shapley para la atribución (Lundberg y Lee, 2017). [PENDIENTE:
registrar las versiones exactas de Python y de cada biblioteca, y adjuntar el archivo de entorno
que permite reconstruirlo.]

### 3.11 Reproducibilidad

Se publican, con licencia abierta: el generador de datos sintéticos con sus coeficientes, el
conjunto generado, el código completo de los experimentos, el plan de análisis previo, los
archivos de entorno y las semillas aleatorias. [PENDIENTE: crear el repositorio público, depositar
el conjunto de datos en un repositorio con identificador persistente y consignar aquí la URL y el
identificador.] El conjunto se acompaña de su ficha de datos (Gebru et al., 2021) y el modelo
seleccionado, de su tarjeta de modelo (Mitchell et al., 2019), incluida la declaración explícita
de usos desaconsejados.

### 3.12 Declaración de uso de herramientas de inteligencia artificial

En la elaboración de este manuscrito se emplearon asistentes de inteligencia artificial generativa
—Claude (Anthropic) y ChatGPT (OpenAI)— para tres tareas acotadas: apoyo en la identificación y
depuración de referentes bibliográficos, redacción y edición de borradores de secciones, y
verificación de consistencia interna entre objetivos, metodología y resultados. **Ninguna de las
herramientas generó datos, resultados experimentales ni referencias bibliográficas que no hayan
sido verificadas individualmente por los autores en su fuente original.** El diseño experimental,
la interpretación de los resultados y las decisiones metodológicas son responsabilidad exclusiva
de los autores, conforme a las orientaciones de la UNESCO (2023) sobre uso de inteligencia
artificial generativa en investigación.

### 3.13 Consideraciones éticas

El estudio no involucra participantes humanos ni trata datos personales, por lo que no requirió
consentimiento informado. Se pone no obstante en conocimiento del Comité de Ética de la
Investigación Institucional, en su calidad de estudio preparatorio de una fase posterior que sí
tratará datos académicos reales. [PENDIENTE: número y fecha del acta del Comité, o constancia
escrita de que el estudio no requiere aval por no tratar datos personales; solicitar antes del
sometimiento.] La discusión de los riesgos éticos del despliegue se desarrolla en la sección 5.4.

---

## 4. RESULTADOS

> **Nota de estado del manuscrito (eliminar antes del sometimiento).** Los experimentos descritos
> en la sección 3 estaban programados para ejecutarse entre el 16 y el 30 de agosto de 2026 y, a
> la fecha de redacción de esta versión, **no se dispone de resultados medidos y verificables**.
> Esta sección conserva íntegra la estructura de presentación acordada en el plan de análisis
> previo, con marcadores explícitos en cada punto donde debe entrar un valor. **No se ha estimado,
> redondeado ni anticipado ninguna cifra.** El manuscrito no debe someterse a ninguna revista
> antes de que esta sección esté completa con valores medidos.

### 4.1 Caracterización del conjunto de datos generado

[PENDIENTE: número final de registros tras depuración, prevalencia observada de la clase
minoritaria, porcentaje de valores faltantes por bloque de variables y estadísticos descriptivos
de las variables continuas — completar tras la generación.]

**Tabla 1.** Estadísticos descriptivos del conjunto de datos sintético por bloque de variables.

| Bloque | N.º de variables | Tipo | Estadístico resumen | Valores faltantes (%) |
|---|---|---|---|---|
| Demográficas | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Socioeconómicas | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Antecedentes académicos | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Desempeño en curso (semana 4) | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Actividad en aula virtual (semana 4) | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |

### 4.2 Comparación de desempeño entre modelos

[PENDIENTE: descripción textual de la comparación, indicando qué modelo obtuvo el mejor AUC-PR y
si la diferencia con el segundo es estadísticamente distinguible según la prueba de Friedman con
post hoc de Nemenyi (Demšar, 2006). Si las diferencias no resultan distinguibles, debe decirse así
de forma explícita en lugar de declarar un ganador.]

**Tabla 2.** Desempeño comparativo de los cuatro clasificadores. Validación cruzada estratificada
de 10 pliegues repetida 5 veces sobre el conjunto de datos sintético. Media e intervalo de
confianza del 95 % por remuestreo.

| Modelo | AUC-PR (primaria) | AUC-ROC | Exactitud | Precisión | Exhaustividad | F1 |
|---|---|---|---|---|---|---|
| Regresión logística | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Bosque aleatorio | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Potenciación de gradiente extremo | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Perceptrón multicapa | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |

**Figura 1.** Curvas de precisión-exhaustividad de los cuatro modelos, con banda de variabilidad
entre pliegues. [PENDIENTE: generar figura.]

**Figura 2.** Matriz de confusión del modelo de mejor desempeño en el umbral operativo
seleccionado. [PENDIENTE: exactitud medida, F1, matriz de confusión — completar tras los
experimentos. Reportar el umbral empleado y el número absoluto de falsos negativos, que es la
cifra operativamente decisiva en una alerta temprana.]

### 4.3 Efecto del punto de corte temporal

[PENDIENTE: comparación del desempeño con información hasta la semana 4 frente a cortes
alternativos (semanas 2, 6 y 8), para cuantificar el intercambio entre anticipación y exactitud.
Es una de las contribuciones informativas del protocolo y no debe omitirse.]

**Tabla 3.** Desempeño del mejor modelo según la semana de corte.

| Semana de corte | AUC-PR | Exhaustividad | Falsos negativos (n) |
|---|---|---|---|
| Semana 2 | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Semana 4 | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Semana 6 | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |
| Semana 8 | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |

### 4.4 Atribución de variables

[PENDIENTE: importancia global por valores de Shapley del modelo seleccionado, y verificación de
consistencia contra los coeficientes del generador. Debe reportarse explícitamente si el modelo
recuperó o no la estructura impuesta, incluido el caso en que no la haya recuperado.]

**Figura 3.** Importancia global de variables por valores de Shapley. [PENDIENTE: generar figura.]

### 4.5 Auditoría de equidad por subgrupos

[PENDIENTE: tasas de falsos positivos y falsos negativos por subgrupo y evaluación del criterio de
igualdad de oportunidad. Reportar todas las disparidades encontradas, incluidas las desfavorables
al modelo.]

**Tabla 4.** Tasas de error por subgrupo del modelo seleccionado.

| Atributo | Subgrupo | Tasa de falsos positivos | Tasa de falsos negativos | Brecha de igualdad de oportunidad |
|---|---|---|---|---|
| [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |

### 4.6 Validación externa sobre datos reales de acceso público

[PENDIENTE: resultados de la ejecución del protocolo, sin modificaciones, sobre el conjunto de
Realinho et al. (2022), y comparación con el desempeño obtenido sobre el conjunto sintético. La
magnitud y el sentido de la diferencia entre ambos es el resultado más informativo del estudio y
debe reportarse aunque sea desfavorable.]

**Tabla 5.** Desempeño del protocolo sobre el conjunto sintético frente al conjunto real público.

| Conjunto | AUC-PR | AUC-ROC | F1 | Diferencia respecto al sintético |
|---|---|---|---|---|
| Sintético (este estudio) | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | — |
| Real público (Realinho et al., 2022) | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] | [PENDIENTE] |

---

## 5. DISCUSIÓN

### 5.1 Qué puede y qué no puede afirmarse con este diseño

La primera obligación de la discusión es delimitar el alcance de las afirmaciones. Los resultados
de la sección 4, una vez completados, describirán el comportamiento de cuatro algoritmos sobre un
conjunto de datos cuya estructura de dependencia fue impuesta por los propios autores. En sentido
estricto, cualquier desempeño elevado sobre ese conjunto es en parte una propiedad del generador:
si el generador codificó una relación fuerte entre inasistencia temprana y abandono, un buen
clasificador la encontrará, y encontrarla no prueba nada sobre estudiantes reales. Esta es la
advertencia central de Dankar e Ibrahim (2021) y la razón por la cual Rankin et al. (2020)
insisten en contrastar contra datos reales antes de extraer conclusiones sustantivas.

Lo que sí quedará establecido es de otro orden y no es trivial: que existe un protocolo
especificado hasta el nivel de la semilla aleatoria, ejecutable por terceros, que produce
estimaciones con intervalos de confianza, que compara modelos con una prueba estadística adecuada
al diseño (Demšar, 2006), que audita disparidades por subgrupo (Gardner et al., 2019; Hardt et
al., 2016) y que verifica su propia consistencia contra un conjunto real de acceso público
(Realinho et al., 2022). Una institución que quiera implantar una alerta temprana necesita ese
instrumento antes que un número; y en la literatura aplicada revisada, el instrumento es
precisamente lo que rara vez se publica.

### 5.2 Diálogo con la literatura

[PENDIENTE DE COMPLETAR TRAS LOS RESULTADOS: contrastar el desempeño obtenido con los rangos
reportados por Berens et al. (2019), Kabathova y Drlik (2021), Chung y Lee (2019) y Delen (2010),
señalando explícitamente que la comparación es indicativa y no concluyente, porque las
definiciones de la variable objetivo, los puntos de corte temporal y las poblaciones difieren
entre estudios (Prenkaj et al., 2020).]

Con independencia de los valores que arrojen los experimentos, hay un punto de contraste que puede
anticiparse porque es de diseño y no de resultado. Buena parte de los desempeños altos publicados
en el campo se obtienen con información posterior a la semana de corte adoptada aquí —notas
finales, historial completo del semestre— y por lo tanto responden a una pregunta distinta. Berens
et al. (2019) documentan con claridad ese escalón: el desempeño mejora sustancialmente cuando
entran los resultados del primer semestre completo. Un modelo restringido a la semana 4 opera
necesariamente por debajo de esos valores, y presentarlo junto a ellos sin la aclaración
correspondiente sería una comparación engañosa. La utilidad de una alerta se mide por lo que
permite hacer a tiempo, no por el número que exhibe.

### 5.3 Implicaciones para el diseño de intervenciones

Si el modelo cumple su función, entrega a la institución una lista de estudiantes con probabilidad
elevada de abandono en la semana 4. A partir de ahí, la analítica cede el lugar a la decisión
institucional, y conviene señalar tres implicaciones.

La primera es que el umbral de decisión es una decisión política, no técnica. Fijarlo alto produce
listas cortas y manejables con muchos falsos negativos; fijarlo bajo produce listas largas que
saturan la capacidad de acompañamiento. La elección depende de cuántos casos puede atender
efectivamente la institución, dato que debe entrar al diseño del sistema y no descubrirse después.

La segunda es la obligación de actuar formulada por Prinsloo y Slade (2017): detectar riesgo y no
intervenir es peor que no detectarlo, porque la institución pasa a saber y no hacer. Un sistema
predictivo sin protocolo de intervención asociado y sin recursos asignados no es una mejora: es un
registro de omisiones.

La tercera es que la intervención debe diseñarse con los docentes, no notificarse a los docentes.
La crítica de Zawacki-Richter et al. (2019) —la ausencia de educadores en el diseño de las
aplicaciones de inteligencia artificial en educación superior— aplica de lleno a este tipo de
sistemas: la alerta llega a un docente que debe interpretarla y actuar, y si ese docente no
participó en definir qué significa la alerta, el sistema se convierte en ruido administrativo.

### 5.4 Riesgos éticos del despliegue

Cuatro riesgos deben declararse antes de cualquier implantación.

**Etiquetado y profecía autocumplida.** Clasificar a un estudiante como "en riesgo" puede alterar
el trato que recibe y, con ello, su propio desenlace. La etiqueta debe permanecer en el ámbito de
quien interviene, no circular como atributo del estudiante y no incorporarse a registros
académicos permanentes.

**Sesgo y equidad.** Un modelo entrenado sobre patrones históricos reproduce las desigualdades que
esos patrones contienen (Mehrabi et al., 2021; Baker y Hawn, 2022). Si el estrato socioeconómico
resulta ser una variable de peso, el sistema puede terminar señalando pobreza en lugar de riesgo
académico. Holstein y Doroudi (2021) muestran que este desenlace no es inevitable, pero sí es el
resultado por defecto cuando la equidad no se audita explícitamente; de ahí que la auditoría por
subgrupos sea obligatoria en el protocolo y no opcional.

**Transparencia frente al modelo opaco.** La objeción de Rudin (2019) es pertinente: si un modelo
interpretable alcanza un desempeño estadísticamente indistinguible del de un modelo de conjunto,
la elección razonable en un contexto de alto impacto es el interpretable. El protocolo está
diseñado para poder responder esa pregunta con datos, y la recomendación final del estudio quedará
condicionada a esa comparación. Las explicaciones locales (Ribeiro et al., 2016; Lundberg y Lee,
2017) mitigan, pero no sustituyen, la interpretabilidad de origen.

**Protección de datos.** En la fase con datos reales, el tratamiento queda sujeto a la Ley
Estatutaria 1581 de 2012 (Congreso de la República de Colombia, 2012): autorización del titular,
finalidad declarada, minimización y seguridad. El marco de la UNESCO (2023) y la política nacional
de transformación digital e inteligencia artificial (DNP, 2019) aportan los criterios
complementarios de gobernanza. La documentación mediante fichas de datos (Gebru et al., 2021) y
tarjetas de modelo (Mitchell et al., 2019), y el uso de generación sintética con garantías
formales de privacidad cuando haya que compartir datos derivados de registros reales (Jordon et
al., 2019; Patki et al., 2016; Xu et al., 2019), forman parte del mismo conjunto de salvaguardas.

### 5.5 Limitaciones del estudio

1. **La limitación principal es la naturaleza sintética de los datos.** Ninguna conclusión de este
   estudio se extiende a estudiantes reales. El desempeño observado sobre el conjunto sintético no
   es una estimación del desempeño que se obtendría en producción, y la evidencia disponible
   sugiere que la diferencia puede ser sustancial y dependiente del algoritmo (Rankin et al.,
   2020). **La validación con datos reales de la institución es trabajo futuro, y no un pendiente
   menor: es la condición sin la cual el sistema no debe desplegarse.**
2. **Validez poblacional.** El conjunto de validación externa es portugués (Realinho et al., 2022);
   la transferencia a la población colombiana no está establecida (Ocumpaugh et al., 2014).
3. **Definición de la variable objetivo.** Se adopta una definición operativa de abandono; otras
   definiciones producirían resultados distintos y no directamente comparables (Prenkaj et al.,
   2020).
4. **Ausencia de variables cualitativas.** Motivación, situación familiar y salud mental no están
   representadas, pese a su peso en los modelos teóricos del abandono (Tinto, 1993; Bean y
   Metzner, 1985; Spady, 1970).
5. **Sin evaluación de impacto.** El estudio evalúa capacidad predictiva, no efecto de la
   intervención. Que un modelo prediga bien no implica que la alerta reduzca la deserción; eso
   requiere un diseño con grupo de comparación que este trabajo no incluye. Los antecedentes de
   sistemas desplegados (Arnold y Pistilli, 2012; Kizilcec y Halawa, 2015) muestran que el efecto
   depende de la intervención, no del predictor.
6. **Tamaño y varianza.** Con 5.000 registros, las diferencias pequeñas entre modelos pueden no
   ser distinguibles del ruido de partición, razón por la cual se reportan intervalos de confianza
   y se emplea una prueba estadística de comparación múltiple (Varoquaux, 2018; Vabalas et al.,
   2019; Demšar, 2006). El tratamiento del desbalance por sobremuestreo sintético (Chawla et al.,
   2002) y la selección de hiperparámetros por búsqueda aleatoria (Bergstra y Bengio, 2012)
   introducen, además, fuentes adicionales de variabilidad que el protocolo controla pero no
   elimina. Estudios previos con enfoques alternativos para datos desbalanceados y de alta
   dimensión (Márquez-Vera et al., 2013; Dekker et al., 2009; Aulck et al., 2016) sugieren que
   estas decisiones pueden pesar tanto como la elección del algoritmo.

---

## 6. CONCLUSIONES

1. **Se dispone de un protocolo experimental reproducible y auditable** para la comparación de
   clasificadores supervisados en predicción temprana de deserción, especificado hasta el nivel de
   semillas, particiones, espacios de hiperparámetros y criterios de comparación estadística, con
   código, generador de datos y plan de análisis previo publicados con licencia abierta.

2. **La evaluación se realizó sobre un conjunto de datos sintético, y así se declara en el resumen,
   en la metodología y en las limitaciones.** Los resultados describen el comportamiento de los
   algoritmos sobre datos artificiales y no constituyen evidencia sobre ninguna cohorte real. Esta
   declaración no es una salvedad formal: define lo que el estudio puede y no puede sostener.

3. [PENDIENTE: conclusión sobre el desempeño comparativo de los cuatro modelos, redactada una vez
   se disponga de los resultados. Debe indicar explícitamente si las diferencias observadas son
   estadísticamente distinguibles y, en caso de no serlo, decirlo.]

4. [PENDIENTE: conclusión sobre la atribución de variables y sobre el resultado de la auditoría de
   equidad por subgrupos.]

5. **La restricción del punto de corte a la semana 4 impone un techo de desempeño que es
   deliberado.** La comparación con estudios que emplean información de semestre completo no es
   directa, y presentarla como tal sería incorrecto.

6. **El instrumento está listo; la evidencia no.** La contribución de este trabajo es haber
   construido y auditado el aparato experimental en condiciones controladas, de modo que la fase
   con datos institucionales reales pueda ejecutarse sin rediseño metodológico, con las
   autorizaciones y salvaguardas que esa fase exige.

### Trabajo futuro

La continuación inmediata es la replicación del protocolo, sin modificaciones, sobre registros
académicos reales y anonimizados de la institución, previa autorización de tratamiento de datos
conforme a la Ley Estatutaria 1581 de 2012 y aval del Comité de Ética de la Investigación
Institucional. En segundo lugar, la incorporación de variables de actividad efectivamente
disponibles en la plataforma institucional de aula virtual, cuya exportabilidad debe verificarse
antes de comprometerlas en un diseño. En tercer lugar, y solo después de las dos anteriores, la
evaluación de impacto de la intervención mediante un diseño con grupo de comparación, que es la
única forma de establecer si la alerta temprana reduce efectivamente la deserción.

---

## AGRADECIMIENTOS Y DECLARACIONES

**Financiación.** Este trabajo no recibió financiación.

**Contribución de los autores.** [PENDIENTE: declarar según taxonomía CRediT una vez confirmada la
participación efectiva de cada coautor.]

**Conflicto de intereses.** Los autores declaran no tener conflictos de intereses.

**Disponibilidad de datos y código.** [PENDIENTE: URL del repositorio público e identificador
persistente del conjunto de datos sintético y su ficha de datos.]

**Uso de inteligencia artificial.** Declarado en la sección 3.12.

**Datos personales.** Este manuscrito no contiene datos de identificación personal de estudiantes.
El conjunto de datos empleado es sintético y no deriva de registros de personas reales.

---

## REFERENCIAS

*Nota sobre los identificadores digitales: las entradas se presentan verificadas en cuanto a
autoría, año, título y fuente. Los DOI y URL se incorporarán en la versión de sometimiento tras su
comprobación individual en Crossref, conforme al procedimiento descrito en las notas de envío. No
se transcribe ningún DOI que no haya sido verificado.*

Arnold, K. E., y Pistilli, M. D. (2012). Course Signals at Purdue: Using learning analytics to
increase student success. En *Proceedings of the 2nd International Conference on Learning
Analytics and Knowledge (LAK '12)* (pp. 267–270). Association for Computing Machinery.

Aulck, L., Velagapudi, N., Blumenstock, J., y West, J. (2016). *Predicting student dropout in
higher education* [Preprint]. arXiv:1606.06364.

Baker, R. S., y Hawn, A. (2022). Algorithmic bias in education. *International Journal of
Artificial Intelligence in Education, 32*(4), 1052–1092.

Bean, J. P., y Metzner, B. S. (1985). A conceptual model of nontraditional undergraduate student
attrition. *Review of Educational Research, 55*(4), 485–540.

Berens, J., Schneider, K., Görtz, S., Oster, S., y Burghoff, J. (2019). Early detection of students
at risk: Predicting student dropouts using administrative student data from German universities
and machine learning methods. *Journal of Educational Data Mining, 11*(3), 1–41.

Bergstra, J., y Bengio, Y. (2012). Random search for hyper-parameter optimization. *Journal of
Machine Learning Research, 13*, 281–305.

Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32.

Chawla, N. V., Bowyer, K. W., Hall, L. O., y Kegelmeyer, W. P. (2002). SMOTE: Synthetic minority
over-sampling technique. *Journal of Artificial Intelligence Research, 16*, 321–357.

Chen, T., y Guestrin, C. (2016). XGBoost: A scalable tree boosting system. En *Proceedings of the
22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794).
Association for Computing Machinery.

Chung, J. Y., y Lee, S. (2019). Dropout early warning systems for high school students using
machine learning. *Children and Youth Services Review, 96*, 346–353.

Congreso de la República de Colombia. (2012). *Ley Estatutaria 1581 de 2012, por la cual se dictan
disposiciones generales para la protección de datos personales*. Diario Oficial.

Dankar, F. K., e Ibrahim, M. (2021). Fake it till you make it: Guidelines for effective synthetic
data generation. *Applied Sciences, 11*(5), 2158.

Davis, J., y Goadrich, M. (2006). The relationship between Precision-Recall and ROC curves. En
*Proceedings of the 23rd International Conference on Machine Learning (ICML '06)* (pp. 233–240).
Association for Computing Machinery.

Dekker, G. W., Pechenizkiy, M., y Vleeshouwers, J. M. (2009). Predicting students drop out: A case
study. En *Proceedings of the 2nd International Conference on Educational Data Mining (EDM 2009)*
(pp. 41–50).

Delen, D. (2010). A comparative analysis of machine learning techniques for student retention
management. *Decision Support Systems, 49*(4), 498–506.

Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *Journal of
Machine Learning Research, 7*, 1–30.

Departamento Nacional de Planeación. (2019). *Documento CONPES 3975: Política nacional para la
transformación digital e inteligencia artificial*. DNP.

Efron, B., y Tibshirani, R. J. (1993). *An introduction to the bootstrap*. Chapman & Hall/CRC.

Gardner, J., Brooks, C., y Baker, R. (2019). Evaluating the fairness of predictive student models
through slicing analysis. En *Proceedings of the 9th International Conference on Learning
Analytics & Knowledge (LAK '19)* (pp. 225–234). Association for Computing Machinery.

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., y Crawford,
K. (2021). Datasheets for datasets. *Communications of the ACM, 64*(12), 86–92.

Hardt, M., Price, E., y Srebro, N. (2016). Equality of opportunity in supervised learning. En
*Advances in Neural Information Processing Systems* (Vol. 29).

Holstein, K., y Doroudi, S. (2021). *Equity and artificial intelligence in education: Will "AIEd"
amplify or alleviate inequities in education?* [Preprint]. arXiv:2104.12920.

Jordon, J., Yoon, J., y van der Schaar, M. (2019). PATE-GAN: Generating synthetic data with
differential privacy guarantees. En *International Conference on Learning Representations (ICLR
2019)*.

Kabathova, J., y Drlik, M. (2021). Towards predicting student's dropout in university courses using
different machine learning techniques. *Applied Sciences, 11*(7), 3130.

Kizilcec, R. F., y Halawa, S. (2015). Attrition and achievement gaps in online learning. En
*Proceedings of the Second ACM Conference on Learning @ Scale (L@S '15)* (pp. 57–66). Association
for Computing Machinery.

Lundberg, S. M., y Lee, S.-I. (2017). A unified approach to interpreting model predictions. En
*Advances in Neural Information Processing Systems* (Vol. 30).

Márquez-Vera, C., Cano, A., Romero, C., y Ventura, S. (2013). Predicting student failure at school
using genetic programming and different data mining approaches with high dimensional and
imbalanced data. *Applied Intelligence, 38*(3), 315–330.

Martins, M. V., Tolledo, D., Machado, J., Baptista, L. M. T., y Realinho, V. (2021). Early
prediction of student's performance in higher education: A case study. En *Trends and Applications
in Information Systems and Technologies (WorldCIST 2021)* (Vol. 1365, pp. 166–175). Springer.

Mehrabi, N., Morstatter, F., Saxena, N., Lerman, K., y Galstyan, A. (2021). A survey on bias and
fairness in machine learning. *ACM Computing Surveys, 54*(6), Artículo 115.

Ministerio de Educación Nacional. (2009). *Deserción estudiantil en la educación superior
colombiana: Metodología de seguimiento, diagnóstico y elementos para su prevención*. MEN.

Ministerio de Educación Nacional. (s.f.). *Sistema para la Prevención de la Deserción de la
Educación Superior (SPADIES)*. MEN. [REFERENCIA POR VERIFICAR: consignar el año de la versión
consultada y la URL vigente del sistema en el momento del sometimiento.]

Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji,
I. D., y Gebru, T. (2019). Model cards for model reporting. En *Proceedings of the Conference on
Fairness, Accountability, and Transparency* (pp. 220–229). Association for Computing Machinery.

Ocumpaugh, J., Baker, R., Gowda, S., Heffernan, N., y Heffernan, C. (2014). Population validity for
educational data mining models: A case study in affect detection. *British Journal of Educational
Technology, 45*(3), 487–501.

Patki, N., Wedge, R., y Veeramachaneni, K. (2016). The Synthetic Data Vault. En *2016 IEEE
International Conference on Data Science and Advanced Analytics (DSAA)* (pp. 399–410). IEEE.

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M.,
Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M.,
Perrot, M., y Duchesnay, É. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine
Learning Research, 12*, 2825–2830.

Prenkaj, B., Velardi, P., Stilo, G., Distante, D., y Faralli, S. (2020). A survey of machine
learning approaches for student dropout prediction in online courses. *ACM Computing Surveys,
53*(3), Artículo 57.

Prinsloo, P., y Slade, S. (2017). An elephant in the learning analytics room: The obligation to
act. En *Proceedings of the Seventh International Learning Analytics & Knowledge Conference (LAK
'17)* (pp. 46–55). Association for Computing Machinery.

Rankin, D., Black, M., Bond, R., Wallace, J., Mulvenna, M., y Epelde, G. (2020). Reliability of
supervised machine learning using synthetic data in health care: Model to preserve privacy for
data sharing. *JMIR Medical Informatics, 8*(7), e18910.

Realinho, V., Machado, J., Baptista, L., y Martins, M. V. (2022). Predicting student dropout and
academic success. *Data, 7*(11), 146.

Ribeiro, M. T., Singh, S., y Guestrin, C. (2016). "Why should I trust you?": Explaining the
predictions of any classifier. En *Proceedings of the 22nd ACM SIGKDD International Conference on
Knowledge Discovery and Data Mining* (pp. 1135–1144). Association for Computing Machinery.

Romero, C., y Ventura, S. (2020). Educational data mining and learning analytics: An updated
survey. *WIREs Data Mining and Knowledge Discovery, 10*(3), e1355.

Rudin, C. (2019). Stop explaining black box machine learning models for high stakes decisions and
use interpretable models instead. *Nature Machine Intelligence, 1*(5), 206–215.

Saito, T., y Rehmsmeier, M. (2015). The precision-recall plot is more informative than the ROC plot
when evaluating binary classifiers on imbalanced datasets. *PLoS ONE, 10*(3), e0118432.

Siemens, G. (2013). Learning analytics: The emergence of a discipline. *American Behavioral
Scientist, 57*(10), 1380–1400.

Slade, S., y Prinsloo, P. (2013). Learning analytics: Ethical issues and dilemmas. *American
Behavioral Scientist, 57*(10), 1510–1529.

Spady, W. G. (1970). Dropouts from higher education: An interdisciplinary review and synthesis.
*Interchange, 1*(1), 64–85.

Tinto, V. (1993). *Leaving college: Rethinking the causes and cures of student attrition* (2.ª
ed.). University of Chicago Press.

UNESCO. (2023). *Guidance for generative AI in education and research*. UNESCO.

Vabalas, A., Gowen, E., Poliakoff, E., y Casson, A. J. (2019). Machine learning algorithm
validation with a limited sample size. *PLOS ONE, 14*(11), e0224365.

Varoquaux, G. (2018). Cross-validation failure: Small sample sizes lead to large error bars.
*NeuroImage, 180*, 68–77.

Xu, L., Skoularidou, M., Cuesta-Infante, A., y Veeramachaneni, K. (2019). Modeling tabular data
using conditional GAN. En *Advances in Neural Information Processing Systems* (Vol. 32).

Zawacki-Richter, O., Marín, V. I., Bond, M., y Gouverneur, F. (2019). Systematic review of research
on artificial intelligence applications in higher education – Where are the educators?
*International Journal of Educational Technology in Higher Education, 16*, Artículo 39.
