# Matriz de herramientas prácticas (guía docente) — CUN 2026

**Docente:** Julian Andres Castaño · `julian_castanoe@cun.edu.co`  
**Plataforma de entrega:** **CDigital** (placeholder: `[URL CDigital — campus del curso pendiente]`)  
**Script de capturas:** `config/slides/capture_herramientas_practicas.py`  
**Actualizado:** 2026-08-10 (renumerado tras pasar la Sesión 01 a encuadre: Creatividad tiene **7** sesiones e Investigación **6**; los prefijos `SNN_` coinciden con la sesión real)

> **REGLA DE PRÁCTICA:** toda actividad práctica de clase usa **solo componentes gratis + en la nube** (browser / SaaS free tier). Sin software de escritorio de pago, sin instalaciones obligatorias en el PC del estudiante (ni Packet Tracer, Visual Studio desktop, Office desktop obligatorio, Adobe de pago, Mendeley Desktop / Cite en Word, etc.).

> Convención de capturas: `<Curso>/Docente/Guiones/Capturas/Sesion NN/` (+ copia plana en `Docente/Guiones/Capturas/` para embeber en `.docx`, y espejo en `Clases/Sesion NN…/Capturas/` cuando aplica).

---

## 1. Creatividad y Pensamiento Innovador (mié 5–6 pm) — más práctico

| Sesión | Tema | Herramienta práctica (gratis / online) | Entregable | Capturas / estado |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Encuadre** (no se dicta tema) · ficha problema–oportunidad | **Padlet** (tablero expectativas) · **Excalidraw** · tldraw · **Google Docs** · ficha HTML modelo | `Ficha_problema_oportunidad.docx` + post en Padlet | ✅ `Sesion 01/` |
| — | *Lectura autónoma U1–U2* (Propuesta de Innovación · creatividad e IE) | PDF de acceso abierto en `Clases/Sesion 01 - …/` | — | ✅ PDF + `.txt` en la carpeta |
| **02** | Design Thinking y técnicas de ideación | Miro DT templates (free) · Excalidraw journey · IDEO Design Kit (si carga) | `S02_Ideacion_Apellido` | ⏳ capturas plantilla Miro |
| **03** | Gestión de la innovación (Manual de Oslo / OCDE) | Tabla Oslo en Google Docs / Excalidraw | `S03_FichaOslo_Apellido` | ⏳ pendiente guía en pantalla |
| **04** | Tipos de innovación | Misma pizarra + ejemplos | `S04_MatrizTipos_Apellido` | ⏳ |
| **05** | Validación de la propuesta · vigilancia tecnológica (FODA · Canvas · MVP + tablero de señales) | **Canvanizer** BMC · Excalidraw · Strategyzer solo como referencia visual · **Google Scholar** · Patents · docs oficiales (web) | `S05_ValidacionVigilancia_Apellido` | ✅ capturas Canvas en `Capturas/Herramientas/` · ⏳ flujo Scholar/Patents (reutilizar el de Investigación **S04**) |
| **06** | Innovación local–internacional · entidades de apoyo | **Canva free** (opcional) · Google Docs / Slides pitch 1 pág. | `S06_EcosistemaPitch_Apellido` | ⏳ Canva no capturó en headless |
| **07** | Taller de consolidación y sustentación de la propuesta (cierre) | **Google Docs** (documento consolidado) · Slides para la sustentación · CDigital (auto y coevaluación) | `S07_PropuestaConsolidada_Apellido` | ⏳ sin herramienta nueva: se sostiene lo ya escrito |

**Prioridad aula S01–S02:** rompehielos según el tamaño (Slido con más de 20; Padlet hasta 20) → Excalidraw (sin cuenta) → export PNG → Drive de clases.

**Tablero colaborativo (rompehielos / Preséntate / S01) — decisión 2026-08:**

| Rol | Herramienta | URL | Por qué |
| :--- | :--- | :--- | :--- |
| **Hasta 20 estudiantes** (solo Investigación) | **Padlet** | https://padlet.com/andres_dfx/cun-wruz81hmf9k06gd7 | Tablero único de presentación de estudiantes · QR en Presentación del Curso · misma URL en Sesión 01 |

