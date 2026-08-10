# -*- coding: utf-8 -*-
"""Genera un reel vertical (1080x1920) a partir de contenido/reels.json.

Cómo funciona:
  1. arma una página HTML con la animación completa en CSS
  2. Playwright la captura cuadro por cuadro, moviendo el reloj a mano
  3. ffmpeg la pasa a MP4 (H.264 + AAC), que es lo que acepta Instagram
  4. si hay pistas en audio/, le pega una; si no, va una pista de silencio

Salida:
  reels/AAAA-MM-DD.mp4   video listo para publicar
  reels/AAAA-MM-DD.txt   caption listo para publicar
"""
import json, os, pathlib, asyncio, subprocess, datetime as dt, sys, shutil

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import brand

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INICIO = dt.date(2026, 8, 4)      # mismo día 1 que el calendario de estáticos
FPS = 30
# Instagram pide mínimo 3 segundos. Entre 20 y 30 es donde mejor rinde
# un reel de texto: alcanza para leerlo sin que se haga largo.
EXTRA_FINAL = 0.6                 # colita para que no corte el último cuadro

HASHTAGS = [
    "#automatizacion #software #gestion #emprendedores",
    "#desarrolloweb #sistemas #turnos #pymes",
    "#softwareamedida #automatizacion #ecommerce #productividad",
]
SEPARADOR = "·  ·  ·"


# ---------------------------------------------------------------- contenido

def reel_de_hoy(hoy):
    reels = json.loads((RAIZ / "contenido" / "reels.json").read_text(encoding="utf-8"))
    # Los reels salen lunes, miércoles y viernes. El índice avanza de a uno
    # por reel publicado, no por día del calendario.
    if hoy.weekday() not in (0, 2, 4):
        raise SystemExit(f"El {hoy} no toca reel (solo lunes, miércoles y viernes).")
    dias = (hoy - INICIO).days
    if dias < 0:
        raise SystemExit("El ciclo todavía no arrancó.")
    # cuántos lunes/miércoles/viernes hubo desde el inicio, sin contar hoy
    idx = sum(1 for d in range(dias)
              if (INICIO + dt.timedelta(days=d)).weekday() in (0, 2, 4))
    if idx >= len(reels):
        raise SystemExit(
            f"Se acabaron los reels ({len(reels)} guionados). Pedile a Claude el "
            f"próximo lote y actualizá contenido/reels.json.")
    return reels[idx], idx


def resaltar(texto):
    """*asi* queda en verde menta."""
    while "*" in texto:
        texto = texto.replace("*", "<em>", 1).replace("*", "</em>", 1)
    return texto


# ---------------------------------------------------------------- animación

CSS_REEL = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:var(--bg);color:var(--txt);
  font-family:'Inter',sans-serif;overflow:hidden;position:relative}

/* el marco de contenido, centrado verticalmente */
.escena{position:absolute;inset:0;padding:150px 90px 230px;
  display:flex;flex-direction:column;justify-content:center;
  opacity:0;animation:paso var(--dur) both}
.escena.h1x{justify-content:center}
@keyframes paso{
  0%   {opacity:0;transform:translateY(46px) scale(.985)}
  7%   {opacity:1;transform:translateY(0) scale(1)}
  88%  {opacity:1;transform:translateY(0) scale(1)}
  100% {opacity:0;transform:translateY(-30px) scale(.99)}
}

.gancho{font-family:'Grotesk';font-weight:700;font-size:104px;line-height:1.03;
  letter-spacing:-.03em}
.gancho em{font-style:normal;color:var(--mint)}
.beat{font-family:'Grotesk';font-weight:700;font-size:86px;line-height:1.08;
  letter-spacing:-.025em}
.beat em{font-style:normal;color:var(--mint)}
.pie-beat{font-size:40px;line-height:1.4;color:var(--muted);margin-top:40px;max-width:820px}

/* numerito del beat */
.paso-num{font-family:'Mono';font-weight:700;font-size:34px;letter-spacing:.2em;
  color:var(--blue);margin-bottom:34px}

