import streamlit as st
from validations import validate_email
import requests
from urlback import URL
from datetime import datetime, date

val_email, nex_email = False, False

users = requests.get(f"{URL}/usuarios").json()['usuarios']

st.title('Cadastre-se')

nome = st.text_input('Nome', placeholder='Edgar Da silva')

email = st.text_input('Email', placeholder='exemplo@gmail.com')
if email:
    val_email = validate_email(email)
    if not val_email:
        st.error("Email inválido")
    nex_email = email not in [user['email'] for user in users]
    if not nex_email:
        st.error("E-mail já está sendo utiilizado")

data_nascimento = st.date_input('Data de Nascimento', min_value=date(1900, 1, 1))

senha = st.text_input('Senha:', type='password')
conf_senha = st.text_input('Confirme sua senha:', type='password')

val_senha = (senha == conf_senha)

vld_cadastro = not(nome and val_email and nex_email and val_senha)

c1,_,c3 = st.columns((0.4,1,0.6))
if c1.button('Cadastrar', disabled=vld_cadastro):
    json={'nome': nome, 'email': email, 'senha': senha, 'data': data_nascimento.strftime('%Y-%m-%d')}
    json
    post = requests.post(f"{URL}/usuarios", json=json)
    post.status_code
    [user['_id'] for user in requests.get(f"{URL}/usuarios").json()['usuarios'] if user['email'] == email]
    st.session_state.user = [user['_id'] for user in requests.get(f"{URL}/usuarios").json()['usuarios'] if user['email'] == email][0]
    st.switch_page('pages/menu.py')
    
if c3.button('Continuar sem cadastrar'):
    st.switch_page('pages/menu.py')