> Con **más de 20 estudiantes** el rompehielos es **Slido** («dos verdades y una mentira», tres rondas, con premio): Padlet gratis solo da 3 tableros y un muro de 50 o 112 notas no lo lee nadie. La elección la hace `modo_rompehielos()` contando la matrícula real, no una lista escrita a mano.
> Constante de build: `PADLET_PRESENTACION_URL` en `config/slides/cun_slides_engine.py`. **No** usar instrucciones de “Clear posts” / reutilizar borrando posts / “3 padlets del plan gratis”. Jamboard discontinuado. Miro/FigJam free útiles más adelante (DT).

---

## 2. Investigación Ciencia y Tecnología (jue 5–6 pm)

| Sesión | Tema | Herramienta práctica | Entregable | Estado |
| :---: | :--- | :--- | :--- | :--- |
| **01** | **Encuadre** (no se dicta tema) · producto final = artículo | **Padlet** (expectativa / tema de interés) · **Google Docs** | `S01_TemaTentativo_Apellido` + post en tablero | ✅ tablero S01 |
| — | *Lectura autónoma U1–U2* (Syllabus y producto · método científico) | PDF de acceso abierto en `Clases/Sesion 01 - …/` | — | ✅ PDF + `.txt` en la carpeta |
| 02–03 | MinCiencias / 6 líneas de Ingeniería → prueba parcial y 1.er avance | **Google Docs** / plantilla artículo (abrir en Docs) | Avances por unidad | ⏳ guías genéricas |
| **04** ★ | Problema y pregunta · **bases de datos CUN y gestores de citas** (U6+U8) | Excalidraw (espina / árbol) · **Scholar** · SciELO · Redalyc · **ZoteroBib** · biblioteca CUN (login) | `S04_ProblemaPregunta_Apellido` (pregunta + 3 fuentes citadas) | ✅ sesión emblemática (flujo Scholar → ZoteroBib → Docs) |
| **05** | Planteamiento del problema · **marco teórico y revisión de literatura** (U7+U10–12) | **Google Docs** (plantilla APA) · **ZoteroBib** · citas nativas de Docs | `S05_Planteamiento_Apellido` (planteamiento + 1.ª página de marco) | ⏳ reutilizar capturas ZoteroBib de la S04 |
| **06** | Socialización del artículo y cierre del curso | **Google Slides** (socialización) · CDigital (auto y coevaluación) | — *(sin entregable nuevo: el corte 3 cerró el 12/09)* | ⏳ sin herramienta nueva |

★ = emblemática práctica de esta pasada.

> **Temario adelantado 2026-08-11:** U8 (bases + gestores) subió a la **S04** y U10–U12 (marco y revisión) a la **S05**, porque todo el corte 3 cierra el **12/09** y la S06 quedó como socialización y cierre. El flujo Scholar → ZoteroBib → Docs, que era la práctica emblemática de la vieja S06, ahora se dicta en la **S04**.

---

## 3. Proyecto I (lun 8–10 pm)

| Sesión | Tema | Herramienta práctica | Entregable | Estado |
| :---: | :--- | :--- | :--- | :--- |
| **01** ★ | **Encuadre** (no se dicta tema) · presentación del curso, docente, estudiantes y ACAs · tutorías | **Padlet** (expectativa / tema tentativo) · **Form tutorías** · **ZoteroBib** · APA Style (web) · plantilla APA en **Google Docs** · CDigital | Tema tentativo + registro tutoría | ✅ emblemática + capturas + tablero |
| — | *Lectura autónoma ESP329 U1* (Fundamentos y enfoque de investigación) | PDF de acceso abierto en `Clases/Sesion 01 - …/` | — | ✅ 3 PDF + `.txt` en la carpeta |
| 02–06 | Problema → marcos *(S04 = retroalimentación del **Quiz** + antecedentes)* | ZoteroBib + Google Docs + plantilla APA (nube) | Secciones anteproyecto | ⏳ |
| **07** | Marco legal · APA 7 | ZoteroBib · citas en Google Docs · APA Style web · plantilla CUN (Docs) | Citas corregidas | ⏳ (reutilizar capturas P1/ZoteroBib) |
| 08–11 | Método → cierre | CDigital entregas · form tutorías cada encuentro | Anteproyecto / coeval | ⏳ |

