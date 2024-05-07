from streamlit_js_eval import get_geolocation
import folium, requests, asyncio
import streamlit as st
from urlback import URL
import pyperclip

def on_click(event):
    lat_user, lng_user = st.session_state['center']
    lat_rest, lng_rest = event.values()

    coords = requests.get(f'{URL}/get_rota/{lat_user},{lng_user}/{lat_rest},{lng_rest}').json()['resp']['carro_line']

    return folium.vector_layers.PolyLine(
        locations=coords,
        color='blue',
        weight=2,
        popup='Rota',
        tooltip='Rota'
    )

def handle_click(**kwargs):
    lat = kwargs.get('lat')
    lon = kwargs.get('lon')
    # Copy latitude and longitude to clipboard
    pyperclip.copy(f'Latitude: {lat}, Longitude: {lon}')

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

def header():
    _,c2,_,c4 = st.columns((1,0.5,0.8,0.2))
    c2.title('MENU')
    c4.button('A')