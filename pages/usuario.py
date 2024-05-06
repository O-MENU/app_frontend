import streamlit as st
import requests
from urlback import URL
from used_func import login_necessario

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

if 'user_access' in st.session_state:
    if 'user' in st.session_state:
        if st.session_state.user == st.session_state.user_access:
            st.switch_page("pages/perfil.py")

    dados = requests.get(f'{URL}/usuarios/{st.session_state.user_access}')

    if dados.status_code == 200:
        dados = dados.json()
        col1, col2, col3 = st.columns([1, 0.3, 1])

        with col1:
            st.title(dados['usuario']['nome'])
        
        if 'user_type' in st.session_state:
            if st.session_state.user_type == 'person':
                with col3:
                    st.write("")
                    st.write("")
                    if 'user' in st.session_state:
                        botao = 'Seguir' if st.session_state.user not in [seguidor['_id'] for seguidor in dados['usuario']['seguidores']] else 'Seguindo'
                        hover = '' if st.session_state.user not in [seguidor['_id'] for seguidor in dados['usuario']['seguidores']] else 'Deixar de seguir'
                    else:
                        botao = 'seguir'
                        hover = ''

                    profile = st.button(botao, help=hover)
                    if login_necessario(profile):
                        seguir = requests.put(f'{URL}/usuarios/{st.session_state.user}/{st.session_state.user_access}')
                        if seguir.status_code == 200:
                            st.rerun()
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
                        if st.button(f"{seguidor['nome']}", use_container_width=True, key=f"seguidor{seguidor['_id']}"):
                            st.session_state.user_access = seguidor['_id']
                            st.rerun()
            else:
                st.write("")
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
                st.write("")
                st.write('0 seguindo')

        st.subheader('Restaurantes favoritos:')
        for item in dados['usuario']['rest_fav']:
            st.write(f"Nome: {item['nome']}")
        
        st.subheader('Comida favorita:')
        for item in dados['usuario']['comida_fav']:
            st.write(f"Nome: {item}")

        # st.subheader('Localização:')
        # st.write(dados['usuario']['localizacao']['endereco'])                           <------- Mto invasivo? sla
        # st.write(f"latitude: {dados['usuario']['localizacao']['geoloc']['lat']}")
        # st.write(f"longitude: {dados['usuario']['localizacao']['geoloc']['lng']}")

    

