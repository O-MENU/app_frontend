import streamlit as st
from pages import restaurantes, usuarios

PAGES = {
    "usuarios": usuarios,
    "restaurante": restaurantes
}


def main():
    st.sidebar.title("Navegação")
    selection = st.sidebar.radio("Escolha uma página:", list(PAGES.keys()))

    page = PAGES[selection]
    page.app()

if __name__ == "__main__":
    main()