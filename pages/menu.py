import streamlit as st
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import folium
import requests, asyncio
from st_pages import hide_pages
import time
from utils import get_location, location

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

if 'center' not in st.session_state:
    st.session_state['center'] = [-23.588609, -46.681847]
if 'zoom' not in st.session_state:
    st.session_state['zoom'] = 16
if 'loc_atual' not in st.session_state:
    st.session_state['loc_atual'] = False

col1, col2, col3 = st.columns((1,0.3,1))
col2.title('MENU')

asyncio.run(get_location())

col1, col2 = st.columns((1,0.15))
st.session_state.id = col1.text_input('id', label_visibility="collapsed", placeholder="Buscar restaurante pelo id")
if col2.button('Buscar'):
    st.switch_page('pages/restaurante.py')

m = folium.Map(location=st.session_state['center'], zoom_start=st.session_state['zoom'])

folium.Marker(
    st.session_state['center'],
    popup='Liberty Bell',
    tooltip='Liberty Bell'
).add_to(m)

st_data = st_folium(m, width=725)

if not st.session_state.loc_atual:
    with st.expander("Localização manual"):
        with st.form('Definir'):
            end = st.text_input('Endereço*')
            cep = st.text_input('CEP')
            cidade = st.text_input('Cidade')
            sub = st.form_submit_button('Buscar')

    if sub:
        loc = requests.get(f'localhost/get_loc/{end} {cidade} {cep}').json()['resp']

col1, col2 = st.columns([1, 0.25])

with col1:
    if st.button('Usuário'):
        st.switch_page('pages/usuarios.py')

with col2:
    if st.button('Restaurantes'):
        st.switch_page('pages/restaurantes.py')