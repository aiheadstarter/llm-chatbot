from openai import OpenAI
import streamlit as st
from streamlit_feedback import streamlit_feedback
import trubrics
import os

st.title("📝 Chat with feedback (Trubrics)")

# 환경변수에서 API 키 및 Trubrics 자격 증명 읽어오기
openai_api_key = os.getenv('OPENAI_API_KEY')
trubrics_email = os.getenv('TRUBRICS_EMAIL')
trubrics_password = os.getenv('TRUBRICS_PASSWORD')

st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
st.sidebar.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/5_Chat_with_user_feedback.py)")
st.sidebar.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "How can I help you? Leave feedback to help me improve!"}
    ]

messages = st.session_state.messages
for msg in messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="Tell me a joke about sharks"):
    messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.error("Please add your OpenAI API key in the environment variables.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    st.session_state["response"] = response.choices[0].message.content
    with st.chat_message("assistant"):
        messages.append({"role": "assistant", "content": st.session_state["response"]})
        st.write(st.session_state["response"])

if st.session_state["response"]:
    feedback = streamlit_feedback(
        feedback_type="thumbs",
        optional_text_label="[Optional] Please provide an explanation",
        key=f"feedback_{len(messages)}",
    )
    if feedback and trubrics_email and trubrics_password:
        config = trubrics.init(email=trubrics_email, password=trubrics_password)
        collection = trubrics.collect(
            component_name="default",
            model="gpt",
            response=feedback,
            metadata={"chat": messages},
        )
        trubrics.save(config, collection)
        st.toast("Feedback recorded!", icon="📝")
