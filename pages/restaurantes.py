import streamlit as st
import pandas as pd
import requests

url = "URL AQUI"



try:
    users = requests.get(url).json()
except:
    #st.error("Erro na requisição dos usuários") # <--- !!!!!   DESCOMENTAR AO OBTER URL   !!!!!
    users = []

# V  Header  V
col1, col2 = st.columns(2)
col1.title("Restaurantes") # Título da página
with col2:
    st.write("")
    st.write("")
    if st.button("Adicionar novo"):
        st.switch_page("pages/novo_restaurante.py")
            

    # V  Definir filtros pelo usuário  V
st.write("")
st.subheader("Filtrar por:")

op_filtro = ["ID", "Nome", "Localização", "CNPJ", "Menu"] # Opções de filtro
db_op_filtro = ["_id", "Nome", "Localização", "CNPJ", "Menu"] # Opções de filtro como estão na base de dados

id_inicial = 0 # Index da opção inicial

    # V  Filtro  V
filtro = st.radio("filtros", op_filtro, index=id_inicial, label_visibility="collapsed")
txt_filtro = st.text_input("txt filtro", placeholder=f"Filtrando por {filtro}", label_visibility="collapsed")

df_users = pd.DataFrame(users) # DataFrame de usuários
filtered_df_users = [col for col in df_users if col[db_op_filtro[op_filtro.index(filtro)]] == txt_filtro or not filtro] # Filtra o DataFrame de acordo com o filtro passado

st.write("")
st.write("")

    # V   exibir dataframe com botoes   V

if len(filtered_df_users) > 0:
    format_cols = (0.5,1,2,1,2,1,1) # Tamanho de cada coluna + botao de editar + botao de apagar
    cols = st.columns(format_cols)
    fields = ["ID", "Nome", "Localização", "CNPJ", "Menu", "Editar", "Apagar"] # Colunas + botao de editar + botao de apagar

    for col, field_name in zip(cols, fields): # Escreve o título da coluna
        col.write(field_name)

    for i, id in enumerate(filtered_df_users["_id"]):
        col1, col2, col3, col4, col5, col6, col7 = st.columns(format_cols) # Número de fields

        col1.write(str(id))#                        }
        col2.write(filtered_df_users["nome"][i])#    }
        col3.write(filtered_df_users["localização"][i])#    }   Colunas do DataFrame
        col4.write(filtered_df_users["CNPJ"][i])#    }
        col5.write(filtered_df_users["menu"][i])#    }

        button1_phold = col6.empty() #                           }
        update = button1_phold.button("Editar", key=f"{i}b")#     }  Botão de editar

        button2_phold = col7.empty()#                            } 
        delete = button2_phold.button("Apagar", key=f"{i}c")#     }  Botão de deletar

        if update:  # Lógica do botão de editar
            st.session_state.user_id = id
            st.switch_page('edita restaurante')

        if delete:  # Lógica do botão de deletar
            try:
                # requests.delete(f"{url}/{id}")
                pass
            except:
                st.error("Erro ao apagar restaurante")
            else:
                st.success("Restaurante removido com sucesso")
else:
    st.warning("Nenhum restaurante encontrado com estes filtros")




