"""MailGuard ML - signature UI components (presentation only).

Provides:
    inject_extras()                      CSS for everything below + chart motion
    hero_banner(title, subtitle, note)   animated dark hero header
    render_dashboard(result, threshold, is_spam)
                                         animated KPI cards, banner and risk gauge

No model or threshold logic lives here; it only formats values it is given.
"""

from __future__ import annotations

from html import escape
from typing import Any

import streamlit as st


def _h(markup: str) -> str:
    """Collapse markup onto one line so Markdown never treats indentation as code."""
    return " ".join(line.strip() for line in markup.splitlines() if line.strip())


EXTRAS_CSS = """
<style>
@property --i { syntax: '<integer>'; initial-value: 0; inherits: false; }
@property --d { syntax: '<integer>'; initial-value: 0; inherits: false; }

:root { --mx-ease: cubic-bezier(.22, .8, .3, 1); }

@keyframes mxRise   { from { opacity: 0; transform: translateY(20px) scale(.97); } to { opacity: 1; transform: none; } }
@keyframes mxSlide  { from { opacity: 0; transform: translateX(-16px); } to { opacity: 1; transform: none; } }
@keyframes mxCount  { from { --i: 0; --d: 0; } }
@keyframes mxGrowW  { from { transform: scaleX(0); } to { transform: scaleX(1); } }
@keyframes mxGrow   { from { width: 0; } }
@keyframes mxPop    { 0% { transform: scale(.4) rotate(-12deg); opacity: 0; } 70% { transform: scale(1.15) rotate(4deg); } 100% { transform: none; opacity: 1; } }
@keyframes mxGlow   { 0%,100% { box-shadow: 0 4px 14px rgba(var(--glow), .12); } 50% { box-shadow: 0 0 0 5px rgba(var(--glow), .10), 0 10px 26px rgba(var(--glow), .28); } }
@keyframes mxShake  { 0%,100% { transform: none; } 20% { transform: translateX(-4px); } 40% { transform: translateX(4px); } 60% { transform: translateX(-3px); } 80% { transform: translateX(2px); } }
@keyframes mxGauge  { from { stroke-dashoffset: 100; } }
@keyframes mxSwing  { from { transform: rotate(-90deg); } }
@keyframes mxBlob   { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(30px,-18px) scale(1.15); } }
@keyframes mxGridMove { from { background-position: 0 0; } to { background-position: 44px 44px; } }
@keyframes mxSweep  { 0% { transform: translateX(-120%); } 60%,100% { transform: translateX(520%); } }
@keyframes mxFloat  { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-9px); } }
@keyframes mxRingOut{ 0% { transform: scale(.7); opacity: .65; } 100% { transform: scale(1.7); opacity: 0; } }
@keyframes mxCheck  { from { stroke-dashoffset: 90; } to { stroke-dashoffset: 0; } }
@keyframes mxDot    { 0%,100% { opacity: 1; } 50% { opacity: .3; } }
@keyframes mxBarX   { from { transform: scaleX(0); opacity: .25; } to { transform: scaleX(1); opacity: 1; } }
@keyframes mxDraw   { from { stroke-dasharray: 4000; stroke-dashoffset: 4000; } to { stroke-dasharray: 4000; stroke-dashoffset: 0; } }
@keyframes mxFadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes mxBubble { from { opacity: 0; transform: scale(.6) translateX(14px); } to { opacity: 1; transform: none; } }
@keyframes mxWave   { from { transform: rotate(-12deg); } to { transform: rotate(22deg); } }
@keyframes mxBlink  { 0%,90%,100% { transform: scaleY(1); } 94% { transform: scaleY(.1); } }
@keyframes mxDart   { from { transform: translateX(-3.2px); } to { transform: translateX(3.2px); } }
@keyframes mxTilt   { 0%,100% { transform: rotate(0deg); } 50% { transform: rotate(-6deg); } }
@keyframes mxHop    { 0%,100% { transform: translateY(0); } 45% { transform: translateY(-14px); } }
@keyframes mxSearch { 0%,100% { transform: rotate(-4deg); } 50% { transform: rotate(8deg); } }
@keyframes mxCheer  { from { transform: rotate(-35deg) scale(.6); opacity: 0; } to { transform: none; opacity: 1; } }
@keyframes mxSweat  { 0% { transform: translateY(-4px); opacity: 0; } 30% { opacity: 1; } 100% { transform: translateY(16px); opacity: 0; } }
@keyframes mxQ      { 0% { opacity: 0; transform: translateY(8px); } 40%,70% { opacity: 1; } 100% { opacity: 0; transform: translateY(-12px); } }
@keyframes mxSpark  { 0%,100% { transform: scale(.2); opacity: 0; } 50% { transform: scale(1.1); opacity: 1; } }
@keyframes mxFlame  { from { transform: scaleY(.7); } to { transform: scaleY(1.25); } }

/* ================= HERO ================= */
.mx-hero {
    position: relative; overflow: hidden; isolation: isolate;
    display: flex; align-items: center; justify-content: space-between; gap: 24px;
    padding: 34px 40px; margin-bottom: 10px;
    border-radius: 24px;
    background: linear-gradient(135deg, #14113f 0%, #2a2590 55%, #4f46e5 100%);
    box-shadow: 0 20px 50px rgba(52, 44, 160, .35);
    animation: mxRise .8s var(--mx-ease) both;
}
.mx-hero-grid {
    position: absolute; inset: 0; z-index: -1; opacity: .5;
    background-image:
        linear-gradient(rgba(255,255,255,.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.07) 1px, transparent 1px);
    background-size: 44px 44px;
    animation: mxGridMove 6s linear infinite;
    mask-image: radial-gradient(ellipse at 70% 40%, #000 20%, transparent 75%);
    -webkit-mask-image: radial-gradient(ellipse at 70% 40%, #000 20%, transparent 75%);
}
.mx-blob { position: absolute; border-radius: 50%; filter: blur(60px); z-index: -2; animation: mxBlob 9s ease-in-out infinite; }
.mx-blob.b1 { width: 320px; height: 320px; background: #38BDF8; opacity: .35; right: -60px; top: -120px; }
.mx-blob.b2 { width: 260px; height: 260px; background: #9333EA; opacity: .45; left: 30%; bottom: -140px; animation-delay: -4s; }
.mx-hero::after {
    content: ""; position: absolute; top: 0; bottom: 0; left: 0; width: 18%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.13), transparent);
    transform: skewX(-18deg); animation: mxSweep 6s ease-in-out infinite; pointer-events: none;
}
.mx-hero-body { max-width: 720px; position: relative; z-index: 1; }
.mx-pill {
    display: inline-flex; align-items: center; gap: 9px;
    padding: 6px 14px; border-radius: 99px;
    background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.22);
    color: #DDE0FF; font-size: 11px; font-weight: 800; letter-spacing: 1.6px;
    backdrop-filter: blur(6px);
}
.mx-pill .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--dot, #34D399); box-shadow: 0 0 10px var(--dot, #34D399); animation: mxDot 1.6s ease-in-out infinite; }
.mx-hero-title {
    margin: 16px 0 8px; color: #FFFFFF; font-weight: 800; letter-spacing: -0.035em; line-height: 1.08;
    font-size: clamp(1.9rem, 3.4vw, 3rem);
}
.mx-hero-sub  { margin: 0 0 6px; color: #C9CCF5; font-size: 15px; line-height: 1.6; }
.mx-hero-note { margin: 10px 0 0; color: #A5A9E6; font-size: 12.5px; }
.mx-hero.is-spam { background: linear-gradient(135deg, #2a0f2e 0%, #6b1d46 55%, #b42343 100%); box-shadow: 0 20px 50px rgba(180, 35, 67, .35); }
.mx-hero.is-ham  { background: linear-gradient(135deg, #06303a 0%, #0e6a6b 55%, #10a58a 100%); box-shadow: 0 20px 50px rgba(16, 165, 138, .32); }

.mx-hero-art { position: relative; display: flex; align-items: center; gap: 12px; flex: 0 0 auto; z-index: 1; }
.mx-bubble {
    position: relative; max-width: 215px; padding: 13px 17px; border-radius: 18px 18px 4px 18px;
    background: #FFFFFF; color: #252653; font-size: 13.5px; line-height: 1.5;
    box-shadow: 0 14px 30px rgba(0, 0, 0, .28); border: 2px solid transparent;
    animation: mxBubble .6s .5s var(--mx-ease) both;
}
.mx-bubble::after { content: ""; position: absolute; right: -9px; bottom: 14px; border: 9px solid transparent; border-left-color: #FFFFFF; border-right: 0; }
.mx-bubble.spam { border-color: #FBBF24; }
.mx-bubble.ham  { border-color: #34D399; }

.mx-robot { width: 178px; height: 188px; overflow: visible; filter: drop-shadow(0 14px 22px rgba(0, 0, 0, .35)); animation: mxFloat 4.5s ease-in-out infinite; }
.g-eyes   { transform-box: view-box; transform-origin: 100px 80px; animation: mxBlink 4s ease-in-out infinite; }
.g-pupil  { animation: mxDart 1.6s ease-in-out infinite alternate; }
.g-wave   { transform-box: view-box; transform-origin: 132px 142px; animation: mxWave .55s ease-in-out infinite alternate; }
.g-search { transform-box: view-box; transform-origin: 160px 122px; animation: mxSearch 2.2s ease-in-out infinite; }
.g-cheer  { transform-box: view-box; transform-origin: 132px 142px; animation: mxCheer .7s var(--mx-ease) both; }
.mx-robot.spam .g-head { transform-box: view-box; transform-origin: 100px 126px; animation: mxTilt 2.6s ease-in-out infinite; }
.mx-robot.ham .g-all   { animation: mxHop .55s ease-out 4; }
.g-ant    { animation: mxDot 1.2s ease-in-out infinite; }
.g-flame  { transform-box: fill-box; transform-origin: top center; animation: mxFlame .25s ease-in-out infinite alternate; }
.g-sweat  { animation: mxSweat 1.8s ease-in infinite; }
.g-q      { animation: mxQ 2.2s ease-in-out infinite; }
.g-q.q2   { animation-delay: 1.1s; }
.g-spark  { transform-box: fill-box; transform-origin: center; animation: mxSpark 1.6s ease-in-out infinite; }

@media (max-width: 760px) {
    .mx-hero { flex-direction: column; align-items: flex-start; padding: 24px 22px; }
    .mx-hero-art { align-self: center; }
    .mx-bubble { max-width: 170px; font-size: 12.5px; }
    .mx-robot { width: 130px; height: 140px; }
}

/* ================= KPI CARDS ================= */
.mx-card {
    background: #FFFFFF; border: 1px solid #E6E7F2; border-radius: 15px;
    padding: 19px 18px; min-height: 118px;
    box-shadow: 0 4px 14px rgba(75, 70, 160, .055);
    transition: transform .25s var(--mx-ease), box-shadow .25s ease;
    animation: mxRise .6s var(--mx-ease) both;
}
.mx-card:hover { transform: translateY(-4px); box-shadow: 0 12px 26px rgba(75, 70, 160, .14); }
.mx-verdict { animation: mxRise .6s var(--mx-ease) both, mxGlow 2.6s .8s ease-in-out 3; }
.mx-verdict.is-spam { animation: mxRise .6s var(--mx-ease) both, mxShake .5s .6s ease both, mxGlow 2.6s 1s ease-in-out 3; }
.mx-label { font-size: 11px; font-weight: 800; letter-spacing: 1px; margin-bottom: 12px; }
.mx-value { font-size: 27px; line-height: 1.2; font-weight: 800; color: #252653; }
.mx-desc  { font-size: 12px; color: #8587A2; margin-top: 7px; }

.mx-count { counter-reset: i var(--i) d var(--d); animation: mxCount 1.2s .25s var(--mx-ease) both; }
.mx-count.pct::after { content: counter(i) "." counter(d) "%"; }
.mx-count.ms::after  { content: counter(i) "." counter(d) " ms"; }
.mx-count.thr::after { content: counter(i) "." counter(d, decimal-leading-zero); }

.mx-bar { position: relative; height: 7px; border-radius: 99px; background: #ECEDF6; margin-top: 12px; }
.mx-bar-fill { height: 100%; border-radius: 99px; animation: mxGrow 1.2s .25s var(--mx-ease) both; }
.mx-bar-mark { position: absolute; top: -4px; width: 2px; height: 15px; background: #252653; border-radius: 2px; opacity: .55; }

.mx-banner {
    border-radius: 13px; padding: 16px 19px; margin: 15px 0 10px 0;
    display: flex; align-items: center; gap: 13px; font-size: 14px; font-weight: 650;
    animation: mxSlide .55s .35s var(--mx-ease) both;
}
.mx-banner-icon { font-size: 23px; display: inline-block; animation: mxPop .6s .6s var(--mx-ease) both; }

/* ================= PANEL: RISK GAUGE ================= */
.mx-panel {
    background: #FFFFFF; border: 1px solid #E6E7F2; border-radius: 18px;
    padding: 18px 22px 20px; min-height: 300px; height: 100%;
    box-shadow: 0 4px 16px rgba(75, 70, 160, .06);
    transition: transform .3s var(--mx-ease), box-shadow .3s var(--mx-ease);
    animation: mxRise .7s .45s var(--mx-ease) both;
}
.mx-panel:hover { transform: translateY(-4px); box-shadow: 0 16px 34px rgba(99, 91, 255, .16); }
.mx-panel-title { font-size: 11px; font-weight: 800; letter-spacing: 1.4px; color: #635BFF; margin-bottom: 4px; }
.mx-panel-sub   { font-size: 12px; color: #8587A2; margin-bottom: 10px; }

.mx-gauge-svg { width: 100%; max-width: 310px; display: block; margin: 4px auto 0; overflow: visible; }
.mx-gauge-svg path { fill: none; stroke-width: 13; }
.g-track { stroke: #ECEDF6; }
.g-ham   { stroke: rgba(13, 148, 136, .30); }
.g-spam  { stroke: rgba(220, 76, 76, .30); }
.g-val   { stroke-linecap: round; stroke-dasharray: 100; animation: mxGauge 1.4s .3s var(--mx-ease) both; }
.g-tick  { stroke: #252653; stroke-width: 2.5; stroke-linecap: round; transform-box: view-box; transform-origin: 100px 100px; }
.g-needle { transform-box: view-box; transform-origin: 100px 100px; animation: mxSwing 1.6s .3s cubic-bezier(.34, 1.56, .64, 1) both; }
.g-needle line { stroke: #252653; stroke-width: 3; stroke-linecap: round; }
.g-needle circle { fill: #252653; }
.g-text { font-size: 8px; fill: #8587A2; font-weight: 700; }

.mx-readout { text-align: center; font-size: 32px; font-weight: 800; color: #252653; margin-top: -2px; line-height: 1.1; }
.mx-state { text-align: center; margin-top: 10px; }
.mx-chip { display: inline-block; padding: 5px 13px; border-radius: 99px; font-size: 12px; font-weight: 750; }
.mx-chip.spam { background: #FFF0EF; color: #B42318; }
.mx-chip.ham  { background: #E4F8F2; color: #087C70; }

@media (max-width: 700px) {
    .mx-value { font-size: 22px; }
    .mx-card  { padding: 14px; }
}

/* ================= PLOTLY CHART MOTION ================= */
[data-testid="stPlotlyChart"] .barlayer .point path {
    transform-box: fill-box; transform-origin: left center;
    animation: mxBarX .9s var(--mx-ease) both;
}
[data-testid="stPlotlyChart"] .barlayer .point:nth-child(2) path { animation-delay: .08s; }
[data-testid="stPlotlyChart"] .barlayer .point:nth-child(3) path { animation-delay: .16s; }
[data-testid="stPlotlyChart"] .barlayer .point:nth-child(4) path { animation-delay: .24s; }
[data-testid="stPlotlyChart"] .barlayer .point:nth-child(5) path { animation-delay: .32s; }
[data-testid="stPlotlyChart"] .barlayer .point:nth-child(6) path { animation-delay: .40s; }
[data-testid="stPlotlyChart"] .barlayer .point:nth-child(7) path { animation-delay: .48s; }
[data-testid="stPlotlyChart"] .barlayer .point:nth-child(n+8) path { animation-delay: .56s; }
[data-testid="stPlotlyChart"] .scatterlayer .trace .lines path:not([style*="stroke-dasharray"]) { animation: mxDraw 1.6s var(--mx-ease) both; }
[data-testid="stPlotlyChart"] .scatterlayer .trace .points path { animation: mxFadeIn .6s .9s both; }
[data-testid="stPlotlyChart"] .heatmaplayer { animation: mxFadeIn .9s both; }

/* ================= REDUCED MOTION ================= */
@media (prefers-reduced-motion: reduce) {
    .mx-hero, .mx-hero::after, .mx-hero-grid, .mx-blob, .mx-robot, .mx-robot *, .mx-bubble, .mx-pill .dot, .mx-card, .mx-verdict, .mx-verdict.is-spam, .mx-count,
    .mx-bar-fill, .mx-banner, .mx-banner-icon, .mx-panel, .g-val, .g-needle,
    [data-testid="stPlotlyChart"] * { animation: none !important; }
    .mx-card, .mx-panel { transition: none; }
}
</style>
"""


