# 26ET2-G-002 — Plataforma Digital Web PWA Multiplataforma y Chat Inteligente para el Impulso del Turismo en el Municipio de Rivera – Huila

**Sustentación:** martes 18 de agosto de 2026 · 6:20 p. m. – 6:40 p. m. · **Mi rol:** Jurado 2
**Integrantes:** Ferney Acosta Quimbaya (ferney.acostaq@cun.edu.co) · Jhon Alexander Osorio Fernández (john.osoriof@cun.edu.co) · Einsenwauer Alvarez Gutiérrez (einsenwauer.alvarez@cun.edu.co)
**Directora:** María Fernanda Rivera Sanclemente, Ph. D. (p. 2) — es también la moderadora de la sesión
**Línea:** Gestión y Tecnología (según el cronograma de la Dirección; la portada del documento deja el campo «Línea de profundización:» en blanco, pp. 1-2)
**Documentos leídos:**
- `Proyecto_de_grado_II-rivera_actualizadov3.pdf` — **86 páginas**. Es la única versión del trabajo en la carpeta y es la v3, la de mayor número de versión. Todas las citas «(p. N)» de esta ficha son de este archivo salvo que se indique «(diap. N)». **Ojo al citar en voz alta:** los números de esta ficha son las páginas del PDF, y el folio impreso del documento va **dos números por debajo** (verificado: PDF 23 = folio 21; PDF 71 = folio 69; PDF 73 = folio 71; PDF 82 = folio 80; PDF 84 = folio 82). Si se dice «página 73» a secas, el grupo abrirá su folio 73 y no encontrará la frase: conviene decir el apartado («al cierre del 8.7») o ambos números.
- `Presentacion Rivera Turismo.pdf` — **16 diapositivas**.

---

## 1. Resumen para leer en 5 minutos

Rivera (Huila) tiene termales, sitios naturales, hotelería, gastronomía y emprendimientos de café y cacao, pero su información turística está dispersa entre redes sociales, documentos institucionales y medios informales, sin un canal único de consulta (p. 17). La pregunta de investigación es cómo una plataforma web PWA con chat inteligente puede contribuir a la promoción del turismo y al fortalecimiento de los emprendimientos del municipio (p. 15).

**Método.** Estudio aplicado, descriptivo, de enfoque cualitativo (p. 32), en cinco fases: revisión documental del inventario turístico de la Alcaldía, levantamiento de requerimientos, análisis, diseño y validación conceptual (pp. 33-34). La recolección fue una entrevista semiestructurada de 15 preguntas mixtas con ítems Likert de cinco niveles, validada por juicio de tres expertos y prueba piloto, aplicada en junio de 2026 (pp. 35-36). Los participantes son **tres actores institucionales**: Alcalde, Secretaria de Turismo y Secretario de Proyectos, por muestreo intencional (p. 35). El documento advierte de forma expresa que con n = 3 los porcentajes evidencian tendencias y no permiten inferencia estadística (p. 38).

**Resultados del diagnóstico.** Consenso total (3/3) en la necesidad de la plataforma y 0/3 en que la información esté hoy centralizada (Tabla 4, p. 39); 25 requerimientos clasificados en siete categorías (Tabla 5, p. 40); priorización con catálogo turístico 5,0 y geolocalización, acceso PWA y chatbot en 4,7 sobre 5 (Tabla 6, p. 42).

**Producto.** Modelo relacional en SQL Server de doce entidades en cinco grupos funcionales —usuarios y roles, catálogo, interacción, eventos y auditoría— (pp. 49-50), con eliminación lógica, RBAC y flujo de moderación de contenido (pp. 50-51). Arquitectura desacoplada: Next.js 16 en Vercel, API REST en ASP.NET Core con JWT, imágenes en WebP y Google Maps (Tabla 10, pp. 48-49). El prototipo está **desplegado y accesible en https://www.riveraturismohuila.com/** con certificado TLS (p. 74). Verificaron manifiesto, Service Worker, ocho tamaños de icono y operación sin conexión (Tabla 16, pp. 75-76); midieron tiempos de respuesta con mediana en el orden de 101 ms y carga interactiva de la página de inicio en 1.075 ms (p. 78); y trazaron cada requerimiento contra el módulo que lo implementa (Tabla 20, p. 79).

