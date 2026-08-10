# -*- coding: utf-8 -*-
"""Guiones de reel: cada uno muestra algo distinto funcionando.

Cada guion devuelve (html_del_cuerpo, duracion_en_segundos). El armado
general (fondo, barra de progreso, firma y cierre) lo pone reel.py.

La idea de todos es la misma: no contar lo que Axioma hace, mostrarlo
pasando. Pero cada uno con otra pantalla y otro tema, para que la grilla
no se vuelva repetitiva.
"""

# =====================================================================
#  CSS compartido
# =====================================================================

CSS = r"""
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1920px;background:#070A11;color:#EDF2FB;
  font-family:'Inter',sans-serif;overflow:hidden;position:relative}

@property --n{syntax:'<integer>';initial-value:0;inherits:false}

/* ---------- ambiente ---------- */
.amb{position:absolute;inset:-10%;animation:respira 14s ease-in-out infinite}
.amb.azul{background:radial-gradient(120% 60% at 50% 0%,rgba(79,124,255,.42) 0%,transparent 64%),
                    radial-gradient(90% 50% at 50% 100%,rgba(124,255,203,.20) 0%,transparent 62%)}
.amb.menta{background:radial-gradient(110% 55% at 22% 4%,rgba(124,255,203,.32) 0%,transparent 62%),
                     radial-gradient(100% 55% at 82% 96%,rgba(79,124,255,.34) 0%,transparent 64%)}
.amb.hondo{background:radial-gradient(130% 70% at 50% 108%,rgba(79,124,255,.44) 0%,transparent 66%)}
.malla{position:absolute;inset:-14%;opacity:.72;
  animation:deriva 26s linear infinite;
  background-image:linear-gradient(rgba(255,255,255,.055) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,.055) 1px,transparent 1px);
  background-size:96px 96px}
.malla.puntos{background-image:radial-gradient(rgba(255,255,255,.13) 2px,transparent 2px);
  background-size:52px 52px;opacity:.5}
@keyframes deriva{from{transform:translateY(0) scale(1)}
                  to{transform:translateY(96px) scale(1.04)}}
@keyframes respira{0%,100%{transform:scale(1);opacity:1}
                   50%{transform:scale(1.09);opacity:.82}}

/* ---------- rótulo ---------- */
.rotulo{position:absolute;top:150px;left:0;right:0;padding:0 80px;text-align:center;z-index:6}
.rotulo .t{font-family:'Grotesk';font-weight:700;font-size:76px;line-height:1.05;
  letter-spacing:-.03em;opacity:0;animation:rot var(--rd) both}
.rotulo .t em{font-style:normal;color:#7CFFCB}
@keyframes rot{
  0%{opacity:0;filter:blur(10px);
     transform:perspective(1400px) translateZ(-320px) translateY(70px) rotateX(-34deg)}
  7%{opacity:1;filter:blur(0);
     transform:perspective(1400px) translateZ(0) translateY(0) rotateX(0)}
  90%{opacity:1;filter:blur(0);
     transform:perspective(1400px) translateZ(40px) translateY(-10px) rotateX(0)}
  100%{opacity:0;filter:blur(7px);
     transform:perspective(1400px) translateZ(180px) translateY(-40px) rotateX(22deg)}
}

/* ---------- celular ---------- */
.tel{position:absolute;left:50%;top:500px;width:620px;height:1150px;
  transform:translateX(-50%);background:#0C1220;border:14px solid #1B2436;
  border-radius:64px;overflow:hidden;z-index:5;perspective:1100px;
  box-shadow:0 60px 130px rgba(0,0,0,.72),0 0 0 2px rgba(255,255,255,.05),
             0 30px 90px rgba(79,124,255,.22);
  animation:entra 1.1s cubic-bezier(.2,.9,.25,1) both,
            flotaC 11s ease-in-out 1.1s infinite}
.tel.chico{width:440px;height:820px;top:700px;left:auto;right:46px;transform:none;
  animation:entra-der 1s cubic-bezier(.2,.9,.25,1) both,
            flota 9.5s ease-in-out 1s infinite}
@keyframes entra{from{opacity:0;transform:translateX(-50%) translateY(90px) scale(.94)}
                 to{opacity:1;transform:translateX(-50%) translateY(0) scale(1)}}
@keyframes entra-der{from{opacity:0;transform:translateX(140px) scale(.94)}
                     to{opacity:1;transform:none}}
.muesca{position:absolute;top:0;left:50%;transform:translateX(-50%);
  width:190px;height:34px;background:#1B2436;border-radius:0 0 22px 22px;z-index:20}
.appbar{height:120px;background:#111A2B;border-bottom:1px solid rgba(255,255,255,.07);
  display:flex;align-items:flex-end;gap:18px;padding:0 26px 18px;
  position:relative;z-index:3}
.av{width:56px;height:56px;border-radius:50%;flex:none;
  background:linear-gradient(150deg,#4F7CFF,#2B3EE8);display:grid;place-items:center;
  font-family:'Grotesk';font-weight:700;font-size:26px;color:#fff}
.appbar .n{font-family:'Inter';font-weight:600;font-size:28px}
.appbar .e{font-size:20px;color:#7CFFCB;margin-top:4px}
.pant{position:absolute;inset:120px 0 0 0;padding:26px 24px;overflow:hidden}
.pant.chat{display:flex;flex-direction:column;gap:20px;padding-top:30px}
.pant.chat.rueda{animation:rueda 1.2s cubic-bezier(.3,.8,.3,1) both}
@keyframes rueda{to{transform:translateY(-255px)}}

/* burbujas */
.b{max-width:84%;padding:22px 26px;border-radius:26px;font-size:27px;line-height:1.34;
  opacity:0;animation:burb .45s cubic-bezier(.2,.9,.25,1) both}
@keyframes burb{from{opacity:0;
  transform:perspective(900px) translateY(30px) translateZ(-90px) rotateX(-18deg)}
  to{opacity:1;transform:perspective(900px) translateY(0) translateZ(0) rotateX(0)}}
.b.el{align-self:flex-start;background:#1B2740;color:#C7D3E8;border-bottom-left-radius:9px}
.b.yo{align-self:flex-end;background:#15473B;color:#A9F2D6;border-bottom-right-radius:9px}
.b .h{display:block;font-size:18px;color:#6D7C94;margin-top:10px;text-align:right}
.b.yo .h{color:#5E9A85}
.esc{align-self:flex-end;display:flex;gap:10px;background:#15473B;border-radius:26px;
  padding:26px 28px;opacity:0;animation:apaga var(--ed) both}
.esc s{width:13px;height:13px;border-radius:50%;background:#7CFFCB;text-decoration:none;
  animation:bota 1s infinite}
.esc s:nth-child(2){animation-delay:.16s}
.esc s:nth-child(3){animation-delay:.32s}
@keyframes bota{0%,60%,100%{transform:translateY(0);opacity:.45}
                30%{transform:translateY(-11px);opacity:1}}
@keyframes apaga{0%{opacity:0}6%{opacity:1}88%{opacity:1}100%{opacity:0}}

/* ---------- ventana de navegador ---------- */
.win{position:absolute;left:50%;transform:translateX(-50%);z-index:5;
  background:#0C1220;border:1px solid rgba(255,255,255,.09);border-radius:30px;
  overflow:hidden;box-shadow:0 60px 130px rgba(0,0,0,.7),0 26px 80px rgba(79,124,255,.2);
  animation:entra 1.1s cubic-bezier(.2,.9,.25,1) both,
            flotaC 12.5s ease-in-out 1.1s infinite}
.wbar{height:86px;background:#141E30;border-bottom:1px solid rgba(255,255,255,.07);
  display:flex;align-items:center;gap:12px;padding:0 26px}
.wbar u{width:15px;height:15px;border-radius:50%;background:#2C3A50;text-decoration:none}
.wbar .url{margin-left:20px;flex:1;background:#0D1626;border-radius:999px;
  padding:13px 24px;font-family:'Mono';font-size:22px;color:#7E8DA6}
.wcuerpo{padding:36px 38px}

/* ---------- fichas / tarjetas ---------- */
.ficha{background:#131E33;border:1px solid rgba(255,255,255,.08);border-radius:24px;
  padding:28px 30px;opacity:0;animation:burb .45s both}
.ficha.verde{background:#17402F;border-color:rgba(124,255,203,.4)}

/* aviso flotante */
.aviso{position:absolute;left:50%;transform:translateX(-50%);
  display:flex;align-items:center;gap:20px;background:#101A2C;
  border:1px solid rgba(124,255,203,.34);border-radius:26px;padding:26px 34px;
  box-shadow:0 26px 70px rgba(0,0,0,.6);white-space:nowrap;z-index:9;
  opacity:0;animation:avi var(--vd) both}
@keyframes avi{
  0%{opacity:0;transform:translateX(-50%) perspective(1000px) translateZ(-260px) rotateX(38deg)}
  9%{opacity:1;transform:translateX(-50%) perspective(1000px) translateZ(70px) rotateX(0)}
  16%{transform:translateX(-50%) perspective(1000px) translateZ(40px) rotateX(0)}
  88%{opacity:1;transform:translateX(-50%) perspective(1000px) translateZ(40px) rotateX(0)}
  100%{opacity:0;transform:translateX(-50%) perspective(1000px) translateZ(150px) rotateX(-16deg)}}
.aviso .pt{width:16px;height:16px;border-radius:50%;flex:none;background:#7CFFCB;
  box-shadow:0 0 20px #7CFFCB}
.aviso .tx{font-size:29px;color:#C7D3E8}
.aviso .tx b{color:#EDF2FB;font-weight:600}

/* puntero del mouse */
.mouse{position:absolute;width:34px;height:34px;z-index:12;opacity:0;
  animation:var(--ma)}
.mouse::before{content:'';position:absolute;inset:0;
  background:#fff;clip-path:polygon(0 0,0 74%,26% 56%,44% 96%,60% 88%,42% 50%,74% 46%);
  filter:drop-shadow(0 4px 10px rgba(0,0,0,.6))}

/* efecto de tecleo */
.tecla{display:inline-block;overflow:hidden;white-space:nowrap;vertical-align:bottom;
  width:0;animation:teclea var(--td) steps(var(--tn)) both}
@keyframes teclea{to{width:var(--tw)}}

/* números que suben */
.contador{font-family:'Grotesk';font-weight:700;letter-spacing:-.03em;
  counter-reset:v var(--n)}
.contador::after{content:counter(v)}

/* ================= encuadre A: la pantalla ocupa todo ================= */
.llena{position:absolute;inset:0;background:#0A121F;display:flex;flex-direction:column;
  z-index:4}
.llena .estado{height:96px;display:flex;align-items:center;justify-content:space-between;
  padding:0 54px;font-family:'Mono';font-size:30px;color:#8B99B0;
  background:#0A121F}
.llena .cab{display:flex;align-items:center;gap:26px;padding:22px 54px 30px;
  background:#111C2E;border-bottom:1px solid rgba(255,255,255,.07)}
.llena .cab .av{width:86px;height:86px;font-size:38px}
.llena .cab .n{font-size:44px;font-weight:600}
.llena .cab .e{font-size:28px;color:#7CFFCB;margin-top:6px}
.llena .cuerpo{flex:1;display:flex;flex-direction:column;gap:28px;
  padding:44px 54px 40px;overflow:hidden}
.llena .cuerpo .b{max-width:82%;font-size:40px;padding:30px 36px;border-radius:34px}
.llena .cuerpo .b .h{font-size:24px;margin-top:12px}
.llena .barra-esc{height:130px;background:#111C2E;display:flex;align-items:center;
  gap:24px;padding:0 54px;border-top:1px solid rgba(255,255,255,.07)}
.llena .barra-esc .caja{flex:1;height:74px;border-radius:999px;background:#0D1626;
  display:flex;align-items:center;padding:0 30px;font-size:30px;color:#5D6B82}
.llena .barra-esc .env{width:74px;height:74px;border-radius:50%;background:#7CFFCB}

/* rótulo abajo, tipo placa de noticiero */
.rotulo.abajo{top:auto;bottom:340px;padding:0 54px;text-align:left}
.rotulo.abajo .t{display:inline-block;font-size:62px;background:rgba(7,10,17,.86);
  border-left:10px solid #7CFFCB;padding:26px 34px;border-radius:0 20px 20px 0;
  animation:rotPlaca var(--rd) both}
@keyframes rotPlaca{0%{opacity:0;transform:translateX(-90px)}
                    6%{opacity:1;transform:none}
                    92%{opacity:1;transform:none}
                    100%{opacity:0;transform:translateX(-60px)}}

/* ================= encuadre B: tarjetas que se dan vuelta ============ */
.mesa{position:absolute;left:0;right:0;top:680px;display:flex;justify-content:center;
  gap:34px;z-index:5;perspective:2000px}
.carta{width:322px;height:620px;position:relative;
  animation:cartaEntra .75s cubic-bezier(.2,.9,.25,1) both}
@keyframes cartaEntra{from{opacity:0;transform:translateY(90px) rotateY(-26deg)}
                      to{opacity:1;transform:rotateY(-7deg)}}
.cara{position:absolute;inset:0;border-radius:34px;
  padding:40px 34px;display:flex;flex-direction:column;
  border:1px solid rgba(255,255,255,.09);background:#131E33;
  box-shadow:0 40px 90px rgba(0,0,0,.6)}
.cara.frente{animation:caraSale .5s cubic-bezier(.5,0,.9,.4) both}
@keyframes caraSale{from{transform:rotateY(0);opacity:1}
                    to{transform:rotateY(88deg);opacity:0}}
.cara.atras{background:#17402F;border-color:rgba(124,255,203,.45);
  align-items:center;justify-content:center;text-align:center;
  animation:caraEntra .55s cubic-bezier(.2,.9,.25,1) both}
@keyframes caraEntra{from{transform:rotateY(-90deg);opacity:0}
                     to{transform:rotateY(0);opacity:1}}
.cara .av{width:78px;height:78px;font-size:34px;margin-bottom:28px}
.cara .nm{font-family:'Grotesk';font-weight:700;font-size:42px}
.cara .hr{font-family:'Mono';font-size:28px;color:#7E8DA6;margin-top:12px}
.cara .et{margin-top:auto;font-size:26px;color:#6D7C94}
.cara.atras .tick{width:96px;height:96px;border-radius:50%;background:#7CFFCB;
  display:grid;place-items:center;margin-bottom:26px}
.cara.atras .tick s{width:38px;height:20px;border-left:7px solid #0B2A1E;
  border-bottom:7px solid #0B2A1E;transform:rotate(-45deg) translateY(-5px);
  text-decoration:none;display:block}
.cara.atras .tx{font-family:'Grotesk';font-weight:700;font-size:38px;color:#A9F2D6}
.cara.atras .sb{font-size:26px;color:#6FCBA9;margin-top:12px}

/* rótulo grande arriba a la izquierda */
.rotulo.izq{text-align:left;padding:0 64px;top:210px}
.rotulo.izq .t{font-size:88px}

/* ================= encuadre C: tablero a sangre ====================== */
.sangre{position:absolute;inset:0;padding:190px 64px 250px;z-index:4;
  display:flex;flex-direction:column;justify-content:center}
.sangre .tit{font-family:'Mono';font-size:30px;color:#6D7C94;letter-spacing:.2em;
  text-transform:uppercase;margin-bottom:34px}
.gran{display:flex;flex-direction:column;margin-bottom:38px}
.gran .et{font-size:34px;color:#7E8DA6}
.gran .vl{font-family:'Grotesk';font-weight:700;font-size:210px;line-height:.95;
  letter-spacing:-.05em;margin-top:6px}
.par{display:flex;gap:26px;margin-bottom:44px}
.par>div{flex:1}
.par .et{font-size:28px;color:#7E8DA6}
.par .vl{font-family:'Grotesk';font-weight:700;font-size:104px;line-height:1;
  letter-spacing:-.04em;margin-top:8px}

/* rótulo chico abajo a la izquierda */
.rotulo.pie{top:auto;bottom:210px;text-align:left;padding:0 64px}
.rotulo.pie .t{font-size:52px;animation:rotPlaca var(--rd) both}

/* ============ encuadre D: la ficha del producto ocupa todo =========== */
.tienda{position:absolute;inset:0;background:#0A121F;display:flex;flex-direction:column;z-index:4}
.tienda .top{display:flex;align-items:center;justify-content:space-between;
  padding:64px 54px 0;font-family:'Mono';font-size:30px;color:#6D7C94}
.tienda .foto{margin:36px 54px 0;height:520px;border-radius:34px;
  background:linear-gradient(140deg,#1E2C48,#141F35);border:1px solid rgba(255,255,255,.07);
  display:grid;place-items:center;position:relative;overflow:hidden}
.tienda .foto b{width:180px;height:180px;border-radius:44px;
  background:linear-gradient(150deg,rgba(79,124,255,.55),rgba(124,255,203,.34))}
.tienda .nom{padding:44px 54px 0;font-family:'Grotesk';font-weight:700;font-size:66px;
  letter-spacing:-.03em}
.tienda .pre{padding:16px 54px 0;font-family:'Grotesk';font-weight:700;font-size:96px;
  color:#7CFFCB;letter-spacing:-.04em}
.tienda .stk{padding:20px 54px 0;font-size:36px;color:#8B99B0;white-space:nowrap}
.tienda .comprar{margin:auto 54px 90px;padding:44px;border-radius:28px;text-align:center;
  font-family:'Grotesk';font-weight:700;font-size:50px;color:#070A11;background:#7CFFCB}
.sello{position:absolute;left:50%;top:1010px;transform:translate(-50%,0) rotate(-11deg);
  font-family:'Grotesk';font-weight:700;font-size:92px;letter-spacing:.04em;
  color:#7CFFCB;border:9px solid #7CFFCB;border-radius:26px;padding:22px 44px;
  background:rgba(7,10,17,.72);z-index:8;opacity:0;
  animation:sella .55s cubic-bezier(.2,1.4,.4,1) both}
@keyframes sella{0%{opacity:0;transform:translate(-50%,0) rotate(-11deg) scale(2.4)}
                 70%{opacity:1;transform:translate(-50%,0) rotate(-11deg) scale(.94)}
                 100%{opacity:1;transform:translate(-50%,0) rotate(-11deg) scale(1)}}

/* ============ encuadre E: pantalla partida arriba / abajo ============ */
.partida{position:absolute;inset:0;display:flex;flex-direction:column;z-index:4}
.partida .mitad{flex:1;position:relative;overflow:hidden;padding:150px 60px 40px}
.partida .mitad.abajo{padding:60px 60px 240px;background:#0A0F1A}
.partida .raya{height:2px;background:rgba(255,255,255,.09);position:relative}
.pulso{position:absolute;left:50%;top:0;width:22px;height:22px;border-radius:50%;
  background:#7CFFCB;transform:translate(-50%,-50%);box-shadow:0 0 40px #7CFFCB;
  opacity:0;animation:baja 1.5s cubic-bezier(.4,0,.3,1) both;z-index:12}
@keyframes baja{0%{opacity:0;top:-460px}
                12%{opacity:1}
                100%{opacity:0;top:420px}}
.partida .rot{font-family:'Grotesk';font-weight:700;font-size:52px;letter-spacing:-.02em;
  margin-bottom:34px}
.partida .rot em{font-style:normal;color:#7CFFCB}

/* ============ encuadre F: el número manda ============================ */
.plata{position:absolute;inset:0;display:flex;flex-direction:column;
  justify-content:center;padding:0 64px 260px;z-index:4}
.plata .et{font-family:'Mono';font-size:32px;letter-spacing:.2em;color:#7E8DA6;
  text-transform:uppercase}
.plata .mn{font-family:'Grotesk';font-weight:700;font-size:236px;line-height:.92;
  letter-spacing:-.05em;margin-top:18px}
.plata .est{display:inline-flex;align-items:center;gap:20px;align-self:flex-start;
  margin-top:44px;padding:24px 40px;border-radius:999px;font-size:40px;font-weight:600}
.plata .est.pend{background:rgba(255,184,107,.14);color:#FFB86B;
  border:1px solid rgba(255,184,107,.4);animation:apaga4 .5s both}
.plata .est.list{background:#17402F;color:#A9F2D6;border:1px solid rgba(124,255,203,.5);
  animation:burb .6s both}
@keyframes apaga4{to{opacity:0;transform:translateY(-24px)}}
.tira{position:absolute;left:0;right:0;bottom:150px;display:flex;flex-direction:column;
  gap:16px;padding:0 64px;z-index:5}
.tira .b{font-size:30px;padding:20px 26px;border-radius:22px;max-width:78%}

/* ============ encuadre G: la lista que corre sola =================== */
.rollo{position:absolute;left:60px;right:60px;top:0;z-index:4;
  animation:corre var(--rd,20s) linear both}
@keyframes corre{from{transform:translateY(1180px)}to{transform:translateY(-1560px)}}
.rollo .it{display:flex;align-items:center;gap:24px;background:#131E33;
  border:1px solid rgba(255,255,255,.08);border-radius:26px;padding:34px 34px;
  margin-bottom:22px;font-size:38px;color:#C7D3E8}
.rollo .it .hr{font-family:'Mono';font-size:24px;color:#6D7C94;margin-top:10px}
.rollo .it .ok{margin-left:auto;font-size:28px;color:#7CFFCB;opacity:0;
  animation:burb .45s both}
.linea{position:absolute;left:0;right:0;top:900px;height:150px;z-index:6;
  border-top:2px solid rgba(124,255,203,.5);border-bottom:2px solid rgba(124,255,203,.5);
  background:linear-gradient(90deg,rgba(124,255,203,.10),rgba(124,255,203,.03))}
.linea span{position:absolute;left:60px;top:-46px;font-family:'Mono';font-size:26px;
  letter-spacing:.2em;color:#7CFFCB;text-transform:uppercase}
.tapa{position:absolute;left:0;right:0;height:420px;z-index:7;pointer-events:none}
.tapa.arr{top:0;background:linear-gradient(180deg,#070A11 26%,transparent)}
.tapa.aba{bottom:0;background:linear-gradient(0deg,#070A11 30%,transparent)}

@keyframes entraArriba{from{opacity:0;transform:translateY(34px) scale(.96)}to{opacity:1;transform:none}}
@keyframes pulso{0%{transform:scale(1)}45%{transform:scale(.94)}100%{transform:scale(1)}}
@keyframes brilla{0%{box-shadow:0 0 0 rgba(124,255,203,0)}
                  45%{box-shadow:0 0 60px rgba(124,255,203,.42)}
                  100%{box-shadow:0 0 22px rgba(124,255,203,.16)}}
@keyframes sale{0%{opacity:0;transform:translateY(0) scale(.9)}
                18%{opacity:1;transform:translateY(-24px) scale(1)}
                80%{opacity:1;transform:translateY(-40px)}
                100%{opacity:0;transform:translateY(-90px) scale(.96)}}
@keyframes cruza{0%{opacity:0;transform:rotateY(72deg) translateZ(-120px)}
                 6%{opacity:1;transform:none}
                 92%{opacity:1;transform:none}
                 100%{opacity:0;transform:rotateY(-72deg) translateZ(-120px)}}

/* ---------- profundidad: nada queda plano ni quieto ---------- */
@keyframes flotaC{
  0%,100%{transform:translateX(-50%) perspective(1900px) rotateY(-7deg) rotateX(3deg) translateY(0)}
  50%    {transform:translateX(-50%) perspective(1900px) rotateY(6deg) rotateX(-2.5deg) translateY(-22px)}}
@keyframes flota{
  0%,100%{transform:perspective(1600px) rotateY(-9deg) rotateX(2.5deg) translateY(0)}
  50%    {transform:perspective(1600px) rotateY(5deg) rotateX(-2deg) translateY(-18px)}}

/* barrido de luz sobre el vidrio */
.lustre{position:absolute;inset:-40%;z-index:14;pointer-events:none;
  background:linear-gradient(104deg,transparent 38%,rgba(255,255,255,.13) 47%,
             rgba(124,255,203,.16) 50%,transparent 60%);
  transform:translateX(-120%);
  animation:barre var(--bd,7s) ease-in-out var(--bi,2s) infinite}
@keyframes barre{0%{transform:translateX(-120%)}
                 26%{transform:translateX(120%)}
                 100%{transform:translateX(120%)}}
"""