def inject_extras() -> None:
    """Inject CSS for the hero, dashboard, gauge and chart motion."""
    st.markdown(EXTRAS_CSS, unsafe_allow_html=True)


_GUARDY = {
    "hello": ("ENGINE ONLINE · MAILGUARD ML", "#34D399", "Hi, I'm <b>Guardy</b>! 👋<br>Paste an email and I'll check it for you."),
    "spam": ("SUSPICIOUS EMAIL DETECTED", "#FBBF24", "Hmm… <b>suspicious</b> 🤨<br>This looks like spam. Don't click any links!"),
    "ham": ("ALL CLEAR · EMAIL LOOKS SAFE", "#34D399", "All clear! 😄<br>This email looks safe to me."),
}


def _guardy_svg(state: str) -> str:
    """Original cartoon robot: waves hello, squints at spam, cheers at safe email."""
    sc = {"hello": "#38BDF8", "spam": "#FBBF24", "ham": "#34D399"}.get(state, "#38BDF8")
    arm = "#C9CDF5"
    hand = 'fill="#F3F4FF" stroke="#B9BEF0" stroke-width="2.5"'

    if state == "spam":
        face = f"""
        <g>
          <circle cx="82" cy="82" r="10" fill="#FFFFFF"/><circle cx="118" cy="82" r="10" fill="#FFFFFF"/>
          <circle class="g-pupil" cx="82" cy="83" r="4.6" fill="#14113F"/><circle class="g-pupil" cx="118" cy="83" r="4.6" fill="#14113F"/>
        </g>
        <polygon points="69,70 95,70 95,80 69,74" fill="#14113F"/>
        <polygon points="105,70 131,70 131,74 105,80" fill="#14113F"/>
        <line x1="70" y1="64" x2="94" y2="68" stroke="{sc}" stroke-width="4" stroke-linecap="round"/>
        <path d="M106 66 Q118 56 130 63" fill="none" stroke="{sc}" stroke-width="4" stroke-linecap="round"/>
        <path d="M88 101 Q94 97 100 101 T112 101" fill="none" stroke="{sc}" stroke-width="3.5" stroke-linecap="round"/>
        <path class="g-sweat" d="M154 58 Q160 70 154 74 Q148 70 154 58Z" fill="#7DD3FC"/>
        """
        right_arm = f"""
        <g class="g-search">
          <line x1="132" y1="142" x2="158" y2="124" stroke="{arm}" stroke-width="12" stroke-linecap="round"/>
          <circle cx="160" cy="122" r="9" {hand}/>
          <line x1="164" y1="116" x2="174" y2="104" stroke="{sc}" stroke-width="5" stroke-linecap="round"/>
          <circle cx="182" cy="92" r="15" fill="rgba(251,191,36,.16)" stroke="{sc}" stroke-width="5"/>
          <path d="M174 90 A9 9 0 0 1 181 83" stroke="#FFFFFF" stroke-width="2.5" fill="none" stroke-linecap="round" opacity=".85"/>
        </g>
        """
        extras = (
            f'<text class="g-q" x="16" y="62" font-size="24" font-weight="800" fill="{sc}">?</text>'
            f'<text class="g-q q2" x="32" y="34" font-size="17" font-weight="800" fill="{sc}">?</text>'
        )
    elif state == "ham":
        face = f"""
        <path d="M70 87 Q82 72 94 87" fill="none" stroke="{sc}" stroke-width="5" stroke-linecap="round"/>
        <path d="M106 87 Q118 72 130 87" fill="none" stroke="{sc}" stroke-width="5" stroke-linecap="round"/>
        <path d="M84 96 Q100 115 116 96 Z" fill="{sc}"/>
        <ellipse cx="100" cy="104" rx="6" ry="3" fill="#F9A8D4"/>
        <ellipse cx="66" cy="96" rx="6.5" ry="4" fill="#F9A8D4" opacity=".65"/>
        <ellipse cx="134" cy="96" rx="6.5" ry="4" fill="#F9A8D4" opacity=".65"/>
        """
        right_arm = f"""
        <g class="g-cheer">
          <line x1="132" y1="142" x2="160" y2="112" stroke="{arm}" stroke-width="12" stroke-linecap="round"/>
          <rect x="158" y="88" width="9" height="18" rx="4.5" {hand}/>
          <circle cx="163" cy="109" r="10" {hand}/>
        </g>
        """
        sparks = [(26, 48, 0.0), (186, 62, 0.5), (22, 122, 1.0), (192, 134, 0.3)]
        extras = "".join(
            f'<g transform="translate({x},{y})"><path class="g-spark" style="animation-delay:{d}s" '
            f'd="M0 -8 L2 -2 L8 0 L2 2 L0 8 L-2 2 L-8 0 L-2 -2Z" fill="#FDE68A"/></g>'
            for x, y, d in sparks
        )
    else:  # hello
        face = f"""
        <g class="g-eyes">
          <circle cx="82" cy="80" r="9" fill="#7DD3FC"/><circle cx="118" cy="80" r="9" fill="#7DD3FC"/>
          <circle cx="85" cy="77" r="3" fill="#FFFFFF"/><circle cx="121" cy="77" r="3" fill="#FFFFFF"/>
        </g>
        <path d="M88 96 Q100 107 112 96" fill="none" stroke="#7DD3FC" stroke-width="4" stroke-linecap="round"/>
        <ellipse cx="68" cy="95" rx="6" ry="3.6" fill="#F9A8D4" opacity=".6"/>
        <ellipse cx="132" cy="95" rx="6" ry="3.6" fill="#F9A8D4" opacity=".6"/>
        """
        right_arm = f"""
        <g class="g-wave">
          <line x1="132" y1="142" x2="162" y2="106" stroke="{arm}" stroke-width="12" stroke-linecap="round"/>
          <circle cx="165" cy="101" r="9.5" {hand}/>
        </g>
        """
        extras = ""

    return _h(
        f"""
        <svg class="mx-robot {state}" viewBox="0 0 215 225" aria-hidden="true">
          <defs>
            <linearGradient id="gdBody" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D8DCFF"/></linearGradient>
            <linearGradient id="gdHead" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DCE0FF"/></linearGradient>
          </defs>
          <ellipse cx="100" cy="216" rx="34" ry="6" fill="rgba(0,0,0,.28)"/>
          <g class="g-all">
            <path class="g-flame" d="M88 192 Q100 214 112 192Z" fill="{sc}" opacity=".8"/>
            <g>
              <line x1="68" y1="142" x2="46" y2="170" stroke="{arm}" stroke-width="12" stroke-linecap="round"/>
              <circle cx="44" cy="173" r="9" {hand}/>
            </g>
            <rect x="66" y="124" width="68" height="68" rx="22" fill="url(#gdBody)" stroke="#B9BEF0" stroke-width="2.5"/>
            <rect x="82" y="142" width="36" height="26" rx="9" fill="#14113F"/>
            <path d="M100 146 L110 150 V157 C110 162 105 165 100 167 C95 165 90 162 90 157 V150 Z" fill="{sc}"/>
            {right_arm}
            <g class="g-head">
              <line x1="100" y1="40" x2="100" y2="23" stroke="#B9BEF0" stroke-width="4" stroke-linecap="round"/>
              <circle class="g-ant" cx="100" cy="17" r="7" fill="{sc}"/>
              <rect x="34" y="66" width="12" height="28" rx="6" fill="{arm}"/>
              <rect x="154" y="66" width="12" height="28" rx="6" fill="{arm}"/>
              <rect x="42" y="38" width="116" height="88" rx="32" fill="url(#gdHead)" stroke="#B9BEF0" stroke-width="2.5"/>
              <rect x="56" y="54" width="88" height="56" rx="22" fill="#14113F"/>
              {face}
            </g>
            {extras}
          </g>
        </svg>
        """
    )