**Lo que falta.** El cuarto objetivo —evaluar el impacto— se resolvió **diseñando** un protocolo de usabilidad (tareas, escala de 10 enunciados y tabla de indicadores) cuya columna «Valor obtenido» está **en blanco**: no se aplicó (pp. 80-82). El documento lo reconoce sin maquillaje (p. 84).

## 2. Coherencia título → objetivo → resultados

Título, objetivo general (p. 19) y pregunta de investigación (p. 15) dicen lo mismo con otras palabras: **desarrollar** una plataforma web PWA con chat inteligente para impulsar el turismo de Rivera. El verbo «desarrollar» obliga a mostrar producto, y hay producto público. **Acreditados sin reservas: 2 de 4.**

| Objetivo específico | ¿Se cumplió? | Evidencia (p. N) | Qué falta |
|---|---|---|---|
| **1. Analizar** la situación actual del turismo y la visibilidad digital | **Sí**, con alcance limitado | Tabla 4 (p. 39), Tabla 5 (p. 40), Tabla 9 (p. 47) | Solo mirada institucional (3 funcionarios). No hay voz de turistas, hoteleros, restauradores ni operadores; el documento lo declara (p. 83) |
| **2. Diseñar** la plataforma que centralice la información | **Sí** | Doce entidades en cinco grupos (pp. 49-50), decisiones de diseño justificadas (pp. 50-51), figuras 6-11 (pp. 52-57), arquitectura de software (p. 62), Tabla 10 (pp. 48-49) | Nada sustantivo. Es la sección más sólida del trabajo |
| **3. Implementar** la PWA **y el chat inteligente** | **Parcial** | PWA: URL pública (p. 74), manifiesto y Service Worker (Tabla 16, pp. 75-76), tiempos de respuesta (p. 78), geolocalización verificada con un par de coordenadas real (p. 77) | El chat: **el documento se contradice** — pp. 69-70 dicen que el módulo «se contempla como la siguiente fase de desarrollo» (la frase arranca en la 69, con «El módulo de chat inteligente» como sujeto); la p. 73 dice que «opera sobre el entorno productivo», y la p. 84 lo respalda en otras palabras: «el prototipo se encuentra desplegado en un entorno productivo de acceso público […] junto con el módulo de chat inteligente». La agenda de eventos figura «En revisión» en la Tabla 17 (p. 76). Los perfiles autenticados (turista, empresario, editor, administrador) están «por anexar la captura» (Tablas 17 y 18, pp. 77) |
| **4. Evaluar** el impacto potencial | **No ejecutado; solo formulado** | Protocolo de usabilidad: guion de 8 tareas (Tabla 21, p. 81), escala de 10 enunciados (Tabla 22, p. 81), tabla de indicadores (Tabla 23, p. 82) | La columna «Valor obtenido» de la Tabla 23 está vacía (p. 82). El propio texto aclara que las valoraciones de la Tabla 8 son expectativas previas al uso, no evaluación del producto (p. 80) |

## 3. Fortalezas verificables

1. **El producto existe y es comprobable por terceros.** URL pública con dominio propio y QR (pp. 74-75), y el documento invita explícitamente a que «cualquier evaluador pueda reproducir las verificaciones» (p. 74). En un cohorte donde muchos prototipos son maquetas, esto pesa.
2. **La condición de PWA no se afirma, se demuestra.** Manifiesto en `/manifest.json`, Service Worker en `/sw.js`, ocho tamaños de icono, tres atajos y procedimiento de comprobación paso a paso para cada elemento (Tabla 16, pp. 75-76).
3. **Trazabilidad requerimiento → módulo → prueba** (Tabla 20, p. 79): cada prioridad Likert de la Tabla 6 se conecta con el componente que la implementa y la evidencia que la respalda. Es exactamente lo que la rúbrica llama coherencia metodológica.
4. **Honestidad sobre los límites, y en el sitio correcto.** Reconocen que el diagnóstico es institucional y no generalizable (p. 83) y que el impacto declarado es percepción previa al uso, no medición (p. 84). La diapositiva 6 lo repite en sala («no incluye turistas ni empresarios») y la 14 también. No esconden la debilidad: la nombran.
5. **Diseño del chat técnicamente bien razonado.** El modelo no accede a la base de datos: la API clasifica la intención, ejecuta una consulta parametrizada y solo entonces entrega el contexto; cuatro salvaguardas y registro de conversaciones para auditoría (pp. 70-72). Ocho intenciones mapeadas a entidades concretas (Tabla 15, p. 72).
6. **Medición de desempeño real**, no estimada: cinco repeticiones por recurso, caché desactivada, desde una conexión del municipio (p. 78).

