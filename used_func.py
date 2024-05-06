import streamlit as st
import math
from streamlit_modal import Modal
import requests
from urlback import URL

def find_dist(p1, p2):
    return int(math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))*10**15)

def login_necessario(bool):
    if 'user' not in st.session_state:
        modal = Modal(title="Login necessário", key="login")
        if bool:
            modal.open()
        if modal.is_open():
            with modal.container():
                email = st.text_input('email:')
                senha = st.text_input('Senha: ', type='password')

                if email and senha:
                    users = [user for user in requests.get(f"{URL}/usuarios").json()['usuarios'] if email == user['email'] and senha == user['senha']]

                vld = not(email and senha)

                c1,_,c3 = st.columns((1,3.5,1))
                if c1.button('Entrar', disabled=vld):
                    if len(users) > 0:
                        st.session_state.user = users[0]['_id']
                        modal.close()
                    else:
                        st.error('Usuário não encontrado',)
                if c3.button('Cadastrar-se'):
                    modal.close(False)
                    st.switch_page('pages/cadastro.py')
        return False
    else:
        if bool:
            return True
    
def header(profile= True):
    _,c2,_,c4 = st.columns((1,0.5,0.8,0.2))
    c2.title('MENU')

    if profile:
        c4.write("")
        c4.write("")
        icon = '👤'
        profile = c4.button(icon)
        if login_necessario(profile):
            st.switch_page('pages/perfil.py')
        