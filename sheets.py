# sheets.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta
import pandas as pd  # 꼭 필요

def _authorize_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    gcp_credentials = st.secrets["gcp_service_account"]
    creds_dict = dict(gcp_credentials)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    return gspread.authorize(credentials)

def load_restaurant_data():
    client = _authorize_gsheet()
    worksheet = client.open("what2eat").worksheet("sinchon_restaurants")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def init_gsheet():
    client = _authorize_gsheet()
    return client.open("what2eat").worksheet("user")

def write_user_data(sheet, user_id, food_categories):
    food_pref = ", ".join(food_categories)
    kr_time = datetime.now(timezone(timedelta(hours=9)))
    created_at = kr_time.strftime("%Y-%m-%d %H:%M:%S")
    row = [user_id, food_pref, created_at]
    sheet.append_row(row)

def get_user_row(sheet, user_id):
    records = sheet.get_all_records()
    for row in records:
        if row["user_id"] == user_id:
            return row
    return None

def update_feedback_count(rating):
    """
    좋아요/싫어요 수치를 누적하는 함수
    rating: 'like' 또는 'dislike'
    """
    client = _authorize_gsheet()
    sheet = client.open("what2eat").worksheet("feedback")

    # 시트 구조: A1='like', B1='dislike' / A2와 B2에 숫자 있음
    cell_map = {"like": "A2", "dislike": "B2"}
    cell = cell_map.get(rating)
    if not cell:
        return

    current = sheet.acell(cell).value
    current_value = int(current) if current else 0
    sheet.update_acell(cell, str(current_value + 1))
