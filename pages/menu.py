import streamlit as st
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import folium
import requests, asyncio
from st_pages import hide_pages
import time
from utils import get_location, rest_locs
from urlback import URL
from streamlit_searchbox import st_searchbox
from used_func import find_dist, login_necessario, header
from streamlit_modal import Modal

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

restaurantes = requests.get(f'{URL}/restaurantes').json()['restaurantes']

def buscar_restaurante(termo: str) -> list[any]:
    return [restaurante['nome'] for restaurante in restaurantes if termo.lower() in restaurante['nome'].lower()] if termo else []

if 'center' not in st.session_state:
    st.session_state['center'] = [-23.588609, -46.681847]
if 'zoom' not in st.session_state:
    st.session_state['zoom'] = 16
if 'loc_atual' not in st.session_state:
    st.session_state['loc_atual'] = False
if 'rests_id' not in st.session_state:
    st.session_state.rests_id = 10
if 'i' not in st.session_state:
    st.session_state.i = 0

header()

asyncio.run(get_location())

col1, col2 = st.columns((1,0.15))
with col1:
    busca_rest = st_searchbox(buscar_restaurante, key="busca_restaurante", placeholder="Buscar restaurante...")
if busca_rest:
    st.session_state.id = [rest['_id'] for rest in restaurantes if rest['nome'] == busca_rest][0]
if col2.button('Buscar'):
    st.switch_page('pages/restaurante.py')

pessoa = folium.Icon(icon='fa-sharp fa-solid fa-person', color="darkblue")

m = folium.Map(location=st.session_state['center'], zoom_start=st.session_state['zoom'])

fg = folium.FeatureGroup(name='Restaurantes')

folium.Marker(
    st.session_state['center'],
    popup='Sua Localização',
    tooltip='Sua Localização',
    icon=pessoa,
).add_to(m)

for rest in restaurantes:
    if rest["nota"] == []:
        txt = "n/a"
    else:
        txt = '★' * int(rest["nota"])

    pop = folium.Popup(f'<p>{rest["nome"]}, {rest["nota"]} &#x2605 </p>')
    fg.add_child(
        folium.Marker(
            location=[rest['localizacao']['geoloc']['lat'], rest['localizacao']['geoloc']['lng']],
            popup=pop,
            tooltip=f'{rest["nome"]}, {txt}',
        )
    )

st_data = st_folium(
    m,
    feature_group_to_add=fg,
    center=st.session_state['center'],
    width=850,
    height=650,
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
        loc = requests.get(f'{URL}/get_loc/{l}').json()['resp']
        if loc != st.session_state.center:
            pass
        st.session_state['center'] = loc
        st.rerun()
else:
    if st.session_state.i == 0:
        if 'user' in st.session_state:
            if 'user_type' in st.session_state:
                if st.session_state.user_type == 'person':
                    requests.put(f'{URL}/usuario/{st.session_state.user}/loc', json={'loc':tuple(st.session_state.center)})
                    st.session_state.i += 1

c1,c2,c3,c4 = st.columns((0.5,1,0.4,0.1))
c2.subheader("RESTAURANTES PRÓXIMOS")
if c4.button("Y"):
    pass

st.write("")
st.write("")

def ordem(rest):
    return find_dist(tuple(rest['localizacao']['geoloc'].values()), st.session_state.center)

restaurantes.sort(key=ordem)
a = find_dist([tuple(rest['localizacao']['geoloc'].values()) for rest in restaurantes][0], st.session_state.center)


for rest in restaurantes[0:st.session_state.rests_id]:
    if rest["nota"] == []:
        txt = "n/a"
    else:
        txt = '★' * int(rest["nota"])
    espaco = r"$\hspace{1cm}$"

    if st.button(f"{rest['nome']}{espaco}{rest['categorias'][0]}{espaco}{txt}{espaco}{rest['localizacao']['endereco']}", use_container_width=True):
        st.session_state.id = rest['_id']
        st.switch_page('pages/restaurante.py')
    
st.write("")
st.write("")
c1,c2,c3 = st.columns((2,1,2))
if c2.button("Exibir mais..."):
    st.session_state.rests_id += 10
    st.rerun()


