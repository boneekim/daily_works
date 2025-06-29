-- 노션의 실제 데이터로 데이터베이스 교체
-- Supabase SQL Editor에서 실행하세요

-- 1단계: 기존 데이터 모두 삭제
DELETE FROM daily_works;

-- 2단계: AUTO INCREMENT 리셋
ALTER SEQUENCE daily_works_id_seq RESTART WITH 1;

-- 3단계: 노션의 실제 데이터 삽입
INSERT INTO daily_works (title, category, link) VALUES
('네이버 핫딜 (생필품)', '핫딜', 'https://section.cafe.naver.com/ca-fe/home/feed?t=1735122787699'),
('책', '체험단', 'http://www.10x10.co.kr/culturestation/'),
('좌담회, 설문 엠브래인', '재태크', 'https://www.panel.co.kr/user/main');

-- 4단계: 삽입 결과 확인
SELECT * FROM daily_works ORDER BY id;

-- 5단계: 카테고리별 개수 확인
SELECT category, COUNT(*) as count 
FROM daily_works 
GROUP BY category 
ORDER BY count DESC;
