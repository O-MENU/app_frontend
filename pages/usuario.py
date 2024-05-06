import streamlit as st
import requests
from urlback import URL
from time import sleep

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

if 'user' not in st.session_state:
    st.error('Por favor, faça o login para acessar esta página.')
    sleep(3)
    st.switch_page('pages/Login.py')


dados = requests.get(f'{URL}/usuarios/{st.session_state.user}')
if dados.status_code == 200:
    dados = dados.json()
    col1, col2, col3 = st.columns([1, 0.3, 1])

    with col1:
        st.title(dados['usuario']['nome'])

    with col3:
        if st.button('Seguir'):
            seguir = requests.put(f'{URL}/usuarios/{st.session_state.user}')
            if seguir.status_code == 200:
                st.success('Seguindo com sucesso!')
            else:
                st.error('Você já segue este usuário!')

    row1, row2 = st.columns([1, 1])
    with row1:
        seguidores = dados['usuario']['seguidores']
        tamanho = len(dados['usuario']['seguidores'])
        if seguidores != []:
            c = st.expander(label=f'{tamanho} seguidores:')
            with c:
                for seguidor in dados['usuario']['seguidores']:
                    st.write(f"Nome: {seguidor['nome']}")
        else:
            st.write('0 seguidores')
    

    with row2:
        seguindo = dados['usuario']['seguindo']
        tamanho = len(dados['usuario']['seguindo'])
        if seguindo != []:
            c = st.expander(label=f'{tamanho} seguindo:')
            with c:
                for seguindo in dados['usuario']['seguindo']:
                    st.write(f"Nome: {seguindo['nome']}")
        else:
            st.write('0 seguindo')

    st.subheader('Restaurantes favoritos:')
    for item in dados['usuario']['rest_fav']:
        st.write(f"Nome: {item['nome']}")
    
    st.subheader('Comida favorita:')
    for item in dados['usuario']['comida_fav']:
        st.write(f"Nome: {item}")

    st.subheader('Localização:')
    st.write(dados['usuario']['localizacao']['endereco'])
    st.write(f"latitude: {dados['usuario']['localizacao']['geoloc']['lat']}")
    st.write(f"longitude: {dados['usuario']['localizacao']['geoloc']['lng']}")

    

