# axioma-ig

Publica un post por día en Instagram (`@axiomasoftwareok`), solo, desde GitHub Actions.

Cada día a las 13:00 (hora argentina) el workflow:

1. busca en `contenido/calendario.json` qué post toca,
2. genera la imagen 1080×1350 en JPEG con el sistema visual de la marca,
3. la commitea al repo (así queda con URL pública, que es lo que pide la API de Meta),
4. la publica en Instagram.

Los posts marcados como borrador (los que esperan un dato o una captura tuya) **se generan
pero no se publican**: aparecen en `posts/` para que los mires y los subas a mano.

---

## Puesta en marcha

### 1. El repo

Tiene que ser **público**. La API de Meta descarga la imagen desde una URL pública
(`raw.githubusercontent.com`), así que el repo público es lo que hace que esto sea gratis.
Los secretos van en Settings → Secrets, nunca en el código: que el repo sea público no
expone el token.

```bash
git init
git add .
git commit -m "primer commit"
git branch -M main
git remote add origin https://github.com/USUARIO/axioma-ig.git
git push -u origin main
```

Después, en el repo: **Settings → Actions → General → Workflow permissions →
Read and write permissions**.

### 2. La cuenta de Instagram

- Cuenta **profesional tipo Empresa** (no Creador).
- **Pública**, no privada.
- 2FA activado.

### 3. La app en Meta for Developers

1. Entrá a [developers.facebook.com/apps](https://developers.facebook.com/apps) → **Crear app**.
2. Caso de uso: **Otro** → tipo **Empresa**.
3. Agregá el producto **Instagram** → *API de Instagram con inicio de sesión de Instagram*.
4. En **Configuración de la API con inicio de sesión de Instagram**, vinculá la cuenta
   `@axiomasoftwareok`.
5. Generá el token con estos permisos:
   - `instagram_business_basic`
   - `instagram_business_content_publish`
6. Copiá el **token de larga duración** (dura 60 días) y el **id de la cuenta de Instagram**
   (un número largo, aparece en la misma pantalla).

Mientras la app esté en modo desarrollo alcanza con tu propia cuenta: no hace falta
revisión de Meta para publicar en la cuenta que sos dueño.

### 4. Los secrets

En el repo: **Settings → Secrets and variables → Actions → New repository secret**.

| Secret | Qué es | Obligatorio |
|---|---|---|
| `IG_USER_ID` | El id numérico de la cuenta de Instagram | sí |
| `IG_ACCESS_TOKEN` | El token de larga duración | sí |
| `GH_PAT` | Token personal de GitHub (fine-grained, solo este repo, permiso *Secrets: Read and write*) | solo para el refresco automático |

Sin `GH_PAT` todo funciona igual, pero cada 60 días tenés que pegar el token nuevo a mano.
Con él, el workflow `refrescar-token.yml` lo renueva solo cada 3 semanas.

### 5. Probar sin publicar

En la pestaña **Actions** → *Publicar en Instagram* → **Run workflow**, poné
`solo_generar` en `true`. Genera la imagen y la sube al repo sin tocar Instagram.
Cuando el resultado te guste, corré de nuevo sin esa opción.

---

## Uso diario

No hay uso diario. Anda solo.

Lo único que aparece cada tanto:

- **Un post en borrador.** Lo vas a ver en `posts/` con el marco vacío. Metele la captura
  o los números reales y subilo a mano.
- **El calendario se termina.** Trae 30 posts. Cuando se acaba, el workflow falla con un
  mensaje claro y te avisa por mail. Pedile a Claude el próximo lote y reemplazá
  `contenido/calendario.json`.

## Cambiar cosas

| Qué | Dónde |
|---|---|
| La hora de publicación | `cron` en `.github/workflows/publicar.yml` (está en UTC: restale 3 horas para saber la hora argentina) |
| Los textos de los posts | `contenido/calendario.json` |
| Colores, tipografías, diseño | `scripts/brand.py` |
| El día en que arranca el ciclo | `INICIO` en `scripts/generar.py` |
| Los hashtags | `HASHTAGS` en `scripts/generar.py` |

## Límites que conviene saber

- Instagram permite **25 publicaciones por API cada 24 horas**. Uno por día queda muy lejos.
- La API acepta **solo JPEG** para fotos. El generador ya convierte.
- Relación de aspecto entre 4:5 y 1.91:1. Las imágenes salen en 1080×1350 (4:5), que es
  lo que más pantalla ocupa en el feed y entra completo en la grilla del perfil.