## 4. Debilidades y huecos (con página)

1. **Contradicción interna sobre el estado del chat inteligente.** Pp. 69-70, cerrando el apartado 8.6: «El módulo de chat inteligente, por su parte, cuenta ya con el soporte de datos estructurado […] y **se contempla como la siguiente fase de desarrollo** dentro de la hoja de ruta». P. 73, cerrando el 8.7: «junto con el módulo de chat inteligente […] que opera sobre el entorno productivo». P. 84 respalda la segunda versión con otras palabras («desplegado en un entorno productivo de acceso público […] junto con el módulo de chat inteligente»). Dos párrafos de dos versiones distintas del documento que quedaron uno al lado del otro. Como jurado no puedo saber, leyendo el trabajo, si el chat existe.
2. **El cuarto objetivo no se ejecutó.** Protocolo impecable, columna de resultados vacía (Tabla 23, p. 82). El prototipo estaba en producción desde julio (p. 74) y la sustentación es en agosto: hubo ventana para aplicarlo.
3. **Las limitaciones no se actualizaron.** P. 23 afirma que el proyecto «no contempla, en esta etapa, la implementación completa de la plataforma en un entorno productivo», y p. 74 informa un despliegue productivo con dominio propio. La sección de alcances quedó congelada en la versión de anteproyecto.
4. **El documento se sigue llamando «anteproyecto»** en el resumen (p. 11), la introducción (p. 15) y la apertura del capítulo 8 (p. 47), siendo la entrega final de Proyecto de Grado II.
5. **Evidencia pendiente en la mitad de las pruebas de rol.** Tabla 17: publicación «Por anexar captura» (p. 77); Tabla 18: turista registrado, empresario, editor y administrador, todos «Por anexar la captura» (p. 77). El «espacio para empresarios y productores locales» es una de las tres promesas del objetivo general (p. 23) y es justo lo que no tiene evidencia gráfica.
6. **Una prueba funcional quedó abierta:** «Agenda de eventos — consulta: Requiere nueva verificación sobre el servicio · En revisión» (p. 76), mientras la diapositiva 13 presenta la agenda como funcionalidad terminada.
7. **No hay cronograma ni presupuesto ni reporte de similitud.** Buscados en todo el documento con búsqueda de texto sobre las 86 páginas («Turnitin», «similitud», «presupuesto», «cronograma»): cero coincidencias. La rúbrica de ACA 3 pesa 15% en cronograma-presupuesto-viabilidad y 15% en integridad; es asunto del metodólogo, pero conviene registrarlo.
8. **Referencias: 10 entradas** (p. 86) para un marco que abarca turismo digital, IA conversacional, smart tourism e ingeniería de software. Ninguna posterior a 2021 y ninguna sobre PWA, la tecnología central del trabajo. Además, p. 31 cita «(Pressman, 2014)» y la lista trae «Pressman, R. S., & Maxim, B. R. (2020)»: la cita del texto no corresponde a la referencia.
9. **El modelo de lenguaje nunca se nombra.** La Tabla 10 dice «Modelo de lenguaje consumido mediante API» (p. 49) sin proveedor, versión ni costo. Para un producto que se entrega a una alcaldía, quién paga la credencial es una pregunta de viabilidad, no de curiosidad.
10. **Restos de forma:** «7.2.4 Diseño y desarrollo social» donde debería decir «de software» (p. 34); un «8» suelto al cierre del párrafo de la introducción (p. 15); un «17» intercalado en el marco referencial (p. 26); el marco todavía habla de «la app móvil» (p. 27), producto que se sustituyó por la PWA; «Tabla 9 Síntesis de hallazgos por objeto especifico» (p. 47). Se anotan como dato sobre el cuidado del documento; **no se preguntan en sala.**

