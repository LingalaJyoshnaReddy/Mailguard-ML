"""Guardy - MailGuard's cartoon robot mascot + animated hero banner.

Self-contained (own CSS, own class names) so it works regardless of what
other UI files contain. Presentation only: it just draws what it is told.

    guardy_hero(title, subtitle, note="", state="hello")

state: "hello" (waving) | "spam" (suspicious) | "ham" (happy)
"""

from __future__ import annotations

from html import escape

import streamlit as st


def _h(markup: str) -> str:
    """Collapse markup onto one line so Markdown never treats indentation as code."""
    return " ".join(line.strip() for line in markup.splitlines() if line.strip())


GUARDY_CSS = """
<style>
:root { --gd-ease: cubic-bezier(.22, .8, .3, 1); }

@keyframes gdRise    { from { opacity: 0; transform: translateY(20px) scale(.97); } to { opacity: 1; transform: none; } }
@keyframes gdBlob    { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(30px,-18px) scale(1.15); } }
@keyframes gdGrid    { from { background-position: 0 0; } to { background-position: 44px 44px; } }
@keyframes gdSweep   { 0% { transform: translateX(-120%) skewX(-18deg); } 60%,100% { transform: translateX(520%) skewX(-18deg); } }
@keyframes gdDot     { 0%,100% { opacity: 1; } 50% { opacity: .3; } }
@keyframes gdFloat   { 0%,100% { transform: translateY(0); } 50% { transform: translateY(-9px); } }
@keyframes gdBubble  { from { opacity: 0; transform: scale(.6) translateX(14px); } to { opacity: 1; transform: none; } }
@keyframes gdWave    { from { transform: rotate(-12deg); } to { transform: rotate(22deg); } }
@keyframes gdBlink   { 0%,90%,100% { transform: scaleY(1); } 94% { transform: scaleY(.1); } }
@keyframes gdDart    { from { transform: translateX(-3.2px); } to { transform: translateX(3.2px); } }
@keyframes gdTilt    { 0%,100% { transform: rotate(0deg); } 50% { transform: rotate(-6deg); } }
@keyframes gdHop     { 0%,100% { transform: translateY(0); } 45% { transform: translateY(-14px); } }
@keyframes gdSearch  { 0%,100% { transform: rotate(-4deg); } 50% { transform: rotate(8deg); } }
@keyframes gdCheer   { from { transform: rotate(-35deg) scale(.6); opacity: 0; } to { transform: none; opacity: 1; } }
@keyframes gdSweat   { 0% { transform: translateY(-4px); opacity: 0; } 30% { opacity: 1; } 100% { transform: translateY(16px); opacity: 0; } }
@keyframes gdQ       { 0% { opacity: 0; transform: translateY(8px); } 40%,70% { opacity: 1; } 100% { opacity: 0; transform: translateY(-12px); } }
@keyframes gdSpark   { 0%,100% { transform: scale(.2); opacity: 0; } 50% { transform: scale(1.1); opacity: 1; } }
@keyframes gdFlame   { from { transform: scaleY(.7); } to { transform: scaleY(1.25); } }

.gd-hero {
    position: relative; overflow: hidden; isolation: isolate;
    display: flex; align-items: center; justify-content: space-between; gap: 24px;
    padding: 34px 40px; margin-bottom: 10px; border-radius: 24px;
    background: linear-gradient(135deg, #14113f 0%, #2a2590 55%, #4f46e5 100%);
    box-shadow: 0 20px 50px rgba(52, 44, 160, .35);
    animation: gdRise .8s var(--gd-ease) both;
}
.gd-hero.is-spam { background: linear-gradient(135deg, #2a0f2e 0%, #6b1d46 55%, #b42343 100%); box-shadow: 0 20px 50px rgba(180, 35, 67, .35); }
.gd-hero.is-ham  { background: linear-gradient(135deg, #06303a 0%, #0e6a6b 55%, #10a58a 100%); box-shadow: 0 20px 50px rgba(16, 165, 138, .32); }

.gd-grid {
    position: absolute; inset: 0; z-index: -1; opacity: .5;
    background-image:
        linear-gradient(rgba(255,255,255,.07) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.07) 1px, transparent 1px);
    background-size: 44px 44px; animation: gdGrid 6s linear infinite;
    mask-image: radial-gradient(ellipse at 70% 40%, #000 20%, transparent 75%);
    -webkit-mask-image: radial-gradient(ellipse at 70% 40%, #000 20%, transparent 75%);
}
.gd-blob { position: absolute; border-radius: 50%; filter: blur(60px); z-index: -2; animation: gdBlob 9s ease-in-out infinite; }
.gd-blob.b1 { width: 320px; height: 320px; background: #38BDF8; opacity: .35; right: -60px; top: -120px; }
.gd-blob.b2 { width: 260px; height: 260px; background: #9333EA; opacity: .45; left: 30%; bottom: -140px; animation-delay: -4s; }
.gd-hero::after {
    content: ""; position: absolute; top: 0; bottom: 0; left: 0; width: 18%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.13), transparent);
    animation: gdSweep 6s ease-in-out infinite; pointer-events: none;
}

.gd-body { max-width: 720px; position: relative; z-index: 1; }
.gd-pill {
    display: inline-flex; align-items: center; gap: 9px; padding: 6px 14px; border-radius: 99px;
    background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.22);
    color: #DDE0FF; font-size: 11px; font-weight: 800; letter-spacing: 1.6px; backdrop-filter: blur(6px);
}
.gd-pill .dot { width: 8px; height: 8px; border-radius: 50%; background: var(--dot, #34D399); box-shadow: 0 0 10px var(--dot, #34D399); animation: gdDot 1.6s ease-in-out infinite; }
.gd-title { margin: 16px 0 8px; color: #FFFFFF; font-weight: 800; letter-spacing: -0.035em; line-height: 1.08; font-size: clamp(1.9rem, 3.4vw, 3rem); }
.gd-sub   { margin: 0 0 6px; color: #C9CCF5; font-size: 15px; line-height: 1.6; }
.gd-note  { margin: 10px 0 0; color: #A5A9E6; font-size: 12.5px; }

.gd-art { position: relative; display: flex; align-items: center; gap: 12px; flex: 0 0 auto; z-index: 1; }
.gd-bubble {
    position: relative; max-width: 215px; padding: 13px 17px; border-radius: 18px 18px 4px 18px;
    background: #FFFFFF; color: #252653; font-size: 13.5px; line-height: 1.5;
    box-shadow: 0 14px 30px rgba(0, 0, 0, .28); border: 2px solid transparent;
    animation: gdBubble .6s .5s var(--gd-ease) both;
}
.gd-bubble::after { content: ""; position: absolute; right: -9px; bottom: 14px; border: 9px solid transparent; border-left-color: #FFFFFF; border-right: 0; }
.gd-bubble.spam { border-color: #FBBF24; }
.gd-bubble.ham  { border-color: #34D399; }

.gd-robot { width: 178px; height: 188px; overflow: visible; filter: drop-shadow(0 14px 22px rgba(0,0,0,.35)); animation: gdFloat 4.5s ease-in-out infinite; }
.gr-eyes   { transform-box: view-box; transform-origin: 100px 80px; animation: gdBlink 4s ease-in-out infinite; }
.gr-pupil  { animation: gdDart 1.6s ease-in-out infinite alternate; }
.gr-wave   { transform-box: view-box; transform-origin: 132px 142px; animation: gdWave .55s ease-in-out infinite alternate; }
.gr-search { transform-box: view-box; transform-origin: 160px 122px; animation: gdSearch 2.2s ease-in-out infinite; }
.gr-cheer  { transform-box: view-box; transform-origin: 132px 142px; animation: gdCheer .7s var(--gd-ease) both; }
.gd-robot.spam .gr-head { transform-box: view-box; transform-origin: 100px 126px; animation: gdTilt 2.6s ease-in-out infinite; }
.gd-robot.ham .gr-all   { animation: gdHop .55s ease-out 4; }
.gr-ant    { animation: gdDot 1.2s ease-in-out infinite; }
.gr-flame  { transform-box: fill-box; transform-origin: top center; animation: gdFlame .25s ease-in-out infinite alternate; }
.gr-sweat  { animation: gdSweat 1.8s ease-in infinite; }
.gr-q      { animation: gdQ 2.2s ease-in-out infinite; }
.gr-q.q2   { animation-delay: 1.1s; }
.gr-spark  { transform-box: fill-box; transform-origin: center; animation: gdSpark 1.6s ease-in-out infinite; }

@media (max-width: 760px) {
    .gd-hero { flex-direction: column; align-items: flex-start; padding: 24px 22px; }
    .gd-art { align-self: center; }
    .gd-bubble { max-width: 170px; font-size: 12.5px; }
    .gd-robot { width: 130px; height: 140px; }
}
@media (prefers-reduced-motion: reduce) {
    .gd-hero, .gd-hero::after, .gd-grid, .gd-blob, .gd-robot, .gd-robot *, .gd-bubble, .gd-pill .dot { animation: none !important; }
}
</style>
"""

