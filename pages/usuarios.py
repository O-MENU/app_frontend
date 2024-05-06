import streamlit as st
import pandas as pd
import requests
from urlback import URL

update, delete = False, False

try:
    users = requests.get(f"{URL}/usuarios").json()['usuarios']
except:
    st.error("Erro na requisição dos usuários") # <--- !!!!!   DESCOMENTAR AO OBTER URL   !!!!!
    users = []

    # V  Header  V
col1, col2 = st.columns(2)
col1.title("Usuários") # Título da página
with col2:
    st.write("")
    st.write("")
    if st.button("Adicionar novo"):
        st.switch_page("pages/cadastro.py")

# V  Definir filtros pelo usuário  V
st.write("")
st.subheader("Filtrar por:")

op_filtro = ["ID", "Nome", "E-mail", "Data", "Senha"] # Opções de filtro
db_op_filtro = ["_id", "nome", "email", "data", "senha"] # Opções de filtro como estão na base de dados

id_inicial = 0 # Index da opção inicial

# V  Filtro  V
filtro = st.radio("filtros", op_filtro, index=id_inicial, label_visibility="collapsed")
txt_filtro = st.text_input("txt filtro", placeholder=f"Filtrando por {filtro}", label_visibility="collapsed")
if filtro == "ID" and txt_filtro:
    txt_filtro = int(txt_filtro)

filtered_users = [user for user in users if user[db_op_filtro[op_filtro.index(filtro)]] == txt_filtro or not txt_filtro] # Filtra o DataFrame de acordo com o filtro passado

st.write("")
st.write("")

    # V   exibir dataframe com botoes   V
df_filtrado = pd.DataFrame(filtered_users).set_index("_id").reindex(columns=["nome", "email", "rest_fav", "seguidores", "seguindo", "localizacao", "data", "senha"])
st.dataframe(df_filtrado)

if len(filtered_users) == 1:
    _,c1,c2,_ = st.columns((1,1,0.9,1))
    update = c1.button('Atualizar')
    delete = c2.button('Apagar')

if update:  # Lógica do botão de editar
    st.session_state.user_id = id
    st.switch_page('edita usuario')

if delete:  # Lógica do botão de deletar
    try:
        requests.delete(f"{URL}/usuarios/{id}")
        pass
    except:
        st.error("Erro ao apagar usuário")
    else:
        st.success("Usuário removido com sucesso")




