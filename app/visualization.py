import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import Draw
import plotly.express as px
import numpy as np
import geotext  # extracting "cities"


def display_map(data):
    m = folium.Map(location=data.values.tolist()[0])
    Draw(export=True).add_to(m)
    for i in range(len(data)):
        folium.Marker(location=data.values.tolist()[i], tooltip=f'Hi{i}').add_to(m)

    c1, c2 = st.columns(2)
    with c1:
        output = st_folium(m, width=700, height=500)

    with c2:
        st.write(output)


def top_industries(companies):
    st.subheader('Top 10 industries with many companies')
    counts_df = companies['industry'].value_counts().rename_axis('industry').reset_index(name='count')
    fig = px.bar(counts_df.nlargest(10, "count").sort_values(by='count'), x="count", y="industry",
                 width=1000)  # , title='Top 10 industries with many companies'
    st.write(fig)


def company_size(companies):
    st.subheader('Distribution of companies size range')
    fig = px.pie(companies, names='size range', width=1000)  # ,column='size range',
    st.write(fig)


def top_countries(companies):
    """
    display country with the most company
    """
    st.subheader('Top 10 countries with many companies')
    counts_df = companies['country'].value_counts().rename_axis('country').reset_index(name='count')
    fig = px.bar(counts_df.nlargest(10, 'count').sort_values(by='count'), x='count', y='country',
                 width=1000)  # , title='Top 10 industries with many companies'
    # fig.update_layout(width=800)
    st.write(fig)


def get_city(x: str) -> str:
    geo = geotext.GeoText(x).cities
    if len(geo) > 0:
        return geo[0]
    return x.split(',')[0]  # first part of the text as a possible city


def it_companies(companies):
    """
    Count of IT companies By countries
    """
    companies.dropna(subset=['name', 'industry', 'country'], inplace=True)
    companies['locality'].fillna('missing', inplace=True)
    df_companies = companies[companies['current employee estimate'].apply(np.int64) > 0]
    df_companies.locality = df_companies.locality.str.title()
    df_companies.country = df_companies.country.str.title()

    df_companies['city'] = df_companies.locality.map(get_city)
    df_companies['country_city'] = df_companies['country'] + '; ' + df_companies['city']
    IT_industries = [
        'animation',
        'biotechnology',
        'computer & network security',
        'computer games',
        'computer hardware',
        'computer networking',
        'computer software',
        'consumer electronics',
        'defense & space',
        'e-learning',
        'industrial automation',
        'information services',
        'information technology and services',
        'internet',
        'mechanical or industrial engineering',
        'program development',
        'telecommunications',
        'wireless'
    ]
    it_frame = df_companies[df_companies.industry.isin(IT_industries)]

    # it_cities = it_frame[it_frame.city != 'Missing'].country_city.value_counts().sort_values(ascending=False) \
    #     .reset_index().rename(columns={'index': 'country_city', 'country_city': 'count'})

    it_counted = it_frame[['country', 'name']].groupby(['country', ], as_index=False).count().rename(
        columns={'name': 'count'})
    it_counted.sort_values(by='count', ascending=False).reset_index(drop=True)

    fig = px.choropleth(it_counted,
                        locations='country',
                        locationmode='country names',
                        color='count',
                        color_continuous_scale='twilight'
                        # animation_frame=it_counted['country']
                        )

    fig.update_layout(title='Count of IT companies by countries',
                      title_x=0.5,
                      title_font=dict(size=22, family='Balto', color='DarkSlateBlue'),
                      geo=dict(showframe=False,
                               showcoastlines=True,
                               projection_type='natural earth'))
    st.write(fig)