# ---------------------------------------------------------------------
#  ayudantes
# ---------------------------------------------------------------------

def rot(txt, ini, dur, donde=""):
    return (f"<div class='rotulo {donde}'><div class='t' "
            f"style='--rd:{dur}s;animation-delay:{ini}s'>{txt}</div></div>")


def burbuja(quien, texto, hora, ini):
    return (f"<div class='b {quien}' style='animation-delay:{ini}s'>{texto}"
            f"<span class='h'>{hora}</span></div>")


def escribiendo(ini, dur):
    return (f"<div class='esc' style='--ed:{dur}s;animation-delay:{ini}s'>"
            f"<s></s><s></s><s></s></div>")


def aviso(texto, ini, dur, top=1300):
    return (f"<div class='aviso' style='top:{top}px;--vd:{dur}s;"
            f"animation-delay:{ini}s'>"
            f"<span class='pt'></span><span class='tx'>{texto}</span></div>")


def telefono(titulo, subtitulo, pantallas, clase=""):
    return (f"<div class='tel {clase}'><div class='muesca'></div>"
            f"<div class='lustre' style='--bd:8s;--bi:2.4s'></div>"
            f"<div class='appbar'><div class='av'>A</div>"
            f"<div><div class='n'>{titulo}</div><div class='e'>{subtitulo}</div></div></div>"
            f"{pantallas}</div>")


