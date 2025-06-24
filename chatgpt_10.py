## 
## API를 숨기기
## 01. 해당 작업 폴더 내에 '.streamlit'라는 폴더를 만든다.
## 02. 해당 폴더 내에 'secrets.toml'이라는 파일을 만든다.
## 03. secrets.toml 파일에 아래와 같이 작성한다.
## [openai]
## API_KEY = "sk-..." # 본인의 API 키를 입력한다.

import openai
import streamlit as st
from openai import OpenAI
import os

# Streamlit app
st.title("여행용 챗봇과 대화하기")
openai_api_key = st.secrets['openai']['API_KEY']
client = OpenAI(api_key  = openai_api_key)

# 초기 대화 상태 설정
if "messages" not in st.session_state:
    st.session_state.messages = [  
        {"role": "system", 
         "content": "기본적으로 한국어와 영어로 제공해 주세요."
                "당신은 여행에 관한 질문에 답하는 챗봇입니다. "
                "여행지 추천, 준비물, 문화, 음식 등 다양한 주제에 대해 친절하게 안내하는 챗봇입니다."
                    }  
    ]

# 사용자 입력
user_input = st.text_input("사용자:", key="user_input")

# 대화 초기화 버튼 추가
if st.button("대화 초기화") and st.session_state.messages:
    st.session_state.messages = []

if st.button("전송") and user_input:
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", 
                                      "content": user_input})

    # OpenAI API 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # gpt-4o-mini로 변경
        messages=st.session_state.messages
    )

    # OpenAI 응답 추가
    response_message = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", 
                                      "content": response_message})

    # 사용자 입력 초기화
    user_input = ""

# 대화 내용 표시
for message in st.session_state.messages:
    role = "👤"  if message["role"] == "user" else "🤖"
    st.markdown(f"{role}: {message['content']}")
