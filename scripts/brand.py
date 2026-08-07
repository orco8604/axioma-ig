"""Sistema visual de Axioma Software -> HTML para renderizar posts de Instagram."""

CSS = r"""
@font-face{font-family:'Inter';src:url('fonts/inter-latin-400-normal.woff2');font-weight:400}
@font-face{font-family:'Inter';src:url('fonts/inter-latin-600-normal.woff2');font-weight:600}
@font-face{font-family:'Inter';src:url('fonts/inter-latin-700-normal.woff2');font-weight:700}
@font-face{font-family:'Inter';src:url('fonts/inter-latin-900-normal.woff2');font-weight:900}
@font-face{font-family:'Grotesk';src:url('fonts/space-grotesk-latin-500-normal.woff2');font-weight:500}
@font-face{font-family:'Grotesk';src:url('fonts/space-grotesk-latin-700-normal.woff2');font-weight:700}
@font-face{font-family:'Mono';src:url('fonts/jetbrains-mono-latin-400-normal.woff2');font-weight:400}
@font-face{font-family:'Mono';src:url('fonts/jetbrains-mono-latin-700-normal.woff2');font-weight:700}

:root{
  --bg:#0A0E17; --surface:#131C2B; --line:rgba(255,255,255,.09);
  --txt:#EDF2FB; --muted:#8B99B0; --blue:#4F7CFF; --mint:#7CFFCB;
}
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:var(--bg);color:var(--txt);
  font-family:'Inter',sans-serif;overflow:hidden;position:relative}

/* fondo: grilla + halo */
.grid{position:absolute;inset:0;
  background-image:linear-gradient(var(--line) 1px,transparent 1px),
                   linear-gradient(90deg,var(--line) 1px,transparent 1px);
  background-size:90px 90px;opacity:.55}
.glow{position:absolute;width:1100px;height:1100px;border-radius:50%;
  top:-380px;right:-380px;filter:blur(10px);
  background:radial-gradient(circle,rgba(79,124,255,.30) 0%,rgba(79,124,255,.09) 42%,transparent 68%)}
.glow2{position:absolute;width:900px;height:900px;border-radius:50%;
  bottom:-460px;left:-320px;
  background:radial-gradient(circle,rgba(124,255,203,.15) 0%,transparent 66%)}

.frame{position:absolute;inset:0;padding:86px 86px 76px;display:flex;flex-direction:column}

/* cabecera */
.brand{display:flex;align-items:center;gap:16px}
.mark{width:62px;height:62px;border-radius:17px;position:relative;
  background:linear-gradient(150deg,var(--blue),#2B3EE8);
  box-shadow:0 12px 34px rgba(79,124,255,.42)}
.mark i{position:absolute;width:9px;height:9px;border-radius:50%;background:#fff}
.mark i:nth-child(1){top:17px;left:26.5px}
.mark i:nth-child(2){bottom:17px;left:16px}
.mark i:nth-child(3){bottom:17px;right:16px}
.brand-txt{font-family:'Grotesk';font-weight:700;font-size:27px;letter-spacing:.16em}
.brand-txt span{color:var(--mint)}

.eyebrow{margin-top:auto;display:inline-flex;align-items:center;gap:12px;align-self:flex-start;
  font-family:'Mono';font-weight:700;font-size:21px;letter-spacing:.15em;color:var(--mint);
  text-transform:uppercase;border:1px solid rgba(124,255,203,.32);border-radius:999px;
  padding:11px 22px;background:rgba(124,255,203,.07)}

h1{font-family:'Grotesk';font-weight:700;font-size:88px;line-height:1.04;
  letter-spacing:-.025em;margin-top:34px}
h1 em{font-style:normal;color:var(--mint)}
.sub{font-size:33px;line-height:1.45;color:var(--muted);margin-top:30px;max-width:800px}

/* listas */
.items{margin-top:52px;display:flex;flex-direction:column;gap:24px}
.item{display:flex;gap:24px;align-items:flex-start;background:var(--surface);
  border:1px solid var(--line);border-radius:22px;padding:28px 30px}
.num{flex:none;width:46px;height:46px;border-radius:13px;display:grid;place-items:center;
  background:rgba(79,124,255,.16);color:var(--blue);
  font-family:'Mono';font-weight:700;font-size:23px}
.item p{font-size:31px;line-height:1.36}
.item b{color:var(--mint);font-weight:700}

/* cita / axioma */
.quote{font-family:'Grotesk';font-weight:700;font-size:96px;line-height:1.08;
  letter-spacing:-.03em;margin-top:40px}
.quote em{font-style:normal;color:var(--mint)}
.qmark{position:relative;width:110px;height:92px}
.qmark i{position:absolute;width:22px;height:22px;border-radius:50%;background:var(--blue)}
.qmark i:nth-child(1){top:0;left:44px}
.qmark i:nth-child(2){bottom:0;left:0}
.qmark i:nth-child(3){bottom:0;left:88px}

/* stat */
.stat{margin-top:56px;display:flex;gap:26px}
.chip{flex:1;background:var(--surface);border:1px solid var(--line);border-radius:24px;padding:34px 30px}
.chip .big{font-family:'Grotesk';font-weight:700;font-size:66px;color:var(--mint);letter-spacing:-.02em}
.chip .lbl{font-size:25px;color:var(--muted);margin-top:10px;line-height:1.3}

/* pie */
.foot{margin-top:auto;padding-top:44px;border-top:1px solid var(--line);
  display:flex;justify-content:space-between;align-items:center}
.handle{font-family:'Mono';font-size:26px;color:var(--muted);white-space:nowrap;overflow:hidden}
.cta{font-family:'Grotesk';font-weight:700;font-size:26px;color:var(--txt);
  display:flex;align-items:center;gap:12px;white-space:nowrap;flex:none}
.cta i{font-style:normal;color:var(--blue);font-size:30px}
/* ---- fondos: mismas tres tintas, seis climas distintos ---- */
.dots{position:absolute;inset:0;
  background-image:radial-gradient(rgba(255,255,255,.16) 1.8px,transparent 1.8px);
  background-size:44px 44px;opacity:.55}
.diag{position:absolute;inset:0;opacity:.7;
  background-image:repeating-linear-gradient(52deg,rgba(255,255,255,.085) 0 1px,transparent 1px 24px)}
.arco{position:absolute;width:1600px;height:1600px;border-radius:50%;
  border:1.5px solid rgba(124,255,203,.22);left:-380px;top:-620px}
.arco2{position:absolute;width:1200px;height:1200px;border-radius:50%;
  border:1.5px solid rgba(79,124,255,.28);right:-360px;bottom:-470px}
.banda{position:absolute;left:0;right:0;top:0;height:700px;
  background:linear-gradient(180deg,#1B2B47 0%,#111A2C 45%,rgba(10,14,23,0) 100%)}
.brillo{position:absolute;inset:0;
  background:radial-gradient(130% 82% at 50% -6%,rgba(79,124,255,.42) 0%,rgba(79,124,255,.10) 45%,transparent 70%)}
.glow-m{position:absolute;width:1250px;height:1250px;border-radius:50%;
  top:-420px;right:-360px;filter:blur(4px);
  background:radial-gradient(circle,rgba(124,255,203,.34) 0%,rgba(124,255,203,.10) 45%,transparent 70%)}
.glow-b2{position:absolute;width:1050px;height:1050px;border-radius:50%;
  bottom:-400px;left:-300px;
  background:radial-gradient(circle,rgba(79,124,255,.30) 0%,transparent 66%)}
.tenue{position:absolute;inset:0;
  background:radial-gradient(90% 60% at 82% 88%,rgba(79,124,255,.20) 0%,transparent 65%)}
/* ---- escenas: objetos reconocibles de fondo, no solo abstracto ---- */
.esc{position:absolute;inset:0;overflow:hidden}
/* chat de WhatsApp */
.chat{position:absolute;right:-40px;bottom:-30px;width:640px;
  display:flex;flex-direction:column;gap:22px;opacity:.5;
  transform:rotate(-6deg);filter:blur(.4px)}
.bub{max-width:78%;padding:26px 30px;border-radius:26px;font-size:26px;
  background:#1B2A44;color:#8FA3C4;line-height:1.35}
.bub.yo{align-self:flex-end;background:#17453A;color:#7FD9BC;border-bottom-right-radius:8px}
.bub.el{border-bottom-left-radius:8px}
/* tablero */
.dash{position:absolute;right:-60px;bottom:-40px;width:720px;opacity:.5;
  transform:rotate(-4deg)}
.barras{display:flex;align-items:flex-end;gap:20px;height:330px}
.barras u{flex:1;border-radius:10px 10px 0 0;
  background:linear-gradient(180deg,rgba(79,124,255,.95),rgba(79,124,255,.18))}
.barras u:nth-child(4),.barras u:nth-child(6){
  background:linear-gradient(180deg,rgba(124,255,203,.95),rgba(124,255,203,.16))}
/* agenda */
.cal{position:absolute;right:-70px;top:120px;width:700px;opacity:.42;
  display:grid;grid-template-columns:repeat(5,1fr);gap:16px;transform:rotate(-5deg)}
.cal b{height:96px;border-radius:16px;background:#16233A;display:block}
.cal b.on{background:linear-gradient(160deg,rgba(79,124,255,.85),rgba(79,124,255,.35))}
.cal b.ok{background:linear-gradient(160deg,rgba(124,255,203,.8),rgba(124,255,203,.3))}
/* velo para que el texto siempre se lea */
.velo{position:absolute;inset:0;
  background:linear-gradient(105deg,#0A0E17 34%,rgba(10,14,23,.88) 52%,rgba(10,14,23,.55) 100%)}

"""

