import streamlit as st

def render_real_time_feed(records=None):
    """
    Renders the Real-Time Verification Feed (Sections 16 & 17).
    Clean, live operational panel on the right side of the dashboard.
    Uses existing verification data, and ensures exact identities:
    - Priyanshu Vijay
    - Ravi Kumar Gangwar
    - Soumya Pandey
    """
    items = []

    # If there are real records today that are present, format them
    if records:
        for r in records[:5]:
            name = r.get('students', {}).get('name') or r.get('name') or "Student"
            ts = r.get('timestamp', '')
            time_str = ts.split('T')[-1][:5] if 'T' in ts else "Just now"
            items.append({
                "name": name,
                "status": "AI Verified",
                "time": time_str,
                "is_present": True
            })

    # Ensure required static/demo identities are included
    demo_defaults = [
        {"name": "Priyanshu Vijay", "status": "AI Verified", "time": "10:42 AM", "is_present": True, "initials": "PV", "color": "#2563EB"},
        {"name": "Ravi Kumar Gangwar", "status": "AI Verified", "time": "10:44 AM", "is_present": True, "initials": "RK", "color": "#0284C7"},
        {"name": "Soumya Pandey", "status": "AI Verified", "time": "10:46 AM", "is_present": True, "initials": "SP", "color": "#7C3AED"},
    ]

    # Combine: if no real records, use demo defaults; otherwise blend them
    if not items:
        display_items = demo_defaults
    else:
        # Augment with defaults to guarantee presence of the requested reference names
        display_items = items
        existing_names = {it['name'].lower() for it in items}
        for demo in demo_defaults:
            if demo['name'].lower() not in existing_names:
                display_items.append(demo)
        display_items = display_items[:5]

    feed_items_html = ""
    for idx, it in enumerate(display_items):
        name = it['name']
        time_str = it.get('time', '10:42 AM')
        initials = it.get('initials') or "".join([part[0] for part in name.split()[:2]]).upper()
        color = it.get('color', '#2563EB')
        border_bottom = "border-bottom: 1px solid #F1F5F9;" if idx < len(display_items) - 1 else ""

        feed_items_html += f"""
        <div style="display:flex; align-items:center; justify-content:space-between; padding:12px 14px; {border_bottom} transition:background 0.15s ease;">
            <div style="display:flex; align-items:center; gap:11px;">
                <div style="
                    width:34px;
                    height:34px;
                    border-radius:50%;
                    background:{color};
                    color:#FFFFFF;
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:0.75rem;
                    font-weight:700;
                    letter-spacing:0.02em;
                    flex-shrink:0;
                ">{initials}</div>
                <div>
                    <div style="font-size:0.88rem; font-weight:600; color:#0F172A; line-height:1.2;">{name}</div>
                    <div style="display:flex; align-items:center; gap:4px; margin-top:2px;">
                        <span style="color:#059669; font-size:0.75rem; font-weight:700;">✓</span>
                        <span style="font-size:0.75rem; color:#059669; font-weight:600; background:#ECFDF5; padding:1px 6px; border-radius:4px;">AI Verified</span>
                    </div>
                </div>
            </div>
            <div style="font-size:0.76rem; color:#94A3B8; font-weight:500; font-family:monospace;">
                {time_str}
            </div>
        </div>
        """

    st.markdown(f"""
    <div style="
        background:#FFFFFF;
        border:1px solid #E2E8F0;
        border-radius:14px;
        box-shadow:0 1px 3px rgba(15,23,42,0.05);
        overflow:hidden;
        margin-bottom:20px;
    ">
        <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            padding:14px 16px;
            background:#FAFCFF;
            border-bottom:1px solid #E2E8F0;
        ">
            <div>
                <div style="font-family:'Space Grotesk', sans-serif; font-weight:700; font-size:0.95rem; color:#0F172A;">
                    Real-Time Verification Feed
                </div>
                <div style="font-size:0.74rem; color:#64748B;">
                    Live optical biometric telemetry
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:6px; background:#ECFDF5; border:1px solid #A7F3D0; padding:3px 8px; border-radius:12px;">
                <span style="display:inline-block; width:6px; height:6px; border-radius:50%; background:#10B981; box-shadow:0 0 6px #10B981;"></span>
                <span style="font-size:0.68rem; font-weight:700; color:#059669; letter-spacing:0.04em;">LIVE</span>
            </div>
        </div>
        <div>
            {feed_items_html}
        </div>
    </div>
    """, unsafe_allow_html=True)
