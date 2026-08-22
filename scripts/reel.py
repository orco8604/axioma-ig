# -*- coding: utf-8 -*-
"""Genera un reel vertical (1080x1920) mostrando el producto funcionando.

Cómo funciona:
  1. scripts/guiones.py arma la escena en HTML+CSS (cada guion es distinto)
  2. Playwright la captura cuadro por cuadro, moviendo el reloj a mano
  3. ffmpeg la pasa a MP4 (H.264 + AAC), que es lo que acepta Instagram
  4. si hay pistas en audio/, le pega una; si no, va una pista de silencio

Salida:
  reels/AAAA-MM-DD.mp4   video listo para publicar
  reels/AAAA-MM-DD.txt   caption listo para publicar
"""
import json, os, pathlib, asyncio, subprocess, datetime as dt, sys, shutil

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import brand, guiones

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INICIO = dt.date(2026, 8, 4)      # mismo día 1 que el calendario de estáticos
DIAS_REEL = (0, 2, 4)             # lunes, miércoles, viernes
FPS = 30
CIERRE = 4.6                      # lo que dura la placa final

HASHTAGS = [
    "#automatizacion #software #gestion #emprendedores",
    "#desarrolloweb #sistemas #turnos #pymes",
    "#softwareamedida #automatizacion #ecommerce #productividad",
]
SEPARADOR = "·  ·  ·"

