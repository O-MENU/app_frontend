import streamlit as st
import requests
from streamlit_star_rating import st_star_rating

if "id" in st.session_state:
    dados = requests.get(f'http://127.0.0.1:5000/restaurantes/{st.session_state.id}')
    if dados.status_code == 200:
        resposta = dados.json()

        st.title(resposta['restaurante']['nome'])

        st.subheader('Cardápio')
        for item in resposta['restaurante']['cardapio']:
            st.write(f"Prato: {item['nome_prato']}")
            st.write(f"Descrição: {item['descricao']}")
            st.write(f"Preço: R${item['preco']:0.2f}")
            if item['foto_prato']: 
                st.image(item['foto_prato'], caption=item['nome_prato'], width=300)

        st.subheader('Localização:')
        st.write(resposta['restaurante']['localizacao']['endereco'])

        st.subheader('Contato:')
        st.write(resposta['restaurante']['email'])

        if st.button('Avalie a gente'):
            c = st.container(border=True)
            with c:
                stars = st_star_rating("Avalie nosso restaurante", maxValue=5, defaultValue=3, key="rating")
                motivo = st.text_area(label='Motivo', placeholder='Dei essa nota porque...')
                comentario = st.text_area(label='Comentarios', placeholder='Lugar agradável...')


    else:
        st.error('Falha ao obter dados do restaurante. Status code: {}'.format(dados.status_code))
else:
    st.write('Por favor, pesquise um ID válido!')
