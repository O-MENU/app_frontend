import streamlit as st
import requests
from urlback import URL

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

if 'user' in st.session_state:
    dados = requests.get(f'{URL}/usuarios/{st.session_state.user}').json()

    st.title(dados['usuario']['nome'])

    row1, row2 = st.columns([1, 1])

    with row1:
        seguidores = dados['usuario']['seguidores']
        tamanho = len(dados['usuario']['seguidores'])
        if seguidores != []:
            c = st.expander(label=f'{tamanho} seguidores:')
            with c:
                for seguidor in dados['usuario']['seguidores']:
                    if st.button(f"{seguidor['nome']}", use_container_width=True, key=f"seguidor{seguidor['_id']}"):
                        st.session_state.user_access = seguidor['_id']
                        st.rerun()
        else:
            st.write('0 seguidores')


    with row2:
        seguindo = dados['usuario']['seguindo']
        tamanho = len(dados['usuario']['seguindo'])
        if seguindo != []:
            c = st.expander(label=f'{tamanho} seguindo:')
            with c:
                for seguindo in dados['usuario']['seguindo']:
                    if st.button(f"{seguindo['nome']}", use_container_width=True, key=f"seguindo{seguindo['_id']}"):
                        st.session_state.user_access = seguindo['_id']
                        st.rerun()
        else:
            st.write('0 seguindo')

    st.subheader('Restaurantes favoritos:')
    for item in dados['usuario']['rest_fav']:
        st.write(f"Nome: {item['nome']}")

    st.subheader('Comida favorita:')
    for item in dados['usuario']['comida_fav']:
        st.write(f"Nome: {item}")
    options = ['?']
    st.selectbox("Adicionar outro", options=options)
else:
    st.switch_page("pages/menu.py")