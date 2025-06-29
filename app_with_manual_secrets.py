import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Daily Works - 데일리 실천 체험단",
    page_icon="📝",
    layout="wide"
)

# 수동 Secrets 입력 방식 (임시 해결책)
def manual_supabase_setup():
    st.header("🔧 Supabase 연결 설정")
    st.info("Streamlit Cloud Secrets 설정이 작동하지 않는 경우 임시로 직접 입력할 수 있습니다.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        supabase_url = st.text_input(
            "Supabase URL", 
            placeholder="https://your-project-id.supabase.co",
            help="Supabase 프로젝트의 Project URL을 입력하세요"
        )
    
    with col2:
        supabase_key = st.text_input(
            "Supabase Anon Key", 
            type="password",
            placeholder="eyJhbGciOiJIUzI1NiIs...",
            help="Supabase 프로젝트의 anon public key를 입력하세요"
        )
    
    if supabase_url and supabase_key:
        try:
            supabase = create_client(supabase_url, supabase_key)
            # 연결 테스트
            response = supabase.table("daily_works").select("count", count="exact").execute()
            st.success("✅ Supabase 연결 성공!")
            return supabase
        except Exception as e:
            st.error(f"❌ 연결 실패: {str(e)}")
            return None
    else:
        st.warning("⚠️ URL과 Key를 모두 입력해주세요.")
        return None

# 일반 Supabase 설정 (Secrets 사용)
@st.cache_resource
def init_supabase():
    try:
        if hasattr(st, 'secrets') and "SUPABASE_URL" in st.secrets and "SUPABASE_ANON_KEY" in st.secrets:
            url = st.secrets["SUPABASE_URL"]
            key = st.secrets["SUPABASE_ANON_KEY"]
            return create_client(url, key)
        else:
            return None
    except Exception:
        return None

# 카테고리 목록
CATEGORIES = [
    "핫딜", "체험단", "재태크", "매일읽기", "전시,문화", "방송", "시사회", 
    "온라인 강의,공부", "세미나", "회사 혜택", "책관련", "웹진(무료)", 
    "감성블로그", "생활편의"
]

def main():
    st.title("📝 Daily Works - 데일리 실천 체험단")
    
    # 연결 방식 선택
    connection_mode = st.radio(
        "연결 방식 선택:",
        ["🔐 Secrets 사용 (권장)", "⚙️ 수동 입력 (임시)"],
        help="Streamlit Cloud Secrets가 작동하지 않으면 수동 입력을 선택하세요"
    )
    
    st.markdown("---")
    
    # Supabase 연결
    if connection_mode == "🔐 Secrets 사용 (권장)":
        supabase = init_supabase()
        if not supabase:
            st.error("🚨 Secrets에서 Supabase 설정을 찾을 수 없습니다.")
            st.info("💡 Streamlit Cloud → Settings → Secrets에서 SUPABASE_URL과 SUPABASE_ANON_KEY를 설정해주세요.")
            
            # Secrets 디버깅 정보
            with st.expander("🔍 Secrets 디버깅 정보"):
                if hasattr(st, 'secrets'):
                    st.write("✅ st.secrets 접근 가능")
                    secrets_keys = list(st.secrets.keys()) if hasattr(st.secrets, 'keys') else []
                    st.write(f"현재 Secrets 키들: {secrets_keys}")
                else:
                    st.write("❌ st.secrets 접근 불가")
            
            st.stop()
    else:
        supabase = manual_supabase_setup()
        if not supabase:
            st.stop()
    
    st.markdown("---")
    
    # 새 항목 추가 섹션
    st.header("✨ 새 항목 추가")
    
    with st.form("add_item_form"):
        col1, col2, col3 = st.columns([3, 2, 3])
        
        with col1:
            title = st.text_input("제목", placeholder="제목을 입력하세요")
        
        with col2:
            category = st.selectbox("종류", CATEGORIES)
        
        with col3:
            link = st.text_input("링크", placeholder="https://...")
        
        submitted = st.form_submit_button("추가하기", type="primary")
        
        if submitted:
            if title and category and link:
                try:
                    data = {
                        "title": title,
                        "category": category,
                        "link": link,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    result = supabase.table("daily_works").insert(data).execute()
                    
                    if result.data:
                        st.success("✅ 새 항목이 성공적으로 추가되었습니다!")
                        st.experimental_rerun()
                    else:
                        st.error("❌ 항목 추가에 실패했습니다.")
                        
                except Exception as e:
                    st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                    if "RLS" in str(e) or "permission" in str(e).lower():
                        st.info("💡 RLS 문제일 수 있습니다. Supabase에서 'ALTER TABLE daily_works DISABLE ROW LEVEL SECURITY;' 실행해보세요.")
            else:
                st.error("❌ 모든 필드를 입력해주세요.")
    
    st.markdown("---")
    
    # 기존 항목 목록 표시
    st.header("📋 데일리 실천 체험단 목록")
    
    try:
        # 카테고리 필터
        col1, col2 = st.columns([2, 6])
        
        with col1:
            selected_categories = st.multiselect(
                "카테고리 필터",
                CATEGORIES,
                default=CATEGORIES
            )
        
        with col2:
            search_term = st.text_input("검색", placeholder="제목으로 검색...")
        
        # Supabase에서 데이터 조회
        response = supabase.table("daily_works").select("*").order("created_at", desc=True).execute()
        
        if response.data:
            # 데이터 필터링
            filtered_data = []
            for item in response.data:
                if item['category'] in selected_categories:
                    if not search_term or search_term.lower() in item['title'].lower():
                        filtered_data.append(item)
            
            if filtered_data:
                # 데이터를 표 형태로 표시
                df_display = []
                for item in filtered_data:
                    created_date = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
                    
                    df_display.append({
                        "제목": item['title'],
                        "종류": item['category'],
                        "링크": item['link'],
                        "등록일": created_date
                    })
                
                df = pd.DataFrame(df_display)
                st.dataframe(df, use_container_width=True)
                
                # 링크 목록
                st.subheader("🔗 링크 목록")
                for item in filtered_data:
                    col1, col2, col3 = st.columns([3, 2, 1])
                    with col1:
                        st.write(f"**{item['title']}**")
                    with col2:
                        st.write(item['category'])
                    with col3:
                        st.link_button("이동", item['link'])
                
                st.info(f"📊 총 {len(filtered_data)}개의 항목이 있습니다.")
                
            else:
                st.info("🔍 필터 조건에 맞는 항목이 없습니다.")
                
        else:
            st.info("📝 아직 등록된 항목이 없습니다. 첫 번째 항목을 추가해보세요!")
            
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
        if "RLS" in str(e) or "permission" in str(e).lower():
            st.info("💡 RLS 문제일 수 있습니다. Supabase에서 'ALTER TABLE daily_works DISABLE ROW LEVEL SECURITY;' 실행해보세요.")
    
    # 사이드바에 가이드
    with st.sidebar:
        st.header("ℹ️ 설정 가이드")
        
        if connection_mode == "⚙️ 수동 입력 (임시)":
            st.subheader("📍 Supabase 정보 찾기")
            st.markdown("""
            1. https://supabase.com 접속
            2. 프로젝트 → Settings → API
            3. Project URL과 anon public key 복사
            """)
        
        st.subheader("📋 카테고리")
        for i, category in enumerate(CATEGORIES, 1):
            st.markdown(f"{i}. {category}")

if __name__ == "__main__":
    main()
