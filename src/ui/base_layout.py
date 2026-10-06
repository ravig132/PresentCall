import streamlit as st

# ============================================================
# PRESENT CALL ENTERPRISE DESIGN SYSTEM
# Brand: Present Call (Deep Navy Brand Identity)
# Product: Light Operational Dashboard (#F7F9FC)
# ============================================================

THEMES = {
    'light': {
        'bg':             '#F7F9FC',
        'surface':        '#FFFFFF',
        'sidebar_bg':     '#0B132B',
        'text':           '#0F172A',
        'text_secondary': '#64748B',
        'text_muted':     '#94A3B8',
        'accent':         '#2563EB',       # Present Call Blue
        'accent_hover':   '#1D4ED8',
        'accent_soft':    '#EFF6FF',
        'success':        '#10B981',       # Present
        'success_soft':   '#ECFDF5',
        'warning':        '#F59E0B',       # Late / Alert
        'warning_soft':   '#FFFBEB',
        'danger':         '#EF4444',        # Absent
        'danger_soft':    '#FEF2F2',
        'border':         '#E2E8F0',
        'card_shadow':    '0 1px 3px rgba(15, 23, 42, 0.05), 0 1px 2px rgba(15, 23, 42, 0.03)',
    },
    'dark': {
        'bg':             '#0B132B',
        'surface':        '#111C38',
        'sidebar_bg':     '#070D1E',
        'text':           '#F8FAFC',
        'text_secondary': '#94A3B8',
        'text_muted':     '#64748B',
        'accent':         '#38BDF8',
        'accent_hover':   '#0284C7',
        'accent_soft':    '#0C3A52',
        'success':        '#34D399',
        'success_soft':   '#064E3B',
        'warning':        '#FBBF24',
        'warning_soft':   '#78350F',
        'danger':         '#F87171',
        'danger_soft':    '#7F1D1D',
        'border':         '#1E293B',
        'card_shadow':    '0 4px 20px rgba(0,0,0,0.4)',
    }
}


def get_theme():
    # As instructed: The Streamlit dashboard is the light operational product (#F7F9FC)
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    return st.session_state.theme


def theme_colors():
    return THEMES[get_theme()]


def toggle_theme():
    st.session_state.theme = 'dark' if get_theme() == 'light' else 'light'


def theme_toggle_button(key='theme_toggle'):
    theme = get_theme()
    icon = ':material/dark_mode:' if theme == 'light' else ':material/light_mode:'
    if st.button('', icon=icon, key=key, type='tertiary', width='stretch'):
        toggle_theme()
        st.rerun()


def style_background_home():
    style_base_layout()


def style_background_dashboard():
    style_base_layout()


