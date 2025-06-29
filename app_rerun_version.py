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

# 테이블 구조 자동 설정
def setup_table_structure(supabase):
    """테이블 구조를 확인하고 필요시 생성/수정"""
    try:
        # 테이블 존재 여부 및 구조 확인
        try:
            response = supabase.table("daily_works").select("*").limit(1).execute()
            # 테이블이 존재하고 접근 가능하면 성공
            return True
        except Exception as e:
            if "does not exist" in str(e) or "relation" in str(e) or "PGRST" in str(e):
                st.warning("🔧 테이블 구조에 문제가 있어 자동으로 수정합니다...")
                
                # 테이블 재생성 시도
                st.info("📋 올바른 테이블 구조로 재생성하고 있습니다...")
                
                with st.expander("🛠️ 테이블 수정 과정 (자동)"):
                    st.code("""
-- daily_works 테이블 재생성
DROP TABLE IF EXISTS daily_works;

CREATE TABLE daily_works (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    link TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

ALTER TABLE daily_works DISABLE ROW LEVEL SECURITY;
                    """)
                    
                st.error("❌ 테이블 구조 문제가 감지되었습니다!")
                st.markdown("""
                **📋 해결 방법:**
                1. **Supabase SQL Editor** 접속: https://supabase.com → 프로젝트 → SQL Editor
                2. 다음 명령어들을 **순서대로** 실행:
                
                ```sql
                -- 1. 기존 테이블 삭제
                DROP TABLE IF EXISTS daily_works;
                
                -- 2. 올바른 구조로 재생성
                CREATE TABLE daily_works (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    link TEXT NOT NULL,
                    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
                );
                
                -- 3. RLS 비활성화
                ALTER TABLE daily_works DISABLE ROW LEVEL SECURITY;
                
                -- 4. 테스트 데이터 추가
                INSERT INTO daily_works (title, category, link) 
                VALUES ('테스트 항목', '핫딜', 'https://example.com');
                ```
                
                3. **완료 후 이 페이지를 새로고침**하세요!
                """)
                
                return False
            else:
                st.error(f"알 수 없는 오류: {str(e)}")
                return False
                
    except Exception as e:
        st.error(f"테이블 설정 중 오류: {str(e)}")
        return False

