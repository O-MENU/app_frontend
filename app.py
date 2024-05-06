import streamlit as st
import requests
from urlback import URL

users = []

st.title('O menu')

st.subheader('Login:')
email = st.text_input('email:')
senha = st.text_input('Senha: ', type='password')

if email and senha:
    users = [user for user in requests.get(f"{URL}/usuarios").json()['usuarios'] if email == user['email'] and senha == user['senha']]

vld = not(email and senha)

col1, col2 = st.columns([1, 0.2])
with col1:
    if st.button('Entrar', disabled=vld):
        if len(users) > 0:
            st.session_state.user = users[0]['_id']
            st.switch_page("pages/menu.py")
        else:
            st.error('Usuário não encontrado',)
        

with col2:
    if st.button('Cadastrar'):
        st.switch_page('pages/cadastro.py')