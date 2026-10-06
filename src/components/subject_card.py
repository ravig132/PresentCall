import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    """
    Renders an enterprise-grade subject/course card.
    White card, subtle border, blue accent, badges, and stats.
    """
    stats_html = ""
    if stats:
        stats_html += '<div style="display:flex; gap:8px; flex-wrap:wrap; margin-top:14px;">'
        for icon, label, value in stats:
            stats_html += f"""
            <div style="
                background: #F8FAFC;
                border: 1px solid #E2E8F0;
                color: #334155;
                padding: 4px 10px;
                border-radius: 8px;
                font-size: 0.82rem;
                display: flex;
                align-items: center;
                gap: 5px;
            ">
                <span>{icon}</span>
                <span style="font-weight:700; color:#0F172A;">{value}</span>
                <span style="color:#64748B;">{label}</span>
            </div>
            """
        stats_html += '</div>'

    html = f"""
    <div style="
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #2563EB;
        padding: 20px 22px;
        border-radius: 14px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
    ">
        <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:12px;">
            <div>
                <h3 style="margin:0 0 6px 0; color:#0F172A; font-size:1.18rem; font-weight:700; font-family:'Plus Jakarta Sans', sans-serif;">{name}</h3>
                <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
                    <span style="background:#EFF6FF; color:#2563EB; border:1px solid #DBEAFE; padding:2px 8px; border-radius:6px; font-weight:600; font-size:0.78rem; font-family:monospace;">
                        {code}
                    </span>
                    <span style="color:#94A3B8; font-size:0.8rem;">·</span>
                    <span style="color:#64748B; font-size:0.82rem; font-weight:500;">
                        Section {section}
                    </span>
                </div>
            </div>
            <div style="background:#ECFDF5; color:#059669; border:1px solid #A7F3D0; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:6px;">
                ACTIVE
            </div>
        </div>
        {stats_html}
    </div>
    """

    st.markdown(html, unsafe_allow_html=True)

    if footer_callback:
        footer_callback()
