# sheets.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta
import pandas as pd  # 꼭 필요

def load_restaurant_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    gcp_credentials = st.secrets["gcp_service_account"]
    creds_dict = dict(gcp_credentials)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(credentials)

    # ✅ 여기가 핵심: 시트 탭 이름을 정확히 지정
    worksheet = client.open("what2eat").worksheet("sinchon_restaurants")
    data = worksheet.get_all_records()
    return pd.DataFrame(data)

def init_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    gcp_credentials = st.secrets["gcp_service_account"]
    creds_dict = dict(gcp_credentials)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(credentials)
    return client.open("what2eat").worksheet("user")

def write_user_data(sheet, user_id, food_categories):
    # 1. 음식 선호 → 문자열
    food_pref = ", ".join(food_categories)

    # 2. 현재 시간 (한국 시간대 기준)
    kr_time = datetime.now(timezone(timedelta(hours=9)))
    created_at = kr_time.strftime("%Y-%m-%d %H:%M:%S")

    # 3. 행 저장
    row = [user_id, food_pref, created_at]
    sheet.append_row(row)

def get_user_row(sheet, user_id):
    records = sheet.get_all_records()
    for row in records:
        if row["user_id"] == user_id:
            return row
    return None
