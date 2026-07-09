import streamlit as st
from google import genai

# 화면 타이틀 설정
st.title("🤖 나만의 진짜 Gemini 챗봇")

# Streamlit Cloud 설정(Secrets)에 등록한 키를 안전하게 가져옵니다.
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]

# Gemini 클라이언트 초기화
client = genai.Client(api_key=GEMINI_API_KEY)

# 세션 상태(채팅 기록 저장용) 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 채팅 기록이 있다면 화면에 보여주기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력창 만들기
prompt = st.chat_input("무엇이든 물어보세요!")

# 안전장치: prompt 변수에 글자가 '실제로 존재할 때만' 챗봇 작동 시작
if prompt and prompt.strip():
    # # 1. 사용자가 입력한 글 화면에 띄우고 기록에 저장
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # # 2. Gemini에게 답변 요청하기 (가성비 최고인 gemini-2.5-flash 모델 사용!)
    try:
        # API 호출 부분을 try 안에 넣어서 보호합니다.
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        
        # # 3. AI의 답변을 화면에 띄우고 기록에 저장
        ai_response = response.text
        with st.chat_message("assistant"):
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
        
    except Exception as e:
        # 구글 서버 제한이나 오류가 발생했을 때 앱이 죽지 않고 예쁜 안내문을 띄웁니다.
        with st.chat_message("assistant"):
            st.error("💡 구글 API 요청 제한이 걸렸거나 일시적인 오류가 발생했습니다. 1~2분 뒤에 다시 질문을 입력해 주세요!")
            st.caption(f"상세 에러 내용: {e}")
