---
name: transcribir-video
description: >
  Transcribe videos o audios EXISTENTES (MP4, MKV, MOV, MP3, M4A, WAV…) a texto y
  subtítulos — genera .txt (transcripción) + .srt y .vtt (subtítulos sincronizados).
  Corre LOCAL y OFFLINE (no sube nada a internet, sin costo) usando ffmpeg + faster-whisper
  (Whisper). Español por defecto. Úsalo cuando el usuario pida transcribir, subtitular o
  sacar el texto de un video/audio, o generar subtítulos para un reproductor/LMS/examlab/YouTube.
---

# Transcribir video / audio (local, offline)

Convierte cualquier video o audio existente en **transcripción de texto** y **subtítulos**.

- **Motor:** `ffmpeg` (extrae el audio) + **faster-whisper** (Whisper, en CPU). Todo local; no sube el archivo a ningún servicio.
- **Salidas** (por cada entrada, junto al archivo original salvo `--outdir`): `<nombre>.txt`, `<nombre>.srt`, `<nombre>.vtt`.
- **Idioma por defecto:** español (`--lang es`; usa `--lang auto` para detectarlo).
- **Modelo por defecto:** `large-v3` (máxima calidad; en CPU es lento — puede tardar tanto o más que la duración del video). Para borradores rápidos usa `--model medium` o `--model small`.

## Cómo ejecutarlo

Un archivo:
```
python ".claude/skills/transcribir-video/transcribir.py" "ruta/al/video.mp4"
```

Una carpeta completa (procesa todos los videos/audios que encuentre):
```
python ".claude/skills/transcribir-video/transcribir.py" "Manuales"
```

Opciones útiles:
```
--model    tiny|base|small|medium|large-v3     (def: large-v3)
--lang     es | en | auto | …                  (def: es)
--formats  txt,srt,vtt                          (def: txt,srt,vtt)
--outdir   carpeta de salida                    (def: junto a cada archivo)
--device   cpu|cuda   --compute  int8|float16   (def: cpu / int8)
```

Ejemplo (subtítulos rápidos en una carpeta de salida):
```
python ".claude/skills/transcribir-video/transcribir.py" "clase.mp4" --model medium --formats srt,vtt --outdir "Subtitulos"
```

## Notas para el asistente

- **Requisitos:** `ffmpeg` en el PATH (ya instalado) y `pip install faster-whisper` (ya instalado). Si falta, instálalo.
- **Primera ejecución:** faster-whisper **descarga el modelo** desde Hugging Face al cache (`large-v3` ≈ 3 GB; `medium` ≈ 1.5 GB). Solo la primera vez. Avísale al usuario si el modelo aún no está en cache.
- **Duración en CPU:** `large-v3` es lento sin GPU. Para videos largos, corre el comando **en segundo plano** (`run_in_background`) o sugiere `medium`. El script imprime cada segmento a medida que sale, así se ve el progreso.
- **Verificación:** para probar sin esperar un video completo, corta un clip corto con ffmpeg
  (`ffmpeg -y -i entrada.mp4 -t 60 -c copy clip.mp4`) y transcribe el clip.
- **Formatos de salida:** `.srt`/`.vtt` sirven para reproductores, YouTube y para cargar subtítulos en el LMS; `.txt` para editar, resumir o generar material.
- El script acepta archivos sueltos o una **carpeta** (procesa todos los medios: mp4, mkv, mov, avi, webm, m4a, mp3, wav, …).
