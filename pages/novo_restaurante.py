import streamlit as st
import pandas as pd
import requests
import json

st.title("Adicionar novo restaurante:")

nome = st.text_input("Nome: ")
email = st.text_input("Email: ")
localizacao = st.text_input("Localização: ")
cnpj = st.text_input("CNPJ")
senha = st.text_input("Senha:", type="password")
categorias = st.text_input("Categorias:")

col1, col2 = st.columns([1, 0.2])  

with col2:
    if st.button("enviar"):
        data = ({
            "nome": nome,
            "email": email,
            "localizacao": localizacao,
            "cnpj": cnpj,
            "senha": senha,
            "categorias": categorias,
        })

        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://127.0.0.1:5000/restaurantes', data=json.dumps(data), headers=headers)
        
        if response.status_code == 201:
            st.success("Restaurante adicionado com sucesso!")
        else:
            st.error(f"Erro ao adicionar restaurante: {response.status_code}")
            st.text(f"Detalhes do erro: {response.text} {requests.Response}")  

with col1:
    if st.button("voltar"):
        st.switch_page('pages/restaurantes.py')