def ventana(url, cuerpo, top, alto, ancho=760):
    return (f"<div class='win' style='top:{top}px;width:{ancho}px;height:{alto}px'>"
            f"<div class='lustre' style='--bd:9s;--bi:3.1s'></div>"
            f"<div class='wbar'><u></u><u></u><u></u>"
            f"<div class='url'>{url}</div></div>"
            f"<div class='wcuerpo'>{cuerpo}</div></div>")


def tecleo(texto, ini, dur):
    """El texto aparece letra por letra, como si alguien lo escribiera."""
    n = max(len(texto), 1)
    return (f"<span class='tecla' style=\"--td:{dur}s;--tn:{n};--tw:{n}ch;"
            f"animation-delay:{ini}s\">{texto}</span>")


def puntero(nombre, pasos, ini):
    """pasos = [(x, y, t_relativo), ...] recorrido del mouse en pantalla."""
    total = pasos[-1][2]
    cuadros = []
    for x, y, t in pasos:
        pct = round(t / total * 100, 2)
        cuadros.append(f"{pct}%{{opacity:1;left:{x}px;top:{y}px}}")
    css = f"@keyframes {nombre}{{{''.join(cuadros)}}}"
    div = (f"<div class='mouse' style=\"left:{pasos[0][0]}px;top:{pasos[0][1]}px;"
           f"--ma:{nombre} {total}s both;animation-delay:{ini}s\"></div>")
    return css, div


