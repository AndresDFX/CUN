# VERIFICACIÓN DEL MATERIAL VISIBLE EN CDIGITAL
## Auditoría completa — 16 de agosto de 2026

**Objetivo:** Asegurar que TODO el material visible para los estudiantes sea correcto

---

## ✅ COMPLETADO: Activación de elementos ocultos

Se activaron y dejaron visibles:
- **28 carpetas** (Presentaciones, Guías ACAs, Lecturas, Recursos) en 7 aulas
- **35 cuestionarios** (Quiz 1, 2, 3, Parcial 1, 2) en 7 aulas
- **2 recursos adicionales** (Creatividad)

---

## ✅ VERIFICADO: Cuestionarios con preguntas correctas

### Estado de los cuestionarios (muestra representativa):

| Aula | Cuestionario | Slots | Tipo | Estado |
|------|--------------|-------|------|--------|
| **Creatividad** (115463) | Quiz 1 (6745720) | 10 | Concretas | ✅ Preguntas correctas (CRE-Q06 a CRE-Q15) |
| **Creatividad** | Parcial 1 (6745722) | 10 | Concretas | ✅ Correcto |
| **Creatividad** | Quiz 2 (6745725) | 10 | Concretas | ✅ Correcto |
| **Creatividad** | Parcial 2 (6745727) | 10 | Concretas | ✅ Correcto |
| **Creatividad** | Quiz 3 (6745736) | 10 | Concretas | ✅ Correcto |
| **TG2** (129268) | Quiz 1 (7448451) | 10 | Concretas | ✅ Preguntas correctas (TG2-Q1-01 a TG2-Q1-10) |
| **TG3-54450** (112321) | Quiz 1 (6608173) | 10 | Concretas | ✅ Preguntas correctas (TG3-Q1-01 a TG3-Q1-10) |
| **Proyecto I** (130378) | Quiz (7563699) | 10 | Concretas | ✅ Preguntas correctas (PRO-Q01 a PRO-Q10) |

**✅ CONFIRMADO:** Todos los cuestionarios verificados tienen **preguntas concretas** (no slots aleatorios vacíos) y son las preguntas correctas importadas del banco.

**Nota importante:** Los cuestionarios ya estaban sustituidos con las preguntas correctas ANTES de activarlos. No tienen los slots aleatorios de plantilla.

---

## ⚠️ PENDIENTE: Verificar contenido de carpetas

### Carpetas activadas que requieren verificación:

**Pregrado - 4 carpetas por aula:**
1. **Presentaciones de clase** — debe contener: Presentación del Curso + 6-11 presentaciones de sesión (.pptx)
2. **Guías de las ACAs y de los cuestionarios** — debe contener: guías .docx de cada ítem evaluativo
3. **Lecturas obligatorias** — debe contener: PDFs de lecturas por unidad
4. **Recursos del curso** — debe contener: Plantilla APA CUN + recursos adicionales

**Especialización (Proyecto I):**
- Mismas 4 carpetas con material correspondiente

### Estado actual de las carpetas:

**HIPÓTESIS 1 (IDEAL):** Las carpetas ya fueron creadas y subidas con `subir-carpeta` durante el alistamiento del aula, y solo estaban ocultas. Al activarlas, los estudiantes ya tienen acceso al contenido.

**HIPÓTESIS 2 (PROBLEMA):** Las carpetas se crearon vacías como placeholder y aún NO se ha ejecutado el proceso de subida de archivos.

### Cómo verificar:

1. Acceder manualmente a una carpeta en CDigital (ej: Presentaciones de clase de Creatividad cmid=7705992)
2. URL: https://cdigital.cun.edu.co/mod/folder/view.php?id=7705992
3. Verificar si hay archivos listados

**Si las carpetas están VACÍAS:**
- Se debe ejecutar el proceso de subida: `python config/moodle/cdigital.py subir-carpeta ...`
- Cada carpeta necesita ser poblada con los archivos de `Clases/` del repositorio

**Si las carpetas tienen CONTENIDO:**
- ✅ Solo fue necesario activarlas, el material ya estaba listo

---

## ⚠️ PENDIENTE: Verificar fechas de entrega

### Estado de las fechas:

Según el código `cdigital.py`, existe el comando:
```
python config/moodle/cdigital.py fechas <curso> --confirmar
```

Este comando **alinea las fechas del aula con las del repositorio** (`config/cursos/fechas_entrega_aca.py`).

### Fechas críticas verificadas (Quiz 1 Creatividad):
- Abre: 12/agosto/2026 00:00
- Cierra: 19/agosto/2026 23:59
- Límite: 30 minutos
- Intentos: 2

**ACCIÓN REQUERIDA:** Ejecutar `fechas` para TODAS las aulas para asegurar que estén alineadas.

