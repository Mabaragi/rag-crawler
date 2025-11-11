# app.py (FastAPI 호출 로직 추가)
import requests
import streamlit as st

st.title("FastAPI 크롤러 제어 인터페이스")

# 1. 사용자 입력 폼 (텍스트 입력 위젯)
channel_name = st.text_input("채널 이름", value="시부키 다시보기")
channel_handle = st.text_input("채널 핸들", value="@shibukireplay")
streamer_name = st.text_input("스트리머 이름", value="시부키")

# 2. 버튼 추가 (API 호출 트리거)
if st.button("크롤링 작업 시작 (API 호출)"):
    # FastAPI 엔드포인트 URL (FastAPI 서버가 8000번 포트에서 실행 중이라고 가정)
    API_URL = "http://localhost:8000/youtube/insert_channel/"

    # 3. 전송할 데이터 (JSON 형태)
    payload = {"channel_name": channel_name, "channel_handle": channel_handle, "streamer_name": streamer_name}
    print("Payload to be sent:", payload)
    # 4. API 호출
    try:
        # POST 요청으로 데이터 전송
        response = requests.post(API_URL, json=payload)

        # 5. 응답 결과 표시
        if response.status_code == 200:
            st.success("✅ 채널 삽입 작업이 FastAPI 서버에 요청되었습니다!")
            st.json(response.json())
        else:
            st.error(f"❌ API 호출 실패. 상태 코드: {response.status_code}")
            st.json(response.json())

    except requests.exceptions.ConnectionError:
        st.error("⚠️ FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
