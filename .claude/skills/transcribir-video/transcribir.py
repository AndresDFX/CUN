# -*- coding: utf-8 -*-
"""
Transcribe videos/audios LOCALMENTE (offline) a texto y subtítulos.

Pipeline:  ffmpeg (extrae audio 16 kHz mono)  ->  faster-whisper (Whisper)
Salidas por cada entrada:  <nombre>.txt  ·  <nombre>.srt  ·  <nombre>.vtt

Uso:
    python transcribir.py "ruta/al/video.mp4"
    python transcribir.py "ruta/a/carpeta"          # procesa todos los videos/audios
    python transcribir.py video.mp4 --model medium --lang es --formats txt,srt
    python transcribir.py video.mp4 --outdir "carpeta/salida"

Opciones:
    --model    tiny|base|small|medium|large-v3   (def: large-v3)
    --lang     código ISO (es, en, …) o 'auto'   (def: es)
    --device   cpu|cuda                          (def: cpu)
    --compute  int8|int8_float16|float16|float32  (def: int8)
    --formats  lista separada por comas de txt,srt,vtt   (def: txt,srt,vtt)
    --outdir   carpeta de salida (def: junto a cada archivo de entrada)

Requiere: ffmpeg en el PATH y `pip install faster-whisper`.
"""
import os, sys, argparse, subprocess, tempfile, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MEDIA_EXT = {".mp4", ".mkv", ".mov", ".avi", ".webm", ".m4v", ".flv",
             ".m4a", ".mp3", ".wav", ".aac", ".ogg", ".flac", ".wma"}


def fmt_ts(seconds, sep=","):
    """Segundos -> HH:MM:SS,mmm (SRT) o HH:MM:SS.mmm (VTT)."""
    if seconds < 0:
        seconds = 0
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def extract_audio(src, wav_path):
    """Extrae audio a WAV 16 kHz mono con ffmpeg."""
    cmd = ["ffmpeg", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
           "-f", "wav", wav_path]
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg falló:\n" + r.stderr.decode("utf-8", "replace")[-800:])
    return wav_path


def audio_duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                          "-of", "default=noprint_wrappers=1:nokey=1", path],
                         capture_output=True, text=True)
    try:
        return float(out.stdout.strip())
    except Exception:
        return 0.0


