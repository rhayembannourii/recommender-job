import string
import spacy
from keybert import KeyBERT
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import pdfplumber
from sentence_transformers import SentenceTransformer, util  # , InputExample, losses
import os
from data_base import *
from email.message import EmailMessage
import ssl
import smtplib
import en_core_web_sm

# path = r"C:\Users\rhayem\AppData\Local\Programs\Python\Python39\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.4.0"
# nlp = spacy.load(path)
nlp = en_core_web_sm.load()


# function to clean the data
@st.cache(suppress_st_warning=True, persist=True)
def clean_data(data):
    # path = r"C:\Users\rhayem\AppData\Local\Programs\Python\Python39\Lib\site-packages" \
    #        r"\en_core_web_sm\en_core_web_sm-3.4.0"
    # nlp = spacy.load(path)
    nlp = en_core_web_sm.load()
    data = ' '.join(str(k) for k in nlp(data) if str(k) not in string.punctuation)
    # remove stop words , punct , space, and extract root words
    data = ' '.join([str(k.lemma_.lower()) for k in nlp(data) if not k.is_punct and not k.is_stop and not k.is_space
                     and not k.like_url and not k.like_num and k.is_alpha and not k.is_digit
                     and not k.is_currency and not k.like_email])
    # POS
    data = ' '.join(str(w) for w in nlp(data) if w.pos_ in ['PRON', 'NOUN', 'PROPN'])
    return data


@st.cache(suppress_st_warning=True)
def key_words_extraction(text):
    text = clean_data(text)
    kw_model = KeyBERT(model='all-MiniLM-L6-v2')
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(5, 8),
                                         stop_words='english', use_maxsum=True, nr_candidates=25, top_n=5)
    list_keywords = [key[0] for key in keywords]
    # list_keywords=' '.join(list_keywords)
    return list_keywords


@st.cache(suppress_st_warning=True)
def summary_cover(cover):
    # save_directory = './saved'
    # tokenizer = AutoTokenizer.from_pretrained(save_directory)
    # model = AutoModelForSeq2SeqLM.from_pretrained(save_directory)
    # classifier = pipeline("summarization", model=model, tokenizer=tokenizer)
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    summary = summarizer(cover, max_length=200, min_length=100, do_sample=False)
    # summary = classifier(cover, max_length=200, min_length=100, do_sample=False)
    # max_length=100, min_length=40
    return summary[0]['summary_text']


if "file_uploaded" not in st.session_state:
    st.session_state.file_uploaded = False


def change_file():
    st.session_state.file_uploaded = True


def upload_file(value=True):
    file_name = 'resume'
    if not value:
        file_name = 'cover letter'
    file_text = ''
    phrases = []
    try:
        uploaded_file = st.file_uploader(f'Please Upload your {file_name} ')  # return UploadedFile object.
        # , on_change = change_file
    except:
        st.write('File is empty')
    if uploaded_file:
        uploaded_file.seek(0)
        with pdfplumber.open(uploaded_file) as pdf:
            # The open method returns an instance of the pdfplumber.PDF class.
            pages = pdf.pages
            for page in pages:
                file_text += page.extract_text()
                if value:
                    phrases.extend(key_words_extraction(file_text))
                else:
                    phrases.extend(file_text)

    return phrases, file_text  # phrases ,


# def resume_jobs_cleaned(resume,jobs):
#   """
#   function to clean the data and split it .
#
#   """
#   ## clean the resume
#   resume=resume['Resume'].apply(str)
#   resume=resume.apply(key_words_extraction)
#   resume=pd.DataFrame(data=resume,columns=['Resume'])
#
#   ## clean the job
#   jobs=jobs['FullDescription'].apply(str)
#   jobs=jobs.apply(key_words_extraction)
#   jobs=pd.DataFrame(data=jobs,columns=['FullDescription'])
#
#   return resume , jobs

# resume,jobs =resume_jobs_cleaned(resume,jobs)

