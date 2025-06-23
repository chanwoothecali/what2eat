# chatbot.py
import streamlit as st
import pandas as pd
from openai import OpenAI
from sheets import load_restaurant_data, update_feedback_count

# 🔍 음식 관련 키워드 필터
def is_food_related(question):
    food_keywords = [
        "맛집", "추천", "식당", "먹을", "밥", "점심", "저녁", "한끼", "혼밥", "배고파",
        "뭐 먹", "파스타", "라멘", "카레", "김밥", "떡볶이", "술집", "치킨", "고기", "메뉴", "소주", "맥주", "땡기"
    ]
    return any(keyword in question for keyword in food_keywords)

# 📦 GPT 프롬프트 생성
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

# 🤖 GPT 호출 함수
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

# 👍 피드백 UI 표시 함수
def show_feedback_ui():
    st.markdown("---")
    st.markdown("이 추천은 어땠나요?")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 좋아요", key="like"):
            update_feedback_count("like")
            st.success("좋아요 평가 감사합니다! 🙏")
            st.session_state["feedback_ready"] = False
            st.rerun()

    with col2:
        if st.button("👎 별로에요", key="dislike"):
            update_feedback_count("dislike")
            st.success("피드백 감사합니다! 더 나은 추천에 반영할게요!")
            st.session_state["feedback_ready"] = False
            st.rerun()

# 💬 챗봇 실행 함수
def show_chatbot():
    df = load_restaurant_data()

    # 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "awaiting_response" not in st.session_state:
        st.session_state.awaiting_response = False

    st.title("🍜 신촌 맛집 추천 챗봇")
    st.markdown("신촌 근처에서 뭐 먹을지 고민될 때 물어보세요!")

    # ✅ 자동 추천 (최초 진입 시 1회 실행)
    if not st.session_state.messages and st.session_state.food_category:
        preferred = ", ".join(st.session_state.food_category)
        intro_question = f"{preferred} 계열 음식을 좋아하는 사람에게 신촌에서 어떤 맛집을 추천해줄 수 있을까?"
        answer = ask_gpt(intro_question, df)

        greeting = f"안녕하세요 {st.session_state.user_id}님, 반가워요! 🎉\n\n오늘은 이런 곳 어떠세요?\n\n{answer}"
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        st.session_state["feedback_ready"] = True

    # 💬 메시지 출력
    for msg in st.session_state.messages:
        with st.chat_message("user" if msg["role"] == "user" else "assistant"):
            st.markdown(msg["content"])

    # ✍️ 사용자 입력
    if not st.session_state.awaiting_response:
        user_input = st.chat_input("예: 혼밥하기 좋은 라멘집 알려줘")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.awaiting_response = True
            st.rerun()

    # 🤖 GPT 응답 생성
    elif st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("GPT가 대답을 고르는 중..."):
            last_question = st.session_state.messages[-1]["content"]
            answer = ask_gpt(last_question, df)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            st.session_state.awaiting_response = False
            st.session_state["feedback_ready"] = True
            st.rerun()

    # ✅ 피드백 조건 분기 (자동 or 사용자 질문)
    if st.session_state.get("feedback_ready", False):
        msgs = st.session_state.messages

        if len(msgs) == 1 and msgs[0]["role"] == "assistant":
            show_feedback_ui()  # 자동 추천

        elif (
            len(msgs) >= 2
            and msgs[-1]["role"] == "assistant"
            and msgs[-2]["role"] == "user"
            and is_food_related(msgs[-2]["content"])
        ):
            show_feedback_ui()  # 사용자 질문 후 추천
