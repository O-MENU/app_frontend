import streamlit as st
import requests
from urlback import URL
from used_func import header, login_necessario

users = []

header(profile=False)

st.subheader('Login:')
email = st.text_input('email:', key='email')
senha = st.text_input('Senha: ', type='password', key='senha')

if email and senha:
    users = [user for user in requests.get(f"{URL}/usuarios").json()['usuarios'] if email == user['email'] and senha == user['senha']]

vld = not(email and senha)

col1, col2 = st.columns([1, 0.2])
with col1:
    if st.button('Entrar', disabled=vld, key='entrar'):
        if len(users) > 0:
            st.session_state.user = users[0]['_id']
            st.switch_page("pages/menu.py")
        else:
            st.error('Usuário não encontrado')
        
with col2:
    if st.button('Cadastrar',key='cadadstro'):
        st.switch_page('pages/cadastro.py')