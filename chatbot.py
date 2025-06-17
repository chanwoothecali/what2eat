# chatbot.py
import streamlit as st
import pandas as pd
from openai import OpenAI
from sheets import load_restaurant_data

def is_food_related(question):
    food_keywords = [
        "맛집", "추천", "식당", "먹을", "밥", "점심", "저녁", "한끼", "혼밥", "배고파",
        "뭐 먹", "파스타", "라멘", "카레", "김밥", "떡볶이", "술집", "치킨", "고기", "메뉴", "소주", "맥주"
    ]
    return any(keyword in question for keyword in food_keywords)

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

def ask_gpt(user_question, df):
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])

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

def show_chatbot():
    df = load_restaurant_data()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "awaiting_response" not in st.session_state:
        st.session_state.awaiting_response = False

    st.title("🍜 신촌 맛집 추천 챗봇")
    st.markdown("신촌 근처에서 뭐 먹을지 고민될 때 물어보세요!")

    # ✅ 첫 자동 추천 메시지 (세션에 메시지 없고, 취향 정보 있을 경우)
    if not st.session_state.messages and st.session_state.food_category:
        preferred = ", ".join(st.session_state.food_category)
        
        # 👉 사용자 취향 기반으로 GPT 추천 받기
        intro_question = f"{preferred} 계열 음식을 좋아하는 사람에게 신촌에서 어떤 맛집을 추천해줄 수 있을까?"
        answer = ask_gpt(intro_question, df)
        
        greeting = f"안녕하세요 {st.session_state.user_id}님, 반가워요! 🎉\n\n오늘은 이런 곳 어떠세요?\n\n{answer}"
        st.session_state.messages.append({"role": "assistant", "content": greeting})

    # 채팅창 출력
    for msg in st.session_state.messages:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

    if not st.session_state.awaiting_response:
        user_input = st.chat_input("예: 혼밥하기 좋은 라멘집 알려줘")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.awaiting_response = True
            st.rerun()

    elif st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("GPT가 대답을 고르는 중..."):
            last_question = st.session_state.messages[-1]["content"]
            answer = ask_gpt(last_question, df)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.awaiting_response = False
            st.rerun()