def hero_banner(title: str, subtitle: str, note: str = "", state: str = "hello") -> None:
    """Animated dark hero header with the Guardy mascot.

    state: "hello" (waving), "spam" (suspicious) or "ham" (happy). Display only.
    """
    if state not in _GUARDY:
        state = "hello"
    pill_text, dot_color, bubble = _GUARDY[state]
    note_html = f'<p class="mx-hero-note">🔒 {escape(note)}</p>' if note else ""
    st.markdown(
        _h(
            f"""
            <div class="mx-hero is-{state}">
              <div class="mx-blob b1"></div><div class="mx-blob b2"></div><div class="mx-hero-grid"></div>
              <div class="mx-hero-body">
                <div class="mx-pill" style="--dot:{dot_color};"><span class="dot"></span>{pill_text}</div>
                <div class="mx-hero-title" role="heading" aria-level="1">{escape(title)}</div>
                <p class="mx-hero-sub">{escape(subtitle)}</p>
                {note_html}
              </div>
              <div class="mx-hero-art">
                <div class="mx-bubble {state}" role="status">{bubble}</div>
                {_guardy_svg(state)}
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def _split(value: float, decimals: int) -> tuple[str, str]:
    whole, frac = f"{value:.{decimals}f}".split(".")
    return whole, frac


def _gauge_html(prob: float, threshold: float, is_spam: bool) -> str:
    pct = max(0.0, min(100.0, prob * 100))
    t = max(0.0, min(100.0, threshold * 100))
    color = "#DC4C4C" if is_spam else "#0D9488"
    needle = pct * 1.8 - 90
    tick = t * 1.8 - 90
    arc = "M20 100A80 80 0 0 1 180 100"
    p_i, p_d = _split(pct, 1)
    state_cls = "spam" if is_spam else "ham"
    state_txt = "▲ Above threshold" if is_spam else "▼ Below threshold"
    return _h(
        f"""
        <div class="mx-panel">
          <div class="mx-panel-title">RISK GAUGE</div>
          <div class="mx-panel-sub">Needle = model probability · tick = decision threshold</div>
          <svg class="mx-gauge-svg" viewBox="0 0 200 122" role="img"
               aria-label="Spam probability {pct:.1f} percent, threshold {threshold:.2f}">
            <path class="g-track" d="{arc}" pathLength="100"/>
            <path class="g-ham"   d="{arc}" pathLength="100" style="stroke-dasharray:{t:.2f} 100"/>
            <path class="g-spam"  d="{arc}" pathLength="100" style="stroke-dasharray:0 {t:.2f} {100 - t:.2f} 100"/>
            <path class="g-val"   d="{arc}" pathLength="100" style="stroke:{color};stroke-dashoffset:{100 - pct:.2f}"/>
            <line class="g-tick" x1="100" y1="6" x2="100" y2="30" style="transform:rotate({tick:.2f}deg)"/>
            <g class="g-needle" style="transform:rotate({needle:.2f}deg)">
              <line x1="100" y1="100" x2="100" y2="36"/><circle cx="100" cy="100" r="6"/>
            </g>
            <text class="g-text" x="20" y="118" text-anchor="middle">0%</text>
            <text class="g-text" x="180" y="118" text-anchor="middle">100%</text>
          </svg>
          <div class="mx-readout">
            <span class="mx-count pct" role="img" aria-label="{prob:.1%}" style="--i:{p_i}; --d:{p_d};"></span>
          </div>
          <div class="mx-state"><span class="mx-chip {state_cls}">{state_txt}</span></div>
        </div>
        """
    )


def render_dashboard(result: Any, threshold: float, is_spam: bool) -> None:
    """KPI cards, result banner and risk gauge."""
    verdict = "SPAM" if is_spam else "HAM"
    verdict_color = "#DC4C4C" if is_spam else "#0D9488"
    verdict_bg = "#FFF0EF" if is_spam else "#E4F8F2"
    glow = "220, 76, 76" if is_spam else "13, 148, 136"
    verdict_description = "Potentially suspicious email" if is_spam else "Legitimate email"

    pct = result.spam_probability * 100
    prob_i, prob_d = _split(pct, 1)
    lat_i, lat_d = _split(result.latency_ms, 1)
    thr_i, thr_d = _split(threshold, 2)
    bar_pct = max(0.0, min(100.0, pct))
    thr_pct = max(0.0, min(100.0, threshold * 100))

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        st.markdown(
            _h(
                f"""
                <div class="mx-card mx-verdict {'is-spam' if is_spam else ''}"
                     style="background:{verdict_bg}; --glow:{glow};">
                  <div class="mx-label" style="color:{verdict_color};">VERDICT</div>
                  <div class="mx-value" style="color:{verdict_color};">{verdict}</div>
                  <div class="mx-desc">{verdict_description}</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            _h(
                f"""
                <div class="mx-card" style="animation-delay:.1s;">
                  <div class="mx-label" style="color:#635BFF;">SPAM PROBABILITY</div>
                  <div class="mx-value"><span class="mx-count pct" role="img" aria-label="{result.spam_probability:.1%}"
                       style="--i:{prob_i}; --d:{prob_d};"></span></div>
                  <div class="mx-bar">
                    <div class="mx-bar-fill" style="width:{bar_pct:.1f}%; background:{verdict_color};"></div>
                    <div class="mx-bar-mark" style="left:{thr_pct:.1f}%;" title="Threshold {threshold:.2f}"></div>
                  </div>
                  <div class="mx-desc">Model probability · marker = threshold</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            _h(
                f"""
                <div class="mx-card" style="animation-delay:.2s;">
                  <div class="mx-label" style="color:#D18A22;">DECISION THRESHOLD</div>
                  <div class="mx-value"><span class="mx-count thr" role="img" aria-label="{threshold:.2f}"
                       style="--i:{thr_i}; --d:{int(thr_d)};"></span></div>
                  <div class="mx-desc">Current classification threshold</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            _h(
                f"""
                <div class="mx-card" style="animation-delay:.3s;">
                  <div class="mx-label" style="color:#2878C7;">PROCESSING TIME</div>
                  <div class="mx-value"><span class="mx-count ms" role="img" aria-label="{result.latency_ms:.1f} ms"
                       style="--i:{lat_i}; --d:{lat_d};"></span></div>
                  <div class="mx-desc">Analysis latency</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    # ----- result banner -----
    if is_spam:
        banner_style = "background:#FFF0EF;color:#B42318;border:1px solid #F8C9C5;"
        icon, headline, op = "⚠️", "Potential spam detected", "≥"
    else:
        banner_style = "background:#E4F8F2;color:#087C70;border:1px solid #B8EBDD;"
        icon, headline, op = "✓", "Email classified as legitimate", "&lt;"
    st.markdown(
        _h(
            f"""
            <div class="mx-banner" style="{banner_style}">
              <span class="mx-banner-icon">{icon}</span>
              <div><div>{headline}</div>
                <div style="font-size:12px;font-weight:400;margin-top:4px;">
                  Spam probability {result.spam_probability:.3f} {op} threshold {threshold:.2f}
                </div></div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    # ----- risk gauge -----
    _, g_col, _ = st.columns([1, 1.3, 1], gap="medium")
    with g_col:
        st.markdown(_gauge_html(result.spam_probability, threshold, is_spam), unsafe_allow_html=True)