# sheets.py
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def init_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    gcp_credentials = st.secrets["gcp_service_account"]
    creds_dict = dict(gcp_credentials)
    creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(credentials)
    return client.open("what2eat").worksheet("user")

def write_user_data(sheet, user_name, food_categories):
    row = [user_name, ", ".join(food_categories)]
    sheet.append_row(row)