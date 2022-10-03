from streamlit_option_menu import option_menu
import webbrowser
from processing_resume import *
from data_base import *
from visualization import *
from data_base import query

# import nltk
# import uvicorn

if "site_clicked" not in st.session_state:
    st.session_state.site_clicked = False


def site_clicked():
    st.session_state.site_clicked = True


if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False


def form_callback():
    st.session_state.button_clicked = True


country = ''


# @st.cache(suppress_st_warning=True,persist =True)
def selct_country():
    countries = (
        "turkey", "trinidad and tobago", "macau", "poland", "colombia", "hong kong", "saudi arabia",
        "uruguay", "united states", "mozambique", "singapore", "armenia", "romania", "albania",
        "guernsey", "moldova", "lesotho", "liberia", "tajikistan", "maldives", "denmark", "algeria",
        "ecuador", "gibraltar", "egypt", "azerbaijan", "kenya", "brazil", "norway", "ukraine",
        "côte d’ivoire", "fiji", "mongolia", "south africa", "mexico", "czechia", "italy", "spain",
        "réunion", "rwanda", "burkina faso", "senegal", "swaziland", "gambia", "bangladesh", "ethiopia",
        "nigeria", "dominican republic", "nicaragua", "montenegro", "south sudan", "argentina", "curaçao",
        "Åland islands", "united kingdom", "san marino", "cambodia", "luxembourg", "pakistan", "austria",
        "hungary", "iraq", "bahrain", "netherlands antilles", "puerto rico", "andorra", "cuba", "sudan",
        "morocco", "georgia", "slovakia", "bhutan", "philippines", "mauritius", "british virgin islands",
        "japan", "ireland", "isle of man", "guadeloupe", "ghana", "grenada", "lebanon", "netherlands",
        "venezuela", "equatorial guinea", "dominica", "macedonia", "democratic republic of the congo",
        "laos", "saint vincent and the grenadines", "israel", "kazakhstan", "slovenia", "new zealand",
        "sri lanka", "sweden", "qatar", "estonia", "myanmar", "tunisia", "indonesia", "guam", "libya", "canada",
        "guatemala", "botswana", "belarus", "djibouti", "yemen", "niger", "bermuda", "south korea", "lithuania",
        "guyana", "jordan", "malaysia", "monaco", "aruba", "greece", "thailand", "germany", "belize",
        "bosnia and herzegovina", "cayman islands", "madagascar", "kuwait", "kyrgyzstan", "angola",
        "cameroon", "tanzania", "switzerland", "el salvador", "croatia", "china", "malta", "vietnam",
        "cyprus", "togo", "american samoa", "chile", "jamaica", "costa rica", "paraguay", "french guiana",
        "france", "russia", "uzbekistan", "bolivia", "finland", "brunei", "australia", "united arab emirates",
        "somalia", "palestine", "nepal", "peru", "portugal", "india", "iceland", "micronesia", "bulgaria",
        "malawi", "honduras", "french polynesia", "uganda", "latvia", "zambia", "afghanistan", "mali",
        "marshall islands", "new caledonia", "iran", "benin", "suriname", "taiwan", "serbia",
        "papua new guinea", "syria", "bahamas", "greenland", "belgium", "sierra leone", "guinea",
        "martinique", "jersey", "liechtenstein", "panama", "oman", "saint lucia", "namibia", "zimbabwe"
    )
    global country
    country = st.selectbox(
        'Select Country ', countries)


# @st.cache(suppress_st_warning=True,persist =True)

df = pd.DataFrame(columns=['Company Name', 'Web Site', 'Linkedin'])


def query_call(x, y):
    global df
    df = query(x, y)


selected = option_menu(
    menu_title="Main Menu",
    options=['Recommended Companies', 'Vizualization'],
    icons=["books", "gear"],
    menu_icon='cast',
    default_index=0,
    orientation="horizontal"
)

if selected == 'Recommended Companies':
    st.subheader('Company Recommendation System')

    col1, col2 = st.columns([8, 6])
    with col1:
        with st.form(key='my_form'):
            phrases, _ = upload_file()

            selct_country()

            submit_button = st.form_submit_button(label='Search', on_click=form_callback)
        if submit_button or st.session_state.button_clicked:
            # df = query(country, phrases)
            query_call(country, phrases)
            # st.write(df['Company Name'])
    with col2:

        with st.form(key='my_form22'):
            site = st.selectbox(
                'The appropriate companies ', options=[site for site in df['Web Site'].values])

            button_site = st.form_submit_button(label='visit Web site')  # ,on_click=site_clicked
        if button_site:  # or st.session_state.site_clicked
            webbrowser.open_new(site)

    with st.form(key='my_form3'):
        linkedin = st.selectbox(
            'linekedin Profiles', options=[linkedin for linkedin in df['Linkedin'].values])

        button_linkedin = st.form_submit_button(label='Visit linkedin profile')
    if button_linkedin:
        webbrowser.open_new(linkedin)

if 'data_company' not in st.session_state:
    st.session_state.data_company = None

data = get_company_data()
st.session_state.data_company = data

if selected == 'Vizualization':
    companies = st.session_state.data_company
    top_industries(companies)
    company_size(companies)
    top_countries(companies)

    it_companies(companies)