## 5. PREGUNTAS ANTES de escuchar la sustentación

### 🎯 Las 3 que sí voy a preguntar

**1. El estado real del chat inteligente — y demostrarlo.**
> «El documento dice, al cerrar el apartado 8.6 —folio 68, página 70 del PDF—, que el módulo de chat se contempla como la siguiente fase de desarrollo, y al cerrar el 8.7 —folio 71, página 73 del PDF— que ya opera sobre el entorno productivo. ¿Cuál de las dos es el estado a hoy? Y si está operando, hágale en vivo una pregunta que esté fuera de alcance, para ver la respuesta que ustedes describen en el folio 69.»

- **Por qué:** el chat es la mitad del objetivo específico 3 y aparece en el título. La contradicción p. 70 vs p. 73 impide acreditarlo desde el documento. Ellos mismos invitan a probarlo en la diapositiva 16.
- **Qué la resuelve:** demuestran el chat en vivo sobre la URL pública, la respuesta cita lugares reales de Rivera y, ante una pregunta fuera de alcance, el asistente declara desconocimiento y ofrece las categorías disponibles, tal como promete la p. 71. Además reconocen que la p. 70 es un párrafo de una versión anterior que no se depuró.
- **Qué la agrava:** «está en desarrollo», «funciona en local», o mostrar un video pregrabado en lugar de la aplicación. Peor: que el asistente responda con conocimiento general sobre Rivera y no con registros de la base de datos, porque eso invalida la salvaguarda descrita en la p. 71.

**2. Qué evidencia cierra el cuarto objetivo específico.**
> «El objetivo 4 es evaluar el impacto potencial. Ustedes diseñaron el protocolo de usabilidad de las tablas 21 a 23, pero la columna "Valor obtenido" de la tabla 23 está vacía. ¿Consideran el objetivo cumplido con el diseño del instrumento, y qué impidió aplicarlo si el prototipo estaba en producción desde julio?»

- **Por qué:** p. 82 (columna vacía) y p. 80, donde ellos mismos aclaran que la Tabla 8 mide expectativas institucionales previas al uso y no evalúa el producto. Es el hueco clásico del cuarto objetivo y el más discriminante del trabajo.
- **Qué la resuelve:** distinguen con claridad «impacto potencial» de «impacto medido», sostienen que el objetivo pedía lo primero, y aportan aunque sea una aplicación piloto del protocolo —dos o tres usuarios, con el puntaje de la escala— o una fecha y un responsable concretos para aplicarlo.
- **Qué la agrava:** afirmar que el objetivo está cumplido porque la Tabla 8 da 5,0 en visibilidad, contradiciendo su propia página 80. Si dicen eso, la nota de coherencia baja.

**3. El espacio del empresario: la tercera promesa del objetivo general.**
> «El objetivo general habla de fortalecer los emprendimientos productivos, y la tabla 18 registra las pruebas de los perfiles empresario, editor y administrador como "por anexar la captura". ¿Cuántos empresarios de Rivera tienen hoy una publicación creada por ellos mismos en la plataforma y qué pasó cuando pasó por el flujo de moderación de la Secretaría?»

- **Por qué:** p. 77, Tabla 18: los cuatro perfiles autenticados quedaron sin evidencia gráfica. El registro de emprendimientos fue priorizado en 4,3/5 (Tabla 6, p. 42) y el RBAC se justifica precisamente por esa necesidad (p. 51). La diapositiva 9 presenta los cuatro perfiles como construidos, y las diapositivas 12-13 solo muestran vistas de visitante.
- **Qué la resuelve:** entran con una sesión de empresario, crean o muestran una publicación propia y la aprueban desde el perfil editor; o responden con honestidad «el flujo existe y está probado técnicamente, pero ningún empresario real lo ha usado todavía», lo cual es una respuesta perfectamente defensible a nivel de especialización.
- **Qué la agrava:** describir el flujo solo con el diagrama de la Figura 7 sin poder abrir una sesión, o afirmar que hay empresarios usándolo sin poder decir cuántos.

### Banco de reserva

