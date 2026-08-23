# -*- coding: utf-8 -*-
"""Convierte el manuscrito en la versión de PROTOCOLO que sí se puede depositar.

Por qué: el título ya dice «protocolo reproducible», pero el cuerpo conservaba el esqueleto de una
sección de resultados con 77 marcadores vacíos y una nota interna que decía «eliminar antes del
sometimiento». Un protocolo **no tiene resultados**: eso no es una carencia, es el género.

Qué hace, y nada más que esto:
  1. Elimina la sección 4 (RESULTADOS) completa y la sustituye por una sección breve que declara
     qué se reportará y dónde.
  2. Deja UN SOLO AUTOR. Los coautores del Equipo 1 no han dado autorización escrita —el propio
     manuscrito lo exige— y el checklist de SciELO obliga a declarar que todos consienten.
  3. Convierte cada marcador `[PENDIENTE: …]` en prosa en futuro, que es lo honesto en un protocolo:
     no afirma que algo se hizo, dice qué se hará y cómo se verificará.
  4. Quita la «Nota de estado del manuscrito», que era una instrucción interna.
"""
import re
import sys
from pathlib import Path

BASE = Path(r"g:\My Drive\Trabajos\Empleo\CUN\Cursos\Investigacion\dashboard\datos\entregables")
ORIGEN = BASE / "Articulo_Calidad_D_Desercion_ML.md"
DESTINO = BASE / "Preprint_Protocolo_Desercion_ML.md"

a = ORIGEN.read_text(encoding="utf-8")

# ── 1 · fuera la sección de resultados ────────────────────────────────────────
i4, i5 = a.find("## 4. RESULTADOS"), a.find("## 5. DISCUSIÓN")
if i4 == -1 or i5 == -1 or i5 < i4:
    sys.exit("no encuentro los límites de la sección 4")
NUEVA_4 = """## 4. RESULTADOS ESPERADOS Y ESTADO DEL ESTUDIO

Este documento es un **protocolo**: registra el diseño, el procedimiento y el plan de análisis
**antes** de disponer de resultados, con el fin de dejar constancia pública y fechada de las
decisiones metodológicas y de reducir el margen de análisis oportunista.

Al ejecutar el protocolo se reportarán, en una publicación posterior que citará este preprint por su
DOI: la caracterización del conjunto de datos generado; la comparación de desempeño entre los cuatro
modelos descritos en 3.6, con AUC-PR, exactitud, precisión, exhaustividad y F1, cada una con su
intervalo de confianza del 95 % por remuestreo; el efecto del punto de corte temporal descrito en
3.4; la atribución de variables; la auditoría de equidad por subgrupos descrita en 3.8; y la
validación externa sobre el conjunto de acceso público indicado en 3.9.

No se anticipa aquí ninguna cifra de desempeño. Cualquier valor que se publicara antes de ejecutar
el procedimiento no sería un resultado sino una expectativa, y presentarlo como lo primero es
justamente la práctica que este protocolo pretende evitar.

"""
a = a[:i4] + NUEVA_4 + a[i5:]

# ── 2 · un solo autor ─────────────────────────────────────────────────────────
a = re.sub(r"\*\*Coautores\*\*\s*\n\s*\[POR COMPLETAR:.*?\]\s*\n",
           "**Autoría:** este protocolo lo firma un único autor. Los integrantes del semillero que\n"
           "participen efectivamente en la ejecución se incorporarán como coautores en la publicación\n"
           "de resultados, con arreglo a los criterios de autoría del ICMJE y previa autorización\n"
           "expresa y por escrito de cada uno.\n",
           a, flags=re.S)