**Links fijos P1**
- Estudiante (compartir): https://forms.gle/oZ8xCYiUo3KEWr1d9  
- Docente (NO compartir): https://forms.gle/6t6BXqQ2Kwmivpct8  

---

## 4. TG2 / TG3 (menos “lab”, sí herramientas de escritura)

| Curso | Uso típico | Herramienta | Capturas |
| :--- | :--- | :--- | :--- |
| TG2 / TG3 S01 | Encuadre / acuerdo pedagógico | **Slido** — «dos verdades y una mentira», 3 rondas, 8 min (50 y 112 estudiantes) | ✅ slide + guion S01 |
| TG2 / TG3 | Búsqueda y citas | Google Scholar · **ZoteroBib** (https://zbib.org/) | ✅ `Docente/Guiones/Capturas/Herramientas/tg_*.png` (ambos cursos) |
| TG2 / TG3 | Formato artículo / APA | Plantilla APA CUN abierta en **Google Docs** · APA Style web | Reutilizar `p1_apa_style.png` |
| TG2 / TG3 | Antiplagio | Herramienta institucional CUN si existe en CDigital; si no, **no inventar** URL — instruir ruta oficial del semestre | ⏳ pendiente URL real |
| TG2 / TG3 | Estructura artículo | **Google Docs** + ZoteroBib | Guía breve (misma lógica de Investigación **S04–S05**) |

---

## 5. Bloqueos reales documentados (no inventar)

| Herramienta | Qué pasó al capturar | Qué hacer en clase |
| :--- | :--- | :--- |
| MCP `cursor-ide-browser` | Servidor no disponible en esta sesión | Usar Chrome del docente + script headless |
| Google Docs / Forms | Pantalla de login (esperado) | El estudiante inicia sesión; no pedir claves en Meet |
| Form tutorías P1 | Modal “Iniciar sesión para continuar” | Parte del flujo; documentado en captura |
| Scholar (búsqueda deep) | “Tráfico inusual” en headless | Usar Chrome interactivo; home Scholar sí capturó |
| Canva Whiteboard | Timeout headless (reconfirmado 2026-08) | Plan B: Excalidraw / tldraw; Canva free manual si lo necesitan |
| Miro Empathy Map | Timeout headless ocasional | Reutilizar home Miro DT (`s01_miro_design_thinking.png`) o abrir en Chrome interactivo |
| Biblioteca CUN / CDigital | URL campus pendiente | Placeholder + instrucción de login institucional |
| IDEO Design Kit | Captura casi vacía (9 KB) | No usar esa PNG; abrir manualmente en clase si aplica |

---

## 6. Orden sugerido para siguientes pasadas

1. Creatividad **S02** (Design Thinking en Miro free / Excalidraw) + **S05** (Canvanizer paso a paso del lienzo, y Scholar/Patents para el tablero de vigilancia).  
2. Proyecto I **S07** (APA + ZoteroBib + Google Docs) con pantallas de Docs en el navegador.  
3. TG2/TG3: 1 guía corta “estructura artículo + antiplagio institucional”.  
4. Cuando existan URLs reales Meet/CDigital: sustituir placeholders y re-capturar flujos de entrega.

---

## 7. Catálogo preferido (gratis + nube) vs. no usar en práctica

| Preferir (browser / free tier) | No exigir en clase |
| :--- | :--- |
| **Slido** (rompehielos S01 con más de 20) · **Padlet** (hasta 20) | Apps de escritorio de pago; instalaciones locales |
| Excalidraw, tldraw, diagrams.net, Miro free, Canva free, Canvanizer | Adobe de pago, Visio, Office desktop obligatorio |
| Google Docs / Slides / Forms, CDigital | Instalaciones locales pesadas / “abre el .exe” |
| Google Scholar, SciELO, Redalyc, biblioteca CUN web | — |
| **ZoteroBib** (zbib.org), citas nativas de Google Docs | Mendeley Desktop, Mendeley Cite + Word, Zotero Desktop obligatorio |
| CodePen / CodeSandbox / Colab (si algún taller lo pide) | Visual Studio desktop, Packet Tracer, Cisco desktop |
