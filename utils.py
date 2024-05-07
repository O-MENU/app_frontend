from streamlit_js_eval import get_geolocation
import asyncio
import streamlit as st
import requests
from urlback import URL

def location(loc):
    st.session_state.center = (loc["latitude"], loc['longitude'])
    return (loc["latitude"], loc['longitude'])

async def get_location():
    loc = get_geolocation()
    timer = 60

    while timer > 0 and loc is None:
        asyncio.sleep(1)
        timer -= 1
    
    if loc is not None:
        st.session_state.loc_atual = True
        st.session_state.center = (loc['coords']['latitude'], loc['coords']['longitude'])
        

def rest_locs(dic):
    return [{'localizacao': rest['localizacao'], 'nome' : rest['nome'], 'nota' : rest['nota']} for rest in dic]