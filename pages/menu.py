import streamlit as st
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import folium
import requests
from st_pages import hide_pages

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
    st.session_state['buscando_loc'] = True
    st.session_state['center'] = requests.get(f'http://127.0.0.1:5000/get_loc/{end} {cidade} {cep}').json()['resp']
    loc = {'latitude' : None}
elif not st.session_state['buscando_loc'] and loc['latitude'] != None:
    st.session_state['center'] = [loc['latitude'], loc['longitude']]

if loc['latitude'] != None:
    st.session_state['buscando_loc'] = False

st.session_state['buscando_loc']

m = folium.Map(location=st.session_state['center'], zoom_start=st.session_state['zoom'])

folium.Marker(
    st.session_state['center'],
    popup='Liberty Bell',
    tooltip='Liberty Bell'
).add_to(m)

st.title('O MENU')

st.session_state.id = st.text_input('Digite o id do restaurante que deseja: ')

if st.button('buscar'):
    st.switch_page('pages/restaurante.py')

st_data = st_folium(m, width=725)

col1, col2 = st.columns([1, 0.25])

with col1:
    if st.button('Usuário'):
        st.switch_page('pages/usuarios.py')

with col2:
    if st.button('Restaurantes'):
        st.switch_page('pages/restaurantes.py')
