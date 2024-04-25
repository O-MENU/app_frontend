import streamlit as st


st.title('Cadastro: ')

nome = st.text_input('Nome', placeholder='Edgar Da silva')
email = st.text_input('Email', placeholder='exemplo@gmail.com')
data = st.date_input('Data')
senha = st.text_input('Senha:', type='password')
if st.button('Cadastrar'):
    #logica de implementar no banco de dados
    st.switch_page('pages/menu.py')
    pass