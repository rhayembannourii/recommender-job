# import streamlit as st
# import pandas as pd
from streamlit_option_menu import option_menu
from processing_resume import *
from data_base import *
# import pdfplumber
# import streamlit.components.v1 as components
# import folium
# from streamlit_folium import st_folium
# from folium.plugins import Draw
from visualization import *

st.set_page_config(layout="wide")

if "job_clicked" not in st.session_state:
    st.session_state.job_clicked = False


def job_clicked():
    st.session_state.job_clicked = True


# if "map_clicked" not in st.session_state:
#     st.session_state.map_clicked=False
#
# def map_clicked():
#     st.session_state.map_clicked = True


if 'text_file' not in st.session_state:
    st.session_state.text_file = None

# if "upload_file_check" not in st.session_state:
#     st.session_state.upload_file_check=None

selected = option_menu(
    menu_title="Main Menu",
    options=['Recommended jobs', 'Vizualization'],
    icons=["books", "gear"],
    menu_icon='cast',
    default_index=0,
    orientation="horizontal"
)


def job():
    st.subheader('Job Recommendation System')
    job_desc = get_All_collections()
    phrases, _ = upload_file()
    recomend_job, scores = compute_similarity(phrases, job_desc)

    data = job_desc[job_desc["Key Skills"].isin(recomend_job)]
    # st.session_state.text_file = data
    cordiante = data[['Latitude', 'Longitude']]
    cordiante.columns = ['lat', 'lon']
    cordiante = cordiante.astype({'lat': 'float', 'lon': 'float'})
    st.session_state.text_file = cordiante

    submit_button = st.button(label='Get Recommended Jobs', on_click=job_clicked)
    # submit_button = st.form_submit_button(label='Get Recommended Jobs', on_click=job_clicked)
    # st.subheader('Your Resume Summary:')
    if submit_button:  # or st.session_state.job_clicked :
        st.subheader("Your potentiels offers")
        for i in range(len(data)):
            st.markdown(f'<h1 style="color:#f9d200;font-size:34px;">{data["Job Title"].iloc[i]}</h1>',
                        unsafe_allow_html=True)
            st.write("Role needed : " + str(data["Role"].iloc[i]))
            st.write("Experience required : " + data["Job Experience Required"].iloc[i])
            st.write("Key skills : " + data["Key Skills"].iloc[i])
            st.write("Avarage salary : " + str(data["sal"].iloc[i]))
            st.write("Location  : " + str(data["Location"].iloc[i]))


if selected == 'Recommended jobs':
    job()

if selected == 'Vizualization':
    "## The jobs visualization"

    b = st.session_state.text_file
    # st.write(b)
    display_map(b)
