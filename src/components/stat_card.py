import streamlit as st
from src.ui.base_layout import theme_colors


def stat_row(stats):
    """Renders a row of KPI-style stat cards, enterprise-dashboard style.
    `stats` is a list of (icon, label, value, subtext) tuples. subtext is optional."""
    t = theme_colors()
    cols = st.columns(len(stats))

    for col, stat in zip(cols, stats):
        icon, label, value, *rest = stat
        subtext = rest[0] if rest else None

        html = f"""
<div style="background:{t['surface']}; border:1px solid {t['border']}; border-radius:16px; padding:18px 20px; box-shadow:{t['card_shadow']};">
<div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
<span style="font-size:1.3rem;">{icon}</span>
<span style="color:{t['text_secondary']}; font-size:0.8rem; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">{label}</span>
</div>
<div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:1.9rem; color:{t['text']}; line-height:1;">{value}</div>
"""
        if subtext:
            html += f'<div style="color:{t["text_secondary"]}; font-size:0.78rem; margin-top:4px;">{subtext}</div>'
        html += "</div>"

        with col:
            st.markdown(html, unsafe_allow_html=True)
