-- daily_works 테이블에 샘플 데이터 추가
-- Notion의 데일리 실천 체험단 정보를 참고한 실용적인 데이터

INSERT INTO daily_works (title, category, link) VALUES

-- 핫딜 카테고리
('네이버 쇼핑 핫딜 특가', '핫딜', 'https://shopping.naver.com/hotdeal'),
('쿠팡 로켓배송 할인', '핫딜', 'https://www.coupang.com/np/campaigns'),
('11번가 슈퍼세일', '핫딜', 'https://www.11st.co.kr/browsing/MallSearch.tmall'),

-- 체험단 카테고리  
('미즈노 신발 체험단', '체험단', 'https://revu.co.kr'),
('올리브영 신제품 체험', '체험단', 'https://www.oliveyoung.co.kr/store/main/main.do'),
('네이버 카페 리뷰단', '체험단', 'https://cafe.naver.com'),

-- 재태크 카테고리
('토스 용돈벌이 이벤트', '재태크', 'https://toss.im/event'),
('카카오페이 적립 이벤트', '재태크', 'https://pay.kakao.com'),
('신한은행 적금 이벤트', '재태크', 'https://www.shinhan.com'),

-- 매일읽기 카테고리
('경향신문 무료구독', '매일읽기', 'https://www.khan.co.kr'),
('조선일보 디지털 구독', '매일읽기', 'https://www.chosun.com'),
('매일경제 무료체험', '매일읽기', 'https://www.mk.co.kr'),

-- 전시,문화 카테고리
('국립현대미술관 무료관람', '전시,문화', 'https://www.mmca.go.kr'),
('롯데콘서트홀 공연할인', '전시,문화', 'https://www.lotteconcerthall.com'),
('예술의전당 문화행사', '전시,문화', 'https://www.sac.or.kr'),

-- 방송 카테고리
('KBS 시청자 참여', '방송', 'https://www.kbs.co.kr'),
('MBC 프로그램 체험', '방송', 'https://www.imbc.com'),
('유튜브 크리에이터 지원', '방송', 'https://www.youtube.com'),

-- 시사회 카테고리
('CGV 시사회 이벤트', '시사회', 'https://www.cgv.co.kr'),
('메가박스 VIP 시사회', '시사회', 'https://www.megabox.co.kr'),
('롯데시네마 특별상영', '시사회', 'https://www.lottecinema.co.kr'),

-- 온라인 강의,공부 카테고리
('코세라 무료강의', '온라인 강의,공부', 'https://www.coursera.org'),
('인프런 개발자 강의', '온라인 강의,공부', 'https://www.inflearn.com'),
('패스트캠퍼스 할인', '온라인 강의,공부', 'https://www.fastcampus.co.kr'),

-- 세미나 카테고리
('구글 개발자 컨퍼런스', '세미나', 'https://developers.google.com'),
('네이버 DEVIEW', '세미나', 'https://deview.kr'),
('카카오 if 컨퍼런스', '세미나', 'https://if.kakao.com'),

-- 회사 혜택 카테고리
('삼성 임직원 할인', '회사 혜택', 'https://www.samsung.com'),
('LG 패밀리세일', '회사 혜택', 'https://www.lge.co.kr'),
('현대자동차 임직원 혜택', '회사 혜택', 'https://www.hyundai.com'),

-- 책관련 카테고리
('교보문고 북클럽', '책관련', 'https://www.kyobobook.co.kr'),
('YES24 독서모임', '책관련', 'https://www.yes24.com'),
('알라딘 중고서점', '책관련', 'https://www.aladin.co.kr'),

-- 웹진(무료) 카테고리
('브런치 스토리', '웹진(무료)', 'https://brunch.co.kr'),
('미디움 아티클', '웹진(무료)', 'https://medium.com'),
('네이버 포스트', '웹진(무료)', 'https://post.naver.com'),

-- 감성블로그 카테고리
('인스타그램 감성계정', '감성블로그', 'https://www.instagram.com'),
('티스토리 블로그', '감성블로그', 'https://www.tistory.com'),
('네이버 블로그', '감성블로그', 'https://section.blog.naver.com'),

-- 생활편의 카테고리
('배달의민족 할인쿠폰', '생활편의', 'https://www.baemin.com'),
('요기요 무료배달', '생활편의', 'https://www.yogiyo.co.kr'),
('마켓컬리 무료체험', '생활편의', 'https://www.kurly.com');

-- 데이터 확인
SELECT category, COUNT(*) as count 
FROM daily_works 
GROUP BY category 
ORDER BY count DESC;
