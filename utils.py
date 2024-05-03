from streamlit_js_eval import get_geolocation
import asyncio
import streamlit as st

async def get_location():
    loc = get_geolocation()
    timer = 60

    while timer > 0 and loc is None:
        asyncio.sleep(1)
        timer -= 1
    
    if loc is not None:
        st.session_state.coords = loc['center']