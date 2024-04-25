import streamlit as st

st.title('O menu')

st.subheader('Login:')
email = st.text_input('email:')
senha = st.text_input('Senha: ', type='password')

col1, col2 = st.columns([1, 0.2])
with col1:
    if st.button('entrar'):
        #logica hash
        pass

with col2:
    if st.button('Cadastrar'):
        st.switch_page('pages/cadastro.py')