CSS_CIERRE = r"""
/* ---------- la cámara: cada guion elige la suya ---------- */
.camara{position:absolute;inset:0;transform-origin:50% 46%}
.camara.fija{}
/* Regla: ninguna camara pasa de escala 1.06. Arriba de eso se recorta mas
   del 6% del cuadro y lo que se muestra deja de leerse, que es justo lo
   contrario de lo que tiene que hacer un reel. El movimiento se nota igual:
   lo que da vida es el cambio, no la cantidad de zoom. */
.camara.empuje{animation:camEmpuje var(--total) cubic-bezier(.35,0,.25,1) both}
@keyframes camEmpuje{0%{transform:scale(1)}100%{transform:scale(1.05) translateY(-14px)}}
.camara.lateral{animation:camLateral var(--total) cubic-bezier(.4,0,.35,1) both}
@keyframes camLateral{0%{transform:scale(1.06) translateX(30px)}
                      100%{transform:scale(1.06) translateX(-30px)}}
.camara.retiro{animation:camRetiro var(--total) cubic-bezier(.25,.6,.2,1) both}
@keyframes camRetiro{0%{transform:scale(1.06) translate(-14px,26px)}
                     46%{transform:scale(1.01)}
                     100%{transform:scale(1)}}
.camara.vaiven{animation:camVaiven var(--total) ease-in-out both}
@keyframes camVaiven{0%{transform:scale(1.03) translateX(-20px)}
                     50%{transform:scale(1.01) translateX(18px)}
                     100%{transform:scale(1.05) translateX(-10px)}}

.prog{position:absolute;top:0;left:0;height:9px;background:#7CFFCB;width:0;
  animation:avanza var(--total) linear both;z-index:30}
@keyframes avanza{to{width:1080px}}
.firma{position:absolute;left:0;right:0;bottom:450px;text-align:center;
  font-family:'Mono';font-size:34px;color:#8B99B0;z-index:9}
.firma.oculta{display:none}

/* ---------- cierres: cuatro placas distintas ----------
   Ojo con los margenes de abajo: la interfaz de reels de Instagram
   (nombre de cuenta, caption, audio) tapa los ultimos ~420 px. El boton
   de CTA y el arroba tienen que quedar por encima de esa franja o no se
   ven, que es justo lo unico que no puede pasar en la placa final. */
.fin{position:absolute;inset:0;z-index:20;opacity:0;
  animation:apareceFin var(--fd) both}
@keyframes apareceFin{0%{opacity:0}9%{opacity:1}100%{opacity:1}}
.fin .mk{width:150px;height:150px;border-radius:42px;position:relative;flex:none;
  background:linear-gradient(150deg,#4F7CFF,#2B3EE8);
  box-shadow:0 26px 70px rgba(79,124,255,.5)}
.fin .mk i{position:absolute;width:22px;height:22px;border-radius:50%;background:#fff}
.fin .mk i:nth-child(1){top:40px;left:64px}
.fin .mk i:nth-child(2){bottom:40px;left:38px}
.fin .mk i:nth-child(3){bottom:40px;right:38px}
.fin .lm{font-family:'Grotesk';font-weight:700;letter-spacing:-.03em;line-height:1.04}
.fin .lm em{font-style:normal;color:#7CFFCB}
.fin .btn{font-family:'Grotesk';font-weight:700;color:#070A11;background:#7CFFCB;
  border-radius:999px}
.fin .ar{font-family:'Mono';color:#8B99B0}

/* a · placa oscura centrada */
.fin.centro{display:flex;flex-direction:column;align-items:center;justify-content:center;
  background:radial-gradient(78% 46% at 50% 44%,rgba(32,50,88,.55) 0%,transparent 72%),#070A11;
  text-align:center}
.fin.centro .mk{margin-bottom:52px;
  animation:giraMarca 9s ease-in-out infinite}
@keyframes giraMarca{0%,100%{transform:perspective(900px) rotateY(-16deg) rotateX(8deg)}
                     50%{transform:perspective(900px) rotateY(16deg) rotateX(-6deg)}}
.fin.centro .lm{font-size:86px;padding:0 70px}
.fin.centro .sub{font-size:38px;color:#8B99B0;margin-top:28px;line-height:1.4}
.fin.centro .btn{margin-top:58px;font-size:46px;padding:30px 58px;
  box-shadow:0 22px 60px rgba(124,255,203,.32)}
.fin.centro .ar{margin-top:36px;font-size:32px}

/* b · placa clara, al revés: fondo menta y texto oscuro */
.fin.claro{display:flex;flex-direction:column;justify-content:flex-end;
  background:#7CFFCB;color:#070A11;padding:0 92px 440px}
.fin.claro .mk{width:112px;height:112px;border-radius:32px;margin-bottom:44px;
  background:#070A11;box-shadow:none}
.fin.claro .mk i{background:#7CFFCB;width:17px;height:17px}
.fin.claro .mk i:nth-child(1){top:30px;left:47px}
.fin.claro .mk i:nth-child(2){bottom:30px;left:28px}
.fin.claro .mk i:nth-child(3){bottom:30px;right:28px}
.fin.claro .lm{font-size:96px}
.fin.claro .lm em{color:#0B7A55}
.fin.claro .sub{font-size:36px;color:rgba(7,10,17,.62);margin-top:26px;line-height:1.4}
.fin.claro .btn{align-self:flex-start;margin-top:52px;font-size:44px;padding:28px 54px;
  background:#070A11;color:#7CFFCB}
.fin.claro .ar{margin-top:30px;font-size:30px;color:rgba(7,10,17,.55)}

/* c · panel que sube y deja ver la escena atrás */
.fin.panel{display:flex;flex-direction:column;justify-content:flex-end;
  background:linear-gradient(180deg,transparent 0%,rgba(7,10,17,.62) 26%,#070A11 58%)}
.fin.panel .caja{margin:0 64px 380px;background:rgba(12,18,32,.94);
  border:1px solid rgba(124,255,203,.28);border-radius:38px;padding:56px 58px;
  box-shadow:0 40px 110px rgba(0,0,0,.7);
  animation:sube-panel .9s cubic-bezier(.2,.9,.25,1) both}
@keyframes sube-panel{from{opacity:0;transform:translateY(150px)}to{opacity:1;transform:none}}
.fin.panel .fila{display:flex;align-items:center;gap:26px;margin-bottom:34px}
.fin.panel .mk{width:92px;height:92px;border-radius:26px}
.fin.panel .mk i{width:14px;height:14px}
.fin.panel .mk i:nth-child(1){top:25px;left:39px}
.fin.panel .mk i:nth-child(2){bottom:25px;left:23px}
.fin.panel .mk i:nth-child(3){bottom:25px;right:23px}
.fin.panel .lm{font-size:64px}
.fin.panel .sub{font-size:34px;color:#8B99B0;line-height:1.4}
.fin.panel .btn{display:inline-block;margin-top:40px;font-size:40px;padding:26px 46px}
.fin.panel .ar{margin-top:26px;font-size:28px}

/* d · franja diagonal: mitad menta, mitad oscuro */
.fin.franja{display:flex;flex-direction:column;justify-content:flex-start;
  background:#070A11;padding:250px 78px 460px;overflow:hidden}
.fin.franja::before{content:'';position:absolute;inset:-20% -30%;background:#7CFFCB;
  transform:rotate(-13deg) translateY(58%);transform-origin:50% 50%}
.fin.franja>*{position:relative;z-index:2}
.fin.franja .mk{width:120px;height:120px;border-radius:34px;margin-bottom:40px}
.fin.franja .lm{font-size:90px}
.fin.franja .sub{font-size:36px;color:#8B99B0;margin-top:26px;line-height:1.4}
.fin.franja .btn{align-self:flex-start;margin-top:auto;font-size:44px;padding:28px 54px;
  background:#7CFFCB;color:#070A11;box-shadow:0 22px 60px rgba(124,255,203,.3)}
.fin.franja .ar{margin-top:28px;font-size:30px;color:#8B99B0}
"""