# =====================================================================
#  guiones
# =====================================================================

def g_turnos():
    """Encuadre A: estás mirando la pantalla del cliente. Cámara quieta."""
    chat = "".join([
        burbuja("el", "Hola! Tenés turno para el jueves?", "23:04", 0.9),
        burbuja("el", "Perdón la hora", "23:04", 1.7),
        escribiendo(2.3, 1.0),
        burbuja("yo", "Hola! Tengo 15:30 y 17:00 libres", "23:04", 3.5),
        burbuja("el", "El de las 17 me sirve", "23:05", 5.0),
        burbuja("yo", "Listo, te lo reservo", "23:05", 6.0),
        burbuja("yo", "Confirmado: jueves 17:00", "23:05", 13.9),
        burbuja("yo", "Te aviso un día antes", "23:05", 15.0),
    ])
    pantalla = (
        "<div class='llena'>"
        "<div class='estado'><span>23:05</span><span>· · ·</span></div>"
        "<div class='cab'><div class='av'>A</div>"
        "<div><div class='n'>Axioma</div><div class='e'>en línea</div></div></div>"
        f"<div class='cuerpo'>{chat}</div>"
        "<div class='barra-esc'><div class='caja'>Escribí un mensaje</div>"
        "<div class='env'></div></div></div>")

    p = [pantalla,
         rot("Son las <em>23:04</em>", 0.4, 4.2, "abajo"),
         rot("Nadie está atendiendo", 4.9, 3.8, "abajo"),
         rot("El sistema <em>sí</em>", 9.1, 4.2, "abajo")]
    return {"cuerpo": "".join(p), "dur": 17.6, "amb": "azul", "trama": "malla",
            "camara": "fija", "cierre_estilo": "claro", "cierre_dur": 4.2,
            "sin_firma": True, "lema": "Software <em>a tu medida</em>"}