HEAD = "<!doctype html><meta charset='utf-8'><style>%s</style>" % CSS
# Nueve fondos con la misma paleta. Rotan por dia para que la grilla del
# perfil no quede monotona, sin perder la identidad.
FONDOS = [
    # 1 · grilla + halo azul arriba-derecha  (el clasico)
    "<div class='grid'></div><div class='glow'></div><div class='glow2'></div>",
    # 2 · trama de puntos + verde menta dominante
    "<div class='dots'></div><div class='glow-m'></div>",
    # 3 · cupula de luz azul arriba + arcos
    "<div class='brillo'></div><div class='arco'></div><div class='arco2'></div>",
    # 4 · lineas diagonales + azul desde abajo
    "<div class='diag'></div><div class='glow-b2'></div>",
    # 5 · banda clara arriba + puntos
    "<div class='banda'></div><div class='dots'></div><div class='glow2'></div>",
    # 6 · oscuro y quieto, apenas un resplandor al pie
    "<div class='grid'></div><div class='tenue'></div>",
    # 7 · escena: conversacion de WhatsApp de fondo
    ("<div class='grid'></div><div class='esc'><div class='chat'>"
     "<div class='bub el'>Hola! Tenes turno para el jueves?</div>"
     "<div class='bub yo'>Si, 15:30 o 17:00</div>"
     "<div class='bub el'>El de las 17 me sirve</div>"
     "<div class='bub yo'>Listo, te llega la confirmacion</div>"
     "</div></div><div class='velo'></div><div class='glow2'></div>"),
    # 8 · escena: tablero con barras
    ("<div class='dots'></div><div class='esc'><div class='dash'>"
     "<div class='barras'><u style='height:38%'></u><u style='height:62%'></u><u style='height:45%'></u><u style='height:80%'></u><u style='height:55%'></u><u style='height:92%'></u><u style='height:70%'></u><u style='height:48%'></u></div>"
     "</div></div><div class='velo'></div><div class='glow-m'></div>"),
    # 9 · escena: agenda con turnos tomados
    ("<div class='diag'></div><div class='esc'><div class='cal'><b></b><b></b><b class='on'></b><b></b><b></b><b class='ok'></b><b></b><b class='on'></b><b></b><b></b><b></b><b class='on'></b><b></b><b class='ok'></b><b></b></div></div>"
     "<div class='velo'></div><div class='glow-b2'></div>"),
]
BG = FONDOS[0]


