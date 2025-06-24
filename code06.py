import streamlit as st
from openai import OpenAI

# 페이지 설정
st.set_page_config(
    page_title="AI 이미지 생성기",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 상단 타이틀 및 설명
st.markdown(
    """
    <div style="text-align:center;">
        <h1 style="color:#6C63FF;">🖼️ AI 이미지 생성기</h1>
        <p style="font-size:18px; color:#444;">
            원하는 이미지를 텍스트로 설명해보세요.<br>
            <span style="color:#6C63FF;">AI</span>가 멋진 그림을 만들어 드립니다!
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# 사이드바 디자인
st.sidebar.markdown(
    """
    <div style="text-align:center;">
        <h2 style="color:#6C63FF;">🔑 설정</h2>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("텍스트를 입력하면, 해당 내용을 바탕으로 이미지를 생성합니다.")

st.sidebar.title("🔑 설정")
openai_api_key = st.sidebar.text_input("OpenAI API 키 입력", 
                                type="password" )

if not openai_api_key:
    st.sidebar.warning("OpenAI API 키를 입력하세요.")
    st.stop()

# OpenAI 클라이언트 설정 
client = OpenAI(api_key=openai_api_key)

# 스타일 및 크기 선택을 컬럼으로 배치
col1, col2 = st.columns(2)
with col1:
    style = st.selectbox(
        "🎨 이미지 스타일",
        ("기본", "수채화", "만화"),
        help="이미지의 스타일을 선택하세요."
    )
with col2:
    size = st.selectbox(
        "🖼️ 이미지 크기",
        ("1024x1024", "1024x1792", "1792x1024"),
        help="이미지의 해상도를 선택하세요."
    )

# 스타일에 따라 프롬프트에 스타일 정보 추가
style_prompt_map = {
    "기본": "",
    "수채화": ", watercolor style",
    "만화": ", cartoon style",
    "일러스트": ", illustration style"
}

# 사용자 입력
prompt = st.text_input(
    "📝 이미지 설명을 입력하세요",
    value="A cute dog",
    help="생성하고 싶은 이미지를 간단하게 설명해 주세요."
)

# 버튼 스타일 커스텀
button_style = """
    <style>
    div.stButton > button {
        background-color: #6C63FF;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        font-size: 18px;
        margin-top: 10px;
    }
    </style>
"""

# 전송버튼
if st.button("이미지 생성하기"):
    styled_prompt = prompt + style_prompt_map[style]
    with st.spinner("이미지를 생성 중입니다..."):
        try:
            response1 = client.images.generate(
                prompt = prompt,
                model="dall-e-3",
                size=size
            )

            response2 = client.images.generate(
                prompt = prompt,
                model="dall-e-3",
                size=size
            )

            image_url1 = response1.data[0].url
            image_url2 = response2.data[0].url
            st.image(image_url1, caption="생성된 이미지", use_column_width=True)
            st.image(image_url2, caption="생성된 이미지", use_column_width=True)

        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다 :{e}")