def g_tienda():
    """Encuadre D: la ficha del producto ocupa toda la pantalla. Sello que cae."""
    css, mouse = puntero("mTienda", [(820, 900, 0), (700, 1200, .7),
                                     (540, 1560, 1.6), (540, 1560, 2.6)], 2.4)
    tienda = (
        f"<style>{css}</style>"
        "<div class='tienda'>"
        "<div class='top'><span>tutienda.com.ar</span><span>03:12</span></div>"
        "<div class='foto'><b></b></div>"
        "<div class='nom'>Kit de instalación</div>"
        "<div class='pre'>$ 48.500</div>"
        "<div class='stk'>Stock: "
        "<span style='position:relative;display:inline-block;width:36px;height:42px;vertical-align:-8px'>"
        "<b style='position:absolute;left:0;color:#EDF2FB;"
        "animation:sale .9s forwards;animation-delay:9.4s'>4</b>"
        "<b style='position:absolute;left:0;opacity:0;color:#7CFFCB;"
        "animation:entraArriba .55s both;animation-delay:10.0s'>3</b></span></div>"
        "<div class='comprar' style='animation:pulso .5s both;animation-delay:5.0s'>"
        "Comprar</div></div>"
        "<div class='sello' style='animation-delay:9.6s'>VENDIDO</div>")

    p = [tienda, mouse,
         rot("Son las <em>3 de la mañana</em>", 0.5, 5.0, "abajo"),
         rot("Alguien compra", 5.8, 3.4, "abajo"),
         rot("El stock <em>baja solo</em>", 9.6, 5.2, "abajo"),
         aviso("Venta nueva · <b>$ 48.500</b>", 12.0, 3.4, top=380)]
    return {"cuerpo": "".join(p), "dur": 16.4, "amb": "menta", "trama": "malla puntos",
            "camara": "empuje", "cierre_estilo": "panel", "sin_firma": True,
            "lema": "Vendé <em>mientras dormís</em>"}


