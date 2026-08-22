# -*- coding: utf-8 -*-
"""Cosecha de métricas de Instagram.

Corre una vez por semana y guarda una foto de cómo viene cada publicación:
likes, comentarios, alcance, guardados. No decide nada ni publica nada.
La idea es tener historia acumulada para poder mirar, en dos meses, qué
funcionó de verdad en vez de acordarse de memoria.

Nunca falla el workflow por una métrica que Meta no devuelve: si un dato
no está, lo deja vacío y sigue.
"""
import csv
import datetime as dt
import json
import os
import pathlib
import urllib.error
import urllib.parse
import urllib.request

API = "https://graph.instagram.com/v23.0"
RAIZ = pathlib.Path(__file__).resolve().parent.parent
CARPETA = RAIZ / "metricas"
HISTORIAL = CARPETA / "historial.csv"

COLUMNAS = ["fecha_medicion", "id", "publicado", "tipo", "permalink",
            "likes", "comentarios", "alcance", "guardados", "compartidos",
            "reproducciones", "titulo"]


def pedir(url):
    with urllib.request.urlopen(url, timeout=45) as r:
        return json.loads(r.read().decode("utf-8"))


def publicaciones(uid, token, limite=60):
    campos = "id,caption,timestamp,media_type,permalink,like_count,comments_count"
    url = f"{API}/{uid}/media?" + urllib.parse.urlencode(
        {"fields": campos, "limit": limite, "access_token": token})
    salida = []
    while url and len(salida) < limite:
        d = pedir(url)
        salida += d.get("data", [])
        url = d.get("paging", {}).get("next")
    return salida[:limite]


def insights(mid, token, tipo, quejas):
    """Las métricas de reel y de foto no son las mismas, y Meta rechaza el
    pedido entero si una sola métrica no aplica. Por eso las pido de a una:
    así una que falle no se lleva puestas a las demás.

    Los motivos de rechazo se juntan en `quejas` y se imprimen una sola vez
    al final, para saber qué pasó sin llenar el log de ruido."""
    if tipo == "VIDEO":
        metricas = ["reach", "saved", "shares", "views", "total_interactions"]
    else:
        metricas = ["reach", "saved", "shares", "total_interactions"]

    salida = {}
    for m in metricas:
        try:
            url = f"{API}/{mid}/insights?" + urllib.parse.urlencode(
                {"metric": m, "access_token": token})
            d = pedir(url)
            for x in d.get("data", []):
                if x.get("values"):
                    salida[x["name"]] = x["values"][0].get("value")
        except urllib.error.HTTPError as e:
            try:
                cuerpo = json.loads(e.read().decode("utf-8"))
                motivo = cuerpo.get("error", {}).get("message", str(e))
            except Exception:
                motivo = str(e)
            quejas.setdefault(f"{tipo}/{m}", motivo)
        except Exception as e:
            quejas.setdefault(f"{tipo}/{m}", str(e))
    return salida


def main():
    uid = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]
    hoy = dt.date.today().isoformat()

    try:
        medios = publicaciones(uid, token)
    except Exception as e:
        print(f"::warning::No pude leer las publicaciones ({e}). "
              f"No guardo nada esta semana.")
        raise SystemExit(0)

    filas = []
    quejas = {}
    for m in medios:
        ins = insights(m["id"], token, m.get("media_type", ""), quejas)
        titulo = (m.get("caption") or "").split("\n")[0][:90]
        filas.append({
            "fecha_medicion": hoy,
            "id": m["id"],
            "publicado": (m.get("timestamp") or "")[:10],
            "tipo": m.get("media_type", ""),
            "permalink": m.get("permalink", ""),
            "likes": m.get("like_count", ""),
            "comentarios": m.get("comments_count", ""),
            "alcance": ins.get("reach", ""),
            "guardados": ins.get("saved", ""),
            "compartidos": ins.get("shares", ""),
            "reproducciones": ins.get("views", ""),
            "titulo": titulo,
        })

    CARPETA.mkdir(exist_ok=True)
    (CARPETA / f"{hoy}.json").write_text(
        json.dumps(filas, ensure_ascii=False, indent=2), encoding="utf-8")

    # Si ya se midió hoy (por ejemplo porque alguien corrió el workflow a
    # mano), reemplazo esas filas en vez de sumarlas: dos mediciones del
    # mismo día contarían doble cuando después se analicen los datos.
    previas = []
    if HISTORIAL.exists():
        with open(HISTORIAL, newline="", encoding="utf-8") as f:
            previas = [r for r in csv.DictReader(f)
                       if r.get("fecha_medicion") != hoy]
    with open(HISTORIAL, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNAS)
        w.writeheader()
        w.writerows(previas)
        w.writerows(filas)

    print(f"Medidas {len(filas)} publicaciones. Historial: {HISTORIAL.name}")
    if quejas:
        print("\nMétricas que Meta no devolvió (y por qué):")
        for k, v in quejas.items():
            print(f"  · {k}: {v}")


if __name__ == "__main__":
    main()