if "similarity" not in st.session_state:
    st.session_state.similarity = False


def compute_similarity(resume, jobs, top_jobs=5):
    """
  function to compute the similarity between the resume
  and the jobs then returns the top jobs
  """
    jobs_recommender = []
    scores = []
    jobs.drop(jobs[jobs['Key Skills'] == 'vide'].index, inplace=True)
    model = SentenceTransformer('all-MiniLM-L6-v2')
    Jobs = jobs['Key Skills'].values.tolist()
    Jobs = model.encode(Jobs, convert_to_tensor=True)
    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    # Resume=resume['Resume'].values.tolist()
    if resume:
        skills = ' '.join(resume)
        skills_embeddings = model.encode(skills, convert_to_tensor=True)
        hits = util.semantic_search(skills_embeddings, Jobs, top_k=5)[0]
        for hit in hits:
            jobs_recommender.append(jobs['Key Skills'].iloc[hit["corpus_id"]])
            scores.append(hit["score"])
    return jobs_recommender, scores


################## Recruteur Page #########################
# @st.cache(suppress_st_warning=True)
def get_cover_resume_path():
    """
    return data frame contains full path for cover and resume
    """
    # cover_dir = os.path.join("C:\/Users\/rhayem\PycharmProjects\Job_Recommender\/app\condidatures")
    cover_dir = os.path.join("./condidatures")
    condidate_dir = os.listdir(cover_dir)  # output ['condidat0', 'condidat1', 'condidat2', 'condidat3', 'condidat4']

    list_cond = dict()
    for cond in condidate_dir:
        cond_path = os.path.join(cover_dir, cond)  # exp C:\/Users\p\OneDrive\Bureau\job\/app\condidatures\condidat0
        cond_files = os.listdir(cond_path)  ## output : list of files in each condidature folder
        ## exp : resume1 and cover 1
        list_cond[os.path.join(cond_path, cond_files[0])] = list_cond.get(os.path.join(cond_path, cond_files[0]),
                                                                          os.path.join(cond_path, cond_files[1]))
    data = pd.DataFrame(list_cond.items(), columns=['Cover', 'Resume'])
    a = data.iloc[1][0]
    data.iloc[1][0] = data.iloc[1][1]
    data.iloc[1][1] = a
    return data


# @st.cache(suppress_st_warning=True)
def open_file(pathe):
    # phrases = []
    file_text = ''
    with pdfplumber.open(pathe) as pdf:
        pages = pdf.pages
        for page in pages:
            file_text += page.extract_text()
    # phrases.append(file_text)
    return file_text


# @st.cache(suppress_st_warning=True)
def summary_cover_and_resume(pathe):
    # phrases = []
    # file_text = ''
    # with pdfplumber.open(pathe) as pdf:
    #     pages = pdf.pages
    #     for page in pages:
    #         file_text += page.extract_text()
    # phrases.append(file_text)
    file = open_file(pathe)
    # summary = [summary_cover(file) for file in phrases]
    summary = summary_cover(file)
    return summary


# @st.cache(suppress_st_warning=True,persist =True)
def get_skills(pathe):
    # path = r"C:\Users\rhayem\AppData\Local\Programs\Python\Python39\Lib\site-packages\en_core_web_sm\en_core_web_sm-3.4.0"
    # nlp = spacy.load(path)
    nlp = en_core_web_sm.load()
    # skill_pattern_path = r"C:\Users\rhayem\PycharmProjects\Job_Recommender\app\jz_skill_patterns.jsonl"
    skill_pattern_path = "./jz_skill_patterns.jsonl"
    ruler = nlp.add_pipe("entity_ruler")
    ruler.from_disk(skill_pattern_path)

    data = open_file(pathe)
    data = ' '.join(str(k.lemma_.upper()) for k in nlp(data) if not k.is_punct and not k.is_stop
                    )
    doc = nlp(data)
    myset = []
    subset = []
    for ent in doc.ents:
        if ent.label_ == "SKILL":
            subset.append(ent.text)
    myset.append(subset)

    subset = list(set(subset))
    subset = ','.join(subset)
    return subset