def g_formulario():
    """Encuadre E: arriba la web, abajo tu celular. Un pulso baja de una a otra."""
    campos = [("Nombre", "Marina Ruiz", 1.4, 1.0),
              ("Teléfono", "351 468 2290", 2.7, 1.0),
              ("Qué necesitás", "Una web con turnos online", 4.0, 1.5)]
    filas = "".join(
        f"<div style='margin-bottom:20px'>"
        f"<div style='font-size:24px;color:#7E8DA6;margin-bottom:8px'>{e}</div>"
        f"<div style='background:#0D1626;border:1px solid rgba(255,255,255,.09);"
        f"border-radius:14px;padding:18px 22px;font-size:30px;min-height:70px'>"
        f"{tecleo(v, i, d)}</div></div>" for e, v, i, d in campos)

    arriba = ("<div class='mitad'>"
              "<div class='rot'>En <em>tu web</em></div>" + filas +
              "<div style='margin-top:8px;padding:24px;border-radius:16px;text-align:center;"
              "font-family:\"Grotesk\";font-weight:700;font-size:34px;color:#070A11;"
              "background:#7CFFCB;animation:pulso .5s both;animation-delay:6.2s'>Enviar</div>"
              "</div>")

    abajo = ("<div class='mitad abajo'>"
             "<div class='rot'>En <em>tu celular</em></div>"
             "<div class='ficha' style='animation-delay:8.0s'>"
             "<div style='font-size:28px;color:#7CFFCB;font-weight:600'>Consulta nueva</div>"
             "<div style='font-size:34px;margin-top:16px;line-height:1.5'>"
             "Marina Ruiz<br>351 468 2290<br>«Una web con turnos online»</div></div>"
             "<div class='ficha' style='margin-top:18px;font-size:28px;color:#8B99B0;"
             "animation-delay:9.2s'>Origen: formulario de la web · 09:41</div></div>")

    p = ["<div class='partida'>" + arriba +
         "<div class='raya'><div class='pulso' style='animation-delay:6.5s'></div></div>"
         + abajo + "</div>",
         aviso("Llegó en <b>2 segundos</b>", 10.4, 3.6, top=1660)]
    return {"cuerpo": "".join(p), "dur": 15.4, "amb": "azul", "trama": "malla",
            "camara": "fija", "cierre_estilo": "franja", "sin_firma": True,
            "lema": "Sin copiar <em>ni pegar nada</em>"}


