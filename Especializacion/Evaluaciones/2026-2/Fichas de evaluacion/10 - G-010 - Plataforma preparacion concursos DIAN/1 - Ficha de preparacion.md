# 26ET2-G-010 — Desarrollo de un prototipo de plataforma digital para fortalecer la preparación de aspirantes a concursos públicos de la DIAN en Colombia

**Sustentación:** miércoles 19 de agosto de 2026 · 6:00 p. m. – 6:20 p. m. · **Mi rol:** Jurado 2
**Integrantes:** Jose David Puello Avilez (Jose.Puello@cun.edu.co), Jenny Viviana Rivas Rivas (jenny.rivas@cun.edu.co)
**Línea:** Gestión y Tecnologías
**Documentos leídos:** `ACA 3 - Proyecto Jenny Rivas_ José Puello.pdf` (78 páginas). **La carpeta del grupo no contiene presentación** (un único archivo; verificado el 15/08/2026 y de nuevo el 19/08/2026, el día de la sustentación). Toda esta ficha se apoya en el documento; no hay diapositivas que comparar, y así lo dice la §5.

---

## 1. Resumen para leer en 5 minutos

Problema: los aspirantes a los concursos de méritos de la DIAN se preparan sin herramientas digitales accesibles que integren simulacros, autoevaluación y retroalimentación, lo que castiga a quienes no pueden pagar cursos y debilita el principio del mérito (p. 14). Pregunta de investigación: «¿Cómo influye una plataforma de entrenamiento interactivo en el rendimiento de los aspirantes en las pruebas de conocimientos de la DIAN?» (p. 14).

Objetivo general (p. 15): «Desarrollar e implementar un prototipo de plataforma digital basado en tecnologías No-Code y analítica de aprendizaje, orientado al diagnóstico y fortalecimiento del rendimiento técnico-normativo de los aspirantes en las pruebas de selección de la DIAN». **Ojo: no es el objetivo que transcribió la Dirección en el cronograma** (allí se habla de simulacros, gamificación y análisis estadístico, y del verbo «evaluar»).

Método: estudio descriptivo de alcance aplicado con componente exploratorio (p. 28), enfoque mixto (p. 28), diseño **no experimental – transeccional** (p. 30), seis fases (diagnóstico, diseño, desarrollo, implementación, validación, interpretación) (p. 31). Unidad de análisis: aspirantes de niveles técnico y profesional (p. 31); muestreo **por conveniencia** (p. 32); **el documento no declara tamaño de muestra en la sección de participantes** (buscado en pp. 31-32).

Producto: un prototipo de plataforma con módulos por los tres bloques del manual de funciones de la DIAN —básicos, funcionales y comportamentales (p. 45)—, simulacros tipo juicio situacional y tablero de indicadores. El documento describe **dos arquitecturas distintas**: la comprometida en objetivos, Glide Apps/AppSheet + Google Sheets + Looker Studio (pp. 15-16, 26-27), y la efectivamente reportada, Microsoft Power Pages + Forms + Excel + Power BI + OneDrive (pp. 38, 50-51). Hay 32 figuras incrustadas como imágenes —15 ilustraciones y 17 gráficos— entre las pp. 31 y 73, incluido el tablero (p. 41) y capturas de módulos (pp. 57-58); **no hay URL, repositorio ni QR del prototipo desplegado** (búsqueda de «http», «enlace», «repositorio» en las 78 páginas: solo aparece en las referencias, pp. 76-78).

Resultados: se reportan porcentajes de aceptación de 90 % a 100 % en todos los indicadores, atribuidos a una encuesta a **100 funcionarios de la DIAN** (pp. 52, 59, 65) —aunque el mismo objetivo 4 se reporta antes con **10 personas** (p. 42)—; el 100 % de aprobación en identificación de fortalezas se califica como el punto más fuerte «según la simulación» (p. 43). Limitaciones declaradas, honestas y bien escritas: especificidad DIAN, incumplimiento de WCAG 2.1, naturaleza de prototipo, dependencia de la CNSC y acceso tecnológico (pp. 19-21). Conclusiones (p. 74) y recomendaciones de IA adaptativa (p. 75).

## 2. Coherencia título → objetivo → resultados

El documento contiene **dos juegos de objetivos específicos que no coinciden entre sí**: el del capítulo de objetivos (p. 15) y el que estructura el desarrollo y los resultados (pp. 36-73, allí llamados «Requisito 1» a «Requisito 4»). Evalúo el segundo, que es el que el trabajo efectivamente responde, y dejo constancia del primero.

