import streamlit as st
import pandas as pd
import requests
import json


st.title("Adicionar novo restaurante:")

nome = st.text_input("Nome: ")
localizacao = st.text_input("Localização: ")
cnpj = st.text_input("CNPJ")
menu = st.text_input("Menu")
genero = st.radio(
"Gênero: ", 
["Arabe", "Mexicana", "Japonesa", "Nenhum destes"],
index=None,
)

col1, col2 = st.columns([1,0.2])  

with col2:
    if st.button("enviar"):
        data = ({
            "Nome": nome,
            "Localização": localizacao,
            "CNPJ": cnpj,
            "Menu": menu,
            "genero": genero
        })

        headers = {'Content-Type': 'application/json'}

        response = requests.post('V colocar url verdadeira V', data=json.dumps(data), headers=headers)
        if response.status_code == 201:
            st.success("Restaurante adicionado com sucesso!")
        else:
            st.error(f"Erro ao adicionar restaurante: {response.status_code}")

with col1:
    if st.button("voltar"):
        st.switch_page('pages/restaurantes.py')


