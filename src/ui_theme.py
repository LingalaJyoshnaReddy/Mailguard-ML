"""MailGuard ML - Colorful light theme with motion."""

import streamlit as st


def inject_mailguard_styles():
    """Apply colorful MailGuard styling and animations (presentation only)."""

    st.markdown(
        """
        <style>
        /* ===== COLOR SYSTEM ===== */

        :root {
            --mg-primary: #635BFF;
            --mg-primary-dark: #4F46E5;
            --mg-purple: #9333EA;
            --mg-teal: #0D9488;
            --mg-coral: #F97360;
            --mg-amber: #E9A23B;
            --mg-pink: #DB2777;
            --mg-sky: #38BDF8;
            --mg-bg: #F5F6FF;
            --mg-card: #FFFFFF;
            --mg-heading: #252653;
            --mg-muted: #72749A;
            --mg-border: #E6E7F2;
            --mg-ease: cubic-bezier(.22, .8, .3, 1);
        }

        /* ===== KEYFRAMES ===== */

        @keyframes mgUp     { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: none; } }
        @keyframes mgFlow   { 0% { background-position: 0% 50%; } 100% { background-position: 200% 50%; } }
        @keyframes mgShine  { 0% { transform: translateX(-120%) skewX(-20deg); } 55%, 100% { transform: translateX(320%) skewX(-20deg); } }
        @keyframes mgRing   { 0% { box-shadow: 0 0 0 0 rgba(13, 148, 136, .40); } 100% { box-shadow: 0 0 0 14px rgba(13, 148, 136, 0); } }
        @keyframes mgGrowX  { from { transform: scaleX(0); } to { transform: scaleX(1); } }
        @keyframes mgScan   { 0% { top: 0; opacity: 0; } 15% { opacity: 1; } 85% { opacity: 1; } 100% { top: calc(100% - 3px); opacity: 0; } }
        @keyframes mgBlink  { 0%, 100% { opacity: 1; } 50% { opacity: .45; } }

        /* ===== MAIN BACKGROUND ===== */

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(800px 380px at 92% -8%, rgba(99, 91, 255, .13), transparent 60%),
                radial-gradient(700px 320px at -4% 4%, rgba(56, 189, 248, .11), transparent 60%),
                var(--mg-bg);
            color: var(--mg-heading);
        }

        [data-testid="stMain"] {
            background: transparent;
            color: var(--mg-heading);
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1450px;
            padding: 2rem 2.5rem 3rem;
        }

        [data-testid="stHeader"] {
            background: transparent;
        }

        /* ===== STAGGERED PAGE ENTRANCE (top-level blocks only) ===== */

        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > div {
            animation: mgUp .7s var(--mg-ease) both;
        }
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > div:nth-child(1) { animation-delay: .00s; }
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > div:nth-child(2) { animation-delay: .07s; }
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > div:nth-child(3) { animation-delay: .14s; }
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > div:nth-child(4) { animation-delay: .21s; }
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > div:nth-child(5) { animation-delay: .28s; }
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > div:nth-child(6) { animation-delay: .35s; }
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] > div:nth-child(n+7) { animation-delay: .42s; }

        /* ===== SIDEBAR ===== */

        [data-testid="stSidebar"] {
            background: rgba(255, 255, 255, .85);
            backdrop-filter: blur(12px);
            border-right: 1px solid var(--mg-border);
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label {
            color: #45516E;
        }

        [data-testid="stSidebar"] a,
        [data-testid="stSidebarNavLink"] {
            border-radius: 10px;
            transition: transform .25s var(--mg-ease), background .25s, color .25s;
        }

        [data-testid="stSidebar"] a:hover,
        [data-testid="stSidebarNavLink"]:hover {
            transform: translateX(7px);
            background: rgba(99, 91, 255, .12);
        }

        [data-testid="stSidebar"] [aria-current="page"] {
            background: #EEEDFF;
            border-radius: 9px;
            box-shadow: inset 4px 0 0 var(--mg-primary);
        }

        [data-testid="stSidebar"] [aria-current="page"] p {
            color: var(--mg-primary-dark);
            font-weight: 750;
        }

        /* "Model ready" badge: heartbeat glow */
        [data-testid="stSidebar"] [data-testid="stAlert"] {
            animation: mgUp .7s .3s var(--mg-ease) both, mgRing 2.2s 1s ease-out infinite;
        }

        /* ===== TYPOGRAPHY ===== */

        h1, h2, h3 {
            color: var(--mg-heading) !important;
            font-weight: 750 !important;
            letter-spacing: -0.035em;
        }

        /* Hero title: flowing gradient text */
        .stApp h1 {
            background: linear-gradient(90deg, #252653, #635BFF, #38BDF8, #635BFF, #252653);
            background-size: 200% auto;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: mgFlow 7s linear infinite;
        }

        [data-testid="stCaptionContainer"] p {
            color: var(--mg-muted);
            line-height: 1.6;
        }

        /* ===== METRIC CARDS ===== */

        [data-testid="stMetric"] {
            background: #FFFFFF;
            border: 1px solid var(--mg-border);
            border-radius: 16px;
            padding: 18px;
            box-shadow: 0 4px 15px rgba(75, 70, 160, 0.06);
            transition: transform .3s var(--mg-ease), box-shadow .3s var(--mg-ease);
        }

        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 12px 26px rgba(75, 70, 160, 0.14);
        }

        [data-testid="stMetricLabel"] {
            color: var(--mg-muted) !important;
            font-weight: 650;
        }

        [data-testid="stMetricValue"] {
            color: var(--mg-heading) !important;
            font-weight: 800;
        }

        /* ===== CONTAINERS: lift + sweeping accent line ===== */

        [data-testid="stVerticalBlockBorderWrapper"] {
            position: relative;
            overflow: hidden;
            background: #FFFFFF;
            border: 1px solid var(--mg-border);
            border-radius: 18px;
            box-shadow: 0 4px 16px rgba(75, 70, 160, 0.045);
            transition: transform .35s var(--mg-ease), box-shadow .35s var(--mg-ease), border-color .3s;
        }

        [data-testid="stVerticalBlockBorderWrapper"]::before {
            content: "";
            position: absolute;
            left: 0; right: 0; top: 0;
            height: 3px;
            background: linear-gradient(90deg, #635BFF, #38BDF8, #9333EA, #635BFF);
            background-size: 200% 100%;
            transform: scaleX(0);
            transform-origin: left;
            transition: transform .5s var(--mg-ease);
            animation: mgFlow 4s linear infinite;
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-5px);
            box-shadow: 0 4px 8px rgba(75, 70, 160, .06), 0 24px 48px rgba(99, 91, 255, .18);
            border-color: rgba(99, 91, 255, .38);
        }

        [data-testid="stVerticalBlockBorderWrapper"]:hover::before {
            transform: scaleX(1);
        }

        /* ===== INPUTS ===== */

        [data-testid="stTextArea"] textarea,
        [data-testid="stTextInput"] input {
            background: #FFFFFF;
            color: var(--mg-heading);
            border: 1px solid #D9DAEA;
            border-radius: 11px;
            transition: box-shadow .3s var(--mg-ease), border-color .25s, transform .25s var(--mg-ease);
        }

        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stTextInput"] input:focus {
            border-color: var(--mg-primary);
            box-shadow: 0 0 0 4px rgba(99, 91, 255, .18), 0 10px 24px rgba(99, 91, 255, .12);
            transform: translateY(-1px);
        }

        /* ===== FILE UPLOADER ===== */

        [data-testid="stFileUploader"] section {
            background: #F8F7FF;
            border: 1px dashed #A9A3FF;
            border-radius: 13px;
            transition: background .3s, border-color .3s, transform .3s var(--mg-ease);
        }

        [data-testid="stFileUploader"] section:hover {
            background: rgba(99, 91, 255, .08);
            border-color: var(--mg-primary);
            transform: scale(1.01);
        }

        /* ===== BUTTONS ===== */

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 11px;
            font-weight: 700;
            min-height: 42px;
            transition: transform .2s var(--mg-ease), box-shadow .25s, border-color .2s, color .2s;
        }

        .stButton > button:not([kind="primary"]):hover,
        .stDownloadButton > button:hover {
            transform: translateY(-2px);
            border-color: var(--mg-primary);
            color: var(--mg-primary);
            box-shadow: 0 8px 18px rgba(99, 91, 255, .18);
        }

        .stButton > button[kind="primary"] {
            position: relative;
            overflow: hidden;
            background: linear-gradient(120deg, #635BFF, #9333EA, #38BDF8, #635BFF);
            background-size: 250% 100%;
            color: #FFFFFF;
            border: none;
            box-shadow: 0 4px 12px rgba(99, 91, 255, 0.25);
            animation: mgFlow 6s linear infinite;
        }

        /* sweeping shine */
        .stButton > button[kind="primary"]::after {
            content: "";
            position: absolute;
            top: 0; bottom: 0; left: 0;
            width: 35%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, .55), transparent);
            animation: mgShine 3.2s ease-in-out infinite;
            pointer-events: none;
        }

        .stButton > button[kind="primary"]:hover {
            transform: translateY(-3px) scale(1.015);
            box-shadow: 0 14px 30px rgba(99, 91, 255, .45);
        }

        .stButton > button[kind="primary"]:active {
            transform: scale(.97);
        }

        /* ===== TABS ===== */

        [data-testid="stTabs"] button {
            font-weight: 650;
            border-radius: 10px 10px 0 0;
            transition: color .25s, background .25s, transform .25s var(--mg-ease);
        }

        [data-testid="stTabs"] button:hover {
            background: rgba(99, 91, 255, .09);
            transform: translateY(-2px);
        }

        [data-testid="stTabs"] button[aria-selected="true"] {
            color: var(--mg-primary);
            border-bottom-color: var(--mg-primary);
        }

        [data-testid="stTabs"] [data-baseweb="tab-highlight"] {
            background: linear-gradient(90deg, #635BFF, #38BDF8) !important;
            height: 3px !important;
            transition: left .45s var(--mg-ease), width .45s var(--mg-ease);
        }

        [data-testid="stTabs"] [role="tabpanel"] {
            animation: mgUp .5s var(--mg-ease) both;
        }

        /* ===== SLIDERS ===== */

        [data-testid="stSlider"] [role="slider"] {
            background: var(--mg-primary);
            transition: transform .2s var(--mg-ease), box-shadow .25s;
        }

        [data-testid="stSlider"] [role="slider"]:hover,
        [data-testid="stSlider"] [role="slider"]:active {
            transform: scale(1.35);
            box-shadow: 0 0 0 10px rgba(99, 91, 255, .16);
        }

        /* ===== ALERTS ===== */

        [data-testid="stAlert"] {
            border-radius: 13px;
            animation: mgUp .5s var(--mg-ease) both;
        }

        /* ===== TABLES / CHARTS / EXPANDERS ===== */

        [data-testid="stDataFrame"] {
            border: 1px solid var(--mg-border);
            border-radius: 12px;
            overflow: hidden;
            animation: mgUp .7s .1s var(--mg-ease) both;
        }

        [data-testid="stPlotlyChart"] {
            animation: mgUp .8s .1s var(--mg-ease) both;
        }

        [data-testid="stExpander"] {
            border-radius: 14px;
            transition: box-shadow .3s, transform .3s var(--mg-ease);
        }

        [data-testid="stExpander"]:hover {
            box-shadow: 0 10px 24px rgba(99, 91, 255, .12);
            transform: translateY(-2px);
        }

        /* ===== DIVIDER DRAWS ITSELF ===== */

        hr {
            border: none !important;
            height: 2px !important;
            background: linear-gradient(90deg, #635BFF, #38BDF8, transparent) !important;
            transform-origin: left;
            animation: mgGrowX 1s var(--mg-ease) both;
        }

        /* ===== SCANNING SPINNER (st.spinner) ===== */

        [data-testid="stSpinner"] {
            position: relative;
            overflow: hidden;
            padding: 20px 22px;
            border-radius: 14px;
            background: linear-gradient(135deg, rgba(99, 91, 255, .10), rgba(56, 189, 248, .10));
            border: 1px solid rgba(99, 91, 255, .25);
            animation: mgBlink 1.4s ease-in-out infinite;
        }

        [data-testid="stSpinner"]::after {
            content: "";
            position: absolute;
            left: 0; right: 0; top: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, #635BFF, #38BDF8, transparent);
            box-shadow: 0 0 14px #635BFF;
            animation: mgScan 1.1s ease-in-out infinite;
        }
        /* ===== PLOTLY CHART MOTION ===== */

        @keyframes mgBarX   { from { transform: scaleX(0); opacity: .25; } to { transform: scaleX(1); opacity: 1; } }
        @keyframes mgDraw   { from { stroke-dasharray: 4000; stroke-dashoffset: 4000; } to { stroke-dasharray: 4000; stroke-dashoffset: 0; } }
        @keyframes mgFadeIn { from { opacity: 0; } to { opacity: 1; } }

        /* bars grow in one after another */
        [data-testid="stPlotlyChart"] .barlayer .point path {
            transform-box: fill-box;
            transform-origin: left center;
            animation: mgBarX .9s var(--mg-ease) both;
        }
        [data-testid="stPlotlyChart"] .barlayer .point:nth-child(2) path { animation-delay: .08s; }
        [data-testid="stPlotlyChart"] .barlayer .point:nth-child(3) path { animation-delay: .16s; }
        [data-testid="stPlotlyChart"] .barlayer .point:nth-child(4) path { animation-delay: .24s; }
        [data-testid="stPlotlyChart"] .barlayer .point:nth-child(5) path { animation-delay: .32s; }
        [data-testid="stPlotlyChart"] .barlayer .point:nth-child(6) path { animation-delay: .40s; }
        [data-testid="stPlotlyChart"] .barlayer .point:nth-child(7) path { animation-delay: .48s; }
        [data-testid="stPlotlyChart"] .barlayer .point:nth-child(n+8) path { animation-delay: .56s; }

        /* lines draw themselves (dotted reference lines are left alone) */
        [data-testid="stPlotlyChart"] .scatterlayer .trace .lines path:not([style*="stroke-dasharray"]) {
            animation: mgDraw 1.6s var(--mg-ease) both;
        }

        /* markers and heatmap fade in */
        [data-testid="stPlotlyChart"] .scatterlayer .trace .points path { animation: mgFadeIn .6s .9s both; }
        [data-testid="stPlotlyChart"] .heatmaplayer { animation: mgFadeIn .9s both; }
        /* ===== ACCESSIBILITY ===== */

        :focus-visible {
            outline: 3px solid rgba(99, 91, 255, .55);
            outline-offset: 3px;
        }

        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation: none !important;
                transition: none !important;
            }
            .stApp h1 {
                -webkit-text-fill-color: var(--mg-heading);
            }
        }

        /* ===== RESPONSIVE ===== */

        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem;
            }

            h1 {
                font-size: 1.9rem !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str):
    """Display a colorful page heading using native Streamlit components."""

    st.markdown(
        """
        <span style="
            color: #635BFF;
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 2px;">
            MAILGUARD ML · EMAIL SECURITY
        </span>
        """,
        unsafe_allow_html=True,
    )

    st.title(title)
    st.caption(subtitle)