| Objetivo específico (pp. 36-42, 45-73) | ¿Se cumplió? | Evidencia | Qué falta |
|---|---|---|---|
| 1. Analizar los manuales de funciones y competencias de la carrera específica para definir los módulos | **Sí** | Marco normativo TACI (pp. 36-37); clasificación en conocimientos básicos, funcionales y comportamentales (p. 45); capturas de los manuales Facilitador, Analista, Gestor e Inspector (pp. 46-49) | El «mapa de calor de errores por temática» y el «% de desaciertos» que la Tabla 1 (pp. 15-16) fijaba como entregable e indicador del diagnóstico |
| 2. Diseñar los módulos con criterios de usabilidad, accesibilidad y gamificación | **Parcial** | Descripción de heurísticas de Nielsen y diseño responsivo (p. 39); micro-recompensas visuales y sonoras (p. 40); capturas de módulos (pp. 57-58); encuesta de usabilidad (pp. 53-56) | La accesibilidad se afirma «total» (pp. 39, 43) y la limitación del propio documento dice que **no** cumple WCAG 2.1 (pp. 20-21). El texto está en futuro («se diseñarán», p. 39), lo que deja en duda qué se construyó |
| 3. Implementar el prototipo con herramientas de análisis estadístico para seguimiento de progreso | **Sí, en su versión descriptiva** | Tablero con KPIs y evolución temporal (p. 41, Ilustración 3); descripción del rol de Power BI (p. 51); resultados de 5 preguntas (pp. 60-64) | «Análisis estadístico» se agota en visualización descriptiva; no hay prueba estadística alguna. Falta la salida real de datos (base, número de intentos, fechas) |
| 4. Validar el impacto mediante pruebas de usuario y pilotos controlados | **No, como impacto** | 8 preguntas de percepción a 100 funcionarios (pp. 65-73); antes, 3 preguntas Likert a 10 personas (pp. 42-43) | Todo es autorreporte. No hay medición de rendimiento antes/después, pese a que la metodología la anuncia (p. 28). La **escala SUS** prometida como indicador (>68/100) en pp. 15-16 y 28 **no se aplica en ninguna página**. La población validadora son *funcionarios*, no los *aspirantes* declarados como unidad de análisis (p. 31) |

**Techo del verbo:** el objetivo general dice «desarrollar e implementar» (p. 15) y eso sí está sustentado con figuras; la Dirección transcribió «desarrollar y evaluar», y es la parte de «evaluar» la que queda débil. El título («fortalecer la preparación») promete un efecto que el diseño transeccional (p. 30) no puede demostrar.

## 3. Fortalezas verificables

1. **Anclaje normativo real y poco frecuente.** El contenido no es genérico: se apoya en el Decreto Ley 714 de 2020 y el umbral aprobatorio 65/100 de la DIAN (pp. 25-26), el Estatuto Tributario y el Decreto 1165 de 2019 (p. 37), y en los manuales de funciones por empleo (pp. 46-49). Ese trabajo de mapeo existe y se ve.
2. **Limitaciones honestas y específicas.** Cinco limitaciones bien argumentadas, incluida la admisión de que el prototipo no cumple WCAG 2.1 y no soporta concurrencia masiva (pp. 20-21). Es exactamente lo que se espera de un trabajo profesionalizante que no se sobrevende… en ese capítulo.
3. **Arquitectura pensada por capas.** Captura, lógica, analítica y retroalimentación, con justificación de por qué No-Code frente a desarrollo tradicional (pp. 26-28). Hay criterio técnico, no solo herramientas nombradas.
4. **Producto con evidencia gráfica.** 32 figuras incrustadas entre las pp. 31 y 73: tablero (p. 41), diagrama de flujo (p. 52), módulos de competencias (pp. 57-58). No es un proyecto sin nada que mostrar.
5. **Documento completo y firmado.** Estructura institucional entera, declaraciones de originalidad y exoneración con firma escaneada de los dos autores (pp. 10-11), cronograma de 24 semanas por fases (pp. 33-34) y fuentes de financiación (pp. 35-36).

## 4. OBSERVACIONES DEL DOCUMENTO — debilidades y huecos (con página)

