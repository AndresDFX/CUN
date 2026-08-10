# -*- coding: utf-8 -*-
"""
Genera los 7 decks .pptx del curso CABLEADO ESTRUCTURADO (6 sesiones + presentación).
Identidad gráfica mejorada (réplica del deck real de Internetworking):
foto lavada en portadas, objetivos con foto duotono azul + tarjeta blanca,
gestores con el flyer institucional real.

Temario: Coursera "Bits y Bytes de las redes informáticas" (Google), 6 módulos = 6 clases.
Config: config/cursos/cableado-estructurado.json
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fesna_slides_engine import *

# --- Contenido ampliado por sesión, cargado desde config/slides/content/<slug>_s<N>.json ---
# (generado por el workflow 'expandir-contenido-sesiones'; si falta, se usa el 'contenido' inline).
CONTENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")
COURSE_SLUG = "cableado"

# --- Diapositivas MIXTAS: algunas slides llevan un diagrama de concepto (imagen+texto),
#     otras quedan solo texto. Mapa título→id del catálogo (config/slides/diagramas.py). ---
DIAG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "diagramas")
IMG = [
    ("Todo se piensa por capas", "net_topologia"),
    ("Dos mapas", "stack_tcpip_osi"),
    ("capa física", "duplex"),
    ("32 bits, red y host", "ip_32bits"),
    ("muñecas rusas", "encapsulamiento"),
    ("Dividir en subredes", "subred_split"),
    ("tres vías", "handshake"),
    ("Estados de un socket", "socket_estados"),
    ("Todas las capas juntas", "stack_viaje"),
    ("Resolución de un nombre", "dns_resolucion"),
    ("arrendador", "dora"),
    ("recepcionista", "nat"),
    ("FTTX", "fttx"),
    ("Conectar sedes", "wan_vpn"),
    ("Canales 1, 6 y 11", "wifi_canales"),
    ("ICMP", "embudo"),
    ("dos reglas de compresión", "ipv6_compresion"),
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

BASE = r"g:\My Drive\Trabajos\Empleo\FESNA\Cursos\Cableado Estructurado\Clases"
CURSO = "Cableado Estructurado"
PROGRAMA = "Ingeniería de Sistemas"

TUTOR = ("Julian Andrés Castaño Espinosa",
         ["Líder Técnico", "Ingeniero de Sistemas", "Candidato a MsC en IA"],
         "julian.castano@lanuevaamerica.edu.co")

OBJETIVOS_CURSO = [
    "Identificar los componentes físicos y lógicos de una red: el modelo de cinco capas, los medios de transmisión, los dispositivos y el direccionamiento IP.",
    "Analizar cómo las capas, los servicios de red (DNS, DHCP, NAT, VPN) y las tecnologías de acceso llevan los datos de extremo a extremo.",
    "Diagnosticar y solucionar problemas de conectividad con herramientas estándar, evaluando también la nube y la transición a IPv6.",
]

EVAL_ROWS = [
    ["**Destreza** — entrenamientos en la ruta de aprendizaje (LMS)", "@@50%@@"],
    ["**Prueba de rendimiento** — LMS", "@@40%@@"],
    ["**Asistencia** — al final de la sesión", "@@10%@@"],
    ["**Total**", "**100%**"],
]
EVAL_OPCIONALES = [
    "Participación en clase = **+0.3** (opcional)",
    "Kahoot — bonificación por puesto (opcional): 🥇 1er **+0.5** · 🥈 2do **+0.4** · 🥉 3er **+0.3**",
]

RECORDAR = [
    "Objetivo del curso: **describir las redes en términos del modelo de cinco capas**, identificar los medios físicos del cableado estructurado y diagnosticar la conectividad de extremo a extremo.",
    "Competencia: comprender la **infraestructura física y lógica** de las redes para instalarlas, documentarlas y diagnosticarlas según los estándares del sector.",
    "El curso avanza por niveles: **Identificar → Analizar → Diagnosticar**; hoy trabajamos uno de ellos.",
    "Toda la práctica es en @@examlab@@ y con herramientas en línea — sin instalar nada.",
]

AGENDA_ROWS = [
    ["**Motivación y encuadre**", "15 min", "Pregunta gancho, objetivos y acuerdos de la clase"],
    ["**Enunciación**", "25 min", "Explicación de los conceptos de hoy"],
    ["**Modelación**", "25 min", "Ejemplos guiados por el docente"],
    ["**Ejercitación y simulación**", "25 min", "Práctica en examlab y herramientas en línea"],
    ["**Cierre**", "10 min", "Resumen, dudas y conexión con la próxima clase"],
    ["**Actividad individual**", "@@15 min@@", "Trabajo autónomo en examlab"],
]

NIVELES = {
    1: "Nivel 1 — Identificar",
    2: "Nivel 2 — Analizar",
    3: "Nivel 3 — Evaluar",
}


def std_proposito(prs, foco, nivel):
    items = ["**El propósito de la tutoría de hoy es:**", (foco, 1), "Niveles de logro de la asignatura:"]
    for n in (1, 2, 3):
        txt = NIVELES[n]
        items.append((f"@@{txt}  ←  hoy@@" if n == nivel else txt, 1))
    content_slide(prs, "El propósito de hoy", items, size=16, idx=2)

def std_autonomo(prs, items, idx):
    content_slide(prs, "Trabajo autónomo (15 min)", items, size=16, idx=idx)

def std_logros(prs, items, idx):
    content_slide(prs, "¿Qué logramos hoy?", items + [
        "Chequea tu saber con el **quiz de la sesión en examlab (Test)**; la práctica va en @@examlab (Lab) o en la herramienta online@@ indicada.",
    ], size=16, idx=idx)


# ============================== SESIONES ==============================
SESIONES = {
 1: dict(
    titulo="Fundamentos de Redes y Medios Físicos",
    subtitulo="El modelo de cinco capas y el cableado que sostiene la red",
    archivo="Sesion 1 - Fundamentos de Redes y Medios Fisicos",
    nivel=1, gancho="¡Manos a la red!",
    foco="Identificar el modelo TCP/IP de cinco capas, los dispositivos de red y los medios físicos: cables, dúplex, puertos, paneles de conexión, Ethernet y direcciones MAC.",
    contenido=[
        ("tabla", "El modelo de red de cinco capas", ["Capa", "Qué hace", "Ejemplos"], [
            ["**5. Aplicación**", "El contenido que el usuario ve", "HTTP, DNS, correo"],
            ["**4. Transporte**", "Entrega los datos al programa correcto", "TCP, UDP, puertos"],
            ["**3. Red**", "Lleva los datos entre redes distintas", "IP, routers"],
            ["**2. Enlace de datos**", "Entrega dentro de la misma red local", "Ethernet, direcciones MAC"],
            ["**1. Física**", "Transmite los bits por el medio", "Cables, señales, conectores"],
        ], dict(col_w=[2.6, 5.2, 4.2], note="El modelo **OSI** usa 7 capas: divide Aplicación en Sesión, Presentación y Aplicación.")),
        ("bullets", "Dispositivos de red: del cable al router", [
            "**Cables**: par trenzado (cobre) y fibra óptica — las autopistas de los bits.",
            "**Concentrador (hub)**: capa física; repite TODO a TODOS los puertos (dominio de colisión).",
            "**Switch**: capa de enlace; lee la dirección **MAC** y entrega solo al destinatario.",
            "**Router**: capa de red; conecta redes distintas y decide rutas usando direcciones **IP**.",
            "**Servidores y clientes**: el servidor @@ofrece@@ el servicio; el cliente lo @@consume@@.",
            "Un mismo equipo puede ser servidor y cliente a la vez (nodo).",
        ]),
        ("bullets", "Medios físicos: par trenzado, dúplex y paneles de conexión", [
            "Los bits viajan como **pulsos eléctricos** (cobre) o **de luz** (fibra): 1 = hay señal, 0 = no hay.",
            "El **trenzado** de los pares cancela la interferencia electromagnética y la diafonía (crosstalk).",
            "**Dúplex completo**: ambos extremos hablan a la vez (pares dedicados). **Semidúplex**: por turnos.",
            "**Puertos de red** en los equipos ↔ **paneles de conexión (patch panels)** en el rack: el corazón del @@cableado estructurado@@.",
            "El patch panel NO es inteligente: solo organiza; los cables llegan a un switch.",
            "Herramientas del oficio: crimpadora, ponchadora, probador de cables (tester).",
        ]),
        ("tabla", "Ethernet, direcciones MAC y la trama", ["Tipo de envío", "¿Quién recibe?", "Ejemplo"], [
            ["**Unicast**", "Un solo destinatario (1 a 1)", "Tu PC → el servidor"],
            ["**Multicast**", "Un grupo que se suscribe", "Streaming a varios equipos"],
            ["**Broadcast**", "TODOS los de la red local", "ARP: '¿quién tiene esta IP?'"],
        ], dict(col_w=[2.8, 5.0, 4.2], note="La **MAC** son 48 bits (6 octetos) grabados en la tarjeta. La **trama Ethernet** empaqueta: preámbulo, MAC destino/origen, tipo, datos y FCS (control de errores).")),
    ],
    autonomo=[
        "En **examlab → Taller 'red consola'**: abre el escenario de la sesión (PC – switch – router).",
        "Configura el router: `enable` → `configure terminal` → `interface g0/0` → `ip address …` → `no shutdown`.",
        ("Verifica con `show ip interface brief` y haz `ping` al equipo directamente conectado.", 1),
        "En la **pizarra de examlab** (o draw.io) rotula cada dispositivo con su capa del modelo de cinco capas.",
        "Responde: ¿por qué el switch NO necesita dirección IP para reenviar tramas?",
    ],
    logros=[
        "Identificamos las **cinco capas** y qué hace cada una.",
        "Distinguimos **hub, switch y router** por la capa en la que operan.",
        "Vimos cómo el **par trenzado, los puertos y los patch panels** forman el cableado estructurado.",
        "Entendimos **Ethernet, la MAC y la trama**, y los envíos unicast/multicast/broadcast.",
    ],
    cierre=("¡Nos vemos en la Sesión 2!",
            ["Próxima sesión: **La Capa de Red — Direccionamiento IP y Subredes**.",
             "Completa el escenario de 'red consola' y la actividad en **examlab**."],
            "De los cables… ¡a las direcciones IP!"),
 ),

 2: dict(
    titulo="La Capa de Red: Direccionamiento IP y Subredes",
    subtitulo="IPv4, máscaras, binario, CIDR y enrutamiento",
    archivo="Sesion 2 - La Capa de Red - Direccionamiento IP y Subredes",
    nivel=1, gancho="¡A calcular subredes!",
    foco="Identificar el direccionamiento IPv4, el encapsulamiento en datagramas, ARP, la división en subredes con matemática binaria, CIDR y los conceptos básicos de enrutamiento.",
    contenido=[
        ("bullets", "Direcciones IPv4 y datagramas", [
            "Una IP son **32 bits = 4 octetos** (0–255): p. ej. **192.168.1.10**.",
            "La IP pertenece a la **red**, no al equipo: si te mueves de red, cambia tu IP.",
            "**Encapsulamiento**: el datagrama IP viaja DENTRO de la trama Ethernet, y el segmento TCP DENTRO del datagrama (muñecas rusas).",
            "**Clases históricas**: A (0–126, /8) · B (128–191, /16) · C (192–223, /24).",
            "**ARP**: pregunta por broadcast '¿quién tiene la IP X?' para descubrir la **MAC** del vecino.",
            "Direcciones **privadas (RFC 1918)**: 10.0.0.0/8 · 172.16.0.0/12 · 192.168.0.0/16.",
        ]),
        ("tabla", "Subredes: máscaras y matemática binaria", ["Concepto", "Ejemplo", "Significado"], [
            ["Octeto en binario", "192 = **11000000**", "128+64 = 192"],
            ["Máscara /24", "255.255.255.0", "24 bits de red · 8 de host → **254 hosts**"],
            ["Máscara /26", "255.255.255.192", "26 bits de red · 6 de host → **62 hosts**"],
            ["Dirección de red", "192.168.1.**0**", "Todos los bits de host en 0 (no se asigna)"],
            ["Broadcast", "192.168.1.**255**", "Todos los bits de host en 1 (no se asigna)"],
        ], dict(col_w=[3.4, 3.8, 4.8], note="Hosts útiles = 2^(bits de host) − 2. La máscara divide la IP en **parte de red** y **parte de host**.")),
        ("bullets", "CIDR: la notación que simplifica todo", [
            "**CIDR** (enrutamiento sin clases) reemplaza las clases A/B/C rígidas.",
            "La notación **/N** dice cuántos bits son de red: 192.168.1.0**/26**.",
            "Permite **dividir** redes grandes (subnetting) y **agrupar** rutas (supernetting).",
            "Ejemplo: una /24 se parte en **4 subredes /26** de 62 hosts cada una.",
            "@@Demo en clase:@@ calculadora IP en línea + verificación manual en binario.",
        ]),
        ("bullets", "Enrutamiento básico: tablas, IGP/EGP e IANA", [
            "Un **router** mira la IP destino y consulta su **tabla de enrutamiento**: red destino → siguiente salto.",
            "Los routers aprenden rutas con protocolos: **IGP** dentro de una organización (RIP, OSPF), **EGP** entre organizaciones (**BGP**).",
            "Los **sistemas autónomos (AS)** son los 'países' de Internet; BGP los conecta.",
            "La **IANA** asigna los bloques de direcciones IP en el mundo.",
            "Las direcciones privadas **no son enrutables** en Internet: por eso existirá **NAT** (Sesión 4).",
        ]),
    ],
    autonomo=[
        "Con una **calculadora IP en línea** (subnettingpractice.com / subnetting.net): divide **192.168.10.0/24** en 4 subredes iguales.",
        ("Para cada subred anota: dirección de red, broadcast, rango útil y máscara.", 1),
        "Verifica **a mano en binario** la primera subred (muestra el procedimiento).",
        "En **examlab → 'red consola'** asigna a la interfaz del router la 1.ª IP útil de tu subred (`ip address … /26`), `no shutdown`, y comprueba con `ping` la conectividad dentro de la subred.",
    ],
    logros=[
        "Identificamos la estructura de una **dirección IPv4** y el encapsulamiento.",
        "Calculamos **subredes** con máscaras y matemática binaria.",
        "Usamos la notación **CIDR /N** para dividir y agrupar redes.",
        "Entendimos cómo los **routers** deciden rutas y quién gobierna las direcciones (IANA).",
    ],
    cierre=("¡Nos vemos en la Sesión 3!",
            ["Próxima sesión: **Capas de Transporte y Aplicación** — TCP, UDP y el viaje completo del paquete.",
             "Practica subnetting en línea y completa la actividad en **examlab**."],
            "Ya sabes DÓNDE están los equipos… ¡ahora veremos CÓMO conversan!"),
 ),

 3: dict(
    titulo="Capas de Transporte y Aplicación",
    subtitulo="TCP/UDP, sockets, firewalls y cómo todo funciona junto",
    archivo="Sesion 3 - Capas de Transporte y Aplicacion",
    nivel=2, gancho="¡Sigamos el viaje del paquete!",
    foco="Analizar el segmento TCP, el protocolo de enlace de tres vías, los estados de los sockets, TCP vs UDP, los firewalls y cómo todas las capas funcionan en conjunto.",
    contenido=[
        ("bullets", "La capa de transporte y el segmento TCP", [
            "La capa de red lleva datos **al equipo** correcto; la de transporte, **al programa** correcto.",
            "**Multiplexación**: muchos servicios a la vez gracias a los **puertos** (web 80/443, correo 25, DNS 53).",
            "**Puertos del sistema** (1–1023, servicios conocidos) vs **puertos efímeros** (los usa el cliente).",
            "El **segmento TCP** incluye: puerto origen/destino, **número de secuencia**, número de **ACK**, banderas, ventana y checksum.",
            "Un **socket** = IP + puerto: la 'puerta' concreta de una conversación.",
        ]),
        ("bullets", "El protocolo de enlace de tres vías", [
            "Como una llamada: '¿Aló?' → '¡Aló! ¿me escuchas?' → 'Sí, te escucho' — y ya podemos hablar.",
            "**1. SYN**: el cliente pide abrir conexión. **2. SYN/ACK**: el servidor acepta. **3. ACK**: el cliente confirma.",
            "Cada byte enviado se **confirma (ACK)**; si algo se pierde, TCP lo **retransmite**: entrega confiable.",
            "Estados del socket: **LISTEN** (esperando) → **SYN_SENT** → **ESTABLISHED** (conversando) → cierre con **FIN/ACK** → CLOSE_WAIT / CLOSED.",
            "Banderas de control: **SYN, ACK, FIN, RST, PSH, URG**.",
        ]),
        ("tabla", "TCP vs UDP y firewalls", ["Característica", "TCP", "UDP"], [
            ["Conexión", "**Orientado a conexión** (handshake)", "Sin conexión (dispara y olvida)"],
            ["Confiabilidad", "Confirma y retransmite", "Sin garantía de entrega"],
            ["Velocidad/costo", "Más control, más overhead", "@@Ligero y rápido@@"],
            ["Usos típicos", "Web, correo, archivos", "Streaming, juegos, DNS"],
        ], dict(col_w=[3.0, 4.6, 4.4], note="El **firewall** filtra tráfico según reglas —normalmente por **puerto**—: deja pasar el 443 (web) y bloquea lo demás.")),
        ("bullets", "La capa de aplicación: todas las capas funcionan en conjunto", [
            "La capa de aplicación habla el idioma del servicio: **HTTP**, correo, DNS…",
            "En el modelo **OSI** equivale a Sesión + Presentación + Aplicación (7 capas).",
            "El viaje completo de abrir una página web:",
            ("Física: los bits viajan por el cable → Enlace: la trama llega al router (MAC)", 1),
            ("Red: el datagrama IP cruza Internet router a router", 1),
            ("Transporte: TCP abre el three-way handshake al puerto 443", 1),
            ("Aplicación: el navegador pide la página con HTTP y la renderiza", 1),
            "@@Cada capa usa a la de abajo y sirve a la de arriba.@@",
        ]),
    ],
    autonomo=[
        "Elige una acción cotidiana (abrir YouTube, enviar un correo, jugar en línea).",
        "En la **pizarra de examlab** (o draw.io) construye el diagrama del viaje del dato por las **cinco capas**: en cada una anota protocolo, unidad de datos (trama/datagrama/segmento) y dirección (MAC/IP/puerto).",
        "Indica si usa **TCP o UDP** y justifica por qué.",
        "Adjunta el diagrama en **examlab**.",
    ],
    logros=[
        "Analizamos el **segmento TCP** y la multiplexación por puertos.",
        "Explicamos el **three-way handshake** y los estados de un socket.",
        "Comparamos **TCP vs UDP** y el papel del **firewall**.",
        "Seguimos un dato de extremo a extremo: **todas las capas en conjunto**.",
    ],
    cierre=("¡Nos vemos en la Sesión 4!",
            ["Próxima sesión: **Servicios de Red — DNS, DHCP, NAT y VPN**.",
             "Completa la actividad en **examlab**."],
            "La red ya funciona… ¡ahora hagámosla fácil de usar!"),
 ),

 4: dict(
    titulo="Servicios de Red: DNS, DHCP, NAT y VPN",
    subtitulo="Los servicios que hacen que la red funcione sola",
    archivo="Sesion 4 - Servicios de Red - DNS DHCP NAT y VPN",
    nivel=2, gancho="¡La red que se configura sola!",
    foco="Analizar cómo DNS resuelve nombres, cómo DHCP configura los equipos automáticamente, y cómo NAT, las VPN y los proxies conectan y protegen las redes.",
    contenido=[
        ("bullets", "DNS: la guía telefónica de Internet", [
            "Los humanos recordamos **nombres** (google.com); la red necesita **IPs**. DNS traduce.",
            "Los 5 pasos de la **resolución de nombres**:",
            ("1. Caché local → 2. Servidor **recursivo** → 3. Servidor **raíz** → 4. Servidor **TLD** (.com) → 5. Servidor **autoritativo** del dominio", 1),
            "La respuesta se guarda en **caché** con un **TTL** (tiempo de vida).",
            "DNS usa **UDP puerto 53**: una consulta cabe en un solo datagrama (rápido).",
            "Anatomía: **www**.google.**com** = subdominio · dominio · TLD.",
        ]),
        ("tabla", "Tipos de registro y zonas DNS", ["Registro", "Qué guarda", "Ejemplo"], [
            ["**A**", "Nombre → IPv4", "web.empresa.co → 190.1.2.3"],
            ["**AAAA**", "Nombre → IPv6", "web → 2800:e2:1080::1"],
            ["**CNAME**", "Alias → otro nombre", "www → empresa.co"],
            ["**MX**", "Servidor de correo", "correo del dominio"],
            ["**NS**", "Servidor de nombres de la zona", "ns1.empresa.co"],
            ["**TXT / PTR**", "Texto (verificación) / IP → nombre", "SPF · resolución inversa"],
        ], dict(col_w=[2.4, 4.6, 5.0], note="Una **zona DNS** es la porción del espacio de nombres que administra un autoritativo; se define en el archivo de zona.")),
        ("bullets", "DHCP: configuración automática de la red", [
            "Sin DHCP tocaría configurar **a mano** IP, máscara, puerta de enlace y DNS en cada equipo.",
            "El baile **DORA** (por broadcast):",
            ("**D**iscover: '¿hay un DHCP?' → **O**ffer: 'te ofrezco esta IP' → **R**equest: 'la acepto' → **A**ck: 'es tuya por X horas'", 1),
            "La IP se entrega en **arriendo (lease)**: al vencer, se renueva o se libera.",
            "Estrategias: **dinámica** (pool), **automática** (fija por MAC) y **reserva** para servidores/impresoras.",
        ]),
        ("bullets", "NAT, VPN y proxies: conectar y proteger", [
            "**NAT**: el router 'traduce' muchas IPs **privadas** a una IP **pública** (soluciona la escasez de IPv4).",
            "Con **PAT/sobrecarga** usa los **puertos** para saber a quién devolver cada respuesta.",
            "**VPN**: un **túnel cifrado** que te mete lógicamente en otra red (teletrabajo seguro).",
            "**Proxy**: intermediario que filtra, acelera (caché) o anonimiza la navegación.",
            "@@NAT esconde tu red · VPN te transporta · proxy habla por ti.@@",
        ]),
    ],
    autonomo=[
        "En la **terminal de tu equipo** (o un nslookup en línea como nslookup.io) ejecuta **nslookup** para google.com, lanuevaamerica.edu.co y un dominio a tu elección.",
        ("Anota: IP(s) devuelta(s), servidor DNS que respondió y si hay registros A/AAAA/CNAME.", 1),
        "Ejecuta **ipconfig /all** (Windows) e identifica: tu IP privada, la puerta de enlace, el servidor DHCP y el DNS.",
        "Responde: ¿tu red usa NAT? ¿Cómo lo sabes? Adjunta las capturas en **examlab**.",
    ],
    logros=[
        "Analizamos los **5 pasos de la resolución DNS** y los tipos de registro.",
        "Explicamos el baile **DORA** de DHCP y el arriendo de IPs.",
        "Entendimos cómo **NAT** multiplica las IPv4 y cómo **VPN y proxy** protegen.",
        "Vimos estos servicios funcionando en **nuestra propia red**.",
    ],
    cierre=("¡Nos vemos en la Sesión 5!",
            ["Próxima sesión: **Conexión a Internet — Banda Ancha, Fibra e Inalámbricas**.",
             "Completa la actividad en **examlab**."],
            "Ya dominas la red local… ¡salgamos a Internet!"),
 ),

 5: dict(
    titulo="Conexión a Internet: Banda Ancha, Fibra e Inalámbricas",
    subtitulo="De la línea telefónica a la fibra y el Wi-Fi",
    archivo="Sesion 5 - Conexion a Internet - Banda Ancha Fibra e Inalambricas",
    nivel=3, gancho="¡Conectados a toda velocidad!",
    foco="Evaluar las tecnologías de acceso a Internet (dial-up, T-carrier, DSL, cable, fibra), las WAN, y las redes inalámbricas y celulares, eligiendo la adecuada para cada escenario.",
    contenido=[
        ("bullets", "De la línea telefónica a la banda ancha", [
            "**Dial-up**: módem sobre la línea de voz, ~56 kbps, ocupaba el teléfono.",
            "**Banda ancha**: conexiones permanentes y de alta velocidad (todo lo que vino después).",
            "**T-carrier (T1/T3)**: líneas dedicadas empresariales (1.544 Mbps / ~45 Mbps).",
            "**DSL**: usa el par de cobre telefónico con frecuencias distintas a la voz — Internet y teléfono a la vez. **ADSL**: más bajada que subida.",
            "**Cable (DOCSIS)**: viaja por el coaxial de la TV; el ancho de banda se **comparte** con los vecinos.",
        ]),
        ("bullets", "Fibra óptica y redes de área extensa", [
            "**Fibra**: pulsos de **luz** — inmune a interferencia, llega mucho más lejos y más rápido.",
            "**FTTX** = fibra hasta X: **FTTN** (nodo), **FTTB** (edificio), **FTTH** (hogar) — cuanto más cerca, mejor.",
            "**WAN**: une sedes lejanas como una sola red, contratada a un proveedor (ISP).",
            "**VPN punto a punto (sitio a sitio)**: la alternativa económica a la WAN dedicada — túnel cifrado entre las dos sedes por Internet.",
            "@@Criterio de evaluación: costo · velocidad · distancia · confiabilidad.@@",
        ]),
        ("tabla", "Redes inalámbricas: canales y seguridad", ["Estándar 802.11", "Banda", "Velocidad máx. teórica"], [
            ["b / g", "2.4 GHz", "11 / 54 Mbps"],
            ["n (Wi-Fi 4)", "2.4 y 5 GHz", "600 Mbps"],
            ["ac (Wi-Fi 5)", "5 GHz", "~3.5 Gbps"],
            ["**ax (Wi-Fi 6)**", "2.4 y 5 GHz", "@@~9.6 Gbps@@"],
        ], dict(col_w=[3.6, 3.2, 5.2], note="En 2.4 GHz solo **1, 6 y 11** no se solapan. Seguridad: WEP (roto) → WPA → **WPA2** → **WPA3**. Modos: infraestructura (AP) vs ad-hoc.")),
        ("bullets", "Redes celulares y de dispositivos móviles", [
            "La red celular divide el territorio en **celdas**, cada una con su antena; al moverte haces **handoff** sin cortar la llamada.",
            "Generaciones: 2G (voz/SMS) → 3G (datos) → **4G/LTE** (banda ancha móvil) → **5G** (baja latencia, IoT).",
            "Las frecuencias celulares viajan **más lejos** que el Wi-Fi: cobertura de kilómetros.",
            "Dispositivos móviles: Wi-Fi + celular + **Bluetooth/NFC** para lo cercano; **anclaje (tethering)** comparte el celular como módem.",
            "@@Evalúa siempre: movilidad vs velocidad vs costo por GB.@@",
        ]),
    ],
    autonomo=[
        "Para **3 escenarios**, elige y justifica la tecnología de acceso más adecuada (costo, velocidad, distancia, confiabilidad):",
        ("a) Vereda rural a 15 km del casco urbano, presupuesto bajo.", 1),
        ("b) Empresa con sede principal y sucursal en otra ciudad que comparten un ERP.", 1),
        ("c) Apartamento familiar: teletrabajo + streaming + juegos en línea.", 1),
        "Arma la tabla comparativa en la **pizarra de examlab** (o una hoja en línea) y adjúntala en **examlab**.",
    ],
    logros=[
        "Recorrimos la evolución del acceso: **dial-up → DSL → cable → fibra**.",
        "Comparamos **WAN dedicada vs VPN punto a punto** para unir sedes.",
        "Evaluamos los estándares **Wi-Fi**, sus canales y su seguridad (WPA2/WPA3).",
        "Entendimos las **redes celulares** y cuándo conviene cada tecnología.",
    ],
    cierre=("¡Nos vemos en la Sesión 6!",
            ["Última sesión: **Solución de Problemas de Red y el Futuro — Nube e IPv6**.",
             "Repasa el diagnóstico con las herramientas en línea y en **examlab**."],
            "Ya estamos conectados… ¡aprendamos a diagnosticar como profesionales!"),
 ),

 6: dict(
    titulo="Solución de Problemas de Red y el Futuro: Nube e IPv6",
    subtitulo="ping, traceroute, DNS, la nube y la transición a IPv6",
    archivo="Sesion 6 - Solucion de Problemas de Red y el Futuro - Nube e IPv6",
    nivel=3, gancho="¡Doctores de la red!",
    foco="Diagnosticar problemas de conectividad con ping, traceroute y herramientas de nombres en Windows/macOS/Linux; evaluar la nube ('todo como servicio') y la transición a IPv6.",
    contenido=[
        ("bullets", "Herramientas de diagnóstico: ping y traceroute", [
            "**ICMP**: el protocolo de los mensajes de control y error de la red (no lleva datos de usuario).",
            "**ping destino**: envía eco ICMP y mide **latencia** y **pérdida de paquetes** — ¿está vivo el destino?",
            "**traceroute / tracert**: revela **cada router del camino** aumentando el TTL de a 1 — ¿dónde se rompe la ruta?",
            "Probar un **puerto** concreto: `Test-NetConnection -Port 443` (Windows) · `nc -zv host 443` (Linux/macOS).",
            "@@Método del embudo:@@ ping a tu gateway → ping a una IP pública (8.8.8.8) → ping a un dominio. Cada paso descarta una causa.",
        ]),
        ("bullets", "Diagnóstico de nombres: nslookup, DNS públicos y hosts", [
            "Si `ping 8.8.8.8` funciona pero `ping google.com` no… ¡el problema es **DNS**, no la red!",
            "**nslookup / dig**: consultan directamente al servidor DNS y muestran qué responde.",
            "**DNS públicos**: 8.8.8.8 (Google) · 1.1.1.1 (Cloudflare) — útiles para descartar el DNS del ISP.",
            "El **archivo hosts** resuelve nombres ANTES que el DNS (útil para pruebas, peligroso si un malware lo edita).",
            "Los dominios se **registran** y **vencen**: un dominio vencido también 'daña' la web.",
        ]),
        ("tabla", "La nube: todo como servicio (XaaS)", ["Modelo", "Qué te dan", "Ejemplos"], [
            ["**IaaS**", "Infraestructura: máquinas virtuales, discos, redes", "AWS EC2, Azure VMs"],
            ["**PaaS**", "Plataforma lista para desplegar tu código", "App Engine, Heroku"],
            ["**SaaS**", "Software terminado por suscripción", "Gmail, Office 365"],
        ], dict(col_w=[2.4, 5.4, 4.2], note="La nube = **virtualización a escala**: hardware compartido, pago por uso. Nubes públicas, privadas e híbridas. El **almacenamiento en la nube** replica tus datos en varios centros de datos.")),
        ("bullets", "IPv6: el futuro del direccionamiento", [
            "IPv4 (32 bits) **se agotó**; IPv6 usa **128 bits**: 2¹²⁸ direcciones (¡miles por metro cuadrado de la Tierra!).",
            "Notación: 8 grupos hexadecimales — **2001:0db8:0000:0000:0000:0000:0000:0001**.",
            "Compresión: quitar ceros a la izquierda y UNA sola vez '::' → **2001:db8::1**.",
            "Conviven con **dual stack** (ambos protocolos a la vez) y **túneles** (IPv6 viajando dentro de IPv4).",
            "IPv6 elimina la necesidad de NAT: cada dispositivo puede tener IP pública propia.",
            "@@Bonus de cierre:@@ en la entrevista laboral te preguntarán por el modelo de capas, subnetting y diagnóstico — ¡ya los dominas!",
        ]),
    ],
    autonomo=[
        "Diagnóstico guiado — ejecuta y pega evidencias (capturas):",
        ("1. `ping` a tu puerta de enlace y a 8.8.8.8 (anota latencia y pérdida).", 1),
        ("2. `tracert` / `traceroute` a lanuevaamerica.edu.co — ¿cuántos saltos hay?", 1),
        ("3. `nslookup` a un dominio con tu DNS y luego con 1.1.1.1 — ¿cambia la respuesta?", 1),
        ("4. En **examlab → 'red consola'** reactiva la interfaz caída del escenario (`show ip interface brief` → `no shutdown`) hasta que el `ping` funcione.", 1),
        ("5. Comprime a mano (verifica con un validador IPv6 en línea): 2001:0db8:0000:0000:00ff:0000:0000:0001 → ¿?", 1),
        "Adjunta todo en **examlab**.",
    ],
    logros=[
        "Diagnosticamos redes con **ping, traceroute y pruebas de puerto** (método del embudo).",
        "Separamos fallas de **red** vs fallas de **DNS** con nslookup y DNS públicos.",
        "Evaluamos los modelos de nube **IaaS / PaaS / SaaS**.",
        "Comprimimos direcciones **IPv6** y entendimos la transición dual stack.",
        "@@¡Completamos las 6 sesiones del curso!@@",
    ],
    cierre=("¡Gracias por llegar hasta aquí!",
            ["Cierra el curso presentando la **prueba de rendimiento** en examlab.",
             "Completa los **talleres y entrenamientos** pendientes y responde la **encuesta de satisfacción**.",
             "Recorrimos las 6 sesiones: de los medios físicos a la nube y el IPv6."],
            "De los cables a la nube: ¡ya piensas como ingeniero de redes!"),
 ),
}


# ============================== BUILDERS ==============================
def build_presentacion():
    set_footer(CURSO)
    prs = new_prs()
    course_cover(prs, CURSO, None, "¡Bienvenidos estudiantes!",
        [PROGRAMA, "Cuatrimestre No. [N]", "Duración: **6 clases** (105 min c/u)",
         "Horario: Lunes, Miércoles y Viernes · 6:00–7:45 PM",
         "Fechas: 13/07/2026 – 25/07/2026"],
        "Empezamos a las 6:00 PM…")
    tutor_slide(prs, TUTOR[0], TUTOR[1], TUTOR[2], idx=2)
    content_slide(prs, "METODOLOGÍA", [
        "**Sesiones teórico-prácticas**: cada clase combina teoría, modelación y práctica.",
        "Momentos por clase:",
        ("**Motivación**: preguntas y ejemplos que generan interés y conexión.", 1),
        ("**Encuadre**: explicación de objetivos, ruta de aprendizaje y acuerdos.", 1),
        ("**Modelación**: ejemplos guiados para mostrar conceptos y técnicas.", 1),
        ("**Simulación**: trabajo en grupos pequeños para aplicar conceptos.", 1),
        ("**Ejercitación**: práctica individual utilizando la plataforma.", 1),
        ("**Cierre**: retroalimentación, resumen y conexión con objetivos.", 1),
        ("**Evaluación**: tareas individuales y ejercicios prácticos en plataforma.", 1),
    ], idx=3)
    objectives_slide(prs, "Objetivos", OBJETIVOS_CURSO, idx=4)
    table_content(prs, "¿Cómo se evalúa?", ["Componente", "Ponderación"], EVAL_ROWS,
                  col_w=[9.2, 2.8], aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER], idx=5,
                  note=EVAL_OPCIONALES[0] + "  ·  " + EVAL_OPCIONALES[1])
    content_slide(prs, "EJEMPLO DE EVALUACIÓN", [
        "Asistencia (10%): asistió → 1 × 0.1 = **0.1**",
        "Prueba de rendimiento — LMS (40%): 4.8 × 0.40 = **1.92**",
        "Destreza — entrenamientos de la ruta (50%): 4.5 × 0.50 = **2.25**",
        "Participación en clase: no participó → **0**",
        "Kahoot: quedó de primero → **+0.5**",
        "@@Nota final = 0.1 + 1.92 + 2.25 + 0 + 0.5 = 4.77@@",
    ], idx=6)
    content_slide(prs, "CONTENIDO", [
        f"**Sesión {n}** — {d['titulo']}." for n, d in SESIONES.items()
    ], idx=7)
    content_slide(prs, "RECURSOS", [
        "**Material de clases:** 🔗 [inserta aquí el hipervínculo] — guiones, diapositivas y material de apoyo.",
        "**Curso base (Coursera):** Los bits y bytes de las redes informáticas — Google",
        ("https://www.coursera.org/learn/redes-informaticas", 1),
        "Guías, videos y ruta de aprendizaje: en **examlab**.",
        ("https://examlab.lovable.app/app", 1),
    ], idx=8)
    content_slide(prs, "HERRAMIENTAS", [
        "**En examlab** (plataforma del curso · https://examlab.lovable.app/app):",
        ("Test (quizzes) · Lab \"red consola\" (Cisco IOS) · editor de código · pizarra.", 1),
        "**Solo online (gratuitas):**",
        ("subnettingpractice.com · subnetting.net · subnetipv4.com · nslookup.io · dnschecker.org · NetPilot · draw.io.", 1),
        "**En el mundo laboral** (lo que usarás en el trabajo):",
        ("Wireshark (análisis de paquetes) · GNS3 / EVE-NG · equipos Cisco reales (IOS) · certificadoras de cableado (Fluke) · terminal (ping/tracert/nslookup).", 1),
    ], size=15, idx=9)
    content_slide(prs, "¡ IMPORTANTE !", [
        "La **prueba de rendimiento (LMS)** está abierta desde **8 días antes** del cierre de la asignatura, hasta el último día.",
        "La **prueba de nivelación** (formulario de Google) se realiza solo en caso de perder la asignatura.",
        "Las **notas** se envían para validación el siguiente día hábil después de finalizar el curso.",
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
    session_cover(prs, f"SESIÓN {n}", NIVELES[d["nivel"]], d["titulo"], d["subtitulo"],
                  d["gancho"],
                  [f"{CURSO} · {PROGRAMA}", "Duración: **105 min** (1 h 45 min)"])
    # SIN slides "Recordemos la asignatura" ni "¿Cómo trabajaremos hoy?" (reglas del usuario)
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
    print("LISTO: 7 decks generados.")
