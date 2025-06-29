# Supabase 연결 테스트 스크립트
# 로컬에서 연결을 테스트해볼 수 있습니다

import streamlit as st
from supabase import create_client, Client

st.title("🔗 Supabase 연결 테스트")

# 수동으로 URL과 Key 입력
st.header("1️⃣ Supabase 정보 입력")
supabase_url = st.text_input("Supabase URL", placeholder="https://xxxxxxxxxxx.supabase.co")
supabase_key = st.text_input("Supabase Anon Key", type="password")

if st.button("연결 테스트"):
    if supabase_url and supabase_key:
        try:
            # Supabase 클라이언트 생성
            supabase = create_client(supabase_url, supabase_key)
            
            # 테이블 조회 테스트
            response = supabase.table("daily_works").select("*").limit(1).execute()
            
            st.success("✅ Supabase 연결 성공!")
            st.write("📊 테이블 구조:", response)
            
            # Secrets 형식 출력
            st.header("2️⃣ Streamlit Cloud Secrets에 입력할 내용")
            st.code(f'''SUPABASE_URL = "{supabase_url}"
SUPABASE_ANON_KEY = "{supabase_key}"''')
            
        except Exception as e:
            st.error(f"❌ 연결 실패: {str(e)}")
            st.info("💡 URL과 Key를 다시 확인해주세요.")
    else:
        st.warning("⚠️ URL과 Key를 모두 입력해주세요.")

st.markdown("---")
st.header("3️⃣ Supabase 정보 찾는 방법")
st.markdown("""
1. **https://supabase.com** 접속
2. 프로젝트 선택
3. **Settings** → **API** 클릭
4. **Project URL**과 **anon public** key 복사
""")
