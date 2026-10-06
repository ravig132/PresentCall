import streamlit as st
from datetime import datetime

def render_system_bar():
    """
    Renders the subtle production system bar:
    🔒 app.presentcall.ai — Production Attendance Hub        ● Engine Online
    """
    st.markdown("""
    <div style="
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 8px 16px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
        font-family: 'Inter', -apple-system, sans-serif;
    ">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="font-size:0.85rem;">🔒</span>
            <span style="font-family:monospace; font-size:0.82rem; font-weight:600; color:#0F172A;">app.presentcall.ai</span>
            <span style="color:#CBD5E1; font-size:0.8rem;">—</span>
            <span style="font-size:0.8rem; color:#64748B; font-weight:500;">Production Attendance Hub</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="
                display:inline-block;
                width:7px;
                height:7px;
                border-radius:50%;
                background:#10B981;
                box-shadow:0 0 6px rgba(16,185,129,0.7);
            "></span>
            <span style="font-size:0.78rem; font-weight:600; color:#059669;">Engine Online</span>
            <span style="
                background: #EFF6FF;
                color: #2563EB;
                border: 1px solid #DBEAFE;
                font-size: 0.7rem;
                font-weight: 600;
                padding: 1px 7px;
                border-radius: 6px;
            ">v2.4 Enterprise</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_page_header(title, subtitle=None, breadcrumb="Executive Overview", badge=None):
    """
    Renders the clean enterprise page title & breadcrumbs area.
    """
    today_str = datetime.now().strftime("%A, %b %d, %Y")
    badge_html = f'<div style="background:#EFF6FF; color:#2563EB; border:1px solid #BFDBFE; font-size:0.78rem; font-weight:600; padding:4px 10px; border-radius:8px;">{badge}</div>' if badge else ""
    subtitle_html = f'<p style="color:#64748B; font-size:0.92rem; margin:2px 0 0 0; font-weight:400;">{subtitle}</p>' if subtitle else ""

    st.markdown(f"""
    <div style="
        display:flex;
        align-items:flex-start;
        justify-content:space-between;
        margin-bottom:20px;
        padding-bottom:14px;
        border-bottom:1px solid #E2E8F0;
    ">
        <div>
            <div style="font-size:0.8rem; font-weight:600; color:#64748B; margin-bottom:4px; display:flex; align-items:center; gap:6px;">
                <span>Present Call</span>
                <span style="color:#CBD5E1;">/</span>
                <span style="color:#2563EB; font-weight:600;">{breadcrumb}</span>
            </div>
            <h1 style="margin:0 !important; font-size:1.9rem !important; color:#0F172A !important; line-height:1.2 !important;">{title}</h1>
            {subtitle_html}
        </div>
        <div style="display:flex; align-items:center; gap:10px; padding-top:4px;">
            <div style="
                display:flex;
                align-items:center;
                gap:6px;
                background:#FFFFFF;
                border:1px solid #E2E8F0;
                border-radius:8px;
                padding:6px 12px;
                font-size:0.82rem;
                color:#475569;
                font-weight:500;
                box-shadow: 0 1px 2px rgba(0,0,0,0.02);
            ">
                <span>📅</span>
                <span>{today_str}</span>
            </div>
            {badge_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
