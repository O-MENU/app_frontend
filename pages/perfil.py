import streamlit as st
import requests
from urlback import URL

espaco = r"$\hspace{2.5cm}$"

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

if 'user_type' == 'restaurant':
    st.switch_page("page/menu.py")

if 'user' in st.session_state:
    dados = requests.get(f'{URL}/usuarios/{st.session_state.user}').json()

    c1,c2,_ = st.columns(3)
    c2.title(dados['usuario']['nome'])
    c1.write("")
    c1.image(dados['usuario']['foto_perfil'],width = 75)

    st.write("")
    st.write("")

    row1, row2 = st.columns([1, 1])

    with row1:
        seguidores = dados['usuario']['seguidores']
        tamanho = len(dados['usuario']['seguidores'])
        if seguidores != []:
            c = st.expander(label=f'{espaco}{tamanho} seguidores:')
            with c:
                for seguidor in dados['usuario']['seguidores']:
                    if st.button(f"{seguidor['nome']}", use_container_width=True, key=f"seguidor{seguidor['_id']}"):
                        st.session_state.user_access = seguidor['_id']
                        st.rerun()
        else:
            st.write(f'{espaco}0 seguidores')


    with row2:
        seguindo = dados['usuario']['seguindo']
        tamanho = len(dados['usuario']['seguindo'])
        if seguindo != []:
            c = st.expander(label=f'{espaco}{tamanho} seguindo:')
            with c:
                for seguindo in dados['usuario']['seguindo']:
                    if st.button(f"{seguindo['nome']}", use_container_width=True, key=f"seguindo{seguindo['_id']}"):
                        st.session_state.user_access = seguindo['_id']
                        st.rerun()
        else:
            st.write(f'{espaco}0 seguindo')

    st.write("")
    st.write("")
    st.write("")
    st.subheader('Restaurantes favoritos:')
    for item in dados['usuario']['rest_fav']:
        st.write(f"Nome: {item['nome']}")

    st.write("")
    st.write("")
    st.write("")
    st.subheader('Comida favorita:')
    for item in dados['usuario']['comida_fav']:
        st.write(f"Nome: {item}")
    options = ['?']
    st.selectbox("Adicionar outro", options=options)
else:
    st.switch_page("pages/menu.py")