import streamlit as st
import pandas as pd
from supabase import create_client, Client
from datetime import datetime, date

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Daily Works - 데일리 실천 체험단",
    page_icon="📝",
    layout="wide"
)

# Supabase 설정
@st.cache_resource
def init_supabase():
    url = st.secrets.get("SUPABASE_URL", "")
    key = st.secrets.get("SUPABASE_ANON_KEY", "")
    if not url or not key:
        st.error("Supabase 설정이 필요합니다. .streamlit/secrets.toml 파일을 확인해주세요.")
        return None
    return create_client(url, key)

# 카테고리 목록
CATEGORIES = [
    "핫딜", "체험단", "재태크", "매일읽기", "전시,문화", "방송", "시사회", 
    "온라인 강의,공부", "세미나", "회사 혜택", "책관련", "웹진(무료)", 
    "감성블로그", "생활편의"
]

# 우선순위 옵션
PRIORITY_OPTIONS = {
    1: "🔴 높음",
    2: "🟡 보통", 
    3: "🟢 낮음"
}

def main():
    st.title("📝 Daily Works - 데일리 실천 체험단")
    st.markdown("---")
    
    # Supabase 클라이언트 초기화
    supabase = init_supabase()
    if not supabase:
        return
    
    # 새 항목 추가 섹션
    st.header("✨ 새 항목 추가")
    
    with st.form("add_item_form"):
        # 기본 정보
        col1, col2 = st.columns([2, 1])
        with col1:
            title = st.text_input("제목", placeholder="제목을 입력하세요")
        with col2:
            category = st.selectbox("종류", CATEGORIES)
        
        # 링크와 설명
        col1, col2 = st.columns([2, 1])
        with col1:
            link = st.text_input("링크", placeholder="https://...")
        with col2:
            priority = st.selectbox("우선순위", options=[1, 2, 3], 
                                  format_func=lambda x: PRIORITY_OPTIONS[x], 
                                  index=1)
        
        # 설명과 옵션
        description = st.text_area("설명 (선택사항)", placeholder="간단한 설명을 입력하세요...")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            is_favorite = st.checkbox("⭐ 즐겨찾기")
        with col2:
            has_expiry = st.checkbox("📅 만료일 설정")
        with col3:
            source = st.selectbox("출처", ["manual", "instagram", "email", "website", "notion", "기타"])
        
        # 만료일 설정
        expiry_date = None
        if has_expiry:
            expiry_date = st.date_input("만료일", min_value=date.today())
        
        # 태그 입력
        tags_input = st.text_input("태그 (쉼표로 구분)", placeholder="예: 할인, 무료, 체험")
        
        submitted = st.form_submit_button("추가하기", type="primary")
        
        if submitted:
            if title and category and link:
                try:
                    # 태그 처리
                    tags = []
                    if tags_input:
                        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
                    
                    # Supabase에 데이터 추가
                    data = {
                        "title": title,
                        "category": category,
                        "link": link,
                        "description": description,
                        "priority": priority,
                        "is_favorite": is_favorite,
                        "source": source,
                        "tags": tags,
                        "created_at": datetime.now().isoformat()
                    }
                    
                    if expiry_date:
                        data["expiry_date"] = expiry_date.isoformat()
                    
                    result = supabase.table("daily_works").insert(data).execute()
                    
                    if result.data:
                        st.success("✅ 새 항목이 성공적으로 추가되었습니다!")
                        st.rerun()
                    else:
                        st.error("❌ 항목 추가에 실패했습니다.")
                        
                except Exception as e:
                    st.error(f"❌ 오류가 발생했습니다: {str(e)}")
            else:
                st.error("❌ 제목, 카테고리, 링크는 필수 입력 항목입니다.")
    
    st.markdown("---")
    
    # 기존 항목 목록 표시
    st.header("📋 데일리 실천 체험단 목록")
    
    try:
        # 필터 옵션
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            selected_categories = st.multiselect(
                "카테고리 필터",
                CATEGORIES,
                default=CATEGORIES
            )
        
        with col2:
            priority_filter = st.multiselect(
                "우선순위 필터",
                options=[1, 2, 3],
                format_func=lambda x: PRIORITY_OPTIONS[x],
                default=[1, 2, 3]
            )
        
        with col3:
            status_filter = st.selectbox(
                "상태 필터",
                ["전체", "활성", "비활성", "만료됨"],
                index=0
            )
        
        with col4:
            show_favorites = st.checkbox("⭐ 즐겨찾기만")
        
        # 검색
        search_term = st.text_input("🔍 검색", placeholder="제목이나 설명으로 검색...")
        
        # Supabase에서 데이터 조회
        query = supabase.table("daily_works").select("*")
        
        # 상태 필터 적용
        if status_filter != "전체":
            status_map = {"활성": "active", "비활성": "inactive", "만료됨": "expired"}
            query = query.eq("status", status_map[status_filter])
        
        response = query.order("created_at", desc=True).execute()
        
        if response.data:
            # 데이터 필터링
            filtered_data = []
            for item in response.data:
                # 카테고리 필터
                if item['category'] not in selected_categories:
                    continue
                
                # 우선순위 필터
                if item.get('priority', 2) not in priority_filter:
                    continue
                
                # 즐겨찾기 필터
                if show_favorites and not item.get('is_favorite', False):
                    continue
                
                # 검색 필터
                if search_term:
                    search_text = f"{item['title']} {item.get('description', '')}".lower()
                    if search_term.lower() not in search_text:
                        continue
                
                filtered_data.append(item)
            
            if filtered_data:
                # 데이터를 표 형태로 표시
                df_display = []
                for item in filtered_data:
                    priority_icon = "🔴" if item.get('priority', 2) == 1 else "🟡" if item.get('priority', 2) == 2 else "🟢"
                    favorite_icon = "⭐" if item.get('is_favorite', False) else ""
                    
                    # 만료일 체크
                    expiry_text = ""
                    if item.get('expiry_date'):
                        expiry = datetime.fromisoformat(item['expiry_date']).date()
                        if expiry < date.today():
                            expiry_text = f"❌ 만료됨 ({expiry})"
                        elif expiry <= date.today() + pd.Timedelta(days=7):
                            expiry_text = f"⚠️ 곧 만료 ({expiry})"
                        else:
                            expiry_text = f"📅 {expiry}"
                    
                    df_display.append({
                        "제목": f"{favorite_icon}{priority_icon} [{item['title']}]({item['link']})",
                        "종류": item['category'],
                        "설명": item.get('description', '')[:50] + ('...' if len(item.get('description', '')) > 50 else ''),
                        "만료일": expiry_text,
                        "조회수": item.get('view_count', 0),
                        "등록일": datetime.fromisoformat(item['created_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d'),
                        "출처": item.get('source', 'manual')
                    })
                
                df = pd.DataFrame(df_display)
                
                # 표시할 컬럼 선택
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "제목": st.column_config.LinkColumn(
                            "제목",
                            help="클릭하면 해당 사이트로 이동합니다",
                            display_text=".*"
                        ),
                        "종류": st.column_config.TextColumn("종류", width="medium"),
                        "설명": st.column_config.TextColumn("설명", width="large"),
                        "만료일": st.column_config.TextColumn("만료일", width="medium"),
                        "조회수": st.column_config.NumberColumn("조회수", width="small"),
                        "등록일": st.column_config.DateColumn("등록일", width="medium"),
                        "출처": st.column_config.TextColumn("출처", width="small")
                    }
                )
                
                st.info(f"📊 총 {len(filtered_data)}개의 항목이 있습니다.")
                
            else:
                st.info("🔍 필터 조건에 맞는 항목이 없습니다.")
                
        else:
            st.info("📝 아직 등록된 항목이 없습니다. 첫 번째 항목을 추가해보세요!")
            
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
    
    # 사이드바에 정보 표시
    with st.sidebar:
        st.header("ℹ️ 앱 정보")
        st.markdown("""
        **Daily Works**는 데일리 실천 체험단 정보를 관리하는 앱입니다.
        
        **새로운 기능:**
        - 🔴🟡🟢 우선순위 설정
        - ⭐ 즐겨찾기 기능
        - 📝 상세 설명 추가
        - 📅 만료일 관리
        - 🏷️ 태그 시스템
        - 📊 조회수 추적
        - 📍 출처 관리
        """)
        
        st.markdown("**카테고리:**")
        for i, category in enumerate(CATEGORIES, 1):
            st.markdown(f"{i}. {category}")

if __name__ == "__main__":
    main()
