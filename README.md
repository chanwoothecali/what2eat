# 🍜 신촌 맛집 추천 챗봇

Streamlit 기반의 **개인화된 신촌 맛집 추천 챗봇**입니다.  
사용자의 음식 취향에 따라, 신촌 지역의 실제 맛집 데이터를 기반으로 GPT가 2~3개 맛집을 추천해줍니다.

---

## 🔗 배포 링크
👉 [https://what2eat.streamlit.app/](https://what2eat.streamlit.app/)

---

## 📋 프로젝트 개요

| 항목           | 내용 |
|----------------|------|
| 목적           | 음식 취향 기반 신촌 맛집 추천 챗봇 개발 |
| 기반 모델      | OpenAI GPT-3.5 Turbo (`chat.completions`) |
| UI 인터페이스  | Streamlit |
| 데이터 저장소  | Google Sheets (사용자 정보 및 맛집 목록 저장) |
| 기술 스택       | Python, Streamlit, pandas, gspread, oauth2client, openai |

---

## 🧠 사용자 흐름도

```
[1] 사용자 ID 입력
      ↓
  (이미 존재?)
      ↓                    ↘
[예] 기존 유저        [아니오] 신규 유저
      ↓                    ↓
음식 취향 불러오기     음식 취향 선택 → 저장
      ↓                    ↓
      →→→→→→ 챗봇 진입 ←←←←←←
            (취향 기반 자동 추천 출력)
```

---

## 🗂️ 시트 구조 요약

| 시트 이름              | 설명 |
|------------------------|------|
| `user`                 | 사용자 ID, 음식 취향(`food_preferences`), 가입일(`created_at`) |
| `sinchon_restaurants` | 맛집 목록, 평점, 메뉴, 주소, 설명 등 |

---

## 🏗️ 프로젝트 구조

```
📁 your_project/
├── app.py                 # 메인 실행 파일 (Streamlit 진입점)
├── ui.py                  # 사용자 입력 흐름 관리 (ID, 선호 선택)
├── chatbot.py             # GPT 추천 챗봇 UI 및 응답 처리
├── sheets.py              # Google Sheets 입출력 함수들
├── .streamlit/
│   └── secrets.toml       # API 키 및 서비스 계정 키 보관 (배포 시)
├── sinchon_restaurants.csv  # (개발 중 사용한 샘플 CSV)
```

---

## ▶️ 실행 방법 (로컬 기준)

### 1. 필수 패키지 설치
```bash
pip install streamlit pandas gspread oauth2client openai
```

### 2. 서비스 계정 키 설정 (`.streamlit/secrets.toml`)
```toml
[gcp_service_account]
type = "service_account"
project_id = "..."
private_key_id = "..."
private_key = "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
client_email = "..."
client_id = "..."
...

[openai]
api_key = "sk-..."
```

### 3. 실행
```bash
streamlit run app.py
```

---

## 💡 향후 개선 아이디어
- 음식점 상세 페이지 링크 추가
- 위치 기반 지도 시각화
- 사용자 선호도 학습 기반 추천 강화 (Collaborative Filtering)
- 리뷰 기반 감성 분석 추천

---

## 📬 문의
개선 제안이나 협업 문의는 이슈나 PR로 남겨주세요!

---

감사합니다 🙏
