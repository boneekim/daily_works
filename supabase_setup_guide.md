# Supabase 데이터베이스 설정 가이드

## 📋 단계별 설정 방법

### 1️⃣ Supabase 프로젝트 생성

1. **Supabase 웹사이트 접속**
   - https://supabase.com 방문
   - "Start your project" 클릭

2. **새 프로젝트 생성**
   - "New project" 클릭
   - 프로젝트 이름: `daily-works`
   - 데이터베이스 비밀번호: 강력한 비밀번호 설정
   - 지역: 한국과 가까운 지역 선택 (예: Singapore)
   - "Create new project" 클릭

3. **프로젝트 준비 대기**
   - 프로젝트 생성에 1-2분 소요
   - 생성 완료까지 대기

### 2️⃣ 데이터베이스 테이블 생성

1. **SQL Editor 접속**
   - 왼쪽 메뉴에서 "SQL Editor" 클릭
   - "New query" 클릭

2. **SQL 스크립트 실행**
   - `setup_database.sql` 파일의 내용을 복사
   - SQL Editor에 붙여넣기
   - "Run" 버튼 클릭

3. **실행 결과 확인**
   - 모든 명령이 성공적으로 실행되었는지 확인
   - 테이블이 생성되었는지 확인

### 3️⃣ API 키 확인

1. **Settings > API 이동**
   - 왼쪽 메뉴에서 "Settings" 클릭
   - "API" 탭 클릭

2. **필요한 정보 복사**
   - `Project URL`: 프로젝트 URL 복사
   - `anon public`: anon key 복사

### 4️⃣ Streamlit 앱 설정

1. **secrets.toml 파일 생성**
   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. **API 정보 입력**
   `.streamlit/secrets.toml` 파일을 열고 다음과 같이 수정:
   ```toml
   SUPABASE_URL = "https://your-project-id.supabase.co"
   SUPABASE_ANON_KEY = "your-anon-key-here"
   ```

### 5️⃣ 테스트

1. **로컬에서 앱 실행**
   ```bash
   streamlit run app.py
   ```

2. **기능 테스트**
   - 새 항목 추가 테스트
   - 목록 표시 확인
   - 링크 클릭 테스트
