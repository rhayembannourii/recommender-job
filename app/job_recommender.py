# import io
# import streamlit as st
# import pymongo
# from pymongo import MongoClient
# import pandas as pd
# import pdfplumber
# # import PyPDF2
# # import lxml
# from processing_resume import *
# from data_base import *
# # import nltk
# # import uvicorn
#
# def job_recommender() :
#     st.subheader('Job Recommendation System')
#     # st.title('Job Recommendation System')
#     # country=st.sidebar.text_input('Country')
#     countries = (
#         "turkey", "trinidad and tobago", "macau", "poland", "colombia", "hong kong", "saudi arabia",
#         "uruguay", "united states", "mozambique", "singapore", "armenia", "romania", "albania",
#         "guernsey", "moldova", "lesotho", "liberia", "tajikistan", "maldives", "denmark", "algeria",
#         "ecuador", "gibraltar", "egypt", "azerbaijan", "kenya", "brazil", "norway", "ukraine",
#         "côte d’ivoire", "fiji", "mongolia", "south africa", "mexico", "czechia", "italy", "spain",
#         "réunion", "rwanda", "burkina faso", "senegal", "swaziland", "gambia", "bangladesh", "ethiopia",
#         "nigeria", "dominican republic", "nicaragua", "montenegro", "south sudan", "argentina", "curaçao",
#         "Åland islands", "united kingdom", "san marino", "cambodia", "luxembourg", "pakistan", "austria",
#         "hungary", "iraq", "bahrain", "netherlands antilles", "puerto rico", "andorra", "cuba", "sudan",
#         "morocco", "georgia", "slovakia", "bhutan", "philippines", "mauritius", "british virgin islands",
#         "japan", "ireland", "isle of man", "guadeloupe", "ghana", "grenada", "lebanon", "netherlands",
#         "venezuela", "equatorial guinea", "dominica", "macedonia", "democratic republic of the congo",
#         "laos", "saint vincent and the grenadines", "israel", "kazakhstan", "slovenia", "new zealand",
#         "sri lanka", "sweden", "qatar", "estonia", "myanmar", "tunisia", "indonesia", "guam", "libya", "canada",
#         "guatemala", "botswana", "belarus", "djibouti", "yemen", "niger", "bermuda", "south korea", "lithuania",
#         "guyana", "jordan", "malaysia", "monaco", "aruba", "greece", "thailand", "germany", "belize",
#         "bosnia and herzegovina", "cayman islands", "madagascar", "kuwait", "kyrgyzstan", "angola",
#         "cameroon", "tanzania", "switzerland", "el salvador", "croatia", "china", "malta", "vietnam",
#         "cyprus", "togo", "american samoa", "chile", "jamaica", "costa rica", "paraguay", "french guiana",
#         "france", "russia", "uzbekistan", "bolivia", "finland", "brunei", "australia", "united arab emirates",
#         "somalia", "palestine", "nepal", "peru", "portugal", "india", "iceland", "micronesia", "bulgaria",
#         "malawi", "honduras", "french polynesia", "uganda", "latvia", "zambia", "afghanistan", "mali",
#         "marshall islands", "new caledonia", "iran", "benin", "suriname", "taiwan", "serbia",
#         "papua new guinea", "syria", "bahamas", "greenland", "belgium", "sierra leone", "guinea",
#         "martinique", "jersey", "liechtenstein", "panama", "oman", "saint lucia", "namibia", "zimbabwe"
#     )
#
#     country = st.selectbox(
#         'Select Country ', countries)
#
#     phrases,_=upload_file()
#     if len(phrases) > 0:
#         q_terms = st.multiselect('Select key phrases', options=phrases, default=phrases)
#         # st.write(phrases)
#         # st.write(file_text)
#
#     if st.button('Search'):
#         df = query(country, phrases)
#         st.write(df)
#
#     _,cover_letter = upload_file(value=False)
#     if len(cover_letter)> 0:
#         cover_summary = summary_cover(cover_letter)
#         st.write(cover_summary)
#
#
#
#
