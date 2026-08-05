# -*- coding: utf-8 -*-
"""Genera la imagen y el caption del post del día.

Salida:
  posts/AAAA-MM-DD.jpg   imagen 1080x1350 lista para Instagram
  posts/AAAA-MM-DD.txt   caption listo para publicar
"""
import json, os, pathlib, asyncio, datetime as dt, sys
from playwright.async_api import async_playwright
from PIL import Image

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import brand

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INICIO = dt.date(2026, 8, 4)          # día 1 del ciclo
# Cuatro hashtags bien elegidos rinden igual que diez y no ensucian el pie.
HASHTAGS = [
 "#automatizacion #software #gestion #emprendedores",
 "#desarrolloweb #sistemas #turnos #pymes",
 "#softwareamedida #automatizacion #ecommerce #productividad",
]
SEPARADOR = "\u00b7  \u00b7  \u00b7"


def post_de_hoy(hoy):
    posts = json.loads((RAIZ / "contenido" / "calendario.json").read_text(encoding="utf-8"))
    idx = (hoy - INICIO).days
    if idx < 0:
        raise SystemExit("El ciclo todavía no arrancó.")
    if idx >= len(posts):
        raise SystemExit(
            f"Se acabó el calendario ({len(posts)} posts). Pedile a Claude el próximo lote "
            f"y actualizá contenido/calendario.json.")
    return posts[idx], idx


def _wrap(palabras, ancho):
    lineas, actual = [], ""
    for p in palabras:
        if actual and len(actual) + 1 + len(p) > ancho:
            lineas.append(actual); actual = p
        else:
            actual = f"{actual} {p}".strip()
    if actual:
        lineas.append(actual)
    return lineas


def cortar(texto, max_lineas=5, ancho_max=17):
    """Corta el titulo en renglones parejos y resalta lo marcado con *asteriscos*."""
    palabras = texto.split()
    mejor = None
    for ancho in range(10, ancho_max + 1):
        lineas = _wrap(palabras, ancho)
        if len(lineas) > max_lineas or max(len(l) for l in lineas) > ancho_max:
            continue
        desparejo = max(len(l) for l in lineas) - min(len(l) for l in lineas)
        clave = (len(lineas), desparejo)
        if mejor is None or clave < mejor[0]:
            mejor = (clave, lineas)
    lineas = mejor[1] if mejor else _wrap(palabras, ancho_max)

    if "*" not in texto:
        lineas[-1] = f"<em>{lineas[-1]}</em>"
    html = "<br>".join(lineas)
    while "*" in html:
        html = html.replace("*", "<em>", 1).replace("*", "</em>", 1)
    return html


# La CTA del pie va corta: la larga va en el caption, no en la imagen.
CTA_PIE = {
    "Axioma": "Guardalo",
    "Tip aplicable": "Seguime",
    "Servicio": "Escribime por DM",
    "Mini-guía": "Guardalo",
    "Para el que decide": "Hablemos por DM",
    "Detrás de escena": "Seguime",
    "Conversación": "Te leo abajo",
}


def cta_pie(pilar):
    return CTA_PIE.get(pilar, "Seguime")


def armar_html(post):
    pilar = post["pilar"]
    titulo = cortar(post["gancho"])
    cuerpo = post["copy"]
    pie = cta_pie(pilar)

    # Los posts que esperan datos o capturas tuyas se generan como borrador
    # y NO se publican solos.
    if "[COMPLETAR" in cuerpo:
        return brand.captura(pilar, titulo, "axioma · borrador",
                             "ACÁ VA TU CAPTURA<br>O TUS NÚMEROS REALES", pie), False

    items = [l.lstrip("0123456789. ") for l in cuerpo.split("\n")
             if l.strip() and l.strip()[0].isdigit()][:3]
    if items:
        return brand.tip(pilar, titulo, items, pie), True

    primera = cuerpo.split("\n\n")[0]
    return brand.axioma(titulo, primera, pie), True


def caption(post, idx):
    """El gancho ya esta gritado en la imagen: el caption arranca donde ella termina."""
    return (f"{post['copy']}\n\n{post['cta']}\n\n"
            f"{SEPARADOR}\n\n{HASHTAGS[idx % len(HASHTAGS)]}\n")


async def render(html, destino_jpg):
    tmp = RAIZ / "_tmp.html"
    tmp.write_text(html, encoding="utf-8")
    png = destino_jpg.with_suffix(".png")
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350},
                              device_scale_factor=1)
        await pg.goto(f"file://{tmp}")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=str(png))
        await b.close()
    tmp.unlink()
    # Instagram solo acepta JPEG en la API de publicación
    Image.open(png).convert("RGB").save(destino_jpg, "JPEG", quality=92, optimize=True)
    png.unlink()


def main():
    hoy = dt.date.fromisoformat(os.environ.get("FECHA") or dt.date.today().isoformat())
    post, idx = post_de_hoy(hoy)
    salida = RAIZ / "posts"
    salida.mkdir(exist_ok=True)
    jpg = salida / f"{hoy}.jpg"
    html, listo = armar_html(post)
    asyncio.run(render(html, jpg))
    (salida / f"{hoy}.txt").write_text(caption(post, idx), encoding="utf-8")

    print(f"Generado {jpg.name} — día {idx+1} del ciclo — pilar {post['pilar']}")
    if not listo:
        print("::warning::Borrador: este post necesita tus datos o tu captura. "
              "No se publica solo.")

    if (gh := os.environ.get("GITHUB_OUTPUT")):
        with open(gh, "a") as f:
            f.write(f"archivo={jpg.name}\nfecha={hoy}\npilar={post['pilar']}\n"
                    f"listo={'true' if listo else 'false'}\n")


if __name__ == "__main__":
    main()
