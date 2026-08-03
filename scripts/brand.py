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
"""

HEAD = "<!doctype html><meta charset='utf-8'><style>%s</style>" % CSS
BG = "<div class='grid'></div><div class='glow'></div><div class='glow2'></div>"
HEADER = ("<div class='brand'><div class='mark'><i></i><i></i><i></i></div>"
          "<div class='brand-txt'>AXIOMA<span>.</span>SOFTWARE</div></div>")


def foot(cta="axiomasoftware.com"):
    return (f"<div class='foot'><div class='handle'>@axiomasoftwareok</div>"
            f"<div class='cta'><i>&rarr;</i>{cta}</div></div>")


def page(body):
    return f"<html><head>{HEAD}</head><body>{BG}<div class='frame'>{body}</div></body></html>"


def axioma(texto, sub, cta="Guardalo para cuando dudes"):
    return page(f"{HEADER}<div style='margin-top:auto'></div>"
                f"<div class='qmark'><i></i><i></i><i></i></div><div class='quote'>{texto}</div>"
                f"<div class='sub'>{sub}</div>{foot(cta)}")


def tip(eyebrow, titulo, items, cta="Seguime para mas"):
    lis = "".join(f"<div class='item'><div class='num'>{i+1}</div><p>{t}</p></div>"
                  for i, t in enumerate(items))
    return page(f"{HEADER}<div class='eyebrow'>{eyebrow}</div><h1>{titulo}</h1>"
                f"<div class='items'>{lis}</div>{foot(cta)}")


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


def captura(eyebrow, titulo, etiqueta_ventana, texto_placeholder, cta="Escribime por DM"):
    head = HEAD.replace("</style>", CSS_EXTRA + "</style>")
    body = (f"{HEADER}<div class='eyebrow'>{eyebrow}</div><h1>{titulo}</h1>"
            f"<div class='win'><div class='bar'><u></u><u></u><u></u>"
            f"<span>{etiqueta_ventana}</span></div>"
            f"<div class='shot'><p>{texto_placeholder}</p></div></div>{foot(cta)}")
    return (f"<html><head>{head}</head><body>{BG}"
            f"<div class='frame'>{body}</div></body></html>")
