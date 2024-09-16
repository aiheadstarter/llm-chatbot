import os
import openai
import streamlit as st
from langchain.prompts import PromptTemplate

st.title("🦜🔗 Langchain - Blog Outline Generator App")

# 환경변수에서 API 키 읽어오기
openai_api_key = os.getenv('OPENAI_API_KEY')

st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")

# OpenAI API 키를 환경변수로 설정
openai.api_key = openai_api_key

def blog_outline(topic):
    if topic:  # 입력 검증 추가
        # 프롬프트 생성
        template = "As an experienced data scientist and technical writer, generate an outline for a blog about {topic}."
        prompt = PromptTemplate(input_variables=["topic"], template=template)
        prompt_query = prompt.format(topic=topic)

        try:
            # OpenAI의 새로운 Completion API 사용
            response = openai.completions.create(
                model="gpt-4",  # 최신 gpt-4 모델 사용
                messages=[
                    {"role": "system", "content": "You are an experienced data scientist and technical writer."},
                    {"role": "user", "content": prompt_query}
                ]
            )

            # 결과 출력
            result = response['choices'][0]['message']['content']
            return st.info(result)
        
        except Exception as e:
            st.error(f"Error generating response: {e}")

    else:
        st.error("Please enter a valid topic to generate an outline.")  # 오류 메시지 출력

with st.form("myform"):
    topic_text = st.text_input("Enter prompt:", "")
    submitted = st.form_submit_button("Submit")
    if submitted:
        if not openai_api_key:
            st.error("Please add your OpenAI API key to the environment variables.")
        else:
            blog_outline(topic_text)
