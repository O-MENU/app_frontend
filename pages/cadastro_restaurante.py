import streamlit as st
import requests
import json
from urlback import URL
from used_func import header, login_necessario
from validations import validate_email

with open("font.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

restaurantes = requests.get(f"{URL}/restaurantes").json()['restaurantes']
usuarios = requests.get(f"{URL}/usuarios").json()['usuarios']

header(profile=False, search=False)

st.subheader("Cadastrar Restaurante")

with st.form("register_form"):
    nome = st.text_input("Nome:", placeholder="Nome do restaurante")
    email = st.text_input("Email:", placeholder="email@email.com")
    if email:
        val_email = validate_email(email)
        if not val_email:
            st.error("Email inválido")
        nex_email = email not in [user['email'] for user in restaurantes+usuarios]
        if not nex_email:
            st.error("E-mail já está sendo utiilizado")

    localizacao = st.text_input("Localização:", placeholder="Rua X")
    cnpj = st.text_input("CNPJ", placeholder="00.000.000/0000-00")
    categorias = st.multiselect(
        "Categorias:", 
        ["Árabe", "Mexicana", "Japonesa", "Brasileira", "Prato Feito", "Hambúrguer", 
         "Hot-dog", "Chinesa", "Italiana", "Saudável", "Fast-food", "Outro(s)"],
    )
    senha = st.text_input("Senha:", type="password", placeholder="Senha")

    col1, col2 = st.columns([1, 0.2])
    with col2:
        submit_button = st.form_submit_button("Enviar")

if submit_button:
    if "Outro(s)" in categorias:
        categorias.remove("Outro(s)")

    data = ({
        "nome": nome,
        "email": email,
        "localizacao": localizacao,
        "cnpj": cnpj,
        "senha": senha,
        "categorias": categorias,
    })

    headers = {'Content-Type': 'application/json'}
    response = requests.post(f'{URL}/restaurantes', data=json.dumps(data), headers=headers)
    
    if response.status_code == 201:
        st.session_state.user = [user['_id'] for user in requests.get(f'{URL}/restaurantes').json()['restaurantes'] if user['email'] == email]
        st.session_state.user_type = "restaurant"
        st.switch_page("pages/menu.py")
    else:
        st.error(f"Erro ao adicionar restaurante: {response.status_code}")
        st.text(f"Detalhes do erro: {response.text}")

