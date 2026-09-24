import streamlit as st

THEMES = {
    'light': {
        'bg':             '#F3F4F6',
        'surface':        '#FFFFFF',
        'text':           '#0A0A0A',
        'text_secondary': '#6B7280',
        'accent':         '#0EA5E9',
        'accent_soft':    '#E0F2FE',
        'border':         '#E5E7EB',
        'card_shadow':    '0 4px 20px rgba(0,0,0,0.06)',
    },
    'dark': {
        'bg':             '#0A0A0B',
        'surface':        '#18181B',
        'text':           '#F5F5F5',
        'text_secondary': '#9CA3AF',
        'accent':         '#38BDF8',
        'accent_soft':    '#0C3A52',
        'border':         '#27272A',
        'card_shadow':    '0 4px 20px rgba(0,0,0,0.5)',
    }
}


def get_theme():
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
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
    t = theme_colors()
    st.markdown(f"""
        <style>
        .stApp {{ background: {t['bg']} !important; }}
        .stApp div[data-testid="stColumn"] {{
            background-color: {t['surface']} !important;
            padding: 2rem !important;
            border-radius: 1.6rem !important;
            border: 1px solid {t['border']} !important;
            box-shadow: {t['card_shadow']};
        }}
        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():
    t = theme_colors()
    st.markdown(f"""
        <style>
        .stApp {{ background: {t['bg']} !important; }}
        </style>
    """, unsafe_allow_html=True)


def style_base_layout():
    t = theme_colors()
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        #MainMenu, footer, header {{ visibility: hidden; }}
        .block-container {{ padding-top: 1.2rem !important; max-width: 1200px !important; }}

        html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; }}

        h1 {{
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 700 !important; font-size: 3rem !important;
            line-height: 1.1 !important; margin-bottom: 0rem !important;
            color: {t['text']} !important; letter-spacing: -0.02em;
        }}
        h2 {{
            font-family: 'Space Grotesk', sans-serif !important;
            font-weight: 600 !important; font-size: 1.8rem !important;
            line-height: 1.2 !important; margin-bottom: 0rem !important;
            color: {t['text']} !important;
        }}
        h3, h4 {{ font-family: 'Space Grotesk', sans-serif !important; color: {t['text']} !important; }}
        p, span, label {{ font-family: 'Inter', sans-serif; color: {t['text_secondary']}; }}

        /* ---------- Buttons: explicit states, no default Streamlit overlay ---------- */
        button {{
            border-radius: 0.85rem !important;
            background-color: {t['accent']} !important;
            color: #FFFFFF !important;
            padding: 9px 18px !important;
            border: none !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            box-shadow: none !important;
            outline: none !important;
            transition: filter 0.15s ease, transform 0.15s ease !important;
        }}
        button * {{ color: inherit !important; }}

        button[kind="secondary"] {{
            background-color: {t['text']} !important;
            color: {t['bg']} !important;
        }}
        button[kind="tertiary"] {{
            background-color: {t['surface']} !important;
            color: {t['text']} !important;
            border: 1.5px solid {t['border']} !important;
        }}

        button:hover, button:focus, button:focus-visible, button:active {{
            box-shadow: none !important;
            outline: none !important;
            background-image: none !important;
        }}
        button:hover {{ filter: brightness(1.12); transform: scale(1.02); }}
        button[kind="tertiary"]:hover {{
            background-color: {t['accent_soft']} !important;
            border-color: {t['accent']} !important;
            color: {t['accent']} !important;
        }}
        button:active {{ filter: brightness(0.92); transform: scale(0.99); }}

        /* Neutralize Streamlit's own hover/focus fill layered under our buttons */
        [data-testid^="stBaseButton"] {{ box-shadow: none !important; }}
        [data-testid^="stBaseButton"]:hover {{ box-shadow: none !important; background-image: none !important; }}

        [data-testid="stDataFrame"] {{ border-radius: 1rem !important; overflow: hidden; }}

        /* ---------- Responsive tweaks ---------- */
        @media (max-width: 640px) {{
            h1 {{ font-size: 2.1rem !important; }}
            h2 {{ font-size: 1.4rem !important; }}
            .block-container {{ padding-left: 1rem !important; padding-right: 1rem !important; }}
        }}
        </style>
    """, unsafe_allow_html=True)
