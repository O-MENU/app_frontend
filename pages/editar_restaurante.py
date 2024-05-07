import streamlit as st
import requests
from urlback import URL
from used_func import header

header(False, False)

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.subheader("Editar restaurante:")
if "id" in st.session_state:
    dados = requests.get(f'{URL}/restaurantes/{st.session_state.id}')
    if dados.status_code == 200:
        resposta = dados.json()


        nome = resposta['restaurante']['nome']
        email = resposta['restaurante']['email']
        localizacao = resposta['restaurante']['localizacao']
        cnpj = resposta['restaurante']['cnpj']
        senha = resposta['restaurante']['senha']
        

        nome = st.text_input("Nome: ", value=nome, key='nome')
        email = st.text_input("Email: ", value=email, key='email')
        endereco = st.text_input("Endereço:", value=localizacao['endereco'], key='endereco')
        cnpj = st.text_input("CNPJ", value=cnpj, key='cnpj')
        senha = st.text_input("Senha:", value=senha, type="password", key='senha')

        if st.button("salvar alterações"):
            dados_atualizados = {
                "nome": nome,
                "email": email,
                "localizacao": endereco,
                "cnpj": cnpj,
                "senha": senha,
            }
            response = requests.put(f'{URL}/restaurantes/{st.session_state.id}', json=dados_atualizados)
            if response.status_code == 200:
                st.success("Restaurante atualizado com sucesso!")
            else:
                st.error(f"Erro ao atualizar restaurante: {response.status_code}")
                st.text(f"Detalhes do erro: {response.text}")
    else:
        st.error("Erro ao buscar restaurante")
else:
    st.error("ID do restaurante não definido")