# 샘플 데이터 자동 로드 기능
def load_sample_data(supabase):
    """데이터베이스가 비어있을 때 샘플 데이터를 자동으로 추가"""
    
    sample_data = [
        # 핫딜
        ("네이버 쇼핑 핫딜 특가", "핫딜", "https://shopping.naver.com/hotdeal"),
        ("쿠팡 로켓배송 할인", "핫딜", "https://www.coupang.com/np/campaigns"),
        ("11번가 슈퍼세일", "핫딜", "https://www.11st.co.kr/browsing/MallSearch.tmall"),
        
        # 체험단
        ("미즈노 신발 체험단", "체험단", "https://revu.co.kr"),
        ("올리브영 신제품 체험", "체험단", "https://www.oliveyoung.co.kr/store/main/main.do"),
        ("네이버 카페 리뷰단", "체험단", "https://cafe.naver.com"),
        
        # 재태크
        ("토스 용돈벌이 이벤트", "재태크", "https://toss.im/event"),
        ("카카오페이 적립 이벤트", "재태크", "https://pay.kakao.com"),
        ("신한은행 적금 이벤트", "재태크", "https://www.shinhan.com"),
        
        # 매일읽기
        ("경향신문 무료구독", "매일읽기", "https://www.khan.co.kr"),
        ("조선일보 디지털 구독", "매일읽기", "https://www.chosun.com"),
        ("매일경제 무료체험", "매일읽기", "https://www.mk.co.kr"),
        
        # 전시,문화
        ("국립현대미술관 무료관람", "전시,문화", "https://www.mmca.go.kr"),
        ("롯데콘서트홀 공연할인", "전시,문화", "https://www.lotteconcerthall.com"),
        ("예술의전당 문화행사", "전시,문화", "https://www.sac.or.kr"),
        
        # 방송
        ("KBS 시청자 참여", "방송", "https://www.kbs.co.kr"),
        ("MBC 프로그램 체험", "방송", "https://www.imbc.com"),
        ("유튜브 크리에이터 지원", "방송", "https://www.youtube.com"),
        
        # 시사회
        ("CGV 시사회 이벤트", "시사회", "https://www.cgv.co.kr"),
        ("메가박스 VIP 시사회", "시사회", "https://www.megabox.co.kr"),
        ("롯데시네마 특별상영", "시사회", "https://www.lottecinema.co.kr"),
        
        # 온라인 강의,공부
        ("코세라 무료강의", "온라인 강의,공부", "https://www.coursera.org"),
        ("인프런 개발자 강의", "온라인 강의,공부", "https://www.inflearn.com"),
        ("패스트캠퍼스 할인", "온라인 강의,공부", "https://www.fastcampus.co.kr"),
        
        # 세미나
        ("구글 개발자 컨퍼런스", "세미나", "https://developers.google.com"),
        ("네이버 DEVIEW", "세미나", "https://deview.kr"),
        ("카카오 if 컨퍼런스", "세미나", "https://if.kakao.com"),
        
        # 회사 혜택
        ("삼성 임직원 할인", "회사 혜택", "https://www.samsung.com"),
        ("LG 패밀리세일", "회사 혜택", "https://www.lge.co.kr"),
        ("현대자동차 임직원 혜택", "회사 혜택", "https://www.hyundai.com"),
        
        # 책관련
        ("교보문고 북클럽", "책관련", "https://www.kyobobook.co.kr"),
        ("YES24 독서모임", "책관련", "https://www.yes24.com"),
        ("알라딘 중고서점", "책관련", "https://www.aladin.co.kr"),
        
        # 웹진(무료)
        ("브런치 스토리", "웹진(무료)", "https://brunch.co.kr"),
        ("미디움 아티클", "웹진(무료)", "https://medium.com"),
        ("네이버 포스트", "웹진(무료)", "https://post.naver.com"),
        
        # 감성블로그
        ("인스타그램 감성계정", "감성블로그", "https://www.instagram.com"),
        ("티스토리 블로그", "감성블로그", "https://www.tistory.com"),
        ("네이버 블로그", "감성블로그", "https://section.blog.naver.com"),
        
        # 생활편의
        ("배달의민족 할인쿠폰", "생활편의", "https://www.baemin.com"),
        ("요기요 무료배달", "생활편의", "https://www.yogiyo.co.kr"),
        ("마켓컬리 무료체험", "생활편의", "https://www.kurly.com"),
    ]
    
    try:
        # 기존 데이터 확인
        existing = supabase.table("daily_works").select("id").limit(1).execute()
        
        if not existing.data:  # 데이터가 없으면 샘플 데이터 추가
            st.info("🎁 데이터베이스가 비어있어서 샘플 데이터를 추가하고 있습니다...")
            
            # 샘플 데이터 배치 입력
            for title, category, link in sample_data:
                data = {
                    "title": title,
                    "category": category,
                    "link": link,
                    "created_at": datetime.now().isoformat()
                }
                supabase.table("daily_works").insert(data).execute()
            
            st.success(f"✅ {len(sample_data)}개의 샘플 데이터가 추가되었습니다!")
            # Streamlit 최신 버전용 rerun 사용
            if hasattr(st, 'rerun'):
                st.rerun()
            else:
                st.experimental_rerun()
            
    except Exception as e:
        st.warning(f"⚠️ 샘플 데이터 추가 중 오류: {str(e)}")
        if "category" in str(e) or "PGRST204" in str(e):
            st.error("❌ 테이블 구조에 'category' 컬럼이 없습니다!")
            st.markdown("**해결 방법**: 위의 테이블 수정 SQL을 Supabase에서 실행해주세요.")

