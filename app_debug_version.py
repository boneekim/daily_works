import streamlit as st
import pandas as pd
from datetime import datetime

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Daily Works - 데일리 실천 체험단",
    page_icon="📝",
    layout="wide"
)

# Secrets 디버깅
def debug_secrets():
    st.header("🔍 Secrets 디버깅")
    
    # Secrets 존재 여부 확인
    if hasattr(st, 'secrets'):
        st.success("✅ st.secrets 접근 가능")
        
        # 개별 키 확인
        try:
            url = st.secrets["SUPABASE_URL"]
            st.success(f"✅ SUPABASE_URL 발견: {url[:20]}...")
        except KeyError:
            st.error("❌ SUPABASE_URL이 Secrets에 없습니다")
        except Exception as e:
            st.error(f"❌ SUPABASE_URL 접근 오류: {e}")
        
        try:
            key = st.secrets["SUPABASE_ANON_KEY"]
            st.success(f"✅ SUPABASE_ANON_KEY 발견: {key[:20]}...")
        except KeyError:
            st.error("❌ SUPABASE_ANON_KEY가 Secrets에 없습니다")
        except Exception as e:
            st.error(f"❌ SUPABASE_ANON_KEY 접근 오류: {e}")
            
        # 전체 Secrets 구조 표시
        st.subheader("🔧 현재 Secrets 구조")
        try:
            secrets_dict = dict(st.secrets)
            for key in secrets_dict.keys():
                st.write(f"- {key}: {'설정됨' if secrets_dict[key] else '비어있음'}")
        except Exception as e:
            st.error(f"Secrets 구조 확인 실패: {e}")
    else:
        st.error("❌ st.secrets 접근 불가")

# Supabase 설정 (안전한 방식)
@st.cache_resource
def init_supabase():
    try:
        # Secrets 존재 여부 먼저 확인
        if not hasattr(st, 'secrets'):
            st.error("🚨 Streamlit Secrets에 접근할 수 없습니다.")
            return None
            
        # 각 키 개별 확인
        if "SUPABASE_URL" not in st.secrets:
            st.error("🚨 SUPABASE_URL이 Secrets에 설정되지 않았습니다.")
            st.info("💡 Streamlit Cloud → Settings → Secrets에서 SUPABASE_URL을 추가해주세요.")
            return None
            
        if "SUPABASE_ANON_KEY" not in st.secrets:
            st.error("🚨 SUPABASE_ANON_KEY가 Secrets에 설정되지 않았습니다.")
            st.info("💡 Streamlit Cloud → Settings → Secrets에서 SUPABASE_ANON_KEY를 추가해주세요.")
            return None
        
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        
        # 값 검증
        if not url or not url.startswith('https://'):
            st.error("🚨 SUPABASE_URL 형식이 올바르지 않습니다. https://로 시작해야 합니다.")
            return None
            
        if not key or len(key) < 100:  # Supabase anon key는 보통 매우 깁니다
            st.error("�� SUPABASE_ANON_KEY가 올바르지 않습니다.")
            return None
        
        # Supabase 클라이언트 생성
        from supabase import create_client
        supabase = create_client(url, key)
        
        st.success("✅ Supabase 연결 성공!")
        return supabase
        
    except ImportError:
        st.error("🚨 supabase 패키지를 가져올 수 없습니다. requirements.txt를 확인해주세요.")
        return None
    except Exception as e:
        st.error(f"🚨 Supabase 초기화 오류: {str(e)}")
        return None

# 카테고리 목록
CATEGORIES = [
    "핫딜", "체험단", "재태크", "매일읽기", "전시,문화", "방송", "시사회", 
    "온라인 강의,공부", "세미나", "회사 혜택", "책관련", "웹진(무료)", 
    "감성블로그", "생활편의"
]

def main():
    st.title("📝 Daily Works - 데일리 실천 체험단")
    
    # 디버깅 모드 토글
    debug_mode = st.checkbox("🔧 디버깅 모드", help="Secrets 설정 문제를 진단합니다")
    
    if debug_mode:
        debug_secrets()
        st.markdown("---")
    
    # Supabase 클라이언트 초기화
    supabase = init_supabase()
    
    if not supabase:
        st.stop()  # Supabase 연결 실패시 여기서 중단
    
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
                    # Supabase에 데이터 추가
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
                
                # 표시
                st.dataframe(df, use_container_width=True)
                
                # 링크를 클릭 가능한 형태로 별도 표시
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
        st.info("💡 데이터베이스 연결을 확인해주세요.")
    
    # 사이드바에 설정 가이드
    with st.sidebar:
        st.header("⚙️ 설정 가이드")
        
        st.subheader("1️⃣ Supabase 정보 확인")
        st.markdown("""
        1. https://supabase.com 접속
        2. 프로젝트 → Settings → API
        3. Project URL과 anon public key 복사
        """)
        
        st.subheader("2️⃣ Streamlit Secrets 설정")
        st.markdown("""
        1. https://share.streamlit.io 접속
        2. 앱 → ⚙️ → Settings → Secrets
        3. 다음 형식으로 입력:
        """)
        
        st.code('''SUPABASE_URL = "https://xxx.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGci..."''')
        
        st.subheader("3️⃣ 카테고리")
        for i, category in enumerate(CATEGORIES, 1):
            st.markdown(f"{i}. {category}")

if __name__ == "__main__":
    main()