# ---------------------------------------------------------------- contenido

def reel_de_hoy(hoy):
    datos = json.loads((RAIZ / "contenido" / "reels.json").read_text(encoding="utf-8"))
    if hoy.weekday() not in DIAS_REEL:
        raise SystemExit(f"El {hoy} no toca reel (solo lunes, miércoles y viernes).")
    dias = (hoy - INICIO).days
    if dias < 0:
        raise SystemExit("El ciclo todavía no arrancó.")
    idx = sum(1 for d in range(dias)
              if (INICIO + dt.timedelta(days=d)).weekday() in DIAS_REEL)
    if idx >= len(datos):
        raise SystemExit(
            f"Se acabaron los reels ({len(datos)} guionados). Pedile a Claude el "
            f"próximo lote y actualizá contenido/reels.json.")
    ficha = datos[idx]
    por_id = dict(guiones.GUIONES)
    if ficha["guion"] not in por_id:
        raise SystemExit(f"No existe el guion «{ficha['guion']}» en scripts/guiones.py.")
    return ficha, por_id[ficha["guion"]], idx


def armar_html(ficha, fabrica):
    """Cada guion trae su propio encuadre, su cámara y su placa de cierre."""
    esc = fabrica(ficha.get("datos") or {})
    total = esc["dur"] + esc.get("cierre_dur", CIERRE)
    lema = ficha.get("lema") or esc["lema"]
    cd = esc.get("cierre_dur", CIERRE)
    estilo = ficha.get("cierre_estilo") or esc.get("cierre_estilo", "centro")

    bloque = (f"<div class='mk'><i></i><i></i><i></i></div>"
              f"<div class='lm'>{lema}</div>"
              f"<div class='sub'>{ficha['cierre']}</div>"
              f"<div class='btn'>{ficha['boton']}</div>"
              f"<div class='ar'>@axiomasoftwareok</div>")
    if estilo == "panel":
        # el logo y el lema van en la misma fila, adentro de la caja
        bloque = (f"<div class='caja'>"
                  f"<div class='fila'><div class='mk'><i></i><i></i><i></i></div>"
                  f"<div class='lm'>{lema}</div></div>"
                  f"<div class='sub'>{ficha['cierre']}</div>"
                  f"<div class='btn'>{ficha['boton']}</div>"
                  f"<div class='ar'>@axiomasoftwareok</div></div>")

    fin = (f"<div class='fin {estilo}' style='--fd:{cd}s;"
           f"animation-delay:{esc['dur']}s'>{bloque}</div>")

    firma = "" if esc.get("sin_firma") else "<div class='firma'>@axiomasoftwareok</div>"
    css = brand.CSS.split("body{")[0] + guiones.CSS + CSS_CIERRE + esc.get("css", "")
    # El reel puede pisar el clima visual del encuadre: mismo molde, otra
    # foto. Asi un encuadre repetido dentro del trimestre no se ve igual.
    amb = ficha.get("amb") or esc["amb"]
    trama = ficha.get("trama") or esc["trama"]
    camara = ficha.get("camara") or esc.get("camara", "empuje")
    cuerpo = esc["cuerpo"]
    return (f"<html><head><meta charset='utf-8'><style>{css}</style></head>"
            f"<body style='--total:{total}s'>"
            f"<div class='amb {amb}'></div><div class='{trama}'></div>"
            f"<div class='prog'></div>"
            f"<div class='camara {camara}'>{cuerpo}</div>"
            f"{fin}{firma}</body></html>"), total


