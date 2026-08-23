# `_Revisiones/` — donde caen los documentos de estudiantes que se van a comentar

**Nada de esta carpeta entra a git.** El `.gitignore` de aquí ignora todo salvo sí mismo y este
archivo. Sí se sincroniza con Google Drive, que es el Drive del propio Docente y donde el documento
ya vive de todos modos; lo que no puede pasar es que el trabajo de un estudiante entre al historial
de git, porque de ahí no sale nunca.

## Qué se pone aquí

Por cada documento que revisas, tres archivos con la misma raíz:

| Archivo | Quién lo pone | Qué es |
|---|---|---|
| `<algo>.docx` | tú | la copia que descargaste del documento compartido |
| `<algo>.plan.json` | yo | los comentarios redactados, uno por criterio |
| `<algo> - Plan.gs` | `plan_comentarios.py` | lo que pegas en Apps Script |

Ponles nombre corto. La ruta completa de esta carpeta ya gasta unos 60 caracteres con la unidad de
Google Drive, y Windows corta en 260.

## Cómo se usa

El procedimiento completo está en
**[LEEME - Comentar documentos de estudiantes.md](../LEEME%20-%20Comentar%20documentos%20de%20estudiantes.md)**,
en la raíz. En corto:

```bash
python config/gdocs/plan_comentarios.py leer "_Revisiones/ACA1 - Perez.docx" \
    --curso proyecto1 --aca aca1
python config/gdocs/plan_comentarios.py generar "_Revisiones/ACA1 - Perez.plan.json"
```

## Cuándo se limpia

Cuando el corte ya cerró y la nota está puesta. No hay automatismo que borre: es tu carpeta y la
vacías cuando quieras. Lo único que conviene no dejar aquí de un semestre para otro son los `.docx`,
porque son la versión vieja del trabajo de alguien y ya no sirven para nada.