# 수동 Secrets 입력 방식
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
            # 연결 테스트 및 테이블 구조 확인
            if setup_table_structure(supabase):
                st.success("✅ Supabase 연결 및 테이블 구조 확인 완료!")
                return supabase
            else:
                return None
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
            supabase = create_client(url, key)
            
            # 테이블 구조 확인
            if setup_table_structure(supabase):
                return supabase
            else:
                return None
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
    st.markdown("*Notion의 데일리 실천 체험단 정보를 바탕으로 한 관리 시스템*")
    
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
            st.error("🚨 Secrets에서 Supabase 설정을 찾을 수 없거나 테이블 구조에 문제가 있습니다.")
            st.info("💡 Streamlit Cloud → Settings → Secrets에서 SUPABASE_URL과 SUPABASE_ANON_KEY를 설정하거나, 위의 테이블 수정 SQL을 실행해주세요.")
            st.stop()
    else:
        supabase = manual_supabase_setup()
        if not supabase:
            st.stop()
    
    # 샘플 데이터 자동 로드 (데이터베이스가 비어있고 테이블 구조가 올바를 때)
    load_sample_data(supabase)
    
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
                        # Streamlit 최신 버전 호환성
                        if hasattr(st, 'rerun'):
                            st.rerun()
                        else:
                            st.experimental_rerun()
                    else:
                        st.error("❌ 항목 추가에 실패했습니다.")
                        
                except Exception as e:
                    st.error(f"❌ 오류가 발생했습니다: {str(e)}")
                    if "category" in str(e) or "PGRST204" in str(e):
                        st.markdown("**💡 해결 방법**: 위의 테이블 수정 SQL을 Supabase에서 실행해주세요.")
            else:
                st.error("❌ 모든 필드를 입력해주세요.")
    
    st.markdown("---")
    
    # 기존 항목 목록 표시
    st.header("📋 데일리 실천 체험단 목록")
    
    try:
        # 필터 섹션
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
                # 카테고리별 통계
                category_stats = {}
                for item in filtered_data:
                    cat = item['category']
                    category_stats[cat] = category_stats.get(cat, 0) + 1
                
                # 통계 표시
                st.subheader("📊 카테고리별 현황")
                cols = st.columns(5)
                for i, (cat, count) in enumerate(sorted(category_stats.items())):
                    with cols[i % 5]:
                        st.metric(cat, count)
                
                st.markdown("---")
                
                # 데이터를 표 형태로 표시
                df_display = []
                for item in filtered_data:
                    created_date = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00')).strftime('%Y-%m-%d')
                    
                    df_display.append({
                        "제목": item['title'],
                        "종류": item['category'],
                        "등록일": created_date
                    })
                
                df = pd.DataFrame(df_display)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                # 링크 목록
                st.subheader("🔗 바로가기 링크")
                
                # 카테고리별로 그룹화해서 표시
                for category in CATEGORIES:
                    items_in_category = [item for item in filtered_data if item['category'] == category]
                    if items_in_category:
                        with st.expander(f"📂 {category} ({len(items_in_category)}개)"):
                            for item in items_in_category:
                                col1, col2 = st.columns([5, 1])
                                with col1:
                                    st.write(f"**{item['title']}**")
                                with col2:
                                    st.link_button("이동", item['link'], use_container_width=True)
                
                st.info(f"📊 총 {len(filtered_data)}개의 항목이 있습니다.")
                
            else:
                st.info("🔍 필터 조건에 맞는 항목이 없습니다.")
                
        else:
            st.info("📝 데이터베이스가 비어있습니다. 샘플 데이터를 추가하고 있습니다...")
            
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
        if "category" in str(e) or "PGRST204" in str(e):
            st.markdown("**💡 해결 방법**: 위의 테이블 수정 SQL을 Supabase에서 실행해주세요.")
    
    # 사이드바에 가이드
    with st.sidebar:
        st.header("ℹ️ 사용 가이드")
        
        st.subheader("🎯 주요 기능")
        st.markdown("""
        - **자동 테이블 생성**: 구조 문제 자동 감지 및 안내
        - **자동 샘플 데이터**: 첫 실행시 42개의 실용적인 데이터 추가
        - **카테고리별 관리**: 15개 카테고리로 체계적 분류
        - **검색 및 필터**: 원하는 정보 빠르게 찾기
        """)
        
        if connection_mode == "⚙️ 수동 입력 (임시)":
            st.subheader("📍 Supabase 정보 찾기")
            st.markdown("""
            1. https://supabase.com 접속
            2. 프로젝트 → Settings → API
            3. Project URL과 anon public key 복사
            """)
        
        st.subheader("�� 카테고리 목록")
        for i, category in enumerate(CATEGORIES, 1):
            st.markdown(f"{i}. {category}")

if __name__ == "__main__":
    main()
