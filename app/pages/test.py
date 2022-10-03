# import streamlit as st
# import spacy
# import pdfplumber
# import nltk
# import warnings
#
# nltk.download(['stopwords', 'wordnet'])
#
# warnings.filterwarnings('ignore')
#
# def get_file():
#     file_text = ''
#     phrases = []
#     uploaded_file = st.file_uploader(f'Please Upload your resume ')
#     if uploaded_file:
#         uploaded_file.seek(0)
#         with pdfplumber.open(uploaded_file) as pdf:
#             # The open method returns an instance of the pdfplumber.PDF class.
#             pages = pdf.pages
#             for page in pages:
#                 file_text += page.extract_text()
#                 phrases.append(file_text)
#     return file_text
#
#
# def clean_data(data):
#     path = r"C:\Users\p\AppData\Local\Programs\Python\Python39\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.4.0"
#     nlp = spacy.load(path)
#     skill_pattern_path = r"C:\Users\p\OneDrive\Bureau\job\app\jz_skill_patterns.jsonl"
#     ruler = nlp.add_pipe("entity_ruler")
#     ruler.from_disk(skill_pattern_path)
#
#     data = ' '.join(str(k.lemma_.upper()) for k in nlp(data) if not k.is_punct and not k.is_stop
#                     )
#     doc = nlp(data)
#     myset = []
#     subset = []
#     for ent in doc.ents:
#         if ent.label_ == "SKILL":
#             subset.append(ent.text)
#     myset.append(subset)
#
#     subset = list(set(subset))
#     return subset
#
#
# file_text = get_file()
# skills = clean_data(file_text)
# st.write(skills)
