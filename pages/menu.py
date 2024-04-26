import streamlit as st
from streamlit_folium import st_folium
import folium

m = folium.Map(location=[39.431, -75], zoom_start=16)
folium.Marker(
    [39.431, -75],
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
