# -*- coding: utf-8 -*-
"""Avisa cuánto contenido queda antes de que la cuenta se quede muda.

No falla nunca: escribe el resultado en la salida del workflow para que
el aviso salga por un issue y no por un mail de error.
"""
import datetime as dt
import json
import os
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
INICIO = dt.date(2026, 8, 4)
DIAS_REEL = (0, 2, 4)
AVISAR_DIAS = 21


def ultimo_dia(n, solo_reel=False):
    """Devuelve la fecha de la última pieza planificada."""
    fecha, quedan = INICIO, n
    while quedan:
        if not solo_reel or fecha.weekday() in DIAS_REEL:
            quedan -= 1
            ultimo = fecha
        fecha += dt.timedelta(days=1)
    return ultimo


def main():
    hoy = dt.date.today()
    posts = json.loads((RAIZ / "contenido" / "calendario.json").read_text("utf-8"))
    reels = json.loads((RAIZ / "contenido" / "reels.json").read_text("utf-8"))

    fin_post = ultimo_dia(len(posts))
    fin_reel = ultimo_dia(len(reels), solo_reel=True)
    d_post = (fin_post - hoy).days
    d_reel = (fin_reel - hoy).days

    print(f"Posts: {len(posts)} planificados, último el {fin_post} ({d_post} días).")
    print(f"Reels: {len(reels)} planificados, último el {fin_reel} ({d_reel} días).")

    urge = min(d_post, d_reel) <= AVISAR_DIAS
    cuerpo = (
        f"Los posts alcanzan hasta el **{fin_post}** ({d_post} días).\n"
        f"Los reels alcanzan hasta el **{fin_reel}** ({d_reel} días).\n\n"
        f"Cuando se termina el contenido la cuenta no rompe nada: los workflows "
        f"avisan y no publican. Pero deja de salir.\n\n"
        f"Para renovar: pedile a Claude el próximo lote y actualizá "
        f"`contenido/calendario.json` y `contenido/reels.json`.")

    if (gh := os.environ.get("GITHUB_OUTPUT")):
        with open(gh, "a") as f:
            f.write(f"urge={'true' if urge else 'false'}\n")
            f.write(f"fin_post={fin_post}\nfin_reel={fin_reel}\n")
            f.write("cuerpo<<FIN\n" + cuerpo + "\nFIN\n")


if __name__ == "__main__":
    main()
