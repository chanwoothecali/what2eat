# ui.py
import streamlit as st
from sheets import write_user_data

def show_intro_or_chat(sheet):
    if "name_entered" not in st.session_state:
        st.session_state.name_entered = False
    if "category_selected" not in st.session_state:
        st.session_state.category_selected = False
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "food_category" not in st.session_state:
        st.session_state.food_category = []

    if not st.session_state.name_entered:
        name = st.text_input("당신의 이름을 알려주세요 👋")
        if name:
            st.session_state.user_name = name
            st.session_state.name_entered = True
            st.rerun()
        return False

    elif not st.session_state.category_selected:
        st.write(f"반가워요, **{st.session_state.user_name}**님!")
        category = st.multiselect("어떤 종류의 음식을 좋아하시나요?", 
                                  ["한식", "일식", "양식", "중식", "분식", "디저트", "패스트푸드"])
        if category:
            st.session_state.food_category = category
            st.session_state.category_selected = True
            write_user_data(sheet, st.session_state.user_name, category)
            st.rerun()
        return False

    return True
