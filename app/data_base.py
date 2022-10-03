import pymongo
# from pymongo import MongoClient
import urllib.parse
import pandas as pd
import sqlite3
import streamlit as st


def connect_base():
    # DB Management
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    return cursor, conn


def create_usertable():
    c, _ = connect_base()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')


def login_user(username, password):
    cc, _ = connect_base()
    cc.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = cc.fetchall()
    return data


def add_userdata(username, password):
    c, conn = connect_base()
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', (username, password))
    conn.commit()


def connect_mongo():
    mongo_uri = "mongodb+srv://rhayem:" + urllib.parse.quote(
        "wweraw5W@") + "@cluster0.9elwmya.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(mongo_uri)
    return client


@st.cache(allow_output_mutation=True)
def get_company_data():
    client = connect_mongo()
    result = client['jobs_resume']['jobs'].find()
    df = pd.DataFrame(result)
    df.drop("_id", inplace=True, axis=1)
    df = df.dropna()
    df = df.drop_duplicates(keep=False)
    return df


def query(country, keywords):
    # mongo_uri = "mongodb+srv://rhayem:" + urllib.parse.quote(
    #     "wweraw5W@") + "@cluster0.9elwmya.mongodb.net/?retryWrites=true&w=majority"
    # client = pymongo.MongoClient(mongo_uri)
    client = connect_mongo()
    result = client['jobs_resume']['jobs'].aggregate([  # collection for company
        {
            '$search': {  # stage 1
                #  stage 1  contains an operator(text)
                'text': {
                    # the operator text conatains 3 fields
                    'path': [
                        'industry'
                    ],
                    'query': [
                        ' %s' % keywords
                    ],
                    'fuzzy': {
                        'maxEdits': 2,
                        'prefixLength': 2
                    }
                }
            }
        }, {
            '$project': {  # stage 2
                'Company Name': '$name',
                'Web Site': '$domain',
                'Industry': '$industry',
                'Linkedin': '$linkedin url',
                'City': '$locality',
                'Country': '$country',
                'score': {
                    '$meta': 'searchScore'
                }
            }
        }, {
            '$match': {  # stage 3
                'Country': '%s' % country
            }
        }, {
            '$limit': 10  # stage 4
            # $limit stage to limit the output to 10 results

        }
    ])

    df = pd.DataFrame(result)
    # df.drop("_id",inplace=True, axis=1)
    df = df[['Company Name', 'Web Site', 'Linkedin']]
    df = df.dropna()
    df = df.drop_duplicates(keep=False)
    # df = df.astype({"_id": str})
    return df


# @st.cache(suppress_st_warning=True,persist =True)
def local_mongo():
    mongo_uri = "mongodb://localhost:27017"
    client = pymongo.MongoClient(mongo_uri)
    return client


@st.cache(allow_output_mutation=True)
def get_All_collections(value=True):  # pour la vizualization
    client = local_mongo()
    if value:
        result = client['job_recommender']['job_description'].find()  # job page
    else:
        result = client['job_recommender']['job_desc'].find()  # recruteur page
    df = pd.DataFrame(result)
    df.drop("_id", inplace=True, axis=1)
    df = df.dropna()
    df = df.drop_duplicates(keep=False)
    return df

# @st.cache(suppress_st_warning=True,persist =True)
# def query_local_mongo(skills,keywords):
#     client = local_mongo()
#     result = client['job_recommender']['job_description'].aggregate([
#         {
#             '$search': {  ## stage 1
#                 #  stage 1  contains an operator(text)
#                 'text': {
#                     ## the operator text conatains 3 fields
#                     'path': [
#                         'Key Skills'
#                     ],
#                     'query': [
#                         ' %s' % (keywords)
#                     ],
#                     'fuzzy': {
#                         'maxEdits': 2,
#                         'prefixLength': 2
#                     }
#                 }
#             }
#         }, {
#             '$project': {  ## stage 2
#                 'Company Name': '$name',
#                 'Web Site': '$domain',
#                 'Industry': '$industry',
#                 'Linkedin': '$linkedin url',
#                 'City': '$locality',
#                 'Country': '$country',
#                 'score': {
#                     '$meta': 'searchScore'
#                 }
#             }
#         }, {
#             '$match': {  ## stage 3
#                 'Country': '%s' % (country)
#             }
#         }, {
#             '$limit': 10  ## stage 4
#             # $limit stage to limit the output to 10 results
#
#         }
#     ])
