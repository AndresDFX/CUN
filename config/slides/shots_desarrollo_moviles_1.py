# -*- coding: utf-8 -*-
"""
Genera los pantallazos de 'Kotlin Playground · Salida' (PNG) con el código y su
salida EXACTOS, para incrustar en los guiones docentes del curso
Desarrollo de Aplicaciones Móviles 1. Usa terminal_shot (tema oscuro, banner 'env').

El código va como comentario (editor) y la salida como texto de consola; se resalta
la línea clave en naranja de marca (hl=True). Salida a Clases/Version vigente (nuevo dictado 2026)/Guiones/Capturas/.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from terminal_shot import render_many

DEST = r"g:\My Drive\Trabajos\Empleo\FESNA\Cursos\Desarrollo de Aplicaciones Moviles 1\Clases\Version vigente (nuevo dictado 2026)\Guiones\Capturas"
ENV = "Kotlin Playground · Salida"


def cm(t):  return {"t": "comment", "text": t}
def out(t, hl=False): return {"t": "out", "text": t, "hl": hl}
def blank(): return {"t": "blank", "text": ""}


SPECS = [
 # ---- S1 ----
 {"id": "moviles_s1_hola", "env": ENV, "title": "Primer programa · variables y plantillas de string", "prompt": "",
  "lines": [cm("// fun main() {"), cm("//   val nombre = \"Ana\"    // val: inmutable"),
            cm("//   var edad = 20         // var: mutable"),
            cm("//   println(\"Hola, soy $nombre y tengo $edad años.\")"), cm("// }"), blank(),
            out("Hola, soy Ana y tengo 20 años.", hl=True)]},
 {"id": "moviles_s1_println", "env": ENV, "title": "println() vs print()", "prompt": "",
  "lines": [cm("// print(\"A\"); print(\"B\"); println(\"C\"); println(\"D\")"), blank(),
            out("ABC"), out("D")]},
 # ---- S2 ----
 {"id": "moviles_s2_nota", "env": ENV, "title": "Clasificar una nota con if y when", "prompt": "",
  "lines": [cm("// val nota = 4.2"),
            cm("// val estado = if (nota >= 3.0) \"Aprobó\" else \"Reprobó\""),
            cm("// val letra = when { nota>=4.5 -> \"Excelente\";"),
            cm("//                    nota>=3.0 -> \"Aceptable\"; else -> \"Insuficiente\" }"),
            cm("// println(\"$estado - $letra\")"), blank(),
            out("Aprobó - Aceptable", hl=True)]},
 {"id": "moviles_s2_when_dia", "env": ENV, "title": "when con rangos", "prompt": "",
  "lines": [cm("// val dia = 6"),
            cm("// println(when (dia) { in 1..5 -> \"Entre semana\";"),
            cm("//                      6, 7 -> \"Fin de semana\"; else -> \"No válido\" })"), blank(),
            out("Fin de semana", hl=True)]},
 # ---- S3 ----
 {"id": "moviles_s3_tabla", "env": ENV, "title": "Tabla de multiplicar con bucles anidados", "prompt": "",
  "lines": [cm("// for (i in 1..3) { for (j in 1..3) print(\"${i*j}\\t\"); println() }"), blank(),
            out("1    2    3"), out("2    4    6"), out("3    6    9", hl=True)]},
 {"id": "moviles_s3_rangos", "env": ENV, "title": "Rangos: 1..5, until, downTo, step", "prompt": "",
  "lines": [cm("// for (i in 1..5) print(\"$i \")"), out("1 2 3 4 5"),
            cm("// for (i in 5 downTo 1 step 2) print(\"$i \")"), out("5 3 1", hl=True)]},
 # ---- S4 ----
 {"id": "moviles_s4_funciones", "env": ENV, "title": "Funciones: retorno y argumentos por defecto/nombrados", "prompt": "",
  "lines": [cm("// fun suma(a: Int, b: Int) = a + b"),
            cm("// fun saludar(nombre: String, saludo: String = \"Hola\") = \"$saludo, $nombre\""),
            cm("// println(suma(3, 4))"),
            cm("// println(saludar(\"Ana\"))"),
            cm("// println(saludar(\"Luis\", saludo = \"Hey\"))"), blank(),
            out("7"), out("Hola, Ana"), out("Hey, Luis", hl=True)]},
 {"id": "moviles_s4_mayoria", "env": ENV, "title": "esMayorDeEdad(edad): Boolean", "prompt": "",
  "lines": [cm("// fun esMayorDeEdad(edad: Int): Boolean = edad >= 18"),
            cm("// println(esMayorDeEdad(20)); println(esMayorDeEdad(15))"), blank(),
            out("true"), out("false")]},
 # ---- S5 ----
 {"id": "moviles_s5_cuenta", "env": ENV, "title": "Clase CuentaBancaria", "prompt": "",
  "lines": [cm("// class CuentaBancaria(val titular: String, var saldo: Double) {"),
            cm("//   fun depositar(m: Double) { saldo += m } }"),
            cm("// val c = CuentaBancaria(\"Ana\", 0.0); c.depositar(50.0); println(c.saldo)"), blank(),
            out("50.0", hl=True)]},
 {"id": "moviles_s5_persona", "env": ENV, "title": "Crear un objeto y llamar un método", "prompt": "",
  "lines": [cm("// class Persona(val nombre: String, var edad: Int) {"),
            cm("//   fun saludar() = println(\"Hola, soy $nombre\") }"),
            cm("// val p = Persona(\"Ana\", 20); p.saludar(); p.edad++; println(p.edad)"), blank(),
            out("Hola, soy Ana"), out("21", hl=True)]},
 # ---- S6 ----
 {"id": "moviles_s6_polimorfismo", "env": ENV, "title": "Herencia y polimorfismo", "prompt": "",
  "lines": [cm("// open class Animal { open fun hacerSonido() = \"...\" }"),
            cm("// class Perro : Animal() { override fun hacerSonido() = \"Guau\" }"),
            cm("// class Gato : Animal() { override fun hacerSonido() = \"Miau\" }"),
            cm("// listOf(Perro(), Gato()).forEach { println(it.hacerSonido()) }"), blank(),
            out("Guau"), out("Miau", hl=True)]},
 {"id": "moviles_s6_vehiculo", "env": ENV, "title": "Vehiculo, Carro y Moto (override)", "prompt": "",
  "lines": [cm("// open class Vehiculo { open fun describir() = \"Un vehículo\" }"),
            cm("// class Carro : Vehiculo() { override fun describir() = \"Soy un carro\" }"),
            cm("// class Moto  : Vehiculo() { override fun describir() = \"Soy una moto\" }"),
            cm("// listOf(Carro(), Moto()).forEach { println(it.describir()) }"), blank(),
            out("Soy un carro"), out("Soy una moto")]},
 # ---- S7 ----
 {"id": "moviles_s7_dataclass", "env": ENV, "title": "data class: toString() y copy()", "prompt": "",
  "lines": [cm("// data class Persona(val nombre: String, val edad: Int)"),
            cm("// val a = Persona(\"Ana\", 20); val b = a.copy(edad = 21)"),
            cm("// println(a); println(b)"), blank(),
            out("Persona(nombre=Ana, edad=20)"), out("Persona(nombre=Ana, edad=21)", hl=True)]},
 {"id": "moviles_s7_null", "env": ENV, "title": "Nulabilidad (Elvis) y try/catch", "prompt": "",
  "lines": [cm("// val desc: String? = null"),
            cm("// println(desc ?: \"Sin descripción\")"),
            cm("// val n = try { \"10x\".toInt() } catch (e: Exception) { 0 }"),
            cm("// println(n)"), blank(),
            out("Sin descripción"), out("0", hl=True)]},
 # ---- S8 ----
 {"id": "moviles_s8_filter_map", "env": ENV, "title": "filter y map sobre una lista", "prompt": "",
  "lines": [cm("// val nums = listOf(1, 2, 3, 4, 5, 6)"),
            cm("// println(nums.filter { it % 2 == 0 }.map { it * 10 })"), blank(),
            out("[20, 40, 60]", hl=True)]},
 {"id": "moviles_s8_map", "env": ENV, "title": "Recorrer un Map (clave, valor)", "prompt": "",
  "lines": [cm("// val edades = mapOf(\"Ana\" to 20, \"Luis\" to 25)"),
            cm("// for ((nombre, edad) in edades) println(\"$nombre: $edad\")"), blank(),
            out("Ana: 20"), out("Luis: 25")]},
 # ---- S9 ----
 {"id": "moviles_s9_evidencia", "env": ENV, "title": "Evidencia final · data class + colecciones + filter", "prompt": "",
  "lines": [cm("// data class Tarea(val titulo: String, var hecha: Boolean)"),
            cm("// val lista = mutableListOf(Tarea(\"Estudiar\", false), Tarea(\"Practicar\", true))"),
            cm("// lista.filter { it.hecha }.forEach { println(\"[x] ${it.titulo}\") }"), blank(),
            out("[x] Practicar", hl=True)]},
]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    os.makedirs(DEST, exist_ok=True)
    paths = render_many(SPECS, DEST)
    print(f"OK: {len(paths)} pantallazos de Kotlin Playground -> {DEST}")
