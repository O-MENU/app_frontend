import streamlit as st
import requests
from urlback import URL
from used_func import header, login_necessario

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

users = []
rests = []

header(profile=False, search=False)

st.subheader('Login:')
email = st.text_input('email:', key='email')
senha = st.text_input('Senha: ', type='password', key='senha')

if email and senha:
    users = [user for user in requests.get(f"{URL}/usuarios").json()['usuarios'] if email == user['email'] and senha == user['senha']]
    rests = [rest for rest in requests.get(f"{URL}/restaurantes").json()['restaurantes'] if email == rest['email'] and senha == rest['senha']]

login, login_type = (users[0], 'person') if len(users) > 0 else (rests[0], 'restaurant') if len(rests) > 0 else (False, '')

vld = not(email and senha)

col1, col2 = st.columns([1, 0.2])
with col1:
    if st.button('Entrar', disabled=vld, key='entrar'):
        if login:
            st.session_state.user = login['_id']
            st.session_state.user_type = login_type
            st.switch_page("pages/menu.py")
        else:
            st.error('Email e/ou senha incorretos')
        
with col2:
    if st.button('Cadastrar',key='cadadstro'):
        st.switch_page('pages/cadastro.py')