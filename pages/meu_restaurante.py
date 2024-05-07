import base64
import streamlit as st
import requests
from streamlit_star_rating import st_star_rating
from urlback import URL
from used_func import login_necessario, header
import time

header(profile=False, search=False)

if 'user' in st.session_state:
    if 'user_type' in st.session_state:
        if st.session_state.user_type != 'restaurant':
            st.switch_page("pages/menu.py")
        
    with open( "font.css" ) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    if "user" in st.session_state:
        # time.sleep(5)
        dados = requests.get(f'{URL}/restaurantes/{st.session_state.user}')
        if dados.status_code == 200:

            resposta = dados.json()

            st.title(resposta['restaurante']['nome'])

            with st.expander(r"$\Large MENU$"):
                for item in resposta['restaurante']['cardapio']:
                    st.write(f"Prato: {item['nome_prato']}")
                    st.write(f"Descrição: {item['descricao']}")
                    if type(item['preco']) in (int, float): 
                        st.write(f"Preço: R${item['preco']:0.2f}")
                    else:
                        st.write(f"Preço: R${item['preco']}")
                    if item['foto_prato']: 
                        st.image(item['foto_prato'], caption=item['nome_prato'], width=300)
            with st.popover("Adicionar item ao MENU"):
                nome = st.text_input("nome", placeholder="Nome do item", label_visibility="collapsed")
                desc = st.text_input("nome", placeholder="Descrição", label_visibility="collapsed")
                preco = st.text_input("nome", placeholder="Preço", label_visibility="collapsed")
                ft=''
                uploaded_file = st.file_uploader("Imagem do item",['jpg', 'png'])
                if uploaded_file is not None:
                    encoded_string = base64.b64encode(uploaded_file.read())
                    _,c,_ = st.columns((0.5,1,0.5))
                    c.image("data:image/jpeg;base64," + str(encoded_string)[2:-1])
                    ft = "data:image/jpeg;base64," + str(encoded_string)[2:-1]
                _,c,_ = st.columns((0.8,1,0.8))
                if c.button("Adicionar item"):
                    requests.put(f"{URL}/restaurantes/{st.session_state.user}/adicionar_prato", json={"descricao": desc, "foto_prato": ft, "nome_prato": nome, "preco": preco})
                


            st.subheader('Localização:')
            st.write(resposta['restaurante']['localizacao']['endereco'])

            st.subheader('Contato:')
            st.write(resposta['restaurante']['email'])
                
else: st.switch_page("pages/menu.py")