def style_base_layout():
    t = theme_colors()
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

        /* Hide Streamlit default chrome */
        #MainMenu, footer, header {{ visibility: hidden; height: 0; }}
        header[data-testid="stHeader"] {{ display: none !important; }}

        /* Root & typography */
        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: {t['text']};
            background-color: {t['bg']} !important;
            overflow-x: hidden !important;
        }}

        .stApp {{
            background-color: {t['bg']} !important;
        }}

        [data-testid="stAppViewContainer"] {{
            background-color: {t['bg']} !important;
            overflow-x: hidden !important;
        }}

        .block-container {{
            padding-top: 0.8rem !important;
            padding-bottom: 3.5rem !important;
            max-width: 1320px !important;
            overflow-x: hidden !important;
        }}

        /* Headings */
        h1 {{
            font-family: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 700 !important;
            font-size: 2.1rem !important;
            line-height: 1.2 !important;
            color: {t['text']} !important;
            letter-spacing: -0.02em;
            margin-bottom: 0.2rem !important;
        }}
        h2 {{
            font-family: 'Space Grotesk', 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.45rem !important;
            line-height: 1.25 !important;
            color: {t['text']} !important;
            letter-spacing: -0.01em;
            margin-bottom: 0.2rem !important;
        }}
        h3 {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.15rem !important;
            color: {t['text']} !important;
            margin-bottom: 0.2rem !important;
        }}
        h4, h5, h6 {{
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 600 !important;
            color: {t['text']} !important;
        }}
        p, span, label {{
            color: {t['text_secondary']};
        }}

        /* ============================================================
           SIDEBAR STYLING — Deep Navy Brand Sidebar (#0B132B)
           ============================================================ */
        section[data-testid="stSidebar"] {{
            background-color: {t['sidebar_bg']} !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            box-shadow: 2px 0 12px rgba(0, 0, 0, 0.15) !important;
            overflow-x: hidden !important;
        }}

        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {{
            padding: 1.4rem 1rem !important;
        }}

        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label {{
            color: {t['text_muted']} !important;
        }}

        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: #FFFFFF !important;
        }}

        section[data-testid="stSidebar"] hr {{
            border-color: rgba(255, 255, 255, 0.08) !important;
            margin: 14px 0 !important;
        }}

        /* Sidebar buttons */
        section[data-testid="stSidebar"] button {{
            width: 100% !important;
            text-align: left !important;
            justify-content: flex-start !important;
            padding: 10px 14px !important;
            margin: 3px 0 !important;
            border-radius: 9px !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.15s ease !important;
            box-shadow: none !important;
            display: flex !important;
            align-items: center !important;
            gap: 10px !important;
        }}

        /* Inactive sidebar buttons */
        section[data-testid="stSidebar"] button[kind="tertiary"],
        section[data-testid="stSidebar"] button[kind="secondary"] {{
            background-color: transparent !important;
            color: #CBD5E1 !important;
            border: 1px solid transparent !important;
        }}

        section[data-testid="stSidebar"] button[kind="tertiary"]:hover,
        section[data-testid="stSidebar"] button[kind="secondary"]:hover {{
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #FFFFFF !important;
            border-color: rgba(255, 255, 255, 0.12) !important;
            transform: translateX(2px) !important;
        }}

        /* Active sidebar buttons (Strong Present Call Blue) */
        section[data-testid="stSidebar"] button[kind="primary"] {{
            background-color: {t['accent']} !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 2px 10px rgba(37, 99, 235, 0.45) !important;
        }}

        section[data-testid="stSidebar"] button[kind="primary"]:hover {{
            background-color: {t['accent_hover']} !important;
            transform: translateX(2px) !important;
        }}

        /* ============================================================
           WORKSPACE BUTTONS — Enterprise SaaS Style
           ============================================================ */
        button {{
            border-radius: 9px !important;
            padding: 9px 18px !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1) !important;
            outline: none !important;
            box-shadow: none !important;
        }}

        button[kind="primary"] {{
            background-color: {t['accent']} !important;
            color: #FFFFFF !important;
            border: 1px solid {t['accent']} !important;
            box-shadow: 0 1px 2px rgba(37, 99, 235, 0.2) !important;
        }}

        button[kind="primary"]:hover {{
            background-color: {t['accent_hover']} !important;
            border-color: {t['accent_hover']} !important;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25) !important;
            transform: translateY(-1px) !important;
        }}

        button[kind="secondary"] {{
            background-color: {t['surface']} !important;
            color: {t['text']} !important;
            border: 1px solid {t['border']} !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        }}

        button[kind="secondary"]:hover {{
            background-color: {t['accent_soft']} !important;
            color: {t['accent']} !important;
            border-color: {t['accent']} !important;
            transform: translateY(-1px) !important;
        }}

        button[kind="tertiary"] {{
            background-color: {t['surface']} !important;
            color: {t['text']} !important;
            border: 1px solid {t['border']} !important;
        }}

        button[kind="tertiary"]:hover {{
            background-color: {t['bg']} !important;
            border-color: #CBD5E1 !important;
            color: {t['text']} !important;
        }}

        button:active {{
            transform: translateY(0px) !important;
            filter: brightness(0.96) !important;
        }}

        /* Link buttons */
        [data-testid="stLinkButton"] > a {{
            border-radius: 9px !important;
            font-weight: 600 !important;
            padding: 9px 18px !important;
            font-family: 'Inter', sans-serif !important;
            border: 1px solid {t['border']} !important;
            background-color: {t['surface']} !important;
            color: {t['text']} !important;
            text-decoration: none !important;
            transition: all 0.15s ease !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
        }}

        [data-testid="stLinkButton"] > a:hover {{
            background-color: {t['accent_soft']} !important;
            color: {t['accent']} !important;
            border-color: {t['accent']} !important;
        }}

        /* ============================================================
           INPUTS, SELECTS, AND FORMS
           ============================================================ */
        div[data-baseweb="input"],
        div[data-baseweb="base-input"] {{
            background-color: {t['surface']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 9px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03) !important;
            transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        }}

        div[data-baseweb="input"]:focus-within,
        div[data-baseweb="base-input"]:focus-within {{
            border-color: {t['accent']} !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
        }}

        div[data-baseweb="input"] input {{
            color: {t['text']} !important;
            font-family: 'Inter', sans-serif !important;
            font-size: 0.92rem !important;
        }}

        div[data-baseweb="select"] > div {{
            background-color: {t['surface']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 9px !important;
            color: {t['text']} !important;
        }}

        div[data-baseweb="select"] > div:focus-within {{
            border-color: {t['accent']} !important;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12) !important;
        }}

        /* ============================================================
           CARDS & METRICS
           ============================================================ */
        div[data-testid="stMetric"] {{
            background-color: {t['surface']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 14px !important;
            padding: 18px 22px !important;
            box-shadow: {t['card_shadow']} !important;
        }}

        div[data-testid="stMetricLabel"] p {{
            font-size: 0.8rem !important;
            color: {t['text_secondary']} !important;
            text-transform: uppercase !important;
            font-weight: 600 !important;
            letter-spacing: 0.05em !important;
        }}

        div[data-testid="stMetricValue"] {{
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important;
            font-size: 2.1rem !important;
            color: {t['text']} !important;
        }}

        /* Dataframe styling */
        [data-testid="stDataFrame"] {{
            border-radius: 12px !important;
            overflow: hidden !important;
            border: 1px solid {t['border']} !important;
            background: {t['surface']} !important;
            box-shadow: {t['card_shadow']} !important;
        }}

        /* Camera input styling — clean white card container */
        [data-testid="stCameraInput"] {{
            max-width: 540px !important;
            margin: 0 auto !important;
            background: {t['surface']} !important;
            border: 1px solid {t['border']} !important;
            border-radius: 14px !important;
            padding: 16px !important;
            box-shadow: {t['card_shadow']} !important;
        }}

        [data-testid="stCameraInput"] video,
        [data-testid="stCameraInput"] img {{
            max-height: 380px !important;
            width: 100% !important;
            object-fit: cover !important;
            border-radius: 10px !important;
            border: 1px solid {t['border']} !important;
        }}

        /* Dialogs */
        div[data-testid="stDialog"] div[role="dialog"] {{
            background-color: {t['surface']} !important;
            border-radius: 16px !important;
            border: 1px solid {t['border']} !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.18) !important;
            padding: 24px !important;
        }}

        /* Progress bars */
        div[data-testid="stProgressBar"] > div {{
            background-color: #E2E8F0 !important;
            border-radius: 6px !important;
            height: 8px !important;
        }}
        div[data-testid="stProgressBar"] > div > div {{
            background-color: {t['accent']} !important;
            border-radius: 6px !important;
        }}

        /* Alerts */
        div[data-testid="stAlert"] {{
            border-radius: 10px !important;
            border: 1px solid {t['border']} !important;
            padding: 12px 16px !important;
            font-size: 0.9rem !important;
        }}

        hr {{
            border-color: {t['border']} !important;
            margin: 1.5rem 0 !important;
        }}

        /* Prevent horizontal overflow page-wide */
        .main, .stApp, [data-testid="stAppViewContainer"], .block-container {{
            max-width: 100vw;
            box-sizing: border-box;
        }}

        /* Hero cards on home chooser */
        .st-key-hero_cards div[data-testid="stColumn"] {{
            background-color: {t['surface']} !important;
            padding: 2.2rem !important;
            border-radius: 16px !important;
            border: 1px solid {t['border']} !important;
            box-shadow: {t['card_shadow']} !important;
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease !important;
        }}

        .st-key-hero_cards div[data-testid="stColumn"]:hover {{
            transform: translateY(-3px) !important;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08) !important;
            border-color: {t['accent']} !important;
        }}

        /* Back to top floating button */
        #pc-back-to-top {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: {t['accent']};
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
            cursor: pointer;
            z-index: 999999;
            opacity: 0;
            visibility: hidden;
            transform: translateY(10px);
            transition: opacity 0.2s ease, transform 0.2s ease, background-color 0.15s ease;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        #pc-back-to-top.visible {{
            opacity: 1;
            visibility: visible;
            transform: translateY(0);
        }}
        #pc-back-to-top:hover {{
            background: {t['accent_hover']};
            transform: translateY(-2px);
        }}
        @media (prefers-reduced-motion: reduce) {{
            #pc-back-to-top {{ transition: none !important; }}
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.7rem !important; }}
            h2 {{ font-size: 1.3rem !important; }}
            .block-container {{ padding-left: 0.8rem !important; padding-right: 0.8rem !important; }}
            .st-key-hero_cards div[data-testid="stColumn"] {{ padding: 1.4rem !important; }}
        }}
        </style>

        <!-- Back to Top Button HTML & Script -->
        <div id="pc-back-to-top" title="Back to top" aria-label="Back to top" onclick="
            (function() {{
                try {{
                    const el = window.parent.document.querySelector('.main') || window.parent.document.querySelector('[data-testid=stAppViewContainer]') || window;
                    if (el && el.scrollTo) el.scrollTo({{ top: 0, behavior: 'smooth' }});
                }} catch(e) {{}}
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }})();
        ">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M18 15l-6-6-6 6"/>
            </svg>
        </div>

        <script>
        (function() {{
            function setupScroll() {{
                const btn = document.getElementById('pc-back-to-top');
                if (!btn) return;
                function check() {{
                    let scrollY = 0;
                    try {{
                        const doc = window.parent.document;
                        const main = doc.querySelector('.main') || doc.querySelector('[data-testid=stAppViewContainer]');
                        scrollY = main ? main.scrollTop : (window.parent.pageYOffset || 0);
                    }} catch(e) {{
                        scrollY = window.pageYOffset || 0;
                    }}
                    if (scrollY > 220) {{
                        btn.classList.add('visible');
                    }} else {{
                        btn.classList.remove('visible');
                    }}
                }}
                try {{
                    const doc = window.parent.document;
                    const main = doc.querySelector('.main') || doc.querySelector('[data-testid=stAppViewContainer]');
                    if (main) main.addEventListener('scroll', check, {{ passive: true }});
                    window.parent.addEventListener('scroll', check, {{ passive: true }});
                }} catch(e) {{}}
                window.addEventListener('scroll', check, {{ passive: true }});
            }}
            setTimeout(setupScroll, 600);
        }})();
        </script>
    """, unsafe_allow_html=True)
