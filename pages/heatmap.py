import streamlit as st
import requests
from urlback import URL
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from used_func import header

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)


if 'center' not in st.session_state:
    st.session_state['center'] = [-23.588609, -46.681847]

if 'heatmap' not in st.session_state:
    st.switch_page('pages/usuarios.py')

data = requests.get(f'{URL}/usuarios/loc').json() if st.session_state.heatmap[0] == 'all' else requests.get(f'{URL}/usuario/{st.session_state.heatmap[1]}/loc').json()

m = folium.Map(location=st.session_state.center, zoom_start=13)  # Coordenadas do centro dos EUA
HeatMap(data).add_to(m)


header(False, False)

st.subheader("Heatmap")
st_folium(m, width=725)