# @st.cache(suppress_st_warning=True)
def get_cover_resume_summary():
    data = get_cover_resume_path()
    data['Cover'] = data['Cover'].map(summary_cover_and_resume)
    data['Resume'] = data['Resume'].map(get_skills)
    return data


##################### Recruteur Page ######################################
# @st.cache(suppress_st_warning=True)
def summary_job_desc(longe=3):
    """
    return the summarazation of the jobs
    """
    jobs = get_All_collections(False)  # return dataframe
    # jobs=jobs.sample(n=longe)
    # st.write(jobs['FullDescription'])
    full_desc = jobs['FullDescription'].iloc[8:longe + 8].apply(summary_cover)
    job_title_nd_desc = jobs[['Title', 'FullDescription']].iloc[0:20]
    job_title_nd_desc['FullDescription'] = job_title_nd_desc['FullDescription'].apply(summary_cover)
    return full_desc.values.tolist(), job_title_nd_desc


def send_test():
    email_sender = "rhayembannouri1@gmail.com"
    email_password = "tqfxsyzutdzwugjr"
    email_receiver = "rhayembannouri5@gmail.com"

    subject = "Your Python test"
    body = """
    Question 1/5 : Python
    Barème : bonne réponse 4 points, mauvaise réponse -0,5 point, je ne sais pas 0 point
    
    
    n = 0
    while n<15 :
        n = n + 2
    print(n)
    
    Qu'affiche le script ?
    
    Je ne sais pas
    A) 14
    B) 15
    C) 16
    D) 17 
    
    
    Question 2/5 : Python
    
    Barème : bonne réponse 4 points, mauvaise réponse -0,5 point, je ne sais pas 0 point
    
    
    n = 10
    while n>=11 :
        n = n + 2
    print(n)
    
    Qu'affiche le script ?
    
    Je ne sais pas
    A) 10
    B) 11
    C) 12
    D) 13
    
    Question 3/5 : Python
    
    Barème : bonne réponse 4 points, mauvaise réponse -0,5 point, je ne sais pas 0 point
    
    
    n = 0
    for i in range(5) :
        n = n + 1
    print(n)
    
    Qu'affiche le script ?
    
    Je ne sais pas
    A) 4
    B) 5
    C) 6
    D) 7
    
    Question 4/5 : Python
    
    Barème : bonne réponse 4 points, mauvaise réponse -0,5 point, je ne sais pas 0 point
    
    
    n = 0
    for i in range(5) :
        n = n + 1
    print(i)
    
    Qu'affiche le script ?
    
    Je ne sais pas
    A) 4
    B) 5
    C) 6
    D) 7
    
    Question 5/5 : Python
    
    Barème : bonne réponse 4 points, mauvaise réponse -1 point, je ne sais pas 0 point
    
    
    resultat = ""
    for c in "Bonsoir" :
        resultat = resultat + c
    print(resultat)
    
    Qu'affiche le script ?
    
    Je ne sais pas
    A) Bonsoir
    B) riosnoB
    C) BonsoirBonsoirBonsoirBonsoirBonsoirBonsoirBonsoir
    
    
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


# @st.cache(suppress_st_warning=True,persist =True)
def job_desc_similarity(description, cover_letters, top_k=3):  # description text
    # cover_letters list
    cover_recommender = []
    scores = []
    model = SentenceTransformer('all-MiniLM-L6-v2')
    cover_encode = model.encode(cover_letters, convert_to_tensor=True)
    description_embeddings = model.encode(description, convert_to_tensor=True)

    hits = util.semantic_search(description_embeddings, cover_encode, top_k=top_k)[0]  # , top_k=4
    for hit in hits:
        cover_recommender.append(cover_letters[hit["corpus_id"]])
        scores.append(hit["score"])
    return cover_recommender, scores
