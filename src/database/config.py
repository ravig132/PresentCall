import streamlit as st

try:
    from supabase import Client, create_client
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "The 'supabase' package is missing. Install the project dependencies with: "
        "python -m pip install -r requirements.txt"
    ) from exc

try:
    supabase: Client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"],
    )
except KeyError as exc:
    raise RuntimeError(
        "Missing Supabase configuration. Add SUPABASE_URL and SUPABASE_KEY to your Streamlit secrets."
    ) from exc