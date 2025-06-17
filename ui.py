import streamlit as st
from sheets import write_user_data, get_user_row
import time

def show_intro_or_chat(sheet):
    # 🧱 세션 상태 초기화
    for key, default in {
        "user_id": "",
        "existing_user": False,
        "login_done": False,
        "category_selected": False,
        "pending_category": [],
        "food_category": [],
        "show_saved_message": False,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = default

    # ✅ 1단계: 사용자 ID 입력
    if not st.session_state.login_done:
        user_list = sheet.col_values(1)  # ID 목록
        input_id = st.text_input("사용자 ID를 입력해주세요", key="id_input")

        if input_id:
            st.session_state.user_id = input_id
            st.session_state.existing_user = input_id in user_list
            st.session_state.login_done = True

            if st.session_state.existing_user:
                # 기존 사용자 → 음식 취향도 불러옴
                user_row = get_user_row(sheet, input_id)
                if user_row:
                    st.session_state.food_category = user_row.get("food_preferences", "").split(", ")
            st.rerun()

        return False  # 여기서 반드시 끊어줘야 함

    # ✅ 2단계: 기존 사용자 → 챗봇 바로 진입
    if st.session_state.existing_user:
        return True

    # ✅ 3단계: 신규 사용자 → 음식 취향 입력
    if not st.session_state.category_selected:
        st.info(f"{st.session_state.user_id}님, 음식 취향을 선택해주세요.")
        selected = st.multiselect("좋아하는 음식 종류 (복수 선택 가능)",
                                  ["한식", "일식", "양식", "중식", "분식", "디저트", "패스트푸드"],
                                  key="category_select")
        st.session_state.pending_category = selected

        if st.button("확인"):
            if selected:
                write_user_data(sheet, st.session_state.user_id, selected)
                st.session_state.food_category = selected  # → 챗봇 추천용
                st.session_state.category_selected = True
                st.session_state.show_saved_message = True
                st.rerun()
            else:
                st.warning("최소 하나 이상의 항목을 선택해주세요.")
        return False

    # ✅ 4단계: 저장 완료 메시지 딱 2초만
    if st.session_state.show_saved_message:
        with st.empty():
            st.success("정보가 저장되었습니다!")
            time.sleep(2)
        st.session_state.show_saved_message = False
        st.rerun()

    return True

