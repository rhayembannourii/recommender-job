from processing_resume import *
from streamlit_option_menu import option_menu
from data_base import *
import plotly.express as px

# Delete all the items in Session state
# for key in st.session_state.keys():
#     del st.session_state[key]
selected = option_menu(
    menu_title="Main Menu",
    options=['Preferred Candidate'],
    icons=["books", "gear"],
    menu_icon='cast',
    default_index=0,
    orientation="horizontal"
)
if "cover_button" not in st.session_state:
    st.session_state.cover_button = False

if "cover_button2" not in st.session_state:
    st.session_state.cover_button2 = False

if "cover_button3" not in st.session_state:
    st.session_state.cover_button3 = False


def cover_button():
    st.session_state.cover_button = True
    st.session_state.cover_button2 = False
    st.session_state.cover_button3 = False


def cover_button2():
    st.session_state.cover_button2 = True
    st.session_state.cover_button = False
    st.session_state.cover_button3 = False


def cover_button3():
    st.session_state.cover_button3 = True
    st.session_state.cover_button = False
    st.session_state.cover_button2 = False



def display_job(i=0):
    st.markdown(f'<h1 style="color:#f9d200;font-size:34px;">Job Summary Number {i + 1}</h1>',
                unsafe_allow_html=True)
    st.write(list_job_desc_summary[i])


def test_skills(p=0):
    button_test = st.button(label='Send Code', key=f'teste{p}')
    if button_test:
        send_test()


resume_recommender = []
df = None
cover_summary = None
covers_recommender = None


def find_person(j=0):
    global resume_recommender
    resume_recommender, _ = job_desc_similarity(list_job_desc_summary[j], resume_summary, 4)  # list
    global df
    df = cover_resume_summary[cover_resume_summary['Resume'].isin(resume_recommender)]
    global cover_summary
    cover_summary = df['Cover'].values.tolist()
    global covers_recommender
    covers_recommender, _ = job_desc_similarity(list_job_desc_summary[j], cover_summary, 2)


def rec_cover(p=0):
    st.markdown(f'<h1 style="color:#00ecf9;font-size:28px;">Cover  Number {p + 1}</h1>',
                unsafe_allow_html=True)
    st.write(covers_recommender[p])

    st.markdown(f'<h1 style="color:#7A00F9;font-size:24px;">Skills</h1>',
                unsafe_allow_html=True)
    resume_skills = df[df['Cover'] == covers_recommender[p]]
    skills = resume_skills['Resume'].values.tolist()
    st.markdown(f'<h1 style="color:#000000;font-size:20px;">{skills}\n</h1>',
                unsafe_allow_html=True)
    _, data = summary_job_desc(longe=3)
    description_data = data['FullDescription'].values.tolist()
    recommender_desc, scores = job_desc_similarity(skills, description_data, 5)
    dataf = data[data['FullDescription'].isin(recommender_desc)]
    dataf['Score'] = scores
    title_score = dataf[['Title', 'Score']]
    fig = px.bar(title_score.sort_values(by='Score'), x='Score', y='Title',
                 width=1000)
    st.write(fig)


if selected == 'Preferred Candidate':
    cover_resume_summary = get_cover_resume_summary()  # return data frame with summary of resume and cover
    resume_summary = cover_resume_summary['Resume'].values.tolist()  # output list of resume
    list_job_desc_summary, _ = summary_job_desc(longe=3)  # 3 jobs description

    display_job(i=0)
    button1 = st.button(label='Find Candidats', key=f'button{0}', on_click=cover_button)
    # cover_button()
    if button1 or st.session_state.cover_button:
        find_person(j=0)
        rec_cover(p=0)

        button_test1 = st.button(label='Send Code', key=f'teste{0}')

        if button_test1:
            send_test()

        rec_cover(p=1)
        button_test2 = st.button(label='Send Code', key=f'teste{1}')
        if button_test2:
            send_test()

    display_job(i=1)
    button2 = st.button(label='Find Candidats', key=f'button{1}', on_click=cover_button2)
    if button2 or st.session_state.cover_button2:
        # del st.session_state["cover_button"]
        find_person(j=1)
        rec_cover(p=0)
        button_test1 = st.button(label='Send Code', key=f'teste{0}')
        if button_test1:
            send_test()

        rec_cover(p=1)
        button_test2 = st.button(label='Send Code', key=f'teste{1}')
        if button_test2:
            send_test()

    display_job(i=2)
    button3 = st.button(label='Find Candidats', key=f'button{2}', on_click=cover_button3)
    if button3 or st.session_state.cover_button3:
        find_person(j=2)
        rec_cover(p=0)
        button_test1 = st.button(label='Send Code', key=f'teste{0}')
        if button_test1:
            send_test()

        rec_cover(p=1)
        button_test2 = st.button(label='Send Code', key=f'teste{1}')
        if button_test2:
            send_test()
