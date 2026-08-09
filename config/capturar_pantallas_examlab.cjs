/* Captura pantallas REALES de examlab (login con credenciales FESNA) + herramientas online.
   Se ejecuta desde el repo de examlab (para resolver 'playwright'). */
const { chromium } = require("C:/Projects/Personal/examlab/node_modules/playwright");
const path = require("node:path");
const fs = require("node:fs");

const APP = "https://examlab.lovable.app";  // base; el script arma /auth y /app/... por su cuenta
const EMAIL = process.env.EL_EMAIL;
const PASSWORD = process.env.EL_PASS;
const TENANT_RE = /fesna|nueva\s*am|am[eé]rica/i;
// Staging de capturas CRUDAS (fuera de la raíz de FESNA). Luego copia cada captura
// a la carpeta del curso donde aplica: Cursos/<Curso>/Guiones/Capturas/.
const OUT = "G:/Mi unidad/Trabajos/Empleo/FESNA/config/_capturas_raw";
fs.mkdirSync(OUT, { recursive: true });
const VP = { width: 1440, height: 900 };

const APP_SCREENS = [
  ["/app", "01-dashboard"],
  ["/app/teacher/courses", "02-cursos"],
  ["/app/teacher/contents", "03-contenidos-generar-IA"],
  ["/app/teacher/exams", "04-examenes-Test"],
  ["/app/teacher/workshops", "05-talleres-Lab"],
  ["/app/teacher/polls", "06-encuestas-sesion-en-vivo"],
  ["/app/teacher/whiteboards", "07-pizarras"],
];

const TOOLS = [
  ["https://bellard.org/jslinux/", "online-01-jslinux", 9000],
  ["https://subnettingpractice.com/", "online-02-subnettingpractice", 4000],
];

const log = (m) => console.log(m);

async function shot(page, name) {
  try {
    await page.screenshot({ path: path.join(OUT, name + ".png") });
    log(`  📸 ${name}.png`);
  } catch (e) { log(`  ✗ screenshot ${name}: ${e.message}`); }
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: VP, ignoreHTTPSErrors: true });
  const page = await ctx.newPage();
  let loginOk = false;

  // ---------- LOGIN ----------
  try {
    log(`→ Abriendo ${APP}/auth`);
    await page.goto(`${APP}/auth`, { waitUntil: "domcontentloaded", timeout: 45000 });
    await page.waitForSelector('input[type="email"]', { timeout: 20000 });
    await shot(page, "00-login-form");

    // Seleccionar tenant (Radix Select #li-tenant)
    let tenantPicked = "(ninguno)";
    try {
      await page.locator("#li-tenant").click({ timeout: 8000 });
      await page.waitForSelector('[role="option"]', { timeout: 8000 });
      const opts = page.locator('[role="option"]');
      const n = await opts.count();
      const labels = [];
      for (let i = 0; i < n; i++) labels.push(((await opts.nth(i).textContent()) || "").trim());
      log("  Tenants: " + labels.join(" | "));
      let pick = labels.find((t) => TENANT_RE.test(t));
      if (!pick) pick = labels.find((t) => t && !t.startsWith("—") && !/cross-tenant/i.test(t));
      if (pick) {
        await page.getByRole("option", { name: pick, exact: true }).first().click();
        tenantPicked = pick;
      }
      log("  → Tenant elegido: " + tenantPicked);
    } catch (e) {
      log("  (sin selector de tenant o falló: " + e.message + ")");
    }

    await page.fill('input[type="email"]', EMAIL);
    await page.fill('input[type="password"]', PASSWORD);
    const btn = page.locator('button[type="submit"]').first();
    await btn.waitFor({ state: "visible", timeout: 8000 });
    try {
      await page.waitForFunction(() => {
        const b = document.querySelector('button[type="submit"]');
        return b && !b.disabled;
      }, { timeout: 8000 });
    } catch { log("  (submit no se habilitó; intento igual)"); }
    await btn.click();

    try {
      await page.waitForURL(/\/app(\/|$)/, { timeout: 25000 });
      loginOk = true;
      log("  ✓ LOGIN EXITOSO → " + page.url());
    } catch {
      log("  ✗ LOGIN NO redirigió a /app. URL actual: " + page.url());
      const errs = await page.locator('[role="alert"], .text-destructive, [data-sonner-toast]').allTextContents();
      if (errs.length) log("  Mensajes: " + errs.map((e) => e.trim()).filter(Boolean).join(" | "));
      await shot(page, "00-login-resultado");
    }
  } catch (e) {
    log("  ✗ Error en login: " + e.message);
    await shot(page, "00-login-error");
  }

  // ---------- PANTALLAS DE examlab ----------
  if (loginOk) {
    await page.waitForTimeout(2500);
    for (const [p, name] of APP_SCREENS) {
      try {
        await page.goto(APP + p, { waitUntil: "domcontentloaded", timeout: 30000 });
        await page.waitForTimeout(3500);
        await shot(page, name);
      } catch (e) { log(`  ✗ ${name}: ${e.message}`); }
    }
  }
  await ctx.close();

  // ---------- HERRAMIENTAS ONLINE (sin login) ----------
  const ctx2 = await browser.newContext({ viewport: VP, ignoreHTTPSErrors: true });
  const page2 = await ctx2.newPage();
  for (const [url, name, wait] of TOOLS) {
    try {
      await page2.goto(url, { waitUntil: "domcontentloaded", timeout: 45000 });
      await page2.waitForTimeout(wait);
      await shot(page2, name);
    } catch (e) { log(`  ✗ ${name}: ${e.message}`); }
  }
  await ctx2.close();
  await browser.close();

  log(`\nRESULTADO LOGIN examlab: ${loginOk ? "EXITOSO" : "FALLÓ (ver 00-login-*.png)"}`);
})();