/* cierre */
.cierre{align-items:flex-start}
.cierre .marca{display:flex;align-items:center;gap:22px;margin-bottom:52px}
.cierre .mk{width:96px;height:96px;border-radius:26px;position:relative;
  background:linear-gradient(150deg,var(--blue),#2B3EE8);
  box-shadow:0 18px 46px rgba(79,124,255,.45)}
.cierre .mk i{position:absolute;width:14px;height:14px;border-radius:50%;background:#fff}
.cierre .mk i:nth-child(1){top:26px;left:41px}
.cierre .mk i:nth-child(2){bottom:26px;left:25px}
.cierre .mk i:nth-child(3){bottom:26px;right:25px}
.cierre .mk-txt{font-family:'Grotesk';font-weight:700;font-size:40px;letter-spacing:.14em}
.cierre .mk-txt span{color:var(--mint)}
.cierre .lema{font-family:'Grotesk';font-weight:700;font-size:74px;line-height:1.1;
  letter-spacing:-.02em}
.cierre .lema em{font-style:normal;color:var(--mint)}
.cierre .accion{margin-top:46px;display:inline-flex;align-items:center;gap:18px;
  font-family:'Grotesk';font-weight:700;font-size:44px;color:var(--bg);
  background:var(--mint);border-radius:999px;padding:26px 46px}

/* barrita de progreso arriba */
.barra{position:absolute;top:0;left:0;height:9px;background:var(--mint);
  width:0;animation:avanza var(--total) linear both;z-index:9}
@keyframes avanza{from{width:0}to{width:1080px}}

/* firma fija abajo */
.firma{position:absolute;left:90px;bottom:120px;display:flex;align-items:center;gap:18px;
  font-family:'Mono';font-size:36px;color:var(--muted);z-index:8}
.firma u{width:14px;height:14px;border-radius:50%;background:var(--blue);
  text-decoration:none;display:block}
"""


def armar_html(reel, bg):
    """Cada escena arranca cuando termina la anterior, con animation-delay."""
    escenas = []
    t = 0.0

    def add(cuerpo, dur, clase=""):
        nonlocal t
        escenas.append(
            f"<div class='escena {clase}' style=\"--dur:{dur}s;animation-delay:{t}s\">"
            f"{cuerpo}</div>")
        t += dur

    add(f"<div class='gancho'>{resaltar(reel['gancho'])}</div>", reel.get("dur_gancho", 3.6))

    for i, b in enumerate(reel["beats"]):
        pie = f"<div class='pie-beat'>{resaltar(b['pie'])}</div>" if b.get("pie") else ""
        num = (f"<div class='paso-num'>{i+1:02d}</div>"
               if reel.get("numerar", True) else "")
        add(f"{num}<div class='beat'>{resaltar(b['texto'])}</div>{pie}",
            b.get("dur", 4.2))

    add("<div class='marca'><div class='mk'><i></i><i></i><i></i></div>"
        "<div class='mk-txt'>AXIOMA<span>.</span>SOFTWARE</div></div>"
        f"<div class='lema'>{resaltar(reel.get('lema', 'Software *a tu medida*'))}</div>"
        f"<div class='accion'>{reel['cta_video']}</div>",
        reel.get("dur_cierre", 4.4), "cierre")

    total = t
    # Todo el sistema visual (tipografías, paleta y los 9 fondos) y encima
    # las reglas del vertical, que pisan lo que haga falta.
    css = brand.CSS + CSS_REEL
    cuerpo = "".join(escenas)
    html = (f"<html><head><meta charset='utf-8'><style>{css}</style></head>"
            f"<body style='--total:{total}s'>{brand.fondo(bg)}"
            f"<div class='barra'></div>{cuerpo}"
            f"<div class='firma'><u></u>@axiomasoftwareok</div></body></html>")
    return html, total


# ---------------------------------------------------------------- render

async def grabar(html, carpeta_tmp, segundos):
    """Captura cuadro por cuadro moviendo el reloj de las animaciones a mano.

    Grabar en tiempo real deja el video fuera de sincronía con los tiempos
    que definimos en CSS. Acá congelamos las animaciones y las adelantamos
    nosotros, así cada cuadro cae exactamente donde tiene que caer.
    """
    from playwright.async_api import async_playwright
    tmp_html = RAIZ / "_reel.html"
    tmp_html.write_text(html, encoding="utf-8")
    total = int(round((segundos + EXTRA_FINAL) * FPS))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--disable-lcd-text"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920},
                              device_scale_factor=1)
        await pg.goto(f"file://{tmp_html}")
        await pg.wait_for_timeout(700)          # que terminen de cargar las fuentes
        await pg.evaluate("document.getAnimations().forEach(a => a.pause())")
        for i in range(total):
            ms = i * 1000 / FPS
            await pg.evaluate(
                "t => document.getAnimations().forEach(a => a.currentTime = t)", ms)
            await pg.screenshot(path=str(carpeta_tmp / f"f{i:05d}.jpg"),
                                type="jpeg", quality=92)
        await b.close()
    tmp_html.unlink()
    return carpeta_tmp / "f%05d.jpg"


def elegir_pista(idx):
    carpeta = RAIZ / "audio"
    if not carpeta.exists():
        return None
    pistas = sorted(p for p in carpeta.iterdir()
                    if p.suffix.lower() in (".mp3", ".m4a", ".aac", ".wav", ".ogg"))
    return pistas[idx % len(pistas)] if pistas else None


def a_mp4(patron, destino, segundos, pista):
    """Instagram quiere H.264 + AAC, yuv420p, dimensiones pares."""
    dur = round(segundos + EXTRA_FINAL, 2)
    cmd = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(patron)]
    if pista:
        # la pista se recorta al largo del video y se apaga al final
        cmd += ["-stream_loop", "-1", "-i", str(pista)]
        audio = ["-filter:a", f"afade=t=out:st={max(dur-1.5, 0):.2f}:d=1.5,volume=0.85"]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        audio = []
    cmd += [
        "-map", "0:v:0", "-map", "1:a:0",
        "-t", str(dur),
        "-r", str(FPS),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p",
        "-vf", "scale=1080:1920:flags=lanczos",
        "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
        *audio,
        "-movflags", "+faststart",
        "-shortest", str(destino),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ffmpeg falló:\n" + r.stderr[-3000:])


def caption(reel, idx):
    return (f"{reel['copy']}\n\n{reel['cta']}\n\n"
            f"{SEPARADOR}\n\n{HASHTAGS[idx % len(HASHTAGS)]}\n")


def main():
    hoy = dt.date.fromisoformat(os.environ.get("FECHA") or dt.date.today().isoformat())
    reel, idx = reel_de_hoy(hoy)
    bg = idx % len(brand.FONDOS)

    salida = RAIZ / "reels"
    salida.mkdir(exist_ok=True)
    mp4 = salida / f"{hoy}.mp4"
    tmp = RAIZ / "_video_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    html, segundos = armar_html(reel, bg)
    cuadros = asyncio.run(grabar(html, tmp, segundos))
    pista = elegir_pista(idx)
    a_mp4(cuadros, mp4, segundos, pista)
    shutil.rmtree(tmp)

    (salida / f"{hoy}.txt").write_text(caption(reel, idx), encoding="utf-8")

    peso = mp4.stat().st_size / 1e6
    print(f"Generado {mp4.name} — reel {idx+1} — {segundos + EXTRA_FINAL:.1f}s — "
          f"{peso:.1f} MB — audio: {pista.name if pista else 'silencio'}")
    if pista is None:
        print("::warning::No hay pistas en audio/. El reel sale mudo. "
              "Subí 3 o 4 mp3 de licencia libre a esa carpeta.")

    if (gh := os.environ.get("GITHUB_OUTPUT")):
        with open(gh, "a") as f:
            f.write(f"archivo={mp4.name}\nfecha={hoy}\nnumero={idx+1}\n")


if __name__ == "__main__":
    main()