- **Contenido real cargado.** «La página de inicio anuncia más de 50 lugares, 20 restaurantes, 15 hoteles y 30 experiencias tomados de las tablas Categories y Publications (p. 65). ¿Cuántos registros hay hoy en producción y de dónde salieron: del inventario de la Alcaldía o de datos de prueba?»
- **Sostenibilidad del asistente.** «La tabla 10 (p. 49) dice "modelo de lenguaje consumido mediante API" sin nombrarlo. ¿Qué modelo es, cuánto cuesta el consumo mensual estimado y a nombre de quién queda la credencial cuando ustedes se gradúen?»
- **Alcance vs. resultado.** «La página 23 dice que el proyecto no contempla la implementación en un entorno productivo y la 74 informa un despliegue con dominio propio. ¿Por qué no se actualizó la sección de alcances?» — pregunta de coherencia del documento; usar solo si sobra tiempo o si el grupo se muestra muy sólido en todo lo demás.
- **Del anteproyecto al producto.** «El objetivo que la Dirección tiene registrado habla de una aplicación web y una aplicación móvil; el documento entrega una PWA. ¿Por qué la PWA sustituye a la app nativa y qué se pierde con esa decisión?» — buena oportunidad para que luzcan criterio técnico.
- **Continuidad institucional.** «¿Existe algún acto administrativo, convenio o compromiso de la Alcaldía para adoptar la plataforma, o el municipio es hasta ahora un caso de estudio?»
- **Titularidad de los datos.** «Los comentarios y las cuentas de turistas implican datos personales y el AuditLog registra IP (p. 50). ¿Contemplaron política de tratamiento de datos y quién es el responsable?»

## 6. PREGUNTAS DESPUÉS — condicionales, para marcar en caliente

- **Si mostraron el chat funcionando y respondió bien →** no gastar la pregunta 1: pasar a preguntar de dónde salió esa respuesta concreta (qué intención de la Tabla 15 se activó) y qué hace ante una pregunta ambigua. Sube dominio si lo explican con la Figura 18 en la cabeza.
- **Si NO mostraron el chat, o solo lo mencionaron →** la pregunta 1 completa, sin rodeos, y pedir la demostración en vivo sobre riveraturismohuila.com.
- **Si presentaron todo con capturas y no abrieron la aplicación →** «Están invitando a probarlo desde el teléfono en la diapositiva 16. ¿Podemos abrirlo ahora y hacer la tarea 1 del guion de la tabla 21: localizar las termales y decir a qué hora abren hoy?» Es su propio protocolo; es justo pedirlo.
- **Si dijeron que ya aplicaron la prueba de usabilidad →** exigir los números de la Tabla 23: cuántos turistas, cuántos empresarios, tasa de tareas completadas y puntaje de la escala. Si no hay cifras, la afirmación no se sostiene.
- **Si dijeron que la plataforma «ya la usa la Alcaldía» →** preguntar quién publica hoy, con qué frecuencia y quién aprueba, y si existe algún compromiso formal (ver reserva de continuidad institucional).
- **Si afirmaron que la muestra valida el diagnóstico →** recordarles su propia página 83 y preguntar qué cambiaría el diseño si hubieran entrevistado a diez hoteleros. Van a poder responder: la limitación ya la tienen pensada.
- **Si se pasaron del tiempo y saltaron los resultados o el producto →** ir directo al objetivo 3: «en 30 segundos, ¿qué de lo que prometió el objetivo 3 está hoy operando y qué no?»
- **Si solo habló uno de los tres →** pedir explícitamente al que no habló que explique el flujo del chat inteligente de la Figura 18 (p. 73) o el flujo de moderación de la publicación (p. 51). Es la vía legítima para verificar dominio individual.
- **Si el que responde lo técnico no es quien firmó la parte metodológica →** pedir a otro integrante que explique por qué el estudio es cualitativo si las tablas 6 y 8 promedian escalas Likert. La p. 38 les da la respuesta correcta; ver si la conocen.
- **Si leyeron las diapositivas palabra por palabra →** no preguntarlo, anotarlo: afecta claridad y dominio, no se discute en sala.

## 7. Umbrales de nota (escala 0,1–5,0, cuatro criterios del jurado)

