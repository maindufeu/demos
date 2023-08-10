
import streamlit as st
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
st.title('Question Answering')
st.write('''Question Answering.
         Visit this URL at `:8008/docs` for FastAPI documentation.''')  # description and instructions

user_input_key = st.text_area("openai key:")
user_input_context = st.text_area("Context:")
user_input_question = st.text_area("Question:")

if st.button('Get Answering'):

    if user_input_context and user_input_question and user_input_key:

        result = process(user_input_context, user_input_question, user_input_key, backend)
        st.write(f'Respuesta:    {result.content}')

    elif user_input_context:
        # handle case with no question
        st.write("Insert question!")

    elif user_input_context:
        # handle case with context
        st.write("Insert context!")

    else:
        # handle case with no question & context
        st.write("Insert context and question!")