# ── 3 · los marcadores, uno a uno ─────────────────────────────────────────────
CAMBIOS = [
    (r"ORCID: \[POR COMPLETAR:[^\]]*\]",
     "ORCID: en trámite de registro; se consignará en la versión de resultados."),
    (r"\[PENDIENTE: síntesis de los resultados principales[^\]]*\]",
     "Por tratarse de un protocolo, no se reportan resultados: el resumen describe el diseño y el "
     "plan de análisis, y los hallazgos se publicarán por separado."),
    (r"\[PENDIENTE: consignar el identificador de confirmación[^\]]*\]",
     "La fecha de depósito de este preprint actúa como constancia pública de que el plan de análisis "
     "quedó fijado antes de ejecutar los experimentos."),
    (r"\[PENDIENTE: registrar la fuente exacta[^\]]*\]",
     "La fuente, el año de corte y la tabla empleada para cada variable calibrada se registrarán en "
     "la ficha de datos que acompañará al conjunto; no se declarará ninguna distribución cuya fuente "
     "no haya sido consultada directamente."),
    (r"\[PENDIENTE: fijar y declarar el valor exacto de prevalencia[^\]]*\]",
     "El valor de prevalencia y su justificación documental se fijarán y declararán al generar el "
     "conjunto, y quedarán en la ficha de datos."),
    (r"\[PENDIENTE: declarar el valor de precisión mínima[^\]]*\]",
     "El umbral de precisión mínima se fijará antes de evaluar los modelos y se justificará en "
     "términos de la capacidad real de atención institucional."),
    (r"\[PENDIENTE: registrar las versiones exactas[^\]]*\]",
     "Las versiones exactas de Python y de cada biblioteca, junto con el archivo de entorno que "
     "permite reconstruirlo, se publicarán con el código."),
    (r"\[PENDIENTE: crear el repositorio público[^\]]*\]",
     "El repositorio público con el código y el conjunto de datos sintético, con identificador "
     "persistente, se publicará al reportar los resultados y se enlazará desde este preprint."),
    (r"\[PENDIENTE: número y fecha del acta del Comité[^\]]*\]",
     "El estudio se ejecutará sobre datos sintéticos y sobre un conjunto de acceso público ya "
     "anonimizado, de modo que no trata datos personales identificables. Antes de reportar "
     "resultados se solicitará al Comité de Ética institucional la constancia que corresponda."),
    (r"\[PENDIENTE DE COMPLETAR TRAS LOS RESULTADOS: contrastar[^\]]*\]",
     "El contraste con los rangos reportados por Berens et al. (2019), Kabathova y Drlik (2021), "
     "Chung y Lee (2019) y Delen (2010) se realizará en la publicación de resultados."),
    (r"\[PENDIENTE: conclusión sobre el desempeño comparativo[^\]]*\]",
     "La conclusión sobre el desempeño comparativo de los cuatro modelos, y sobre si las diferencias "
     "son estadísticamente distinguibles, corresponde a la publicación de resultados."),
    (r"\[PENDIENTE: conclusión sobre la atribución de variables[^\]]*\]",
     "La conclusión sobre atribución de variables y sobre la auditoría de equidad por subgrupos "
     "corresponde igualmente a la publicación de resultados."),
    (r"\[PENDIENTE: confirmar con la Dirección Nacional de Investigación[^\]]*\]",
     "Trabajo adscrito a la convocatoria interna CUN 2026, Fase II. Sin financiación externa."),
    (r"\[PENDIENTE: declarar según taxonomía CRediT[^\]]*\]",
     "Conceptualización, metodología, redacción del borrador original y redacción con revisión y "
     "edición: el autor único firmante."),
    (r"\[PENDIENTE: URL del repositorio público[^\]]*\]",
     "La URL del repositorio y el identificador persistente del conjunto sintético se publicarán "
     "junto con los resultados."),
]
for patron, texto in CAMBIOS:
    a, n = re.subn(patron, texto, a, flags=re.S)
    if not n:
        print("  AVISO: no casó ->", patron[:62])

# ── 4 · fuera la nota interna de estado ───────────────────────────────────────
a = re.sub(r">\s*\*\*Nota de estado del manuscrito.*?(?=\n#{2,3}\s|\n\*\*|\Z)", "", a, flags=re.S)

DESTINO.write_text(a, encoding="utf-8")
resta = re.findall(r"\[(?:PENDIENTE|POR VERIFICAR|POR COMPLETAR)[^\]]*\]", a, re.S)
print("Escrito %s" % DESTINO.name)
print("  palabras: %d" % len(re.findall(r"[A-Za-zÁÉÍÓÚÑáéíóúñ][\wÁÉÍÓÚÑáéíóúñ'-]*", a)))
print("  marcadores que quedan: %d" % len(resta))
for r in resta[:6]:
    print("     ·", " ".join(r.split())[:120])
