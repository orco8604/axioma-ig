# -*- coding: utf-8 -*-
"""Publica en Instagram vía la API de Meta (Instagram API with Instagram Login).

Proceso en dos pasos, como pide Meta:
  1. crear un contenedor de medios apuntando a la URL pública de la imagen
  2. publicar ese contenedor

Variables de entorno necesarias:
  IG_USER_ID       id numérico de la cuenta de Instagram
  IG_ACCESS_TOKEN  token de larga duración
  IMAGE_URL        URL pública de la imagen (raw.githubusercontent.com)
  CAPTION_FILE     ruta al .txt con el caption
"""
import os, sys, time, json, urllib.parse, urllib.request

API = "https://graph.instagram.com/v23.0"


def llamar(metodo, ruta, datos):
    url = f"{API}/{ruta}"
    cuerpo = urllib.parse.urlencode(datos).encode()
    req = urllib.request.Request(url, data=cuerpo if metodo == "POST" else None,
                                 method=metodo)
    if metodo == "GET":
        req = urllib.request.Request(f"{url}?{urllib.parse.urlencode(datos)}")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        detalle = e.read().decode(errors="replace")
        raise SystemExit(f"Error {e.code} de la API de Instagram:\n{detalle}")


def main():
    uid = os.environ["IG_USER_ID"]
    token = os.environ["IG_ACCESS_TOKEN"]
    image_url = os.environ["IMAGE_URL"]
    caption = open(os.environ["CAPTION_FILE"], encoding="utf-8").read().strip()

    print(f"Imagen: {image_url}")
    cont = llamar("POST", f"{uid}/media", {
        "image_url": image_url,
        "caption": caption,
        "access_token": token,
    })
    cid = cont["id"]
    print(f"Contenedor creado: {cid}")

    # Meta procesa la imagen de forma asincrónica: esperamos a que quede lista
    for intento in range(20):
        est = llamar("GET", cid, {"fields": "status_code,status",
                                  "access_token": token})
        code = est.get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise SystemExit(f"Meta rechazó la imagen: {est.get('status')}")
        print(f"  procesando... ({code})")
        time.sleep(6)
    else:
        raise SystemExit("El contenedor nunca quedó listo. Reintentá más tarde.")

    pub = llamar("POST", f"{uid}/media_publish", {
        "creation_id": cid,
        "access_token": token,
    })
    print(f"PUBLICADO. id del post: {pub['id']}")

    # Dejamos constancia para que ninguna otra corrida vuelva a publicar lo mismo.
    registro = os.environ.get("REGISTRO")
    fecha = os.environ.get("FECHA")
    if registro and fecha:
        ya = []
        if os.path.exists(registro):
            ya = open(registro, encoding="utf-8").read().split()
        if fecha not in ya:
            with open(registro, "a", encoding="utf-8") as f:
                f.write(fecha + "\n")
        print(f"Anotado en {registro}")


if __name__ == "__main__":
    main()
