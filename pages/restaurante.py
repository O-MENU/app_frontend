import streamlit as st
import requests
from streamlit_star_rating import st_star_rating
from urlback import URL
from used_func import login_necessario

with open( "font.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

if "id" in st.session_state:
    dados = requests.get(f'{URL}/restaurantes/{st.session_state.id}')
    if dados.status_code == 200:

        favoritado = False

        resposta = dados.json()
        if 'user' in st.session_state:
            if 'user_type' in st.session_state:
                if st.session_state.user_type == 'person':
                    favoritado = resposta['restaurante']['_id'] in [rest['_id'] for rest in requests.get(f"{URL}/usuarios/{st.session_state.user}").json()['usuario']['rest_fav']]
                else:
                    st.switch_page('pages/menu.py')

        fav_button = r"$\LARGE \bigstar$" if favoritado else r"$\LARGE ☆$"

        col1, col2 = st.columns([1,0.1])
        with col1:
            st.title(resposta['restaurante']['nome'])

        if st.session_state.user_type == 'person':        
            with col2:
                st.write("")
                st.write("")
                fav = st.button(fav_button)
                if login_necessario(fav):
                    if favoritado:
                        requests.delete(f'{URL}/usuarios/{st.session_state.user}/restaurante/{st.session_state.id}')
                        st.rerun()
                    else:
                        requests.put(f'{URL}/usuarios/{st.session_state.user}/restaurante/{st.session_state.id}')
                        st.rerun()

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

        st.subheader('Localização:')
        st.write(resposta['restaurante']['localizacao']['endereco'])

        st.subheader('Categoria:')
        for index, item in enumerate(resposta['restaurante']['categorias']):
            st.write(item)
            if st.button('Favoritar categoria', key=f'favoritar_categoria_{index}'):
                response = requests.put(f'{URL}/usuarios/{st.session_state.user}/comidas', json=[item])
                if response.status_code == 200:
                    st.success('Categoria favoritada com sucesso!')
                else:
                    st.error(f'Erro ao favoritar categoria {item}: {response.text}')


        st.subheader('Contato:')
        st.write(resposta['restaurante']['email'])

        if st.session_state.user_type == 'person':
            c = st.expander(label='Avalie a gente!')
            with c:
                stars = st_star_rating("Avalie a gente", maxValue=5, defaultValue=0, key="rating")
                mot = ['serviço', 'bebidas', 'infraestrutura', 'tempo', 'ambiente', 'tempero', 'comida']
                selected_motivos = {}
                st.subheader('Pontos fortes!')
                for motivo in mot:
                    selected_motivos[motivo] = st.checkbox(motivo, key=motivo)
                comentario = st.text_area(label='Comentários', placeholder='Lugar agradável...')
                avaliar = st.button('Enviar Avaliação', key='submit_rating', disabled=not stars)
                if login_necessario(avaliar):
                    av = {
                        'nota': stars,
                        'pontos_fortes': [motivo for motivo in selected_motivos if selected_motivos[motivo]],
                        'comentario': comentario
                    }
                    avaliacao = requests.post(f'{URL}/avaliacoes/usuarios/{st.session_state.user}/restaurantes/{st.session_state.id}', json=av)
                    if avaliacao.status_code == 201 or avaliacao.status_code == 200 or avaliacao.status_code == 204 or avaliacao.status_code == 202 or avaliacao.status_code == 203:
                        st.success('Avaliação enviada com sucesso!')
                    else:
                        st.error(f'{avaliacao}')

    else:
        st.error('Falha ao obter dados do restaurante. Status code: {}'.format(dados.status_code))
else:
    st.switch_page("pages/menu.py")
