import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 구글 시트 연동 설정
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_cred_file.json", scope)
client = gspread.authorize(creds)

# 시트 열기
sheet = client.open("feedback").sheet1  # 시트 이름: feedback

def increment_feedback(rating: str):
    """
    rating: 'like' 또는 'dislike'
    """
    cell_map = {"like": "A2", "dislike": "B2"}
    cell = cell_map.get(rating)

    if not cell:
        return

    current_value = sheet.acell(cell).value
    current_value = int(current_value) if current_value else 0
    sheet.update_acell(cell, current_value + 1)