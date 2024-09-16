import streamlit as st
import os
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.tools import DuckDuckGoSearchRun
from langdetect import detect

# 환경변수에서 API 키 읽어오기
openai_api_key = os.getenv('OPENAI_API_KEY')

st.sidebar.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
st.sidebar.markdown("[View the source code](https://github.com/streamlit/llm-examples/blob/main/pages/2_Chat_with_search.py)")
st.sidebar.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")

st.title("🔎 마케팅 정보 검색 챗봇")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요, 웹에서 정보를 검색할 수 있는 챗봇입니다. 어떤 마케팅 정보가 필요하신가요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input(placeholder="2018년 여성의 U.S. Open 우승자는 누구인가요?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    if not openai_api_key:
        st.error("OpenAI API 키를 환경변수에 설정해 주세요.")
        st.stop()

    # 언어 감지
    try:
        language = detect(prompt)
    except:
        st.error("입력 언어를 감지할 수 없습니다. 다시 시도해 주세요.")
        st.stop()

    # 언어에 맞는 응답 프롬프트 설정
    if language == 'ko':
        system_message = "당신은 한국어를 사용하는 마케팅 정보 전문가입니다."
    else:
        system_message = "You are a marketing information expert who speaks English."

    # LLM 모델 생성
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
    search = DuckDuckGoSearchRun(name="Search")
    search_agent = initialize_agent(
        tools=[search], llm=llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True
    )
    
    # 사용자 메시지 추가
    st.session_state.messages.insert(0, {"role": "system", "content": system_message})

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.write(response)
