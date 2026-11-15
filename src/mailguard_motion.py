"""
mailguard_motion.py - page-wide animation layer (presentation only).

Usage in views/analyzer.py (and any other page):

    from mailguard_motion import inject_motion
    inject_mailguard_styles()
    inject_motion()
"""
import streamlit as st

MOTION_CSS = """
<style>
:root{
  --mg-p:#635BFF; --mg-p2:#8B7BFF; --mg-sky:#38BDF8;
  --mg-ease:cubic-bezier(.22,.8,.3,1);
}

@keyframes mgUp     {from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:none}}
@keyframes mgFlow   {0%{background-position:0% 50%}100%{background-position:200% 50%}}
@keyframes mgShine  {0%{transform:translateX(-120%) skewX(-20deg)}55%,100%{transform:translateX(320%) skewX(-20deg)}}
@keyframes mgRing   {0%{box-shadow:0 0 0 0 rgba(13,148,136,.45)}100%{box-shadow:0 0 0 14px rgba(13,148,136,0)}}
@keyframes mgGrowX  {from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes mgScan   {0%{top:0;opacity:0}15%{opacity:1}85%{opacity:1}100%{top:calc(100% - 3px);opacity:0}}
@keyframes mgBlink  {0%,100%{opacity:1}50%{opacity:.35}}
@keyframes mgFloat  {0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}

/* ---------- Animated background ---------- */
.stApp{
  background:
    radial-gradient(800px 380px at 90% -10%, rgba(99,91,255,.12), transparent 60%),
    radial-gradient(700px 320px at -5% 5%, rgba(56,189,248,.10), transparent 60%),
    #F6F7FB;
}

/* ---------- Hero title: flowing gradient text ---------- */
.stApp h1{
  background:linear-gradient(90deg,#1B1F4B,#635BFF,#38BDF8,#635BFF,#1B1F4B);
  background-size:200% auto;
  -webkit-background-clip:text; background-clip:text;
  -webkit-text-fill-color:transparent; color:transparent;
  animation:mgFlow 7s linear infinite, mgUp .8s var(--mg-ease) both;
  letter-spacing:-.03em;
}
.stApp h1 + div, [data-testid="stCaptionContainer"]{animation:mgUp .8s .15s var(--mg-ease) both}

/* ---------- Staggered page entrance ---------- */
[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] > div{
  animation:mgUp .75s var(--mg-ease) both;
}
[data-testid="stMainBlockContainer"] > div > [data-testid="stVerticalBlock"] > div:nth-child(1){animation-delay:.00s}
[data-testid="stMainBlockContainer"] > div > [data-testid="stVerticalBlock"] > div:nth-child(2){animation-delay:.08s}
[data-testid="stMainBlockContainer"] > div > [data-testid="stVerticalBlock"] > div:nth-child(3){animation-delay:.16s}
[data-testid="stMainBlockContainer"] > div > [data-testid="stVerticalBlock"] > div:nth-child(4){animation-delay:.24s}
[data-testid="stMainBlockContainer"] > div > [data-testid="stVerticalBlock"] > div:nth-child(5){animation-delay:.32s}
[data-testid="stMainBlockContainer"] > div > [data-testid="stVerticalBlock"] > div:nth-child(6){animation-delay:.40s}
[data-testid="stMainBlockContainer"] > div > [data-testid="stVerticalBlock"] > div:nth-child(n+7){animation-delay:.48s}

/* ---------- Bordered cards: lift + glowing accent line ---------- */
[data-testid="stVerticalBlockBorderWrapper"]{
  position:relative; overflow:hidden;
  background:#fff;
  border:1px solid rgba(99,91,255,.14)!important;
  border-radius:18px!important;
  box-shadow:0 1px 2px rgba(20,20,60,.05),0 10px 28px rgba(20,20,60,.06);
  transition:transform .35s var(--mg-ease),box-shadow .35s var(--mg-ease),border-color .3s;
}
[data-testid="stVerticalBlockBorderWrapper"]::before{
  content:""; position:absolute; left:0; right:0; top:0; height:3px;
  background:linear-gradient(90deg,var(--mg-p),var(--mg-sky),var(--mg-p));
  background-size:200% 100%;
  transform:scaleX(0); transform-origin:left;
  transition:transform .5s var(--mg-ease);
  animation:mgFlow 4s linear infinite;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover{
  transform:translateY(-5px);
  box-shadow:0 4px 8px rgba(20,20,60,.06),0 24px 48px rgba(99,91,255,.20);
  border-color:rgba(99,91,255,.38)!important;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover::before{transform:scaleX(1)}

/* ---------- Primary button: gradient + sweeping shine ---------- */
[data-testid="stBaseButton-primary"], button[kind="primary"]{
  position:relative; overflow:hidden;
  background:linear-gradient(120deg,var(--mg-p),var(--mg-p2),var(--mg-sky),var(--mg-p))!important;
  background-size:250% 100%;
  border:none!important; border-radius:14px!important;
  animation:mgFlow 6s linear infinite;
  transition:transform .2s var(--mg-ease),box-shadow .3s var(--mg-ease);
}
[data-testid="stBaseButton-primary"]::after, button[kind="primary"]::after{
  content:""; position:absolute; top:0; bottom:0; left:0; width:35%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.55),transparent);
  animation:mgShine 3.2s ease-in-out infinite;
  pointer-events:none;
}
[data-testid="stBaseButton-primary"]:hover, button[kind="primary"]:hover{
  transform:translateY(-3px) scale(1.015);
  box-shadow:0 14px 30px rgba(99,91,255,.45);
}
[data-testid="stBaseButton-primary"]:active, button[kind="primary"]:active{transform:scale(.97)}

[data-testid="stBaseButton-secondary"]{
  border-radius:12px!important;
  transition:transform .2s var(--mg-ease),box-shadow .25s,border-color .2s,color .2s;
}
[data-testid="stBaseButton-secondary"]:hover{
  transform:translateY(-2px); border-color:var(--mg-p)!important; color:var(--mg-p)!important;
  box-shadow:0 8px 18px rgba(99,91,255,.18);
}

/* ---------- Inputs ---------- */
[data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input,
[data-baseweb="select"] > div{
  border-radius:12px!important;
  transition:box-shadow .3s var(--mg-ease),border-color .25s,transform .25s var(--mg-ease);
}
[data-testid="stTextArea"] textarea:focus{
  border-color:var(--mg-p)!important;
  box-shadow:0 0 0 4px rgba(99,91,255,.18),0 10px 24px rgba(99,91,255,.12)!important;
  transform:translateY(-1px);
}
[data-testid="stFileUploader"] section{
  border:2px dashed rgba(99,91,255,.35); border-radius:14px;
  transition:background .3s,border-color .3s,transform .3s var(--mg-ease);
}
[data-testid="stFileUploader"] section:hover{
  background:rgba(99,91,255,.06); border-color:var(--mg-p); transform:scale(1.01);
}

/* ---------- Slider ---------- */
[data-testid="stSlider"] [role="slider"]{
  transition:transform .2s var(--mg-ease),box-shadow .25s;
}
[data-testid="stSlider"] [role="slider"]:hover,
[data-testid="stSlider"] [role="slider"]:active{
  transform:scale(1.35); box-shadow:0 0 0 10px rgba(99,91,255,.16);
}

/* ---------- Tabs ---------- */
[data-testid="stTabs"] button[role="tab"]{
  transition:color .25s,background .25s,transform .25s var(--mg-ease);
  border-radius:10px 10px 0 0;
}
[data-testid="stTabs"] button[role="tab"]:hover{background:rgba(99,91,255,.09); transform:translateY(-2px)}
[data-testid="stTabs"] [data-baseweb="tab-highlight"]{
  background:linear-gradient(90deg,var(--mg-p),var(--mg-sky))!important; height:3px!important;
  transition:left .45s var(--mg-ease),width .45s var(--mg-ease);
}
[data-testid="stTabs"] [role="tabpanel"]{animation:mgUp .5s var(--mg-ease) both}

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"]{
  background:rgba(255,255,255,.80); backdrop-filter:blur(12px);
  border-right:1px solid rgba(99,91,255,.12);
}
[data-testid="stSidebar"] a, [data-testid="stSidebarNavLink"]{
  position:relative; border-radius:10px;
  transition:transform .25s var(--mg-ease),background .25s,color .25s;
}
[data-testid="stSidebar"] a:hover, [data-testid="stSidebarNavLink"]:hover{
  transform:translateX(7px); background:rgba(99,91,255,.12);
}
[data-testid="stSidebarNavLink"][aria-current="page"]{
  box-shadow:inset 4px 0 0 var(--mg-p);
}
/* "Model ready" badge: heartbeat glow */
[data-testid="stSidebar"] [data-testid="stAlert"]{
  border-radius:14px; animation:mgUp .7s .3s var(--mg-ease) both, mgRing 2.2s 1s ease-out infinite;
}

/* ---------- Divider draws itself ---------- */
hr{border:none!important; height:2px!important; background:linear-gradient(90deg,var(--mg-p),var(--mg-sky),transparent)!important;
   transform-origin:left; animation:mgGrowX 1s var(--mg-ease) both}

/* ---------- Alerts / charts / tables / expanders ---------- */
[data-testid="stAlert"]{border-radius:14px; animation:mgUp .5s var(--mg-ease) both}
[data-testid="stPlotlyChart"], [data-testid="stDataFrame"]{animation:mgUp .8s .1s var(--mg-ease) both}
[data-testid="stExpander"]{border-radius:14px; transition:box-shadow .3s,transform .3s var(--mg-ease)}
[data-testid="stExpander"]:hover{box-shadow:0 10px 24px rgba(99,91,255,.12); transform:translateY(-2px)}
[data-testid="stMetric"]{transition:transform .3s var(--mg-ease)}
[data-testid="stMetric"]:hover{transform:translateY(-3px)}

/* ---------- Scanning spinner (use with st.spinner) ---------- */
[data-testid="stSpinner"]{
  position:relative; overflow:hidden; padding:20px 22px; border-radius:14px;
  background:linear-gradient(135deg,rgba(99,91,255,.10),rgba(56,189,248,.10));
  border:1px solid rgba(99,91,255,.25);
  animation:mgBlink 1.4s ease-in-out infinite;
}
[data-testid="stSpinner"]::after{
  content:""; position:absolute; left:0; right:0; height:3px; top:0;
  background:linear-gradient(90deg,transparent,var(--mg-p),var(--mg-sky),transparent);
  box-shadow:0 0 14px var(--mg-p);
  animation:mgScan 1.1s ease-in-out infinite;
}

/* ---------- Accessibility ---------- */
:focus-visible{outline:3px solid rgba(99,91,255,.55); outline-offset:3px}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important; transition:none!important}
  .stApp h1{-webkit-text-fill-color:#1B1F4B; color:#1B1F4B}
}
</style>
"""


def inject_motion() -> None:
    st.markdown(MOTION_CSS, unsafe_allow_html=True)