def caption(ficha, idx):
    return (f"{ficha['copy']}\n\n{ficha['cta']}\n\n"
            f"{SEPARADOR}\n\n{HASHTAGS[idx % len(HASHTAGS)]}\n")


# ---------------------------------------------------------------- render

async def capturar(html, tmp, segundos):
    """Congelamos las animaciones y las adelantamos nosotros: así el video
    queda exactamente sincronizado con los tiempos escritos en el guion."""
    from playwright.async_api import async_playwright
    f = RAIZ / "_reel.html"
    f.write_text(html, encoding="utf-8")
    n = int(round(segundos * FPS))
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--disable-lcd-text"])
        pg = await b.new_page(viewport={"width": 1080, "height": 1920},
                              device_scale_factor=1)
        await pg.goto(f"file://{f}")
        await pg.wait_for_timeout(700)          # que carguen las fuentes
        await pg.evaluate("document.getAnimations().forEach(a => a.pause())")
        for i in range(n):
            await pg.evaluate(
                "t => document.getAnimations().forEach(a => a.currentTime = t)",
                i * 1000 / FPS)
            await pg.screenshot(path=str(tmp / f"f{i:05d}.jpg"),
                                type="jpeg", quality=92)
        await b.close()
    f.unlink()


def elegir_pista(idx):
    carpeta = RAIZ / "audio"
    if not carpeta.exists():
        return None
    pistas = sorted(p for p in carpeta.iterdir()
                    if p.suffix.lower() in (".mp3", ".m4a", ".aac", ".wav", ".ogg"))
    return pistas[idx % len(pistas)] if pistas else None


def a_mp4(patron, destino, segundos, pista):
    """Instagram quiere H.264 + AAC, yuv420p, dimensiones pares."""
    dur = round(segundos, 2)
    cmd = ["ffmpeg", "-y", "-framerate", str(FPS), "-i", str(patron)]
    if pista:
        cmd += ["-stream_loop", "-1", "-i", str(pista)]
        audio = ["-filter:a", f"afade=t=out:st={max(dur - 1.6, 0):.2f}:d=1.6,volume=0.8"]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
        audio = []
    cmd += ["-map", "0:v:0", "-map", "1:a:0", "-t", str(dur), "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-profile:v", "high", "-level", "4.0", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-ar", "44100", "-ac", "2",
            *audio, "-movflags", "+faststart", "-shortest", str(destino)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ffmpeg falló:\n" + r.stderr[-3000:])


def main():
    hoy = dt.date.fromisoformat(os.environ.get("FECHA") or dt.date.today().isoformat())
    ficha, fabrica, idx = reel_de_hoy(hoy)

    salida = RAIZ / "reels"
    salida.mkdir(exist_ok=True)
    mp4 = salida / f"{hoy}.mp4"
    tmp = RAIZ / "_video_tmp"
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir()

    html, segundos = armar_html(ficha, fabrica)
    asyncio.run(capturar(html, tmp, segundos))
    pista = elegir_pista(idx)
    a_mp4(tmp / "f%05d.jpg", mp4, segundos, pista)
    shutil.rmtree(tmp)

    (salida / f"{hoy}.txt").write_text(caption(ficha, idx), encoding="utf-8")

    print(f"Generado {mp4.name} — reel {idx+1} «{ficha['guion']}» — "
          f"{segundos:.1f}s — {mp4.stat().st_size/1e6:.1f} MB — "
          f"audio: {pista.name if pista else 'silencio'}")
    if pista is None:
        print("::warning::No hay pistas en audio/. El reel sale mudo. "
              "Subí 3 o 4 mp3 de licencia libre a esa carpeta.")

    if (gh := os.environ.get("GITHUB_OUTPUT")):
        with open(gh, "a") as f:
            f.write(f"archivo={mp4.name}\nfecha={hoy}\nnumero={idx+1}\n")


if __name__ == "__main__":
    main()