_TEXT = {
    "hello": ("ENGINE ONLINE · MAILGUARD ML", "#34D399", "Hi, I'm <b>Guardy</b>! 👋<br>Paste an email and I'll check it for you."),
    "spam": ("SUSPICIOUS EMAIL DETECTED", "#FBBF24", "Hmm… <b>suspicious</b> 🤨<br>This looks like spam. Don't click any links!"),
    "ham": ("ALL CLEAR · EMAIL LOOKS SAFE", "#34D399", "All clear! 😄<br>This email looks safe to me."),
}


def _robot(state: str) -> str:
    """Original cartoon robot: waves hello, squints at spam, cheers at safe email."""
    sc = {"hello": "#38BDF8", "spam": "#FBBF24", "ham": "#34D399"}.get(state, "#38BDF8")
    arm = "#C9CDF5"
    hand = 'fill="#F3F4FF" stroke="#B9BEF0" stroke-width="2.5"'

    if state == "spam":
        face = f"""
        <g>
          <circle cx="82" cy="82" r="10" fill="#FFFFFF"/><circle cx="118" cy="82" r="10" fill="#FFFFFF"/>
          <circle class="gr-pupil" cx="82" cy="83" r="4.6" fill="#14113F"/><circle class="gr-pupil" cx="118" cy="83" r="4.6" fill="#14113F"/>
        </g>
        <polygon points="69,70 95,70 95,80 69,74" fill="#14113F"/>
        <polygon points="105,70 131,70 131,74 105,80" fill="#14113F"/>
        <line x1="70" y1="64" x2="94" y2="68" stroke="{sc}" stroke-width="4" stroke-linecap="round"/>
        <path d="M106 66 Q118 56 130 63" fill="none" stroke="{sc}" stroke-width="4" stroke-linecap="round"/>
        <path d="M88 101 Q94 97 100 101 T112 101" fill="none" stroke="{sc}" stroke-width="3.5" stroke-linecap="round"/>
        <path class="gr-sweat" d="M154 58 Q160 70 154 74 Q148 70 154 58Z" fill="#7DD3FC"/>
        """
        right_arm = f"""
        <g class="gr-search">
          <line x1="132" y1="142" x2="158" y2="124" stroke="{arm}" stroke-width="12" stroke-linecap="round"/>
          <circle cx="160" cy="122" r="9" {hand}/>
          <line x1="164" y1="116" x2="174" y2="104" stroke="{sc}" stroke-width="5" stroke-linecap="round"/>
          <circle cx="182" cy="92" r="15" fill="rgba(251,191,36,.16)" stroke="{sc}" stroke-width="5"/>
          <path d="M174 90 A9 9 0 0 1 181 83" stroke="#FFFFFF" stroke-width="2.5" fill="none" stroke-linecap="round" opacity=".85"/>
        </g>
        """
        extras = (
            f'<text class="gr-q" x="16" y="62" font-size="24" font-weight="800" fill="{sc}">?</text>'
            f'<text class="gr-q q2" x="32" y="34" font-size="17" font-weight="800" fill="{sc}">?</text>'
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
        <g class="gr-cheer">
          <line x1="132" y1="142" x2="160" y2="112" stroke="{arm}" stroke-width="12" stroke-linecap="round"/>
          <rect x="158" y="88" width="9" height="18" rx="4.5" {hand}/>
          <circle cx="163" cy="109" r="10" {hand}/>
        </g>
        """
        sparks = [(26, 48, 0.0), (186, 62, 0.5), (22, 122, 1.0), (192, 134, 0.3)]
        extras = "".join(
            f'<g transform="translate({x},{y})"><path class="gr-spark" style="animation-delay:{d}s" '
            f'd="M0 -8 L2 -2 L8 0 L2 2 L0 8 L-2 2 L-8 0 L-2 -2Z" fill="#FDE68A"/></g>'
            for x, y, d in sparks
        )
    else:  # hello
        face = f"""
        <g class="gr-eyes">
          <circle cx="82" cy="80" r="9" fill="#7DD3FC"/><circle cx="118" cy="80" r="9" fill="#7DD3FC"/>
          <circle cx="85" cy="77" r="3" fill="#FFFFFF"/><circle cx="121" cy="77" r="3" fill="#FFFFFF"/>
        </g>
        <path d="M88 96 Q100 107 112 96" fill="none" stroke="#7DD3FC" stroke-width="4" stroke-linecap="round"/>
        <ellipse cx="68" cy="95" rx="6" ry="3.6" fill="#F9A8D4" opacity=".6"/>
        <ellipse cx="132" cy="95" rx="6" ry="3.6" fill="#F9A8D4" opacity=".6"/>
        """
        right_arm = f"""
        <g class="gr-wave">
          <line x1="132" y1="142" x2="162" y2="106" stroke="{arm}" stroke-width="12" stroke-linecap="round"/>
          <circle cx="165" cy="101" r="9.5" {hand}/>
        </g>
        """
        extras = ""

    return _h(
        f"""
        <svg class="gd-robot {state}" viewBox="0 0 215 225" aria-hidden="true">
          <defs>
            <linearGradient id="grBody" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D8DCFF"/></linearGradient>
            <linearGradient id="grHead" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#DCE0FF"/></linearGradient>
          </defs>
          <ellipse cx="100" cy="216" rx="34" ry="6" fill="rgba(0,0,0,.28)"/>
          <g class="gr-all">
            <path class="gr-flame" d="M88 192 Q100 214 112 192Z" fill="{sc}" opacity=".8"/>
            <g>
              <line x1="68" y1="142" x2="46" y2="170" stroke="{arm}" stroke-width="12" stroke-linecap="round"/>
              <circle cx="44" cy="173" r="9" {hand}/>
            </g>
            <rect x="66" y="124" width="68" height="68" rx="22" fill="url(#grBody)" stroke="#B9BEF0" stroke-width="2.5"/>
            <rect x="82" y="142" width="36" height="26" rx="9" fill="#14113F"/>
            <path d="M100 146 L110 150 V157 C110 162 105 165 100 167 C95 165 90 162 90 157 V150 Z" fill="{sc}"/>
            {right_arm}
            <g class="gr-head">
              <line x1="100" y1="40" x2="100" y2="23" stroke="#B9BEF0" stroke-width="4" stroke-linecap="round"/>
              <circle class="gr-ant" cx="100" cy="17" r="7" fill="{sc}"/>
              <rect x="34" y="66" width="12" height="28" rx="6" fill="{arm}"/>
              <rect x="154" y="66" width="12" height="28" rx="6" fill="{arm}"/>
              <rect x="42" y="38" width="116" height="88" rx="32" fill="url(#grHead)" stroke="#B9BEF0" stroke-width="2.5"/>
              <rect x="56" y="54" width="88" height="56" rx="22" fill="#14113F"/>
              {face}
            </g>
            {extras}
          </g>
        </svg>
        """
    )


def guardy_hero(title: str, subtitle: str, note: str = "", state: str = "hello") -> None:
    """Animated hero banner with Guardy. Display only."""
    if state not in _TEXT:
        state = "hello"
    pill_text, dot_color, bubble = _TEXT[state]
    note_html = f'<p class="gd-note">🔒 {escape(note)}</p>' if note else ""
    st.markdown(GUARDY_CSS, unsafe_allow_html=True)
    st.markdown(
        _h(
            f"""
            <div class="gd-hero is-{state}">
              <div class="gd-blob b1"></div><div class="gd-blob b2"></div><div class="gd-grid"></div>
              <div class="gd-body">
                <div class="gd-pill" style="--dot:{dot_color};"><span class="dot"></span>{pill_text}</div>
                <div class="gd-title" role="heading" aria-level="1">{escape(title)}</div>
                <p class="gd-sub">{escape(subtitle)}</p>
                {note_html}
              </div>
              <div class="gd-art">
                <div class="gd-bubble {state}" role="status">{bubble}</div>
                {_robot(state)}
              </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )