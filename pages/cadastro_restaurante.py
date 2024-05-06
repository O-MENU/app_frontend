import streamlit as st
import pandas as pd
import requests
import json
from urlback import URL

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.title("Cadastrar restaurante")
st.write("")
st.write("")
st.write("")

nome = st.text_input("Nome: ")
email = st.text_input("Email: ")
localizacao = st.text_input("Localização: ")
cnpj = st.text_input("CNPJ")
menu = st.text_input("Menu")
categorias = st.multiselect(
"Categorias: ", 
["Arabe", "Mexicana", "Japonesa", "Brasileira", "Pf", "Hambúrguer", "Hot-dog", "Chinesa", "Italiana", "Saudável", "Fast-food", "Outro(s)"],
)
senha = st.text_input("Senha:", type="password")
col1, col2 = st.columns([1, 0.2])  

with col2:
    if st.button("enviar"):
        data = ({
            "nome": nome,
            "email": email,
            "localizacao": localizacao,
            "cnpj": cnpj,
            "senha": senha,
            "categorias": categorias.remove("Outro"),
        })

        headers = {'Content-Type': 'application/json'}
        response = requests.post(f'{URL}/restaurantes', data=json.dumps(data), headers=headers)
        
        if response.status_code == 201:
            st.success("Restaurante adicionado com sucesso!")
        else:
            st.error(f"Erro ao adicionar restaurante: {response.status_code}")
            st.text(f"Detalhes do erro: {response.text} {requests.Response}")  

with col1:
    if st.button("voltar"):
        st.switch_page('pages/cadastro.py')
