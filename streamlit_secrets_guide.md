# Streamlit Community Cloud Secrets 설정 가이드

## 🔐 1단계: Supabase 정보 확인

### Supabase 대시보드에서 API 정보 찾기:
1. **https://supabase.com** 접속
2. 프로젝트 선택
3. 왼쪽 메뉴에서 **Settings** 클릭
4. **API** 탭 클릭
5. 다음 정보 복사:
   - **Project URL** (예: https://xxxxxxxxxxx.supabase.co)
   - **anon public key** (긴 문자열)

## 🚀 2단계: Streamlit Community Cloud Secrets 설정

### Streamlit Cloud에서 설정:
1. **https://share.streamlit.io** 접속
2. daily_works 앱 찾기
3. 앱 오른쪽의 **⚙️ (설정 아이콘)** 클릭
4. **Settings** 선택
5. **Secrets** 탭 클릭
6. 다음 내용 입력:

```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key-here"
```

**⚠️ 주의사항:**
- URL과 Key는 따옴표로 감싸야 합니다
- 실제 값으로 교체해야 합니다
- 공백이나 오타가 없는지 확인

## 🔄 3단계: 앱 재시작
1. **Save** 클릭
2. **Reboot app** 클릭 (또는 앱이 자동으로 재시작됨)

## ✅ 4단계: 확인
앱이 재시작되면 오류 메시지 없이 정상 작동해야 합니다.
