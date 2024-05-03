import streamlit as st
import requests
from streamlit_star_rating import st_star_rating

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

if "id" in st.session_state:
    dados = requests.get(f'http://127.0.0.1:5000/restaurantes/{st.session_state.id}')
    if dados.status_code == 200:
        resposta = dados.json()


        col1, col2, col3 = st.columns([1, 0.5, 1])
        with col1:
            st.title(resposta['restaurante']['nome'])
        
        with col3:
            if st.button('favoritar'):
                fav = requests.put(f'http://127.0.0.1:5000/usuarios/2/restaurante/{st.session_state.id}')
                if fav.status_code == 200:
                    st.success('Restaurante favoritado com sucesso!')


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


        c = st.expander(label='Avalie a gente!')
        with c:
            st.session_state.stars = st_star_rating("Avalie a gente", maxValue=5, defaultValue=3, key="rating")
            mot = ['serviço', 'bebidas', 'infraestrutura', 'tempo', 'ambiente', 'tempero', 'comida']
            selected_motivos = {}
            st.subheader('Pontos fortes!')
            for motivo in mot:
                selected_motivos[motivo] = st.checkbox(motivo, key=motivo)
            st.session_state.comentario = st.text_area(label='Comentários', placeholder='Lugar agradável...')
            if st.button('Enviar Avaliação', key='submit_rating'):
                av = {
                    'nota': st.session_state.stars,
                    'pontos_fortes': [motivo for motivo in selected_motivos if selected_motivos[motivo]],
                    'comentario': st.session_state.comentario
                }
                avaliacao = requests.post(f'http://127.0.0.1:5000/avaliacoes/usuarios/1/restaurantes/6', json=av)
                if avaliacao.status_code == 201 or avaliacao.status_code == 200 or avaliacao.status_code == 204 or avaliacao.status_code == 202 or avaliacao.status_code == 203:
                    st.success('Avaliação enviada com sucesso!')
                else:
                    st.error(f'{avaliacao}')

    else:
        st.error('Falha ao obter dados do restaurante. Status code: {}'.format(dados.status_code))
else:
    st.write('Por favor, pesquise um ID válido!')