def g_cobro():
    """Encuadre F: la plata en pantalla completa. Pendiente → pagado."""
    plata = (
        "<div class='plata'>"
        "<div class='et'>Seña para reservar</div>"
        "<div class='mn'>$ 12.000</div>"
        "<div class='est pend' style='animation-delay:7.4s'>"
        "<span style='width:16px;height:16px;border-radius:50%;background:#FFB86B'></span>"
        "Pendiente de pago</div>"
        "<div class='est list' style='position:absolute;margin-top:0;top:1130px;"
        "animation-delay:7.9s'>"
        "<span style='width:16px;height:16px;border-radius:50%;background:#7CFFCB'></span>"
        "Pagado · turno confirmado</div>"
        "</div>")

    tira = ("<div class='tira'>"
            + burbuja("yo", "Te dejo el link para dejarlo reservado", "18:22", 1.6)
            + burbuja("el", "Listo, ya pagué", "18:24", 6.4)
            + burbuja("yo", "Confirmado: martes 10:30", "18:24", 10.6)
            + "</div>")

    p = [plata, tira,
         rot("El link va <em>en el mismo mensaje</em>", 0.5, 5.4, "izq"),
         rot("Se reserva <em>cuando se paga</em>", 6.4, 5.4, "izq"),
         rot("Las cancelaciones <em>bajan solas</em>", 12.2, 5.0, "izq")]
    return {"cuerpo": "".join(p), "dur": 17.0, "amb": "hondo", "trama": "malla",
            "camara": "vaiven", "cierre_estilo": "claro", "sin_firma": True,
            "lema": "Cobrá <em>antes, no después</em>"}


def g_recordatorio():
    """Encuadre B: tres cartas paradas que se dan vuelta. Cámara que pasea."""
    gente = [("Marina", "10:30"), ("Diego", "14:00"), ("Sofía", "17:30")]
    cartas = []
    for i, (nom, hora) in enumerate(gente):
        entra = round(1.0 + i * 0.28, 2)
        gira = round(7.6 + i * 0.75, 2)
        cartas.append(
            f"<div class='carta' style='animation-delay:{entra}s'>"
            f"<div class='cara frente' style='animation-delay:{gira}s'>"
            f"<div class='av'>{nom[0]}</div>"
            f"<div class='nm'>{nom}</div><div class='hr'>mañana {hora}</div>"
            f"<div class='et'>sin confirmar</div></div>"
            f"<div class='cara atras' style='animation-delay:{round(gira + .42, 2)}s'>"
            f"<div class='tick'><s></s></div>"
            f"<div class='tx'>Recordatorio<br>enviado</div>"
            f"<div class='sb'>18:00 · automático</div></div></div>")

    p = [f"<div class='mesa'>{''.join(cartas)}</div>",
         rot("El que no avisa<br><em>se olvidó</em>", 0.5, 6.2, "izq"),
         rot("Un mensaje<br><em>el día antes</em>", 7.0, 5.4, "izq"),
         rot("Sin perseguir<br><em>a nadie</em>", 12.8, 5.0, "izq"),
         aviso("<b>3</b> recordatorios · 0 llamadas tuyas", 10.4, 3.6, top=1330)]
    return {"cuerpo": "".join(p), "dur": 17.8, "amb": "menta", "trama": "malla puntos",
            "camara": "vaiven", "cierre_estilo": "centro",
            "lema": "Software <em>a tu medida</em>"}