def split_audio(wav, td, chunk_secs):
    """Trocea un WAV en bloques de chunk_secs con ffmpeg (evita picos de RAM en audios
    largos: Whisper carga el espectrograma completo en memoria). Devuelve [(ruta, offset_s)]
    con offsets acumulados a partir de la duración REAL de cada bloque."""
    pat = os.path.join(td, "chunk_%04d.wav")
    r = subprocess.run(["ffmpeg", "-y", "-i", wav, "-f", "segment",
                        "-segment_time", str(chunk_secs), "-c", "copy", pat],
                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode != 0:
        raise RuntimeError("ffmpeg (segment) falló:\n" + r.stderr.decode("utf-8", "replace")[-800:])
    files = sorted(glob.glob(os.path.join(td, "chunk_*.wav")))
    out, off = [], 0.0
    for f in files:
        out.append((f, off))
        off += audio_duration(f)
    return out


def write_txt(path, segments):
    with open(path, "w", encoding="utf-8") as f:
        for seg in segments:
            t = seg["text"].strip()
            if t:
                f.write(t + "\n")


def write_srt(path, segments):
    with open(path, "w", encoding="utf-8") as f:
        n = 1
        for seg in segments:
            t = seg["text"].strip()
            if not t:
                continue
            f.write(f"{n}\n{fmt_ts(seg['start'], ',')} --> {fmt_ts(seg['end'], ',')}\n{t}\n\n")
            n += 1


def write_vtt(path, segments):
    with open(path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for seg in segments:
            t = seg["text"].strip()
            if not t:
                continue
            f.write(f"{fmt_ts(seg['start'], '.')} --> {fmt_ts(seg['end'], '.')}\n{t}\n\n")


def collect_inputs(path):
    if os.path.isdir(path):
        out = [os.path.join(path, f) for f in sorted(os.listdir(path))
               if os.path.splitext(f)[1].lower() in MEDIA_EXT]
        return out
    return [path]


def transcribe_one(model, src, outdir, formats, lang, chunk_secs=600):
    base = os.path.splitext(os.path.basename(src))[0]
    dest = outdir or os.path.dirname(os.path.abspath(src))
    os.makedirs(dest, exist_ok=True)
    print(f"\n=== {os.path.basename(src)} ===")
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "audio.wav")
        print("  · extrayendo audio (ffmpeg)…")
        extract_audio(src, wav)
        dur = audio_duration(wav)
        # Audios largos: trocear para no cargar el espectrograma completo en RAM.
        if chunk_secs and dur > chunk_secs:
            chunks = split_audio(wav, td, chunk_secs)
            print(f"  · duración {fmt_ts(dur, ':')} → {len(chunks)} bloques de ~{chunk_secs//60} min")
        else:
            chunks = [(wav, 0.0)]
        print("  · transcribiendo (faster-whisper)… (segmentos a medida que salen)")
        segments = []
        for ci, (cpath, off) in enumerate(chunks):
            if len(chunks) > 1:
                print(f"    — bloque {ci+1}/{len(chunks)} (desde {fmt_ts(off, ':')}) —")
            seg_iter, info = model.transcribe(
                cpath,
                language=None if lang == "auto" else lang,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
                beam_size=5,
            )
            for seg in seg_iter:
                s, e = seg.start + off, seg.end + off
                segments.append({"start": s, "end": e, "text": seg.text})
                print(f"    [{fmt_ts(s, ':')} → {fmt_ts(e, ':')}] {seg.text.strip()}")
    written = []
    if "txt" in formats:
        p = os.path.join(dest, base + ".txt"); write_txt(p, segments); written.append(p)
    if "srt" in formats:
        p = os.path.join(dest, base + ".srt"); write_srt(p, segments); written.append(p)
    if "vtt" in formats:
        p = os.path.join(dest, base + ".vtt"); write_vtt(p, segments); written.append(p)
    print("  ✓ generado:")
    for p in written:
        print("     -", p)
    return written


# ---- Modo PARALELO: varios workers, cada uno con su propio modelo (usa más RAM
#      y TODOS los núcleos → mucho más rápido en audios largos). ----
_WORKER = {}

def _init_worker(model, device, compute, threads, lang, beam):
    from faster_whisper import WhisperModel
    _WORKER["m"] = WhisperModel(model, device=device, compute_type=compute, cpu_threads=threads)
    _WORKER["lang"] = None if lang == "auto" else lang
    _WORKER["beam"] = beam

def _transcribe_chunk(task):
    cpath, off = task
    m = _WORKER["m"]
    seg_iter, _ = m.transcribe(cpath, language=_WORKER["lang"], vad_filter=True,
                               vad_parameters=dict(min_silence_duration_ms=500), beam_size=_WORKER["beam"])
    return [(s.start + off, s.end + off, s.text) for s in seg_iter]

def _has_outputs(src, outdir, formats):
    base = os.path.splitext(os.path.basename(src))[0]
    dest = outdir or os.path.dirname(os.path.abspath(src))
    return all(os.path.isfile(os.path.join(dest, base + "." + f)) for f in formats)

def _transcribe_file(task):
    """Worker de PARALELISMO POR SESIÓN: transcribe un archivo completo con el modelo del worker."""
    src, outdir, formats, lang, chunk_secs = task
    try:
        transcribe_one(_WORKER["m"], src, outdir, formats, lang, chunk_secs)
        return (os.path.basename(src), True, "")
    except Exception as e:
        return (os.path.basename(src), False, str(e)[:200])

def transcribe_parallel(src, outdir, formats, lang, chunk_secs, workers, model, device, compute, beam):
    from concurrent.futures import ProcessPoolExecutor
    base = os.path.splitext(os.path.basename(src))[0]
    dest = outdir or os.path.dirname(os.path.abspath(src))
    os.makedirs(dest, exist_ok=True)
    print(f"\n=== {os.path.basename(src)} (PARALELO: {workers} workers) ===")
    with tempfile.TemporaryDirectory() as td:
        wav = os.path.join(td, "audio.wav")
        print("  · extrayendo audio (ffmpeg)…")
        extract_audio(src, wav)
        dur = audio_duration(wav)
        chunks = split_audio(wav, td, chunk_secs) if (chunk_secs and dur > chunk_secs) else [(wav, 0.0)]
        threads = max(1, (os.cpu_count() or workers) // workers)
        print(f"  · duración {fmt_ts(dur, ':')} → {len(chunks)} bloques · {workers} workers × {threads} hilos c/u")
        segs = []
        with ProcessPoolExecutor(max_workers=workers, initializer=_init_worker,
                                 initargs=(model, device, compute, threads, lang, beam)) as ex:
            for i, res in enumerate(ex.map(_transcribe_chunk, chunks)):
                segs.extend(res)
                print(f"    ✓ bloque {i+1}/{len(chunks)} ({len(res)} segmentos)")
        segs.sort(key=lambda x: x[0])
        segments = [{"start": s, "end": e, "text": t} for s, e, t in segs]
    written = []
    if "txt" in formats:
        p = os.path.join(dest, base + ".txt"); write_txt(p, segments); written.append(p)
    if "srt" in formats:
        p = os.path.join(dest, base + ".srt"); write_srt(p, segments); written.append(p)
    if "vtt" in formats:
        p = os.path.join(dest, base + ".vtt"); write_vtt(p, segments); written.append(p)
    print("  ✓ generado:")
    for p in written:
        print("     -", p)
    return written


def main():
    ap = argparse.ArgumentParser(description="Transcribe videos/audios a texto y subtítulos (local, offline).")
    ap.add_argument("path", help="archivo de video/audio o carpeta")
    ap.add_argument("--model", default="large-v3")
    ap.add_argument("--lang", default="es")
    ap.add_argument("--device", default="cpu")
    ap.add_argument("--compute", default="int8")
    ap.add_argument("--formats", default="txt,srt,vtt")
    ap.add_argument("--outdir", default=None)
    ap.add_argument("--chunk", type=int, default=600,
                    help="segundos por bloque para audios largos (0 = sin trocear; def: 600)")
    ap.add_argument("--workers", type=int, default=1,
                    help="nº de procesos en paralelo (cada uno carga su modelo; usa más RAM y núcleos). def: 1")
    ap.add_argument("--beam", type=int, default=5, help="beam size (menor = más rápido). def: 5")
    ap.add_argument("--skip-existing", action="store_true",
                    help="salta los archivos que ya tienen sus salidas en el destino")
    args = ap.parse_args()

    formats = {x.strip().lower() for x in args.formats.split(",") if x.strip()}
    inputs = collect_inputs(args.path)
    if not inputs:
        print("No se encontraron videos/audios en:", args.path); sys.exit(1)
    if args.skip_existing:
        n0 = len(inputs)
        inputs = [s for s in inputs if not _has_outputs(s, args.outdir, formats)]
        print(f"skip-existing: {n0 - len(inputs)} ya transcrito(s), quedan {len(inputs)}")
        if not inputs:
            print("Nada por transcribir."); return

    # Modo PARALELO (varios workers) — no carga el modelo en el proceso principal.
    if args.workers and args.workers > 1:
        from concurrent.futures import ProcessPoolExecutor
        threads = max(1, (os.cpu_count() or args.workers) // args.workers)
        if len(inputs) > 1:
            # Paralelismo POR SESIÓN: varias sesiones a la vez (una por worker).
            nw = min(args.workers, len(inputs))
            print(f"Modo PARALELO por sesión: {nw} workers × {threads} hilos · modelo '{args.model}'")
            tasks = [(s, args.outdir, formats, args.lang, args.chunk) for s in inputs]
            ok = 0
            with ProcessPoolExecutor(max_workers=nw, initializer=_init_worker,
                                     initargs=(args.model, args.device, args.compute, threads, args.lang, args.beam)) as ex:
                for name, success, err in ex.map(_transcribe_file, tasks):
                    print(("  ✓ " if success else "  ✗ ") + name + ("" if success else f" — {err}"))
                    ok += 1 if success else 0
            print(f"\nListo: {ok}/{len(inputs)} sesión(es).")
        else:
            # Un solo archivo: paralelismo por BLOQUES.
            print(f"Modo PARALELO por bloques: {args.workers} workers · modelo '{args.model}'")
            ok = 0
            for src in inputs:
                try:
                    transcribe_parallel(src, args.outdir, formats, args.lang, args.chunk, args.workers,
                                        args.model, args.device, args.compute, args.beam)
                    ok += 1
                except Exception as e:
                    print(f"  ✗ ERROR con {os.path.basename(src)}: {e}")
            print(f"\nListo: {ok}/{len(inputs)} archivo(s).")
        return

    from faster_whisper import WhisperModel
    print(f"Cargando modelo '{args.model}' ({args.device}/{args.compute})…")
    print("  (la primera vez descarga el modelo desde Hugging Face; large-v3 ≈ 3 GB)")
    model = WhisperModel(args.model, device=args.device, compute_type=args.compute)

    ok = 0
    for src in inputs:
        try:
            transcribe_one(model, src, args.outdir, formats, args.lang, args.chunk)
            ok += 1
        except Exception as e:
            print(f"  ✗ ERROR con {os.path.basename(src)}: {e}")
    print(f"\nListo: {ok}/{len(inputs)} archivo(s) transcrito(s).")


if __name__ == "__main__":
    main()