def fondo(i=0):
    return FONDOS[i % len(FONDOS)]


HEADER = ("<div class='brand'><div class='mark'><i></i><i></i><i></i></div>"
          "<div class='brand-txt'>AXIOMA<span>.</span>SOFTWARE</div></div>")


def foot(cta="axiomasoftware.com"):
    return (f"<div class='foot'><div class='handle'>@axiomasoftwareok</div>"
            f"<div class='cta'><i>&rarr;</i>{cta}</div></div>")


def page(body, bg=0):
    return (f"<html><head>{HEAD}</head><body>{fondo(bg)}"
            f"<div class='frame'>{body}</div></body></html>")


def axioma(texto, sub, cta="Guardalo para cuando dudes", bg=0):
    return page(f"{HEADER}<div style='margin-top:auto'></div>"
                f"<div class='qmark'><i></i><i></i><i></i></div><div class='quote'>{texto}</div>"
                f"<div class='sub'>{sub}</div>{foot(cta)}", bg)


def tip(eyebrow, titulo, items, cta="Seguime para mas", bg=0):
    lis = "".join(f"<div class='item'><div class='num'>{i+1}</div><p>{t}</p></div>"
                  for i, t in enumerate(items))
    return page(f"{HEADER}<div class='eyebrow'>{eyebrow}</div><h1>{titulo}</h1>"
                f"<div class='items'>{lis}</div>{foot(cta)}", bg)


