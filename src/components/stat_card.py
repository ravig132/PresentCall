import streamlit as st

def _get_card_accent(label, icon, idx):
    l = label.lower()
    if 'absent' in l:
        return '#EF4444', '#FEF2F2'       # Danger Red
    if 'present' in l or 'attended' in l or 'active' in l:
        return '#10B981', '#ECFDF5'       # Success Green
    if 'total' in l or 'student' in l or 'enrolled' in l:
        return '#2563EB', '#EFF6FF'       # Primary Blue
    if 'rate' in l or 'overall' in l:
        return '#0284C7', '#E0F2FE'       # Sky Blue
    if 'subject' in l or 'class' in l:
        return '#F59E0B', '#FFFBEB'       # Warning Orange
    
    # Palette fallback based on position index
    palette = [
        ('#2563EB', '#EFF6FF'),
        ('#10B981', '#ECFDF5'),
        ('#0284C7', '#E0F2FE'),
        ('#F59E0B', '#FFFBEB'),
    ]
    return palette[idx % len(palette)]


def stat_row(stats):
    """
    Renders a row of professional enterprise metric cards (Section 11, 12, 13, 14).
    `stats` is a list of (icon, label, value, subtext) tuples. subtext is optional.
    Cards have:
    - White background (#FFFFFF)
    - 1px subtle neutral border
    - Colored top accent line
    - Icon container
    - Large metric number (32-44px)
    - Supporting text & status
    """
    cols = st.columns(len(stats))

    for idx, (col, stat) in enumerate(zip(cols, stats)):
        icon, label, value, *rest = stat
        subtext = rest[0] if rest else None
        accent_color, accent_soft = _get_card_accent(label, icon, idx)

        subtext_html = ""
        if subtext:
            subtext_html = f'<div style="color:#64748B; font-size:0.78rem; margin-top:6px; font-weight:400;">{subtext}</div>'
        else:
            # Subtle default contextual note if none provided
            if 'subject' in label.lower():
                subtext_html = '<div style="color:#64748B; font-size:0.76rem; margin-top:6px;">Across active courses</div>'
            elif 'total student' in label.lower():
                subtext_html = '<div style="color:#64748B; font-size:0.76rem; margin-top:6px;">Enrolled learners</div>'
            elif 'present' in label.lower():
                subtext_html = '<div style="color:#059669; font-size:0.76rem; margin-top:6px; font-weight:600;">Verified today</div>'
            elif 'absent' in label.lower():
                subtext_html = '<div style="color:#DC2626; font-size:0.76rem; margin-top:6px; font-weight:500;">Needs follow-up</div>'

        html = f"""
        <div style="
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-top: 3.5px solid {accent_color};
            border-radius: 14px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
            margin-bottom: 12px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        ">
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
                <span style="
                    color: #64748B;
                    font-size: 0.76rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.06em;
                ">{label}</span>
                <div style="
                    width: 34px;
                    height: 34px;
                    border-radius: 8px;
                    background: {accent_soft};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 1.15rem;
                ">{icon}</div>
            </div>
            <div>
                <div style="
                    font-family: 'Space Grotesk', -apple-system, sans-serif;
                    font-weight: 700;
                    font-size: 2.15rem;
                    color: #0F172A;
                    line-height: 1.1;
                ">{value}</div>
                {subtext_html}
            </div>
        </div>
        """

        with col:
            st.markdown(html, unsafe_allow_html=True)