Criterios: **dominio del tema · claridad · coherencia del documento · capacidad de defensa.** Nivel exigido: especialización profesionalizante.

- **4,6 – 5,0 (excelente / candidato a meritoria).** Necesito ver **las dos cosas**: (a) el chat inteligente respondiendo en vivo sobre la URL pública, con una respuesta que provenga de la base de datos y con el comportamiento de «no sé» ante una pregunta fuera de alcance; y (b) una respuesta que distinga con precisión conceptual «impacto potencial» de «impacto medido», asumiendo sin defensas que el protocolo no se aplicó. Súmese que los tres integrantes respondan, cada uno sobre lo suyo. **Recordatorio: 5,0 no es «me gustó»: es proponer laureada, y exige acuerdo de ambos jurados.**
- **4,0 – 4,5 (buen desempeño).** Es el rango de llegada esperable con lo que trae el documento. Aquí caen si el chat se muestra pero con tropiezos, o si el chat no se muestra pero el resto de la defensa es sólida, o si sostienen que el objetivo 4 está cumplido sin distinguir potencial de medido. También si solo uno de los tres domina el producto. Si falta la demostración en vivo del producto que ellos mismos invitan a probar, difícilmente pasa de **4,4**.
- **3,6 – 3,9.** Si aparece que el chat no existe en producción (es decir, que la p. 73 y la p. 84 afirman algo que no se sostiene) pero reconocen el error con transparencia y defienden bien la PWA, que sí está desplegada y verificada.
- **3,0 – 3,5 (aceptable).** Si no logran demostrar ningún componente en funcionamiento, si no pueden explicar la arquitectura que firman, o si atribuyen al trabajo resultados que el documento no tiene.
- **Por debajo de 3,0.** No lo veo posible con este documento: hay producto desplegado, modelo de datos serio y trazabilidad. Solo lo justificaría una defensa en la que ningún integrante pueda explicar lo que entregó.

**Mi posición de partida antes de la sala: 4,3 – 4,7**, y lo que mueve la aguja dentro de ese rango es una sola cosa: **que el chat inteligente y el perfil de empresario se vean funcionando.**

## 8. Observaciones administrativas (no académicas)

1. **El título del cronograma no coincide con el del documento.** Dirección registró «Diseño e implementación de una plataforma digital web y móvil con chat inteligente para la promoción turística de Rivera, Huila»; el documento se titula «Plataforma Digital Web PWA Multiplataforma y Chat Inteligente para el Impulso del Turismo en el Municipio de Rivera – Huila» (pp. 1-2). Hay que fijar cuál es el título de grado antes del acta. No es una debilidad académica: la PWA es una respuesta legítima al «web y móvil», pero el título oficial debe ser uno.
2. **La portada deja «Línea de profundización:» en blanco** (pp. 1-2). El cronograma la registra como «Gestión y Tecnología». Corrección de una línea.
3. **Equipo de 3 integrantes:** cumple el máximo de la norma.
4. **Correo institucional:** el cronograma registra `john.osoriof@cun.edu.co` para Jhon Alexander Osorio Fernández (sin la «h» intermedia de «Jhon»). Verificar antes de enviar cualquier notificación.
5. **Anexos anunciados y no incluidos:** el documento remite a evidencia gráfica «anexa por separado» para las operaciones con sesión autenticada (p. 76) y a capturas «por anexar» (pp. 77). En la carpeta del grupo solo hay el trabajo y la presentación. Si esos anexos existen, deberían estar en la carpeta; conviene pedirlos al grupo o al metodólogo.
6. **Sin reporte de similitud ni cronograma ni presupuesto** en el documento (búsqueda de texto sobre las 86 páginas, sin coincidencias). Corresponde al metodólogo, que lleva el 75% de la nota; se registra para la Dirección, no para descontar en la sustentación.
7. **La directora del trabajo es también la moderadora de la sesión** (María Fernanda Rivera Sanclemente, p. 2). Es lo previsto en el cronograma para todos los grupos de esta hoja; se anota solo por transparencia del acta.
8. **Firmas de originalidad y exoneración presentes** con los tres nombres, fechadas el 8 de agosto de 2026 en Rivera (pp. 13-14).