def g_tablero():
    """Encuadre C: los números ocupan la pantalla. La cámara arranca encima
    de uno y va retrocediendo hasta mostrar los tres."""
    keyframes = "".join(f"@keyframes sube{v}{{to{{--n:{v}}}}}" for v in (127, 9, 62))
    keyframes += "@keyframes crece{to{transform:scaleY(1)}}"

    cuerpo = (
        f"<style>{keyframes}</style>"
        "<div class='sangre'>"
        "<div class='tit'>Tu mes · en tres números</div>"

        "<div class='gran'><div class='et'>Turnos que entraron</div>"
        "<div class='vl contador' style='--n:0;"
        "animation:sube127 2.1s cubic-bezier(.2,.8,.3,1) both;animation-delay:.5s'></div></div>"

        "<div class='par'>"
        "<div><div class='et'>Se cayeron</div>"
        "<div class='vl contador' style='--n:0;color:#FFB86B;"
        "animation:sube9 1.6s cubic-bezier(.2,.8,.3,1) both;animation-delay:6.2s'></div></div>"
        "<div><div class='et'>Vinieron de la web</div>"
        "<div class='vl contador' style='--n:0;color:#7CFFCB;"
        "animation:sube62 1.8s cubic-bezier(.2,.8,.3,1) both;animation-delay:9.6s'></div></div>"
        "</div>"

        "<div style='display:flex;align-items:flex-end;gap:20px;height:300px;margin-top:20px'>"
        + "".join(
            f"<u style='flex:1;display:block;border-radius:14px 14px 0 0;height:{h}%;"
            f"transform-origin:bottom;transform:scaleY(0);"
            f"background:linear-gradient(180deg,rgba(79,124,255,.95),rgba(79,124,255,.18));"
            f"animation:crece .7s cubic-bezier(.2,.9,.25,1) both;"
            f"animation-delay:{round(11.8 + i * 0.1, 2)}s'></u>"
            for i, h in enumerate([38, 55, 47, 72, 61, 88, 76]))
        + "</div></div>")

    p = [cuerpo,
         rot("Cuánto <em>entró</em>", 1.0, 4.6, "pie"),
         rot("Cuánto <em>se cayó</em>", 6.2, 3.2, "pie"),
         rot("Y <em>de dónde llegó</em> cada uno", 9.6, 5.0, "pie")]
    return {"cuerpo": "".join(p), "dur": 15.6, "amb": "hondo", "trama": "malla",
            "camara": "retiro", "cierre_estilo": "panel", "sin_firma": True,
            "lema": "Medí <em>lo que importa</em>"}


def g_repetido():
    """Encuadre G: una lista que corre sola. Lo que cruza la franja, se contesta."""
    preguntas = [("Hacen envíos?", "09:02"), ("Qué horario tienen?", "09:07"),
                 ("Cuánto sale?", "09:11"), ("Aceptan tarjeta?", "09:15"),
                 ("Dónde están?", "09:20"), ("Hacen factura A?", "09:26"),
                 ("Tienen stock del azul?", "09:31"), ("Se puede retirar?", "09:38")]
    # la lista viaja 2330 px en 17 s: cada ítem cruza la franja en su momento
    alto = 152
    items = []
    for i, (q, h) in enumerate(preguntas):
        # cuándo este ítem pasa por la franja del medio
        cruce = round(2.0 + i * 1.05, 2)
        items.append(
            f"<div class='it'><div><div>{q}</div><div class='hr'>{h}</div></div>"
            f"<span class='ok' style='animation-delay:{cruce}s'>respondida</span></div>")

    # la lista se repite una vez para que la pantalla nunca quede vacía
    p = [f"<div class='rollo' style='--rd:17s'>{''.join(items)}{''.join(items[:4])}</div>",
         "<div class='linea'><span>se contestan solas</span></div>",
         "<div class='tapa arr'></div><div class='tapa aba'></div>",
         rot("Las mismas preguntas <em>de siempre</em>", 0.5, 5.6, "pie"),
         rot("Se contestan <em>solas</em>", 6.6, 4.6, "pie"),
         rot("Vos aparecés <em>cuando hace falta</em>", 11.8, 4.8, "pie")]
    return {"cuerpo": "".join(p), "dur": 17.0, "amb": "hondo", "trama": "malla puntos",
            "camara": "fija", "cierre_estilo": "centro", "sin_firma": True,
            "lema": "Software <em>a tu medida</em>"}


# id → (funcion, lema por defecto)
GUIONES = [
    ("turnos", g_turnos),
    ("tienda", g_tienda),
    ("formulario", g_formulario),
    ("cobro", g_cobro),
    ("recordatorio", g_recordatorio),
    ("tablero", g_tablero),
    ("repetido", g_repetido),
]