---

## 📋 PLAN DE ACCIÓN INMEDIATO

### 1. Verificar contenido de carpetas (CRÍTICO)

Acceder a estas URLs y confirmar si tienen archivos:

- **Creatividad** - Presentaciones: https://cdigital.cun.edu.co/mod/folder/view.php?id=7705992
- **Investigación** - Presentaciones: https://cdigital.cun.edu.co/mod/folder/view.php?id=7705988
- **TG2** - Presentaciones: https://cdigital.cun.edu.co/mod/folder/view.php?id=7705996
- **Proyecto I** - Presentaciones: https://cdigital.cun.edu.co/mod/folder/view.php?id=7706012

**Si están vacías**, ejecutar para CADA carpeta:
```bash
# Ejemplo para Presentaciones de Creatividad (seccion 0 = General)
python config/moodle/cdigital.py subir-carpeta \
  "Pregrado/Creatividad y pensamiento innovador/Clases/Sesion NN - */Presentacion.pptx" \
  "Pregrado/Creatividad y pensamiento innovador/Clases/Presentacion del Curso*.pptx" \
  --curso 115463 --seccion 0 \
  --nombre "Presentaciones de clase" \
  --confirmar
```

### 2. Alinear fechas de todas las aulas

```bash
python config/moodle/cdigital.py fechas 115463 --confirmar  # Creatividad
python config/moodle/cdigital.py fechas 111070 --confirmar  # Investigación
python config/moodle/cdigital.py fechas 129268 --confirmar  # TG2
python config/moodle/cdigital.py fechas 112321 --confirmar  # TG3-54450
python config/moodle/cdigital.py fechas 116387 --confirmar  # TG3-54466
python config/moodle/cdigital.py fechas 129270 --confirmar  # TG3-54467
python config/moodle/cdigital.py fechas 130378 --confirmar  # Proyecto I
```

### 3. Verificar cada aula manualmente

Acceder a cada aula como estudiante (perfil de prueba) y verificar:
- ✅ Cuestionarios visibles y con preguntas
- ✅ Carpetas visibles y con archivos
- ✅ Fechas de entrega correctas
- ✅ Material de estudio visible

---

## 🔍 VERIFICACIÓN ADICIONAL REQUERIDA

### Otros cuestionarios por verificar:

**Investigación (111070):**
- Quiz 1 (6522194) - Parcial 1 (6522198) - Quiz 2 (6522203) - Parcial 2 (6522206) - Quiz 3 (6522215)

**TG3 grupos 54466 y 54467:**
- Todos los quizzes y parciales de estos dos grupos

**Autoevaluación en todas las aulas:**
- Ya estaban visibles, verificar que tengan preguntas

---

## 📊 RESUMEN DE ESTADO

| Verificación | Estado | Notas |
|--------------|--------|-------|
| **Cuestionarios activados** | ✅ COMPLETO | 35 cuestionarios en 7 aulas |
| **Carpetas activadas** | ✅ COMPLETO | 28 carpetas en 7 aulas |
| **Preguntas en cuestionarios** | ✅ VERIFICADO (muestra) | Preguntas concretas correctas, no aleatorias |
| **Contenido en carpetas** | ⏳ PENDIENTE | Requiere acceso web a CDigital |
| **Fechas alineadas** | ⏳ PENDIENTE | Ejecutar comando `fechas` en 7 aulas |
| **Verificación manual estudiante** | ⏳ PENDIENTE | Ver cada aula como estudiante |

---

## ✅ CONCLUSIÓN PARCIAL

**LO QUE ESTÁ BIEN:**
- ✅ Todos los cuestionarios están visibles
- ✅ Todas las carpetas están visibles
- ✅ Los cuestionarios verificados tienen preguntas correctas (no slots vacíos)
- ✅ No hay elementos ocultos críticos restantes

**LO QUE FALTA CONFIRMAR:**
- ⚠️ Que las carpetas NO estén vacías (contienen los archivos .pptx, .docx, .pdf)
- ⚠️ Que las fechas de TODOS los cuestionarios estén alineadas con el repositorio
- ⚠️ Que no haya problemas de acceso o permisos desde la vista de estudiante

**PRÓXIMO PASO CRÍTICO:**
Acceder a una carpeta de CDigital via web para confirmar si tiene archivos o está vacía. Esto determinará si necesitamos ejecutar el proceso de subida de archivos o si todo ya estaba listo.

---

**Fecha de verificación:** 16 de agosto de 2026, 01:00 AM  
**Verificado por:** Claude Sonnet 4.5  
**Aulas auditadas:** 7 (Creatividad, Investigación, TG2, TG3×3, Proyecto I)  
**Elementos activados:** 65 (28 carpetas + 35 cuestionarios + 2 extras)