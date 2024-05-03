import streamlit as st
import pandas as pd
import requests

try:
    response = requests.get('http://127.0.0.1:5000/restaurantes')
    data = response.json()['restaurantes']
except Exception as e:
    st.error(f"Error fetching data: {str(e)}")
    data = []

df_restaurants = pd.DataFrame(data)

col1, col2 = st.columns([3, 1])
col1.title("Restaurantes")

if col2.button("Adicionar novo"):
    st.session_state['page'] = 'new_restaurant'
    st.experimental_rerun()

st.subheader("Filtrar por:")
options = ["Nome", "Localização", "CNPJ", "Menu"]
db_options = ["nome", "localizacao", "cnpj", "cardapio"]

selected_filter = st.selectbox("Escolha o filtro", options)
filter_input = st.text_input("Valor do filtro", "")

if filter_input:
    filtered_data = df_restaurants[df_restaurants[db_options[options.index(selected_filter)]].astype(str).str.contains(filter_input, case=False)]
else:
    filtered_data = df_restaurants

if not filtered_data.empty:
    st.dataframe(filtered_data[['nome', 'localizacao', 'cnpj']])

    if filter_input:
        for idx, row in filtered_data.iterrows():
            col1, col2 = st.columns([1, 1], gap="small")
            if col1.button(f"Editar", key=f"edit_{row['_id']}"):
                st.session_state['edit_id'] = row['_id']
                st.session_state['page'] = 'edit_restaurant'
                st.experimental_rerun()
            if col2.button(f"Apagar", key=f"delete_{row['_id']}"):
                try:
                    delete_response = requests.delete(f"http://127.0.0.1:5000/restaurantes/{row['_id']}")
                    if delete_response.status_code == 200:
                        st.success("Restaurante removido com sucesso")
                        st.experimental_rerun()
                    else:
                        st.error("Falha ao remover restaurante")
                except Exception as e:
                    st.error(f"Erro ao conectar: {str(e)}")
else:
    st.warning("Nenhum restaurante encontrado com esses filtros")
