import streamlit as st
from streamlit_searchbox import st_searchbox

# Mandar email para solcitar um novo genero
generos = ['a', 'abra', 'kadabra', 'alakazam']

# def buscar_genero(termo: str) -> List[any]:

def search_wikipedia(searchterm: str) -> list[any]:
    return [term for term in generos if searchterm in term] if searchterm else []

teste = st_searchbox(search_wikipedia, key="wiki_searchbox", placeholder="Buscar restaurante...")