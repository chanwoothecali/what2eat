# app.py (메인 실행 파일)
import streamlit as st
from ui import show_intro_or_chat
from sheets import init_gsheet, write_user_data
from chatbot import show_chatbot

# 페이지 설정
st.set_page_config(page_title="신촌 맛집 추천 챗봇", layout="centered")

# 시트 연결
sheet = init_gsheet()

# 이름/선호 카테고리 입력 및 챗 화면 전환
if show_intro_or_chat(sheet):
    show_chatbot()