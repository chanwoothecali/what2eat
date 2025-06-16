import streamlit as st
import pandas as pd
from openai import OpenAI

# 🧾 페이지 설정은 가장 먼저
st.set_page_config(page_title="신촌 맛집 추천 챗봇", layout="centered")

# 🔐 OpenAI API 설정
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# 🍽 CSV 불러오기
@st.cache_data
def load_data():
    return pd.read_csv("sinchon_restaurants.csv")

df = load_data()

import re

def is_food_related(question):
    food_keywords = [
        "맛집", "추천", "식당", "먹을", "밥", "점심", "저녁", "한끼", "혼밥", "배고파",
        "뭐 먹", "파스타", "라멘", "카레", "김밥", "떡볶이", "술집", "치킨", "고기", "메뉴", "소주", "맥주"
    ]
    return any(keyword in question for keyword in food_keywords)


# GPT 요청 함수
def ask_gpt(user_question, df):
    if is_food_related(user_question):
        prompt = build_prompt(user_question, df)
        system_role = "당신은 신촌 맛집을 추천해주는 도우미입니다. 사용자의 질문을 바탕으로 식당을 2~3곳 추천해주세요."
    else:
        prompt = user_question
        system_role = "당신은 친절한 챗봇입니다. 자연스럽게 대화에 응답해주세요. 식당 추천은 하지 마세요."

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )
    return response.choices[0].message.content.strip()


# 프롬프트 생성 함수
def build_prompt(user_question, df):
    rows = df.head(10).to_dict(orient="records")
    desc = "\n".join([
        f"{i+1}. {row['Restaurant Name']} ({row['Rating']}점) - {row['Menu']}\n"
        f"   주소: {row['Address']}\n"
        f"   설명: {row['Description']}"
        for i, row in enumerate(rows)
    ])
    return f"""
신촌 맛집 리스트가 아래에 있습니다.
사용자의 질문에 가장 적절한 맛집을 2~3개 추천하고, 추천 이유도 함께 알려주세요.

맛집 목록:
{desc}

사용자 질문: {user_question}
추천:
"""

# 세션 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

if "awaiting_response" not in st.session_state:
    st.session_state.awaiting_response = False

# 타이틀 및 설명
st.title("🍜 신촌 맛집 추천 챗봇")
st.markdown("신촌 근처에서 뭐 먹을지 고민될 때 물어보세요!")

# 채팅 UI 출력
for msg in st.session_state.messages:
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# 🚧 입력창 (GPT 응답 중일 땐 입력 차단)
if not st.session_state.awaiting_response:
    user_input = st.chat_input("예: 혼밥하기 좋은 라멘집 알려줘")
    if user_input:
        # 사용자 메시지 기록
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.awaiting_response = True
        st.rerun()

# 🚀 GPT 응답 처리
elif st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("GPT가 대답을 고르는 중..."):
        last_question = st.session_state.messages[-1]["content"]
        answer = ask_gpt(last_question, df)  # ✅ 이제 질문을 직접 넘김
        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.awaiting_response = False
        st.rerun()


