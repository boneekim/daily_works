# 🔐 Streamlit Community Cloud Secrets 설정 완전 가이드

## ❌ 현재 오류: "Supabase 설정을 확인해주세요. Secrets에 SUPABASE_URL과 SUPABASE_ANON_KEY를 추가해주세요."

이 오류는 Streamlit Community Cloud에서 Supabase 연결 정보가 올바르게 설정되지 않았을 때 발생합니다.

## 🎯 해결 방법 (단계별)

### 1단계: Supabase 정보 확인 ✅

1. **https://supabase.com** 접속
2. 본인의 **daily-works** 프로젝트 클릭
3. 왼쪽 메뉴에서 **Settings** 클릭
4. **API** 탭 클릭
5. 다음 정보를 정확히 복사:

```
📍 Project URL: https://xxxxxxxxxxxxxxxxx.supabase.co
🔑 anon public key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxxxxxxxxx
```

### 2단계: Streamlit Cloud Secrets 설정 ✅

1. **https://share.streamlit.io** 접속
2. **daily_works** 앱 찾기
3. 앱 오른쪽의 **⚙️ (톱니바퀴)** 아이콘 클릭
4. **Settings** 클릭
5. **Secrets** 탭 클릭
6. 기존 내용을 모두 지우고 다음 형식 **정확히** 입력:

```toml
SUPABASE_URL = "https://xxxxxxxxxxxxxxxxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.xxxxxxxxxxxxxxxxx"
```

### ⚠️ 중요한 주의사항

1. **따옴표 필수**: URL과 Key는 반드시 큰따옴표("")로 감싸야 합니다
2. **공백 금지**: = 앞뒤에 불필요한 공백이 있으면 안 됩니다
3. **실제 값 사용**: 위의 xxx는 실제 Supabase 값으로 교체해야 합니다
4. **오타 금지**: 한 글자라도 틀리면 작동하지 않습니다

### 3단계: 저장 및 재시작 ✅

1. **Save** 버튼 클릭
2. **Reboot app** 클릭 (또는 자동 재시작 대기)
3. 앱이 재시작되면 "🔧 디버깅 모드" 체크박스 클릭
4. Secrets 설정 상태 확인

## 🔧 디버깅 방법

앱에서 **"🔧 디버깅 모드"** 를 체크하면 다음을 확인할 수 있습니다:

- ✅ st.secrets 접근 가능 여부
- ✅ SUPABASE_URL 존재 및 형식 검증
- ✅ SUPABASE_ANON_KEY 존재 및 길이 검증
- ✅ 현재 설정된 Secrets 키 목록

## 🚨 자주 발생하는 오류들

### 오류 1: "SUPABASE_URL이 Secrets에 없습니다"
**해결**: Secrets에서 키 이름을 `SUPABASE_URL`로 정확히 입력 (대소문자 구분)

### 오류 2: "SUPABASE_URL 형식이 올바르지 않습니다"
**해결**: URL이 `https://`로 시작하는지 확인

### 오류 3: "SUPABASE_ANON_KEY가 올바르지 않습니다"
**해결**: anon key가 충분히 긴지 확인 (보통 200자 이상)

### 오류 4: "st.secrets 접근 불가"
**해결**: Streamlit Cloud에서 앱을 완전히 재시작

## ✅ 성공 확인 방법

디버깅 모드에서 다음이 모두 녹색으로 표시되면 성공:
- ✅ st.secrets 접근 가능
- ✅ SUPABASE_URL 발견
- ✅ SUPABASE_ANON_KEY 발견
- ✅ Supabase 연결 성공!

## 📞 추가 도움이 필요한 경우

1. Supabase 프로젝트가 제대로 생성되었는지 확인
2. daily_works 테이블이 존재하는지 확인
3. Supabase 프로젝트가 일시중지되지 않았는지 확인