1. **Dos juegos de objetivos específicos en el mismo documento.** Los de p. 15 (Google Forms, Glide/AppSheet, Looker Studio, SUS) no son los que responde el cuerpo (pp. 36-42, 45-73). Es el hallazgo más costoso: rompe la trazabilidad objetivo → resultado que la rúbrica llama coherencia metodológica.
2. **Dos arquitecturas tecnológicas.** Google (pp. 15-16, 26-28) frente a Microsoft Power Platform (pp. 38, 43, 50-51); y en la mención de recursos vuelve a aparecer «Power BI o entornos de Python» (p. 36). El documento nunca explica el cambio.
3. **Muestra contradictoria: 10 frente a 100.** El objetivo 4 se valida «con un grupo de 10 personas… mediante la escala de Likert» (p. 42) y el capítulo de resultados lo valida con «100 funcionarios de la DIAN» (pp. 52, 59, 65). Además la sección de participantes no declara ningún tamaño (pp. 31-32).
4. **La población validadora no es la población objetivo.** Se declara «ciudadanos aspirantes» (p. 19) y «aspirantes de niveles técnico y profesional» (p. 31); se encuesta a *funcionarios* de la DIAN (pp. 52, 59, 65), que ya superaron el concurso.
5. **La palabra «simulación» sobre los propios resultados.** «Es el punto más fuerte del prototipo **según la simulación**, con un 100 % de respuestas positivas» (p. 43). Junto a resultados de 90 %-100 % con 0 % de desacuerdo en casi todas las preguntas (pp. 53-56, 60-64, 66-73), obliga a preguntar por el origen del dato antes de darle valor.
6. **Sin instrumento, sin ficha técnica y sin anexos.** No hay cuestionario anexo, fecha de aplicación, medio, ni autorización institucional para encuestar a 100 funcionarios de una entidad pública (buscado en todo el documento; no hay capítulo de anexos ni de consideraciones éticas).
7. **El indicador que el propio grupo fijó no se reporta.** SUS > 68/100 (pp. 15-16, 28) no aparece en ningún resultado.
8. **Sin línea base.** El diagnóstico del objetivo 1 de p. 15 (base de datos inicial, mapa de calor) no existe en el documento, y sin él la pregunta de investigación sobre «rendimiento» queda sin cómo responderse; la metodología, en cambio, promete «medir el rendimiento inicial y final» (p. 28).
9. **Sin enlace al prototipo.** Ninguna URL, QR ni repositorio (pp. 1-78; los únicos enlaces son bibliográficos, pp. 76-78). Para un producto No-Code desplegado en web esto es fácil de subsanar y hoy no está.
10. **Resumen en tiempo futuro.** «Como resultados esperados, se proyecta…» (p. 8) y el Abstract igual (p. 9), en un informe final que ya tiene resultados. El capítulo de metodología también está en futuro (pp. 31-33).
11. **Antecedentes como compilación, no como análisis.** Los antecedentes son tres citas largas textuales seguidas, sin síntesis propia (pp. 22-23), y arrastran un artefacto de copiado («la interacción entre usuarios en 36 el foro», p. 22).
12. **Referencias: apoyo conceptual débil.** De 22 entradas (pp. 76-78), varias son glosarios o blogs comerciales (Hostgator, IEBSchool, Cognizant, pensemos.com, blog Konrad Lorenz) usados para definir conceptos centrales del marco (pp. 24-25); arbitradas hay pocas (Basantes et al., 2017; Disla, 2025; Pradas, 2017). No es motivo para castigar el número, sí para preguntar por el criterio de selección.
13. **Sin declaración de similitud.** No hay mención de Turnitin ni porcentaje de similitud en ninguna página (buscado en las 78).
14. **Forma.** Numeración de capítulos duplicada (7 y 8 aparecen dos veces, pp. 26-28 y 36-45; el 9 también, pp. 36 y 45); «9.1» no existe y «9.3» está dos veces (pp. 38, 41); «Tabla 1» tres veces (pp. 15, 33, 37) e «Ilustración 4» dos (pp. 39, 43), con la 3 después de la 4 (p. 41); frase truncada «mediante pruebas de usuario y.» (p. 74); primera persona del singular «me base en» en un trabajo de dos autores (p. 40); erratas en enunciados de encuesta («comprar su puntaje», p. 63; «Identificación de Debilidad#», p. 61; «Dahboard», p. 62) y «Se realizado una encuesta» (p. 52).

## 5. OBSERVACIONES DE LAS DIAPOSITIVAS — no hay mazo que comparar

**No hay presentación entregada.** La carpeta `26ET2-G-010` contiene **un solo archivo**, `ACA 3 - Proyecto Jenny Rivas_ José Puello.pdf` (4,86 MB, modificado el 10/08/2026). Verificado dos veces: el **15/08/2026** y de nuevo el **19/08/2026**, el día de la sustentación. Así que esta sección no tiene contenido de origen —no hay diapositivas que cotejar contra el documento— y en su lugar fija **cómo se procede cuando el mazo aparece por primera vez en la pantalla**.

1. **Lo que proyecten se ve por primera vez en sala.** No hubo posibilidad de revisarlo, así que no puede sostener ninguna afirmación de la ficha ni ninguna casilla del formulario: **las cinco casillas de la §8.1 se responden con el documento** y así queda dicho en su encabezado. Si una diapositiva contradice al documento, el reparo se anota por la frase que se oiga, no por una página que nadie puede citar después.
2. **Regla de registro, porque no queda copia.** De lo que se proyecte no habrá archivo que volver a mirar al llenar el `4 - Evaluacion.md`: lo que no quede escrito a mano en la §A y en el bloque de respuestas de la hoja **no va a existir en ninguna parte**. Cifra que se oiga, cifra que se escribe con su rótulo tal como lo digan.
3. **Lo más probable es que el mazo sean las figuras del documento.** Hay 32 imágenes incrustadas entre las pp. 31 y 73 —15 ilustraciones y 17 gráficos—: el tablero (Ilustración 3, p. 41), el diagrama de flujo (p. 52), los módulos de competencias (pp. 57-58) y las 17 gráficas de encuesta (pp. 53-56, 60-64, 66-73). Si lo que se proyecta son esas mismas imágenes, **cada reparo de la §4 sigue vigente tal cual** y se puede citar por página con normalidad.
4. **Si proyectan algo que el documento no trae** —una URL viva, un puntaje, un dato de campo nuevo, otra arquitectura—, **eso es la respuesta a mis preguntas, no un hallazgo nuevo:** las tres prioritarias de la §6 preguntan justamente por lo que falta en las 78 páginas. Se recibe como respuesta y se anota literal.
5. **La ausencia del mazo no baja la nota por sí sola.** No es un criterio del formulario ni de los cuatro del acta. Lo que sí queda dicho, y está en la §8.1: si sustentan con diapositivas que los jurados no pudieron revisar, **califico contra el documento y lo digo en voz alta**. Y va a la Dirección como observación administrativa (§9, ítem 1), no como reparo académico.

### Qué mirar en pantalla mientras exponen

- **La barra de direcciones**, en cuanto aparezca cualquier captura de la plataforma. La del documento (p. 57) dice `dian.colombia.noulo`, que no resuelve. Si en pantalla hay una URL distinta y viva, la pregunta 1 está contestada antes de hacerla.
- **De qué color es el stack.** Si lo proyectado es Power Pages / Microsoft Forms / Power BI, la reserva 4 se convierte en «¿por qué los objetivos del folio 15 siguen escritos con Glide y Looker Studio?». Si es Google, el hueco se invierte y hay que preguntar por los resultados de las pp. 50-51.
- **El tablero, si lo proyectan.** Dos cosas concretas de la Ilustración 3 (p. 41): las **dos series rotuladas «Simulacro 2»** y el eje de meses **Ago-Sep-Oct-Sep-Oct**. Condicional atómico: si no sale en pantalla, no se pregunta.
- **La columna «Posición Actual 112 h»** del tablero: si se proyecta legible, es el momento de la reserva 5.
- **Si aparece una gráfica de encuesta con un rótulo de n.** El documento dice 10 en el folio 42 y 100 en los folios 52, 59 y 65. El número que se proyecte es el que se les cita en la pregunta 2.
- **Si aparece la palabra «simulación» junto a un resultado** —como en la p. 43—: anotarla textual. Es la puerta honesta de salida y conviene ofrecérsela, no cerrarla.

---

## 6. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. Página 57: la barra de direcciones dice “dian.colombia.noulo”. Dígannos ahora, en voz alta y letra por letra, la URL con la que un aspirante entra hoy al prototipo. Si no hay URL, díganlo con esas palabras: “la plataforma no está desplegada”.**
- *Sale de:* solo del **documento** —la captura del folio 57 con `dian.colombia.noulo`, la ausencia de cualquier URL, QR o repositorio en las 78 páginas (los únicos enlaces son bibliográficos, pp. 76-78) y el segundo párrafo del Objetivo específico 2, folio 38—. **Del mazo, nada: no hay mazo** (§5). Si en pantalla aparece una dirección viva, esta pregunta queda contestada antes de hacerla.
- *Por qué:* es la pregunta que decide si el producto existe, y es la primera porque de su respuesta dependen las otras dos. La captura de la p. 57 muestra un dominio que no resuelve, el documento no trae enlace en ninguna de sus 78 páginas (pp. 1-78) y el segundo párrafo del Objetivo específico 2 (folio 38) describe el desarrollo en Power Pages sin decir dónde quedó publicado. Pedir la dirección letra por letra cierra las tres salidas habituales: «está en la nube», «se lo mostramos después», «está en el computador de la oficina».
- *Qué la resuelve:* dictan una URL y se abre ahí mismo; o comparten pantalla y navegan un simulacro; o dicen sin rodeos que no está desplegada y que corre en local, que es un límite legítimo cuando se declara con precisión.
- *Qué la agrava:* describir la plataforma con las palabras de la exposición sin poder decir dónde vive; o sostener que está publicada y no poder dictar la dirección.

**2. El Gráfico 11 de la página 67 pregunta por “su confianza para presentar el examen real”. Un funcionario de carrera ya lo presentó. ¿Los 100 que respondieron eran funcionarios o aspirantes? Una sola palabra.**
- *Sale de:* solo del **documento** —Gráfico 11 del folio 67, unidad de análisis del folio 31, «100 funcionarios» de los folios 52, 59 y 65, y las 10 personas del folio 42—. **Del mazo, nada** (§5). Si proyectan una gráfica de encuesta con un `n` rotulado, ese es el número que se les cita.
- *Por qué:* la unidad de análisis declarada son *aspirantes* (p. 31), los encuestados se nombran *funcionarios de la DIAN* (pp. 52, 59, 65) y el objetivo 4 habla de 10 personas (p. 42); la sección de participantes no fija tamaño de muestra (pp. 31-32). El Gráfico 11 vuelve incompatibles las dos lecturas: quien ya es funcionario de carrera no necesita confianza para presentar el examen que ya presentó. Pedir una sola palabra impide que la respuesta se vaya a «lo validamos con el equipo».
- *Qué la resuelve:* decir «aspirantes» y sostener cómo se les contactó; decir «funcionarios» y reconocer entonces que la población validadora no es la declarada; o reconocer que los gráficos son un ejercicio ilustrativo y no datos de campo, que en este nivel es una respuesta honesta y suma.
- *Qué la agrava:* mantener las dos cifras y las dos poblaciones como si fueran compatibles, o afirmar 100 funcionarios reales de una entidad pública sin poder decir cuándo, cómo ni con qué autorización se les encuestó.

**3. Denos dos números del Excel de respuestas: el puntaje del primer simulacro y el del último simulacro de una misma persona. No de la Ilustración 3, del archivo. Si el Excel no guarda dos intentos por persona, díganlo.**
- *Sale de:* solo del **documento** —pregunta de investigación del folio 14, «rendimiento inicial y final» del folio 28, diseño transeccional del folio 30, cierre del Objetivo específico 4 en el folio 44 y las 17 gráficas de percepción de los folios 53-73—. **Del mazo, nada** (§5); pero si proyectan el archivo de respuestas o el tablero con datos, ahí está la respuesta y hay que mirarla antes de preguntar.
- *Por qué:* la pregunta de investigación indaga por el *rendimiento* (p. 14) y la metodología anuncia medir «rendimiento inicial y final» (p. 28), pero el diseño es no experimental transeccional (p. 30) y todo lo reportado es percepción (pp. 53-73). Dos puntajes de una misma persona en dos momentos son el único artefacto que zanja la discusión, y el cierre del Objetivo específico 4 (folio 44) no los trae. **Va después de la 1:** si la plataforma no está desplegada, el archivo de respuestas tampoco existe y la respuesta llega sola.
- *Qué la resuelve:* dos puntajes de un mismo usuario, aunque sea de una sola persona y aunque los digan de memoria; o decir con precisión «medimos percepción, no rendimiento; el efecto sobre el puntaje queda como trabajo futuro», con lo cual la conclusión de la p. 74 se reformula sola.
- *Qué la agrava:* insistir en que el rendimiento mejoró porque los usuarios dicen que mejoró, presentar el 100 % de aprobación como prueba de eficacia, o remitir el dato a un anexo que el documento no trae.

### Banco de reserva

#### Del documento

4. Las dos arquitecturas: los objetivos específicos comprometen Glide Apps/AppSheet, Google Sheets y Looker Studio (pp. 15-16), la arquitectura por capas los repite (pp. 26-27) y la mención de recursos añade «Power BI o entornos de Python» (p. 36), pero el segundo párrafo del Objetivo específico 2 (folio 38) y los resultados describen Power Pages, Microsoft Forms, Excel y Power BI (pp. 50-51): ¿cuál de las dos construyeron y por qué el documento no registra el cambio? *(Al citarlo en voz alta hay que nombrar el objetivo específico, nunca el número de apartado: el «9.3» titula dos apartados distintos, folios 38 y 41.)*
5. En el tablero del prototipo aparece una columna «Posición Actual 112 h»: ¿qué mide esa cifra, sobre qué universo de aspirantes y con qué periodicidad se actualiza? *(La cifra está en la captura del tablero; conviene confirmar la página antes de usarla en sala.)*
6. La limitación de la p. 20 dice que el prototipo no cumple WCAG 2.1 y las pp. 39 y 43 afirman accesibilidad «total» y «plenamente operable»: ¿qué criterio de accesibilidad sí cumplieron y cuál no?
7. La p. 15 fija como indicador un puntaje SUS mayor a 68/100: ¿aplicaron la escala SUS? Si no, ¿por qué la reemplazaron por Likert y qué se pierde con ese cambio?
8. El objetivo 1 de la p. 15 comprometía una base de datos inicial y un mapa de calor de errores por temática: ¿existe ese diagnóstico y qué mostró?
9. ¿Con qué banco de preguntas funciona el simulacro: cuántos ítems, quién los redactó y cómo validaron que sean equivalentes a los juicios situacionales de la CNSC (afirmación de «simulador fiel», p. 52)?
10. Los ejes del marco normativo son tres (tributario, aduanero-cambiario, comportamental, p. 25), en resultados son cuatro —tributario, aduanero, cambiario e internacional, «TACI» (pp. 36, 41)— y los módulos son tres bloques del manual (p. 45): ¿cuál es la estructura definitiva?
11. El presupuesto está solo como imagen (p. 35) y valora el tiempo del equipo «a precio de mercado»: ¿cuánto costaría sostener la plataforma un año con usuarios reales, dado que el stack es de capa gratuita?
12. La p. 35 menciona a un tercer integrante («Puello, Rivas y Villacob») y atribuye la dirección a la Dra. María Fernanda Rivera, mientras la portada (p. 2) registra al Ing. Luis Alfredo Blanquiceth Benavides: ¿cuál es la conformación real del equipo y su director? *(Pregunta administrativa: mejor a la Dirección que en sala.)*
13. Recomiendan IA adaptativa y multi-entidad (p. 75): ¿qué del diseño actual habría que rehacer para que el sistema lea manuales de funciones de otra entidad, dado que ustedes mismos declararon esa limitación (p. 20)?

#### De las diapositivas

**Ninguna.** No hay mazo entregado (§5), así que no hay preguntas escritas de antemano contra la pantalla. Lo que dependa de lo que proyecten está en la lista «Qué mirar en pantalla» de la §5 y en los condicionales de la §7, que es donde se decide en caliente.

## 7. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si no mostraron la plataforma funcionando** (ni URL, ni video, ni navegación en vivo) → «¿podemos ver el prototipo ahora, aunque sea la pantalla principal y un simulacro?». Es el único modo de cerrar el criterio de que el producto existe, porque el documento no trae enlace (pp. 1-78).
- **Si mostraron la plataforma y era Power Pages/Power BI** → dar por resuelta la pregunta 1 y pasar a la reserva 4: «¿por qué los objetivos de la p. 15 siguen escritos con herramientas de Google?».
- **Si presentan la Ilustración 3 (p. 41) como la evolución de los simulacros** → «en esa gráfica hay dos series rotuladas “Simulacro 2” y el eje de meses va Ago-Sep-Oct-Sep-Oct: ¿qué mide cada serie y en qué orden van los meses?». Condicional atómico: si no la proyectan, no se pregunta.
- **Si dijeron «validamos con 100 funcionarios»** → «¿en qué fechas, por qué medio y con qué autorización de la entidad?». Si no hay respuesta concreta, no insistir en público: anotarlo para el acta y la nota.
- **Si reconocieron que los datos de las encuestas son ilustrativos o simulados** → tratarlo como fortaleza de honestidad y preguntar en cambio: «¿qué haría falta para una validación real y cuánto tomaría?». No convertirlo en un juicio de integridad en sala.
- **Si presentaron el 100 % y el 98 % como prueba de eficacia sin matizar** → «¿qué explicación tienen para que ninguna de las 17 preguntas registre desacuerdo, y qué le dirían a un lector escéptico de esos porcentajes?».
- **Si hablaron de gamificación como eje central** → «en el documento la gamificación son checkmarks y sonidos de confirmación (p. 40): ¿hay niveles, insignias o barras de progreso como anuncia el alcance (p. 19), y dónde se ven?».
- **Si saltaron los resultados por tiempo** → ir directo al objetivo 4: «denos en un minuto quién probó el prototipo, cuántos eran y qué encontraron».
- **Si solo habló un integrante** → pedir explícitamente al otro que explique una parte técnica concreta: «cómo se calcula la nota ponderada por eje normativo y contra el umbral 65/100» (pp. 26-27). Es la vía legítima para verificar dominio individual.
- **Si afirmaron que la plataforma es accesible o inclusiva** → contrastar con su propia limitación de WCAG 2.1 (pp. 20-21) y dejarles corregir el alcance de la afirmación.
- **Si atribuyeron el trabajo a tres personas o mencionaron a un tercero** → no indagar en sala; anotar para la Dirección (p. 35).

## 8. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

**Dominio del tema.** Para 4,6+ necesito que expliquen sin leer cómo viaja un dato desde el simulacro hasta el indicador del tablero y cómo se calcula el puntaje frente al umbral 65/100 (pp. 26-27), y que los dos integrantes lo sostengan. Si solo describen pantallas, 3,5–3,9. Si no distinguen su propia arquitectura (pregunta 1), 3,0–3,4.

**Claridad.** Para 4,6+ necesito una exposición que en 12 minutos deje claros problema, producto y qué se validó, con la honestidad de decir «medimos percepción». Si el relato mezcla las dos arquitecturas y las dos cifras de muestra, 3,4–3,8.

**Coherencia del documento.** Aquí está el techo real de este trabajo. Con dos juegos de objetivos específicos (p. 15 frente a pp. 36-73), dos arquitecturas (pp. 15-16 frente a p. 38), 10 frente a 100 participantes (p. 42 frente a pp. 52, 59, 65), población validadora distinta de la declarada (p. 31 frente a p. 52) y el indicador SUS prometido y no reportado, **no puedo poner más de 3,5 en este criterio por lo que está escrito**; sube a 3,8–4,0 si en sala explican y ordenan las tres contradicciones. Cuenta a favor, y lo cuento: las limitaciones (pp. 19-21) y el marco normativo (pp. 25-26, 37) son de buena calidad.

**Capacidad de defensa.** Para 4,6+ necesito que respondan la pregunta de la muestra con una cifra sostenida y verificable, y la del rendimiento reconociendo el límite de su diseño (p. 30). Reconocer un límite con precisión sube la nota; defender el 100 % como prueba la baja. Si esquivan la pregunta de quién validó, 3,0–3,3.

**Rango que hoy anticipo: 3,4–3,9.** Puede llegar a 4,0–4,3 si muestran la plataforma en vivo y aclaran muestra y arquitectura con soltura. **No veo base para distinción meritoria** (requeriría ≥4,5 en todos los criterios y la coherencia documental no lo permite). Por debajo de 3,0 solo si en sala se cae la existencia del producto.

### 8.1 Formulario oficial del jurado — 5 criterios en escala 1–5

> **Instrumento distinto de los cuatro criterios de arriba.** Son las cinco preguntas del formulario que la Dirección le pide al jurado, cada una con opciones **1 2 3 4 5**. **Ninguna califica la sustentación oral:** las cinco se responden con el documento, así que van precargadas con la página que las sostiene y en sala solo se confirman.
>
> Lectura de la escala, fijada de antemano: **5** sobresaliente, sin reparos de fondo · **4** sólido, con reparos menores y declarados · **3** aceptable, con un reparo de fondo que el documento no resuelve · **2** deficiente: hay material, pero se contradice o no sostiene lo que afirma · **1** sin base verificable en el documento.
>
> ⚠️ **Este 1–5 no es la nota del acta.** La nota que se reporta sale de los cuatro criterios y de los umbrales de esta §8. La casilla del formulario la marca el jurado humano; esto es una propuesta con página.

**1. Planteamiento de la problemática y formulación de objetivos** — propuesto **2** / 5

> Claridad, pertinencia y delimitación del problema de investigación, así como la coherencia y precisión de los objetivos propuestos, verificando su alineación con el propósito del estudio y su viabilidad investigativa.

Es el planteamiento más desordenado de la jornada, y no por interpretación: el documento trae **dos juegos de objetivos específicos** —los de la p. 15 y los «Requisito 1-4» que estructuran las pp. 36-73—, sin decir cuál manda. La pregunta de investigación indaga por el **rendimiento** (p. 14) y la metodología anuncia medir rendimiento inicial y final (p. 28) sobre un diseño no experimental transeccional (p. 30) que no puede hacerlo. Y la población que valida son funcionarios de la DIAN, no los aspirantes que la p. 31 declara como participantes.

**2. Marco teórico y referentes conceptuales** — propuesto **3** / 5

> Solidez del sustento teórico del proyecto, la pertinencia y actualidad de las fuentes consultadas, y la capacidad de articular conceptos, enfoques y antecedentes que fundamenten adecuadamente la investigación.

El marco normativo es lo mejor del documento y se sostiene con página: Decreto Ley 714 de 2020 con el umbral de 65/100 (pp. 25-26), Decreto 1165 de 2019 (p. 37) y los manuales de funciones (pp. 46-49). No pasa de 3 porque el referente es normativo y no conceptual: no hay literatura sobre plataformas de preparación, usabilidad ni evaluación del aprendizaje, y lo que hay son enlaces bibliográficos (pp. 76-78).

**3. Metodología, muestra y coherencia del diseño** — propuesto **2** / 5

> Correspondencia entre el enfoque metodológico, el tipo de estudio, las técnicas e instrumentos de recolección de información y la definición de la muestra, garantizando la coherencia interna del diseño investigativo.

El diseño se declara (no experimental transeccional, muestreo por conveniencia, p. 30) pero no se puede reconstruir: **la sección de participantes no da tamaño de muestra** (pp. 31-32), el objetivo 4 habla de **10 personas** (p. 42) y los resultados de **100 funcionarios de la DIAN** (pp. 52, 59, 65), un resultado se presenta «según la simulación» (p. 43), no hay anexo del instrumento y no hay ninguna consideración ética para una encuesta a funcionarios públicos. Se queda en 2 y no en 1 porque el diseño y la técnica sí están nombrados.

**4. Resultados y conclusiones** — propuesto **2** / 5

> Calidad en la presentación, interpretación y análisis de los resultados obtenidos, así como la consistencia y pertinencia de las conclusiones en relación con los objetivos, la problemática y el marco teórico del estudio.

Los resultados son de aceptación —90 a 100 % de acuerdo con 0 % de desacuerdo en casi todos los ítems—, sin línea base con la que comparar, y **el indicador que ellos mismos fijaron, SUS superior a 68/100 (pp. 15-16, 28), no se aplica en ninguna página**. La conclusión sobre «accesibilidad total» (pp. 39, 43) contradice su propio reconocimiento de que no se cumple WCAG 2.1 (pp. 20-21). Lo que sostiene el 2 es que la sección de limitaciones es honesta y admite ese incumplimiento.

**5. Pertinencia disciplinar y articulación con la especialización** — propuesto **3** / 5

> Grado de alineación del proyecto con el campo disciplinar y los énfasis de la especialización cursada, así como su aporte potencial al desarrollo académico, profesional o investigativo del área.

Una plataforma de preparación para concursos de méritos es una solución digital útil y con destinatario claro, pero el componente de transformación digital es moderado —no hay rediseño de proceso, ni arquitectura de datos, ni analítica— y no hay URL, repositorio ni QR que permita verificar el producto.

**Suma propuesta: 12 / 25.**

**Qué subiría una casilla en sala:** El **criterio 1 pasa a 3** si dicen cuál de los dos juegos de objetivos manda y cuál de las dos arquitecturas construyeron (pregunta prioritaria 1). El **criterio 3 pasa a 3** si aclaran cuántos usuarios probaron el prototipo, quiénes eran y cómo consiguieron el acceso (pregunta 2). El **criterio 4 pasa a 3** si reconocen que sin puntajes del mismo usuario en dos momentos la conclusión de la p. 74 no puede hablar de rendimiento (pregunta 3).

**Qué la bajaría:** El **criterio 4 baja a 1** si presentan los porcentajes de aceptación como medición de rendimiento o sostienen la «accesibilidad total». **No entregaron presentación**: si sustentan con diapositivas que los jurados no pudieron revisar, califico contra el documento y lo digo.

## 9. Observaciones administrativas (no académicas)

1. **No entregaron presentación.** La carpeta del grupo tenía un único archivo al 15/08/2026 y seguía igual el 19/08/2026, el día de la sustentación (`ACA 3 - Proyecto Jenny Rivas_ José Puello.pdf`, modificado el 10/08/2026). Avisar a la moderadora antes de la sala: si sustentan con diapositivas no cargadas, no hubo posibilidad de revisarlas, y este jurado califica solo contra el documento.
2. **Tercer nombre en el equipo.** La p. 35 dice «El equipo de investigadores Puello, Rivas y Villacob»; la portada (pp. 1-2) y el cronograma registran dos integrantes. Consultar a la Dirección si hubo un tercer integrante que se retiró o si es un residuo de otro documento.
3. **Director inconsistente.** La portada (p. 2) indica «Ing. Luis Alfredo Blanquiceth Benavides» y la p. 35 atribuye la dirección a la «Dra. María Fernanda Rivera» —quien es la moderadora de este panel—. Importa porque el 75 % de la nota es del metodólogo: conviene que la Dirección confirme quién es.
4. **Fechas de firma incoherentes.** Portada «Julio de 2026» (p. 1); declaración de originalidad firmada el 19 de julio de 2026 (p. 10); exoneración de responsabilidad firmada el 30 de enero de 2026 (p. 11).
5. **Sin declaración de similitud ni de uso de IA generativa,** y sin capítulo de anexos con el instrumento aplicado ni consentimiento informado (buscado en las 78 páginas). Es un requisito de la rúbrica de integridad (15 %) que le corresponde exigir al metodólogo, no a mí; lo dejo anotado.
6. **Encuesta a 100 funcionarios de una entidad pública** (pp. 52, 59, 65) sin evidencia de autorización institucional. Si la cifra es real, la Dirección debería pedir el respaldo; si no lo es, hay que corregir el documento antes de acta.
7. **Este grupo va en la segunda jornada del mismo panel, y sí me corresponde.** La hoja `CRONOGRAMA` registra dos sesiones de la Especialización en Transformación Digital: la fila 9, martes 18 de agosto (6:00–9:00 p. m., 9 grupos), y la fila 10, **miércoles 19 de agosto (6:00–7:20 p. m., 4 grupos)**, que por celdas combinadas hereda el mismo panel —Rivera (directora), Romero (Jurado 1), Castaño (Jurado 2)—. Lo único por confirmar con la Dirección es que la convocatoria del miércoles se haya enviado, porque los nombres del panel están escritos solo en la fila del martes.
8. **Forma del documento** (no se pregunta en sala, va al acta): numeración de capítulos y de tablas/ilustraciones duplicada (pp. 15, 26-28, 33, 36-45), frase truncada en conclusiones (p. 74), erratas en enunciados de encuesta (pp. 52, 61, 62, 63) y cambio de persona gramatical (p. 40).
