# Mover las grabaciones de Meet (v2) — Guía de uso

**Versión 2 — parametrizable por diccionario**

Este es el Apps Script que mueve automáticamente las grabaciones de Google Meet a las carpetas
de Drive que les corresponden, según el curso.

## Diferencias con la v1

| | v1 | v2 |
|:--|:--|:--|
| **Destinos** | UN destino para todo + subcarpetas por materia | Cada curso va a SU carpeta |
| **Configuración** | Se regenera desde Python cuando cambias un curso | Se edita directo en Apps Script |
| **Número de sesión** | Consulta Calendar para corregirlo | Se queda con el del nombre (congelado por Meet) |
| **Dependencias** | Lee `carga_academica.py` y `sesiones_cun.py` | Solo editas el diccionario del `.gs` |

## Qué hace

1. Cada 30 minutos, lee la carpeta de Meet donde nacen las grabaciones (Meet Recordings).
2. Por cada archivo de grabación:
   - Lee el título y busca qué curso coincide (por fragmento: "Trabajo de grado 3", "Proyecto", etc.).
   - O, si el curso tiene código de Meet configurado, también puede clasificar por sala.
   - Mueve el archivo a la carpeta destino de ese curso.
3. No borra nada, no copia: MUEVE (el enlace que Meet envió por correo sigue funcionando).
4. Si no sabe clasificar algo, lo deja quieto y lo nombra en el registro.

## Pasos de instalación

### 1. Abre Apps Script

Ve a [script.google.com](https://script.google.com) con la cuenta que **organiza las clases**
(las grabaciones nacen en el Mi unidad del organizador).

### 2. Crea un proyecto nuevo

- Nuevo proyecto
- Pega TODO el contenido de `PRINCIPAL - Mover grabaciones de Meet (v2).gs`
- Guarda (le pone nombre automáticamente, o cámbiale el nombre si quieres)

### 3. Edita `CONFIG_CURSOS`

Al principio del archivo hay un diccionario. Por cada curso:

```javascript
{
  tituloContiene: "Trabajo de grado 3",  // <- fragmento del título del evento
  meetLink: "",                           // <- código de meet.google.com/abc-defg-hij, o "" si no aplica
  carpetaDestino: ""                      // <- enlace de la carpeta de Drive (pégalo tal cual)
}
```

**Cómo obtener el enlace de carpetaDestino:**
1. Abre la carpeta en Google Drive donde quieres que vayan las grabaciones de ESE curso
2. Copia el enlace de la barra de direcciones (el que dice `drive.google.com/drive/folders/...`)
3. Pégalo tal cual en `carpetaDestino`

No hace falta sacarle el ID: el script lo extrae solo.

### 4. Pega `ORIGEN_ID`

Es la carpeta donde Meet deja las grabaciones (normalmente se llama "Meet Recordings").

1. Busca esa carpeta en tu Mi unidad de Drive
2. Copia el enlace (igual que arriba)
3. Pégalo en `ORIGEN_ID` (línea ~80)

**Si no la encuentras:** ejecuta `verificarGrabaciones()` (paso 5) con `ORIGEN_ID` vacío, y el
script te SUGIERE candidatos.

### 5. Verifica (solo lectura)

Ejecuta la función `verificarGrabaciones()`:
- Botón ▶️ arriba, elige `verificarGrabaciones`
- La primera vez pedirá permisos (Autorizar → elige tu cuenta → Avanzado → Ir a [nombre del proyecto])
- Lee TODO el registro: te dice qué archivos hay, a qué carpeta iría cada uno, y si falta algo

### 6. Ejecuta una vez a mano

Si el paso anterior cuadra:
1. Cambia `SIMULAR = true` por `SIMULAR = false` (línea ~77)
2. Guarda
3. Ejecuta `moverGrabaciones()` UNA vez a mano
4. Lee el registro: debe decir "✓ MOVIDO:" para cada archivo

### 7. Instala el disparador automático

Ejecuta `instalarDisparador()`:
- Se crea un trigger que corre `moverGrabaciones()` cada 30 minutos
- A partir de ahí es automático: no hace falta que el computador esté encendido

## Funciones disponibles

| Función | Qué hace |
|:--|:--|
| `verificarGrabaciones()` | Solo lectura. Dice qué haría sin mover nada. |
| `moverGrabaciones()` | Mueve las grabaciones (respeta `SIMULAR`). |
| `instalarDisparador()` | Instala el trigger de 30 minutos. |
| `quitarDisparador()` | Quita el trigger (para el automatismo). |
| `revertirMovimientos()` | Devuelve todo a la carpeta origen. |
| `olvidarRegistro()` | Borra el historial de movimientos. |

## Cómo agregar un curso nuevo

1. Abre el proyecto en Apps Script
2. Edita `CONFIG_CURSOS` (línea ~30): agrega una entrada más
3. Guarda
4. Ejecuta `verificarGrabaciones()` para comprobar

**No hace falta regenerar nada**: editas directo en Apps Script.

## Mismo curso en varios semestres

Si tienes el MISMO curso en DOS semestres (ej: "Trabajo de grado 3" en 26ES4 y 27ES4), usa el campo
`periodo` para distinguirlos:

```javascript
{
  periodo: "26ES4",
  tituloContiene: "Trabajo de grado 3",
  meetLink: "",
  carpetaDestino: "https://drive.google.com/drive/folders/1ABC..."  // <- carpeta de 26ES4
},
{
  periodo: "27ES4",
  tituloContiene: "Trabajo de grado 3",
  meetLink: "",
  carpetaDestino: "https://drive.google.com/drive/folders/1DEF..."  // <- carpeta de 27ES4
}
```

El script verifica que el nombre del archivo contenga el periodo antes de clasificar. Así:
- "26ES4 - 54ES4 - Trabajo de grado 3 - Sesion 01" → va a la carpeta de 26ES4
- "27ES4 - 55ES4 - Trabajo de grado 3 - Sesion 01" → va a la carpeta de 27ES4

Si dejas `periodo: ""`, clasifica sin mirar el periodo (útil cuando el curso es único o cuando los
nombres de archivo no traen periodo).

## Cómo cambiar la carpeta destino de un curso

Igual: editas el diccionario, cambias el enlace en `carpetaDestino`, guardas, listo.

## Limitaciones

- **Número de sesión congelado:** Meet congela el título del evento con el que se estrenó la
  sala. Si la segunda clase dice "Sesión 01", el archivo también lo dirá. La v1 corregía esto
  consultando Calendar; la v2 no, porque es más simple y no pide permisos de Calendar.
- **Cuota de Apps Script:** 360 minutos/día de ejecución de triggers. Con 30 min entre pasadas
  y un límite de 4,5 min por pasada, no lo alcanzas.
- **Una cuenta, un organizador:** Si otra persona organiza un Meet, la grabación nace en SU
  Mi unidad, y este script no la ve.

## Dónde están los archivos

- Generador: `config/slides/build_apps_script_grabaciones_v2.py`
- .gs generado: `PRINCIPAL - Mover grabaciones de Meet (v2).gs`
- Este LEEME: `LEEME - Mover las grabaciones de Meet (v2).md`

Regenerar:
```bash
python config/slides/build_apps_script_grabaciones_v2.py
```

## Versión y autoría

**v2 — 26/08/2026**
Parametrizable por diccionario editable en Apps Script. No depende del repositorio CUN.

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>