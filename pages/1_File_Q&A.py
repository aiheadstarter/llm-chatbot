import streamlit as st
import anthropic
import os
from dotenv import load_dotenv
import PyPDF2

# .env 파일 로드
load_dotenv()

# 환경변수에서 API 키 읽어오기
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')

st.sidebar.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/1_File_Q%26A.py)")
st.sidebar.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

st.title("📊 마케팅 자료 Q&A")
uploaded_file = st.file_uploader("마케팅 자료를 업로드하세요.", type=("txt", "md", "pdf"))
question = st.text_input(
    "자료에 대한 질문을 입력하세요.",
    placeholder="이 자료의 주요 내용은 무엇입니까?",
    disabled=not uploaded_file,
)

# 파일 내용 읽기 함수 (PDF 및 텍스트 파일 처리)
def read_file(file):
    if file.type == "application/pdf":
        # PDF 파일 읽기
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    else:
        # 텍스트 파일 읽기
        return file.read().decode()

# Anthropic API 키가 없을 경우 오류 메시지 출력
if uploaded_file and question and not anthropic_api_key:
    st.error("Anthropic API 키를 환경변수에 설정해 주세요.")

# 파일과 질문이 있고 Anthropic API 키가 설정된 경우 실행
if uploaded_file and question and anthropic_api_key:
    article = read_file(uploaded_file)  # 파일 읽기 함수로 변경
    
    # 대화 형식으로 프롬프트 수정
    prompt = f"\n\nHuman: {article}\n\nQuestion: {question}\n\nAssistant:"

    client = anthropic.Client(api_key=anthropic_api_key)
    response = client.completions.create(
        prompt=prompt,
        stop_sequences=["\n\nHuman:"],
        model="claude-v1",  # 또는 claude-2
        max_tokens_to_sample=1000,  # 응답 길이를 늘리기 위해 토큰 수 증가
    )
    
    st.write("### 답변")
    st.write(response.completion)
