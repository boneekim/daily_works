# Daily Works - 데일리 실천 체험단 관리 앱

Daily Works는 Streamlit과 Supabase를 사용하여 만든 데일리 실천 체험단 정보 관리 웹 애플리케이션입니다.

## 🌟 주요 기능

- **항목 추가**: 제목, 카테고리, 링크를 입력하여 새로운 체험단/이벤트 정보 추가
- **카테고리 필터링**: 15개 카테고리별로 항목 필터링
- **검색 기능**: 제목으로 항목 검색
- **링크 연결**: 링크 클릭 시 새 창에서 해당 사이트 열기
- **실시간 업데이트**: 항목 추가 시 즉시 목록에 반영

## 📋 카테고리

1. 핫딜
2. 체험단
3. 재태크
4. 매일읽기
5. 전시,문화
6. 방송
7. 시사회
8. 온라인 강의,공부
9. 세미나
10. 회사 혜택
11. 책관련
12. 웹진(무료)
13. 감성블로그
14. 생활편의

## 🚀 설치 및 실행

### 1. 저장소 클론
```bash
git clone <repository-url>
cd daily_works
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. Supabase 설정

#### 3.1 Supabase 프로젝트 생성
1. [Supabase](https://supabase.com)에 접속하여 새 프로젝트 생성
2. 프로젝트 설정에서 API URL과 anon key 확인

#### 3.2 테이블 생성
Supabase 대시보드의 SQL Editor에서 다음 쿼리 실행:

```sql
-- daily_works 테이블 생성
CREATE TABLE daily_works (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    link TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL
);

-- RLS (Row Level Security) 활성화 (선택사항)
ALTER TABLE daily_works ENABLE ROW LEVEL SECURITY;

-- 모든 사용자가 읽고 쓸 수 있도록 정책 생성 (개발용)
CREATE POLICY "Allow all operations" ON daily_works FOR ALL USING (true);
```

### 4. 환경 변수 설정

`.streamlit/secrets.toml` 파일을 생성하고 다음 내용 추가:

```toml
SUPABASE_URL = "your-supabase-url"
SUPABASE_ANON_KEY = "your-supabase-anon-key"
```

### 5. 앱 실행
```bash
streamlit run app.py
```

## 🔧 기술 스택

- **Frontend**: Streamlit
- **Database**: Supabase (PostgreSQL)
- **Language**: Python
- **Libraries**: pandas, supabase-py

## 📁 프로젝트 구조

```
daily_works/
├── app.py              # 메인 애플리케이션 파일
├── requirements.txt    # Python 패키지 의존성
├── README.md          # 프로젝트 문서
├── .streamlit/
│   └── secrets.toml   # Supabase 설정 (생성 필요)
└── .gitignore         # Git 무시 파일
```

## 🌐 배포

### Streamlit Community Cloud
1. GitHub에 코드 푸시
2. [Streamlit Community Cloud](https://share.streamlit.io)에서 앱 배포
3. Secrets 설정에서 Supabase 정보 입력

## 📝 사용법

1. **새 항목 추가**:
   - 상단의 "새 항목 추가" 섹션에서 제목, 카테고리, 링크 입력
   - "추가하기" 버튼 클릭

2. **항목 필터링**:
   - 카테고리 필터를 사용하여 원하는 카테고리만 표시
   - 검색창에 키워드 입력하여 제목으로 검색

3. **링크 이동**:
   - 목록의 제목을 클릭하면 해당 사이트로 새 창에서 이동

## 🤝 기여하기

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 라이선스

MIT License

## 📞 문의

프로젝트에 대한 문의사항이 있으시면 이슈를 생성해주세요.
