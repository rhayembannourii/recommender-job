import streamlit as st
from streamlit import _RerunData, _RerunException
from streamlit.source_util import get_pages
from streamlit_option_menu import option_menu


def switch_page(page_name: str):
    def standardize_name(name: str) -> str:
        return name.lower().replace("_", " ")

    page_name = standardize_name(page_name)

    pages = get_pages("main.py")  # OR whatever your main page is called

    for page_hash, config in pages.items():
        if standardize_name(config["page_name"]) == page_name:
            raise _RerunException(
                _RerunData(
                    page_script_hash=page_hash,
                    page_name=page_name,
                )
            )

    page_names = [standardize_name(config["page_name"]) for config in pages.values()]

    raise ValueError(f"Could not find page {page_name}. Must be one of {page_names}")


def main():
    st.title("Welcome to Job Recommender System")
    st.subheader("Home")
    choice = option_menu(None, ['home', "Signup", "Login"],
                         icons=['house', "Tasks", "gear"],
                         menu_icon="cast", default_index=0, orientation="horizontal")
    if choice == 'home':
        return 0
    if choice == "Signup":
        switch_page('signup')

    if choice == "Login":
        switch_page('login')


if __name__ == '__main__':
    main()
