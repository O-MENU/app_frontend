import streamlit as st
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import folium
import requests, asyncio
from st_pages import hide_pages
import time
from utils import get_location, rest_locs

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

fg = folium.FeatureGroup(name='Restaurantes')

folium.Marker(
    st.session_state['center'],
    popup='Sua Localização',
    tooltip='Sua Localização'
).add_to(m)

restaurantes = rest_locs(requests.get(f'http://127.0.0.1:5000/restaurantes').json()['restaurantes'])

for rest in restaurantes:
    pop = folium.Popup(f'<p>{rest["nome"]}, {rest["nota"]} &#x2605 </p>')
    fg.add_child(
        folium.Marker(
            location=[rest['localizacao']['geoloc']['lat'], rest['localizacao']['geoloc']['lng']],
            popup=pop,
            tooltip=f'{rest["nome"]}, {rest["nota"]}'
        )
    )

st_data = st_folium(
    m,
    feature_group_to_add=fg,
    center=st.session_state['center'],
    width=850,
    height=500,
)

if not st.session_state.loc_atual:
    with st.expander("Localização manual"):
        with st.form('Definir'):
            end = st.text_input('Endereço*')
            cep = st.text_input('CEP')
            cidade = st.text_input('Cidade')
            sub = st.form_submit_button('Buscar')

    if sub:
        l = f'{end} {cidade} {cep}'.strip()
        loc = requests.get(f'http://127.0.0.1:5000/get_loc/{l}').json()['resp']
        st.session_state['center'] = loc
        st.rerun()

col1, col2 = st.columns([1, 0.25])

with col1:
    if st.button('Usuário'):
        st.switch_page('pages/usuarios.py')

with col2:
    if st.button('Restaurantes'):
        st.switch_page('pages/restaurantes.py')