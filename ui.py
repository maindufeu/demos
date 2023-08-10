import streamlit as st
import pandas as pd
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests

# FastAPI endpoint
backend = 'http://fastapi:8008/qas/'

def process(context: str, question: str, key: str, server_url: str):

    m = MultipartEncoder(
        fields={'context': context, 'question': question, 'key' : key}
        )
    r = requests.post(server_url,
                      data=m,
                      params=m.fields,
                      headers={'Content-Type': m.content_type},
                      timeout=8000)
    return r

# UI layout

st.title('Framework de entrenamiento semisupervisado')
st.write('''Cargue su documento de relación para empezar el entrenamiento.
         Visit this URL at `:8008/docs` for FastAPI documentation.''')  # description and instructions

uploaded_file = st.file_uploader("Choose a .csv file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    dict = df.groupby('TKT NAME')['OPCIONES'].apply(list).to_dict()
    for i in dict:
        st.write(i)
        found = dict[i]
        correct = st.multiselect(
            'Cuál de las siguientes es correcta',
            found)
        st.write('You selected:', correct)
        refused = list(set(found) - set(correct))
        user_input_context = st.text_area(f"Por qué {options} son correctas:")
        user_input_question = st.text_area(f"Por qué {refused} son correctas:")
        
