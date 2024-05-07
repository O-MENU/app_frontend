import streamlit as st
import math
from streamlit_modal import Modal
import requests
from urlback import URL
import time
from streamlit_searchbox import st_searchbox
import smtplib
from email.message import EmailMessage

def find_dist(p1, p2):
    return int(math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))*10**15)

def login_necessario(bool):
    if 'user' not in st.session_state:
        users = []
        rests = []

        modal = Modal(title="Login necessário", key="login")
        if bool:
            modal.open()
        if modal.is_open():
            with modal.container():
                email = st.text_input('email:')
                senha = st.text_input('Senha: ', type='password')
                if email and senha:
                    users = [user for user in requests.get(f"{URL}/usuarios").json()['usuarios'] if email == user['email'] and senha == user['senha']]
                    rests = [rest for rest in requests.get(f"{URL}/restaurantes").json()['restaurantes'] if email == rest['email'] and senha == rest['senha']]

                login, login_type = (users[0], 'person') if len(users) > 0 else (rests[0], 'restaurant') if len(rests) > 0 else (False, '')

                vld = not(email and senha)

                col1, col2 = st.columns([1, 0.2])
                with col1:
                    if st.button('Entrar', disabled=vld, key='entrar'):
                        if login:
                            st.session_state.user = login['_id']
                            st.session_state.user_type = login_type
                            modal.close()
                        else:
                            st.error('Email e/ou senha incorretos')
                if col2.button('Cadastrar-se'):
                    modal.close(False)
                    st.switch_page('pages/cadastro.py')
        return False
    else:
        if bool:
            return True
    
def header(profile= True, search= True):
    c5,_,c2,_,c4 = st.columns((0.2,0.8,0.5,0.8,0.2))

    c2.write("")
    if c2.button(r'$\Huge MENU$', type="primary"):
        st.switch_page("pages/menu.py")

    st.markdown(
    """
    <style>
    button[kind="primary"] {
        background: none!important;
        border: none;
        padding: 0!important;
        color: #4C291A !important;
        text-decoration: none;
        cursor: pointer;
        border: none !important;
        font-size: 1px;
    }
    button[kind="primary"]:hover {
        text-decoration: none;
        color: #2C0900 !important;
    }
    button[kind="primary"]:focus {
        outline: none !important;
        box-shadow: none !important;
        color: black !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    # st.markdown('<style> button[kind=primary] { font-size:50px; padding:50px} </style>', unsafe_allow_html=True)

    if profile:
        icon = '👤'
        pgn = 'pages/perfil.py'
        if 'user_type' in st.session_state:
            icon = '🍴' if st.session_state.user_type == 'restaurant' else icon
            pgn = 'pages/meu_restaurante.py' if st.session_state.user_type == 'restaurant' else pgn

        c4.write("")
        c4.write("")
        profile = c4.button(icon)
        if login_necessario(profile):
            st.switch_page(pgn)
    
    if search:
        icon = '🔎'
        
        usuarios = requests.get(f"{URL}/usuarios").json()["usuarios"]        
        def buscar_usuario(termo: str) -> list[any]:
            return [usuario['nome'] for usuario in usuarios if termo.lower() in usuario['nome'].lower()] if termo else []
        
        with c5:
            st.write("")
            st.write("")
            usuario = ""
            with st.popover(icon, ):
                busca_usuario = st_searchbox(buscar_usuario, key="busca_usuario", placeholder="Buscar usuário...")
                if busca_usuario:
                    if len(busca_usuario) > 0:
                        usuario = busca_usuario
                c1,c2 = st.columns(2)
                ver_perfil = c1.button("Ver perfil", disabled=not(usuario))
                if ver_perfil:
                    if usuario in [user['nome'] for user in usuarios]:
                        st.session_state.user_access = [user['_id'] for user in usuarios if user['nome'] == usuario][0]
                        st.switch_page("pages/usuario.py")
                    else:
                        st.error("Não encontrado")

def enviar_email_autorizacao(endereco_novo, endereco_antigo):
    email = EmailMessage()
    email['From'] = 'sistema.o.garfo@gmail.com'
    email['To'] = 'o.garfo.main@gmail.com'
    email['Subject'] = 'Autorização de Mudança de Localização'
    email.set_content(f'O endereço do restaurante foi alterado de {endereco_antigo} para {endereco_novo}. Por favor, verifique e autorize a mudança.')

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login('sistema.o.garfo@gmail.com', 'fhlllm&ogarfo')
        smtp.send_message(email)
        print("Email enviado com sucesso!")