# -*- coding: utf-8 -*-
"""
Genera los 7 decks .pptx del curso ADMINISTRACIÓN DE SISTEMAS OPERATIVOS DE SERVIDOR
(presentación + 6 sesiones). Identidad Nueva América (motor fesna_slides_engine).

Reglas nuevas aplicadas:
- Las diapositivas de sesión NO incluyen la slide "Recordemos la asignatura".
- Todas las clases duran lo mismo (105 min).
- Práctica en terminales de servidor EN LÍNEA (JSLinux/Webminal/DistroSea) + terminal nativa;
  entregables/diagramas/ruta en examlab. Nada se instala. (Curso tipo D — Coursera.)

Referencia: curso interno 'Sistemas Operativos' (FESNA) adaptado a servidor.
Config: config/cursos/administracion-sistemas-operativos-servidor.json
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fesna_slides_engine import *

# --- Contenido ampliado por sesión, desde config/slides/content/<slug>_s<N>.json ---
CONTENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")
COURSE_SLUG = "servidor"

# --- Diapositivas MIXTAS: algunas slides llevan un diagrama de concepto (imagen+texto),
#     otras quedan solo texto. Mapa título→id del catálogo (config/slides/diagramas.py). ---
DIAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "diagramas")
IMG = [
    ("pantalla negra", "servidor_clientes"),
    ("Administración remota", "ssh_remoto"),
    ("tríada por tríada", "permisos_lsl"),
    ("elevar privilegios", "privilegios_escalera"),
    ("la tienda oficial", "repo_flujo"),
    ("confunde a todos", "update_upgrade"),
    ("El recorrido del almacenamiento", "storage_recorrido"),
    ("LVM", "lvm"),
    ("Qué es un proceso", "arbol_procesos"),
    ("SIGTERM vs", "sigterm_sigkill"),
    ("Automatizar con cron", "cron_campos"),
    ("Respaldar", "backup_321"),
    ("método de troubleshooting", "troubleshooting_pasos"),
]

def img_for(title):
    tl = (title or "").lower()
    for sub, did in IMG:
        if sub.lower() in tl:
            p = os.path.join(DIAG_DIR, did + ".png")
            return p if os.path.exists(p) else None
    return None

def load_content(n):
    p = os.path.join(CONTENT_DIR, f"{COURSE_SLUG}_s{n}.json")
    if not os.path.exists(p):
        return None
    try:
        data = json.load(open(p, encoding="utf-8"))
    except Exception:
        return None
    out = []
    for sl in (data or []):
        if not isinstance(sl, dict) or not sl.get("title"):
            continue
        if sl.get("type") == "table" and sl.get("headers") and sl.get("rows"):
            extra = {}
            if sl.get("note"):
                extra["note"] = sl["note"]
            if sl.get("col_w"):
                extra["col_w"] = sl["col_w"]
            out.append(("table", sl["title"], sl["headers"], sl["rows"], extra))
        else:
            items = []
            for b in sl.get("bullets", []):
                if not isinstance(b, str):
                    continue
                lvl = 1 if (len(b) - len(b.lstrip())) >= 2 else 0
                items.append((b.strip(), lvl))
            if items:
                out.append(("bullets", sl["title"], items))
    return out or None

BASE = r"g:\Mi unidad\Trabajos\Empleo\FESNA\Cursos\Administración de Sistemas Operativos de Servidor\Clases"
CURSO = "Administración de Sistemas Operativos de Servidor"
CURSO_CORTO = "Administración de SO de Servidor"
PROGRAMA = "Ingeniería de Sistemas"

TUTOR = ("Julian Andrés Castaño Espinosa",
         ["Líder Técnico", "Ingeniero de Sistemas", "Candidato a MsC en IA"],
         "julian.castano@lanuevaamerica.edu.co")

OBJETIVOS_CURSO = [
    "Operar y administrar un servidor por consola (Linux y Windows Server): sistema de archivos, usuarios y permisos.",
    "Configurar y mantener el servidor: software y servicios, almacenamiento, procesos y tareas programadas.",
    "Evaluar el estado del servidor y diagnosticar problemas con red, logs y respaldos, aplicando buenas prácticas de seguridad.",
]

# --- Evaluación tipo D (Coursera) — heredada del curso de referencia ---
EVAL_ROWS = [
    ["**Progreso del curso en Coursera**", "@@90%@@"],
    ["**Asistencia** — al final de la sesión", "@@10%@@"],
    ["**Total**", "**100%**"],
]
EVAL_NOTE = ("Participación en clase **+0.3** (opcional)  ·  "
             "Kahoot: 🥇 **+0.5** · 🥈 **+0.4** · 🥉 **+0.3** (opcional)")

AGENDA_ROWS = [
    ["**Motivación y encuadre**", "15 min", "Pregunta gancho, objetivos y acuerdos de la clase"],
    ["**Enunciación**", "25 min", "Explicación de los conceptos de hoy"],
    ["**Modelación**", "25 min", "Comandos guiados por el docente en la terminal"],
    ["**Ejercitación y simulación**", "25 min", "Práctica en terminales en línea y examlab"],
    ["**Cierre**", "10 min", "Resumen, dudas y conexión con la próxima clase"],
    ["**Actividad individual**", "@@15 min@@", "Trabajo autónomo (entregable en examlab)"],
]

NIVELES = {1: "Nivel 1 — Identificar", 2: "Nivel 2 — Analizar", 3: "Nivel 3 — Evaluar"}


def std_proposito(prs, foco, nivel):
    items = ["**El propósito de la tutoría de hoy es:**", (foco, 1), "Niveles de logro de la asignatura:"]
    for n in (1, 2, 3):
        txt = NIVELES[n]
        items.append((f"@@{txt}  ←  hoy@@" if n == nivel else txt, 1))
    content_slide(prs, "El propósito de hoy", items, size=16, idx=2)

def std_autonomo(prs, items, idx):
    content_slide(prs, "Trabajo autónomo (15 min)", items, size=15, idx=idx)

def std_logros(prs, items, idx):
    content_slide(prs, "¿Qué logramos hoy?", items + [
        "Chequea tu saber con el **quiz de la sesión en examlab (Test)**; los comandos se practican en un **terminal en línea**.",
    ], size=15, idx=idx)


# ============================== SESIONES ==============================
SESIONES = {
 1: dict(
    titulo="Administración por Consola del Servidor",
    subtitulo="CLI vs GUI, jerarquía de archivos y administración remota",
    archivo="Sesion 1 - Administracion por Consola del Servidor",
    nivel=1, gancho="¡Bienvenido a la consola!",
    foco="Operar el servidor por consola: por qué la CLI manda, la jerarquía del sistema de archivos, navegar y manipular archivos, y el acceso remoto (SSH / PowerShell Remoting).",
    contenido=[
        ("tabla", "CLI vs GUI en servidores", ["Aspecto", "GUI", "CLI (servidores)"], [
            ["Consumo de recursos", "Alto", "@@Mínimo@@"],
            ["Automatización", "Difícil", "Scripts repetibles"],
            ["Acceso remoto", "Pesado", "Ligero (SSH)"],
            ["Reproducibilidad", "Manual, clic a clic", "Comandos versionables"],
        ], dict(col_w=[3.4, 4.3, 4.3], note="La mayoría de servidores corren **sin interfaz gráfica (headless)**: la consola no es opcional.")),
        ("bullets", "La jerarquía del sistema de archivos", [
            "**Linux (FHS):** todo cuelga de la raíz `/`.",
            ("`/etc` configuración · `/var` datos y **logs** · `/home` usuarios · `/bin` `/usr` programas · `/tmp` temporales · `/dev` dispositivos", 1),
            "**Windows:** unidades con letra — `C:\\Windows`, `C:\\Program Files`, `C:\\Users`.",
            "En Linux, @@todo es un archivo@@ (incluso los discos y dispositivos viven en `/dev`).",
        ]),
        ("tabla", "Navegar y manipular archivos", ["Acción", "Linux", "Windows / PowerShell"], [
            ["Listar", "`ls -l`", "`dir` · `Get-ChildItem`"],
            ["Cambiar de carpeta", "`cd`", "`cd`"],
            ["Dónde estoy", "`pwd`", "`Get-Location`"],
            ["Crear carpeta", "`mkdir`", "`mkdir`"],
            ["Copiar", "`cp`", "`copy` · `Copy-Item`"],
            ["Mover / renombrar", "`mv`", "`move` · `Move-Item`"],
            ["Borrar", "`rm`", "`del` · `Remove-Item`"],
        ], dict(col_w=[3.2, 3.4, 5.4], fs_body=12)),
        ("bullets", "Administración remota", [
            "**SSH** (Linux): `ssh usuario@servidor` — puerto 22, cifrado. Preferir **llaves** sobre contraseña.",
            "**Windows Server:** RDP y **PowerShell Remoting** (`Enter-PSSession servidor`).",
            "Nunca administres un servidor de producción sentado frente a él: se hace @@en remoto y seguro@@.",
            "Buena práctica: deshabilitar el acceso directo de **root** por SSH.",
        ]),
    ],
    autonomo=[
        "En **JSLinux** o **Webminal** (terminal en línea): ubícate con `pwd`, recorre `/`, entra a `/etc` y a `/var/log` y lista con `ls -l`.",
        "Crea la estructura `~/practica/dia1`, copia un archivo dentro y renómbralo (`cp`, `mv`).",
        ("Captura `pwd` + `ls -l` mostrando el resultado.", 1),
        "En la **pizarra de examlab** dibuja la jerarquía `/` con 4 carpetas y para qué sirve cada una. Sube todo a **examlab**.",
    ],
    logros=[
        "Entendimos por qué en servidores manda la **CLI**.",
        "Reconocimos la **jerarquía del sistema de archivos** (Linux y Windows).",
        "Navegamos y manipulamos archivos por consola.",
        "Vimos cómo se administra un servidor **en remoto** (SSH / PowerShell Remoting).",
    ],
    cierre=("¡Nos vemos en la Sesión 2!",
            ["Próxima sesión: **Usuarios, Grupos y Permisos del Servidor**.",
             "Avanza tu ruta en Coursera y sube la actividad a **examlab**."],
            "Ya entraste a la consola… ¡ahora controla quién más entra!"),
 ),

 2: dict(
    titulo="Usuarios, Grupos y Permisos del Servidor",
    subtitulo="Seguridad y control de acceso: sudo, grupos y ACLs",
    archivo="Sesion 2 - Usuarios Grupos y Permisos del Servidor",
    nivel=1, gancho="¿Quién puede hacer qué?",
    foco="Controlar el acceso: usuarios y grupos, el modelo de permisos rwx/octal en Linux, sudo, y permisos NTFS en Windows Server, bajo el principio de mínimo privilegio.",
    contenido=[
        ("bullets", "Usuarios y grupos", [
            "Cada persona/servicio es un **usuario**; los **grupos** juntan usuarios con permisos comunes.",
            "Linux: `/etc/passwd` (usuarios) y `/etc/group`; `useradd`, `usermod -aG grupo usuario`, `userdel`.",
            "Windows: `net user`, grupos locales; **Administrador** ≈ **root**.",
            "El **superusuario** (root/Administrator) puede TODO: úsalo lo mínimo posible.",
        ]),
        ("tabla", "Permisos rwx y octales", ["Permiso", "Valor", "Significado"], [
            ["**r** (leer)", "4", "Ver el contenido"],
            ["**w** (escribir)", "2", "Modificar"],
            ["**x** (ejecutar)", "1", "Correr / entrar a la carpeta"],
            ["Ejemplo `rw-r--r--`", "**644**", "Dueño rw · grupo r · otros r"],
            ["Ejemplo `rwxr-x---`", "**750**", "Dueño rwx · grupo r-x · otros nada"],
        ], dict(col_w=[4.0, 2.4, 5.6], note="Se leen en **3 tríadas**: dueño / grupo / otros. Se suman los valores (4+2+1).")),
        ("bullets", "chmod, chown y sudo", [
            "`chmod 640 archivo` (numérico) o `chmod u+x script.sh` (simbólico).",
            "`chown usuario:grupo archivo` cambia el dueño y el grupo.",
            "**sudo**: ejecutar un comando como root de forma puntual (`sudo apt update`); se configura en `/etc/sudoers`.",
            "sudo @@deja rastro en los logs@@ (auditable); iniciar sesión como root directo, no.",
        ]),
        ("bullets", "Windows NTFS y mínimo privilegio", [
            "Permisos **NTFS**: Control total · Modificar · Lectura y ejecución · Lectura · Escritura, con **herencia** de carpetas.",
            "Grupos clave: **Administradores**, **Usuarios**; se asignan permisos al grupo, no persona por persona.",
            "**Principio de mínimo privilegio:** cada quien recibe SOLO lo que necesita para su tarea.",
            "@@Nunca trabajes a diario como Administrador/root.@@",
        ]),
    ],
    autonomo=[
        "En un terminal Linux en línea (Webminal/JSLinux): crea el grupo `proyecto` y el usuario `ana`, y agrega `ana` al grupo.",
        "Crea `informe.txt`, asígnale permisos **640** y verifica con `ls -l`.",
        ("Explica en una frase por qué 640 es adecuado para un archivo confidencial compartido con el grupo.", 1),
        "Sube capturas + tu explicación a **examlab**.",
    ],
    logros=[
        "Creamos y administramos **usuarios y grupos**.",
        "Leímos y asignamos **permisos rwx / octales** con chmod/chown.",
        "Entendimos **sudo** y por qué es preferible a usar root.",
        "Aplicamos el **mínimo privilegio** (Linux y NTFS).",
    ],
    cierre=("¡Nos vemos en la Sesión 3!",
            ["Próxima sesión: **Gestión de Software y Servicios**.",
             "Avanza tu ruta en Coursera y sube la actividad a **examlab**."],
            "Ya controlas el acceso… ¡ahora instala y enciende servicios!"),
 ),

 3: dict(
    titulo="Gestión de Software y Servicios",
    subtitulo="Paquetes, repositorios y servicios (systemd / servicios de Windows)",
    archivo="Sesion 3 - Gestion de Software y Servicios",
    nivel=2, gancho="¡Instala, actualiza, enciende!",
    foco="Mantener el servidor: gestores de paquetes y repositorios (apt/dnf/winget) y administración de servicios/daemons con systemd y el gestor de servicios de Windows.",
    contenido=[
        ("tabla", "Gestores de paquetes", ["Sistema", "Gestor", "Instalar"], [
            ["Debian / Ubuntu", "**apt**", "`apt install <paquete>`"],
            ["RHEL / Fedora", "**dnf**", "`dnf install <paquete>`"],
            ["Windows", "**winget**", "`winget install <app>`"],
        ], dict(col_w=[4.0, 3.0, 5.0], note="El software viene de **repositorios firmados**: no descargues binarios sueltos de sitios dudosos.")),
        ("bullets", "Ciclo de vida del software", [
            "**Actualizar el índice** de paquetes: `apt update`.",
            "**Instalar**: `apt install nginx` · **Buscar**: `apt search <texto>`.",
            "**Actualizar el sistema**: `apt upgrade` · **Remover**: `apt remove` / `purge`.",
            "Un servidor **actualizado** cierra vulnerabilidades: parchar es parte de la seguridad.",
        ]),
        ("tabla", "Servicios: systemd vs Windows", ["Acción", "Linux (systemctl)", "Windows"], [
            ["Iniciar", "`systemctl start sshd`", "`Start-Service`"],
            ["Detener", "`systemctl stop sshd`", "`Stop-Service`"],
            ["Ver estado", "`systemctl status sshd`", "`Get-Service`"],
            ["Habilitar al arranque", "`systemctl enable sshd`", "`Set-Service -StartupType Automatic`"],
        ], dict(col_w=[3.6, 4.6, 3.8], fs_body=12)),
        ("bullets", "Daemons y servicios", [
            "Un **servicio (daemon)** corre en segundo plano: `sshd`, `nginx`, `cron`…",
            "`systemctl status <servicio>` muestra si está **activo/inactivo** y sus últimos logs.",
            "@@Habilitar (enable) ≠ iniciar (start):@@ *enable* hace que arranque solo al bootear; *start* lo enciende ahora.",
            "En Windows, el equivalente es el panel **Servicios** (services.msc) o `Get-Service`.",
        ]),
    ],
    autonomo=[
        "En un terminal Linux en línea: `apt update` y luego instala una utilidad ligera (p. ej. `tree` o `nano`); verifica que quedó instalada.",
        "Consulta el estado de un servicio con `systemctl status cron` (o `ssh`).",
        ("Explica la diferencia entre `start` y `enable` con tus palabras.", 1),
        "Sube capturas + tu explicación a **examlab**.",
    ],
    logros=[
        "Instalamos y mantuvimos software desde **repositorios**.",
        "Distinguimos **apt/dnf/winget**.",
        "Administramos **servicios** con systemd y en Windows.",
        "Entendimos la diferencia entre **iniciar** y **habilitar** un servicio.",
    ],
    cierre=("¡Nos vemos en la Sesión 4!",
            ["Próxima sesión: **Almacenamiento del Servidor**.",
             "Avanza tu ruta en Coursera y sube la actividad a **examlab**."],
            "Ya tienes servicios corriendo… ¿y dónde guardan sus datos?"),
 ),

 4: dict(
    titulo="Almacenamiento del Servidor",
    subtitulo="Sistemas de archivos, particiones y discos (LVM/RAID, montaje y cuotas)",
    archivo="Sesion 4 - Almacenamiento del Servidor",
    nivel=2, gancho="¿Dónde viven los datos?",
    foco="Administrar el almacenamiento: sistemas de archivos, particionado y montaje, volúmenes lógicos LVM y nociones de RAID, y el monitoreo del espacio en disco.",
    contenido=[
        ("tabla", "Sistemas de archivos", ["FS", "Uso típico", "Nota"], [
            ["**ext4**", "Linux, propósito general", "Estable y por defecto"],
            ["**xfs**", "Linux, volúmenes grandes", "Rendimiento en servidores"],
            ["**NTFS**", "Windows Server", "Permisos y journaling"],
            ["**exFAT/vfat**", "Intercambio / USB", "Sin permisos Linux"],
        ], dict(col_w=[3.0, 4.8, 4.2])),
        ("bullets", "Discos, particiones y montaje", [
            "Ver discos y particiones: `lsblk`, `fdisk -l`.",
            "Una partición se **formatea** (`mkfs.ext4 /dev/sdb1`) y luego se **monta** en un directorio: `mount /dev/sdb1 /datos`.",
            "Para que el montaje **persista** al reiniciar, se declara en `/etc/fstab`.",
            "Windows: **Administrador de discos** asigna letras (D:, E:) a las particiones.",
        ]),
        ("bullets", "LVM y RAID (nociones)", [
            "**LVM**: volúmenes lógicos que se **agrandan sin reparticionar** (PV → VG → LV).",
            "**RAID**: varios discos combinados — **RAID1** (espejo, redundancia), **RAID5** (paridad), **RAID0** (velocidad, sin respaldo).",
            "En servidores casi nunca se usa el disco 'crudo': se usa @@LVM y/o RAID@@ para crecer y no perder datos.",
        ]),
        ("tabla", "Monitorear el espacio", ["Comando", "Qué muestra"], [
            ["`df -h`", "Espacio libre/usado por sistema de archivos"],
            ["`du -sh *`", "Tamaño de cada carpeta"],
            ["`lsblk`", "Discos, particiones y puntos de montaje"],
        ], dict(col_w=[3.2, 8.8], note="Un disco lleno **tumba servicios**: vigila `/` y sobre todo `/var` (logs).")),
    ],
    autonomo=[
        "En un terminal Linux en línea: ejecuta `df -h` e identifica qué sistema de archivos monta `/` y cuánto espacio le queda.",
        "Ejecuta `du -sh /var/*` y di cuál carpeta pesa más.",
        ("Explica con tus palabras la diferencia entre **partición** y **punto de montaje**.", 1),
        "Sube capturas + tu explicación a **examlab**.",
    ],
    logros=[
        "Reconocimos los **sistemas de archivos** (ext4/xfs/NTFS).",
        "Entendimos **particionar y montar** (incl. `/etc/fstab`).",
        "Conocimos **LVM y RAID** y para qué sirven.",
        "Monitoreamos el **espacio en disco** (df/du).",
    ],
    cierre=("¡Nos vemos en la Sesión 5!",
            ["Próxima sesión: **Procesos, Recursos y Tareas Programadas**.",
             "Avanza tu ruta en Coursera y sube la actividad a **examlab**."],
            "Ya guardas los datos… ¡ahora vigila lo que corre en el servidor!"),
 ),

 5: dict(
    titulo="Procesos, Recursos y Tareas Programadas",
    subtitulo="Monitoreo del servidor y automatización (cron / Programador de tareas)",
    archivo="Sesion 5 - Procesos Recursos y Tareas Programadas",
    nivel=3, gancho="¿Qué está corriendo ahora?",
    foco="Vigilar y controlar la carga del servidor: procesos y señales, uso de CPU y memoria, prioridades, y automatización de tareas con cron y el Programador de tareas.",
    contenido=[
        ("bullets", "Procesos", [
            "Cada programa en ejecución es un **proceso** con un **PID** (identificador).",
            "Verlos: `ps aux` (lista completa) y `top` / `htop` (en **tiempo real**).",
            "Estados: en ejecución, durmiendo, **zombie** (terminó pero su padre no lo recogió).",
            "Los procesos forman un árbol **padre → hijo**.",
        ]),
        ("tabla", "Señales y control", ["Comando", "Efecto"], [
            ["`kill PID`", "Pide terminar ordenadamente (SIGTERM)"],
            ["`kill -9 PID`", "Fuerza el cierre (SIGKILL) — último recurso"],
            ["`nice` / `renice`", "Cambia la prioridad del proceso"],
            ["`Ctrl + C`", "Interrumpe el proceso en primer plano"],
        ], dict(col_w=[3.4, 8.6], note="Prefiere **SIGTERM**; usa `-9` solo si el proceso no responde.")),
        ("bullets", "Recursos del servidor", [
            "**Carga (load average):** `uptime` — si supera el nº de núcleos, el servidor está saturado.",
            "**Memoria:** `free -h` — vigila la RAM libre y el uso de swap.",
            "**Windows:** Administrador de tareas o `Get-Process` / `Get-Counter`.",
            "Monitorear a tiempo evita que el servidor se @@caiga por saturación@@.",
        ]),
        ("bullets", "Automatización de tareas", [
            "**cron** (Linux): `crontab -e`; formato `min hora día mes díasem comando`.",
            ("Ejemplo — respaldo diario a las 2:00 am: `0 2 * * * /opt/backup.sh`", 1),
            "Alternativa moderna: **systemd timers**.",
            "**Windows:** Programador de tareas (Task Scheduler).",
            "Automatiza lo repetitivo: **respaldos**, limpieza de logs, reinicios de servicios.",
        ]),
    ],
    autonomo=[
        "En un terminal Linux en línea: con `ps aux` o `top`, identifica el proceso que más CPU o memoria usa.",
        "Lanza un proceso (p. ej. `sleep 300 &`), encuéntralo por su PID y termínalo con `kill`.",
        ("Escribe una línea de **cron** que ejecute un comando todos los días a las 6:00 am y explica sus 5 campos.", 1),
        "Sube capturas + la línea de cron comentada a **examlab**.",
    ],
    logros=[
        "Listamos y entendimos los **procesos** (PID, estados, árbol).",
        "Controlamos procesos con **señales** (kill/SIGTERM/SIGKILL).",
        "Monitoreamos **CPU, memoria y carga**.",
        "Automatizamos tareas con **cron / Programador de tareas**.",
    ],
    cierre=("¡Nos vemos en la Sesión 6!",
            ["Última sesión: **Redes, Logs, Respaldos y Troubleshooting**.",
             "Avanza tu ruta en Coursera y sube la actividad a **examlab**."],
            "Ya vigilas el servidor… ¡ahora aprende a repararlo!"),
 ),

 6: dict(
    titulo="Redes, Logs, Respaldos y Troubleshooting",
    subtitulo="El detective digital: diagnóstico, seguridad y disponibilidad del servidor",
    archivo="Sesion 6 - Redes Logs Respaldos y Troubleshooting",
    nivel=3, gancho="¡Modo detective digital!",
    foco="Diagnosticar y sostener el servidor: red (ip/ping/ss), lectura de logs (journalctl / Visor de eventos), respaldos, firewall y hardening básico, y un método ordenado de troubleshooting.",
    contenido=[
        ("tabla", "Red del servidor", ["Comando", "Qué hace"], [
            ["`ip a` / `ipconfig`", "Ver interfaces e IPs del servidor"],
            ["`ping <host>`", "Comprobar si se alcanza un host"],
            ["`ss -tlnp` / `netstat`", "Ver puertos en escucha y quién los abre"],
            ["`curl` / `Test-NetConnection`", "Probar si un servicio responde"],
        ], dict(col_w=[4.2, 7.8], fs_body=12)),
        ("bullets", "Logs: la memoria del servidor", [
            "**Linux:** `journalctl -u sshd` (por servicio), `journalctl -xe` (errores recientes); archivos en `/var/log/` (`syslog`, `auth.log`).",
            "**Windows Server:** **Visor de eventos** (Application / System / Security).",
            "Cuando algo falla, el log dice **qué** y **cuándo**.",
            "@@Regla de oro:@@ ante un problema, mira los **logs PRIMERO**.",
        ]),
        ("bullets", "Respaldos y hardening", [
            "**Respaldos:** `tar czf backup.tgz /etc`, `rsync -a origen/ destino/`; regla **3-2-1** (3 copias, 2 medios, 1 fuera de sitio).",
            "**Firewall:** `ufw` / `firewalld` (Linux), Firewall de Windows Defender — cierra puertos que no uses.",
            "**Hardening mínimo:** actualizar, SSH con llaves, mínimo privilegio, quitar servicios innecesarios.",
            "Un servidor **sin respaldo** es un accidente esperando a ocurrir.",
        ]),
        ("bullets", "Método de troubleshooting", [
            "1. **Reproduce** y describe el síntoma exacto.",
            "2. **Mira los logs** de la app/servicio implicado.",
            "3. **Aísla la capa**: ¿aplicación, servicio, red o disco?",
            "4. Cambia **una sola cosa a la vez** y prueba.",
            "5. **Verifica** que se resolvió y **documenta** qué pasó.",
            "@@El detective digital: evidencia antes que corazonadas.@@",
        ]),
    ],
    autonomo=[
        "Diagnóstico guiado en un terminal en línea:",
        ("1. `ip a` (tus interfaces) y `ping` a un host conocido.", 1),
        ("2. `ss -tlnp` — ¿qué puertos están en escucha?", 1),
        ("3. Lee un log con `journalctl -xe` o `/var/log/syslog` y resume el último evento.", 1),
        ("4. Propón un comando `tar` para respaldar `/etc`.", 1),
        "Aplica el **método de troubleshooting** a este caso: *\"el servicio web no responde\"* (escribe los 5 pasos). Sube todo a **examlab**.",
    ],
    logros=[
        "Inspeccionamos la **red del servidor** (ip/ping/ss).",
        "Leímos **logs** (journalctl / Visor de eventos).",
        "Aplicamos **respaldos, firewall y hardening** básicos.",
        "Usamos un **método ordenado de troubleshooting**.",
        "@@¡Completamos las 6 sesiones del curso!@@",
    ],
    cierre=("¡Gracias por llegar hasta aquí!",
            ["Termina tu **ruta en Coursera** dentro del plazo de licencias y responde la **encuesta de satisfacción**.",
             "Recorrimos la administración del servidor: de la consola a la red, los logs y los respaldos."],
            "De la terminal al servidor en producción: ¡ya piensas como administrador de sistemas!"),
 ),
}


# ============================== BUILDERS ==============================
def build_presentacion():
    set_footer(CURSO)
    prs = new_prs()
    course_cover(prs, CURSO_CORTO, None, "¡Bienvenidos estudiantes!",
        [PROGRAMA, "Cuatrimestre No. [N]", "Duración: **6 clases** (105 min c/u)",
         "Horario: Martes y Jueves 8:00–9:45 PM · Sábado 10:00–11:45 AM",
         "Fechas: 13/07/2026 – 25/07/2026"],
        "Empezamos a las 8:00 PM (sáb. 10:00 AM)…")
    tutor_slide(prs, TUTOR[0], TUTOR[1], TUTOR[2], idx=2)
    content_slide(prs, "METODOLOGÍA", [
        "**Sesiones teórico-prácticas**: cada clase combina teoría, modelación y práctica en la terminal.",
        "Momentos por clase:",
        ("**Motivación**: preguntas y ejemplos que generan interés y conexión.", 1),
        ("**Encuadre**: explicación de objetivos, ruta de aprendizaje y acuerdos.", 1),
        ("**Modelación**: comandos guiados que muestran conceptos y técnicas.", 1),
        ("**Simulación**: trabajo en grupos pequeños para aplicar conceptos.", 1),
        ("**Ejercitación**: práctica individual en terminales en línea y examlab.", 1),
        ("**Cierre**: retroalimentación, resumen y conexión con objetivos.", 1),
        ("**Evaluación**: progreso en Coursera + participación en clase.", 1),
    ], idx=3)
    objectives_slide(prs, "Objetivos", OBJETIVOS_CURSO, idx=4)
    table_content(prs, "¿Cómo se evalúa?", ["Componente", "Ponderación"], EVAL_ROWS,
                  col_w=[9.2, 2.8], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER], idx=5, note=EVAL_NOTE)
    content_slide(prs, "EJEMPLO DE EVALUACIÓN", [
        "Escala de 0 a 5.0.",
        "Asistencia (10%): asistió → 5.0 × 0.10 = **0.5**",
        "Progreso Coursera (90%): completó el 80% → 4.0 × 0.90 = **3.6**",
        "Participación en clase: no participó → **0**",
        "Kahoot: quedó de primero → **+0.5**",
        "@@Nota final = 0.5 + 3.6 + 0 + 0.5 = 4.6@@",
    ], idx=6)
    content_slide(prs, "CONTENIDO", [
        f"**Sesión {n}** — {d['titulo']}." for n, d in SESIONES.items()
    ], idx=7)
    content_slide(prs, "RECURSOS", [
        "**Material de clases:** 🔗 [inserta aquí el hipervínculo] — guiones, diapositivas y material de apoyo.",
        "**Curso base (Coursera):** Administración de sistemas y servicios de infraestructura de TI — Google",
        ("https://www.coursera.org/learn/system-administration-it-infrastructure-services", 1),
        "Guías, videos y ruta de aprendizaje: en **examlab**.",
        ("https://examlab.lovable.app/app", 1),
    ], idx=8)
    content_slide(prs, "HERRAMIENTAS", [
        "**En examlab** (plataforma del curso · https://examlab.lovable.app/app):",
        ("Test (quizzes) · Lab editor de código (Python) · pizarra/diagramas.", 1),
        "**Solo online (gratuitas):**",
        ("JSLinux (bellard.org/jslinux) · Webminal · Copy.sh/v86 · DistroSea.", 1),
        "**En el mundo laboral** (lo que usarás en el trabajo):",
        ("Linux real (Ubuntu Server / RHEL) · Windows Server · SSH (OpenSSH/PuTTY) · PowerShell · systemd · VMs (VirtualBox/VMware).", 1),
    ], size=15, idx=9)
    content_slide(prs, "¡ IMPORTANTE !", [
        "Las **licencias de Coursera** están activas hasta el día hábil posterior a la finalización de la asignatura, a las **9:00 AM**.",
        "Las **notas** se envían para validación el siguiente día hábil tras finalizar el curso; hay **3 días** para reclamaciones por correo.",
        "No olvides responder la **encuesta de satisfacción** el último día del curso.",
    ], idx=10)
    image_slide(prs, "GESTORES", GESTORES_IMG, idx=11)
    out = os.path.join(BASE, "Presentacion del curso.pptx")
    prs.save(out)
    print("OK", out)


def build_sesion(n):
    d = SESIONES[n]
    set_footer(CURSO)
    prs = new_prs()
    # SIN slide "Recordemos la asignatura" NI "¿Cómo trabajaremos hoy?" (reglas del usuario)
    session_cover(prs, f"SESIÓN {n}", NIVELES[d["nivel"]], d["titulo"], d["subtitulo"],
                  d["gancho"],
                  [f"{CURSO_CORTO} · {PROGRAMA}", "Duración: **105 min** (1 h 45 min)"])
    std_proposito(prs, d["foco"], d["nivel"])
    contenido = load_content(n) or d["contenido"]   # contenido ampliado desde JSON si existe
    idx = 3
    for item in contenido:
        kind = item[0]
        if kind == "bullets":
            _, title, items = item
            img = img_for(title)
            if img:
                image_text_slide(prs, title, items, img, size=14, idx=idx)
            else:
                content_slide(prs, title, items, size=15, idx=idx)
        else:
            _, title, headers, rows, extra = item
            table_content(prs, title, headers, rows, idx=idx, **extra)
        idx += 1
    std_autonomo(prs, d["autonomo"], idx); idx += 1
    std_logros(prs, d["logros"], idx)
    big, lines, accent = d["cierre"]
    closing_slide(prs, big, lines, accent)
    folder = os.path.join(BASE, f"Sesion {n}")
    os.makedirs(folder, exist_ok=True)
    out = os.path.join(folder, d["archivo"] + ".pptx")
    prs.save(out)
    print("OK", out)


if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    build_presentacion()
    for n in SESIONES:
        build_sesion(n)
    print("LISTO: 7 decks generados (sin slide 'Recordemos').")
