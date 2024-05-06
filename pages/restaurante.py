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


        resposta = dados.json()
        if 'user' in st.session_state:
            favoritado = resposta['restaurante']['nome'] in [rest['nome'] for rest in requests.get(f"{URL}/usuarios/{st.session_state.user}").json()['usuario']['rest_fav']]
        else:
            favoritado = False

        fav_button = r"$\LARGE \bigstar$" if favoritado else r"$\LARGE ☆$"

        col1, col2 = st.columns([1,0.1])
        with col1:
            st.title(resposta['restaurante']['nome'])
        
        with col2:
            st.write("")
            st.write("")
            fav = st.button(fav_button)
            if login_necessario(fav):
                if not (st.session_state.user or st.session_state.user == 0):
                    #  tela_login() <----- descomentar quando a funcao for feita
                    pass
                else:
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
                st.write(f"Preço: R${item['preco']}")
                if item['foto_prato']: 
                    st.image(item['foto_prato'], caption=item['nome_prato'], width=300)

        st.subheader('Localização:')
        st.write(resposta['restaurante']['localizacao']['endereco'])

        st.subheader('Contato:')
        st.write(resposta['restaurante']['email'])


        c = st.expander(label='Avalie a gente!')
        with c:
            st.session_state.stars = st_star_rating("Avalie a gente", maxValue=5, defaultValue=0, key="rating")
            mot = ['serviço', 'bebidas', 'infraestrutura', 'tempo', 'ambiente', 'tempero', 'comida']
            selected_motivos = {}
            st.subheader('Pontos fortes!')
            for motivo in mot:
                selected_motivos[motivo] = st.checkbox(motivo, key=motivo)
            st.session_state.comentario = st.text_area(label='Comentários', placeholder='Lugar agradável...')
            print(st.session_state.stars)
            if st.button('Enviar Avaliação', key='submit_rating', disabled=not st.session_state.stars):
                av = {
                    'nota': st.session_state.stars,
                    'pontos_fortes': [motivo for motivo in selected_motivos if selected_motivos[motivo]],
                    'comentario': st.session_state.comentario
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
