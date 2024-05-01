import streamlit as st
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import folium
import requests

if 'center' not in st.session_state:
    st.session_state['center'] = [-23.588609, -46.681847]
if 'zoom' not in st.session_state:
    st.session_state['zoom'] = 16
if 'buscando_loc' not in st.session_state:
    st.session_state['buscando_loc'] = False

with st.form('get_loc'):
    end = st.text_input('Endereço*')
    cep = st.text_input('CEP')
    cidade = st.text_input('Cidade')
    sub = st.form_submit_button('Buscar')

loc = streamlit_geolocation()
if sub:
    st.session_state['center'] = requests.get(f'http://127.0.0.1:5000/get_loc/{end} {cidade} {cep}').json()['resp']
    loc = [None]
    st.session_state['buscando_loc'] = True
elif not st.session_state['buscando_loc']:
    st.session_state['center'] = [loc['latitude'], loc['longitude']]

if None not in loc:
    st.session_state['buscando_loc'] = False

m = folium.Map(location=st.session_state['center'], zoom_start=st.session_state['zoom'])

folium.Marker(
    st.session_state['center'],
    popup='Liberty Bell',
    tooltip='Liberty Bell'
).add_to(m)

st.title('O MENU')

st_data = st_folium(m, width=725)

col1, col2 = st.columns([1, 0.25])

with col1:
    if st.button('Usuário'):
        st.switch_page('pages/usuarios.py')

with col2:
    if st.button('Restaurantes'):
        st.switch_page('pages/restaurantes.py')
