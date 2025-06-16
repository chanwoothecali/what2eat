
# 🍜 What2Eat - 신촌 맛집 추천 챗봇

> 팀 이름: **오늘 뭐먹지**  
> 기술 스택: Python, Streamlit, OpenAI API

신촌에서 뭐 먹을지 고민될 때, 이 챗봇에게 물어보세요!  
LLM 기반 자연어 이해와 간단한 데이터 기반 필터링을 통해, 사용자 질문에 맞는 식당을 추천해줍니다.

---

## 🛠 주요 기능

- 📍 사용자 질문을 바탕으로 신촌 맛집 추천
- 💬 GPT-3.5-turbo를 활용한 자연스러운 챗 인터페이스
- 🧾 CSV 기반의 간단한 맛집 데이터 활용
- 🎛 음식 관련 질문과 일반 질문 구분 처리

---

## 🚀 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/your-username/what2eat.git
cd what2eat
```

### 2. 가상환경 설정 (선택)

```bash
python -m venv venv
source venv/bin/activate  # Windows는 venv\Scripts\activate
```

### 3. 필요 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. API 키 등록

`.streamlit/secrets.toml` 파일을 아래와 같이 생성합니다:

```toml
[openai]
api_key = "your-api-key-here"
```

> `.streamlit/secrets.toml`는 `.gitignore`에 포함되어 있어 공개되지 않습니다.

### 5. 앱 실행

```bash
streamlit run sample.py
```

---

## 📂 파일 구조

```text
what2eat/
├── sample.py                # Streamlit 메인 앱
├── sinchon_restaurants.csv # 신촌 맛집 데이터
├── requirements.txt         # 필요한 패키지 목록
├── .streamlit/
│   └── secrets.toml         # OpenAI API 키 (직접 생성)
└── README.md
```

---

## 📊 예시 사용 질문

```
- 혼밥하기 좋은 라멘집 있을까?
- 여자 셋이 데이트 겸 갈만한 신촌 맛집은?
- 오늘 소주 땡기는데 분위기 괜찮은 술집 추천해줘
- 그냥 안부 인사만 해봤어 ㅎㅎ
```

---

## 🧠 사용 기술 요약

- **LLM 기반 추천**: OpenAI GPT-3.5-turbo
- **UI 프레임워크**: Streamlit
- **정보 검색 요소**: 키워드 기반 간단 필터링
- **개인화 요소**: 상황/분위기 기반 추천
- **추천 로직**: 데이터 기반 프롬프트 생성 → GPT 응답 파싱

---

## 🧑‍🤝‍🧑 팀원 역할

| 이름 | 역할 |
|------|------|
| A (웹개발) | Streamlit UI 구현, 챗봇 UX 설계 |
| B (웹개발) | CSV 데이터 정리 및 추천 프롬프트 설계 |
| C (인프라) | 실행 환경 관리, 배포 실험, Git 버전 관리 |

---

## 📌 참고 사항

- 신촌 지역 맛집 데이터는 수동 수집된 샘플이며, 테스트용으로만 사용됩니다.
- 추후 GPT를 통해 지역별 확장도 고려하고 있습니다.

---

## 📮 Contact

궁금한 점이나 제안 사항은 언제든지 이슈를 남겨주세요!
