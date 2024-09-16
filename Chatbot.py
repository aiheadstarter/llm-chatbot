from openai import OpenAI
import streamlit as st
import os

# 환경변수에서 API 키 읽어오기
openai_api_key = os.getenv('OPENAI_API_KEY')

st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
st.sidebar.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
st.sidebar.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

st.title("💬 온라인 마케팅 전문 챗봇")
st.caption("🚀 한국광고연구소(Kiad)를 위한 Streamlit 챗봇")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "어떻게 도와드릴까요? 온라인 마케팅에 대한 궁금한 점을 물어보세요."}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.error("OpenAI API 키를 환경변수에 설정해 주세요.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
