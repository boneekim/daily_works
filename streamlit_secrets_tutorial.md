# 🎯 Streamlit Cloud Secrets 설정 - 실제 단계

## 현재 상황: "SUPABASE_URL을 추가해주세요" 메시지

✅ 디버깅이 정상 작동 중 - 이제 Secrets를 설정하면 됩니다!

## 🔗 1단계: Supabase에서 정보 복사

### A. Supabase 접속
1. 새 탭에서 **https://supabase.com** 열기
2. 로그인 후 **daily-works** (또는 생성한 프로젝트명) 클릭

### B. API 정보 찾기
1. 왼쪽 메뉴에서 **⚙️ Settings** 클릭
2. **API** 탭 클릭
3. 다음 정보를 복사해두기:

**Project URL 복사:**
```
https://abcdefghijklmnop.supabase.co
```

**anon public 키 복사:**  
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS...
```

## ⚙️ 2단계: Streamlit Cloud Secrets 설정

### A. Streamlit Cloud 접속
1. 새 탭에서 **https://share.streamlit.io** 열기
2. **daily_works** 앱 찾기

### B. Settings 메뉴 접근
1. 앱 오른쪽의 **⚙️ (톱니바퀴 아이콘)** 클릭
2. **Settings** 클릭
3. **Secrets** 탭 클릭

### C. Secrets 입력
기존 내용을 모두 지우고 다음을 **정확히** 입력:

```toml
SUPABASE_URL = "https://abcdefghijklmnop.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS..."
```

**⚠️ 주의사항:**
- `https://abcdefghijklmnop.supabase.co` → 실제 Project URL로 교체
- `eyJhbGciOiJI...` → 실제 anon public 키로 교체  
- 따옴표 `""` 반드시 포함
- 오타 금지

### D. 저장 및 재시작
1. **Save** 버튼 클릭
2. **Reboot app** 클릭 (또는 자동 재시작 대기)

## ✅ 3단계: 결과 확인

앱이 재시작되면:
1. **"🔧 디버깅 모드"** 다시 체크
2. 다음 메시지들이 나타나야 함:
   - ✅ st.secrets 접근 가능
   - ✅ SUPABASE_URL 발견: https://abc...
   - ✅ SUPABASE_ANON_KEY 발견: eyJhbGci...
   - ✅ Supabase 연결 성공!

## 🚨 여전히 오류가 나면?

### "SUPABASE_ANON_KEY를 추가해주세요"
→ anon public 키도 Secrets에 추가 필요

### "SUPABASE_URL 형식이 올바르지 않습니다"  
→ URL이 `https://`로 시작하는지 확인

### "Supabase 연결 실패"
→ Supabase 프로젝트가 활성화되어 있는지 확인
