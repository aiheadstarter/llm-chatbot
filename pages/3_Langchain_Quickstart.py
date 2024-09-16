import os
import streamlit as st
from langchain.llms import OpenAI

st.title("🦜🔗 Langchain Quickstart App")

# 환경변수에서 API 키 읽어오기
openai_api_key = os.getenv('OPENAI_API_KEY')

st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

def generate_response(input_text):
    if openai_api_key:
        llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
        response = llm(input_text)
        st.info(response)
    else:
        st.error("OpenAI API 키를 환경변수에 설정해 주세요.")

with st.form("my_form"):
    text = st.text_area("Enter text:", "What are 3 key advice for learning how to code?")
    submitted = st.form_submit_button("Submit")
    if submitted:
        generate_response(text)