def caso(eyebrow, titulo, sub, chips, cta="Escribime por DM"):
    cs = "".join(f"<div class='chip'><div class='big'>{b}</div><div class='lbl'>{l}</div></div>"
                 for b, l in chips)
    return page(f"{HEADER}<div class='eyebrow'>{eyebrow}</div><h1>{titulo}</h1>"
                f"<div class='sub'>{sub}</div><div class='stat'>{cs}</div>{foot(cta)}")


CSS_EXTRA = """
.win{margin-top:44px;background:#0E1626;border:1px solid var(--line);border-radius:24px;
  overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.5);flex:1;display:flex;flex-direction:column}
.bar{height:64px;background:#151F31;border-bottom:1px solid var(--line);
  display:flex;align-items:center;gap:11px;padding:0 24px}
.bar u{width:14px;height:14px;border-radius:50%;background:#2C3A50;text-decoration:none}
.bar span{margin-left:18px;font-family:'Mono';font-size:19px;color:#5D6B82}
.shot{flex:1;display:grid;place-items:center;text-align:center;padding:40px;
  background:repeating-linear-gradient(45deg,#101a2b,#101a2b 22px,#0d1524 22px,#0d1524 44px)}
.shot p{font-family:'Mono';font-size:26px;color:#6C7B93;line-height:1.6}
"""


def captura(eyebrow, titulo, etiqueta_ventana, texto_placeholder,
            cta="Escribime por DM", bg=0):
    head = HEAD.replace("</style>", CSS_EXTRA + "</style>")
    body = (f"{HEADER}<div class='eyebrow'>{eyebrow}</div><h1>{titulo}</h1>"
            f"<div class='win'><div class='bar'><u></u><u></u><u></u>"
            f"<span>{etiqueta_ventana}</span></div>"
            f"<div class='shot'><p>{texto_placeholder}</p></div></div>{foot(cta)}")
    return (f"<html><head>{head}</head><body>{fondo(bg)}"
            f"<div class='frame'>{body}</div></body></html>")
