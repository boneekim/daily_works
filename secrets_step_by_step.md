# 🔐 Streamlit Cloud Secrets 설정 문제 해결

## 🚨 현재 상황
"SUPABASE_URL이 Secrets에 설정되지 않았습니다" 메시지가 계속 나타남

## 🔍 단계별 확인 및 해결

### 1️⃣ Streamlit Cloud 앱 찾기 확인
1. **https://share.streamlit.io** 접속
2. 로그인 상태 확인
3. **daily_works** 앱이 목록에 있는지 확인
4. 앱 상태가 "Running" 인지 확인

### 2️⃣ Settings 메뉴 정확한 경로
1. **daily_works** 앱 찾기
2. 앱 이름 오른쪽의 **⚙️ (톱니바퀴 아이콘)** 클릭
   - ⚠️ 주의: 앱 제목을 클릭하는 게 아니라 톱니바퀴 아이콘 클릭
3. 드롭다운 메뉴에서 **Settings** 클릭
4. 상단 탭에서 **Secrets** 클릭

### 3️⃣ Secrets 입력 정확한 형식
기존 내용을 **모두 지우고** 다음을 정확히 입력:

```toml
SUPABASE_URL = "https://실제프로젝트ID.supabase.co"
SUPABASE_ANON_KEY = "실제anon키"
```

### ⚠️ 자주 발생하는 실수들

1. **따옴표 실수**
   ❌ 잘못: `SUPABASE_URL = https://xxx.supabase.co`
   ✅ 올바름: `SUPABASE_URL = "https://xxx.supabase.co"`

2. **공백 실수**
   ❌ 잘못: `SUPABASE_URL  =  "https://xxx.supabase.co"`
   ✅ 올바름: `SUPABASE_URL = "https://xxx.supabase.co"`

3. **키 이름 실수**
   ❌ 잘못: `supabase_url = "https://xxx.supabase.co"`
   ✅ 올바름: `SUPABASE_URL = "https://xxx.supabase.co"`

4. **줄바꿈 실수**
   ❌ 잘못: 각 항목이 같은 줄에 있음
   ✅ 올바름: 각 항목이 별도 줄에 있음

### 4️⃣ 저장 및 재시작 확인
1. **Save** 버튼 클릭
2. 성공 메시지 확인
3. **Reboot app** 클릭 (또는 자동 재시작 대기)
4. 앱이 완전히 재시작될 때까지 대기 (1-2분)

### 5️⃣ 재시작 후 확인
1. 앱이 다시 로드되면
2. **"🔧 디버깅 모드"** 체크박스 클릭
3. 메시지 변화 확인

## 🎯 예상 결과

**아직도 같은 오류가 나온다면:**
- Secrets 입력 형식 재확인
- 브라우저 새로고침 후 다시 시도
- 앱을 완전히 삭제 후 재배포

**성공한다면:**
- ✅ SUPABASE_URL 발견: https://xxx...
- "SUPABASE_ANON_KEY를 추가해주세요" 메시지로 변경

## 🚨 그래도 안 되면?

1. **브라우저 캐시 지우기**
2. **다른 브라우저에서 시도**
3. **Streamlit Cloud에서 로그아웃 후 재로그인**
4. **앱을 삭제하고 새로 배포**
